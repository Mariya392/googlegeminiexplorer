#!/usr/bin/env python
# coding: utf-8

# In[11]:


import vertexai
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession
import streamlit as st

# Initialize Vertex AI
project = "sample-gemini-429818"
vertexai.init(project=project)
config = generative_models.GenerationConfig(temperature=0.4)
model = GenerativeModel("gemini-pro", generation_config=config)
chat = model.start_chat()

def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text
    with st.chat_message("model"):
        st.markdown(output)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

# Create a Title for the Streamlit App
st.title("Gemini Explorer")

# Capture User's Name
user_name = st.text_input("Please enter your name")

# Initialize Chat History in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and Load Chat History
for index, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("model"):
            st.markdown(message["content"])

# Set Initial Prompt with User's Name
if len(st.session_state.messages) == 0 and user_name:
    initial_prompt = f"Hello {user_name}, I'm ReX, an assistant powered by Google Gemini. How can I assist you today?"
    llm_function(chat, initial_prompt)

# Capture and Process User Input
query = st.text_input("Share some details about yourself or ask a question")
if st.button("Submit"):
    if query:
        with st.chat_message("user"):
            st.markdown(query)  # Display the user's query in the Streamlit app
        llm_function(chat, query)  # Process the user's query using the llm_function


# In[ ]:




