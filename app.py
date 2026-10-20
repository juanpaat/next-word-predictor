import streamlit as st
from openai import OpenAI
import toml
import os
import math
import html

MODEL = "gpt-4o-mini"

# Continuations sampled in one request; the distinct ones become the ranked predictions
SAMPLES = 40

# Sampling above 1 spreads the samples over more distinct continuations. It doesn't
# change the probabilities shown: OpenAI reports the model's unscaled logprobs.
SAMPLING_TEMPERATURE = 1.5

# Starter texts offered before the first prediction
EXAMPLES = [
    "Once upon a time in",
    "Thank you for your email",
    "To install the package, run",
    "I can't believe we",
]

# Configure the page
st.set_page_config(
    page_title="Next Word Predictor",
    page_icon=":material/edit_note:",
    layout="centered",
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

def strip_icon(label):
    """Drop the leading emoji or flag from an option label ('🇬🇧 English' -> 'English')"""
    return label.split(" ", 1)[1] if " " in label else label

def api_key_input():
    """Ask for the OpenAI API key when it isn't in secrets"""
    st.subheader("OpenAI API key", anchor=False)
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Enter your OpenAI API key to enable predictions",
        label_visibility="collapsed"
    )
    st.caption(
        "Create one at [platform.openai.com](https://platform.openai.com/api-keys). "
        "It's only kept for this session."
    )
    return api_key

# Sidebar - Settings
with st.sidebar:
    st.header("Settings", anchor=False)
    st.caption("Changes apply the next time you press **Predict**.")

    # Without a key in secrets, entering one is the first thing to do
    openai_api_key = default_api_key if api_key_from_secrets else api_key_input()

    st.subheader("Prediction", anchor=False)

    # Prediction length
    num_words = st.slider(
        "Words per prediction",
        min_value=1,
        max_value=10,
        value=3,
        help="How many words each prediction adds to your text"
    )

    # Number of ranked predictions
    num_predictions = st.slider(
        "Number of predictions",
        min_value=1,
        max_value=10,
        value=5,
        help="How many alternative predictions to show, ranked by probability"
    )

    st.subheader("Style", anchor=False)

    # Topic Selector
    topics = st.selectbox(
        "Topic",
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

    # Tone Selector
    tone = st.selectbox(
        "Tone",
        options=["Formal", "Casual", "Creative", "Persuasive", "Informative"],
        help="The writing style the predictions follow"
    )

    # Language Selector. Flags are hidden because Windows shows them as letters.
    language = st.selectbox(
        "Output language",
        options=[
            "🇬🇧 English",
            "🇪🇸 Spanish",
            "🇫🇷 French",
            "🇩🇪 German",
            "🇵🇹 Portuguese"
        ],
        format_func=strip_icon,
        help="The language the predictions are written in, whatever language you type in"
    )

    st.divider()
    if api_key_from_secrets:
        st.badge("API key loaded", icon=":material/check:", color="green")
    st.caption(f"Model: {MODEL} · {SAMPLES} samples per request")

def count_words(text):
    """Count whitespace-separated words, ignoring chunks that are only punctuation"""
    return sum(1 for chunk in text.split() if any(c.isalnum() for c in chunk))

def continues_word(piece):
    """True if a token glues onto the word before it (e.g. 'tension' after ' hyper')"""
    if piece[:1].isspace():
        return False
    try:
        text = piece.decode("utf-8")
    except UnicodeDecodeError:
        return True  # Fragment of a multi-byte character
    return any(c.isalnum() for c in text)

def first_words(choice, num_words):
    """Cut a generated continuation down to its first num_words whole words.

    Returns (text, logprob) where logprob is the sum over every token in the text,
    so exp(logprob) is the probability of the whole phrase. Returns None if the
    continuation is too short or can't be used.
    """
    if not choice.logprobs or not choice.logprobs.content:
        return None

    buffer = b""
    logprob = 0.0
    for token_data in choice.logprobs.content:
        # Work in bytes: a token can hold part of a multi-byte character
        piece = bytes(token_data.bytes) if token_data.bytes is not None else token_data.token.encode("utf-8")
        text = buffer.decode("utf-8", errors="ignore")

        # Stop once we have enough words and this token starts something new
        if count_words(text) >= num_words and not continues_word(piece):
            return text.strip(), logprob

        # -9999 marks a token outside the top 20, whose probability is unknown
        if token_data.logprob <= -9999:
            return None

        buffer += piece
        logprob += token_data.logprob

    # Ran out of tokens: only complete if the model ended the text itself after enough words
    text = buffer.decode("utf-8", errors="ignore")
    if choice.finish_reason == "stop" and count_words(text) >= num_words:
        return text.strip(), logprob
    return None

def get_word_predictions(user_input, settings):
    """Get the most likely continuations of the user's text, ranked by probability"""

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

        # Make the model reply with the continuation only, never echoing the input
        system_content = (
            f"{system_prompt}\n\n"
            "The user message is an unfinished piece of text. Reply with only the words that come next, "
            "continuing exactly where the text stops. Keep writing for at least two more sentences "
            "instead of stopping early. Never repeat the text, and never add quotation marks, "
            "explanations or commentary. "
            f"Write in {output_language}, in a {settings['tone'].lower()} tone, suited to the topic of {topic}."
        )

        # Sample many continuations in ONE request. OpenAI's probabilities shift
        # between requests, so mixing requests would make them inconsistent.
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_input.strip()}
            ],
            temperature=SAMPLING_TEMPERATURE,
            n=SAMPLES,
            # Words average under two tokens; the margin lets the last word finish
            max_tokens=settings['num_words'] * 2 + 8,
            logprobs=True
        )

        # Group identical phrases, keeping the probability of each whole phrase
        phrases = {}
        for choice in response.choices:
            cut = first_words(choice, settings['num_words'])
            if cut and cut[0]:
                text, logprob = cut
                phrases.setdefault(text, []).append(math.exp(logprob))

        # Repeats of a phrase can differ slightly in reported probability, so average them
        ranked = sorted(
            ((text, sum(probs) / len(probs)) for text, probs in phrases.items()),
            key=lambda item: item[1],
            reverse=True
        )
        predictions = [
            {
                'rank': i + 1,
                'text': text,
                'probability': probability
            }
            for i, (text, probability) in enumerate(ranked[:settings['num_predictions']])
        ]

        if not predictions:
            return None, "The model didn't return a usable prediction. Please try again."

        return predictions, None

    except Exception as e:
        return None, f"Error: {str(e)}"

