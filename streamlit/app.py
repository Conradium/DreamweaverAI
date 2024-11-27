import streamlit as st
import google.generativeai as genai
import time
import spacy
import numpy as np
import nltk
nltk.download('punkt_tab')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu
from sentence_transformers import SentenceTransformer
# StoryCoherenceEvaluator class definition
class StoryCoherenceEvaluator:
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_md')
            nltk.download('punkt')
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')  # Using Sentence-BERT
        except Exception as e:
            print(f"Error loading NLP models: {e}")
            raise

    def semantic_coherence(self, text):
        sentences = nltk.sent_tokenize(text)
        sentence_embeddings = self.sentence_model.encode(sentences)

        similarities = []
        for i in range(1, len(sentence_embeddings)):
            similarity = cosine_similarity(
                sentence_embeddings[i-1].reshape(1, -1),
                sentence_embeddings[i].reshape(1, -1)
            )[0][0]
            similarities.append(similarity)

        return {
            'avg_sentence_similarity': np.mean(similarities) if similarities else 0,
            'semantic_coherence_score': np.mean(similarities) if similarities else 0
        }

    def lexical_coherence(self, text):
        sentences = nltk.sent_tokenize(text)

        # TF-IDF vectorization
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)

        # Compute cosine similarities between consecutive sentences
        similarities = []
        for i in range(1, len(sentences)):
            similarity = cosine_similarity(
                tfidf_matrix[i-1],
                tfidf_matrix[i]
            )[0][0]
            similarities.append(similarity)

        return {
            'lexical_similarity': np.mean(similarities) if similarities else 0,
            'lexical_coherence_score': np.mean(similarities) if similarities else 0
        }

    def narrative_flow_evaluation(self, text):
        sentences = nltk.sent_tokenize(text)

        # finds candidates for similarity/pattern in the output
        bleu_scores = []
        for i in range(1, len(sentences)):
            reference = [sentences[i-1].split()]
            candidate = sentences[i].split()
            bleu_score = sentence_bleu(reference, candidate)
            bleu_scores.append(bleu_score)

        return {
            'narrative_flow_score': np.mean(bleu_scores) if bleu_scores else 0,
            'narrative_progression_variance': np.std(bleu_scores) if bleu_scores else 0
        }

    def comprehensive_coherence_analysis(self, text):
        semantic_analysis = self.semantic_coherence(text)
        lexical_analysis = self.lexical_coherence(text)
        narrative_analysis = self.narrative_flow_evaluation(text)

        # scores combined with weight (reason: adjustable preference)
        coherence_score = (
            0.4 * semantic_analysis['semantic_coherence_score'] +
            0.3 * lexical_analysis['lexical_coherence_score'] +
            0.3 * narrative_analysis['narrative_flow_score']
        )

        return {
            'overall_coherence_score': coherence_score,
            'semantic_coherence': semantic_analysis,
            'lexical_coherence': lexical_analysis,
            'narrative_flow': narrative_analysis
        }

# Story generation function
def generate_story(api_key, genre, theme, characters=None, roles=None, extra_info=None, previous_story=None):
    try:
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

# Image generation function
def generate_image(theme):
    return f"https://image.pollinations.ai/prompt/{theme}"

def main():
    evaluator = StoryCoherenceEvaluator()
    
    if 'full_story' not in st.session_state:
        st.session_state.full_story = ""
    
    st.title("Story Generator")
    st.sidebar.title("Dreamweaver AI 🌙")
    st.sidebar.header("API Configuration")
    api_key = st.sidebar.text_input("Enter Google Generative AI API Key", type="password")
    
    image_url = None
    
    if api_key:
        st.sidebar.header("Story Parameters")

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

                        with st.spinner('Generating image...'): 
                            image_url = generate_image(theme)
                            time.sleep(10)
                if image_url:
                    st.image(image_url, caption=f"Image for theme: {theme}", use_column_width=True)

                # Evaluate the story
                evaluation_results = evaluator.comprehensive_coherence_analysis(st.session_state.full_story)
                st.sidebar.header("Story Evaluations")
                st.sidebar.write(f"Overall Coherence Score: {evaluation_results['overall_coherence_score']:.5f}")
                st.sidebar.write(f"Semantic Coherence Score: {evaluation_results['semantic_coherence']['semantic_coherence_score']:.5f}")
                st.sidebar.write(f"Lexical Coherence Score: {evaluation_results['lexical_coherence']['lexical_coherence_score']:.5f}")
                st.sidebar.write(f"Narrative Flow Score: {evaluation_results['narrative_flow']['narrative_flow_score']:.5f}")

                # Button to generate another story
                if st.sidebar.button("Generate Another Story"):
                    st.session_state.full_story = ""
                    st.experimental_rerun()

            else:
                st.warning("Please enter a theme to generate a story.")
        
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
                        st.session_state.full_story += "\n\n" + continued_story
                        st.subheader("Continued Story")
                        st.write(st.session_state.full_story)
                        st.image(image_url, caption=f"Image for theme: {theme}", use_column_width=True)

    else:
        st.info("Please enter your Google Generative AI API Key in the sidebar to get started.")
        st.link_button("Get one here", "https://aistudio.google.com/app/apikey")

main()