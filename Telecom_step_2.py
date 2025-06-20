import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import joblib

# --- User credentials ---
# Pre-hashed password for "1234"
hashed_pw = ['$2b$12$1yXNM7LQMWqQhoXgOkrcp.LXPadXCVYjwYU9PRQsBpJsy4dZh2xga']

# Credentials dictionary format
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": hashed_pw[0]
        }
    }
}

# --- Set up authenticator ---
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name='churn_app',
    key='abcdef',
    cookie_expiry_days=1
)

# --- Login widget ---
authenticator.login(location='main')

# --- After login ---
if authenticator.authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.title("📊 Welcome to the Churn Prediction Dashboard")
    st.success(f"Hello, {authenticator.name}! You're logged in.")

    # ✅ Load model and features
    try:
        model = joblib.load('final_rf_model.pkl')
        features = joblib.load('model_features.pkl')
