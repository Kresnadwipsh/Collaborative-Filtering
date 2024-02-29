
# Import Library
import streamlit as st
import pandas as pd
import time
import pickle

from stqdm import stqdm
from time import sleep
from streamlit_option_menu import option_menu

# Model
prod = pd.read_csv(r"D:\Belajar\Skilvul\Dataset\product_details.csv", sep = ';')[['product_id','category']] # <---- Insert Product Dataset Source
sales = pd.read_csv(r"D:\Belajar\Skilvul\Dataset\sales_dummy.csv") # <---- Insert Sales Dummy Dataset Source

with open("D:\Belajar\Skilvul\svd_model.pkl", 'rb') as file: # <---- Insert Pickle Model Location
    loaded_model = pickle.load(file)

# Function to Get Best Product By its Customer
def best_products(id) :
    pred = []

    df_model = prod[['product_id']]
    df_model['customer_id'] = id

    for _, row in  df_model.iterrows():
        est = loaded_model.predict(row['customer_id'], row['product_id'])
        pred.append(est[3])

    df_model['rating'] = pred

    df_model = (pd.merge(df_model, prod, how='left', on='product_id')).sort_values(by='rating', ascending=False).rename(columns={
        'product_id' : 'Product ID',
        'customer_id' : 'Customer ID',
        'rating' : 'Rating',
        'category' : 'Category'
    })

    return df_model.head(3)

# Web App using Streamlit 
with st.sidebar:
    selected = option_menu("Menu", ["Home", 'Customer Forecast','Dashboard'], 
        icons=['house', 'terminal-plus','tv-fill'], menu_icon="cast", default_index=1)
    
with open('svd_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Page   
if (selected == 'Home'):

    st.title('Welcome to Terra Store Sales Dashboard!')

    img_url = "curved-circles-pattern-vector-141349.jpg"  # Ganti dengan URL gambar yang ingin Anda tampilkan
    st.image(img_url, width=800)
    
    st.balloons()


if (selected == 'Customer Forecast'):
    st.title('Customer Sales Forecast')

    with st.spinner('Please Wait... '):
        time.sleep(1)

    Customer = st.text_input('Customer ID', 'Insert Here!')

    if st.button('Predict') :
        for _ in stqdm(range(50)):
            sleep(0.02)

        if 1 <= int(Customer) <= 5 :

            result_pred = best_products(Customer).reset_index(drop='first')
            
            st.success(f'Here are The Top 3 Products by Customer {Customer}')

            st.dataframe(result_pred)
            

        else :

            st.error('Customer ID is not recognized')



if (selected == 'Dashboard'):
    st.title('Sales Dashboard')

    with st.spinner('Please Wait...'):
        time.sleep(1)
    
    sales_count = pd.DataFrame(sales.groupby('product_id')['product_id'].count()).rename(columns={'product_id':'count'}).reset_index()

    sales_count_date = pd.DataFrame(sales.groupby(['product_id','month'])['product_id'].count()).rename(columns={'product_id':'count'}).reset_index()
    sales_count_date['product_id'] = sales_count_date['product_id'].astype('str')

    sales_date = pd.DataFrame(sales.groupby('month')['month'].count()).rename(columns={'month':'count'}).reset_index()


    st.write('Sales Dashboard by Product')
    st.bar_chart(sales_count, x='product_id', y='count', color="#07A854")

    st.write('Sales Dashboard by Date')
    st.bar_chart(sales_date, x='month', y='count', color="#07A854")

    st.write('Sales Dashboard by Date & Products')
    st.bar_chart(sales_count_date, x='month', y='count', color="product_id")





    