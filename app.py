import streamlit as st
import os
from api.gemini_client import generate_email
from api.resume_parser import extract_resume_text
from api.email_sender import send_email

st.set_page_config(page_title="AI Job Application Assistant", page_icon="🤖")

st.title("AI Job Application Assistant")
st.caption("Upload resume → Paste Job Description → Apply in one click")

# Inputs
resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("🧾 Paste Job Description", height=250)
recipient_email = st.text_input("📧 Recruiter / Company Email")

apply_btn = st.button("🚀 Generate & Apply")

if "email_json" not in st.session_state:
    st.session_state.email_json = None

if apply_btn:
    if not resume_file or not jd_text or not recipient_email:
        st.error("Please fill all fields")
    else:
        with st.spinner("Thinking like a recruiter..."):
            resume_text = extract_resume_text(resume_file)
            st.session_state.email_json = generate_email(resume_text, jd_text)

if st.session_state.email_json:
    email_json = st.session_state.email_json

    st.subheader("✉️ Email Preview")
    subject = st.text_input("Subject", value=email_json["subject"])
    body = st.text_area("Body", value=email_json["body"], height=300)

    if st.button("📨 Send Email"):
        send_email(
            os.getenv("MY_EMAIL"),
            os.getenv("MY_EMAIL_PASSWORD"),
            recipient_email,
            {"subject": subject, "body": body},
        )
        st.success("✅ Email sent successfully!")
