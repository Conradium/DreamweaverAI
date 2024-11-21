# import streamlit as st
# from utils.dreamweavercore import DreamCore

# # Initialize the DreamCore with your API key
# API_KEY = 'AIzaSyCEGT7dvoQG-1VvBgZIYUb4h2lLG9aW5Do'  # Replace with your actual API key
# dream_core = DreamCore(api_key=API_KEY)

# # Streamlit app layout
# st.title("Gemini Chatbot")
# st.write("Welcome to the Gemini Chatbot! Type your message below and get a response.")

# # Initialize session state for chat history
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# # User input
# user_input = st.text_input("You:", "")

# # Generate response button
# if st.button("Send"):
#     if user_input:
#         # Append user message to chat history
#         st.session_state.messages.append({"role": "user", "content": user_input})
        
#         # Generate response from the model
#         with st.spinner("Generating response..."):
#             response = dream_core.generate_content(user_input)
#             st.session_state.messages.append({"role": "assistant", "content": response})
        
#         # Clear the input box after sending
#         user_input = ""

# # Display chat messages
# for message in st.session_state.messages:
#     if message['role'] == 'user':
#         st.chat_message("user").markdown(message['content'])
#     else:
#         st.chat_message("assistant").markdown(message['content'])

# # File upload section (optional)
# st.subheader("Upload Files (Optional)")
# uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx", "jpg", "png"])
# if uploaded_file is not None:
#     file_path = f"./uploads/{uploaded_file.name}"
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
    
#     if st.button("Upload File"):
#         upload_response = dream_core.upload_files(file_path, name=uploaded_file.name)
#         st.success(upload_response)


import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

st.title("🌟 Gemini Quickstart App")

google_api_key = st.sidebar.text_input("Google API Key", type="password")

def generate_response(input_text):
    model = ChatGoogleGenerativeAI(
        google_api_key=google_api_key, 
        model="gemini-pro", 
        temperature=0.7
    )
    response = model.invoke(input_text)
    st.info(response.content)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if not google_api_key:
        st.warning("Please enter your Google API key!", icon="⚠")
    if submitted and google_api_key:
        generate_response(text)
