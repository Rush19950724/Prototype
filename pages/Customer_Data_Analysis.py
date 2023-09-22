import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
import churn_service as churn_service_

if 'user_data' not in st.session_state or st.session_state.user_data == {}:
    st.warning("Please Log in")
else:
    st.set_page_config(
        page_title="E-Commerce Customer Data Analysis",
        page_icon=":bar_chart:",
        layout="wide"
    )
    username = st.session_state.user_data['username']
    df1 = churn_service_.get_customer_data_by_user(username)
    df = pd.read_json(df1[0]["Data"], orient='records')


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

    st.title(":bar_chart: E-commerce Customer Data Analysis")
    st.markdown("##")
    st.dataframe(filtered_df)
    download_excel(filtered_df, "prediction_data.xlsx")
    st.markdown("---")

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        gender_counts = filtered_df['Gender'].value_counts()
        categories = gender_counts.index
        values = gender_counts.values
        gender_fig = px.pie(gender_counts, 
        values=values, names=categories, title='Gender')
        gender_fig.update_traces(textinfo='percent+label', pull=[0.09, 0, 0, 0], textposition='inside', hoverinfo='label+percent')
        st.plotly_chart(gender_fig)

    with right_column:
        payment_mode_counts = filtered_df['PreferredPaymentMode'].value_counts()
        pay_categories = payment_mode_counts.index
        pay_values = payment_mode_counts.values
        payment_fig = px.pie(payment_mode_counts, 
        values=pay_values , names=pay_categories, title='Preferred Payment Mode')
        payment_fig.update_traces(textinfo='percent+label', textposition='inside', hoverinfo='label+percent')
        st.plotly_chart(payment_fig)

    with left_column:
        order_cat_counts = filtered_df['PreferedOrderCat'].value_counts()
        order_cat_categories = order_cat_counts.index
        order_cat_values = order_cat_counts.values
        order_cat_fig = px.pie(order_cat_counts, 
        values=order_cat_values , names=order_cat_categories, title='Preferred Product Category')
        order_cat_fig.update_traces(textinfo='percent+label', textposition='inside', hoverinfo='label+percent')
        st.plotly_chart(order_cat_fig)

    with right_column:
        tenure_fig = go.Figure(data=[go.Histogram(x=filtered_df["Tenure"])])
        tenure_fig.update_layout(
            title="Tenure of the Customers",
            xaxis_title="Tenure",
            yaxis_title="Number of Customers"
        )
        st.plotly_chart(tenure_fig)

        with left_column:
            cashback_fig = go.Figure(data=[go.Histogram(x=filtered_df["CashbackAmount"])])
            cashback_fig.update_layout(
                title="Cashback Amount of the Customers",
                xaxis_title="Cashback Amount",
                yaxis_title="Number of Customers"
            )
            st.plotly_chart(cashback_fig)

        with right_column:
            order_amount_fig = go.Figure(data=[go.Histogram(x=filtered_df["OrderAmountHikeFromlastYear"])])
            order_amount_fig.update_layout(
                title="Order Amount Hike From Last Year of the Customers",
                xaxis_title="Order Amount Hike From last Year",
                yaxis_title="Number of Customers"
            )
            st.plotly_chart(order_amount_fig)
        
