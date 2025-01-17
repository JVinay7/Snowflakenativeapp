import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
import plotly.express as px
from main import *
from footer import Footer
from header import Header


Header()
# Table mappings
table_mappings = get_mappings()
transaction_table = table_mappings["transaction_view"]
taxonomy_view = table_mappings["dim_taxonomy_code_view"]

col1, col2 = st.columns([1, 1])  # Adjust the width ratio as needed

# Display the logo in the first column
# with row1:
#     logo_path = "./assets/app_logo.svg"
#     # Load the SVG file content
#     with open('./assets/app_logo.svg', 'r') as file:
#         svg_code = file.read()

#     # Display the SVG using Markdown
#     st.markdown(f"<div>{svg_code}</div>", unsafe_allow_html=True)

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
#             <span style='color:#1D4077;'>Categories</span>
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
#             <span style='color:#1D4077;'>Categories</span>
#         </h1>
#         """, 
#         unsafe_allow_html=True
#     )



page2 = st.container() 
with page2:
    # Add filters to this tab
    create_filter_section("Categories")  

    st.divider()
    # st.markdown("#### Category Metrics")
    st.subheader(
    "Category Metrics",
    help="This section provides key metrics for different categories, such as total spend and the number of suppliers. It helps you understand how spending is distributed across various categories and how many suppliers are engaged in each."
    )
    # Create two main columns
    col1, col2 = st.columns(2)
    
    total_spend = get_total_spend(st.session_state.filters)
    total_suppliers = get_total_suppliers(st.session_state.filters)

   
    # Left column: Diversity Tools and Metrics
    with col1:
        
        st.metric(label="Total Spend", 
                  help="Shows the total amount spent in the categories.",
                  value=total_spend)

    with col2:
        st.metric(label="Total Suppliers", 
                  help="Shows the total number of supplier spent in the categories.",
                  value=total_suppliers)



    chart_col1,chart_col2=st.columns(2)
    with chart_col1:
        st.divider()
        st.subheader("Total Spend by LOB",
        help="This section shows the total spending broken down by different lines of business (LOB). A bar chart visually displays how much is spent in each business line, making it easy to identify which areas have the highest spending."
        )
        plot_spend_by_lob(st.session_state.filters)  # Your chart function

    with chart_col2:
        st.divider()
        st.subheader(
        "Total Spend by Region",
        help="This section displays total spending by region. A bar chart is used to visualize how much has been spent in each region, allowing you to easily compare the spending across different geographic areas."
        )
        plot_spend_by_region(st.session_state.filters)  # Another chart function

  
    col3,col4 = st.columns(2, gap="medium")
    with col3:
        st.divider()
        st.subheader("Strategic Categories",
        help="This table displays the total spend amount (in millions) for each strategic category. It helps in analyzing spend distribution across different strategic business areas."
        )
        display_spend_by_strategic_category(st.session_state.filters)
    with col4:
        st.divider()
        display_spend_by_category_diversity(st.session_state.filters)
        
    

Footer()
