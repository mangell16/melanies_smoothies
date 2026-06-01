# Import python packages
# MGA start over after trying to rename, don't like the organization of this stuff yet 
# 5/30 this is in Untitled and works to add orders 

import streamlit as st
import os
# from snowflake.snowpark.context import get_active_session - removed here in github
from snowflake.snowpark.functions import col
import requests  

# session  = get_active_session()   -- removed here in github, replaced with next 2 lines
cnx = st.connection("snowflake")
session = cnx.session() 


# Write directly to the app
st.title(f":cup_with_straw: Please place your custom Smoothie Order ")
st.write(
  """Please select up to 5 fruits !
  """
)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input('Name on Smoothie Order: ') 
st.write('The name on your order will be: ', name_on_order)

# The ingredients variable is an object (data type) called a LIST. 
# A LIST is different from a DATAFRAME, which is also different from a STRING.
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list: 
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''

          # st.text(smoothiefroot_response.json())
    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

   # smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""

    st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit my Order')

    if time_to_insert:
    # if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅") 

# this allows streamlit to 
#  The requests library allows us to build and sent REST API calls.  Paste the code below into the bottom of your SniS app.


        

