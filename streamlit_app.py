# Import python packages
# MGA start over after trying to rename, don't like the organization of this stuff yet 
# 5/30 this is in Untitled and works to add orders 

import streamlit as st
import os
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Please place your custom Smoothie Order ")
st.write(
  """Please select up to 5 fruits !
  """
)
session  = get_active_session()
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
    
    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""

    st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit my Order')

    if time_to_insert:
    # if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="?")
        
# st.markdown("""
# - :page_with_curl: [Streamlit open source documentation] (https://docs.streamlit.io)
# - :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
# - :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
# - :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
#   """)

# Create a database connection to Snowflake
# conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
# session = conn.session()

# Use an interactive slider to get user input
# hifives_val = st.slider(
#   "Number of high-fives in Q3",
#   min_value=0,
#   max_value=90,
#   value=60,
#   help="Use this to enter the number of high-fives you gave in Q3",
# )

#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
# created_dataframe = session.create_dataframe(
#   [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
#   schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
# )

# Execute the query and convert it into a Pandas dataframe
# queried_data = created_dataframe.to_pandas()

# Create a simple bar chart
# See docs.streamlit.io for more types of charts
# st.subheader("Number of high-fives")
# st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

# st.subheader("Underlying data")
# st.dataframe(queried_data, use_container_width=True)
