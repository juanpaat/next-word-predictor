# Next Word Predictor

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.51.0-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)

An intelligent web application that predicts what word comes next in your text. Powered by advanced artificial intelligence, this tool analyzes the context of what you've written and suggests the most natural words to follow. Whether you type a single word, a phrase, or an entire paragraph, the AI considers the meaning, flow, and style to provide relevant predictions.

This is a language model that understands context, tone, and subject matter. You can customize everything from the writing style (formal or casual) to the topic (technology, health, sports, etc.) and the output language. The result is a powerful tool for exploring how modern AI processes and predicts human language, making it perfect for writers, language learners, educators, and anyone curious about artificial intelligence.

## 🎯 What Does This Tool Do?

Imagine you're writing and want to see what an AI thinks should come next. This tool analyses your text and predicts the most likely ways to continue it, each 1 to 10 words long, ranked by how probable the model thinks they are. It's like having autocomplete, but smarter and more customisable.

**Basic Example** (3 words per prediction):

You type: "Thank you for your email"

| Rank | Prediction | Probability |
|---|---|---|
| 1 | I appreciate your | 46.8% |
| 2 | regarding the upcoming | 10.8% |
| 3 | regarding our recent | 7.74% |
| 4 | regarding the recent | 7.45% |
| 5 | and for bringing | 5.88% |

**More Examples:**

*Creative Writing:*
- Input: "Once upon a time in"
- Prediction: "a land far away"

*Technical Writing:*
- Input: "To install the package, run"
- Prediction: "pip install in your"

*Business Communication:*
- Input: "Thank you for your email"
- Prediction: ". I will review"

*Conversational:*
- Input: "I can't believe we"
- Prediction: "finally made it to"

The predictions adapt to the context you provide, understanding different writing styles and subject matters based on the patterns the AI has learned.

## 🤖 How It Works

This application uses **GPT-4o-mini**, a powerful language model created by OpenAI. Think of it as an AI that has read millions of books, articles, and websites, learning patterns in how people write and speak.

### The Prediction Process:

1. **You type your text** - Can be a word, phrase, or entire paragraph
2. **The app sends your text to GPT-4o-mini** - Along with your topic, tone and language settings, and an instruction to continue the text without repeating it
3. **GPT-4o-mini writes 40 possible continuations in a single request** - For every token it writes, it also reports the probability it gave that token. The app samples slightly more adventurously than usual so that more distinct alternatives turn up; this doesn't change the probabilities reported.
4. **The app cuts each continuation to the number of words you asked for** - Words the model split into several tokens are kept whole
5. **Identical predictions are merged and ranked** - A prediction's probability is the product of the probabilities of all its tokens, so it is the probability of the whole phrase
6. **You get the ranked list** - Each prediction with its probability, as a number and as a bar

The AI doesn't just look at the last word: it understands the full context of your sentence to make smarter predictions.

### 📈 Reading the Probabilities

- **One probability per prediction.** It is the probability of the whole phrase, however many words or tokens it has.
- **Longer predictions have lower probabilities.** Every extra word is another choice the model has to make, so a 10-word prediction is almost always far less likely than a 1-word one.
- **The list won't add up to 100%.** It only shows the top predictions; the rest of the probability is spread over every other way the text could continue.
- **Fewer predictions than requested** means the model was so confident that its 40 attempts produced only that many distinct continuations. For "The quick brown fox" it is essentially 100% sure of "jumps over the".
- **Numbers can shift between runs.** OpenAI's API doesn't return exactly the same probabilities every time, even for identical requests, so submitting the same text again can show somewhat different percentages.

## ⚙️ Understanding the Parameters

The sidebar contains several controls. Here's what each one does and their current implementation status:

### 📏 Words per Prediction (1-10)
- **What it does:** Sets how long each prediction is, in whole words
- **Example:** If set to 3, every prediction continues your text by three words
- **Tip:** 1 to 3 words is best for comparing clear alternatives. Longer predictions vary more, so each one is less likely.
- **Note:** The model works in tokens (often parts of words), but the app always returns whole words and never cuts one off

### 📊 Number of Predictions (1-10)
- **What it does:** Sets how many alternative predictions to show, ranked from most to least likely
- **Tip:** 5 gives a good overview of what the model is considering

