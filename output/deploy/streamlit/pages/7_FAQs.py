import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
from footer import Footer
from header import Header
 
# Establish Snowflake session
session = Session.builder.getOrCreate()
Header()
# Define the schema and view to fetch FAQs
schema_name = "FAQS_sh"  # Replace with your schema name
faqs_view = f"{schema_name}.view_from_faq "

def add_vertical_space(lines=1):
    for _ in range(lines):
        st.write(" ")

# Fetch FAQs
@st.cache_data
def fetch_faqs(view_name):
    query = f"""
        SELECT
            question,
            answer
        FROM {view_name}
    """
    return session.sql(query).collect()

# Main app logic
st.markdown("####FAQS - Supplier Analytics")
 
try:
    faqs = fetch_faqs(faqs_view)
   
    if len(faqs) == 0:
        st.warning("**No FAQs Configured...**")
    else:
        add_vertical_space(2)
        for index, item in enumerate(faqs):
            # Display the question
            question = f"##### :blue[{index + 1}. {item['QUESTION']}]"
            st.markdown(question)
           
            # Display the answer
            st.markdown(item['ANSWER'])
           
            # Add a divider and space after each FAQ
            if index + 1 < len(faqs):
                st.divider()
                add_vertical_space(2)
except Exception as e:
    st.error(f"An error occurred while fetching FAQs: {e}")



Footer()