import os
import csv
import numpy as np
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import Movie
from app import db, app
from sqlalchemy import text

# Logger setup
logger = logging.getLogger(__name__)

# Global variables
tfidf_vectorizer = None
tfidf_matrix = None
movie_ids = None

def init_recommender():
    """Initialize the movie recommender by loading data and building the TF-IDF model."""
    global tfidf_vectorizer, tfidf_matrix, movie_ids
    
    # Check if we already have movies in the database
    movie_count = Movie.query.count()
    
    if movie_count == 0:
        logger.info("No movies found in database. Loading from CSV file...")
        load_movies_from_csv()
    
    # Get all movies from the database
    movies = Movie.query.all()
    
    if not movies:
        logger.error("No movies available in the database!")
        return
    
    # Extract plot summaries and movie IDs
    plots = [movie.plot for movie in movies]
    movie_ids = [movie.id for movie in movies]
    
    # Create and fit TF-IDF vectorizer
    logger.info("Building TF-IDF model...")
    tfidf_vectorizer = TfidfVectorizer(
        min_df=2,
        max_df=0.95,
        max_features=8000,
        stop_words='english'
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(plots)
    logger.info(f"TF-IDF model built with {tfidf_matrix.shape[0]} movies and {tfidf_matrix.shape[1]} features.")

def reload_movie_data():
    """Drop all existing movies and reload from CSV."""
    try:
        # Delete all existing movies
        Movie.query.delete()
        db.session.commit()
        logger.info("All existing movies deleted from database")
        
        # Load fresh data from CSV
        load_movies_from_csv()
        
        # Reinitialize the recommender
        global tfidf_vectorizer, tfidf_matrix, movie_ids
        tfidf_vectorizer = None
        tfidf_matrix = None
        movie_ids = None
        
        # Get all movies from the database
        movies = Movie.query.all()
        
        if not movies:
            logger.error("Failed to reload movies!")
            return False
        
        # Extract plot summaries and movie IDs
        plots = [movie.plot for movie in movies]
        movie_ids = [movie.id for movie in movies]
        
        # Create and fit TF-IDF vectorizer
        logger.info("Rebuilding TF-IDF model...")
        tfidf_vectorizer = TfidfVectorizer(
            min_df=2,
            max_df=0.95,
            max_features=8000,
            stop_words='english'
        )
        
        tfidf_matrix = tfidf_vectorizer.fit_transform(plots)
        logger.info(f"TF-IDF model rebuilt with {tfidf_matrix.shape[0]} movies and {tfidf_matrix.shape[1]} features.")
        return True
        
    except Exception as e:
        logger.error(f"Error reloading movie data: {str(e)}")
        return False

def load_movies_from_csv():
    """Load movie data from the CSV file into the database."""
    csv_path = os.path.join(app.root_path, 'static', 'data', 'movies.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            
            # Batch insert for better performance
            batch_size = 100
            batch = []
            
            for row in csv_reader:
                movie = Movie(
                    title=row.get('title', ''),
                    year=int(row.get('year', 0)) if row.get('year', '').isdigit() else None,
                    genre=row.get('genre', ''),
                    plot=row.get('plot', '')
                )
                batch.append(movie)
                
                if len(batch) >= batch_size:
                    db.session.add_all(batch)
                    db.session.commit()
                    batch = []
            
            # Add any remaining movies
            if batch:
                db.session.add_all(batch)
                db.session.commit()
                
            logger.info(f"Successfully loaded movie data from {csv_path}")
    except Exception as e:
        logger.error(f"Error loading movies from CSV: {str(e)}")
        # Add some default movies if CSV loading fails
        add_default_movies()

def add_default_movies():
    """Add a few default movies to the database if CSV loading fails."""
    default_movies = [
        Movie(
            title="The Shawshank Redemption",
            year=1994,
            genre="Drama",
            plot="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
        ),
        Movie(
            title="The Godfather",
            year=1972,
            genre="Crime, Drama",
            plot="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
        ),
        Movie(
            title="The Dark Knight",
            year=2008,
            genre="Action, Crime, Drama",
            plot="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
        ),
        Movie(
            title="Inception",
            year=2010,
            genre="Action, Adventure, Sci-Fi",
            plot="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
        ),
        Movie(
            title="Pulp Fiction",
            year=1994,
            genre="Crime, Drama",
            plot="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
        ),
    ]
    
    db.session.add_all(default_movies)
    db.session.commit()
    logger.info("Added default movies to the database")

def get_recommendations(query_text, num_recommendations=5):
    """Get movie recommendations based on the query text."""
    global tfidf_vectorizer, tfidf_matrix, movie_ids
    
    if tfidf_vectorizer is None or tfidf_matrix is None or movie_ids is None:
        logger.warning("Recommender not initialized. Initializing now...")
        init_recommender()
        
        if tfidf_vectorizer is None or tfidf_matrix is None or movie_ids is None:
            logger.error("Failed to initialize recommender!")
            return []
    
    # Extract genre preferences from the query if they exist
    genre_weight = 0.3  # How much to weight genre matches vs text similarity
    genre_preferences = []
    
    # Common genres to look for in the query
    common_genres = [
        "Action", "Adventure", "Animation", "Biography", "Comedy", 
        "Crime", "Documentary", "Drama", "Family", "Fantasy", 
        "Horror", "History", "Music", "Musical", "Mystery", 
        "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"
    ]
    
    query_lower = query_text.lower()
    
    # Check for explicit genre requests
    for genre in common_genres:
        if genre.lower() in query_lower:
            genre_preferences.append(genre)
    
    # Also check for some common genre descriptions
    genre_descriptions = {
        "scary": "Horror",
        "frightening": "Horror",
        "terrifying": "Horror",
        "spooky": "Horror",
        "funny": "Comedy",
        "hilarious": "Comedy",
        "laugh": "Comedy",
        "romantic": "Romance",
        "love story": "Romance",
        "space": "Sci-Fi",
        "superhero": "Action",
        "historical": "History",
        "cartoon": "Animation",
        "animated": "Animation",
        "kid": "Family",
        "children": "Family",
        "detective": "Mystery",
        "mystery": "Mystery",
        "whodunit": "Mystery",
        "thriller": "Thriller",
        "suspense": "Thriller",
        "exciting": "Action",
        "violent": "Action",
        "battle": "Action",
        "war": "War",
        "western": "Western",
        "cowboy": "Western",
        "documentary": "Documentary",
        "musical": "Musical",
        "singing": "Musical",
        "sport": "Sport",
        "emotional": "Drama",
        "dramatic": "Drama",
    }
    
    for desc, genre in genre_descriptions.items():
        if desc in query_lower and genre not in genre_preferences:
            genre_preferences.append(genre)
    
    logger.info(f"Detected genre preferences: {genre_preferences}")
    
    # Transform the query text using the fitted vectorizer
    query_vector = tfidf_vectorizer.transform([query_text])
    
    # Calculate cosine similarity between the query and all movies
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # Adjust similarity based on genre preferences if any were detected
    if genre_preferences:
        # Get all movies
        all_movies = Movie.query.all()
        
        # Create a dictionary to map movie_id to its index in the cosine_similarities array
        id_to_position = {movie_id: i for i, movie_id in enumerate(movie_ids)}
        
        # Boost scores for movies that match the genre preferences
        for movie in all_movies:
            if movie.id in id_to_position:
                movie_genres = movie.genre.split(", ")
                # Check if any of the movie's genres match the preferences
                matching_genres = [g for g in genre_preferences if g in movie_genres]
                if matching_genres:
                    # Boost the similarity score based on number of matching genres
                    position = id_to_position[movie.id]
                    boost = genre_weight * len(matching_genres) / len(genre_preferences)
                    cosine_similarities[position] += boost
    
    # Get indices of top similar movies
    similar_movie_indices = cosine_similarities.argsort()[:-num_recommendations-1:-1]
    
    # Get the movie IDs for these indices
    recommended_movie_ids = [movie_ids[i] for i in similar_movie_indices]
    
    # Retrieve movie details from the database
    recommended_movies = Movie.query.filter(Movie.id.in_(recommended_movie_ids)).all()
    
    # Get similarity scores for logging and debugging
    movie_scores = [(movie_id, cosine_similarities[i]) for i, movie_id in enumerate(movie_ids) if movie_id in recommended_movie_ids]
    movie_scores.sort(key=lambda x: x[1], reverse=True)
    logger.debug(f"Recommendation scores: {movie_scores}")
    
    # Sort the result in the same order as the recommendations
    id_to_index = {movie_id: index for index, movie_id in enumerate(recommended_movie_ids)}
    recommended_movies.sort(key=lambda movie: id_to_index[movie.id])
    
    return recommended_movies
