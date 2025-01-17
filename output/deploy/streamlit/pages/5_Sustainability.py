import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
import plotly.express as px
from main import *
from footer import Footer
from header import Header


# Table mappings
table_mappings = get_mappings()
transaction_table = table_mappings["transaction_view"]
taxonomy_view = table_mappings["dim_taxonomy_code_view"]

Header()

def parse_formatted_spend(spend_str):
    """
    Parse a formatted spend string (e.g., '284.16M', '1.2bn') into a numeric value.
    """
    try:
        if spend_str.endswith('M'):
            return float(spend_str[:-1]) * 1_000_000
        elif spend_str.endswith('bn'):
            return float(spend_str[:-2]) * 1_000_000_000
        else:
            return float(spend_str)  # Direct numeric value
    except ValueError:
        return 0  # Default to 0 if parsing fails 

page5 = st.container()
with page5:
    # Add filters to this tab
    create_filter_section("Sustainability")
     
    
    

# Metrics and bar graph layout
    st.divider()
    col1, col2= st.columns([1, 2])  # Adjust width proportions for bar graph
    with col1:
        st.subheader(
        "Sustainability Metrics",
        help="Displays key sustainability metrics, including the total sustainable spend and number of sustainable suppliers. Track your organization's commitment to sustainable practices across the supply chain."
        )
       
        sustainable_spend_str = get_total_sustainable_spend(st.session_state.filters)
        sustainable_spend = parse_formatted_spend(sustainable_spend_str)
        total_spend_str = get_total_spend(st.session_state.filters)
        total_spend = parse_formatted_spend(total_spend_str)
        # Calculate percentage
        if total_spend > 0:
            percent_total_spend = (sustainable_spend / total_spend) * 100
        else:
            percent_total_spend = 0
        
        st.metric(label="Sustainable Spend",
                  help="Shows the total spend categorized as sustainable, formatted for clarity and based on the applied filters.",
                  value=sustainable_spend_str)
        st.metric(label="% Sustainable Spend", 
                  help="Displays the percentage of total spend attributed to Sustainable suppliers, calculated dynamically.",
                  value=f"{percent_total_spend:.2f}%")

    # Second row
        sustainable_suppliers = get_total_sustainable_suppliers(st.session_state.filters)
        total_supplier= get_total_suppliers(st.session_state.filters)
        if total_supplier > 0:
            percent_total_supplier = (sustainable_suppliers / total_supplier) * 100
        else:
            percent_total_supplier = 0
        st.metric(label="Sustainable Suppliers",
                  help="Displays the total count of suppliers categorized as sustainable based on the applied filters.",
                  value=sustainable_suppliers)
        st.metric(label="%  Sustainable Suppliers",
                  help="Shows the percentage of suppliers categorized as sustainable, calculated relative to the total supplier count.",
                  value=f"{percent_total_supplier:.2f}%")

    with col2:
        st.subheader("Spend Distribution by Supplier Sustainability Rating",
        help="Visualizes the distribution of spend across different supplier sustainability ratings. The chart helps assess how much of the total spend is attributed to suppliers based on their sustainability performance."
        )
        
        plot_spend_by_sust_rating(st.session_state.filters)
          
    st.divider()
    col3 = st.container()
    with col3:
        st.subheader("Top 10 Sustainable Suppliers by Spend",
        help="This chart displays the top 10 suppliers with the highest spend who have a sustainability score of 60 or higher. It helps identify the key contributors to sustainable spend."
        )
        plot_sustainable_suppliers_spend(st.session_state.filters)
    st.divider()
    col4 = st.container()
    with col4:
        metric_options = ["COUNTRY", "LINE_OF_BUSINESS", "GLOBAL_REGION", "CLIENT", "SOURCE_SYSTEM", "BUSINESS_SEGMENT", "SPEND_CATEGORY"]
        st.subheader("Sustainable Spend Analysis",
        help="Select a metric (e.g., Country, Business Segment) to analyze sustainable spend distribution. The dynamic table provides insights based on the chosen metric."
        )
        selected_metric = st.selectbox("", metric_options)

        # Call the function to plot the dynamic bar graph
        if selected_metric:
            display_dynamic_Sustainable_table(selected_metric,st.session_state.filters)

Footer()  
