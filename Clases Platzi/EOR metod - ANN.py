# https://github.com/FreddyEcu-Ch/Machine-Learning/blob/main/ml_app.py
# https://share.streamlit.io/freddyecu-ch/machine-learning/main/ml_app.py


import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Page Layout
# Page expands to full width
st.set_page_config(page_title="EOR_Ml App")

# CSS codes to improve the design of the web app
st.markdown("""
<style>
h1 {text-align: center;
    background-color: white;
}
body {background-color: #DCE3D5;
      width: 1200px;
      margin: 15px auto;
}
</style>""", unsafe_allow_html=True)

# Insert image
image = Image.open("dt_og.jpg")
st.image(image, width=100, use_column_width=True, caption='Dassault Systemes. (2020, July). Oil & Gas Digital Transformation')

# Write title and additional information
st.title("Welcome to Data Science & ML for Oil and Gas Engineering")

st.write('---')

st.markdown("""
This App consists of implementing an **EOR Screening** for any well by using Machine 
Learning algorithms. 
* **By:** [Freddy Carrion](https://www.linkedin.com/in/freddy-carri%C3%B3n-maldonado-b3579b125/)
* **Python Libraries:** scikit-learn, pandas, numpy, streamlit, matplotlib, folium,
pillow, streamlit_folium, pandas_profiling, streamlit-pandas-profiling
""")

# Fill in information about the project implemented in this app
expander_bar = st.beta_expander("About")
expander_bar.markdown("This project consists of implementing an EOR Screening by using "
                      "Machine Learning algorithms. It must be mentioned that the "
                      "dataset used for training and evaluating these algorithms have a"
                      "size of roughly 200 successful EOR Projects (Rows or "
                      "observations) from some countries, as well as 7 reservoir "
                      "parameters, which are the feature or dependent variables. "
                      "Furthermore, the target variable of this model is a categorical "
                      "variable, which contains 5 EOR Methods (classes) such as the "
                      "steam injection method, CO2 injection method, HC injection "
                      "method, polymer injection method, and combustion in situ "
                      "method.")

# Adding of a mp4 video
st.markdown("""
**The Phases of Oil Recovery**
""")
video = open("Oil Phases Recovery.mp4", "rb")
st.video(video)
st.markdown("<span style=“background-color:#121922”>", unsafe_allow_html=True)
st.markdown("Energy & Environmental Research Center. (2014, April). The Phases of Oil Recovery")


# Sidebar - collects user input features into dataframe
with st.sidebar.header("1. Upload the csv data"):
    upload_file = st.sidebar.file_uploader("Upload your csv file", type=["csv"])
    st.sidebar.markdown("""
    [Download csv file](https://raw.githubusercontent.com/FreddyEcu-Ch/Machine-Learning/main/DATA%20WORLWIDE%20EOR%20PROJECTSP.csv)
    """)

# Sidebar - ML Algorithms
with st.sidebar.subheader("2. Select ML Algorithm"):
    algorithm = st.sidebar.selectbox("Select algorithm", ("K Nearest Neighbors(KNN)",
                                                          "Decision Tree"))

# Setting parameters
st.sidebar.subheader("3. Set User Input Parameters")
with st.sidebar.subheader("3.1 Data Split"):
    split_size = st.sidebar.slider('Data split ratio (% for training set)', 10, 90, 80)

with st.sidebar.subheader("3.2 Learning parameters"):
    if algorithm == "K Nearest Neighbors(KNN)":
        parameter_k_neighbors = st.sidebar.slider("Number of K neighbors", 1, 30, 2)

    else:
        parameter_decision_tree = st.sidebar.slider("Number of max depth", 1,10, 3)

with st.sidebar.subheader("3.3 Reservoir Parameters"):
    Porosity = st.sidebar.slider("Porosity (%)", 2, 30)
    Permeability = st.sidebar.slider("Permeability (md)", 8, 5000)
    Depth = st.sidebar.slider("Depth (ft)", 1000, 10000, 1200)
    Gravity = st.sidebar.slider("API Gravity", 5, 40, 8)
    Viscosity = st.sidebar.slider("Oil Viscosity (cp)", 10, 500000, 490058)
    Temperature = st.sidebar.slider("Reservoir Temperature (F)", 50, 300)
    Oil_saturation = st.sidebar.slider("Oil Saturation (%)", 10, 80, 35)

# Exploratory Data Analysis (EDA)
if st.button('Press to See the Exploratory Data Analysis (EDA)'):
    st.header('**Exploratory Data Analysis (EDA)**')
    st.write('---')
    if upload_file is not None:
        @st.cache
        def load_csv():
            data = pd.read_csv(upload_file)
            return data
        df = load_csv()
        report = ProfileReport(df, explorative=True)
        st.markdown('**Input Dataframe**')
        st.write(df)
        st.write('---')
        st.markdown('**EDA Report**')
        st_profile_report(report)

    st.write('---')
    st.header('**Geospatial Data**')

    # Load the coordinates of the countries where the EOR projects of this dataset are
    coordinates = {"Norway": ([64.5783, 17.8882], 5),
                   "Canada": ([56.130366, -106.346771], 38),
                   "Usa": ([37.09024, -95.712891], 140),
                   "Brazil": ([-23.533773, -46.625290], 8),
                   "Egypt": ([26.820553, 30.802498], 1),
                   "Germany": ([51.5167, 9.9167], 10)}
    # Load the world map
    m = folium.Map(zoom_start=14)
    # Load the markers and popups
    for country, point in coordinates.items():
        folium.Marker(point[0], popup="<b>{}: </b> {} EOR Projects".
                              format(country, point[1])).add_to(m)
    folium_static(m)

