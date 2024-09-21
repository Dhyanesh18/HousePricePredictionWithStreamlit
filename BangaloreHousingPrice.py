import streamlit as st
import pickle
import pandas as pd
import numpy as np


def predict_price(location, area, bath, bhk):
    if location in location_stats_above_10:
        loc_index = np.where(location_stats_above_10 == location)[0][0]
    else:
        loc_index = -1
    x = np.zeros(len(location_stats_above_10) + 3)
    x[0] = area
    x[1] = bath
    x[2] = 7 - bhk

    if loc_index >= 0:
        x[loc_index + 3] = 1 

    return model.predict([x])[0]

def format_price(price):
    if price >= 100:
        return f"{price / 100:.2f} Crore"
    else:
        return f"{price:.2f} Lakhs" 

with open("bangalore_home_prices_model.pickle", "rb") as f:
    model = pickle.load(f)

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
        padding-left : 30px;
        color: #fff;
    }
    .header {
        text-align: center;
        font-size: 24px;
        color: grey;
        padding-left:15px;
        margin-bottom: 30px;
    }
    .price {
        font-size: 24px;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
    }
    </style>
    <div class="container">
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>HOUSING PRICE PREDICTOR</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='header'>BANGALORE</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
area = col2.number_input("AREA (in sqft)", min_value=500, value=1000)
bhk = col2.slider("BHK", min_value=1, max_value=7, value=1)
bathrooms = col2.slider("BATHROOMS", min_value=1, max_value=7, value=1)

df = pd.read_csv("bengaluru_house_prices.csv")
df.location = df.location.apply(lambda x: str(x).strip() if isinstance(x, str) else x)

location_stats = df.groupby('location')['location'].agg('count').sort_values(ascending=False)
location_stats_below_10 = location_stats[location_stats <= 10]
locations = df.location.apply(lambda x: 'other' if x in location_stats_below_10 else x)
location_stats_above_10 = location_stats[location_stats > 10].index.values
location = col2.selectbox("LOCATION:", locations.unique())

col1, col2, col3 = st.columns([3.3, 2, 3])
predict = col2.button("Estimate Price", key="predict_button")
if predict:
    predicted_price = predict_price(location, area, bathrooms, bhk)
    formatted_price = format_price(predicted_price)
    col1, col2, col3 = st.columns([1, 2, 1])
    col2.markdown(f"<p class='price'>ESTIMATED PRICE: {formatted_price}</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2,col3 = st.columns([1.4,1,1])
col2.link_button("STATISTICS", "/Stats?id=1234")

