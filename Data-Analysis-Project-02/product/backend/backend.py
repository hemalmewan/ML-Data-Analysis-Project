###Importing necessary libraries
from fastapi import FastAPI
import uvicorn
import numpy as np
import pandas as pd
import pickle
from ME_CFS_Depression import DepressionPredictionRequest 

##Load the pickle file
with open("../train_model.pkl","rb") as file:
    model=pickle.load(file)

app=FastAPI() ##define the app

##define the predict function
@app.post("/predict")
def predict(request: DepressionPredictionRequest):
    """
    Predicts the likelihood of depression based on the ME/CFS questionnaire.
    
    Args:
        request (DepressionPredictionRequest): The request object containing the depression score and post-exertional malaise.
    
    Returns:
        dict: A dictionary containing the prediction result.
    """
    # Convert the request data to a DataFrame
    data =request.dict()
    ##get the depression score and post-exertional malaise from the request
    depression_score = data["depression_score"]
    post_exertional_malaise = data["post_exertional_malaise"]

    ##assign the post_exertional_malaise to a numerical value
    if post_exertional_malaise.lower() == "yes":
        post_exertional_malaise_yes = 1
        post_exertional_malaise_no = 0
    else:
        post_exertional_malaise_no = 1
        post_exertional_malaise_yes = 0

    # Make predictions using the loaded model
    prediction = model.predict([[depression_score, post_exertional_malaise_yes, post_exertional_malaise_no]])

    return {"prediction":prediction[0]}


##run the app using uvicorn
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1",port=8000, log_level="info")