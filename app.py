import streamlit as st
import pickle
import sqlite3
import hashlib

vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("finalized_model.pkl", 'rb'))

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('user_data.db')
    return conn

# Function to create a table to store user data if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()

# Function to insert user data into the database
def add_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

# Function to check if a user exists in the database
def check_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None

# Define the content of the home page
def home():
    st.write("""
    # Welcome to the Fake News Detector App!

    This app uses machine learning to predict the authenticity of news articles. Simply paste in a news article and our model will classify it as reliable or likely to be fake/unreliable. 

    This tool can be useful for fact-checking and verifying information before sharing it on social media or other platforms.

    Please use responsibly and always verify information from multiple sources.

    --- 

    ### How does it work?

    Our model was trained on a dataset of labeled news articles to learn the patterns and characteristics of reliable vs. fake/unreliable news. 

    It takes in the text of a news article as input and outputs a binary classification of 1 (reliable) or 0 (fake/unreliable). 

    --- 

    ### About Fake News

    Fake news refers to deliberate misinformation or hoaxes that are spread through traditional or social media. These false stories can have serious consequences, such as damaging reputations, inciting violence, or influencing political outcomes. 

    It's important to be aware of the signs of fake news and to fact-check information before sharing it. 

    ---
    """)

# Define the content of the login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = create_connection()
        if check_user(conn, username, hashlib.sha256(password.encode()).hexdigest()):
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password.")
            return False

# Define the content of the registration page
def register():
    st.title("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if new_password == confirm_password:
            conn = create_connection()
            add_user(conn, new_username, hashlib.sha256(new_password.encode()).hexdigest())
            st.success("Registration successful! You can now login.")
        else:
            st.error("Passwords do not match.")

# Function to predict the news authenticity
def predict_news(news):
    predict = model.predict(vector.transform([news]))[0]
    return predict

# Define the content of the prediction page
def prediction():
    st.title("Fake News Prediction App")
    st.header("Enter the text of the news article below")
    news = st.text_area("News Text")
    if st.button("Predict"):
        if news:
            prediction = predict_news(news)
            st.success("News headline is -> {}".format(prediction))
        else:
            st.warning("Please enter the text of the news article to make a prediction.")

# Main function to handle page navigation
def main():
    st.sidebar.title("Navigation")
    menu = ["Home", "Login", "Register", "Prediction"]
    choice = st.sidebar.selectbox("Select an option", menu)
    if choice == "Home":
        home()
    elif choice == "Login":
        if login():
            st.experimental_rerun()
    elif choice == "Register":
        register()
    elif choice == "Prediction":
        if login():
            prediction()

if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    main()
