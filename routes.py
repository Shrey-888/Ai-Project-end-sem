from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import Movie, UserQuery
from movie_recommender import get_recommendations, reload_movie_data
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/search', methods=['POST'])
def search():
    """Process the user's movie preference query and display recommendations"""
    query_text = request.form.get('query', '')
    
    if not query_text:
        flash('Please enter your movie preferences or a brief description.', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Save the query to the database
        user_query = UserQuery(query_text=query_text)
        db.session.add(user_query)
        db.session.commit()
        
        # Get movie recommendations
        recommendations = get_recommendations(query_text, num_recommendations=6)
        
        if not recommendations:
            flash('No movie recommendations found. Please try a different description.', 'info')
            return redirect(url_for('index'))
        
        return render_template('recommendations.html', 
                              query=query_text, 
                              recommendations=recommendations)
    
    except Exception as e:
        logger.error(f"Error processing search request: {str(e)}")
        flash('An error occurred while processing your request. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    """Display details for a specific movie"""
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_details.html', movie=movie)

@app.route('/admin/reload-movies', methods=['GET'])
def admin_reload_movies():
    """Admin route to reload all movie data"""
    try:
        success = reload_movie_data()
        if success:
            movie_count = Movie.query.count()
            return jsonify({
                'success': True,
                'message': f'Successfully reloaded movie data. {movie_count} movies now in database.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to reload movie data. Check server logs for details.'
            }), 500
    except Exception as e:
        logger.error(f"Error reloading movie data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/admin/stats')
def admin_stats():
    """Admin route to show database statistics"""
    movie_count = Movie.query.count()
    query_count = UserQuery.query.count()
    
    return render_template('admin_stats.html', 
                          movie_count=movie_count,
                          query_count=query_count)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(e)}")
    return render_template('500.html'), 500
