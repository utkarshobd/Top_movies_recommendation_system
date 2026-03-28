# Top Movies Recommendation System

🚀 **Live Demo:** [Click here to try the app](https://utkarshobd-top-movies-recommendation-system-app-1nku2r.streamlit.app/)

---

## Overview

A content-based movie recommender web app built with Python and Streamlit. Select any movie from a list of 10,000 TMDB movies and get 10 similar recommendations instantly, complete with posters and IMDb links.

---

## How It Works (ML Pipeline)

1. **Dataset** — `top10K-TMDB-movies.csv` contains 10,000 movies from TMDB with fields: `id`, `title`, `genre`, `overview`, `popularity`, `vote_average`, etc.

2. **Feature Engineering** — Only `title`, `overview`, and `genre` are kept. A `tags` column is created by concatenating `overview + genre` for each movie, giving a text blob that captures both plot and genre.

3. **Vectorization** — `CountVectorizer` (max 10,000 features, English stop words removed) converts the `tags` text into a word-frequency matrix of shape `(10000, 10000)`.

4. **Similarity** — `cosine_similarity` is computed across all movie vectors, producing a 10,000×10,000 similarity matrix.

5. **Serialization** — The processed movie list and similarity matrix are saved as `movies_list.pkl` and `similarity.pkl` for fast loading in the app.

---

## The Web App

- User picks a movie from a dropdown (all 10K titles)
- Clicks **"Show Recommendations"**
- The app finds the movie's index, sorts all other movies by cosine similarity, and returns the top 10
- Results are shown in two rows of 5, each with:
  - Movie poster fetched from the **OMDB API**
  - A direct **IMDb search link**
- UI has a dark cinema theme with animated floating bubbles, gold borders, and IMDb-style yellow buttons

---

## Project Structure

| File | Purpose |
|---|---|
| `Main.ipynb` | Data processing + model training |
| `app.py` | Streamlit web app |
| `movies_list.pkl` | Serialized movie dataframe |
| `similarity.pkl` | Precomputed cosine similarity matrix (generated at runtime) |
| `top10K-TMDB-movies.csv` | Raw dataset |
| `requirements.txt` | Python dependencies |
| `Procfile` | For deployment (gunicorn) |

---

## Tech Stack

- **Python** — Core language
- **Pandas** — Data processing
- **Scikit-learn** — CountVectorizer + Cosine Similarity
- **Streamlit** — Web app framework
- **OMDB API** — Movie poster fetching
- **Pickle** — Model serialization

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
