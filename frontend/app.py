import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Malha Sales Predictor")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for features
  col1, col2, col3 = st.columns(3)

    with col1:
        product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027)
        product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)

    with col2:
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        store_location = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
        product_id = st.selectbox("Product ID Character", ["FD", "DR", "NC"])

    with col3:
        store_age = st.number_input("Store Age (Years)", min_value=0, value=16)
        product_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
            'Product_Sugar_Content': product_sugar,
            'Product_Allocated_Area': product_area,
            'Product_MRP': product_mrp,
            'Store_Size': store_size,
            'Store_Location_City_Type': store_location,
            'Store_Type': store_type,
            'Product_Id_char': product_id,
            'Store_Age_Years': store_age,
            'Product_Type_Category': product_category
}])

# Make prediction when the "Predict" button is clicked # for single pridiction
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Sales']
        st.success(f"Predicted Sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
