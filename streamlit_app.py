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


# Snowflake Things
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    all_fruits = my_cur.fetchall()
  return all_fruits

def insert_row_snowflake(new_fruit: str):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{new_fruit}')")
  my_cnx.commit()
  return f"Thanks for adding {new_fruit}"

streamlit.header("View Our Fruit List - Add Your Favorites!")
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

fruit_to_add = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add Your Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  result = insert_row_snowflake(fruit_to_add)
  streamlit.text(result)
