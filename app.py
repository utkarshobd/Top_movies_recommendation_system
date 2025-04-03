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
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .movie-poster {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
    .movie-item {
        text-align: center;
        margin: 10px;
    }
    .movie-item img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    st.markdown('<div class="movie-poster">', unsafe_allow_html=True)
    for movie_name in recommended_movies:
        poster_url = fetch_poster(movie_name)
        st.markdown(
            f"""
            <div class="movie-item">
                <img src="{poster_url}" alt="{movie_name}" width="200">
                <p>{movie_name}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)