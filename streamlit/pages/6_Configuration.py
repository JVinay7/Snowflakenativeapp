import streamlit as st
from snowflake.snowpark import Session
from footer import Footer
from header import Header

Header()
# Initialize Snowflake session
session = Session.builder.getOrCreate()

# Schema name for the Sample option (adjust as necessary)
sample_schema = "APP_DATA"
# Function to fetch data from Snowflake
@st.cache_data
def fetch_data(query):
    return session.sql(query).to_pandas()

# Function to get all views in a specified schema
@st.cache_data
def get_views(schema_name):
    query = f"""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = '{schema_name}'
    """
    return fetch_data(query)['TABLE_NAME'].tolist()

def display_data(view_option):
    query = f"SELECT * FROM {sample_schema}.{view_option}"
    data_view = fetch_data(query)
    st.write("Displaying only the first 1,000 rows to avoid size limits.")
    st.subheader(view_option)
    st.dataframe(data_view.head(1000), use_container_width=True)



with st.form("engine_run_configuration"):
    st.info(f"""
The Data Source defines the data used for out of stock attribution and populating the dashboard. It supports the following options:

- **Sample**: Placeholder data used to demonstrate the app's features. No additional permissions are required when using this data source.
- **Snowflake**: Utilizes your actual data for out of stocks. This option requires specific **account-level privileges** and **access to certain views**.
""")
    col1, col2 = st.columns([3, 1])
    with col1:
        data_source = st.selectbox("Data Source", ["Sample", "Snowflake"], label_visibility="collapsed")
    with col2:
        on_update = st.form_submit_button("Update", use_container_width=True)

# If "Sample" is selected, dynamically fetch and display the views
    if data_source == "Sample" and on_update :
    # Get the list of views from the schema
        views = get_views(sample_schema)

        if views:
        # Dropdown to select the view
            view_option = st.selectbox("Select the view to display:", options=views)

            # Dynamically fetch and display the data for the selected view
            if view_option:
                display_data(view_option)

        # Fetch and display the data for the selected view
            # display_data(view_option)

        else:
            st.warning(f"No views found in schema '{sample_schema}'.")

# Data for "Snowflake"
    elif data_source == "Snowflake" and on_update:
        st.markdown("### Tables for **Snowflake** Data Source")
        st.info("Snowflake integration requires account-level privileges and access to specific views.")
        st.write("Contact your administrator to enable Snowflake data integration.")

Footer()
