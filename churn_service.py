import database as datas
import numpy as np 
import pickle
import pandas as pd
import streamlit as st
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

deta = datas.deta
db = deta.Base("customer_churn")

def insert_churn(user, df):
    return db.put({"key":user, "Data" : df.to_json(orient='records')} )

def get_all_users():
    all_users = db.fetch()
    return all_users.items

# pd.DataFrame(get_all_users())

def get_churn_data(UserId):
    return db.get(UserId)

# Loading the trained model
trained_model = pickle.load(open('prediction_model.sav', 'rb'))

def preprocess_data(test_df):
    df1 = pd.DataFrame()
    #numerical assignment
    df1['Tenure'] = test_df['Tenure']
    df1['CityTier'] = test_df['CityTier']
    df1['WarehouseToHome'] = test_df['WarehouseToHome']
    df1['HourSpendOnApp'] = test_df['HourSpendOnApp']
    df1['NumberOfDeviceRegistered'] = test_df['NumberOfDeviceRegistered']
    df1['SatisfactionScore'] = test_df['SatisfactionScore']
    df1['NumberOfAddress'] = test_df['NumberOfAddress']
    df1['Complain'] = test_df['Complain']
    df1['OrderAmountHikeFromlastYear'] = test_df['OrderAmountHikeFromlastYear']
    df1['CouponUsed'] = test_df['CouponUsed']
    df1['OrderCount'] = test_df['OrderCount']
    df1['DaySinceLastOrder'] = test_df['DaySinceLastOrder']
    df1['CashbackAmount'] = test_df['CashbackAmount']

    #Categorical Assignment
    if test_df.iloc[0]['PreferredLoginDevice'] == 'Computer':
        df1['PreferredLoginDevice_Mobile Phone'] = 0
        df1['PreferredLoginDevice_Phone'] = 0
    elif test_df.iloc[0]['PreferredLoginDevice'] == 'Phone' :
        df1['PreferredLoginDevice_Mobile Phone'] = 0
        df1['PreferredLoginDevice_Phone'] = 1
    else: 
        df1['PreferredLoginDevice_Mobile Phone'] = 1
        df1['PreferredLoginDevice_Phone'] = 0
     

    if test_df.iloc[0]['PreferredPaymentMode'] == 'Debit Card':
        df1['PreferredPaymentMode_COD'] = 0
        df1['PreferredPaymentMode_Debit Card'] = 1
        df1['PreferredPaymentMode_E wallet'] = 0
        df1['PreferredPaymentMode_UPI'] = 0

    elif (test_df.iloc[0]['PreferredPaymentMode'] == 'Cash on Delivery') or (test_df.iloc[0]['PreferredPaymentMode'] == 'COD'):
        df1['PreferredPaymentMode_COD'] = 1
        df1['PreferredPaymentMode_Debit Card'] = 0
        df1['PreferredPaymentMode_E wallet'] = 0
        df1['PreferredPaymentMode_UPI'] = 0
        
    elif test_df.iloc[0]['PreferredPaymentMode'].lower() == 'E wallet':
        df1['PreferredPaymentMode_COD'] = 0
        df1['PreferredPaymentMode_Debit Card'] = 0
        df1['PreferredPaymentMode_E wallet'] = 1
        df1['PreferredPaymentMode_UPI'] = 0
        
    elif test_df.iloc[0]['PreferredPaymentMode'].lower() == 'UPI':
        df1['PreferredPaymentMode_COD'] = 0
        df1['PreferredPaymentMode_Debit Card'] = 0
        df1['PreferredPaymentMode_E wallet'] = 0
        df1['PreferredPaymentMode_UPI'] = 1

    else: 
        df1['PreferredPaymentMode_COD'] = 0
        df1['PreferredPaymentMode_Debit Card'] = 0
        df1['PreferredPaymentMode_E wallet'] = 0
        df1['PreferredPaymentMode_UPI'] = 0
        
    if test_df.iloc[0]['Gender'].lower() == 'Male':
        df1['Gender_Male'] = 1

    else:
        df1['Gender_Male'] = 0
        
    if test_df.iloc[0]['PreferedOrderCat'] == 'Laptop & Accessory':
        df1['PreferedOrderCat_Grocery'] = 0
        df1['PreferedOrderCat_Laptop & Accessory'] = 1
        df1['PreferedOrderCat_Mobile'] = 0
        df1['PreferedOrderCat_Mobile Phone'] = 0
        df1['PreferedOrderCat_Others'] = 0

    elif test_df.iloc[0]['PreferedOrderCat'] == 'Mobile Phone' :
        df1['PreferedOrderCat_Grocery'] = 0
        df1['PreferedOrderCat_Laptop & Accessory'] = 0
        df1['PreferedOrderCat_Mobile'] = 0
        df1['PreferedOrderCat_Mobile Phone'] = 1
        df1['PreferedOrderCat_Others'] = 0

    elif test_df.iloc[0]['PreferedOrderCat'] == 'Mobile' :
        df1['PreferedOrderCat_Grocery'] = 0
        df1['PreferedOrderCat_Laptop & Accessory'] = 0
        df1['PreferedOrderCat_Mobile'] = 1
        df1['PreferedOrderCat_Mobile Phone'] = 0
        df1['PreferedOrderCat_Others'] = 0

    elif test_df.iloc[0]['PreferedOrderCat'] == 'Grocery' :
        df1['PreferedOrderCat_Grocery'] = 1
        df1['PreferedOrderCat_Laptop & Accessory'] = 0
        df1['PreferedOrderCat_Mobile'] = 0
        df1['PreferedOrderCat_Mobile Phone'] = 0
        df1['PreferedOrderCat_Others'] = 0
    elif test_df.iloc[0]['PreferedOrderCat'] == 'Others' :
        df1['PreferedOrderCat_Grocery'] = 1
        df1['PreferedOrderCat_Laptop & Accessory'] = 0
        df1['PreferedOrderCat_Mobile'] = 0
        df1['PreferedOrderCat_Mobile Phone'] = 0
        df1['PreferedOrderCat_Others'] = 1
    else: 
        df1['PreferedOrderCat_Grocery'] = 0
        df1['PreferedOrderCat_Laptop & Accessory'] = 0
        df1['PreferedOrderCat_Mobile'] = 0
        df1['PreferedOrderCat_Mobile Phone'] = 0
        df1['PreferedOrderCat_Others'] = 0
        
    if test_df.iloc[0]['MaritalStatus'] == 'Married':
        df1['MaritalStatus_Married'] = 1
        df1['MaritalStatus_Single'] = 0
    elif test_df.iloc[0]['MaritalStatus'] == 'Single':
        df1['MaritalStatus_Single'] = 1
        df1['MaritalStatus_Married'] = 0
    else:
        df1['MaritalStatus_Married'] = 0
        df1['MaritalStatus_Single'] = 0
    
    #Set Column Order
    columnsTitles = ['Tenure', 'CityTier', 'WarehouseToHome', 'HourSpendOnApp',
       'NumberOfDeviceRegistered', 'SatisfactionScore', 'NumberOfAddress',
       'Complain', 'OrderAmountHikeFromlastYear', 'CouponUsed', 'OrderCount',
       'DaySinceLastOrder', 'CashbackAmount',
       'PreferredLoginDevice_Mobile Phone', 'PreferredLoginDevice_Phone',
       'PreferredPaymentMode_COD', 'PreferredPaymentMode_Debit Card',
       'PreferredPaymentMode_E wallet', 'PreferredPaymentMode_UPI',
       'Gender_Male', 'PreferedOrderCat_Grocery',
       'PreferedOrderCat_Laptop & Accessory', 'PreferedOrderCat_Mobile',
       'PreferedOrderCat_Mobile Phone', 'PreferedOrderCat_Others',
       'MaritalStatus_Married', 'MaritalStatus_Single']
    
    return df1.reindex(columns=columnsTitles)



def get_churn(test_df):
    test_data = preprocess_data(test_df)
    imputer = IterativeImputer(random_state=42)
    test_data = imputer.fit_transform(test_data)

    churn_probability = trained_model.predict(test_data)
    churn_rates= trained_model.predict_proba(test_data)
    
    will_churn = "Customer will be churned!  " if churn_probability[0] == 1 else "Customer will not be churned. "
    churn_rate = '{:.2%}'.format(churn_rates[0][1]) 
    return will_churn, f"Churn Probability : {churn_rate}"

def get_churn_array(test_df):
    test_data = preprocess_data(test_df)

    churn_probability = trained_model.predict(test_data)
    churn_rates= trained_model.predict_proba(test_data)
    
    will_churn = 1 if churn_probability[0] == 1 else 0
    churn_rate = '{:.2%}'.format(churn_rates[0][1]) 
    return [will_churn,churn_rate]


def delete_customer_data_by_user(user):
    customer_data = db.fetch({"key": user})
    if customer_data.count > 0:
        for item in customer_data.items:
            db.delete(item["key"])
        return True 
    else:
        return False

def get_customer_data_by_user(user):
    customer_data = db.fetch({"key": user})
    if customer_data:
        return customer_data.items
    else:
        return None


    
