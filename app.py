import requests
import streamlit as st

# ==========================================
# STUDYMATE AI
# Personal AI Study Assistant
# Python + Streamlit + Ollama
# ==========================================

# PAGE CONFIGURATION

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="wide"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #f5f7fc;
    color: #1e293b;
}

/* Main headings */
h1, h2, h3, h4 {
    color: #263b80 !important;
}

/* Normal text */
p, span, label, li {
    color: #1e293b;
}

/* Quiz and markdown content */
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown strong {
    color: #1e293b !important;
}

/* White content cards */
.feature-card {
    background-color: #ffffff;
    padding: 24px;
    border-radius: 15px;
    border: 1px solid #dbe3f0;
    min-height: 150px;
    margin-bottom: 15px;
    color: #1e293b;
}

.feature-card h3 {
    color: #263b80 !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
}

/* Select boxes */
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff;
    color: #1e293b;
}

/* Buttons */
.stButton button {
    background-color: #4056a1;
    color: #ffffff !important;
    border-radius: 10px;
    font-weight: 600;
    border: none;
}

/* Button hover */
.stButton button:hover {
    background-color: #263b80;
    color: #ffffff !important;
}

/* Quiz radio options */
.stRadio label,
.stRadio label p {
    color: #1e293b !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #eaf0ff;
}

/* Download buttons */
.stDownloadButton button {
    background-color: #16a34a;
    color: #ffffff !important;
    border-radius: 10px;
}

/* Footer */
footer {
    visibility: hidden;
}
</style>

""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================
# AI RESPONSE FUNCTION
# ==========================================

def generate_response(prompt, history=None, system_prompt=None):

    messages = [
        {
            "role": "system",
            "content": system_prompt or
            "You are StudyMate AI, a helpful academic tutor. "
            "Explain topics clearly and provide examples."
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. Please open the Ollama "
            "application and try again."
        )

    except requests.exceptions.Timeout:
        return "The AI response timed out. Please try again."

    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"

    except (KeyError, ValueError):
        return "Unable to process the AI response."


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🎓 StudyMate AI")

    st.caption("Your Personal AI Study Assistant")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "💬 AI Chatbot",
            "📝 Notes Summarizer",
            "🧠 Quiz Generator",
            "📚 Concept Explainer"
        ]
    )

    st.divider()

    st.info(
        "Learn smarter and improve your knowledge "
        "with your personal AI assistant."
    )

    st.caption("Powered by Llama 3.2")


# =========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">'
        'Welcome to StudyMate AI 🎓</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">'
        'Your intelligent companion for smarter learning.'
        '</p>',
        unsafe_allow_html=True
    )

    st.success("Your AI learning workspace is ready!")

    st.subheader("Explore Your Learning Tools")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="feature-card">
            <h3>💬 AI Chatbot</h3>
            <p>Ask academic questions and receive
            helpful AI-generated answers.</p>
        </div>

        <div class="feature-card">
            <h3>📝 Notes Summarizer</h3>
            <p>Convert lengthy notes into clear
            and concise summaries.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Quiz Generator</h3>
            <p>Create practice questions to
            test your knowledge.</p>
        </div>

        <div class="feature-card">
            <h3>📚 Concept Explainer</h3>
            <p>Understand difficult concepts
            through simple explanations.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Project Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("AI Features", "4")
    c2.metric("AI Model", "Llama 3.2")
    c3.metric("Framework", "Streamlit")


# ==========================================
# AI CHATBOT
# ==========================================

elif page == "💬 AI Chatbot":

    st.title("💬 AI Academic Chatbot")

    st.write("Ask any academic question.")

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(
        "Ask your question here..."
    )

    if user_input:

        with st.chat_message("user"):
            st.markdown(user_input)

        previous_history = list(
            st.session_state.chat_history
        )

        with st.chat_message("assistant"):

            with st.spinner("StudyMate AI is thinking..."):

                answer = generate_response(
                    user_input,
                    previous_history
                )

                st.markdown(answer)

        st.session_state.chat_history.extend([
            {
                "role": "user",
                "content": user_input
            },
            {
                "role": "assistant",
                "content": answer
            }
        ])


