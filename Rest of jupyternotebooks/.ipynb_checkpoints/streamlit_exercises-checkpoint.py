# Note that Streamlit is a rather large library. 
    # I will mainly focus the start on text elements, displaying data, charts and custom filters. 
    # This is mainly to help you get going and dig deeper on your own. 

# Important notes. 
    # 1. Make sure that you have opened your Terminal. Go to the top and choose Terminal -> New Terminal
    # 2. If you installed the custom Kernel, then Choose it from below in the right. 

# Exercises.

# 2.1. Let's first of all import all the necessary dependencies to start with our Exercises. 
    # Here you are looking to import streamlit, pandas and numpy.




# 2.2. Run streamlit in your terminal. 
    # The command you want to run in your terminal is -> streamlit run filename.py




# 2.3 - Text elements in Streamlit -> Docs (https://docs.streamlit.io/library/api-reference/text)

    # 2.3.1 - Write the title for your streamlit application -> "Streamlit Web App" -> If prompted in the web "Rerun", Choose "Always Rerun"
    # 2.3.2 - Write the subheader for your streamlit application -> "Created for Programming Lab Session 10"
    # 2.3.3 - Write text for your streamlit application -> "Exploratory Data Analysis for Customer Churn in the Telecommunications industry"

# PS! There are some pretty cool elements available with Markdown and Latex. Feel free to play around with these. 
    # Docs -> Markdown https://www.markdownguide.org/cheat-sheet/ , Latex https://katex.org/docs/supported.html. 



# 2.4 - Importing the dataframe and displaying the first 5 rows as a static table.. 
    # 2.4.1 - Import the dataframe as churn_df.
    # 2.4.2 - Display the first five rows of the table. 
    # 2.4.3 - Display the datatypes.



# 2.5 - Making plots
    # 2.5.1 - Add a filter, so that you can filter it by the Age column. 
        # With min_value & default as minimum value of age, maximum value of age. 
    # 2.5.2 - Show the correlation metric and plot a line between "Age" and "Age Group" using a line chart.
    # 2.5.3 - Analyse the distribution of "Age Group" column using a histogram. 
        # Make the bins equal to the amount of unique values in the column.
    # 2.5.4 - Make a histogram for all the columns and use a numeric input for the input of bins. 
    
import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px

st.title("My first Streamlit App LUCAS NOOB")
st.header("This is a new header")
st.text("This is the explanation of something")



st.text("This is a text")
st.markdown("This is a **markdown** text")
st.code("# This is code\ndata = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})")
st.success("This is a success")
st.info("This is an info")
st.warning("This is a warning")

data = px.data.iris()
st.markdown("We also can include dynamic tables with `st.dataframe`")
st.dataframe(data.head())
st.markdown("And also static tables with `st.table`")
st.table(data.head())
st.markdown("And also metrics with `st.metric` combined with `st.columns`")
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

st.markdown("Including plotly plots with `st.plotly_chart`")
st.plotly_chart(px.scatter(data, x="sepal_width", y="sepal_length", color="species", template="none"))

st.markdown("Including images with `st.image`")
st.image("https://media.giphy.com/media/zGnnFpOB1OjMQ/giphy.gif", caption='My image')

st.markdown("Including video with `st.video`")
st.video("https://youtu.be/5-tHimysW-A")

with st.container():
    st.markdown("Including widgets with `st.button`, `st.checkbox`, `st.radio`, `st.selectbox`, `st.slider`, `st.text_input`, `st.text_area`, `st.date_input`, `st.time_input`")
    st.button("This is a button")
    st.checkbox("This is a checkbox")
    st.radio("This is a radio", ("Option 1", "Option 2"))
    st.selectbox("This is a selectbox", ("Option 1", "Option 2"))
    st.slider("This is a slider", 1, 100)
    st.text_input("This is a text input")
    st.text_area("This is a text area")
    st.date_input("This is a date input")
    st.time_input("This is a time input")

    st.markdown("Including progress bars with `st.progress`")
    my_bar = st.progress(0)
    for p in range(10):
        my_bar.progress(p + 1)

    st.markdown("Or a spinner with `st.spinner`")
    with st.spinner('Wait for it...'):
        time.sleep(1)
    st.success('Done!')


st.markdown("Separating views in different tabs with `st.tabs`")
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
data = np.random.randn(10, 1)

tab1.subheader("A tab with a chart")
tab1.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)

st.markdown("This is a form with `st.form`")
with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)

# Retrieve location data
st.markdown("This is a map with `st.map`")
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)



# Also, we can include those elements in the sidebar
st.sidebar.title("Including things also in a sidebar!")
st.sidebar.button("This is a sidebar button")
st.sidebar.checkbox("This is a sidebar checkbox")
st.sidebar.radio("This is a sidebar radio", ("Option 1", "Option 2"))
st.sidebar.selectbox("This is a sidebar selectbox", ("Option 1", "Option 2"))
st.sidebar.slider("This is a sidebar slider", 1, 100)
st.sidebar.text_input("This is a sidebar text input")
st.sidebar.text_area("This is a sidebar text area")
st.sidebar.date_input("This is a sidebar date input")
st.sidebar.time_input("This is a sidebar time input")

