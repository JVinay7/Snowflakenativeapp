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
#             <span style='color:#1D4077;'>Suppliers</span>
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
#             <span style='color:#1D4077;'>Suppliers</span>
#         </h1>
#         """, 
#         unsafe_allow_html=True
#     )
# st.write("<style>div.block-container{padding-bottom: 0rem;}</style>", unsafe_allow_html=True)
page3 = st.container()
with page3:
    # Add filters to this tab
    create_filter_section("Suppliers") 
    # col1,col2,col3 = st.columns([1,1,1])
    
    col1,col2 = st.columns([1.8,2.5])
    # with st.container():
    
    with col2:
        st.divider()
        # plot_supplier_classification_trend(st.session_state.filters)
        st.subheader("Spend Analysis by Supplier Classification",
        help="This section provides a detailed breakdown of spending by supplier classification. The table shows the total spend, supplier count, and the percentage of total spend and supplier count for each classification. It helps analyze how spend is distributed across different supplier categories, including 'Unclassified' suppliers."
        )
        display_spend_by_supplier_classification(st.session_state.filters)

    with col1:
        st.divider()
        st.subheader("Spend Classification %",
        help="This section shows the total spending categorized by supplier classification. A donut chart visually represents the proportion of spend between 'Qualified' suppliers and others. It helps understand how much spend is allocated to each classification, with detailed breakdowns of the total spend and supplier count."
        )
        plot_spend_by_supplier_classification(st.session_state.filters)
    
    col3,col4 = st.columns(2)
 
    with col3:
        st.divider()
        st.subheader(
        "Monthly Spend: Qualified vs S&P",
        help="This section displays the monthly spend for suppliers categorized as 'Qualified' and 'S&P'. The bar chart differentiates between these two classifications to show how each contributes to the overall spend on a monthly basis. It helps track trends in spending over time for both types of suppliers."
        )
        plot_spend_per_supplier_classification_month(st.session_state.filters)
      
   
    with col4:
        st.divider()
        st.subheader("Supplier Count Trend: Qualified vs S&P",
        help="This chart shows the trend in the number of suppliers categorized as 'Qualified' and 'S&P' over time (monthly). It helps identify patterns in supplier classifications and their changes over different months. Tracking this trend can highlight how supplier classifications evolve, providing insights into the balance of strategic vs non-strategic suppliers."
        )
        plot_supplier_classification_trend(st.session_state.filters)
  
    
    
    col5 = st.container()
    with col5:
        st.divider()
        metric_options = ["COUNTRY", "LINE_OF_BUSINESS", "GLOBAL_REGION", "CLIENT", "SOURCE_SYSTEM", "BUSINESS_SEGMENT", "SPEND_CATEGORY"]
        # st.markdown("#### S&P Compliance %")
        st.subheader("S&P Compliance %",
        help="This section allows you to visualize the percentage of compliance with S&P categories across different metrics. You can select a metric such as Country, Line of Business, or Region to explore how S&P compliance is distributed within that category. Understanding compliance trends is essential for ensuring that spend management aligns with S&P objectives and policies."
        )
        selected_metric = st.selectbox("", metric_options,format_func=lambda x: x.replace("_", " "))
        if selected_metric:
            plot_dynamic_SP_bar_graph(selected_metric,st.session_state.filters)
Footer()