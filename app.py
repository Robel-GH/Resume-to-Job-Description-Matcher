import streamlit as st
import os
import pdfplumber
from docx import Document
from job_matching_crew.crew import JobMatchingCrew

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


def display_report(file_path, title):
    """
    Displays a markdown report with simple formatting.
    """
    if not os.path.exists(file_path):
        st.warning(f"{title} not found.")
        return

    st.header(title)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple formatting: convert markdown-like headings to Streamlit headers
    lines = content.split("\n")
    for line in lines:
        if line.startswith("# "):
            st.subheader(line[2:].strip())
        elif line.startswith("## "):
            st.markdown(f"**{line[3:].strip()}**")
        else:
            st.write(line)


def main():
    st.title("Job Matching Crew AI")
    st.markdown("Upload your CV (Markdown, PDF, or DOCX) and enter job URLs to analyze and find matching jobs.")

    cv_file = st.file_uploader("Upload your CV", type=["md", "txt", "pdf", "docx"])
    job_urls_input = st.text_area(
        "Enter job URLs (one per line)",
        value="https://vuejobs.com/jobs/ralabs-senior-vue-js-engineer\nhttps://vuejobs.com/jobs/mozilla-full-stack-software-engineer\nhttps://vuejobs.com/jobs/trooptravel-front-end-engineer-vue3"
    )

    if st.button("Run Job Matching"):
        if not cv_file:
            st.error("Please upload a CV file.")
            return

        # Save uploaded CV temporarily
        temp_cv_path = "./temp_uploaded_cv"
        ext = cv_file.name.split('.')[-1].lower()
        if ext in ['md', 'txt']:
            temp_cv_path += f".{ext}"
            save_uploaded_file(cv_file, temp_cv_path)
        elif ext == 'pdf':
            temp_cv_path += ".pdf"
            save_uploaded_file(cv_file, temp_cv_path)
            text = extract_text_from_pdf(temp_cv_path)
            with open("./temp_uploaded_cv.md", "w", encoding="utf-8") as f:
                f.write(text)
            temp_cv_path = "./temp_uploaded_cv.md"
        elif ext == 'docx':
            temp_cv_path += ".docx"
            save_uploaded_file(cv_file, temp_cv_path)
            text = extract_text_from_docx(temp_cv_path)
            with open("./temp_uploaded_cv.md", "w", encoding="utf-8") as f:
                f.write(text)
            temp_cv_path = "./temp_uploaded_cv.md"
        else:
            st.error("Unsupported file type.")
            return

        job_urls = [url.strip() for url in job_urls_input.split("\n") if url.strip()]
        inputs = {
            "cv_path": temp_cv_path,
            "job_urls": job_urls
        }

        crew = JobMatchingCrew().crew()
        with st.spinner("Running job matching..."):
            try:
                crew.kickoff(inputs=inputs)
                st.success("Job matching completed!")

                # Path to match report
                match_report_path = './src/job_matching_crew/data/outputs/match_report.md'

                # Download button for match report
                if os.path.exists(match_report_path):
                    with open(match_report_path, 'rb') as report_file:
                        report_bytes = report_file.read()
                    st.download_button(
                        label='Download Match Report',
                        data=report_bytes,
                        file_name='match_report.md',
                        mime='text/markdown'
                    )

                # Display the matching report
                display_report(match_report_path, "Matching Report")

            except Exception as e:
                st.error(f"Error running the crew: {e}")

if __name__ == "__main__":
    main()
