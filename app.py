import streamlit as st
import pickle
import pandas as pd
import requests
import os
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
Authorization = os.getenv("AUTHORIZATION")

# Global session for efficiency
session = requests.Session()
session.headers.update({
    "accept": "application/json",
    "Authorization": f"Bearer {Authorization}"
})

# Load movies list (pandas DataFrame)
movies_list = pickle.load(open('./models/movies.pkl', 'rb'))  # 40 MB

# Load similarity matrix efficiently
def load_similarity():
    """Load similarity matrix from pickle (proper format)."""
    with open('./models/similarity_np_array.pkl', 'rb') as f:
        return pickle.load(f)


similarity = load_similarity()  # Avoid loading entire matrix into RAM

def fetch_poster(movie_id, cache={}):
    """Fetch movie poster URL from TMDB API with caching"""
    # return None
    if movie_id in cache:
        return cache[movie_id]  # Use cached poster

    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = session.get(url)

    if response.status_code != 200:
        return None

    poster_path = response.json().get('poster_path', '')
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    cache[movie_id] = poster_url  # Store in cache
    return poster_url

def recommend(movie):
    """Return top 5 recommended movies & posters"""
    # Load similarity only when needed
    similarity = load_similarity()

    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Use argpartition for efficient sorting
    top_indices = np.argpartition(distances, -6)[-6:]
    top_indices = top_indices[np.argsort(distances[top_indices])][::-1][1:6]

    recommended_movies = movies_list.iloc[top_indices]['title'].tolist()
    recommended_movies_posters = [fetch_poster(movies_list.iloc[i].id) for i in top_indices]

    # ✅ Free memory after use
    del similarity  

    return recommended_movies, recommended_movies_posters

# Streamlit UI
st.title('Movie Recommender System 🎬')
st.write('Enter a movie you like, and we will suggest similar movies!')

option = st.selectbox('Select a movie:', movies_list['title'].values)

if st.button('Recommend'):
    st.write(f'### Recommendations for **{option}**:')
    names, posters = recommend(option)
    # st.text('hi')

    # Streamlit column layout for recommendations
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"**{names[idx]}**")
            if posters[idx]:
                st.image(posters[idx])
    del names, posters