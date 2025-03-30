import streamlit as st
import pickle

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    for i in distance[1:6]:
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie

if st.button("Show Recommend"):
    movie_name = recommend(selectvalue)
    st.write("Recommended Movies:")
    for name in movie_name:
        st.write(name)