SUPERSCRIPTS = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")

def format_percent(percentage):
    """Three significant figures, with tiny values as '1.2 × 10⁻⁵%' instead of '1.2e-05%'"""
    text = f"{percentage:.3g}"
    if "e" in text:
        mantissa, exponent = text.split("e")
        text = f"{mantissa} × 10{str(int(exponent)).translate(SUPERSCRIPTS)}"
    return text + "%"

def describe_settings(settings):
    """One-line summary of the settings, e.g. '3 words · 5 predictions · General · Formal · English'"""
    return " · ".join([
        f"{settings['num_words']} word{'s' if settings['num_words'] != 1 else ''}",
        f"{settings['num_predictions']} prediction{'s' if settings['num_predictions'] != 1 else ''}",
        strip_icon(settings['topics']),
        settings['tone'],
        strip_icon(settings['language'])
    ])

def context_tail(text, max_words=6):
    """The end of the user's text, so each prediction can be read as its continuation"""
    words = text.split()
    tail = " ".join(words[-max_words:])
    return f"…{tail}" if len(words) > max_words else tail

def joins_without_space(prediction):
    """True if a prediction attaches straight onto the text, like ', and then' or '.'"""
    return prediction[:1] in ".,;:!?)]}…%’”" or prediction[:2] in ("'s", "’s")

def predictions_html(predictions, user_text):
    """Ranked list where each prediction continues the end of the user's text"""
    context = html.escape(context_tail(user_text))
    items = []
    for i, p in enumerate(predictions):
        percentage = p['probability'] * 100
        top = i == 0 and len(predictions) > 1
        separator = "" if joins_without_space(p['text']) else " "
        items.append(
            f'<li class="nwp-item{" is-top" if top else ""}" style="--i: {i}">'
            + ('<p class="nwp-top-label">Most likely</p>' if top else "")
            + f'<span class="nwp-rank">{p["rank"]}</span>'
            f'<p class="nwp-phrase"><span class="nwp-context">{context}</span>{separator}'
            f'<mark class="nwp-prediction">{html.escape(p["text"])}</mark></p>'
            f'<span class="nwp-percent">{format_percent(percentage)}</span>'
            # The bar uses an absolute 0 to 100% scale, so a full bar means certainty
            f'<div class="nwp-bar" aria-hidden="true"><span style="width: {min(percentage, 100):.4f}%"></span></div>'
            "</li>"
        )
    return f'<ol class="nwp-list" aria-label="Predictions ranked by probability">{"".join(items)}</ol>'

HOW_IT_WORKS = """
<ol class="nwp-steps">
  <li class="nwp-step">
    <span class="nwp-step-number">1</span>
    <p class="nwp-step-title">Write the start of a sentence</p>
    <p class="nwp-step-text">A single word, a phrase or a whole paragraph.</p>
  </li>
  <li class="nwp-step">
    <span class="nwp-step-number">2</span>
    <p class="nwp-step-title">Set the style</p>
    <p class="nwp-step-text">Choose the length, topic, tone and language in the sidebar.</p>
  </li>
  <li class="nwp-step">
    <span class="nwp-step-number">3</span>
    <p class="nwp-step-title">Compare the predictions</p>
    <p class="nwp-step-text">See the most likely continuations, each with the probability of the whole phrase.</p>
  </li>
</ol>
"""

