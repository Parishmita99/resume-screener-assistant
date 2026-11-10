
import pytest
from pydantic import ValidationError
from schemas import ResumeMatchReport


def valid_report():
    return {
        "candidate_name": "Rahul Sharma",
        "match_score": 82,
        "matching_skills": [
            "Python", "SQL", "Machine Learning",
            "NLP", "Data Analysis"
        ],
        "skill_gaps": [
            "Docker", "Cloud Deployment", "DevOps"
        ],
        "interview_questions": [
            "Explain Python decorators.",
            "How do you optimise SQL queries?",
            "How would you deploy an ML model?"
        ],
        "summary": "Strong candidate for the role."
    }


def test_valid_report():
    report = ResumeMatchReport(**valid_report())

    assert report.match_score == 82
    assert report.candidate_name == "Rahul Sharma"


def test_score_cannot_exceed_100():
    data = valid_report()
    data["match_score"] = 120

    with pytest.raises(ValidationError):
        ResumeMatchReport(**data)


def test_exactly_five_skills_required():
    data = valid_report()
    data["matching_skills"] = ["Python", "SQL"]

    with pytest.raises(ValidationError):
        ResumeMatchReport(**data)


def test_exactly_three_gaps_required():
    data = valid_report()
    data["skill_gaps"] = ["Docker"]

    with pytest.raises(ValidationError):
        ResumeMatchReport(**data)
