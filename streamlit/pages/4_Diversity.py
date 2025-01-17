import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
import plotly.express as px
from  main import *
from footer import Footer
from header import Header



# Table mappings
table_mappings = get_mappings()
transaction_table = table_mappings["transaction_view"]
taxonomy_view = table_mappings["dim_taxonomy_code_view"]

Header()
# row1, row3 = st.columns([1, 5])
# with row1:
#     logo_path = "./assets/app_logo.svg"
#     # Load the SVG file content
#     with open(logo_path, 'r') as file:
#         svg_code = file.read()

#     # Display the SVG with inline CSS styling
#     st.markdown(
#         f"<div style='width: 100px; height: 100px;'>{svg_code}</div>", 
#         unsafe_allow_html=True
#     )
# # Display the main title in the second column
# with row3:
#     st.markdown(
#         """
#         <h1 style='text-align: left;'>
#             <span style='color:#1D4077;'>Diversity</span>
#         </h1>
#         """, 
#         unsafe_allow_html=True
#     )



# col1 = st.container()
# # Display the main title in the second column
# with col1:
#     st.markdown(
#         """
#         <h1 style='text-align: left;'>
#             <span style='color:#1D4077;'>Diversity</span>
#         </h1>
#         """, 
#         unsafe_allow_html=True
#     )

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

page4 = st.container()
with page4:
    # Add filters to this tab
    create_filter_section("Diversity") 

    st.divider()
    # st.write("<style>div.block-container{padding-bottom: 0rem;}</style>", unsafe_allow_html=True) 
    col1,col2 =st.columns([1,3])
    with col1:
        # st.markdown("#### Diversity metrics")
        st.subheader("Diversity Metrics",
        help="Track diversity spend and suppliers, including their percentage of total spend and supplier count."
        )
        # st.markdown("<div style='margin-bottom: 0px;'></div>", unsafe_allow_html=True)
        # diverse_spend=get_total_diverse_spend(st.session_state.filters)
        diverse_spend_str = get_total_diverse_spend(st.session_state.filters)
        diverse_spend = parse_formatted_spend(diverse_spend_str)
        total_spend_str = get_total_spend(st.session_state.filters)
        total_spend = parse_formatted_spend(total_spend_str)
        # Calculate percentage
        if total_spend > 0:
            percent_total_spend = (diverse_spend / total_spend) * 100
        else:
            percent_total_spend = 0
        
        st.metric(label="Diverse Spend",
                  help="Shows the total amount spent in the Diversity.",
                  value=diverse_spend_str)
        st.metric(label="% Diverse Spend",
                   help="Displays the percentage of total spend attributed to diverse suppliers, calculated dynamically.",
                  value=f"{percent_total_spend:.2f}%")
    
        diverse_suppliers= get_total_diverse_suppliers(st.session_state.filters)
        total_supplier= get_total_suppliers(st.session_state.filters)
        if total_supplier > 0:
            percent_total_supplier = (diverse_suppliers / total_supplier) * 100
        else:
            percent_total_supplier = 0
            
            
        st.metric(label="Diverse Suppliers",
                  help="Displays the total count of suppliers categorized as diverse based on the applied filters",
                  value=diverse_suppliers)
        st.metric(label="% Diverse Suppliers",
                  help="Shows the percentage of suppliers categorized as diverse, calculated relative to the total supplier count.",
                  value=f"{percent_total_supplier:.2f}%")

    # col,col6=st.columns([2,2])
    with col2:
        st.subheader("Spend by Diversity Subtype",
        help="Displays the breakdown of spend by supplier diversity subtype. It includes the total spend for each subtype, the number of suppliers in each category, and the percentage of total spend attributed to each diversity subtype."
        )
        display_spend_by_diversity_subtype(st.session_state.filters)
        # display_spend_by_diversity_subtype(st.session_state.filters)

   
    col3,col4=st.columns([2,2]) 
    with st.container():
        with col4:
            st.divider()
            st.subheader("Spend Analysis by Supplier Ethnicity",
            help="Displays the spend breakdown by supplier ethnicity. The table shows the total spend amount and the number of suppliers for each ethnicity, along with the percentage of total spend represented by each group."
            )
        
            display_spend_by_supplier_ethnicity(st.session_state.filters)
   
        with col3:
            st.divider()
        
            st.subheader("Spend by Supplier Diversity Certification Type",
            help="Visualizes the spend breakdown by supplier diversity certification type. Displays a pie chart showing the distribution of spend among different certification types, along with the percentage of total spend for each type."
           )
            plot_spend_by_diversity_cert_type(st.session_state.filters)
    
    st.divider()
    col5 = st.container()
    with col5:
        st.subheader("Top 20 Suppliers by Diverse Spend",
        help="Displays a horizontal bar chart of the top 20 suppliers based on diverse spend. The chart highlights suppliers with the highest diverse spend, providing an overview of how diverse spending is distributed across suppliers."
        )
        plot_diverse_spend_by_supplier(st.session_state.filters)
        
Footer()