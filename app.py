import streamlit as st
import google.generativeai as genai
import sqlite3

# ---- API Configuration ----
API_KEY = "AIzaSyBsq5Kd5nJgx2fejR77NT8v5Lk3PK4gbH8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ---- Database Setup ----
# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect('chat_history.db', check_same_thread=False)
cursor = conn.cursor()

# Create table to store chat logs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        bot_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# ---- Streamlit Setup ----
st.title("🤖 Chatbot - Your AI Assistant")
st.write('This is an AI Chatbot to solve your queries......')

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Say something..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Gemini
    response = st.session_state.chat.send_message(prompt)

    # Display assistant message
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)

    # Store both in the database
    cursor.execute("INSERT INTO chat_log (user_input, bot_response) VALUES (?, ?)", (prompt, response.text))
    conn.commit()
