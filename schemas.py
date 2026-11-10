
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ResumeMatchReport(BaseModel):
    """
    Defines the expected output of the Resume Screener AI.
    """

    model_config = ConfigDict(extra="forbid")

    candidate_name: str = Field(
        description="Candidate's name from the resume, or Unknown"
    )

    match_score: int = Field(
        ge=0,
        le=100,
        description="Job-related match score between 0 and 100"
    )

    matching_skills: list[str] = Field(
        description="Exactly five skills supported by resume evidence"
    )

    skill_gaps: list[str] = Field(
        description="Exactly three relevant missing or insufficiently evidenced skills"
    )

    interview_questions: list[str] = Field(
        description="Exactly three job-specific interview questions"
    )

    summary: str = Field(
        description="Short explanation of the candidate's job-related fit"
    )

    @field_validator("matching_skills")
    @classmethod
    def validate_matching_skills(cls, value):
        if len(value) != 5:
            raise ValueError("Exactly five matching skills are required")
        return value

    @field_validator("skill_gaps")
    @classmethod
    def validate_skill_gaps(cls, value):
        if len(value) != 3:
            raise ValueError("Exactly three skill gaps are required")
        return value

    @field_validator("interview_questions")
    @classmethod
    def validate_interview_questions(cls, value):
        if len(value) != 3:
            raise ValueError("Exactly three interview questions are required")
        return value
