
import streamlit as st

from ai_engine import analyze_resume
from database import (
    initialize_database,
    save_analysis,
    get_analyses
)
from resume_parser import extract_resume_text


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Resume Screener Assistant",
    page_icon="📄",
    layout="wide"
)

# Initialize SQLite database
initialize_database()


# ==========================================
# 2. HELPER FUNCTION
# ==========================================

def display_report(report):

    st.subheader("Candidate Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Candidate Name",
            report["candidate_name"]
        )

    with col2:
        st.metric(
            "Match Score",
            f'{report["match_score"]}/100'
        )

    st.progress(report["match_score"] / 100)

    st.subheader("Summary")
    st.write(report["summary"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Matching Skills")

        for skill in report["matching_skills"]:
            st.markdown(f"- ✅ {skill}")

    with col2:
        st.markdown("### Skill Gaps")

        for gap in report["skill_gaps"]:
            st.markdown(f"- ⚠️ {gap}")

    st.markdown("### Suggested Interview Questions")

    for index, question in enumerate(
        report["interview_questions"],
        start=1
    ):
        st.write(f"**{index}.** {question}")


# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("📄 Resume Screener Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["New Analysis", "Analysis History"]
)

st.sidebar.divider()

st.sidebar.info(
    "AI-assisted recruitment decision support. "
    "All hiring decisions should involve human review."
)
st.sidebar.info(
    "Privacy notice: Resume text is sent to the configured "
    "Gemini API for analysis. The application stores the "
    "generated report locally in SQLite, not the original "
    "resume or job description. Avoid uploading unnecessary "
    "personal or sensitive information."
)

# ==========================================
# 4. NEW ANALYSIS PAGE
# ==========================================

if page == "New Analysis":

    st.title("Resume Screener Assistant")

    st.write(
        "Compare a candidate's resume against a job description "
        "using AI-powered analysis."
    )

    st.divider()

    # --------------------------------------
    # JOB DESCRIPTION INPUT
    # --------------------------------------

    st.subheader("1. Enter Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder=(
            "Enter job title, responsibilities, "
            "required skills and qualifications..."
        )
    )

    # --------------------------------------
    # RESUME UPLOAD
    # --------------------------------------

    st.subheader("2. Upload Candidate Resume")

    uploaded_file = st.file_uploader(
        "Upload a resume",
        type=["txt", "pdf", "docx"]
    )

    resume_text = ""

    if uploaded_file is not None:

        try:
            resume_text = extract_resume_text(uploaded_file)

            if resume_text.strip():
                st.success(
                    "Resume uploaded and text extracted successfully."
                )
            else:
                st.warning(
                    "No readable text was found. "
                    "This may be a scanned PDF. "
                    "Please paste the resume text manually."
                )

        except Exception as error:
            st.error(
                f"Could not read the uploaded file: {error}"
            )

    # --------------------------------------
    # MANUAL RESUME INPUT
    # --------------------------------------

    pasted_resume = st.text_area(
        "Or paste resume text here",
        height=200,
        placeholder="Paste the candidate's resume..."
    )

    # Pasted text takes priority over uploaded text
    if pasted_resume.strip():
        resume_text = pasted_resume

    st.caption(
        "Supported formats: TXT, PDF and DOCX. "
        "You can also paste resume text directly."
    )

    st.divider()

    # ======================================
    # 5. ANALYSE RESUME BUTTON
    # ======================================

    if st.button(
        "🔍 Analyse Resume",
        type="primary",
        use_container_width=True
    ):

        if not job_description.strip():

            st.error(
                "Please enter a job description."
            )

        elif not resume_text.strip():

            st.error(
                "Please upload or paste a resume."
            )

        else:

            # ----------------------------------
            # INPUT LENGTH VALIDATION
            # ----------------------------------

            MAX_JD_LENGTH = 12000
            MAX_RESUME_LENGTH = 20000

            if len(job_description) > MAX_JD_LENGTH:

                st.warning(
                    "Job description is long. "
                    "Only the first 12000 characters will be analysed."
                )

            if len(resume_text) > MAX_RESUME_LENGTH:

                st.warning(
                    "Resume is long. "
                    "Only the first 20000 characters will be analysed."
                )

            job_description = job_description[:MAX_JD_LENGTH]
            resume_text = resume_text[:MAX_RESUME_LENGTH]

            # ----------------------------------
            # CALL GEMINI AI
            # ----------------------------------

            try:

                with st.spinner(
                    "Analysing resume using Gemini AI..."
                ):

                    report = analyze_resume(
                        job_description,
                        resume_text
                    )

                    # Save validated report in SQLite
                    save_analysis(report)

                    report_data = report.model_dump()

                st.success(
                    "Resume analysis completed successfully!"
                )

                # Display analysis
                display_report(report_data)

            except Exception as error:

                st.error(
                    "Unable to complete the analysis. "
                    "Please try again."
                )

                st.caption(str(error))


# ==========================================
# 6. ANALYSIS HISTORY PAGE
# ==========================================

elif page == "Analysis History":

    st.title("Analysis History")

    st.write(
        "Search and review previously analysed candidates."
    )

    st.divider()

    # --------------------------------------
    # SEARCH AND FILTERS
    # --------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        candidate_search = st.text_input(
            "Search candidate name",
            placeholder="Enter candidate name"
        )

    with col2:

        min_score = st.number_input(
            "Minimum Match Score",
            min_value=0,
            max_value=100,
            value=0
        )

    with col3:

        max_score = st.number_input(
            "Maximum Match Score",
            min_value=0,
            max_value=100,
            value=100
        )

    st.divider()

    # --------------------------------------
    # VALIDATE FILTERS
    # --------------------------------------

    if min_score > max_score:

        st.error(
            "Minimum score cannot be greater than maximum score."
        )

    else:

        # Retrieve matching database records
        records = get_analyses(
            candidate_name=candidate_search,
            min_score=min_score,
            max_score=max_score
        )

        st.write(
            f"**{len(records)} analysis record(s) found.**"
        )

        # ----------------------------------
        # DISPLAY HISTORY
        # ----------------------------------

        if not records:

            st.info(
                "No matching analyses found. "
                "Try changing your search or score filters."
            )

        else:

            for record in records:

                with st.expander(
                    f'{record["candidate_name"]} | '
                    f'Score: {record["match_score"]}/100 | '
                    f'{record["created_at"]}'
                ):

                    display_report(record["report"])


# ==========================================
# END OF APPLICATION
# ==========================================
