
from database import initialize_database, save_analysis, get_analyses
from schemas import ResumeMatchReport


def sample_report():
    return ResumeMatchReport(
        candidate_name="Test Candidate",
        match_score=85,
        matching_skills=[
            "Python", "SQL", "Machine Learning",
            "NLP", "Data Analysis"
        ],
        skill_gaps=[
            "Docker", "Cloud", "DevOps"
        ],
        interview_questions=[
            "Explain Python.",
            "Explain SQL.",
            "Explain deployment."
        ],
        summary="Good candidate."
    )


def test_save_and_retrieve():
    initialize_database()

    report = sample_report()
    save_analysis(report)

    records = get_analyses(
        candidate_name="Test Candidate",
        min_score=80,
        max_score=90
    )

    assert len(records) >= 1
    assert records[0]["candidate_name"] == "Test Candidate"


def test_score_filter():
    records = get_analyses(
        min_score=90,
        max_score=100
    )

    assert all(
        90 <= record["match_score"] <= 100
        for record in records
    )
