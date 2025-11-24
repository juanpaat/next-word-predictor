import streamlit as st
from openai import OpenAI
import toml
import os

# Configure the page
st.set_page_config(
    page_title="Next Word Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to set sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 33%;
        max-width: 33%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load API key and system prompt from Streamlit secrets (cloud) or secrets.toml (local)
try:
    # First, try to load from Streamlit secrets (for cloud deployment)
    default_api_key = st.secrets.get("api_key", "")
    system_prompt = st.secrets.get("system_prompt", "You are a helpful next-word prediction assistant that provides accurate, contextual word predictions.")
    api_key_from_secrets = bool(default_api_key)
except (FileNotFoundError, KeyError, Exception):
    # Fall back to secrets.toml for local development
    try:
        secrets_path = os.path.join(os.path.dirname(__file__), "secrets.toml")
        secrets = toml.load(secrets_path)
        default_api_key = secrets.get("api_key", "")
        system_prompt = secrets.get("system_prompt", "You are a helpful next-word prediction assistant that provides accurate, contextual word predictions.")
        api_key_from_secrets = bool(default_api_key)
    except (FileNotFoundError, KeyError, Exception):
        default_api_key = ""
        system_prompt = "You are a helpful next-word prediction assistant that provides accurate, contextual word predictions."
        api_key_from_secrets = False

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # OpenAI API Key Input
    st.subheader("API Configuration")
    if api_key_from_secrets:
        st.success("✓ API Key loaded from secrets")
        openai_api_key = default_api_key
    else:
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable predictions"
        )
    
    # Next-Word Prediction Slicer
    num_words = st.slider(
        "Number of words to predict",
        min_value=1,
        max_value=10,
        value=3,
        help="Choose how many next words the model should predict"
    )
    
    # Topic Selector
    st.subheader("Topics")
    topics = st.selectbox(
        "Select topic",
        options=[
            "General",
            "Technology",
            "Health",
            "Education",
            "Finance",
            "Entertainment",
            "Science",
            "Travel",
            "Food",
            "Sports",
            "History"
        ],
        help="Select a topic to contextualize predictions"
    )
    
    # Model Temperature Control
    temperature = st.slider(
        "Temperature (Randomness)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Lower values = more focused, Higher values = more creative"
    )
    
    # Tone Selector
    tone = st.selectbox(
        "Tone",
        options=["Formal", "Casual", "Creative", "Persuasive", "Informative"]
    )
    
    # Language Selector
    language = st.selectbox(
        "Output Language",
        options=[
            "🇬🇧 English",
            "🇪🇸 Spanish",
            "🇫🇷 French",
            "🇩🇪 German",
            "🇵🇹 Portuguese"
        ]
    )
    
    # Exclude words input
    exclude_words = st.text_input(
        "Exclude words",
        placeholder="optional",
        help="Comma-separated words to exclude from predictions"
    )

def build_prompt(user_input, num_words, topics, tone, language, exclude_words):
    """Build a comprehensive prompt based on all user settings"""
    
    # Map language display to actual language name
    lang_map = {
        "🇬🇧 English": "English",
        "🇪🇸 Spanish": "Spanish",
        "🇫🇷 French": "French",
        "🇩🇪 German": "German",
        "🇵🇹 Portuguese": "Portuguese"
    }
    output_language = lang_map.get(language, "English")
    
    # Build the main prompt
    prompt = f"""You are a next-word prediction assistant. Based on the given text, predict the next {num_words} most likely word(s) that would naturally continue the text.

Input text: "{user_input}"

Context and Requirements:
- Topic/Domain: {topics}
- Tone: {tone}
- Output Language: {output_language}
"""
    
    # Add exclusion if specified
    if exclude_words and exclude_words.strip():
        excluded = [word.strip() for word in exclude_words.split(",")]
        prompt += f"- Excluded words (do not include): {', '.join(excluded)}\n"
    
    prompt += f"""
Instructions:
1. Predict exactly {num_words} word(s) that would most naturally follow the input text
2. Consider the specified topic and tone
3. Return ONLY the predicted words in {output_language}, separated by commas
4. Do not include any explanations or additional text
5. Words should flow naturally from the input text

Example format: word1, word2, word3"""
    
    return prompt

def get_word_predictions(user_input, settings):
    """Get word predictions from OpenAI based on user input and settings"""
    
    if not settings['api_key']:
        return None, "Please enter your OpenAI API key in the sidebar"
    
    try:
        client = OpenAI(api_key=settings['api_key'])
        
        # Build the prompt
        prompt = build_prompt(
            user_input,
            settings['num_words'],
            settings['topics'],
            settings['tone'],
            settings['language'],
            settings['exclude_words']
        )
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=settings['temperature']
        )
        
        # Extract predicted words from response
        predicted_text = response.choices[0].message.content.strip()
        predicted_words = [word.strip() for word in predicted_text.split(",")]
        
        return predicted_words[:settings['num_words']], None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

# Main content
st.title("Next Word Predictor")

# Text input area
user_input = st.text_area(
    "Enter your text",
    placeholder="Type a word, phrase, or paragraph...",
    height=150
)

# Submit button
submit_button = st.button("Submit", type="primary")

# Predicted Words Section
st.subheader("Predicted Words")

# Prepare settings dictionary
settings = {
    'api_key': openai_api_key,
    'num_words': num_words,
    'topics': topics,
    'temperature': temperature,
    'tone': tone,
    'language': language,
    'exclude_words': exclude_words
}

# Display predictions
if submit_button and user_input:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key to get predictions")
    else:
        with st.spinner("Generating predictions..."):
            predicted_words, error = get_word_predictions(user_input, settings)
            
            if error:
                st.error(error)
            elif predicted_words:
                # Create the combined text with original input and predicted words
                predicted_text = " ".join(predicted_words)
                
                # Display the original text with predicted words highlighted
                st.markdown(
                    f"""
                    <div style="
                        padding: 20px;
                        border-radius: 10px;
                        background-color: #f0f2f6;
                        font-size: 18px;
                        line-height: 1.6;
                    ">
                        <span style="color: #262730;">{user_input}</span>
                        <span style="
                            color: #ffffff;
                            background-color: #ff4b4b;
                            padding: 4px 8px;
                            border-radius: 5px;
                            font-weight: bold;
                            margin-left: 5px;
                        ">{predicted_text}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
else:
    st.info("Enter text above and click Submit to get word predictions")
