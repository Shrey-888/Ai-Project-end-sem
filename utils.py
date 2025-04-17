import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

logger = logging.getLogger(__name__)

# Download NLTK resources if needed
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('punkt')
        nltk.download('stopwords')
    except Exception as e:
        logger.warning(f"Failed to download NLTK resources: {str(e)}")

def preprocess_text(text):
    """
    Preprocess text for NLP analysis:
    - Convert to lowercase
    - Remove special characters
    - Remove stopwords
    - Tokenize
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    
    try:
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        
        # Join tokens back into text
        preprocessed_text = ' '.join(filtered_tokens)
        return preprocessed_text
    except Exception as e:
        logger.warning(f"Error in text preprocessing: {str(e)}")
        # Return original text with basic cleaning if NLTK processing fails
        return ' '.join(text.split())

def truncate_text(text, max_length=200):
    """Truncate text to a maximum length and add ellipsis if needed."""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    # Find the last space before max_length
    last_space = text[:max_length].rfind(' ')
    if last_space > 0:
        return text[:last_space] + "..."
    else:
        return text[:max_length] + "..."
