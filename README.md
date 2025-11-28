# Next Word Predictor

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.51.0-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)

An intelligent web application that predicts what word comes next in your text. Powered by advanced artificial intelligence, this tool analyzes the context of what you've written and suggests the most natural words to follow. Whether you type a single word, a phrase, or an entire paragraph, the AI considers the meaning, flow, and style to provide relevant predictions.

This is a language model that understands context, tone, and subject matter. You can customize everything from the writing style (formal or casual) to the topic (technology, health, sports, etc.) to the level of creativity. The result is a powerful tool for exploring how modern AI processes and predicts human language, making it perfect for writers, language learners, educators, and anyone curious about artificial intelligence.

## 🎯 What Does This Tool Do?

Imagine you're writing and want to see what an AI thinks should come next. This tool analyzes your text and predicts the next 1-10 words that would naturally continue your sentence. It's like having autocomplete, but smarter and more customizable.

**Basic Examples:**
- You type: "The quick brown fox"
- The AI predicts: "jumps, over, the"

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
2. **The app sends your text to GPT-4o-mini** - Along with temperature settings to control creativity
3. **GPT-4o-mini analyzes the context** - The AI looks at your text and considers:
   - What words commonly follow in similar contexts
   - The probability of each possible next word
   - The temperature setting to balance predictability and creativity
4. **You get predictions** - The AI returns the most likely next tokens with their probabilities, highlighted in red

The AI doesn't just look at the last word—it understands the full context of your sentence to make smarter predictions.

## ⚙️ Understanding the Parameters

The sidebar contains several controls. Here's what each one does and their current implementation status:

### 📊 Number of Words to Predict (1-10) 
- **What it does:** Controls how many tokens the AI predicts
- **Example:** If set to 3, you get three token predictions. If set to 1, just one token.
- **Tip:** Start with 3-5 tokens to see a good range of possibilities
- **Note:** The model predicts tokens, which may be full words or parts of words

### 🎨 Temperature (0.0 - 1.0) 
- **What it does:** Controls how creative or predictable the AI is
- **Low values (0.0-0.3):** More predictable and focused. The AI picks the most obvious next tokens.
  - Example: "The weather is" → "good" (predictable)
- **Medium values (0.4-0.7):** Balanced between predictable and creative
- **High values (0.8-1.0):** More random and creative. The AI might surprise you with unexpected but valid choices.
  - Example: "The weather is" → "magnificent" (more creative)
- **Tip:** Use 0.7 for general use, lower for factual content, higher for creative writing

**Temperature Examples:**

*Input: "The future of artificial intelligence"*
- **Temperature 0.1:** → " is" (highly predictable, most common continuation)
- **Temperature 0.5:** → " will be" (balanced, natural flow)
- **Temperature 0.9:** → " depends on" (more creative, less predictable)

*Input: "In conclusion, we can"*
- **Temperature 0.2:** → " see that" (formal, expected)
- **Temperature 0.7:** → " confidently say" (moderate creativity)
- **Temperature 1.0:** → " observe remarkable" (highly creative, unexpected)

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
   - Number of tokens to predict (1-10)
   - Temperature for creativity control (0.0-1.0)
   - Topic/Domain for context
   - Tone for writing style
   - Output Language for multilingual predictions
3. **Click "Submit"** to get predictions
4. **View the results:**
   - Token sequence table showing position, cumulative tokens, and probability for each token
   - Overall sequence probability
   - Your original text in gray with predicted tokens highlighted in red
5. **Experiment!** Try changing different parameters to see how predictions change

## 🛠️ Technical Details

- **Framework:** Built with Streamlit (Python web framework)
- **AI Model:** OpenAI's GPT-4o-mini
- **Model Type:** Large Language Model (LLM) trained on diverse text data
- **API:** Communicates with OpenAI's servers to generate predictions
- **Features:**
  - Token-level predictions with probability scores
  - Log probabilities for each predicted token
  - Overall sequence probability calculation
  - Supports temperature control for creativity adjustment
  - Top 5 token alternatives available internally (not displayed in UI)

## 🔐 Privacy & Security

- Text you enter is sent to OpenAI's servers for processing
- No data is stored permanently by this application

---

**Author:** JuanBioData  

