# Movie Recommendation System Using Plot Summaries

A movie recommendation system that uses Natural Language Processing (NLP) to analyze plot summaries and suggest similar movies based on user preferences.

## Overview

This project allows users to input a brief description of a movie they like or their preferences, and the system uses advanced NLP techniques to analyze movie plot summaries to provide recommendations with similar themes, genres, or plot structures.

## Features

- **Content-Based Recommendation**: Uses TF-IDF vectorization to analyze movie plots and find similarities
- **User-Friendly Interface**: Clean, responsive UI built with Bootstrap
- **Semantic Understanding**: Considers the actual content of movies rather than just ratings
- **Real-Time Processing**: Processes user queries instantly to provide immediate recommendations

## Technologies Used

### Frontend
- HTML/CSS
- Bootstrap 5
- JavaScript
- Font Awesome

### Backend
- Python Flask
- SQLAlchemy
- scikit-learn (for TF-IDF vectorization)
- NLTK (for text processing)
- SQLite (database)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Download NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

5. Run the application:
```bash
python main.py
```

6. Open your browser and navigate to:
```
https://f09bea8e-0a06-4fd1-9ea6-40179fae1d96-00-39gjanf2l7utx.janeway.replit.dev/
```

## How It Works

1. **Data Preparation**: Movie plot summaries are processed by removing stop words, tokenizing, and vectorizing the text
2. **TF-IDF Transformation**: The system uses Term Frequency-Inverse Document Frequency (TF-IDF) to convert text into numerical vectors
3. **Similarity Calculation**: When a user inputs preferences, the system calculates the cosine similarity between the input and all movie plots
4. **Ranking**: Movies are ranked by similarity score, and the top matches are presented as recommendations

## Project Structure

```
movie-recommendation-system/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── data/
│       └── movies.csv
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── recommendations.html
│   ├── about.html
│   ├── movie_details.html
│   ├── 404.html
│   └── 500.html
├── app.py
├── main.py
├── models.py
├── movie_recommender.py
├── routes.py
├── utils.py
├── requirements.txt
└── README.md
```

## Screenshots

<!-- Add screenshots of your application here -->

## Future Enhancements

- Implement user authentication and personal recommendation history
- Add more movie data and expand the database
- Implement advanced NLP models like BERT or Sentence-BERT for better semantic understanding
- Add movie posters and external links to more information
- Integrate with external movie databases like TMDB or OMDB

## Team Members

- DUDANI JIYA – KU2407U400
- SHREY PATEL – KU2407U431
- KRISHNA LATHIYA – KU2407U421

## License

This project is licensed under the MIT License - see the LICENSE file for details.
