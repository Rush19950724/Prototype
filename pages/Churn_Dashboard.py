import numpy as np 
import pickle
import pandas as pd
import streamlit as st
import churn_service as churn_service_
from pathlib import Path
import streamlit_authenticator as stauth
import user_service as user_services
import plotly.express as px
import plotly.graph_objs as go

if 'user_data' not in st.session_state or st.session_state.user_data == {}:
    st.warning("Please Log in")
else:
    st.title("Churn Data Dashboard")

    username = st.session_state.user_data['username']
    df1 = churn_service_.get_customer_data_by_user(username)
    df = pd.read_json(df1[0]["Data"], orient='records')
    column_order = ["Churn", "ChurnRate"]
    df = df[column_order + [col for col in df.columns if col not in column_order]]
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
    st.sidebar.header("Filters")
    gender = st.sidebar.multiselect(
        "Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    preferredLoginDevice = st.sidebar.multiselect(
        "Preferred Login Device:",
        options=df["PreferredLoginDevice"].unique(),
        default=df["PreferredLoginDevice"].unique()
    )

    preferedOrderCat = st.sidebar.multiselect(
        "Preferred Product Category:",
        options=df["PreferedOrderCat"].unique(),
        default=df["PreferedOrderCat"].unique()
    )

    maritalStatus = st.sidebar.multiselect(
        "Marital Status:",
        options=df["MaritalStatus"].unique(),
        default=df["MaritalStatus"].unique()
    )

    filtered_df = df.query(
        "Gender == @gender & PreferredLoginDevice == @preferredLoginDevice & PreferedOrderCat== @preferedOrderCat & MaritalStatus == @maritalStatus "
    )
    total_churn = (df["Churn"] == 1).sum()

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Customers Likely to Churn:")
        st.subheader(total_churn)
    with right_column:
        download_excel(filtered_df, "prediction_data.xlsx")
    st.markdown("---")

    st.write(filtered_df)
    left_column, right_column = st.columns(2)
    with left_column:
        churn_counts = filtered_df['Churn'].value_counts()
        categories = churn_counts.index
        values = churn_counts.values
        churn_fig = px.pie(churn_counts, 
        values=values, names=categories, title='Customer Churn')
        churn_fig.update_traces(textinfo='percent+label', pull=[0.09, 0, 0, 0], textposition='inside', hoverinfo='label+percent')
        st.plotly_chart(churn_fig)

    left_column, right_column = st.columns(2)
    with left_column:
        churn_counts = filtered_df.groupby(['Complain', 'Churn']).size().unstack(fill_value=0)
        churn_counts.reset_index(inplace=True)
        churn_counts = churn_counts.melt(id_vars='Complain', var_name='Churn', value_name='Count')
        fig = px.bar(churn_counts, x='Complain', y='Count', color='Churn', 
                    title='Customer Churn by Complain')
        fig.update_layout(xaxis_title='Complaint', yaxis_title='Number of Customers')
        st.plotly_chart(fig, use_container_width=True)

    with right_column:
        churn_counts = filtered_df.groupby(['PreferedOrderCat', 'Churn']).size().unstack(fill_value=0)
        churn_counts.reset_index(inplace=True)
        churn_counts = churn_counts.melt(id_vars='PreferedOrderCat', var_name='Churn', value_name='Count')
        fig = px.bar(churn_counts, x='PreferedOrderCat', y='Count', color='Churn', 
                    title='Customer Churn by Preferred Order Category')
        fig.update_layout(xaxis_title='Preferred Order Category', yaxis_title='Number of Customers')
        st.plotly_chart(fig, use_container_width=True)

    left_column, right_column = st.columns(2)
    with left_column:
        churn_counts = filtered_df.groupby(['MaritalStatus', 'Churn']).size().unstack(fill_value=0)
        churn_counts.reset_index(inplace=True)
        churn_counts = churn_counts.melt(id_vars='MaritalStatus', var_name='Churn', value_name='Count')
        fig = px.bar(churn_counts, x='MaritalStatus', y='Count', color='Churn', 
                    title='Customer Churn by MaritalStatus')
        fig.update_layout(xaxis_title='Marital Status', yaxis_title='Number of Customers')
        st.plotly_chart(fig, use_container_width=True)

    with right_column:
        churn_counts = filtered_df.groupby(['Gender', 'Churn']).size().unstack(fill_value=0)
        churn_counts.reset_index(inplace=True)
        churn_counts = churn_counts.melt(id_vars='Gender', var_name='Churn', value_name='Count')
        fig = px.bar(churn_counts, x='Gender', y='Count', color='Churn', 
                    title='Customer Churn by Gender')
        fig.update_layout(xaxis_title='Gender', yaxis_title='Number of Customers')
        st.plotly_chart(fig, use_container_width=True)


    customer_counts = df.groupby(['Tenure', 'Churn']).size().unstack(fill_value=0)
    customer_counts.reset_index(inplace=True)
    customer_counts = customer_counts.melt(id_vars='Tenure', var_name='Churn', value_name='Customer Count')
    fig = px.line(customer_counts, x='Tenure', y='Customer Count', color='Churn', 
                title='Custome Churn by Tenure',
                labels={'Tenure': 'Tenure', 'Customer Count': 'Number of Customers'})
    fig.update_layout(yaxis_title='Number of Customers')
    st.plotly_chart(fig, use_container_width=True)






