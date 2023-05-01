import streamlit as st
import pickle

vector = pickle.load(open("/home/mr1ncr1d1ble/Downloads/vectorizer.pkl", 'rb'))
model = pickle.load(open("/home/mr1ncr1d1ble/Downloads/finalized_model.pkl", 'rb'))
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


def predict_news(news):
    predict = model.predict(vector.transform([news]))[0]
    return predict

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

def main():
    st.sidebar.title("Navigation")
    menu = ["Home", "Prediction"]
    choice = st.sidebar.selectbox("Select an option", menu)
    if choice == "Home":
        home()
    elif choice == "Prediction":
        prediction()

if __name__ == '__main__':
    main()
