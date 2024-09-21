import streamlit as st
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, '../bengaluru_house_prices.csv')

df = pd.read_csv(csv_path)
df = df.dropna(subset=['size', 'bath', 'price', 'total_sqft'])

df['BHK'] = df['size'].str.extract('(\d+)').astype(int)
df['BHK'] = df['BHK'].clip(upper=7)  
df['bath'] = df['bath'].clip(upper=7)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['total_sqft'] = pd.to_numeric(df['total_sqft'], errors='coerce')

df = df.dropna(subset=['price', 'total_sqft'])
df['availability_category'] = df['availability'].apply(lambda x: 'Ready to Move' if 'Ready To Move' in str(x) else 'Others')


average_price_by_bhk = df.groupby('BHK')['price'].mean()
average_price_by_bath = df.groupby('bath')['price'].mean()
average_price_by_availability = df.groupby('availability_category')['price'].mean()
average_price_by_bhk_sorted = average_price_by_bhk.sort_index()
average_price_by_bath_sorted = average_price_by_bath.sort_index()
average_price_by_availability_sorted = average_price_by_availability.sort_values() 

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
        padding-left: 30px;
        color: #fff;
    }
    </style>
    <div class="container">
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>STATISTICS</h1>", unsafe_allow_html=True)
st.markdown("## PRICE vs BHK")
st.bar_chart(average_price_by_bhk_sorted)

st.markdown("## PRICE vs BATHROOMS")
st.bar_chart(average_price_by_bath_sorted)

st.markdown("## AVERAGE PRICE BY AVAILABILITY STATUS")
st.bar_chart(average_price_by_availability_sorted)


df['price_per_sqft_bhk'] = df['price'] / (df['total_sqft']*df['BHK'])
location_counts = df['location'].value_counts()
filtered_locations = location_counts[location_counts > 10].index 
average_price_per_sqft = df[df['location'].isin(filtered_locations)].groupby('location')['price_per_sqft_bhk'].mean()

st.write("Average price per sqft for filtered locations:")
st.write(average_price_per_sqft.sort_values(ascending=False))

st.markdown("</div>", unsafe_allow_html=True)
