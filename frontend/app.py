import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend. 'backend' is the container name on the shared Docker network,
# which Docker's internal DNS resolves automatically.
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Revenue Prediction")
st.write("Predict the total sales revenue for a product at a given store.")

# ---------------- Online (single) prediction ----------------
st.subheader("Online Prediction — Single Product")

col1, col2 = st.columns(2)
with col1:
    product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66, step=0.1)
    product_allocated_area = st.number_input("Product Allocated Area (ratio)", min_value=0.0, max_value=1.0, value=0.03, step=0.01)
    product_mrp = st.number_input("Product MRP", min_value=0.0, value=150.0, step=1.0)
    store_age_years = st.number_input("Store Age (years)", min_value=0, value=16, step=1)
    sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
with col2:
    id_char = st.selectbox("Product Id Category", ["FD", "DR", "NC"])
    type_cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])

# Assemble the payload in the exact schema the API expects
payload = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": sugar,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": city_type,
    "Store_Type": store_type,
    "Product_Id_char": id_char,
    "Store_Age_Years": store_age_years,
    "Product_Type_Category": type_cat,
}

if st.button("Predict Sales", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
    if response.status_code == 200:
        result = response.json()["Predicted Product Store Sales Total"]
        st.success(f"Predicted Product Store Sales Total: {result}")
    else:
        st.error("Unable to get a prediction from the API. Please ensure the backend container is running.")

# ---------------- Batch prediction ----------------
st.subheader("Batch Prediction — Upload CSV")
st.write("Upload a CSV containing the feature columns to predict sales for many products at once.")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            result_df = pd.DataFrame(list(predictions.items()), columns=["Row", "Predicted_Sales"])
            st.write(result_df)
        else:
            st.error("Unable to get batch predictions from the API. Please ensure the backend container is running.")
