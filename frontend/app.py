import streamlit as st
import requests
import uuid
import random
import os
from streamlit.components.v1 import html

st.set_page_config(page_title="AI Tutor", layout="wide")

st.title("AI powered Tutor and Quiz App")


with st.sidebar:
    st.header("Learning Preferences")
    subject = st.selectbox("Select Subject", ["Mathematics", "Physics", "History", "Computer Science", "Biology", "Programming"])
    level = st.selectbox("Select Learning Level", ["Beginner", "Intermediate", "Advanced"])
    learning_style = st.selectbox("Select Learning Style", ["Text-based", "Visual", "Hands-on"])
    language = st.selectbox("Select Preferred Language", ["English", "Hindi", "Spanish", "French", "German"])
    background = st.selectbox("Select Background Knowledge", ["None", "Basic", "Intermediate", "Experienced"])

API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:8000")

tab1, tab2 = st.tabs(["Ask a Question", "Take a Quiz"])

with tab1:
    st.header("Ask a Question")
    question = st.text_area("What would you like to learn today?",
                            "Explain the Pythagorean theorem.")
    if st.button("Get Explanation"):
        with st.spinner("Generating personalized explanation..."):
            try:
                response = requests.post(f"{API_ENDPOINT}/tutor", json={
                    "subject": subject,
                    "level": level,
                    "question": question,
                    "learning_style": learning_style,
                    "background": background,
                    "language": language
                }).json()
                st.success("Here's your personalized explanation:")
                st.markdown(response['response'],
                unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error getting explanation: {str(e)}")
                st.info(f"Please ensure the backend server is running at {API_ENDPOINT}")

with tab2:
    st.header("Test Your Knowledge with a Quiz")
    col1, col2 = st.columns([2, 1])
    with col1:
        num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)
    with col2:
        quiz_button = st.button("Generate Quiz", use_container_width=True)
    if quiz_button:
        with st.spinner("Creating quiz questions..."):
            try:
                response = requests.post(f"{API_ENDPOINT}/quiz", json={
                    "subject": subject,
                    "level": level,
                    "num_questions": num_questions,
                    "reveal_format": True
                }).json()
                st.success("Quiz generated! Answer the questions below:")
                
                if 'formatted_quiz' in response and response['formatted_quiz']:
                    html(response['formatted_quiz'], height= num_questions * 300)
                else:
                    for i, q in enumerate(response['quiz']):
                        st.expander(f"Question {i+1}: {q['question']}", expanded=True)
                        session_id = str(uuid.uuid4())
                        
                        selected = st.radio(
                            "Select an answer:",
                            q['options'],
                            key=f"q_{session_id}"
                        )

                        if st.button("Check Answer", key=f"check_{session_id}"):
                            if selected == q['correct_answer']:
                                st.success(f"Correct! {q.get('explanation')}")
                            else:
                                st.error(f"Incorrect! The correct answer is: {q['correct_answer']}")
                                if 'explanation' in q:
                                    st.info(q['explanation'])
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
                st.info(f"Please ensure the backend server is running at {API_ENDPOINT}")

st.markdown("---")
st.markdown("Powered by AI - Your personalized learning assistant.")



