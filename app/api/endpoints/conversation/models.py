from enum import StrEnum

from pydantic import BaseModel


class MessageRequest(BaseModel):
    message: str
    include_personal_information: bool


class EvaluateSentimentRequest(BaseModel):
    critical_question_is_needed: bool


class Sentiment(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class EngagementLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class UserEvaluationResult(BaseModel):
    sentiment: Sentiment
    engagement_level: EngagementLevel
    satisfaction_with_role: Sentiment
    challenge_level: Sentiment
    areas_of_interest: str
    potential_issues: str
