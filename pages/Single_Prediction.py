import numpy as np 
import pickle
import pandas as pd
import streamlit as st
import churn_service as churn_service_


def main():
    #set title
    st.title('Single Customer Churn Prediction')
    # Define the options for the dropdown
    list_paymethod = ['Debit Card', 'Credit Card', 'E wallet','UPI','Cash on Delivery']
    list_gender =['Male','Female']
    list_category = ['Laptop & Accessory','Mobile Phone','Mobile','Grocery','Others']
    list_marital = ['Married','Single','Divorced']
    list_device = ['Mobile Phone','Computer','Phone']
    list_citytier = [1,2,3]
    list_complain = {'Yes': 1,'No': 0 }
    list_satisfaction_score = [1,2,3,4,5]

    #get input data
    Tenure = st.number_input('Tenure',step=1)
    PreferredLoginDevice = st.selectbox('Preferred Login Device',list_device)
    CityTier = st.selectbox('City Tier',list_citytier)
    WarehouseToHome = st.number_input('Distance from Warehouse to Home',step=0.01)
    PreferredPaymentMode = st.selectbox('Preferred Payment Method',list_paymethod)
    Gender = st.selectbox('Gender', list_gender)
    NumberOfDeviceRegistered = st.number_input('Number of Devices Registered',min_value=1,step=1)
    PreferedOrderCat = st.selectbox('Preferred Product Category',list_category)
    SatisfactionScore = st.selectbox('Satisfaction Score',list_satisfaction_score)
    MaritalStatus = st.selectbox('Marital Status',list_marital)
    NumberOfAddress = st.number_input('Number Of Addresses',step=1)
    Complain = st.selectbox('Made Complaint?',list(list_complain.keys()))
    OrderAmountHikeFromlastYear = st.number_input('Order Amount Hike From last Year',step=0.01)
    CouponUsed = st.number_input('Coupons Used',step=0.01)
    OrderCount = st.number_input('Order Count',step = 1)
    DaySinceLastOrder = st.number_input('Days Since Last Order',step=0.01)
    CashbackAmount = st.number_input('Cashback Amount',step=0.01)
    HourSpendOnApp  = st.number_input('Hours Spend On App',step=0.01)

    
    result = ''
    test_data = {
    'Tenure': Tenure,
  'PreferredLoginDevice': PreferredLoginDevice,
  'CityTier': CityTier,
  'WarehouseToHome': WarehouseToHome,
  'PreferredPaymentMode': PreferredPaymentMode,
  'Gender': Gender,
  'HourSpendOnApp': HourSpendOnApp,
  'NumberOfDeviceRegistered': NumberOfDeviceRegistered,
  'PreferedOrderCat': PreferedOrderCat,
  'SatisfactionScore': SatisfactionScore,
  'MaritalStatus': MaritalStatus,
  'NumberOfAddress': NumberOfAddress,
  'Complain':  list_complain[Complain],
  'OrderAmountHikeFromlastYear': OrderAmountHikeFromlastYear,
  'CouponUsed': CouponUsed,
  'OrderCount': OrderCount,
  'DaySinceLastOrder': DaySinceLastOrder,
  'CashbackAmount': CashbackAmount
    }

    test_df =   pd.DataFrame([test_data])
    if st.button("Calculate Churn"):
        result = churn_service_.get_churn(test_df)
        st.success(result)


if __name__ == '__main__': 
    main()