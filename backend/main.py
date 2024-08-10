import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Constants
SELECTED_FEATURES = ['genres', 'keywords', 'tagline', 'cast', 'director']
CSV_FILE_PATH = os.path.join('backend', 'movies.csv')
NUM_RECOMMENDATIONS = 10

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to load and preprocess the movie data
def load_and_preprocess_data(csv_file):
    movies_data = pd.read_csv(csv_file)
    
    # Fill missing values and combine features
    for feature in SELECTED_FEATURES:
        movies_data[feature] = movies_data[feature].fillna('')
    
    movies_data['combined_features'] = movies_data[SELECTED_FEATURES].apply(
        lambda row: ' '.join(row), axis=1
    )
    
    return movies_data

# Function to create TF-IDF feature vectors
def create_feature_vectors(movies_data):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(movies_data['combined_features'])

# Function to find the closest movie title match
def find_closest_match(movie_name, movie_titles):
    matches = difflib.get_close_matches(movie_name, movie_titles)
    return matches[0] if matches else None

# Function to get movie recommendations based on similarity scores
def get_recommendations(movies_data, similarity, movie_name, num_recommendations=NUM_RECOMMENDATIONS):
    movie_titles = movies_data['title'].tolist()
    close_match = find_closest_match(movie_name, movie_titles)
    
    if close_match is None:
        return {"error": f"No close matches found for the movie: {movie_name}"}
    
    index_of_movie = movies_data[movies_data.title == close_match].index[0]
    similarity_scores = list(enumerate(similarity[index_of_movie]))
    sorted_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    return [movies_data.loc[index, 'title'] for index, score in sorted_movies[:num_recommendations]]

# API endpoint for movie recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    movie_name = data.get('movie_name')
    recommended_movies = get_recommendations(movies_data, similarity, movie_name)
    
    if "error" in recommended_movies:
        return jsonify({"error": recommended_movies["error"]}), 400
    
    return jsonify({'recommendations': recommended_movies})

# Main function to load data and start the Flask app
if __name__ == "__main__":
    # Load and preprocess the data
    movies_data = load_and_preprocess_data(CSV_FILE_PATH)
    
    # Generate feature vectors and compute similarity
    feature_vectors = create_feature_vectors(movies_data)
    similarity = cosine_similarity(feature_vectors)
    
    # Run Flask app
    app.run(debug=True, port=5000)
