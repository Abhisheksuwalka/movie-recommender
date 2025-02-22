import streamlit as st
import pickle
import pandas as pd
import requests
import time
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

api_key = os.getenv("API_KEY")
Authorization = os.getenv("AUTHORIZATION")


session = requests.Session()
session.headers.update({
    "accept": "application/json",
    "Authorization": f"Bearer {Authorization}"
})

# def fetch_poster(movie_id):
#     # return None
#     session = requests.Session()
#     session.headers.update({
#         "accept": "application/json",
#         "Authorization": f"Bearer {Authorization}"
#     })
    
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
#     response = session.get(url)
    
#     if response.status_code != 200:
#         return None
#     response_json = response.json()
#     # print(response_json)
#     poster_path = response_json.get('poster_path', '')
    
#     if poster_path:
#         poster_link = "https://image.tmdb.org/t/p/w500" + poster_path
#         return poster_link
#     else:
#         return None

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = session.get(url)

    if response.status_code != 200:
        return None

    poster_path = response.json().get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

movies_list = pickle.load(open('./models/movies.pkl', 'rb')) # pandas.core.frame.DataFrame

# similarity = pickle.load(open('./models/similarity_np_array.pkl', 'rb')) # numpy.ndarray
# Load similarity matrix in a memory-efficient way
def load_similarity():
    return np.memmap('./models/similarity_np_array.pkl', dtype='float32', mode='r')

# Load only when needed
similarity = load_similarity()

# def recommend(movie):
#     movie_index = movies_list[movies_list[ 'title'] == movie] .index[0]
#     distances = similarity[movie_index]
    
#     sorted_movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])
#     sorted_movies_list = sorted_movies_list[1:6]
    
#     recommended_movies = []
#     recommended_movies_posters = []
    
        
#     for i in sorted_movies_list:
#         movie_id = movies_list.iloc[i[0]].id
         
#         recommended_movies.append(movies_list.iloc[i[0]]['title'])
#         # fetch poster from API
#         recommended_movies_posters.append(fetch_poster(movie_id))
#         # wait_time = 0.5
#         # time.sleep(wait_time)
    
#     return recommended_movies, recommended_movies_posters

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Use argpartition to find top 5 recommendations efficiently
    top_indices = np.argpartition(distances, -6)[-6:]
    top_indices = top_indices[np.argsort(distances[top_indices])][::-1][1:6]

    recommended_movies = movies_list.iloc[top_indices]['title'].tolist()
    recommended_movies_posters = [fetch_poster(movies_list.iloc[i].id) for i in top_indices]

    return recommended_movies, recommended_movies_posters


##  # # # # # # # # # # # #  App


st.title('Movie Recommender System')
st.write('Welcome to the Movie Recommender System! Please enter the name of a movie you like and we will recommend you some similar movies.')


option = st.selectbox(
    'Select a movie:',
    movies_list['title'].values
    )

if st.button('Recommend'):
    session.close()
    
    st.write('You selected:', option)
    st.write('Here are some recommendations for you:')
    names, posters = recommend(option)
    # posters is a list of ["https://image.tmdb.org/t/p/w500/lpxDrACKJhbbGOlwVMNz5YCj6SI.jpg"]
    
    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     st.text(names[0])
    #     # add poster
    #     if(posters[0] != None):
    #         st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     # add poster
    #     if(posters[1] != None):
    #         st.image(posters[1])
    # with col3:
    #     st.text(names[2])
    #     # add poster
    #     if(posters[2] != None):
    #         st.image(posters[2])

    # with col4:
    #     st.text(names[3])
    #     # add poster
    #     if(posters[3] != None):
    #         st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     # add poster
    #     if(posters[4] != None):
    #         st.image(posters[4])
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"**{names[idx]}**")
            if posters[idx]:
                st.image(posters[idx])
