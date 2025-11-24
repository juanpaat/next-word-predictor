# Next Word Predictor

An intelligent web application that predicts what word comes next in your text. Powered by advanced artificial intelligence, this tool analyzes the context of what you've written and suggests the most natural words to follow. Whether you type a single word, a phrase, or an entire paragraph, the AI considers the meaning, flow, and style to provide relevant predictions.

This is a language model that understands context, tone, and subject matter. You can customize everything from the writing style (formal or casual) to the topic (technology, health, sports, etc.) to the level of creativity. The result is a powerful tool for exploring how modern AI processes and predicts human language, making it perfect for writers, language learners, educators, and anyone curious about artificial intelligence.

## 🎯 What Does This Tool Do?

Imagine you're writing and want to see what an AI thinks should come next. This tool analyzes your text and predicts the next 1-10 words that would naturally continue your sentence. It's like having autocomplete, but smarter and more customizable.

**Example:**
- You type: "The quick brown fox"
- The AI predicts: "jumps, over, the"

The predictions change based on the context you provide—whether you want formal language, creative writing, or technical content.

## 🤖 How It Works (The Simple Version)

This application uses **GPT-4o-mini**, a powerful language model created by OpenAI. Think of it as an AI that has read millions of books, articles, and websites, learning patterns in how people write and speak.

### The Prediction Process:

1. **You type your text** - Can be a word, phrase, or entire paragraph
2. **The app builds a special request** - It packages your text along with your chosen settings (topic, tone, language, etc.)
3. **GPT-4o-mini analyzes the context** - The AI looks at your text and considers:
   - What words commonly follow in similar contexts
   - The topic you selected (Technology, Health, Sports, etc.)
   - The tone you want (Formal, Casual, Creative, etc.)
   - The language you want predictions in
4. **You get predictions** - The AI returns the most likely next words, highlighted in red

The AI doesn't just look at the last word—it understands the full context of your sentence to make smarter predictions.

## ⚙️ Understanding the Parameters

The sidebar contains several controls that change how the AI makes predictions. Here's what each one does:

### 📊 Number of Words to Predict (1-10)
- **What it does:** Controls how many words the AI predicts
- **Example:** If set to 3, you get three word predictions. If set to 1, just one word.
- **Tip:** Start with 3-5 words to see a good range of possibilities

### 🎨 Temperature (0.0 - 1.0)
- **What it does:** Controls how creative or predictable the AI is
- **Low values (0.0-0.3):** More predictable and focused. The AI picks the most obvious next words.
  - Example: "The weather is" → "good" (predictable)
- **Medium values (0.4-0.7):** Balanced between predictable and creative
- **High values (0.8-1.0):** More random and creative. The AI might surprise you with unexpected but valid choices.
  - Example: "The weather is" → "magnificent" (more creative)
- **Tip:** Use 0.7 for general use, lower for factual content, higher for creative writing

### 📚 Topic/Domain
- **What it does:** Tells the AI what subject area you're writing about
- **Available topics:** General, Technology, Health, Education, Finance, Entertainment, Science, Travel, Food, Sports, History
- **Why it matters:** The same sentence can continue differently based on topic
  - Topic: Technology → "The system is" → "processing, data, successfully"
  - Topic: Health → "The system is" → "recovering, healthy, functioning"
- **Tip:** Choose the topic that matches your writing context for better predictions

### 🎭 Tone
- **What it does:** Adjusts the style and formality of predictions
- **Options:**
  - **Formal:** Professional, business-like language
  - **Casual:** Relaxed, everyday conversation
  - **Creative:** Artistic, imaginative, unexpected
  - **Persuasive:** Convincing, compelling language
  - **Informative:** Clear, educational, explanatory
- **Tip:** Match the tone to your writing purpose

### 🌍 Output Language
- **What it does:** Predicts words in the selected language
- **Available languages:** English, Spanish, French, German, Portuguese
- **Note:** You can type in English and get predictions in Spanish, or vice versa
- **Tip:** Great for learning how phrases continue in different languages

### 🚫 Exclude Words
- **What it does:** Prevents specific words from appearing in predictions
- **How to use:** Type words separated by commas (e.g., "very, really, just")
- **Why use it:** Avoid overused words or words that don't fit your context
- **Tip:** Leave blank if you don't need to exclude anything

## 💡 How to Use the Tool

1. **Enter your text** in the main text box (word, phrase, or paragraph)
2. **Adjust the settings** in the sidebar to fit your needs
3. **Click "Submit"** to get predictions
4. **View the results** - Your original text appears in gray, predicted words in red
5. **Experiment!** Try changing parameters to see how predictions change

## 🛠️ Technical Details

- **Framework:** Built with Streamlit (Python web framework)
- **AI Model:** OpenAI's GPT-4o-mini
- **Model Type:** Large Language Model (LLM) trained on diverse text data
- **API:** Communicates with OpenAI's servers to generate predictions
- **Languages Supported:** English, Spanish, French, German, Portuguese

## 🔐 Privacy & Security

- Your OpenAI API key is stored locally in a `secrets.toml` file
- This file is excluded from version control for security
- Text you enter is sent to OpenAI's servers for processing
- No data is stored permanently by this application

## 📊 Use Cases

- **Writers:** Get inspiration for continuing sentences
- **Language Learners:** See natural word progressions in different languages
- **Content Creators:** Explore different tones and styles
- **Educators:** Demonstrate how AI understands language context
- **Curious Minds:** Experiment with how AI predicts human language

## 🎓 Learning Opportunity

This project demonstrates:
- Integration with modern AI APIs (OpenAI)
- Building interactive web applications with Streamlit
- Natural Language Processing (NLP) concepts
- Parameter tuning and its effects on AI output
- Creating user-friendly interfaces for complex technology

---

**Project Type:** Data Science Portfolio Project  
**Author:** Juan Pablo  
**Purpose:** Educational tool to explore AI-powered text prediction  
**Technology Stack:** Python, Streamlit, OpenAI GPT-4o-mini