# Calling data processing modules
sc = MinMaxScaler()
le = LabelEncoder()
ohe = OneHotEncoder()

# Model Building


def model(dataframe):
    # Calling the independent and dependent variables
    X = dataframe.iloc[:, 2:9]
    Y = dataframe.iloc[:, 1:2]

    # Data details
    st.markdown('**1.2. Data Split**')
    st.write('Training set')
    st.info(X.shape)
    st.info(Y.shape)

    # Variable information
    st.markdown('**1.3. Variable details**')
    st.write('Independent Variables')
    st.info(list(X.columns))
    st.write('Dependent Variable')
    st.info(list(Y.columns))

    # data processing step
    X = sc.fit_transform(X)
    dfle = dataframe
    dfle.EOR_Method = le.fit_transform(dfle.EOR_Method)
    Y = ohe.fit_transform(Y).toarray()

    # Data splitting
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=split_size,
                                                        random_state=0)

    # Calling the information that will be used for model prediction
    cnames = ['Porosity', 'Permiability', 'Depth', 'Gravity', 'Viscosity',
              'Temperature', 'Oil_Saturation']
    data = [[Porosity, Permeability, Depth, Gravity, Viscosity, Temperature,
             Oil_saturation]]
    my_X = pd.DataFrame(data=data, columns=cnames)
    my_X = sc.transform(my_X)

    # Calling the ML algorithms for their training, plottings, and predictions
    if algorithm == "K Nearest Neighbors(KNN)":
        Knn = KNeighborsClassifier(n_neighbors=parameter_k_neighbors)
        Knn.fit(X_train, Y_train)
        training_score = Knn.score(X_train, Y_train)
        test_score = Knn.score(X_test, Y_test)

        neighbors = np.arange(1, 30)
        train_accuracy = np.empty(len(neighbors))
        test_accuracy = np.empty(len(neighbors))
        for i, k in enumerate(neighbors):
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X_train, Y_train)
            train_accuracy[i] = knn.score(X_train, Y_train)
            test_accuracy[i] = knn.score(X_test, Y_test)
        plt.plot(neighbors, test_accuracy, label='Test')
        plt.plot(neighbors, train_accuracy, label='Training')
        plt.legend()
        plt.xlabel('K_neighbors')
        plt.ylabel('Accuracy')

        prediction = Knn.predict(my_X)

    else:
        tree = DecisionTreeClassifier(max_depth=parameter_decision_tree)
        tree.fit(X_train, Y_train)
        training_score = tree.score(X_train, Y_train)
        test_score = tree.score(X_test, Y_test)

        max_depth = np.arange(1, 9)
        train_accuracy = np.empty(len(max_depth))
        test_accuracy = np.empty(len(max_depth))
        for i, r in enumerate(max_depth):
            Tree = DecisionTreeClassifier(max_depth=r)
            Tree.fit(X_train, Y_train)
            train_accuracy[i] = Tree.score(X_train, Y_train)
            test_accuracy[i] = Tree.score(X_test, Y_test)
        plt.plot(max_depth, test_accuracy, label='Test')
        plt.plot(max_depth, train_accuracy, label='Train')
        plt.legend()
        plt.xlabel('max_depth_values')
        plt.ylabel('Accuracy')

        prediction = tree.predict(my_X)

    # Model performance information
    st.subheader("2. Model Performance")
    st.markdown('**2.1 Training set**')
    st.write('Accuracy of training set')
    st.info(training_score)
    st.write('---')
    st.markdown('**2.2 Test set**')
    st.write('Accuracy of Test set')
    st.info(test_score)
    st.write('---')
    st.markdown('**2.3 Graphical Performance**')
    st.pyplot(plt)

    # Model prediction information
    st.write('---')
    st.subheader('3. Model Prediction')
    if np.argmax(prediction) == 0:
        st.info('CO2 Injection')
    elif np.argmax(prediction) == 1:
        st.info('Combustion')
    elif np.argmax(prediction) == 2:
        st.info('HC Injection')
    elif np.argmax(prediction) == 3:
        st.info('Polymer')
    elif np.argmax(prediction) == 4:
        st.info('Steam Injection')

# Model Deployment


if st.button('Model Deployment'):
    if upload_file is not None:
        st.write('---')
        st.subheader('1. Dataset')
        df = pd.read_csv(upload_file)
        df.rename(columns={'Viscocity':'Viscosity'}, inplace=True)
        st.markdown('**1.1 Showing dataset**')
        st.write(df)
        model(df)
