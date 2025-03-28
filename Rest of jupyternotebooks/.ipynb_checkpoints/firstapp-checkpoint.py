import streamlit as st
import pandas as pd
from PIL import Image
import base64
import numpy as np
import requests
import datetime
#Background
@st.cache
def load_image(path):
    with open(path, ‘rb’) as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded
def image_tag(path):
    encoded = load_image(path)
    tag = f’<img src=“data:image/png;base64,{encoded}“>'
    return tag
def background_image_style(path):
    encoded = load_image(path)
    style = f’‘'
    <style>
    .stApp {{
        background-image: url(“data:image/png;base64,{encoded}“);
        background-size: cover;
    }}
    </style>
    ‘’'
    return style
image_path = ‘images/b.jpeg’
image_link = ‘https://www.google.com/search?q=background+black+&tbm=isch&ved=2ahUKEwiZkbSs9r30AhWSDGMBHfUmBJYQ2-cCegQIABAA&oq=background+black+&gs_lcp=CgNpbWcQAzIHCCMQ7wMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoGCAAQCBAeUOQKWKgUYLoWaABwAHgAgAFiiAHdBJIBAjEwmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=tvakYZneKZKZjLsP9c2QsAk&bih=630&biw=1433&hl=en#imgrc=45B6kmexcKSPFM’
st.write(background_image_style(image_path), unsafe_allow_html=True)
# Side bar
make_choice = st.sidebar.selectbox(‘Pages:’,
                                   [‘New Movies’, ‘Create Your Own Movie’])
