import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

DATAURL = (
	""
	)

st.title("Tacos and Burrito Places in USA")
st.markdown("This is a Streamlit Web App that can be used to look at taco and burrito places in USA.")

@st.cache(persist = True)
def loading(rows):
	data = pd.read_csv(DATAURL, nrows = rows)
	data = data[['id', 'cuisines', 'country', 'categories', 'priceRangeMax', 'latitude', 'longitude', 'menus.name', 'province']]
	data.dropna(subset = ['latitude', 'longitude', 'priceRangeMax'], inplace = True)
	return data

data = loading(77261)

st.subheader('All restaurants that sell tacos or burritos.')
coun = 'US'
st.map(data.query('country == @coun')[['latitude', 'longitude']].dropna(how = 'any'))

prov_list = data['province'].unique()
st.subheader('Restaurants by Province')
prov = st.selectbox('Select Province', prov_list)
st.map(data.query('province == @prov')[['latitude', 'longitude']].dropna(how = 'any'))

st.subheader('Provinces with the most taco/burrito selling places')
num = st.slider('Select number of top provinces:', 0,49)
bar_data = data['province'].value_counts().sort_values(ascending = False).head(num)
st.bar_chart(bar_data)

rest_list = ['Mexican', 'Take Out Restaurants', 'Fast Food', 'Bars', 'Coffee Shops', 'Vegetarian', 'Kosher', 'Vegan', 'Latin']
st.subheader('Taco selling restaurants by specification:')
choice = st.selectbox('Select:', rest_list)
st.map(data.query('cuisines == @choice')[['latitude', 'longitude']].dropna(how = 'any'))

if st.checkbox("Show Raw Data", False):
	st.subheader('Raw Data')
	st.write(data)
