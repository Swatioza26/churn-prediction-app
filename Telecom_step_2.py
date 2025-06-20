import os
import streamlit as st

# Force Streamlit to use the port Render provides
port = int(os.environ.get("PORT", 8501))

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import joblib

# --- User credentials ---
names = ['Admin']
usernames = ['admin']
passwords = ['1234']

# ✅ Hash the passwords
hashed_pw = stauth.Hasher(passwords).generate()

# ✅ Set up the authenticator
authenticator = stauth.Authenticate(
    names, usernames, hashed_pw,
    'churn_app', 'abcdef', cookie_expiry_days=1
)

# --- Login ---
name, auth_status, username = authenticator.login('Login', 'main')

# --- Main App after Login ---
if auth_status:
    authenticator.logout('Logout', 'sidebar')
    st.title("📊 Welcome to the Churn Prediction Dashboard")
    st.success(f"Hello, {name}! You're logged in.")

    # ✅ Load model and features inside authenticated block
    model = joblib.load('final_rf_model.pkl')
    features = joblib.load('model_features.pkl')

    # ✅ Upload customer file
    uploaded_file = st.file_uploader("📤 Upload a customer CSV file for churn prediction", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df_encoded = pd.get_dummies(df)
            df_encoded = df_encoded.reindex(columns=features, fill_value=0)

            predictions = model.predict(df_encoded)
            df['Churn_Prediction'] = predictions

            st.subheader("📊 Prediction Results")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Predictions", csv, "churn_predictions.csv")

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

elif auth_status is False:
    st.error("❌ Incorrect username or password")

elif auth_status is None:
    st.warning("Please enter your credentials")