### 📚 Topic/Domain 
- **What it does:** Tells the AI what subject area you're writing about to contextualize predictions
- **Available topics:** General, Technology, Health, Education, Finance, Entertainment, Science, Travel, Food, Sports, History
- **Why it matters:** The same sentence can continue differently based on the topic context
- **Tip:** Choose the topic that matches your writing context for better predictions

**Topic/Domain Examples:**

*Input: "The system is"*
- **Topic: Technology** → "processing the data" (tech-specific terms)
- **Topic: Health** → "functioning properly and" (medical context)
- **Topic: Finance** → "showing strong performance" (financial terms)
- **Topic: Science** → "demonstrating consistent results" (scientific language)

*Input: "This breakthrough will"*
- **Topic: Technology** → "revolutionize software development"
- **Topic: Health** → "improve patient outcomes significantly"
- **Topic: Science** → "advance our understanding of"

### 🎭 Tone 
- **What it does:** Adjusts the style and formality of predictions
- **Options:** Formal, Casual, Creative, Persuasive, Informative
- **Why it matters:** Different tones produce different writing styles
- **Tip:** Match the tone to your writing purpose

**Tone Examples:**

*Input: "We need to discuss"*
- **Formal Tone** → "the matter at our" (professional, business-like)
- **Casual Tone** → "this when you're free" (relaxed, conversational)
- **Creative Tone** → "the elephant in the" (idiomatic, imaginative)
- **Persuasive Tone** → "why this solution is" (convincing, compelling)
- **Informative Tone** → "several key points about" (educational, clear)

*Input: "The results show"*
- **Formal Tone** → "a statistically significant correlation"
- **Casual Tone** → "some pretty interesting stuff"
- **Creative Tone** → "a fascinating tapestry of"
- **Persuasive Tone** → "compelling evidence that proves"
- **Informative Tone** → "three main findings concerning"

### 🌍 Output Language 
- **What it does:** Predicts words in the selected language
- **Available languages:** English, Spanish, French, German, Portuguese
- **Why it matters:** You can type in one language and get predictions in another, or maintain consistency in your chosen language
- **Tip:** Great for multilingual writing or learning how phrases continue in different languages

**Output Language Examples:**

*Input: "Good morning, how are"*
- **English** → "you doing today?"
- **Spanish** → "estás hoy?" (you today?)
- **French** → "allez-vous aujourd'hui?" (are you today?)
- **German** → "geht es dir?" (goes it to-you?)
- **Portuguese** → "você está hoje?" (you are today?)

*Input: "I want to"*
- **English** → "share some thoughts about"
- **Spanish** → "compartir algunas ideas sobre"
- **French** → "partager quelques idées sur"
- **German** → "einige Gedanken teilen über"
- **Portuguese** → "compartilhar algumas ideias sobre"

**Note:** This enables cross-language writing assistance where you start in one language and get completions in another.

## 💡 How to Use the Tool

1. **Enter your text** in the main text box (word, phrase, or paragraph)
2. **Adjust the settings** in the sidebar:
   - Words per prediction (1-10)
   - Number of predictions (1-10)
   - Topic/Domain for context
   - Tone for writing style
   - Output Language for multilingual predictions
3. **Click "Predict"** (or press Ctrl+Enter in the text box) to get predictions. New to the tool? Click one of the example sentences to fill the box and predict in one go.
4. **View the results:**
   - Predictions ranked by probability, each shown continuing the end of your text, with one probability for the whole prediction and a bar showing it visually (a full bar is 100%)
   - "View as a table" shows the same predictions as a table you can sort, copy or download
   - Results stay on screen when you change a setting, with a note that they used the old settings until you press Predict again
5. **Experiment!** Try changing different parameters to see how predictions change

The app follows your system's light or dark mode; you can switch it from the menu in the top-right corner (Settings).

## 🛠️ Technical Details

- **Framework:** Built with Streamlit (Python web framework)
- **Design:** Light and dark theme in `.streamlit/config.toml`; styling for the predictions list and layout in `style.css`
- **AI Model:** OpenAI's GPT-4o-mini
- **Model Type:** Large Language Model (LLM) trained on diverse text data
- **API:** Communicates with OpenAI's servers to generate predictions
- **Features:**
  - Whole-word predictions built from the model's tokens
  - One probability per prediction, calculated from the log probabilities of all its tokens
  - All predictions sampled in a single request, so their probabilities are consistent with each other
  - Ranked from most to least likely

## 🔐 Privacy & Security

- Text you enter is sent to OpenAI's servers for processing
- No data is stored permanently by this application

---

**Author:** JuanBioData  

