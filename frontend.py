import streamlit as st
import requests
import json

# 1. Define the API URL
# If you are running locally, this is localhost.
# If you deploy BentoML to Heroku later, you paste that URL here.
BENTO_API_URL = "http://localhost:3000/predict"

st.title("💰 Social Ads Predictor")
st.write("Will this customer buy the product?")

# 2. Create Input Form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.slider("Age", 18, 60, 30)
        
    with col2:
        salary = st.number_input("Estimated Salary ($)", 
                                min_value=15000, 
                                max_value=150000, 
                                value=50000, 
                                step=1000)
    
    submit_btn = st.form_submit_button("Predict Purchase")

# 3. Send Request to BentoML
if submit_btn:
    # Match the "input_data" structure we saw in Swagger UI
    payload = {
        "input_data": {
            "Gender": gender,
            "Age": age,
            "Salary": salary
        }
    }
    
    try:
        response = requests.post(BENTO_API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result['result']
            
            if prediction == "Will Purchase":
                st.success(f"✅ Result: **{prediction}**")
                st.balloons()
            else:
                st.warning(f"❌ Result: **{prediction}**")
                
            with st.expander("See Backend Details"):
                st.json(result)
        else:
            st.error(f"Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("🚨 Could not connect to BentoML backend. Is 'bentoml serve' running?")