# First Page - New Movies Prediction
if make_choice == ‘New Movies’:
    ‘’'
    # CinePred :movie_camera:
    ‘’'
    ‘’'
    ## The Website Predicting The Next Blockbusters
    ‘’'
    #Background image
    image_bat = Image.open(‘images/Batman22.jpg’)
    image_Jur = Image.open(‘images/Jurassic.jpeg’)
    image_wil = Image.open(‘images/williams.jpeg’)
    col1, col2, col3 = st.columns(3)
    col1.image(image_bat,
               caption=‘The Batman - April 2022’,
               use_column_width=“auto”,
               width=10)
    col2.image(image_Jur,
               caption=‘Jurassic World: Dominion - June 2022’,
               use_column_width=“auto”)
    col3.image(image_wil,
               caption=‘King Richard - December 2021’,
               use_column_width=“auto”)
    ‘’'
    # Choose a movie going out soon :popcorn:
    ‘’'
    up_movies = st.selectbox(‘Select an upcoming movie’, [
        “The Batman”, “Jurassic World: Dominion”, “Spiderman: No Way home”,
        “King Richard”
    ])
    #title = st.text_input(‘Movie title’, ‘Enter upcoming movie’)
    st.write(f’Our revenue prediction for {up_movies} is:’)
    param = {“title”: up_movies}
    #prediction
    if st.button(‘Revenue Prediction’):
        res = requests.get(url=‘https://cinepred-g4p6tgs7da-ew.a.run.app/predict')#, params=param)
        pred = res.json()
        col1, col2 = st.columns(2)
        col1.title(f”${np.round(pred/1_000_000,2)} Millions”)
        col1.write(‘’'
                 **Actors**: Tom Holland, Zendaya, Jamie Foxx, Benedict Cumberbatch, Alfred Molina\n
                 **Director**: Jon Watts\n
                 **Production**: Company: Columbia Picture\n
                 **Budget**: $180 Millions\n
                 **Duration** : 2h30\n
                 **Genre** : Adventures, Action, Sci-Fi\n
                 **Release Date**: December 17th 2021
                 ‘’'
                 )
        image_spider = Image.open(‘images/Spiderman.jpeg’)
        col2.image(image_spider,
                     caption=‘Spiderman: No Way Home’,
                     width=280)
    #Side bar Image
    image_spider = Image.open(‘images/gru.jpeg’)
    st.sidebar.image(image_spider,
                     caption=‘Minions:The Rise of Gru’,
                     width=300)
# Second Page - Create your movie
if make_choice == ‘Create Your Own Movie’:
    ‘’'
    # Create your own movie :film_frames:
    ‘’'
    #Background Image
    image_roc = Image.open(‘images/Rocky.jpg’)
    image_sta = Image.open(‘images/Star.jpeg’)
    image_jum = Image.open(‘images/jumanji.jpeg’)
    col1, col2, col3 = st.columns(3)
    col1.image(image_roc, caption=‘Rocky IV’, use_column_width=“auto”)
    col2.image(image_sta,
               caption=‘Star Wars: The Force Awakens’,
               use_column_width=“auto”)
    col3.image(image_jum, caption=‘Jumanji’, use_column_width=“auto”)
    def get_select_box_data():
        return pd.DataFrame({
            ‘director’: [
                “Steven Spielberg”, “Martin Scorsese”, “Quentin Tarantino”,
                “James Cameron”, “Spike Lee”, “Alfred Hitchcock”,
                “Francis Ford Coppola”, “George Lucas”, “Steven Soderbergh”,
                “Ridley Scott”, “Oliver Stone”, “Clint Eastwood”
            ],
            ‘writer’: [
                “Aaron Sorkin”,
                “Woody Allen”,“Luc Besson”,“John Hughes”,“Spike Lee”,
                “William Shakespeare”, “Christopher Nolan”,
                “Tim Burton”,“John Hughes”,“Steven Knight”,“Mike Leigh”,
                “John Sayles”
            ],
            ‘Prod’: [
                “Walt Disney Pictures”, “DreamWorks”, “Lionsgate”,
                “Universal Pictures”, “Warner Bros”, “Fox 2000 Pictures”,
                “Gaumont”, “Columbia Pictures”, “Paramount Pictures”,
                “Metro Goldwyn Mayer”, “Miramax”, “Hollywood Pictures”
            ],
            ‘main_actor’: [
                “Brad Pitt”, “Leonardo DiCaprio”, “Johnny Depp”,
                “Robert Downey Jr.“, “Will Smith”, “Robert De Niro”,
                “Dwayne Johnson”, “Harrison Ford”, “Tom Cruise”,
                “Jean-Claude Van Damme”, “Bruce Willis”, “Daniel Craig”
            ],
            ‘second_actor’: [
                “Jean Dujardin”, “Franck Dubosc”, “Angelina Jolie”,
                “Arnold Schwarzenegger”, “Denzel Washington”, “Vin Diesel”,
                “Cameron Diaz”, “George Clooney”, “Mark Wahlberg”,
                “Jamel Debbouze”, “Jason Statham”, “Benoît Poelvoorde”
            ],
            ‘third_actor’: [
                “Mel Gibson”, “François Damiens”, “Adam Sandler”,
                “Julia Roberts”, “Alec Baldwin”, “Christian Bale”,
                “Christian Clavier”, “Jack Nicholson”, “Joaquin Phoenix”,
                “Natalie Portman”, “Hugh Jackman”, “Penélope Cruz”
            ],
            ‘Genres’: [
                “Drama”, “Action”, “Comedy”, “Horror”, “Thriller”, “Romance”,
                “Animation”, “Adventure”, “Comedy”, “Drama, Romance”, “Family”,
                “Action, Thriller”
            ]
        })
    df = get_select_box_data()
    year = 2022
    director = st.selectbox(‘Select a Director’, df[‘director’])
    filtered_dir = df[df[‘director’] == director]
    writer = st.selectbox(‘Select a Writer’, df[‘writer’])
    filtered_w = df[df[‘writer’] == writer]
    production_company = st.selectbox(‘Select a Production Company’,
                                      df[‘Prod’])
    filtered_pd = df[df[‘Prod’] == production_company]
    main_actor = st.selectbox(‘Select a Main Actor’, df[‘main_actor’])
    filtered_ma = df[df[‘main_actor’] == main_actor]
    second_actor = st.selectbox(‘Select a Second Actor’, df[‘second_actor’])
    filtered_sa = df[df[‘second_actor’] == second_actor]
    third_actor = st.selectbox(‘Select a Third Actor’, df[‘third_actor’])
    filtered_sa = df[df[‘third_actor’] == third_actor]
    budget = st.slider(“Select your Budget (in millions)“,value = 10.0,
                       min_value=1.0,
                       max_value=250.0,
                       step=1.0)
    duration = st.slider(“Select the duration of your movie (in minutes)“,
                         value = 90,
                         min_value=60,
                         max_value=180,
                         step=5)
    genre = st.selectbox(‘Select a movie genre’, df[‘Genres’])
    filtered_cou = df[df[‘Genres’] == genre]
    date_published = st.date_input(“When do you want to publish your movie ?“,
                                   value=datetime.date(2022, 1, 1),
                                   min_value=datetime.date(2022, 1, 1),
                                   max_value=datetime.date(2022, 12, 31))
    st.write(
        f”Our revenue prediction for your **{genre}** movie directed by **{director}**, written by **{writer}**, produced by **{production_company}**, with **{main_actor}**, **{second_actor}** and **{third_actor}**, for a budget of **${budget}**millions, for a duration of **{duration}** minutes, going out on **{date_published}**, is :”
    )
    if st.button(‘Revenue Prediction’):
        parameters = {
            ‘director’: director,
            ‘writer’: writer,
            ‘production_company’: production_company,
            ‘main_actor’: main_actor,
            ‘second_actor’: second_actor,
            ‘third_actor’: third_actor,
            ‘genre’: genre,
            ‘duration’: duration,
            ‘year’: year,
            ‘budget’: budget,
            ‘date_published’: date_published
            #‘Sin’: np.sin(2 * np.pi * months / 12),
            #‘Cos’: np.cos(2 * np.pi * months / 12)
        }
        response = requests.get(
            url=‘https://cinepred-g4p6tgs7da-ew.a.run.app/test?’,
            params=parameters)
        pred = response.json()
        st.title(f”${np.round(pred[‘income’]/1_000_000,2)} Millions”)
    #Side bar Image
    image_avenger = Image.open(‘images/Avengers.jpeg’)
    st.sidebar.image(image_avenger,
                     caption=‘Avengers - End Game’,
                     use_column_width=“auto”)