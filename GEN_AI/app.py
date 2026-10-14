import streamlit as st
import ollama

# Page configuration
st.set_page_config(
    page_title="Ollama AI Text Assistant",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Ollama AI Text Assistant")
st.write("Generate text, answer questions, summarize text, and translate languages.")

# Function to generate text
def generate_text(prompt):
    response = ollama.generate(
        model="llama3.2:1b",
        prompt=prompt
    )
    return response["response"]


# Select a task
task = st.selectbox(
    "Choose a task",
    [
        "Text Generation",
        "Question Answering",
        "Text Summarization",
        "Text Translation"
    ]
)

# Text input
if task == "Text Generation":
    text = st.text_area("Enter your prompt")

elif task == "Question Answering":
    text = st.text_area("Enter your question")

elif task == "Text Summarization":
    text = st.text_area("Enter the text to summarize")

elif task == "Text Translation":
    text = st.text_area("Enter the text to translate")
    language = st.text_input("Enter the target language")

# Generate button
if st.button("Generate Result"):

    if not text.strip():
        st.warning("Please enter some text.")

    elif task == "Text Translation" and not language.strip():
        st.warning("Please enter the target language.")

    else:
        # Create the appropriate prompt
        if task == "Text Generation":
            prompt = text

        elif task == "Question Answering":
            prompt = f"Answer the following question clearly: {text}"

        elif task == "Text Summarization":
            prompt = f"Summarize the following text in one sentence: {text}"

        elif task == "Text Translation":
            prompt = f"Translate the following text into {language}: {text}"

        # Generate the result
        try:
            with st.spinner("Generating response..."):
                result = generate_text(prompt)

            st.subheader("Result")
            st.write(result)

        except Exception as e:
            st.error(
                "Unable to connect to Ollama. "
                "Make sure Ollama is running and the model is installed."
            )