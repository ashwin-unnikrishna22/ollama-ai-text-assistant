import time

import streamlit as st
import ollama

# ------------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Ollama AI Text Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Custom styling
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 2rem; max-width: 820px;}

    .hero {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        padding: 2.2rem 2rem;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.30);
        margin-bottom: 1.5rem;
    }
    .hero h1 {margin: 0; font-size: 2.2rem; font-weight: 800; color: #ffffff;}
    .hero p {margin: 0.5rem 0 0 0; font-size: 1.05rem; color: #ffffff; opacity: 0.92;}

    .task-card {
        background: rgba(124, 58, 237, 0.08);
        border-left: 5px solid #7c3aed;
        padding: 0.9rem 1.1rem;
        border-radius: 10px;
        margin: 0.5rem 0 1rem 0;
        font-size: 0.97rem;
    }

    .result-card {
        background: rgba(79, 70, 229, 0.07);
        border: 1px solid rgba(124, 58, 237, 0.35);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        line-height: 1.65;
        margin-top: 0.5rem;
        white-space: pre-wrap;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.35);
        color: #ffffff;
    }

    .footer-note {
        text-align: center;
        font-size: 0.85rem;
        opacity: 0.65;
        margin-top: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Task definitions
# ------------------------------------------------------------------
TASKS = {
    "Text Generation": {
        "icon": "✍️",
        "desc": "Write stories, emails, ideas, or any creative content from a prompt.",
        "label": "Enter your prompt",
        "placeholder": "e.g. Write a short motivational message for a student...",
    },
    "Question Answering": {
        "icon": "❓",
        "desc": "Ask a question and get a clear, direct answer.",
        "label": "Enter your question",
        "placeholder": "e.g. What is the difference between AI and machine learning?",
    },
    "Text Summarization": {
        "icon": "📝",
        "desc": "Paste a long passage and get a concise one-sentence summary.",
        "label": "Enter the text to summarize",
        "placeholder": "Paste the text you want summarized here...",
    },
    "Text Translation": {
        "icon": "🌐",
        "desc": "Translate text into any language you specify.",
        "label": "Enter the text to translate",
        "placeholder": "Type or paste the text to translate...",
    },
}

# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    model_name = st.text_input(
        "Model name",
        value="llama3.2:1b",
        help="Must already be pulled, e.g. `ollama pull llama3.2:1b`",
    )
    temperature = st.slider(
        "Creativity (temperature)",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.1,
        help="Lower = more focused and predictable. Higher = more creative.",
    )

    st.divider()
    st.markdown("## 📚 About")
    st.caption(
        "A local AI assistant powered by **Ollama** and **Streamlit**. "
        "Everything runs on your own machine, so your text stays private."
    )

    st.divider()
    if st.button("🗑️ Clear history"):
        st.session_state.history = []
        st.rerun()


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------
def generate_text(prompt, model, temp):
    response = ollama.generate(
        model=model,
        prompt=prompt,
        options={"temperature": temp},
    )
    return response["response"]


# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🤖 Ollama AI Text Assistant</h1>
        <p>Generate text, answer questions, summarize content, and translate languages.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Task selection
# ------------------------------------------------------------------
task = st.selectbox(
    "Choose a task",
    list(TASKS.keys()),
    format_func=lambda t: f"{TASKS[t]['icon']}  {t}",
)
cfg = TASKS[task]

st.markdown(
    f"<div class='task-card'><b>{cfg['icon']} {task}</b><br>{cfg['desc']}</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Input
# ------------------------------------------------------------------
text = st.text_area(cfg["label"], placeholder=cfg["placeholder"], height=170)
st.caption(f"{len(text)} characters · {len(text.split())} words")

language = ""
if task == "Text Translation":
    language = st.text_input(
        "Target language",
        placeholder="e.g. Malayalam, Hindi, French, Spanish",
    )

# ------------------------------------------------------------------
# Generate
# ------------------------------------------------------------------
if st.button("✨ Generate Result"):

    if not text.strip():
        st.warning("Please enter some text.")

    elif task == "Text Translation" and not language.strip():
        st.warning("Please enter the target language.")

    else:
        if task == "Text Generation":
            prompt = text
        elif task == "Question Answering":
            prompt = f"Answer the following question clearly: {text}"
        elif task == "Text Summarization":
            prompt = f"Summarize the following text in one sentence: {text}"
        else:
            prompt = f"Translate the following text into {language}: {text}"

        try:
            start = time.time()
            with st.spinner("Generating response..."):
                result = generate_text(prompt, model_name.strip(), temperature)
            elapsed = time.time() - start

            st.success(f"Done in {elapsed:.1f} seconds")
            st.subheader("📄 Result")
            st.markdown(
                f"<div class='result-card'>{result}</div>",
                unsafe_allow_html=True,
            )

            with st.expander("📋 Copy-friendly version"):
                st.code(result, language=None)

            st.download_button(
                "⬇️ Download result (.txt)",
                data=result,
                file_name="result.txt",
                mime="text/plain",
            )

            st.session_state.history.insert(
                0, {"task": task, "input": text, "output": result}
            )

        except Exception as e:
            st.error(
                "Unable to connect to Ollama. "
                "Make sure Ollama is running and the model is installed."
            )
            with st.expander("Technical details"):
                st.code(str(e))
                st.caption(f"To install the model, run: `ollama pull {model_name.strip()}`")

# ------------------------------------------------------------------
# History
# ------------------------------------------------------------------
if st.session_state.history:
    st.divider()
    st.subheader("🕘 Recent activity")
    for item in st.session_state.history[:5]:
        label = f"{TASKS[item['task']]['icon']} {item['task']}: {item['input'][:60]}"
        with st.expander(label, expanded=False):
            st.markdown("**Input**")
            st.write(item["input"])
            st.markdown("**Output**")
            st.write(item["output"])

st.markdown(
    "<div class='footer-note'>Built with Streamlit and Ollama · Runs locally</div>",
    unsafe_allow_html=True,
)