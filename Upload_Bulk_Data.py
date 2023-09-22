import base64
import numpy as np 
import pickle
import pandas as pd
import streamlit as st
import churn_service as churn_service_
from pathlib import Path
import streamlit_authenticator as stauth
import user_service as user_services

st.set_page_config(
    page_title="E-Commerce Churn Prediction",
    page_icon="👋"
    )

if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

users = user_services.get_all_users()
usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "churn_dashboard", "abcdef")
name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username or password is incorrect!")
if authentication_status == None:
    st.session_state.user_data = {}
    st.warning("Please enter your username and password")
if authentication_status:
    authenticator.logout("Logout","sidebar")
    st.session_state.user_data['username'] = username
    st.session_state.user_data['file_uploaded'] = False
    st.sidebar.title(f"Welcome {name}")
    st.title("Customer Data Analysis")

    def download_excel(df, filename):
        df.to_excel(filename, index=False)
        with open(filename, "rb") as file:
            btn = st.download_button(
                label="Export Excel File",
                data=file,
                key="excel-download",
                file_name=filename,
            )
        return btn

    uploaded_file = st.file_uploader("Upload the Customer Data Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)
        for index, row in df.iterrows():
            arr_churn = churn_service_.get_churn_array(pd.DataFrame([row]))
            churn = arr_churn[0]
            churnRate = arr_churn[1]
            df.at[index, 'Churn'] = churn
            df.at[index,'ChurnRate'] = churnRate

        if df.shape[0] >= 1:
            churn_service_.delete_customer_data_by_user(st.session_state.user_data['username'])
            churn_service_.insert_churn(st.session_state.user_data['username'], df)

        st.write("Uploaded Customer Data:")
        st.write(df)
        st.session_state.user_data['file_uploaded'] = True
        download_excel(df, "prediction_data.xlsx")
    else:
        customer_data = churn_service_.get_customer_data_by_user(st.session_state.user_data['username'])
        if(len(customer_data) > 0):
            df1 = pd.read_json(customer_data[0]["Data"], orient='records')
            st.write(df1)
        else:
            st.warning("You have not uploaded any data!")

