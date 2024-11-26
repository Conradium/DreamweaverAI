import streamlit as st
import google.generativeai as genai
import time  # Import time module for sleep

def generate_story(api_key, genre, theme, characters=None, roles=None, extra_info=None, previous_story=None):
    try:
        # Configure the API key
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        if previous_story:
            prompt = f"Continue this story. The previous part was: {previous_story}"
        else:
            prompt = f"Write a {genre} story about {theme}."
        
        if characters:
            prompt += f" Include the following characters: {', '.join(characters)}."
        
        if roles:
            prompt += f" Their roles are: {', '.join(roles)}."
        
        if extra_info:
            prompt += f" Additional information: {extra_info}."
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to generate an image from Pollinations API
def generate_image(theme):
    # Use the Pollinations API to generate an image based on the theme
    return f"https://image.pollinations.ai/prompt/{theme}"

# Streamlit app layout
def main():
    # Initialize session state for story if not exists
    if 'full_story' not in st.session_state:
        st.session_state.full_story = ""
    
    st.title("Story Generator")
    st.sidebar.title("Dreamweaver AI 🌙")
    st.sidebar.header("API Configuration")
    api_key = st.sidebar.text_input("Enter Google Generative AI API Key", type="password")
    
    # Initialize image URL
    image_url = None
    
    if api_key:
        st.sidebar.header("Story Parameters")

        # Genre selection
        genre = st.sidebar.selectbox("Select a Genre", [
            "Fantasy", 
            "Science Fiction", 
            "Mystery", 
            "Romance", 
            "Horror", 
            "Adventure", 
            "Thriller"
        ])

        theme = st.sidebar.text_input("Enter a Theme")
        characters_input = st.sidebar.text_area("Enter Characters (comma-separated)", "")
        characters = [char.strip() for char in characters_input.split(',')] if characters_input else None
        roles_input = st.sidebar.text_area("Enter Roles for the Characters (comma-separated)", "")
        roles = [role.strip() for role in roles_input.split(',')] if roles_input else None
        extra_info = st.sidebar.text_area("Enter Any Extra Information", "")

        # Generate story button
        if st.button("Generate Story"):
            if theme:
                with st.spinner('Generating your story...'):
                    story = generate_story(api_key, genre, theme, characters, roles, extra_info)
                    
                    if story:
                        st.session_state.full_story = story
                        st.subheader("Generated Story")
                        st.write(story)

                        # Simulate longer loading for image generation
                        with st.spinner('Generating image...'):  # Adjust this duration as needed
                            image_url = generate_image(theme)
                            time.sleep(5)

                # Display the generated image at the top
                if image_url:
                    st.image(image_url, caption=f"Image for theme: {theme}", use_column_width=True)

            else:
                st.warning("Please enter a theme to generate a story.")
        
        # Continue story button (only show if there's an existing story)
        if st.session_state.full_story:
            if st.button("Continue Story"):
                with st.spinner('Continuing the story...'):
                    continued_story = generate_story(
                        api_key, 
                        genre, 
                        theme, 
                        characters, 
                        roles, 
                        extra_info, 
                        previous_story=st.session_state.full_story
                    )
                    
                    if continued_story:
                        # Append the new part to the full story
                        st.session_state.full_story += "\n\n" + continued_story
                        st.subheader("Updated Story")
                        st.write(st.session_state.full_story)

    else:
        st.info("Please enter your Google Generative AI API Key in the sidebar to get started.")
        st.link_button("Get one here", "https://aistudio.google.com/app/apikey")

main()
# import streamlit as st
# from utils.dreamweavercore import DreamCore

# # Initialize the DreamCore with your API key
#  Replace with your actual API key
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
