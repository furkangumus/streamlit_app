import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(fruit_choice: str):
  endpoint_url = "https://fruityvice.com/api/fruit/{user_choice}"
  fruityvice_response = requests.get(endpoint_url.format(user_choice=fruit_choice.lower()))
  fruityvice_response_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_response_normalized

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information!")
  else:
    fruit_info = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruit_info)
except URLError as e:
  streamlit.error()

streamlit.stop()
# Snowflake Things
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

fruit_to_add = streamlit.text_input('What fruit would you like add?')
streamlit.write('Thanks for adding', fruit_to_add)

my_cur.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{fruit_to_add}')")
my_cnx.commit()

my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)




