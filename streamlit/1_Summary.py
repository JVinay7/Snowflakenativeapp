import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
import plotly.express as px
from main import *
from footer import *
from header import *


# # Get the current credentials
# session = Session.builder.getOrCreate()
 
Header()

# Table mappings
table_mappings = get_mappings()
transaction_table = table_mappings["transaction_view"]
taxonomy_view = table_mappings["dim_taxonomy_code_view"]




page1 = st.container() 
with page1:
    create_filter_section("Summary")
    
    
   
    col1, col2, col4,col6,col8,col9,col10,col11,col12 = st.columns(9)
    total_spend = get_total_spend(st.session_state.filters)
    total_diverse_spend = get_total_diverse_spend(st.session_state.filters)
    total_sustainable_spend = get_total_sustainable_spend(st.session_state.filters)
    total_sp_spend = get_total_sp_spend(st.session_state.filters)
    total_competitor_spend = get_total_competitor_spend(st.session_state.filters)
    total_suppliers = get_total_suppliers(st.session_state.filters)
    total_sustainable_suppliers = get_total_sustainable_suppliers(st.session_state.filters)
    total_diverse_suppliers = get_total_diverse_suppliers(st.session_state.filters)
    total_sp_suppliers = get_total_sp_suppliers(st.session_state.filters)
    
    # Get the previous year metrics
    previous_total_spend = get_previous_year_metrics(st.session_state.filters, get_total_spend)
    previous_total_diverse_spend = get_previous_year_metrics(st.session_state.filters, get_total_diverse_spend)
    previous_total_sustainable_spend = get_previous_year_metrics(st.session_state.filters, get_total_sustainable_spend)
    previous_total_sp_spend = get_previous_year_metrics(st.session_state.filters, get_total_sp_spend)
    previous_total_competitor_spend = get_previous_year_metrics(st.session_state.filters, get_total_competitor_spend)
    previous_total_suppliers = get_previous_year_metrics(st.session_state.filters, get_total_suppliers)
    previous_total_sustainable_suppliers = get_previous_year_metrics(st.session_state.filters, get_total_sustainable_suppliers)
    previous_total_diverse_suppliers = get_previous_year_metrics(st.session_state.filters, get_total_diverse_suppliers)
    previous_total_sp_suppliers = get_previous_year_metrics(st.session_state.filters, get_total_sp_suppliers)
    
    st.divider()
    # st.markdown("#### Summary Metrics")
    st.subheader("Summary Metrics",
    help="This section provides an overview of key spend metrics, including total spend, diverse spend, sustainable spend, and spend with competitors. It also displays the number of suppliers across different categories, helping you get a quick snapshot of your spending behavior and supplier engagement."
    )
   
    col1, col2, col4, col6 = st.columns(4)
    with col1:      
        if previous_total_spend is not None:
            current_value = parse_metric_value(total_spend)
            previous_value = parse_metric_value(previous_total_spend)
            if previous_value == 0:
                delta_spend_display = "vs. PY YTD: N/A"  # Handle edge case for zero previous value
            else:
                delta_spend = get_percentage_difference(current_value, previous_value)
                delta_spend_display = f"vs. PY YTD: {delta_spend:+.2f}%"
            # delta_spend = get_percentage_difference(current_value, previous_value)
            # delta_spend_display = f"vs. PY YTD: {delta_spend:.2f}%" if delta_spend is not None else "vs. PY YTD: 0.0"
            st.metric(label="Total Spend",
                      help = "Shows the total amount spent based on your selected filters. It makes sure the spend data is valid and then displays the total", 
                      value=total_spend, delta=delta_spend_display)
        else:
            st.metric(label="Total Spend",
                      help="Shows the total amount spent based on your selected filters. It makes sure the spend data is valid and then displays the total",
                      value=total_spend)

    with col2:
        if previous_total_sp_spend is not None:
            current_value = parse_metric_value(total_sp_spend)
            previous_value = parse_metric_value(previous_total_sp_spend)
            delta_sp_spend = get_percentage_difference(current_value, previous_value)
            delta_sp_spend_display = f"vs. PY YTD: {delta_sp_spend:.2f}%" if delta_sp_spend is not None else "vs. PY YTD: 0.0"
            st.metric(label="S&P Spend",
                      help= "Shows the total spend with your most important suppliers (those labeled as 'Strategic' or 'Preferred')",
                      value=total_sp_spend, delta=delta_sp_spend_display)
        else:
            st.metric(label="S&P Spend",
                      help= "Shows the total spend with your most important suppliers (those labeled as 'Strategic' or 'Preferred')",
                      value=total_sp_spend)

    with col4:
        if previous_total_sustainable_spend is not None:
            current_value = parse_metric_value(total_sustainable_spend)
            previous_value = parse_metric_value(previous_total_sustainable_spend)
            delta_sustainable_spend = get_percentage_difference(current_value, previous_value)
            delta_sustainable_spend_display = f"PY YTD: {delta_sustainable_spend:.2f}%" if delta_sustainable_spend is not None else "PY YTD: 0.0"
            st.metric(label="Sustainable Spend",
                      help="Counts how many suppliers you have who are focused on sustainability (those with a good sustainability score), based on your filters.", 
                      value=total_sustainable_spend, delta=delta_sustainable_spend_display)
        else:
            st.metric(label="Sustainable Spend",
                      help="Counts how many suppliers you have who are focused on sustainability (those with a good sustainability score), based on your filters.",
                      value=total_sustainable_spend)

    with col6:
        if previous_total_diverse_spend is not None:
            current_value = parse_metric_value(total_diverse_spend)
            previous_value = parse_metric_value(previous_total_diverse_spend)
            delta_diverse_spend = get_percentage_difference(current_value, previous_value)
            delta_diverse_spend_display = f"PY YTD: {delta_diverse_spend:.2f}%" if delta_diverse_spend is not None else "PY YTD: 0.0"
            st.metric(label="Diverse Spend",
                      help="Shows how much money you’ve spent with diverse suppliers, based on your filters. It only counts suppliers that meet diversity requirements.",
                      value=total_diverse_spend, delta=delta_diverse_spend_display)
        else:
            st.metric(label="Diverse Spend",
                      help="Shows how much money you’ve spent with diverse suppliers, based on your filters. It only counts suppliers that meet diversity requirements.",
                      value=total_diverse_spend)

    st.markdown("<div style='margin-bottom: 58px;'></div>", unsafe_allow_html=True)
    col8, col9, col10, col11, col12 = st.columns(5)

    with col8:
        if previous_total_competitor_spend is not None:
            current_value = parse_metric_value(total_competitor_spend)
            previous_value = parse_metric_value(previous_total_competitor_spend)
            delta_competitor_spend = get_percentage_difference(current_value, previous_value)
            delta_competitor_spend_display = f"PY YTD: {delta_competitor_spend:.2f}%" if delta_competitor_spend is not None else "PY YTD: 0.0"
            st.metric(label="Competitor Spend", 
                      help="Shows how much money you’ve spent with suppliers who are competitors, based on your selected filters.",
                      value=total_competitor_spend, delta=delta_competitor_spend_display)
        else:
            st.metric(label="Competitor Spend",
                      help="Shows how much money you’ve spent with suppliers who are competitors, based on your selected filters.",
                      value=total_competitor_spend)


    with col9:
        if previous_total_suppliers is not None:
            delta_suppliers = get_percentage_difference(total_suppliers, previous_total_suppliers)
           
            delta_suppliers_display = f"PY YTD: {delta_suppliers:.2f}%" if delta_suppliers is not None else "PY YTD: 0.0"
            st.metric(label="No. of Suppliers",
                      help="Counts how many suppliers you have based on the filters you choose. It shows the number of suppliers that have valid transactions.",
                      value=total_suppliers, delta=delta_suppliers_display)
        else:
            st.metric(label="No. of Suppliers", 
                      help="Counts how many suppliers you have based on the filters you choose. It shows the number of suppliers that have valid transactions.",
                      value=total_suppliers)

    with col10:
        if previous_total_sustainable_suppliers is not None:
            delta_sustainable_suppliers = get_percentage_difference(total_sustainable_suppliers, previous_total_sustainable_suppliers)
            delta_sustainable_suppliers_display = f"PY YTD: {delta_sustainable_suppliers:.2f}%" if delta_sustainable_suppliers is not None else "PY YTD: 0.0"
            st.metric(label="Sustainable Suppliers",
                      help="Counts how many suppliers you have who are focused on sustainability (those with a good sustainability score), based on your filters.",
                      value=total_sustainable_suppliers, delta=delta_sustainable_suppliers_display)
        else:
            st.metric(label="Sustainable Suppliers", 
                      help="Counts how many suppliers you have who are focused on sustainability (those with a good sustainability score), based on your filters.",
                      value=total_sustainable_suppliers)

    with col11:
        if previous_total_diverse_suppliers is not None:
            delta_diverse_suppliers = get_percentage_difference(total_diverse_suppliers, previous_total_diverse_suppliers)
            delta_diverse_suppliers_display = f"PY YTD: {delta_diverse_suppliers:.2f}%" if delta_diverse_suppliers is not None else "PY YTD: 0.0"
            st.metric(label="Diverse Suppliers",
                      help="Shows how many diverse suppliers (with specific diversity categories) you have, based on your selected filters.",
                      value=total_diverse_suppliers, delta=delta_diverse_suppliers_display)
        else:
            st.metric(label="Diverse Suppliers",
                      help="Shows how many diverse suppliers (with specific diversity categories) you have, based on your selected filters.",
                      value=total_diverse_suppliers)

    with col12:
        if previous_total_sp_suppliers is not None:
            delta_sp_suppliers = get_percentage_difference(total_sp_suppliers, previous_total_sp_suppliers)
            delta_sp_suppliers_display = f"PY YTD: {delta_sp_suppliers:.2f}%" if delta_sp_suppliers is not None else "PY YTD: 0.0"
            st.metric(label="S&P Suppliers", 
                      help="Counts how many of your suppliers are classified as 'Strategic' or 'Preferred' based on your filters.",
                      value=total_sp_suppliers, delta=delta_sp_suppliers_display)
        else:
            st.metric(label="S&P Suppliers", 
                      help="Counts how many of your suppliers are classified as 'Strategic' or 'Preferred' based on your filters.",
                      value=total_sp_suppliers)
     
         
    col13,col14 = st.columns([2,2])
    with st.container():
        with col14:
            st.divider()
            st.subheader(
                "Total Spend By Month",
                help="This section shows how much money was spent each month, displayed as a bar chart. The months are shown in order from January to December, making it easy to track spending trends over the year."
            )
            plot_spend_by_month(st.session_state.filters)
    with st.container():
        with col13:
            st.divider()
            
          
            display_spend_by_category(st.session_state.filters)
    

    col15 = st.container()

    with col15:
        st.divider()
        st.subheader("Top 10 Suppliers by Total Spend",
        help="This section shows the top 10 suppliers based on the total spending. A bar chart displays each supplier's name and the amount spent, making it easy to identify the most significant suppliers.")
        plot_top_suppliers(st.session_state.filters)
    col16 = st.container()
    with col16:
        #st.title("Spend Analysis Dashboard")
        # Dropdown for metric selection
        st.divider()
        metric_options = ["COUNTRY", "LINE_OF_BUSINESS", "GLOBAL_REGION", "CLIENT", "SOURCE_SYSTEM", "BUSINESS_SEGMENT", "SPEND_CATEGORY"]
        
        # st.markdown("#### Spend Amount")
        st.subheader("Spend Amount across different metrics ",
        help="This section allows you to view spending across different metrics, such as supplier names, categories, or regions. The top 10 results are displayed as a bar chart, showing the total spending in billions of dollars for the selected metric. You can adjust filters to refine the results.")
        selected_metric = st.selectbox("", metric_options,format_func=lambda x: x.replace("_", " "))
        

        # Call the function to plot the dynamic bar graph
        if selected_metric:
            plot_dynamic_bar_graph(selected_metric,st.session_state.filters)

    col17 = st.container()
    
    with col17:
        st.divider()
        st.subheader("Spend per LOB and Region",
        help="This section displays the total spend broken down by different lines of business and regions. A table shows how much was spent in each region for each business line, making it easy to analyze spending across different areas."
        )
       
        
        display_spend_per_lob_region(st.session_state.filters)

    Footer()