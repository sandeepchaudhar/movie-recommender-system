import streamlit as st
import pandas as pd
import pickle
import requests

# === PAGE CONFIG ===
st.set_page_config(page_title="🎥 Movie Recommender", layout="wide")

# === GLOBAL STYLE ===
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #f0f2f6, #ffffff);
    }
    .recommendation-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.07);
        transition: all 0.3s ease-in-out;
        text-align: center;
        margin-bottom: 30px;
        height: 100%;
    }
    .recommendation-card:hover {
        box-shadow: 0 12px 36px rgba(0,0,0,0.12);
        transform: scale(1.03);
    }
    .movie-title {
        font-size: 17px;
        font-weight: 600;
        color: #222222;
        margin-top: 12px;
        line-height: 1.4;
    }
    .movie-section {
        margin-top: 40px;
    }
    .title-center {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #222;
        margin-bottom: 10px;
    }
    hr {
        border: 0;
        height: 1px;
        background: #ddd;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# === POSTER FETCH ===
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=5e72e0f509c71c6a59e2dc08c3f996c6&language=en-US'
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/300x450.png?text=Poster+Not+Found"
    data = response.json()
    path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500{path}" if path else "https://via.placeholder.com/300x450.png?text=No+Image"

# === RECOMMENDER LOGIC ===
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_names = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters

# === LOAD DATA ===
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# === TITLE ===
st.markdown("<div class='title-center'>🎬 Movie Recommender System</div><hr>", unsafe_allow_html=True)

# === SELECT BOX ===
selected_movie_name = st.selectbox("🎞️ Choose a movie you like:", movies['title'].values)

# === RECOMMEND BUTTON ===
if st.button("✨ Recommend"):
    names, posters = recommend(selected_movie_name)

    st.markdown("<div class='movie-section'>", unsafe_allow_html=True)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)
            st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
