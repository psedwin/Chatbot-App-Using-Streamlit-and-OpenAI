# app.py

# -------------------------------
# 🤖 Build an AI Chatbot with GPT
# Using Python + Streamlit + OpenAI
# -------------------------------

import os
from dotenv import load_dotenv  # To read the .env file
import streamlit as st          # For the web app
from openai import OpenAI       # To connect with OpenAI's GPT models

# -------------------------------
# STEP 1: Load the API key safely
# -------------------------------

load_dotenv()  # Load all values from .env file
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ Please add your OpenAI API key to a .env file first!")
    st.stop()  # Stop the app if no key found

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# -------------------------------
# STEP 2: Set up Streamlit page
# -------------------------------

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Your Personal AI Chatbot")
st.write("Chat live with an AI assistant powered by GPT + Streamlit!")

# -------------------------------
# STEP 3: Create a chat history
# -------------------------------
# We’ll use Streamlit’s session_state to remember past messages

if "messages" not in st.session_state:
    st.session_state["messages"] = []
 
# Display previous messages (both user & assistant)

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# -------------------------------
# STEP 4: Get user input
# -------------------------------

user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------------
    # STEP 5: Generate AI response
    # -------------------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 💭"):
            try:
                # Send chat history to GPT
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  
                    messages=[
                        {"role": "system", "content": "You are a helpful, friendly AI assistant."},
                        *st.session_state["messages"]  # Include full chat so far
                    ]
                )

                # Get the text from the response
                ai_message = response.choices[0].message.content

            except Exception as e:
                ai_message = f"⚠️ Error: {str(e)}"

            # Display AI message
            st.markdown(ai_message)

    # Save AI message to chat history
    
    st.session_state["messages"].append({"role": "assistant", "content": ai_message})

# -------------------------------
# STEP 6: Optional features
# -------------------------------
# Add a "Clear Chat" button

if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()  # Reload app