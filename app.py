import streamlit as st
from openai import OpenAI
import toml
import os
import math

# Configure the page
st.set_page_config(
    page_title="Next Word Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
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
            "🌐 General",
            "💻 Technology",
            "🏥 Health",
            "📚 Education",
            "💰 Finance",
            "🎬 Entertainment",
            "🔬 Science",
            "✈️ Travel",
            "🍔 Food",
            "⚽ Sports",
            "📜 History"
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

def get_word_predictions(user_input, settings):
    """Get word predictions from OpenAI based on user input and settings"""
    
    if not settings['api_key']:
        return None, "Please enter your OpenAI API key in the sidebar"
    
    try:
        client = OpenAI(api_key=settings['api_key'])
        
        # Map language display to actual language name
        lang_map = {
            "🇬🇧 English": "English",
            "🇪🇸 Spanish": "Spanish",
            "🇫🇷 French": "French",
            "🇩🇪 German": "German",
            "🇵🇹 Portuguese": "Portuguese"
        }
        output_language = lang_map.get(settings['language'], "English")
        
        # Extract clean topic name (remove emoji)
        topic = settings['topics'].split(" ", 1)[1] if " " in settings['topics'] else settings['topics']
        
        # Build comprehensive prompt with all settings
        system_content = f"You are a next-word prediction assistant. Continue the given text naturally in a {settings['tone'].lower()} tone, considering the topic/domain of {topic}. Provide your response in {output_language}."
        
        prompt = f"Continue this text with the next {settings['num_words']} word(s): {user_input}"
        
        # Call OpenAI API with logprobs enabled
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            temperature=settings['temperature'],
            max_tokens=settings['num_words'],
            logprobs=True,
            top_logprobs=5
        )
        
        # Extract all tokens generated
        all_tokens_data = response.choices[0].logprobs.content
        
        # Build results for each token position
        token_results = []
        overall_logprob = 0  # Sum of logprobs for overall probability
        
        for token_idx, token_data in enumerate(all_tokens_data):
            # Get top 5 alternatives for this token position
            top_tokens = token_data.top_logprobs
            
            # The actual selected token (first in the list)
            selected_token = top_tokens[0].token
            selected_logprob = top_tokens[0].logprob
            
            # Add to overall logprob
            overall_logprob += selected_logprob
            
            # Extract all alternatives
            alternatives = []
            for i, item in enumerate(top_tokens[:5]):
                token = item.token
                prob = math.exp(item.logprob)  # convert logprob → probability
                alternatives.append({
                    'rank': i + 1,
                    'token': token,
                    'probability': prob
                })
            
            token_results.append({
                'position': token_idx + 1,
                'selected_token': selected_token,
                'alternatives': alternatives
            })
        
        # Calculate overall probability of the entire sequence
        overall_probability = math.exp(overall_logprob)
        
        return {
            'tokens': token_results,
            'overall_probability': overall_probability,
            'num_tokens': len(token_results)
        }, None
        
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



# Prepare settings dictionary
settings = {
    'api_key': openai_api_key,
    'num_words': num_words,
    'topics': topics,
    'temperature': temperature,
    'tone': tone,
    'language': language
}

# Display predictions
if submit_button and user_input:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key to get predictions")
    else:
        with st.spinner("Generating predictions..."):
            result, error = get_word_predictions(user_input, settings)
            
            if error:
                st.error(error)
            elif result:
                # Display the sequence of tokens with their probabilities
                st.markdown("### Generated Token Sequence:")
                
                # Create header
                col1, col2, col3 = st.columns([1, 3, 2])
                with col1:
                    st.markdown("**Position**")
                with col2:
                    st.markdown("**Token**")
                with col3:
                    st.markdown("**Probability**")
                
                st.markdown("---")
                
                # Display each token in the sequence
                cumulative_tokens = []
                for token_info in result['tokens']:
                    # Get the selected token's probability (rank 1)
                    selected_prob = token_info['alternatives'][0]['probability']
                    
                    # Build cumulative token sequence with individual backticks and spaces
                    cumulative_tokens.append(token_info['selected_token'])
                    cumulative_text = " ".join([f"`{token}`" for token in cumulative_tokens])
                    
                    col1, col2, col3 = st.columns([1, 3, 2])
                    with col1:
                        st.markdown(f"**{token_info['position']}**")
                    with col2:
                        st.markdown(cumulative_text)
                    with col3:
                        st.markdown(f"*{selected_prob:.5f}*")
                
                st.markdown("---")
                
                # Display overall sequence probability
                st.markdown(f"### Overall Sequence Probability: **{result['overall_probability']:.6f}**")
                st.markdown(f"*Generated {result['num_tokens']} token(s)*")
                
                st.markdown("---")
                
                # Build the complete predicted text from all tokens
                predicted_text = "".join([token_info['selected_token'] for token_info in result['tokens']])
                
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
