from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
from joblib import load
import io
from fastapi.middleware.cors import CORSMiddleware

# Load the trained machine learning pipeline for star type prediction
pipeline = load('Pipeline/pipeline_star_type_pred.joblib')

app = FastAPI()

# Configure CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://star-type.streamlit.app/"],  # Allows all origins; modify for production use
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for validating input features for single star type prediction
class StarFeatures(BaseModel):
    temperature: int = Field(..., alias='Temperature (K)', description='Temperature of the star in Kelvin')
    luminosity: float = Field(..., alias='Luminosity(L/Lo)', description='Luminosity of the star relative to the sun')
    radius: float = Field(..., alias='Radius(R/Ro)', description='Radius of the star relative to the sun')
    absolute_magnitude: float = Field(..., alias='Absolute magnitude(Mv)', description='Absolute magnitude of the star')

# Health check endpoint to confirm the application is running
@app.get("/")
def read_root():
    """
    Health check endpoint.

    Returns a simple message indicating the app is running.
    """
    return {"message": "The Star Type Prediction app is running"}

# Endpoint for predicting the star type based on provided features
@app.post("/predict")
def predict_star_type(star: StarFeatures):
    """
    Predict the type of a star based on its features.

    Args:
        star (StarFeatures): The star features provided by the user.

    Returns:
        dict: Contains the predicted star type and the probability of the prediction.
    """
    # Convert the star features into a dictionary format for processing
    star_dict = {
        'Temperature (K)': star.temperature,
        'Luminosity(L/Lo)': star.luminosity,
        'Radius(R/Ro)': star.radius,
        'Absolute magnitude(Mv)': star.absolute_magnitude,
    }
    
    # Create a DataFrame from the star features dictionary for model input
    test_df = pd.DataFrame([star_dict], index=[0])
    
    # Perform prediction using the loaded machine learning pipeline
    y_pred = pipeline.predict(test_df)[0]
    # Get the probability of the predicted class
    y_pred_prob = pipeline.predict_proba(test_df)[0].max()
    
    return {
        "predicted_type": y_pred,
        "predicted_probability": y_pred_prob
    }

# Endpoint for bulk prediction using a CSV file upload
@app.post("/bulk_predict")
async def bulk_predict(file: UploadFile = File(...)):
    """
    Predict star types in bulk from a CSV file containing star features.

    Args:
        file (UploadFile): The uploaded CSV file containing star features.

    Raises:
        HTTPException: If the uploaded file is not a CSV or if required columns are missing.

    Returns:
        StreamingResponse: A CSV file containing the original features and their predicted star types.
    """
    # Check if the uploaded file has a CSV extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Read the content of the uploaded CSV file into a DataFrame
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    
    # Define the expected column names for the input DataFrame
    expected_columns = ['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']
    
    # Ensure that all expected columns are present in the uploaded DataFrame
    if not all(column in df.columns for column in expected_columns):
        raise HTTPException(
            status_code=400, 
            detail=f"The CSV file must contain the following columns: {expected_columns}"
        )
    
    # Rearrange DataFrame columns to match the expected order for model compatibility
    df = df[expected_columns]
    
    # Generate predictions for all rows in the DataFrame
    predictions = pipeline.predict(df)
    
    # Add the predictions as a new column in the DataFrame
    df['Predicted Type'] = predictions
    
    # Convert the DataFrame to CSV format for download
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Return the CSV file as a streaming response for download
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=predictions.csv"}
    )
