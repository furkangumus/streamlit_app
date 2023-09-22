import streamlit
import pandas as pd

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruits_df = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruits_df = fruits_df.set_index('Fruit')

# Let's put a picker so a user can pick the fruit they want
fruits_list = list(fruits_df.index)
streamlit.multiselect('Pick some fruits:', fruits_list, fruits_list[:2])

# display the table on the screen
streamlit.dataframe(fruits_df)
