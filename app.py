import streamlit as st
import pickle
import os
import pandas as pd
import requests

# Check if the pickle files exist
if not os.path.exists("movies_list.pkl") or not os.path.exists("similarity.pkl"):
    # Generate the pickle files dynamically
    movies = pd.read_csv("top10K-TMDB-movies.csv")  # Ensure this file is included in your deployment
    similarity = ...  # Add logic to compute the similarity matrix

    # Save the generated data as pickle files
    pickle.dump(movies, open("movies_list.pkl", 'wb'))
    pickle.dump(similarity, open("similarity.pkl", 'wb'))
else:
    # Load the pickle files if they already exist
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))

movies_list = movies['title'].values

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for better UI
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        .stSelectbox label {
            font-size: 18px;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .movie-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: nowrap;
            overflow-x: auto;
            padding-top: 20px;
        }
        .movie-item {
            text-align: center;
            width: 180px;
        }
        .movie-item img {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()

st.header("🎥 Movie Recommender System")

selectvalue = st.selectbox("Select a movie from the dropdown", movies_list)

def fetch_poster(movie_title):
    """Fetch the movie poster URL using the OMDB API."""
    api_url = f"http://www.omdbapi.com/?t={movie_title}&apikey=745b3d5b"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")
    return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    """Recommend movies based on similarity."""
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    for i in distance[1:6]:
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie

if st.button("Show Recommendations"):
    recommended_movies = recommend(selectvalue)
    st.write("### Recommended Movies:")
    
    # HTML for displaying images in a row
    st.markdown('<div class="movie-container">', unsafe_allow_html=True)
    
    movie_items = "".join(
        [
            f"""
            <div class="movie-item">
                <img src="{fetch_poster(movie_name)}" alt="{movie_name}">
                <p>{movie_name}</p>
            </div>
            """
            for movie_name in recommended_movies
        ]
    )
    
    st.markdown(movie_items, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
