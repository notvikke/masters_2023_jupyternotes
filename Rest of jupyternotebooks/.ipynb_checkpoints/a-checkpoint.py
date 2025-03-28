import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
import plotly.express as px
import datetime
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
import numpy as np

@st.cache_data()
def load_data():
    bike_df = pd.read_csv('bikes.csv', parse_dates=["dteday"])
    bike = bike_df.copy()
    bike.isnull().sum().sum()
    bike["year"] = bike["dteday"].dt.year
    bike["month"] = bike["dteday"].dt.month
    bike["day"] = bike["dteday"].dt.day
    bike["hour"] = bike["dteday"].dt.hour
    bike["minute"] = bike["dteday"].dt.minute
    bike["second"] = bike["dteday"].dt.second
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    days = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    }
    seasons = {
        1: 'Springer',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    }
    working_day = {
        0: 'Weekend or holiday',
        1: 'Working_day'
    }
    bike["month"] = bike["month"].map(months)
    bike["weekday"] = bike["weekday"].map(days)
    bike["season"] = bike["season"].map(seasons)
    bike["workingday"] = bike["workingday"].map(working_day)
    bike["year_month"] = bike["dteday"].apply(lambda x: f"{x.year}-{x.month}")
    bike['date'] = bike['dteday'].dt.date
    return bike,bike_df

