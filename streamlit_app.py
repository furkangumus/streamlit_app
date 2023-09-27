import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruits_df = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruits_df = fruits_df.set_index('Fruit')

# Let's put a picker so a user can pick the fruit they want
fruits_list = list(fruits_df.index)
selected_fruits = streamlit.multiselect('Pick some fruits:', fruits_list, fruits_list[:2])
fruits_to_show = fruits_df.loc[selected_fruits]

# display the table on the screen
streamlit.dataframe(fruits_to_show)

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

endpoint_url = "https://fruityvice.com/api/fruit/{user_choice}"
fruityvice_response = requests.get(endpoint_url.format(user_choice=fruit_choice.lower()))

# take the json response and normalize it
fruityvice_response_normalized = pd.json_normalize(fruityvice_response.json())
# output the normalized fruityvice response as a table
streamlit.dataframe(fruityvice_response_normalized)

# Snowflake Things
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