READING_NOTES = """
- **One probability per prediction.** It is the probability of the whole phrase, however many words or tokens it has.
- **Longer predictions have lower probabilities.** Every extra word is another choice the model makes, so a 10-word prediction is almost always far less likely than a 1-word one.
- **The list won't add up to 100%.** It only shows the top predictions; the rest of the probability is spread over every other way the text could continue.
- **Fewer predictions than requested** means the model was so confident that its samples produced only that many distinct continuations.
- **Numbers can shift between runs.** OpenAI's API doesn't return exactly the same probabilities every time, so the same text can show slightly different percentages.
"""

def use_example(text):
    """Put an example in the text box and predict straight away"""
    st.session_state.user_text = text
    st.session_state.run_example = True

# Styles for the theme-aware custom elements
st.html(os.path.join(os.path.dirname(__file__), "style.css"))

# Main content
with st.container(key="hero"):
    st.title("Next Word Predictor", anchor=False)
    st.markdown(
        f"Write the start of a sentence and see how {MODEL} would most likely continue it. "
        "Every prediction comes with the probability of the whole phrase."
    )

# Prepare settings dictionary
settings = {
    'api_key': openai_api_key,
    'num_words': num_words,
    'num_predictions': num_predictions,
    'topics': topics,
    'tone': tone,
    'language': language
}

style_settings = {name: value for name, value in settings.items() if name != 'api_key'}

if "user_text" not in st.session_state:
    st.session_state.user_text = ""

# Text input area. Inside a form, Ctrl+Enter predicts as well as the button.
with st.container(key="composer"):
    with st.form("composer_form", border=False):
        st.text_area(
            "Your text",
            key="user_text",
            placeholder="Type a word, phrase, or paragraph...",
            height=140
        )
        with st.container(horizontal=True, vertical_alignment="center", gap="medium"):
            submit_button = st.form_submit_button("Predict", type="primary")
            st.caption(f":material/tune: {describe_settings(style_settings)}")

user_input = st.session_state.user_text
run_example = st.session_state.pop("run_example", False)
run_prediction = submit_button or run_example

# Results from the last prediction stay on screen until the next one
if run_prediction:
    if not user_input.strip():
        st.warning("Type the start of a sentence first.", icon=":material/edit:")
    elif not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar to get predictions", icon=":material/key:")
    else:
        with st.spinner(
            f"Sampling {SAMPLES} continuations from {MODEL}. This usually takes a few seconds.",
            show_time=True
        ):
            predictions, error = get_word_predictions(user_input, settings)

        if error:
            st.session_state.result = None
            st.error(error, icon=":material/error:")
        elif predictions:
            st.session_state.result = {
                'text': user_input,
                'settings': style_settings,
                'predictions': predictions
            }

result = st.session_state.get("result")

if result:
    predictions = result['predictions']
    with st.container(key="results"):
        st.subheader("Predictions", anchor=False)

        if result['settings'] != style_settings:
            st.info(
                f"These predictions used {describe_settings(result['settings'])}. "
                "Press **Predict** to apply your new settings.",
                icon=":material/history:"
            )

        st.html(predictions_html(predictions, result['text']))
        st.caption("Each probability is for the whole prediction, however many words or tokens it has.")

        if len(predictions) < result['settings']['num_predictions']:
            st.caption(
                f":material/info: Only {len(predictions)} distinct prediction(s) found: "
                "the model is very confident about how this text continues."
            )

        with st.expander("View as a table", icon=":material/table_rows:"):
            # Ranked table, one probability per prediction, shown as a number and a bar
            percentages = [p['probability'] * 100 for p in predictions]
            st.dataframe(
                {
                    "Rank": [p['rank'] for p in predictions],
                    "Prediction": [p['text'] for p in predictions],
                    "Probability": percentages,
                    "Bar": percentages
                },
                hide_index=True,
                width="stretch",
                column_config={
                    "Rank": st.column_config.NumberColumn(width="small"),
                    "Prediction": st.column_config.TextColumn(width="large"),
                    "Probability": st.column_config.NumberColumn(format="%.3g%%", width="small"),
                    "Bar": st.column_config.ProgressColumn(
                        " ",
                        min_value=0,
                        max_value=100,
                        format=" ",
                        width="medium"
                    )
                }
            )

        with st.expander("How to read these probabilities", icon=":material/help:"):
            st.markdown(READING_NOTES)

else:
    with st.container(key="empty"):
        if not openai_api_key:
            st.info("Add your OpenAI API key in the sidebar to start.", icon=":material/key:")

        st.subheader("Try an example", anchor=False)
        with st.container(key="examples", horizontal=True):
            for example in EXAMPLES:
                st.button(example, on_click=use_example, args=(example,))

        st.subheader("How it works", anchor=False)
        st.html(HOW_IT_WORKS)

st.divider()
st.caption(
    ":material/lock: Your text is sent to OpenAI to generate predictions and isn't saved by this app."
)
