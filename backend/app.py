# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
SuperKart_api = Flask("SuperKart Prediction System")

# Load the trained machine learning model
model = joblib.load("SuperKart_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@SuperKart_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction System!"

# Define an endpoint for single SuperKart prediction (POST request)
@SuperKart_api.post('/v1/predict')
def predict_SuperKart():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing SuperKart details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    SuperKart_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': data['Product_Weight'],
    'Product_Sugar_Content': data['Product_Sugar_Content'],
    'Product_Allocated_Area': data['Product_Allocated_Area'],
    'Product_MRP': data['Product_MRP'],
    'Store_Size': data['Store_Size'],
    'Store_Location_City_Type': data['Store_Location_City_Type'],
    'Store_Type': data['Store_Type'],
    'Product_Id_char': data['Product_Id_char'],
    'Store_Age_Years': data['Store_Age_Years'],
    'Product_Type_Category': data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction 
    SuperKart_prediction = model.predict(input_data)[0] 

    # Calculate actual sales
    SuperKart_prediction = np.exp(SuperKart_prediction)

    # Convert SuperKart_prediction to Python float
    SuperKart_prediction = round(float(SuperKart_prediction), 2)
    # The conversion above is needed as we convert the model prediction (slaes) to actual sales using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'SuperKart_prediction': SuperKart_prediction})


# Define an endpoint for batch prediction (POST request)
@SuperKart_predictor_api.post('/v1/predictbatch')
def predict_SuperKart_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing SuperKart details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get sales)
    SuperKart_predictions = model.predict(input_data).tolist()

    # Calculate actual sales
    SuperKart_predictions = [np.exp(sales) for sales in SuperKart_predictions]

    # Create a dictionary of predictions with SuperKart IDs as keys
    SuperKart_ids = input_data['id'].tolist()  # Assuming 'id' is the SuperKart ID column
    output_dict = dict(zip(SuperKart_ids, SuperKart_predictions))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    SuperKart_predictor_api.run(debug=True)
