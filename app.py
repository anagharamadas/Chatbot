from openai import OpenAI
import requests
from pydantic import BaseModel
import json
from datetime import datetime
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

st.title("LLM powered Daily Fact Generator Application")

api_key = st.text_input("Enter your API key: ", type="password")
API_URL = "https://api.perplexity.ai/chat/completions"


# User input for the question
user_question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if not api_key:
        st.error("Please enter your Perplexity API key.")
    elif not user_question:
        st.error("Please enter a question.")
    else:
        # Prepare the request payload
        payload = {
            "model": "sonar-reasoning",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_question}
            ]
        }

        # Set up the headers
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}"
        }

        try:
            # Make the API request
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the response
            result = response.json()
            answer = result['choices'][0]['message']['content']

            # Display the answer
            st.subheader("Answer:")
            st.write(answer)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")
        except (KeyError, IndexError) as e:
            st.error("Error parsing the API response. Please try again.")