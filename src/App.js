import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

function App() {
    const [movieName, setMovieName] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState('');

    const getRecommendations = async () => {
        try {
            setError('');
            const response = await axios.post('https://mlh-movie-recmndr.onrender.com/recommend', {  // Updated URL
                movie_name: movieName
            });
            setRecommendations(response.data.recommendations);
        } catch (error) {
            setError('No recommendations found. Please try another movie.');
            setRecommendations([]);
        }
    };

    return (
        <div className="App">
            <h1>Movie Recommender</h1>
            <div className="input-container">
                <input 
                    type="text" 
                    value={movieName} 
                    onChange={(e) => setMovieName(e.target.value)} 
                    placeholder="Enter your favorite movie" 
                    className="input-box"
                />
                <button onClick={getRecommendations} className="recommend-button">Get Recommendations</button>
            </div>
            {error && <p className="error-message">{error}</p>}
            <div className="recommendations">
                {recommendations.length > 0 && <h2>Recommended Movies:</h2>}
                <div className="recommendation-cards">
                    {recommendations.map((movie, index) => (
                        <div key={index} className="movie-card">
                            <p>{movie}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