def main():
    st.set_page_config(layout="wide")
    # Añadir título en la portada
    st.title("BIKE SHARING")
    # Carga de los datos
    bike,bike_df = load_data()

    # Crear menú de navegación en la barra lateral izquierda
    menu = ["Bikes Count","Rental Counts","Rental per Year/month","Relation between varibales and rental bikes","Model"]
    choice = st.sidebar.selectbox("Select a Visualization", menu)
    
 

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image("https://media0.giphy.com/media/l41lYNASsqlUOt9Xq/giphy.gif?cid=ecf05e47gv1zqqqwwnz56fxboz6xksltbxlp1xqxmmh2tyzs&rid=giphy.gif")

    with col3:
        st.write(' ')


    # Bikes Count per year, month and day
    if choice == "Bikes Count":
        menu2 = ["Yearly Count","Monthly Count","Daily Count","Weekdays Count"]
        choice2 = st.sidebar.selectbox("Select a Visualization", menu2)
        st.text("""We can use the start and end date filter here to specify the date range that we're
            interested in observing and view all the graphs according to this filter.""")
        # Define el rango de fechas permitido
        min_date = datetime.date(2010, 1, 1)
        # Define la fecha predeterminada para el start_date
        default_start_date = datetime.date(2011, 1, 1)
        # Crea un widget de entrada de fecha con el rango permitido y la fecha predeterminada
        start_date = st.date_input('Start date', min_value=min_date, value=default_start_date)
        end_date = st.date_input('End date', min_value=min_date)
        # Filtra los datos según el rango de fechas seleccionado
        bike['date'] = bike['dteday'].dt.date
        filtered_data = bike[(bike['date'] >= start_date) & (bike['date'] <= end_date)]

        if choice2 == "Yearly Count":
            st.subheader("Bikes Count")
            st.text("""In this graph, we can observe the number of bicycles rented per year in the established period,
                    so if the range that interests us is only one year, only that year will appear with the total number of 
                    rentals that have occurred in that period of time.""")
            fig1 = px.bar(filtered_data, x="year", y="cnt", title="Per Year")
            st.plotly_chart(fig1)

        if choice2 == "Monthly Count":
            st.subheader("Bikes Count")
            st.text("""The graph displays the frequency of bicycle usage per month over the course of a year. To provide a more 
            detailed explanation, we can analyze the trends in the data and draw conclusions from them.Looking at the graph, we can observe
            that the number of bicycles used per month increases during the warmer months of the year, reaching a peak in the summer months, 
            and then declines during the colder months. This trend is likely due to the more favorable weather conditions during the warmer months, 
            which encourage people to spend more time outdoors and engage in physical activities such as cycling.Furthermore, we can see that there is 
            a gradual increase in bicycle usage from the beginning of the year, with the highest point in usage occurring in August, followed by a gradual decline 
            towards the end of the year. This trend could be attributed to people setting fitness goals or resolutions at the beginning of the year and then gradually 
            losing interest or motivation towards the end of the year.""")
            fig2 = px.bar(filtered_data, x="month", y="cnt", title="Per Month")
            st.plotly_chart(fig2)

        if choice2 == "Daily Count":
            st.subheader("Bikes Count")
            st.text("""The graph displays the frequency of bicycle usage per month over the course of a year. 
                    To provide a more detailed explanation, we can analyze the trends in the data and draw conclusions from them.""")
            fig3 = px.bar(filtered_data, x="day", y="cnt", title="Per Day")
            st.plotly_chart(fig3)

        if choice2 == "Weekdays Count":
            st.subheader("Bikes Count")
            fig4 = px.bar(filtered_data, x="weekday", y="cnt", title="Per Weekday")
            st.plotly_chart(fig4)

    elif choice == "Rental Counts":
        st.subheader("Rental counts")
        menu2 = ["Rental counts", "Rental counts by Season", "Rental counts by Working Day"]
        choice2 = st.sidebar.selectbox("Select a Visualization", menu2)

        st.text("""We can use the start and end date filter here to specify the date range that we're interested in observing and view all the graphs according to this filter.""")
        # Define el rango de fechas permitido
        min_date = datetime.date(2010, 1, 1)
        # Define la fecha predeterminada para el start_date
        default_start_date = datetime.date(2011, 1, 1)
        # Crea un widget de entrada de fecha con el rango permitido y la fecha predeterminada
        start_date = st.date_input('Start date', min_value=min_date, value=default_start_date)
        end_date = st.date_input('End date', min_value=min_date)
        # Filtra los datos según el rango de fechas seleccionado
        bike['date'] = bike['dteday'].dt.date
        filtered_data = bike[(bike['date'] >= start_date) & (bike['date'] <= end_date)]
        
        if choice2 == "Rental counts":
            st.text("""This graph shows the distribution of bicycle usage per hour, with each box representing the data distribution
            for a particular hour of the day. This graph can be used to identify peak usage hours and the overall trend of bicycle usage throughout the day.""")
            fig = px.box(filtered_data, y="cnt", title="Rental counts")
            st.plotly_chart(fig)
        
        elif choice2 == "Rental counts by Season":
            st.text("""This graph displays the distribution of bicycle usage per season, with each box representing the data distribution for a particular season.
            This graph can be used to compare the usage patterns between different seasons and identify any season-specific trends.""")
            fig = px.box(filtered_data, x="season", y="cnt", title="Rental counts by Season")
            st.plotly_chart(fig)
        
        elif choice2 == "Rental counts by Working Day":
            st.text("""This graph shows the distribution of bicycle usage for working and non-working days, with each box representing the data distribution
            for a particular type of day. This graph can be used to compare the usage patterns between working and non-working days and identify any potential differences in bicycle usage.""")
            fig = px.box(filtered_data, x="workingday", y="cnt", title="Rental counts by Working Day")
            st.plotly_chart(fig)

    elif choice == "Rental per Year/month":
        st.text("""We can use the start and end date filter here to specify the date range that we're
            interested in observing and view all the graphs according to this filter.""")
        
        # Define el rango de fechas permitido
        min_date = datetime.date(2010, 1, 1)
        # Define la fecha predeterminada para el start_date
        default_start_date = datetime.date(2011, 1, 1)
        # Crea un widget de entrada de fecha con el rango permitido y la fecha predeterminada
        start_date = st.date_input('Start date', min_value=min_date, value=default_start_date)
        end_date = st.date_input('End date', min_value=min_date)
        # Filtra los datos según el rango de fechas seleccionado
        bike['date'] = bike['dteday'].dt.date
        filtered_data = bike[(bike['date'] >= start_date) & (bike['date'] <= end_date)]

        st.subheader("Rental per Year/month")
        st.text("""The graph depicts the trend of bicycle usage over a two-year period, from January 2011 to December 2012.
        The data is presented in a year-month format, which allows for easy comparison between time periods.From the graph, 
        we can observe that there is an overall increasing trend in bicycle usage from the start of 2011 to the end of 2012. 
        However, there are also fluctuations in usage throughout the time period, with some months exhibiting higher usage than others.
        To gain a deeper understanding of the trends in bicycle usage over this time period, we could conduct further analysis, such as 
        identifying the factors that influence usage during certain months or examining any season-specific patterns. Additionally, this 
        information could be useful for bicycle-sharing companies or city planners to inform their resource allocation and marketing strategies.""")
        fig = px.bar(filtered_data, x="year_month", y="cnt", title="Rental counts by year and month")
        st.plotly_chart(fig)

    elif choice == "Relation between varibales and rental bikes":
        st.subheader("Relationship between variables and number of bike rentals")
        menu2 = ["Temperature","Windspeed","Humidity"]
        choice2 = st.sidebar.selectbox("Select a Visualization", menu2)
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "70 °F", "1.2 °F")
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "86%", "4%")
        st.text("""We can use the start and end date filter here to specify the date range that we're
                interested in observing and view all the graphs according to this filter.""")
        
        # Define el rango de fechas permitido
        min_date = datetime.date(2010, 1, 1)
        # Define la fecha predeterminada para el start_date
        default_start_date = datetime.date(2011, 1, 1)
        # Crea un widget de entrada de fecha con el rango permitido y la fecha predeterminada
        start_date = st.date_input('Start date', min_value=min_date, value=default_start_date)
        end_date = st.date_input('End date', min_value=min_date)
        # Filtra los datos según el rango de fechas seleccionado
        bike['date'] = bike['dteday'].dt.date
        filtered_data = bike[(bike['date'] >= start_date) & (bike['date'] <= end_date)]

        # Filtra los datos según el rango de fechas seleccionado
        bike['date'] = bike['dteday'].dt.date
        filtered_data = bike[(bike['date'] >= start_date) & (bike['date'] <= end_date)]
        if choice2 == "Temperature":
            fig1 = px.scatter(filtered_data, x="temp", y="cnt", trendline="ols",trendline_color_override="red")
            fig1.update_layout(title="Temperature vs Number of bike rentals")
            st.plotly_chart(fig1)

        elif choice2 == "Windspeed":
            fig2 = px.scatter(filtered_data, x="windspeed", y="cnt", trendline="ols",trendline_color_override="red")
            fig2.update_layout(title="Wind speed vs Number of bike rentals")
            st.plotly_chart(fig2)

        elif choice2 == "Humidity":
            fig3 = px.scatter(filtered_data, x="hum", y="cnt", trendline="ols",trendline_color_override="red")
            fig3.update_layout(title="Humidity vs Number of bike rentals")
            st.plotly_chart(fig3)

    elif choice == "Model":
        #MODEL
        bike_df.drop(["registered","casual"],axis=1,inplace=True)
        # Separar los datos en conjunto de entrenamiento y prueba
        X = bike_df.drop('cnt', axis=1)
        y = bike_df['cnt']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        ohe=OneHotEncoder()
        sc=StandardScaler()

        preprocess = ColumnTransformer(
            transformers=[
                ('num', sc, X.select_dtypes(include=['int64', 'float64']).columns),
                ('cat', ohe, X.select_dtypes(include=['object']).columns)])

        pipeline = Pipeline(steps=[('preprocess', preprocess),
                                                    ('model', 
                                                    XGBRegressor(
                                                        random_state=42, 
                                                        learning_rate=0.2, 
                                                        max_depth=8, 
                                                        n_estimators=700))])

        # Ajustar el modelo y hacer predicciones
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        # Asegurarse de que las predicciones sean valores positivos
        y_pred[y_pred < 0] = 1

        # Calcular las métricas de evaluación
        mse_xgb = mean_squared_error(y_test, y_pred)
        r2_xgb = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        r2_xgb=round(r2_xgb,4)
        mse_xgb=round(mse_xgb,4)
        mae=round(mae,4)
        col1, col2, col3 = st.columns(3)
        col1.metric("R^2",r2_xgb)
        col2.metric("MSE", mse_xgb)
        col3.metric("MAE", mae)

        results = Counter(y_pred)
        original = Counter(bike["cnt"])

        results = pd.DataFrame(list(results.items()), columns=['Number of rental Bikes', 'Count'])
        original = pd.DataFrame(list(original.items()), columns=['Number of rental Bikes', 'Count'])

        def get_proportion(data):
            return np.sum(data) / len(data)

        def get_iqr(data):
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            return q3 - q1
        results_bikes = results["Number of rental Bikes"]
        original_bikes = original["Number of rental Bikes"]

        results_proportion = get_proportion(results_bikes)
        original_proportion = get_proportion(original_bikes)

        results_iqr = get_iqr(results_bikes)
        original_iqr = get_iqr(original_bikes)

        results_mean = np.mean(results["Number of rental Bikes"])
        original_mean = np.mean(original["Number of rental Bikes"])

        results_mean=round(results_mean,0)
        original_mean=round(original_mean,0)
        results_proportion=round(results_proportion,1)
        original_proportion=round(original_proportion,1)
        results_iqr=round(results_iqr,1)
        original_iqr=round(original_iqr,1)

        fig = px.histogram(original, x='Number of rental Bikes', y='Count', nbins=50)
        st.write("## Original Rental Bikes")
        col1,col2,col3= st.columns(3)
        col1.metric("Proportion orginal rental bikes",original_proportion)
        col2.metric("Original IQR",original_iqr)
        col3.metric("Original mean",original_mean)
        fig.update_xaxes(title='Number of rental Bikes')
        fig.update_yaxes(title='Count')
        st.plotly_chart(fig)

        fig = px.histogram(results, x='Number of rental Bikes', y='Count', nbins=50)
        st.write("## Predicted Rental Bikes")
        col1,col2,col3= st.columns(3)
        col1.metric("Proportion prediction rental bikes",results_proportion)
        col2.metric("Prediction IQR",results_iqr)
        col3.metric("Predictions mean",results_mean)
        fig.update_xaxes(title='Number of rental Bikes')
        fig.update_yaxes(title='Count')
        st.plotly_chart(fig)
    
if __name__ == '__main__':
    main()