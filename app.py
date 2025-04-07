import streamlit as st
import pickle
import os
import pandas as pd
import requests
import urllib.parse
import time

# Load or generate data
if not os.path.exists("movies_list.pkl") or not os.path.exists("similarity.pkl"):
    movies = pd.read_csv("top10K-TMDB-movies.csv")
    similarity = ...  # Add logic here
    pickle.dump(movies, open("movies_list.pkl", 'wb'))
    pickle.dump(similarity, open("similarity.pkl", 'wb'))
else:
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))

movies_list = movies['title'].values

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Inject CSS + JavaScript
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }

        .floating-bg {
            position: fixed;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: radial-gradient(circle, #1e1e1e, #0f0f0f);
            overflow: hidden;
        }
        .bubble {
            position: absolute;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 10s infinite ease-in-out;
        }
        @keyframes float {
            0% { transform: translateY(100vh) scale(0.5); opacity: 0; }
            100% { transform: translateY(-10vh) scale(1.2); opacity: 0.7; }
        }

        .header-box {
            border: 2px solid #f5c518;
            border-radius: 10px;
            padding: 15px 25px;
            background: #202020;
            color: white;
            margin-bottom: 20px;
            box-shadow: 0 0 12px rgba(245,197,24, 0.3);
        }

        .imdb-link {
            display: inline-block;
            margin-top: 5px;
            font-size: 14px;
            background: #f5c518;
            padding: 5px 10px;
            border-radius: 5px;
            color: black;
            text-decoration: none;
            font-weight: 600;
        }
        .imdb-link:hover {
            background: #ffe072;
        }
    </style>

    <div id="bgAnimation" class="floating-bg">
        <div class="bubble" style="left: 10%; animation-delay: 0s;"></div>
        <div class="bubble" style="left: 25%; animation-delay: 2s;"></div>
        <div class="bubble" style="left: 40%; animation-delay: 4s;"></div>
        <div class="bubble" style="left: 60%; animation-delay: 1s;"></div>
        <div class="bubble" style="left: 80%; animation-delay: 3s;"></div>
    </div>

    <script>
        function hideBackground() {
            const bg = window.parent.document.getElementById('bgAnimation');
            if (bg) {
                bg.style.display = 'none';
            }
        }
    </script>
""", unsafe_allow_html=True)

# Header with styled box
st.markdown("<div class='header-box'><h1>🎥 Welcome to OBD's Cinema</h1></div>", unsafe_allow_html=True)
st.markdown("<h4 style='font-size:20px; font-weight:600;'>🎬 Get a similar movie that you just finished</h4>", unsafe_allow_html=True)
selectvalue = st.selectbox("", movies_list)

# Helpers
def fetch_poster(movie_title):
    api_url = f"http://www.omdbapi.com/?t={urllib.parse.quote(movie_title)}&apikey=745b3d5b"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")
    return "https://via.placeholder.com/300x450?text=No+Image"

def imdb_link(movie_title):
    query = urllib.parse.quote(movie_title)
    return f"https://www.imdb.com/find?q={query}&s=tt"

def recommend(movie):
    if movie not in movies['title'].values:
        return []
    index = movies[movies['title'] == movie].index[0]
    if index >= len(similarity):
        return []
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    return [movies.iloc[i[0]].title for i in distance[1:11]]

# Show Recommendations
if st.button("Show Recommendations"):
    # Hide background animation
    st.markdown("<script>hideBackground()</script>", unsafe_allow_html=True)

    with st.spinner("🍿 Finding your next favorite movies..."):
        time.sleep(2)  # simulate loading

        recommended_movies = recommend(selectvalue)

        st.markdown("### 🎯 Recommended Movies Just For You")
        first_row = recommended_movies[:5]
        second_row = recommended_movies[5:]
        max_cols = 5

        cols = st.columns(max_cols)
        for i, movie_name in enumerate(first_row):
            with cols[i]:
                st.image(fetch_poster(movie_name), caption=movie_name, width=160)
                st.markdown(f"<a class='imdb-link' href='{imdb_link(movie_name)}' target='_blank'>View on IMDb</a>", unsafe_allow_html=True)

        if second_row:
            st.markdown("### 🍿 People also liked:")
            cols = st.columns(len(second_row))
            for i, movie_name in enumerate(second_row):
                with cols[i]:
                    st.image(fetch_poster(movie_name), caption=movie_name, width=160)
                    st.markdown(f"<a class='imdb-link' href='{imdb_link(movie_name)}' target='_blank'>View on IMDb</a>", unsafe_allow_html=True)
