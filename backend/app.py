# Import necessary libraries
import numpy as np
import pandas as pd
import joblib  # For loading the serialized model
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_api = Flask("SuperKart Sales Predictor")

# Load the trained pipeline (preprocessing + model) once at startup
model = joblib.load("superkart_model.joblib")

# The exact feature schema the model expects (order preserved)
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
    "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category"
]


@superkart_api.get('/')
def home():
    """Health-check endpoint confirming the API is running."""
    return "Welcome to the SuperKart Sales Revenue Prediction API!"


@superkart_api.post('/v1/predict')
def predict_sales():
    """Online (single) prediction from a JSON payload of product/store features."""
    # Parse the JSON body of the request
    product_data = request.get_json()

    # Build a one-row DataFrame in the exact feature order the model expects
    sample = {feature: product_data[feature] for feature in FEATURES}
    input_data = pd.DataFrame([sample])

    # Predict and cast NumPy float -> native float so jsonify can serialize it
    prediction = round(float(model.predict(input_data)[0]), 2)

    return jsonify({'Predicted Product Store Sales Total': prediction})


@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    """Batch prediction from an uploaded CSV file (form key 'file')."""
    # Read the uploaded CSV into a DataFrame
    file = request.files['file']
    input_data = pd.read_csv(file)

    # Predict for every row and return a {row_index: prediction} mapping
    predictions = model.predict(input_data)
    output = {str(idx): round(float(pred), 2) for idx, pred in zip(input_data.index, predictions)}

    return jsonify(output)


# Local debugging entry point (in the container, gunicorn runs the app instead)
if __name__ == '__main__':
    superkart_api.run(debug=True, host='0.0.0.0', port=7860)
