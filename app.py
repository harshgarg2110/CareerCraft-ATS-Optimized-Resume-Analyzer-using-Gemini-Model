# ============================ Imports ============================ #
from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs
import google.generativeai as genai
import os
import PyPDF2
from PIL import Image

# ============================ Load Config ============================ #
# Load environment variables from .env
load_dotenv()

# Configure Gemini API using key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro model
model = genai.GenerativeModel('gemini-1.5-flash')


# ============================ Helper Functions ============================ #
# Function to send prompt to Gemini and receive response
def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from PDF resume
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text


# ============================ Prompt Template ============================ #
input_prompt_template = """
As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, DevOps Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess resumes against provided job descriptions. In a fiercely competitive job market, your expertise is crucial in offering top-notch guidance for resume enhancement. Assign precise matching percentages based on the JD (Job Description) and meticulously identify any missing keywords with utmost accuracy.

resume: {resume_text}
description: {jd_text}

I want the response in the following structure:
The first line indicates the percentage match with the job description (JD).
The second line presents a list of missing keywords in a list.
The third section provides a profile summary.
and some tips 

Mention the title for all the three sections.
While generating the response put some space to separate all the three sections.
"""


# ============================ Streamlit Page Setup ============================ #
st.set_page_config(page_title="CareerCraft - ATS Resume Analyzer", layout="wide")

# Inject custom CSS styling
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f8f9fa;
        }
        h1, h2, h3 {
            color: #003366;
        }
        .title-main {
            font-size: 48px;
            font-weight: 700;
            color: #003366;
        }
        .section {
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .highlight-box {
            background-color: #e7f4ff;
            padding: 15px;
            border-left: 6px solid #007acc;
            margin-top: 10px;
            border-radius: 6px;
            font-size: 15px;
        }
        .submit-btn button {
            background-color: #007acc;
            color: white;
            padding: 10px 30px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
        }
        .submit-btn button:hover {
            background-color: #005f99;
        }
    </style>
""", unsafe_allow_html=True)


# ============================ Banner Section ============================ #

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<div class='title-main'>CareerCraft</div>", unsafe_allow_html=True)
    st.subheader("Navigate the Job Market with Confidence!")
    st.markdown("""<div class='highlight-box'><p style='text-align: justify; font-size:16px'>
        Introducing CareerCraft, an ATS-Optimized Resume Analyzer 💼 your ultimate solution for optimizing
        job applications and accelerating career growth. Our innovative platform leverages advanced ATS
        technology to provide job seekers with valuable insights into their resumes' compatibility with
        job descriptions. From resume optimization and skill enhancement to career progression guidance,
        CareerCraft empowers users to stand out in today's competitive job market. Streamline your job
        application process, enhance your skills, and navigate your career path with confidence. Join
        CareerCraft today and unlock new opportunities for professional success!
        </p> </div>""", unsafe_allow_html=True)
    # st.markdown("""
    #     <div class='highlight-box'>
    #         Introducing <b>CareerCraft</b> – your ultimate solution for optimizing job applications.
    #         This ATS-Optimized Resume Analyzer helps you align your resume with job descriptions, 
    #         improve your skills, and stand out in today's competitive market.
    #     </div>
    # """, unsafe_allow_html=True)

with col2:
    st.image("https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif", width=480)

avs(7)


# ============================ Offerings Section ============================ #
col1, col2 = st.columns([4, 3])
with col1:
    try:
        img1 = Image.open("images/icon1.png")
        st.image(img1, width=480)  # Adjust to fit beside text
    except:
        st.warning("Image 'icon1.png' not found.")

with col2:
    st.markdown("<h2>🌟 Wide Range of Offerings</h2>", unsafe_allow_html=True)
    offerings = [
        "✅ ATS-Optimized Resume Analysis",
        "✅ Resume Optimization",
        "✅ Skill Enhancement",
        "✅ Career Progression Guidance",
        "✅ Tailored Profile Summaries",
        "✅ Streamlined Application Process",
        "✅ Personalized Recommendations",
        "✅ Efficient Career Navigation"
    ]
    for item in offerings:
        st.markdown(f"<p style='font-size:20px'>{item}</p>", unsafe_allow_html=True)

avs(7)


# ============================ Resume Upload & JD Section ============================ #
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<p style='font-size:27px'> 🚀 Embark on Your Career Adventure </p>", unsafe_allow_html=True)

    jd = st.text_area("📋 Paste the Job Description Here", key="jd_text_area")
    
    uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF Only)", type="pdf", key="resume_upload")

    avs(1)
    submit = st.button("🔍 Analyze My Resume", type="primary")

    if submit:
        if uploaded_file and jd.strip():
            resume_text = input_pdf_text(uploaded_file)
            full_prompt = input_prompt_template.format(resume_text=resume_text, jd_text=jd)
            with st.spinner("🧠 Processing with Gemini..."):
                response = get_gemini_response(full_prompt)
            st.markdown("<h3>🎯 ATS Analysis Result</h3>", unsafe_allow_html=True)
            st.success(response)
        else:
            st.warning("⚠️ Please upload a resume and paste a job description.")

with col2:
    try:
        img2 = Image.open("images/icon2.png")
        st.image(img2, width=500)
    except:
        st.warning("Image 'icon2.png' not found.")

avs(3)


# ============================ FAQ Section ============================ #
st.markdown("<h2 style='text-align:center;'>❓ Frequently Asked Questions</h2>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 3])
with col1:
    try:
        img3 = Image.open("images/icon3.png")
        st.image(img3, width=550)
    except:
        st.warning("Image 'icon3.png' not found.")
with col2:
    faq = {
        "How does CareerCraft analyze resumes and job descriptions?":
            "CareerCraft uses Google Gemini to extract relevant keywords and match them with job descriptions.",
        "Can it suggest improvements to my resume?":
            "Yes! It provides tailored advice including missing keywords and suggestions for enhancement.",
        "Is it helpful for both freshers and experienced candidates?":
            "Absolutely! CareerCraft caters to all experience levels, from beginners to professionals."
    }
    for question, answer in faq.items():
        st.markdown(f"<p style='font-size:20px; font-weight:600; color:#003366;'>Q: {question}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:18px; color:#333; margin-top:-10px;'>{answer}</p>", unsafe_allow_html=True)
        avs(1)

















