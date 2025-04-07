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
    if movie not in movies['title'].values:
        return []
    index = movies[movies['title'] == movie].index[0]
    if index >= len(similarity):
        return []
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    for i in distance[1:11]:  # Increased to potentially show more movies
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie

if st.button("Show Recommendations"):
    recommended_movies = recommend(selectvalue)
    st.write("### Recommended Movies:")

    max_cols = 5
    first_row = recommended_movies[:5]
    second_row = recommended_movies[5:]

    # Show first 5 movies
    cols = st.columns(max_cols)
    for i, movie_name in enumerate(first_row):
        with cols[i]:
            poster_url = fetch_poster(movie_name)
            st.image(poster_url, caption=movie_name, width=150)

    # Show the next row if there are more movies
    if second_row:
        st.markdown("### People also like these movies:")
        cols = st.columns(len(second_row))  # create just enough columns
        for i, movie_name in enumerate(second_row):
            with cols[i]:
                poster_url = fetch_poster(movie_name)
                st.image(poster_url, caption=movie_name, width=150)