# ==========================================
# NOTES SUMMARIZER
# ==========================================

elif page == "📝 Notes Summarizer":

    st.title("📝 AI Notes Summarizer")

    st.write(
        "Convert your lengthy study notes into summaries."
    )

    notes = st.text_area(
        "Paste your study notes:",
        height=250,
        placeholder="Paste your notes here..."
    )

    length = st.selectbox(
        "Choose summary length:",
        ["Short", "Medium", "Detailed"]
    )

    if st.button("✨ Summarize Notes", type="primary"):

        if not notes.strip():

            st.warning("Please enter your notes.")

        else:

            prompt = f"""
            Summarize the following study notes.

            Summary length: {length}

            Requirements:
            - Use headings.
            - Use bullet points.
            - Highlight key information.
            - Preserve important facts.
            - Do not invent information.

            STUDY NOTES:
            {notes}
            """

            with st.spinner("Summarizing notes..."):

                result = generate_response(prompt)

            st.subheader("📖 Generated Summary")

            st.markdown(
                f"""
                <div style="
                    background-color: #ffffff;
                    color: #1e293b;
                    padding: 25px;
                    border-radius: 15px;
                    border: 1px solid #dbe3f0;
                    line-height: 1.8;
                ">
        {result}
    </div>
    """,
    unsafe_allow_html=True
)

            st.download_button(
                "⬇️ Download Summary",
                data=result,
                file_name="studymate_summary.txt",
                mime="text/plain"
            )


# ==========================================
# QUIZ GENERATOR
# ==========================================

elif page == "🧠 Quiz Generator":

    st.title("🧠 AI Quiz Generator")

    st.write(
        "Generate multiple-choice questions "
        "from your favourite academic topics."
    )

    topic = st.text_input(
        "Enter your topic:",
        placeholder="Example: Python Programming"
    )

    number = st.slider(
        "Number of questions:",
        3, 10, 5
    )

    difficulty = st.selectbox(
        "Select difficulty:",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("🚀 Generate Quiz", type="primary"):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            prompt = f"""
            Create exactly {number} multiple-choice
            questions about {topic}.

            Difficulty: {difficulty}

            For every question provide:
            1. Question.
            2. Four options A, B, C and D.
            3. Correct answer.
            4. Short explanation.

            Put the answer key after all questions.
            Make the questions educational and accurate.
            """

            with st.spinner("Generating quiz..."):

                result = generate_response(prompt)

            st.subheader("📋 Your Practice Quiz")

            st.markdown(result)

            st.download_button(
                "⬇️ Download Quiz",
                data=result,
                file_name="studymate_quiz.txt",
                mime="text/plain"
            )


# ==========================================
# CONCEPT EXPLAINER
# ==========================================

elif page == "📚 Concept Explainer":

    st.title("📚 AI Concept Explainer")

    st.write(
        "Learn difficult academic concepts in simple language."
    )

    concept = st.text_input(
        "Enter a concept:",
        placeholder="Example: Machine Learning"
    )

    level = st.selectbox(
        "Select your knowledge level:",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("💡 Explain Concept", type="primary"):

        if not concept.strip():

            st.warning("Please enter a concept.")

        else:

            prompt = f"""
            Explain the concept: {concept}

            Student level: {level}

            Include:
            1. Simple definition.
            2. Detailed explanation.
            3. Real-world example.
            4. Important points.
            5. Short conclusion.

            Use understandable language.
            """

            with st.spinner("Preparing explanation..."):

                result = generate_response(prompt)

            st.subheader("📖 Concept Explanation")

            st.markdown(result)

            st.download_button(
                "⬇️ Download Explanation",
                data=result,
                file_name="studymate_explanation.txt",
                mime="text/plain"
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    "<center>StudyMate AI | Built with Python, "
    "Streamlit and Llama 3.2 ❤️</center>",
    unsafe_allow_html=True
)
