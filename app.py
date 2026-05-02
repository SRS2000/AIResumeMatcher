import streamlit as st
from model import calculate_similarity
from utils import extract_text_from_pdf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #064e3b, #059669, #10b981);
}

/* Title */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: white;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #d1fae5;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Section headings */
.section-title {
    color: white;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* -------- FILE UPLOADER CLEAN DESIGN -------- */
[data-testid="stFileUploader"] {
    border: 2px dashed white !important;
    border-radius: 12px !important;
    padding: 10px !important;
    color:black;
}
/* -------- TEXT AREA -------- */
textarea {
    background-color: white !important;
    color: black !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

/* -------- BUTTON -------- */
.stButton>button {
    width: 100%;
    height: 50px;
    background: linear-gradient(90deg, #ef4444, #dc2626);
    color: white;
    font-size: 16px;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

/* -------- METRIC -------- */
[data-testid="stMetric"] {
    background: white !important;
    padding: 15px;
    border-radius: 10px;
}
/* SUCCESS BOX */
[data-testid="stAlert"][data-baseweb="notification"] {
    color: white !important;
}

/* SUCCESS TEXT */
[data-testid="stAlert"] p {
    color: white !important;
    font-weight: 500;
}

/* WARNING BOX */
[data-testid="stAlert"][kind="warning"] {
    color: white !important;
}

/* ERROR BOX */
[data-testid="stAlert"][kind="error"] {
    color: white !important;
}

/* METRIC TEXT */
[data-testid="stMetric"] * {
    color: black !important; /* keep metric readable */
}

/* MATCH LEVEL TITLE */
h3 {
    color: white !important;
}

/* PROGRESS TEXT (if any appears) */
.stProgress > div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🤖 AI Resume Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload Resume → Compare → Get Match Score</div>', unsafe_allow_html=True)

st.write("")

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

# Resume Upload
with col1:
    st.markdown('<div class="section-title">📄 Upload Resume</div>', unsafe_allow_html=True)

    resume_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

   
    # Custom file card
    if resume_file:
        file_size_kb = round(len(resume_file.getvalue()) / 1024, 2)

# Job Description
with col2:
    st.markdown('<div class="section-title">💼 Job Description</div>', unsafe_allow_html=True)

    job_text = st.text_area(
        "",
        height=200,
        placeholder="✍️ Paste job description here...",
        label_visibility="collapsed"
    )

# ---------------- BUTTON ----------------
st.write("")
analyze = st.button("🚀 Analyze Resume")

# ---------------- RESULT ----------------
if analyze:

    if resume_file and job_text:

        resume_text = extract_text_from_pdf(resume_file)
        score = calculate_similarity(resume_text, job_text)

        st.write("")
        col3, col4 = st.columns(2)

        with col3:
            st.metric("🎯 Match Score", f"{score}%")

        with col4:
            if score > 70:
                st.success("🔥 Strong Match")
            elif score > 40:
                st.warning("⚠ Moderate Match")
            else:
                st.error("❌ Weak Match")

        st.write("### 📊 Match Level")
        st.progress(score / 100)

    else:
        st.error("⚠ Please upload resume and enter job description")