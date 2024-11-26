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
                            time.sleep(10)

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
