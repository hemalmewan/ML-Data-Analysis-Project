from pydantic import BaseModel

class DepressionPredictionRequest(BaseModel):
    """
    Request model for predicting depression based on the ME/CFS questionnaire.
    """
    depression_score: int
    post_exertional_malaise: str