import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def add_vertical_space(lines=1):
    for _ in range(lines):
        st.write(" ")


def get_session():
    session = Session.builder.getOrCreate()
    return session

def get_mappings():
    schema_name = "app_data"
    database_name = "app"

    return {
        "schema_name": schema_name,
        "database_name": database_name,
        "dim_taxonomy_code_view": f"{database_name}.{schema_name}.DIM_TAXONOMY_CODE",
        "transaction_view": f"{database_name}.{schema_name}.FACT_SUPP_ANALYTICS_SPEND_TRANSACTION"
    }

# Table mappings
table_mappings = get_mappings()
transaction_table = table_mappings["transaction_view"]
taxonomy_view = table_mappings["dim_taxonomy_code_view"]

st.set_page_config(layout="wide")
# col1, col2 = st.columns([1, 3])



def initialize_filters():
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "year_filter": "All",
            "month_filter": "All",
            "supplier_name": "All",
            "norm_supplier_name": "All",
            "country": "All",
            "business_segment": "All",
            "line_of_business": "All",
            "global_region": "All",
            "sector_vertical": "All",
            "pjm_v_fm":"All"
        }
    
# Initialize filters
initialize_filters()



# Function to get unique values for dropdown filters
def get_unique_values(column_name, table_name=transaction_table):
    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    result = get_session().sql(query).toPandas()
    
    # Remove None or NaN values and convert to string for sorting
    return [str(value) for value in result[column_name].dropna().tolist()]

# Fetch unique values for dropdown filters
def build_query(filters):
    base_query = f"SELECT * FROM {transaction_table}"
    where_clauses = []

    # Filter for each field, add to where_clauses if not "All"
    if filters['year_filter'] != "All":
        where_clauses.append(f"SPEND_YEAR = '{filters['year_filter']}'")
    if filters['month_filter'] != "All":
        where_clauses.append(f"SPEND_MONTH = '{filters['month_filter']}'")
    if filters['supplier_name'] != "All":
        where_clauses.append(f"SUPPLIER_NAME = '{filters['supplier_name']}'")
    if filters['norm_supplier_name'] != "All":
        where_clauses.append(f"SUPPLIER_NORM_NAME = '{filters['norm_supplier_name']}'")
    if filters['country'] != "All":
        where_clauses.append(f"COUNTRY = '{filters['country']}'")
    if filters['business_segment'] != "All":
        where_clauses.append(f"BUSINESS_SEGMENT = '{filters['business_segment']}'")
    if filters['line_of_business'] != "All":
        where_clauses.append(f"LINE_OF_BUSINESS = '{filters['line_of_business']}'")
    if filters['global_region'] != "All":
        where_clauses.append(f"GLOBAL_REGION = '{filters['global_region']}'")
    if filters['sector_vertical'] != "All":
        where_clauses.append(f"SECTOR_VERTICAL = '{filters['sector_vertical']}'")
    if filters['pjm_v_fm'] != "All":
        where_clauses.append(f"PJM_V_FM = '{filters['pjm_v_fm']}'")

        
    # Combine the WHERE clauses
    if where_clauses:
        return base_query + " WHERE " + " AND ".join(where_clauses)
    return base_query


def display_info_one_line(filters):
    if all(value == "All" for value in filters.values()):
        st.info("Supplier analytics for all options. Use filters to refine your analysis.")
    else:
        selected_values = ", ".join(f"**{value}**" for value in filters.values() if value != "All")
        st.info(f"Supplier analytics for selected options - {selected_values}.")


def create_filter_section(page_name):
    # Display filters in two rows
    col1, col2, col3, col4, col5 = st.columns(5)
 
    def update_filter(filter_key, new_value):
        if st.session_state.filters[filter_key] != new_value:
            st.session_state.filters[filter_key] = new_value
            st.experimental_rerun()  # Trigger rerun to apply filter updates
 
    with col1:
        year_options = ["All"] + sorted(get_unique_values("SPEND_YEAR"))
        year_selected = st.selectbox(
            "Year",
            year_options,
            index=year_options.index(st.session_state.filters["year_filter"]),
            key=f"year_filter_{page_name}",
        )
        update_filter("year_filter", year_selected)
 
    with col2:
        month_options = ["All"] + sorted(get_unique_values("SPEND_MONTH"))
        month_selected = st.selectbox(
            "Month",
            month_options,
            index=month_options.index(st.session_state.filters["month_filter"]),
            key=f"month_filter_{page_name}",
        )
        update_filter("month_filter", month_selected)
 
    with col3:
        supplier_options = ["All"] + sorted(get_unique_values("SUPPLIER_NAME"))
        supplier_selected = st.selectbox(
            "Supplier Name",
            supplier_options,
            index=supplier_options.index(st.session_state.filters["supplier_name"]),
            key=f"supplier_name_{page_name}",
        )
        update_filter("supplier_name", supplier_selected)
 
    with col4:
        norm_supplier_options = ["All"] + sorted(get_unique_values("SUPPLIER_NORM_NAME"))
        norm_supplier_selected = st.selectbox(
            "Supplier Norm Name",
            norm_supplier_options,
            index=norm_supplier_options.index(st.session_state.filters["norm_supplier_name"]),
            key=f"norm_supplier_name_{page_name}",
        )
        update_filter("norm_supplier_name", norm_supplier_selected)
 
    with col5:
        country_options = ["All"] + sorted(get_unique_values("COUNTRY"))
        country_selected = st.selectbox(
            "Country",
            country_options,
            index=country_options.index(st.session_state.filters["country"]),
            key=f"country_{page_name}",
        )
        update_filter("country", country_selected)
 
    # Second row of filters
    col6, col7, col8, col9, col10 = st.columns(5)
 
    with col6:
        business_segment_options = ["All"] + sorted(get_unique_values("BUSINESS_SEGMENT"))
        business_segment_selected = st.selectbox(
            "Business Segment",
            business_segment_options,
            index=business_segment_options.index(st.session_state.filters["business_segment"]),
            key=f"business_segment_{page_name}",
        )
        update_filter("business_segment", business_segment_selected)
 
    with col7:
        line_of_business_options = ["All"] + sorted(get_unique_values("LINE_OF_BUSINESS"))
        line_of_business_selected = st.selectbox(
            "Line of Business",
            line_of_business_options,
            index=line_of_business_options.index(st.session_state.filters["line_of_business"]),
            key=f"line_of_business_{page_name}",
        )
        update_filter("line_of_business", line_of_business_selected)
 
    with col8:
        global_region_options = ["All"] + sorted(get_unique_values("GLOBAL_REGION"))
        global_region_selected = st.selectbox(
            "Global Region",
            global_region_options,
            index=global_region_options.index(st.session_state.filters["global_region"]),
            key=f"global_region_{page_name}",
        )
        update_filter("global_region", global_region_selected)
 
    with col9:
        sector_vertical_options = ["All"] + sorted(get_unique_values("SECTOR_VERTICAL"))
        sector_vertical_selected = st.selectbox(
            "Sector Vertical",
            sector_vertical_options,
            index=sector_vertical_options.index(st.session_state.filters["sector_vertical"]),
            key=f"sector_vertical_{page_name}",
        )
        update_filter("sector_vertical", sector_vertical_selected)
 
    with col10:
        pjm_v_fm_options = ["All"] + sorted(get_unique_values("PJM_V_FM"))
        pjm_v_fm_selected = st.selectbox(
            "PJM V FM",
            pjm_v_fm_options,
            index=pjm_v_fm_options.index(st.session_state.filters["pjm_v_fm"]),
            key=f"pjm_v_fm_{page_name}",
        )
        update_filter("pjm_v_fm", pjm_v_fm_selected)
        
    display_info_one_line(st.session_state.filters)
        
# display_filters()


        



def format_spend(amount,use_suffix=True):
    """
    Format the amount based on its value:
    - Billions if amount >= 1 billion
    - Millions if amount >= 1 million but < 1 billion
    - Directly display if less than 1 million
    """
    if use_suffix:
        if amount >= 1_000_000_000:  # 1 billion
            return f"{amount / 1_000_000_000:.2f}bn"
        elif amount >= 1_000_000:  # 1 million
            return f"{amount / 1_000_000:.2f}M"
        else:
            return f"{amount:.2f}"  # Directly display the amount
    else:
        # Plain formatting with commas
        return f"{amount:,.2f}"



def get_total_spend(filters):
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)
    # Check if result_df is empty or TOTAL_SPEND is NaN
    if result_df.empty or pd.isna(result_df.iloc[0]['TOTAL_SPEND']):
        total_spend = 0  # Default to 0 if no data matches the filters
    else:
        total_spend = result_df.iloc[0]['TOTAL_SPEND']

    # # Check if result_df is empty and if 'total_spend' exists
    # #if not result_df.empty and 'TOTAL_SPEND' in result_df.columns:
    # total_spend= result_df.iloc[0]['TOTAL_SPEND']
    return format_spend(total_spend,use_suffix=True)

def get_total_suppliers(filters):
    #query = build_query(filters).replace("SELECT *", "SELECT COUNT(SUPPLIER_NAME) AS TOTAL_SUPPLIERS")
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS TOTAL_SUPPLIERS
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)


    # Check if result_df is empty and if 'total_spend' exists
    if not result_df.empty and 'TOTAL_SUPPLIERS' in result_df.columns:
        return result_df.iloc[0]['TOTAL_SUPPLIERS']
    
    # If the DataFrame is empty or 'total_spend' does not exist, return 0
    return 0

# Display total spend metric

def get_total_diverse_suppliers(filters):
    #query = build_query(filters).replace("SELECT *", "SELECT COUNT(SUPPLIER_NAME) AS TOTAL_SUPPLIERS")
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS TOTAL_SUPPLIERS
    FROM ({base_query}) AS subquery
    WHERE SUPPLIER_DIV_SUBTYPE is not null and INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)


    # Check if result_df is empty and if 'total_spend' exists
    if not result_df.empty and 'TOTAL_SUPPLIERS' in result_df.columns:
        return result_df.iloc[0]['TOTAL_SUPPLIERS']
    
    # If the DataFrame is empty or 'total_spend' does not exist, return 0
    return 0

def get_total_diverse_spend(filters):
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE SUPPLIER_DIV_SUBTYPE is not null and INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas() 
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)
    # Handle cases where the result is empty or TOTAL_SPEND is NaN
    if result_df.empty or pd.isna(result_df.iloc[0]['TOTAL_SPEND']):
        total_spend = 0
    else:
        total_spend = result_df.iloc[0]['TOTAL_SPEND']
    # Check if result_df is empty and if 'total_spend' exists
    #if not result_df.empty and 'TOTAL_SPEND' in result_df.columns:
    # total_spend= result_df.iloc[0]['TOTAL_SPEND']
    return format_spend(total_spend,use_suffix=True)

def get_total_sustainable_spend(filters):
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE SUPPLIER_SUST_OVERALL_SCORE >= 60 and INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)

    # Check if result_df is empty or TOTAL_SPEND is NaN
    if result_df.empty or pd.isna(result_df.iloc[0]['TOTAL_SPEND']):
        total_spend = 0  # Default to 0 if no data matches the filters
    else:
        total_spend = result_df.iloc[0]['TOTAL_SPEND']
    # Check if result_df is empty and if 'total_spend' exists
    #if not result_df.empty and 'TOTAL_SPEND' in result_df.columns:
    # total_spend= result_df.iloc[0]['TOTAL_SPEND']
    return format_spend(total_spend,use_suffix=True)

def get_total_sp_spend(filters):
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE SUPPLIER_CLASSIFICATION IN ('Strategic','Preferred') and INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)
    # Handle cases where the result is empty or TOTAL_SPEND is NaN
    if result_df.empty or pd.isna(result_df.iloc[0]['TOTAL_SPEND']):
        total_spend = 0
    else:
        total_spend = result_df.iloc[0]['TOTAL_SPEND']

    # Check if result_df is empty and if 'total_spend' exists
    #if not result_df.empty and 'TOTAL_SPEND' in result_df.columns:
    # total_spend= result_df.iloc[0]['TOTAL_SPEND']
    return format_spend(total_spend,use_suffix=True)

def get_total_competitor_spend(filters):
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE COMPETITOR_STATUS is not null and INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)

    # Check if result_df is empty or TOTAL_SPEND is NaN
    if result_df.empty or pd.isna(result_df.iloc[0]['TOTAL_SPEND']):
        total_spend = 0  # Default to 0 if no data matches the filters
    else:
        total_spend = result_df.iloc[0]['TOTAL_SPEND']
    # Check if result_df is empty and if 'total_spend' exists
    #if not result_df.empty and 'TOTAL_SPEND' in result_df.columns:
    # total_spend= result_df.iloc[0]['TOTAL_SPEND']
    return format_spend(total_spend,use_suffix=True)

def get_total_suppliers(filters):
    #query = build_query(filters).replace("SELECT *", "SELECT COUNT(SUPPLIER_NAME) AS TOTAL_SUPPLIERS")
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS TOTAL_SUPPLIERS
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)


    # Check if result_df is empty and if 'total_spend' exists
    if not result_df.empty and 'TOTAL_SUPPLIERS' in result_df.columns:
        return result_df.iloc[0]['TOTAL_SUPPLIERS']
    
    # If the DataFrame is empty or 'total_spend' does not exist, return 0
    return 0

def get_total_sustainable_suppliers(filters):
    #query = build_query(filters).replace("SELECT *", "SELECT COUNT(SUPPLIER_NAME) AS TOTAL_SUPPLIERS")
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS TOTAL_SUPPLIERS
    FROM ({base_query}) AS subquery
    WHERE SUPPLIER_SUST_OVERALL_SCORE >= 60 and INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)


    # Check if result_df is empty and if 'total_spend' exists
    if not result_df.empty and 'TOTAL_SUPPLIERS' in result_df.columns:
        return result_df.iloc[0]['TOTAL_SUPPLIERS']
    
    # If the DataFrame is empty or 'total_spend' does not exist, return 0
    return 0


def get_total_sp_suppliers(filters):
    #query = build_query(filters).replace("SELECT *", "SELECT COUNT(SUPPLIER_NAME) AS TOTAL_SUPPLIERS")
    base_query = build_query(filters)
    #query = build_query(filters).replace("SELECT *", "SELECT SUM(INV_LINE_AMT_USD) AS total_spend")
    query = f"""
    SELECT  COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS TOTAL_SUPPLIERS
    FROM ({base_query}) AS subquery
    WHERE SUPPLIER_CLASSIFICATION IN ('Strategic','Preferred') and INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    
    """
    # Log the query for debugging
    #st.write("Executing Query:", query)

    result_df = get_session().sql(query).toPandas()
    
    # Debugging output
    #st.write("Result DataFrame:", result_df)


    # Check if result_df is empty and if 'total_spend' exists
    if not result_df.empty and 'TOTAL_SUPPLIERS' in result_df.columns:
        return result_df.iloc[0]['TOTAL_SUPPLIERS']
    
    # If the DataFrame is empty or 'total_spend' does not exist, return 0
    return 0


def get_previous_year_metrics(filters, metric_function):
    """
    Get the metric for the previous year if a year filter is selected.
    If 'All' is selected for the year, return None.
    """
    if filters['year_filter'] == "All":
        return None  # Don't calculate the previous year metric if "All" is selected
    
    # Modify the filters to get the previous year's metrics
    previous_year_filters = filters.copy()
    previous_year_filters['year_filter'] = str(int(filters['year_filter']) - 1)
    
    # Fetch the metric for the previous year
    previous_year_metric = metric_function(previous_year_filters)
    
    return previous_year_metric



import math
def parse_metric_value(metric_value):
    """
    Convert the metric value (e.g., '284.09M', '63707.09', or numeric values) into a float for calculation.
    Handles None and NaN gracefully.
    """
    # Handle None or NaN
    if metric_value is None or (isinstance(metric_value, float) and math.isnan(metric_value)):
        return 0.0  # Default value or customize as needed
    
    # Handle numeric types
    if isinstance(metric_value, (int, float)):
        return float(metric_value)
    
    # Process string values with suffixes
    if isinstance(metric_value, str):
        if "M" in metric_value:
            return float(metric_value.replace("M", "")) * 1_000_000
        elif "bn" in metric_value:
            return float(metric_value.replace("bn", "")) * 1_000_000_000
        else:
            return float(metric_value)  # Plain numeric string
    
    # Raise an error for unsupported types
    raise ValueError(f"Unsupported metric value type: {type(metric_value)}")

def get_percentage_difference(current_value, previous_value):
    """
    Calculate the percentage difference between the current and previous values.
    """
    if previous_value == 0:
        return None  # Avoid division by zero
    return (current_value - previous_value) / previous_value * 100

def plot_spend_by_month(filters):
    # Build query for spending by month
    base_query = build_query(filters)
    query = f"""
    SELECT SPEND_MONTH, SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    GROUP BY SPEND_MONTH 
    """

    # Debug: Print the generated SQL query
    # st.write("Executing Query for Spend by Month:", query)
    
    try:
        spend_by_month_df = get_session().sql(query).toPandas()
        
        # Convert SPEND_MONTH to a categorical type with a specified order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        spend_by_month_df['SPEND_MONTH'] = pd.Categorical(spend_by_month_df['SPEND_MONTH'], categories=month_order, ordered=True)

        # Sort the DataFrame by SPEND_MONTH
        spend_by_month_df.sort_values('SPEND_MONTH', inplace=True)

        # Create a bar graph
        fig = px.bar(spend_by_month_df, x='SPEND_MONTH', y='TOTAL_SPEND',labels={'TOTAL_SPEND': 'Total Spend ($)', 'SPEND_MONTH': 'Month'},  # You can map colors to the months or any category
                      width = 180,height = 385)
        # Update layout to make labels bold and change their color
        fig.update_layout(
            xaxis=dict(
                title='<b>Month</b>',
                title_font=dict(size=15, family='Arial', weight='bold', color='black'),  # Bold and blue color for X axis title
                # tickfont=dict(size=12, color='green')  # Green color for X axis ticks
            ),
            yaxis=dict(
                title='<b>Total Spend ($)</b>',
                title_font=dict(size=15, family='Arial', weight='bold', color='black'),  # Bold and blue color for Y axis title
                # tickfont=dict(size=12, color='green')  # Green color for Y axis ticks
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot area
        )
        
        # Render the bar graph
        fig.update_layout(
            margin=dict(t=7, b=10),  # Reduce top and bottom margins for the chart
        )

        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error executing query: {e}")


def plot_top_suppliers(filters):
    # Build query for top suppliers
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_NAME, SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    GROUP BY SUPPLIER_NAME 
    ORDER BY TOTAL_SPEND DESC 
    LIMIT 10
    """

    try:
        top_suppliers_df = get_session().sql(query).toPandas()
        
        # Create the bar chart using Plotly Express
        fig = px.bar(top_suppliers_df, 
                     x='TOTAL_SPEND', 
                     y='SUPPLIER_NAME', 
                     labels={'TOTAL_SPEND': '<b>Total Spend ($)</b>', 
                             'SUPPLIER_NAME': '<b>Supplier Name</b>'},
                     color='TOTAL_SPEND',  # Bar color based on the spend
                     color_discrete_sequence=['#4CAF50'],  # Choose color scale (optional)
                     width=600, height=400)
        
        # Update the layout to adjust axis and labels
        fig.update_layout(
            xaxis_title='<b>Total Spend ($)</b>',
            yaxis_title='<b>Supplier Name</b>',
            xaxis_tickangle=-45,
            xaxis_title_font=dict(family="Arial", size=14, color="Black", weight="bold"),
            yaxis_title_font=dict(family="Arial", size=14, color="Black", weight="bold"),
        )

        # Display the bar chart
        fig.update_layout(
            margin=dict(t=5, b=20),  # Reduce top and bottom margins for the chart
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error executing query: {e}")


def display_spend_by_category(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT DISTINCT b.LEVEL_1, b.LEVEL_2, SUM(a.INV_LINE_AMT_USD) AS SPEND_AMOUNT
    FROM ({base_query}) a
    LEFT JOIN {taxonomy_view} b ON b.LEVEL_4 = a.SPEND_CATEGORY
    WHERE a.INV_LINE_AMT_USD::string <> '' AND b.LEVEL_1 IS NOT NULL
    GROUP BY b.LEVEL_1, b.LEVEL_2
    ORDER BY b.LEVEL_1, b.LEVEL_2
    """
 
    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
 
        # Rename columns LEVEL_1 to Level1 and LEVEL_2 to Level2
        chart_data = chart_data.rename(columns={"LEVEL_1": "LEVEL 1", "LEVEL_2": "LEVEL 2"})
 
        # Format SPEND_AMOUNT as millions
        chart_data["SPEND_AMOUNT"] = chart_data["SPEND_AMOUNT"].apply(lambda x: round(x / 1_000_000, 2))
 
        # Persistent state to toggle views
        if "filter_view" not in st.session_state:
            st.session_state.filter_view = False  # Default to showing full table
 
        # Display the full table initially
        if not st.session_state.filter_view:
            # Create columns for heading and button
            col1, col2 = st.columns([2.8,1.4])  # Adjust column widths as needed
           
            with col1:
                # st.markdown("#### Full Table: Spend by Category")
                st.subheader("Spend by Category",
                help="This table shows the total spend amount (in millions) for each category. You can view the complete breakdown across all levels and categories."
                )
 
            with col2:
                # Add a button beside the heading
                # st.markdown(
                #     """
                #     <style>
                #     .stButton > button {
                #         margin-left: -20px; /* Adjust left margin */
                #         margin-right: 0; 
                #         width: 250px;       /* Adjust button width */
                #         text-align: center; /* Center the text */
                #     }
                #     </style>
                #     """,
                #     unsafe_allow_html=True,
                # )
                
               
                if st.button("Filter by Category",use_container_width=True):
                    st.session_state.filter_view = True  # Switch to filtered view
                    st.experimental_rerun()  # Force rerun to apply the state change
 
            st.markdown('<div style="margin-bottom: 22px;"></div>', unsafe_allow_html=True)
            chart_data = chart_data.rename(columns={"SPEND_AMOUNT": "TOTAL SPEND AMOUNT (M)"})
            st.dataframe(chart_data, width=595, height=298, use_container_width=True)
 
        # Display the filtered view
        else:
            # Create columns for heading and button
            col1, col2 = st.columns([2.8, 1.4])  # Adjust column widths as needed
           
            with col1:
                # st.markdown("#### Filtered View: Spend by Category")
                st.subheader("Spend by Category",
                help="This view allows you to filter spend by the selected Level 1 category. It provides a more focused analysis of spend distribution across subcategories."
                )
            with col2:
                # Add a button beside the heading
                # st.markdown(
                #     """
                #     <style>
                #     .stButton > button {
                #         margin-left: -20px; /* Adjust left margin */
                #         margin-right: 0; 
                #         width: 250px;       /* Adjust button width */
                #         text-align: center; /* Center the text */
                #     }
                #     </style>
                #     """,
                #     unsafe_allow_html=True,
                # )
                
                if st.button("Show All",use_container_width=True):
                    st.session_state.filter_view = False  # Switch back to full table view
                    st.experimental_rerun()  # Force rerun to apply the state change
 
            # Get unique Level1 categories
            level_1_categories = chart_data["LEVEL 1"].unique()
 
            # Dropdown for Level1 selection
            selected_level_1 = st.selectbox("Level 1 Category", options=["All"] + list(level_1_categories))
 
            if selected_level_1 == "All":
                # Display total spend grouped by Level1
                grouped_data = (
                    chart_data.groupby("LEVEL 1", as_index=False)
                    .agg({"SPEND_AMOUNT": "sum"})
                    .rename(columns={"SPEND_AMOUNT": "TOTAL SPEND AMOUNT (M)"})
                )
                st.dataframe(grouped_data, width=595, height=260, use_container_width=True)
            else:
                # Filter data for the selected Level1 category
                filtered_data = chart_data[chart_data["LEVEL 1"] == selected_level_1]
 
                # Handle case where filtered data is empty
                if filtered_data.empty:
                    st.warning("No data available for the selected Level 1 category.")
                else:
                    # Group by Level2 and calculate spend
                    grouped_data = (
                        filtered_data.groupby("LEVEL 2", as_index=False)
                        .agg({"SPEND_AMOUNT": "sum"})
                        .rename(columns={"SPEND_AMOUNT": "TOTAL SPEND AMOUNT (M)"})
                    )
 
                    grouped_data.loc["Total"] = grouped_data[["TOTAL SPEND AMOUNT (M)"]].sum(numeric_only=True)
                    grouped_data.at["Total", "LEVEL 2"] = "Total"
 
                    # Display the grouped data
                    st.dataframe(grouped_data, width=595, height=260, use_container_width=True)
 
    except Exception as e:
        st.error(f"Error executing query: {e}")
        
        
        
        
        
        
def display_spend_by_category_diversity(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT DISTINCT b.LEVEL_1, b.LEVEL_2, a.SUPPLIER_DIV_SUBTYPE, SUM(a.INV_LINE_AMT_USD) AS SPEND_AMOUNT
    FROM ({base_query}) a
    LEFT JOIN {taxonomy_view} b ON b.LEVEL_4 = a.SPEND_CATEGORY
    WHERE a.INV_LINE_AMT_USD::string <> '' AND b.LEVEL_1 IS NOT NULL
    GROUP BY b.LEVEL_1, b.LEVEL_2, a.SUPPLIER_DIV_SUBTYPE
    """
 
    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
 
        # Format the SPEND_AMOUNT as a numeric value in millions
        chart_data["SPEND_AMOUNT"] = chart_data["SPEND_AMOUNT"].astype(float) / 1_000_000
        chart_data["SPEND_AMOUNT"] = chart_data["SPEND_AMOUNT"].round(3)
 
        # Persistent state to toggle views
        if "filter_view" not in st.session_state:
            st.session_state.filter_view = False  # Default to showing full table
 
        # Display the full table initially
        if not st.session_state.filter_view:
            # Create columns for heading and button
            col1, col2 = st.columns([2.3, 1.4])  # Adjust column widths as needed
 
            with col1:
                st.subheader(
    "Spend by Category",
    help="This table shows the total spend (in millions) by category, with breakdowns by Level 1, Level 2, and Supplier Diversity Subtype. You can toggle to filter the data based on different category levels."
)
            with col2:
                # Add a button beside the heading
                if st.button("Filter by Category ",use_container_width=True):
                    st.session_state.filter_view = True  # Switch to filtered view
                    st.experimental_rerun()  # Force rerun to apply the state change
 
            st.markdown('<div style="margin-bottom: 25px;"></div>', unsafe_allow_html=True)
            chart_data = chart_data.rename(columns={"SPEND_AMOUNT": "TOTAL SPEND AMOUNT (M)"})
            st.dataframe(chart_data, width=800, height=260,use_container_width=True)
 
        # Display the filtered view
        else:
            # Create columns for heading and button
            col1, col2 = st.columns([2.3, 1.4])  # Adjust column widths as needed
 
            with col1:
                st.subheader(
    "Spend by Category",
    help="This filtered view allows you to narrow down the spend data by specific Level 1 and Level 2 categories, and supplier diversity subtypes. You can view total spend for each category or dive deeper into subcategory details."
)
            with col2:
                # Add a button beside the heading
                if st.button("Show All",use_container_width=True):
                    st.session_state.filter_view = False  # Switch back to full table view
                    st.experimental_rerun()  # Force rerun to apply the state change
 
            # Get unique Level 1 categories
            level_1_categories = chart_data["LEVEL_1"].unique()
 
            # Create columns for Level 1 and Level 2 dropdowns
            col3, col4 = st.columns(2)
 
            # Dropdown for Level 1 selection
            with col3:
                selected_level_1 = st.selectbox("Level 1 Category", options=["All"] + list(level_1_categories))
 
            if selected_level_1 == "All":
                # Display total spend grouped by Level 1
                grouped_data = (
                    chart_data.groupby("LEVEL_1", as_index=False)
                    .agg({"SPEND_AMOUNT": "sum"})
                    .rename(columns={"SPEND_AMOUNT": "TOTAL SPEND AMOUNT (M)"})
                )
                st.dataframe(grouped_data, use_container_width=True, width=800, height=195)
            else:
                # Filter data for the selected Level 1 category
                filtered_data = chart_data[chart_data["LEVEL_1"] == selected_level_1]
 
                # Get unique Level 2 categories
                level_2_categories = filtered_data["LEVEL_2"].unique()
 
                # Dropdown for Level 2 selection
                with col4:
                    selected_level_2 = st.selectbox("Level 2 Category", options=["All"] + list(level_2_categories))
 
                if selected_level_2 == "All":
                    # Display total spend grouped by Level 2
                    grouped_data = (
                        filtered_data.groupby("LEVEL_2", as_index=False)
                        .agg({"SPEND_AMOUNT": "sum"})
                        .rename(columns={"SPEND_AMOUNT": "TOTAL SPEND AMOUNT (M)", "LEVEL_2": "LEVEL 2"})
                    )
                else:
                    # Further filter data for the selected Level 2 category
                    filtered_data = filtered_data[filtered_data["LEVEL_2"] == selected_level_2]
 
                    # Group by SUPPLIER_DIV_SUBTYPE and calculate spend
                    grouped_data = (
                        filtered_data.groupby("SUPPLIER_DIV_SUBTYPE", as_index=False)
                        .agg({"SPEND_AMOUNT": "sum"})
                        .rename(columns={"SPEND_AMOUNT": "TOTAL SPEND AMOUNT (M)", "SUPPLIER_DIV_SUBTYPE": "SUPPLIER DIV SUBTYPE"})
                    )
 
                # Add a total row
                total_spend = grouped_data["TOTAL SPEND AMOUNT (M)"].sum()
                grouped_data.loc[len(grouped_data)] = ["Total", total_spend]
 
                # Display the filtered table
                st.dataframe(grouped_data, use_container_width=True, width=800, height=195)
 
    except Exception as e:
        st.error(f"Error executing query: {e}")
 
    

def plot_dynamic_bar_graph(selected_metric,filters):
    # Base query with filters applied
    base_query = build_query(filters)
    query = f"""
    SELECT {selected_metric}, SUM(INV_LINE_AMT_USD) AS total_spend
    FROM ({base_query})
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    """
   
    # Add filters (example with SUPPLIER_NAME filter)
    if 'SUPPLIER_NAME' in st.session_state.filters:
        query += f" AND SUPPLIER_NAME IN ({', '.join([repr(name) for name in st.session_state.filters['SUPPLIER_NAME']])})"
   
    # Complete the query with GROUP BY and ORDER BY clauses
    query += f" GROUP BY {selected_metric} ORDER BY total_spend DESC LIMIT 10"
 
    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
 
        # Check if chart_data is empty
        if chart_data.empty:
            st.warning("No data available for the selected filters.")
            return
       
        # Ensure proper casing for column names
        chart_data.columns = chart_data.columns.str.upper()
 
        # Convert the total spend to billions (assuming USD)
        chart_data['TOTAL_SPEND'] = chart_data['TOTAL_SPEND'] / 1e9  # Convert to billions
 
        # Plotting the bar graph
        fig = px.bar(chart_data, x='TOTAL_SPEND', y=selected_metric.upper(),
                     labels={selected_metric.upper(): selected_metric, 'TOTAL_SPEND': 'Total Spend (in Billion $)'},
                     text='TOTAL_SPEND',width = 998)
        fig.update_traces(texttemplate='$%{text:.4f}B', textposition='outside')
 
        # Custom layout for the figure (setting fixed height)
        fig.update_layout(
            height=400,  # Height of the graph itself
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(
                tickmode='linear',
                title=dict(
                    text=f"<b>{selected_metric}</b>",
                    font=dict(family="Arial", size=15, color="black")
                ),
                tickfont=dict(family="Arial", size=12, color="black")
            ),
            xaxis=dict(
                title=dict(
                text="<b>Total Spend (in Billion $)</b>",
                font=dict(family="Arial", size=15, color="black")
                ),
                tickfont=dict(family="Arial", size=12, color="black")
            )
       
        )
 
       
 
        # Display the graph in the container
        st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False)  # Ensure width is managed properly
        st.markdown('</div>', unsafe_allow_html=True)
 
    except Exception as e:
        st.error(f"Error executing query: {e}")

def display_spend_per_lob_region(filters):
    # Build base query
    base_query = build_query(filters)
    
    # SQL query to get total spend by LOB and Region
    query = f"""
    SELECT LINE_OF_BUSINESS, GLOBAL_REGION, SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    GROUP BY LINE_OF_BUSINESS, GLOBAL_REGION
    ORDER BY LINE_OF_BUSINESS, GLOBAL_REGION
    """
    
    # Debug: Print the generated SQL query
    #st.write("Executing Query for Spend per LOB and Region:", query)
    
    try:
        spend_per_lob_region_df = get_session().sql(query).toPandas()
        
        spend_per_lob_region_df.rename(
            columns={"LINE_OF_BUSINESS": "LINE OF BUSINESS", "GLOBAL_REGION": "GLOBALREGION"}, 
            inplace=True
        )

        # Create a pivot table
        pivot_table = spend_per_lob_region_df.pivot_table(
            index='LINE OF BUSINESS', 
            columns='GLOBALREGION', 
            values='TOTAL_SPEND', 
            fill_value=0  # Fill missing values with 0
        )

        # Add a total row
        pivot_table.loc['Total'] = pivot_table.sum()

        # Display the pivot table
        # st.markdown("#### Spend per LOB and Region")
        # st.markdown("<div style='margin-bottom: 64px;'></div>", unsafe_allow_html=True)
        st.dataframe(pivot_table,use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")


def plot_spend_by_lob(filters):
    # Build query for spending by month
    base_query = build_query(filters)
    query = f"""
    SELECT LINE_OF_BUSINESS, SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    GROUP BY LINE_OF_BUSINESS order by SUM(INV_LINE_AMT_USD) desc
    """

    try:
        # Execute the query and convert results to a DataFrame
        spend_by_lob_df = get_session().sql(query).toPandas()

        # Create a bar graph with custom colors
        fig = px.bar(
            spend_by_lob_df, 
            x='LINE_OF_BUSINESS', 
            y='TOTAL_SPEND', 
            # title='Total Spend by LOB',
            # color_discrete_sequence=['#FDFD96']  # Change to your desired color
        )

        # Customize the layout for bold axis labels
        fig.update_layout(
            xaxis_title=dict(text='Line of Business', font=dict(size=14, color='black', family='Arial', weight="bold")),
            yaxis_title=dict(text='Total Spend (USD)', font=dict(size=14, color='black', family='Arial', weight="bold")),
            # title=dict(font=dict(size=18, weight="bold"))
        )
        # st.markdown("#### Total Spend by LOB")
        # Render the bar graph in Streamlit
        # st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        fig.update_layout(
            margin=dict(t=10, b=20),  # Reduce top and bottom margins for the chart
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error executing query: {e}")


def plot_spend_by_region(filters):
    # Build query for spending by month
    base_query = build_query(filters)
    query = f"""
    SELECT GLOBAL_REGION as REGION, SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> ''
    GROUP BY GLOBAL_REGION order by SUM(INV_LINE_AMT_USD) desc
    """

    # Debug: Print the generated SQL query
    # st.write("Executing Query for Spend by Month:", query)
    
    try:
        spend_by_region_df = get_session().sql(query).toPandas()
        
               

        # Sort the DataFrame by SPEND_MONTH
        #spend_by_lob_df.sort_values('LINE_OF_BUSINESS', inplace=True)

        # Create a bar graph
        fig = px.bar(spend_by_region_df, x='REGION', y='TOTAL_SPEND')

        fig.update_layout(
            xaxis_title=dict(text='Region', font=dict(size=14, color='black', family='Arial', weight = "bold")),
            yaxis_title=dict(text='Total Spend (USD)', font=dict(size=14, color='black', family='Arial', weight="bold")),
            # title=dict(font=dict(size=18, weight="bold"))
        )
        
        # st.markdown("#### Total Spend By Region")
        # Render the bar graph
        # st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        fig.update_layout(
            margin=dict(t=10, b=20),  # Reduce top and bottom margins for the chart
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error executing query: {e}")

#display strategic category vs spend
import plotly.graph_objects as go


def display_spend_by_strategic_category(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT CBRE_L4 as Strategic_Category , SUM(INV_LINE_AMT_USD) as SPEND_AMOUNT from ({base_query}) GROUP BY 
    CBRE_L4 
    """

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
        
        chart_data = chart_data.rename(columns={"Strategic_Category": "STRATEGIC CATEGORY", "SPEND_AMOUNT": "SPEND AMOUNT(M)"})

        # Format the SPEND_AMOUNT column
        chart_data["SPEND AMOUNT(M)"] = chart_data["SPEND AMOUNT(M)"].apply(lambda x: round(x / 1_000_000, 2))
        
        chart_data = chart_data.reset_index(drop=True)

        
        # Display the table using Plotly
        # st.markdown("#### Strategic Categories")
        # st.markdown("<div style='margin-bottom: 27px;'></div>", unsafe_allow_html=True)
        st.dataframe(chart_data,use_container_width=False, width=800, height=280)
        

    except Exception as e:
        st.error(f"Error executing query: {e}")





def plot_spend_by_supplier_classification(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_CLASSIFICATION , SUM(INV_LINE_AMT_USD) as SPEND_AMOUNT, COUNT(DISTINCT UPPER(SUPPLIER_NAME)) as SUPPLIER_COUNT
    from ({base_query})
    GROUP BY SUPPLIER_CLASSIFICATION
    """
 
    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
 
        # Calculate the totals for Spend Amount and Supplier Count
        total_spend = chart_data['SPEND_AMOUNT'].sum()
        total_suppliers = chart_data['SUPPLIER_COUNT'].sum()
 
        # Group the data to create two categories: 'Strategic' and 'Others'
        qualified_spend = chart_data[chart_data['SUPPLIER_CLASSIFICATION'] == 'Qualified']['SPEND_AMOUNT'].sum()
        others_spend = chart_data[chart_data['SUPPLIER_CLASSIFICATION'] != 'Qualified']['SPEND_AMOUNT'].sum()
 
        # Format the SPEND_AMOUNT column
        chart_data["SPEND_AMOUNT"] = chart_data["SPEND_AMOUNT"].apply(lambda x: f"${x:,.2f}M")
        chart_data = chart_data.reset_index(drop=True)
 
        # Display the DataFrame
        # st.markdown("Spend Per Classification")
        
 
        # Create a new DataFrame for donut chart
        pie_data = pd.DataFrame({
            'Category': ['Qualified', 'S&P'],
            'SPEND_AMOUNT': [qualified_spend, others_spend]
        })
 
        # Create a donut chart using Plotly with custom colors
        fig = px.pie(pie_data, values='SPEND_AMOUNT', names='Category',
                     labels={'SPEND_AMOUNT': 'Spend Amount'},
                    #  color='Category',  # Specify the 'Category' column for coloring
                    #  color_discrete_map={
                    #      'Qualified': '#00008B',  # Green for Qualified
                    #      'S&P': '#ADD8E6'  # Red for S&P
                    #  },
                     hole=0.4,  # This makes it a donut chart
                     width=300, height=300)
        # st.markdown("#### Spend Classification %", unsafe_allow_html=True)
        fig.update_layout(
            margin=dict(t=10, b=20),  # Reduce top and bottom margins for the chart
        )
 
        # Display the donut chart in Streamlit
        st.plotly_chart(fig)
 
    except Exception as e:
        st.error(f"Error executing query: {e}")


def display_spend_by_supplier_classification(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_CLASSIFICATION , SUM(INV_LINE_AMT_USD) as SPEND_AMOUNT,COUNT(DISTINCT UPPER(SUPPLIER_NAME)) as SUPPLIER_COUNT from ({base_query}) GROUP BY 
    SUPPLIER_CLASSIFICATION
    """

    # Debug: Print the SQL query
    #st.write("Executing Query for Spend by Category:", query)

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
        # Calculate the totals for Spend Amount and Supplier Count
        chart_data['SUPPLIER_CLASSIFICATION'] = chart_data['SUPPLIER_CLASSIFICATION'].fillna('Unclassified')
        total_spend = chart_data['SPEND_AMOUNT'].sum()
        total_suppliers = chart_data['SUPPLIER_COUNT'].sum()
        chart_data['SPEND_PERCENTAGE'] = (chart_data['SPEND_AMOUNT'] / total_spend) * 100
        chart_data['SUPPLIER_COUNT_PERCENTAGE'] = (chart_data['SUPPLIER_COUNT'] / total_suppliers) * 100
        chart_data['SPEND_PERCENTAGE'] = chart_data['SPEND_PERCENTAGE'].map('{:.2f}%'.format)
        chart_data['SUPPLIER_COUNT_PERCENTAGE'] = chart_data['SUPPLIER_COUNT_PERCENTAGE'].map('{:.2f}%'.format)
        # Format the SPEND_AMOUNT column
        chart_data["SPEND_AMOUNT"] = chart_data["SPEND_AMOUNT"].apply(lambda x: round(x / 1_000_000, 2))
        chart_data = chart_data[
            ['SUPPLIER_CLASSIFICATION', 'SPEND_AMOUNT', 'SPEND_PERCENTAGE', 
             'SUPPLIER_COUNT', 'SUPPLIER_COUNT_PERCENTAGE']
        ]
        chart_data = chart_data.rename(columns={"SUPPLIER_CLASSIFICATION": "SUPPLIER CLASSIFICATION", "SPEND_AMOUNT": "SPEND AMOUNT(M)",
                                             "SPEND_PERCENTAGE":"SPEND %","SUPPLIER_COUNT":"SUPPLIER COUNT",
                                             "SUPPLIER_COUNT_PERCENTAGE":"SUPPLIER COUNT %"})
        chart_data = chart_data.reset_index(drop=True)
        # Display the DataFrame
        # st.markdown("#### Spend Analysis by Supplier Classification")
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        st.dataframe(chart_data)

    except Exception as e:
        st.error(f"Error executing query: {e}")








import plotly.express as px

def plot_dynamic_SP_bar_graph(selected_metric, filters):
    # Define a color mapping for each metric
    metric_color_mapping = {
        'Country': '#1f77b4',  # Blue
        'LINE_OF_BUSINESS': '#ff7f0e',          # Orange
        'GLOBAL_REGION': '#2ca02c',     # Green
        'CLIENT': '#d62728',  # Red
        'SOURCE_SYSTEM': '#f7b6d2', #pink
        'BUSINESS_SEGMENT': '#9467bd', # purple
        'SPEND_CATEGORY': '#17becf' #c cyan
        # Add more mappings for other metrics as needed
    }
    
    # Base query with filters applied
    base_query = build_query(filters)
    query = f"""
    SELECT {selected_metric}, SUM(INV_LINE_AMT_USD) AS total_spend
    FROM ({base_query})
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> '' and SUPPLIER_CLASSIFICATION!='Qualified' 
    """
    
    # Add filters (example with SUPPLIER_NAME filter)
    if 'SUPPLIER_NAME' in st.session_state.filters:
        query += f" AND SUPPLIER_NAME IN ({', '.join([repr(name) for name in st.session_state.filters['SUPPLIER_NAME']])})"
    
    # Complete the query with GROUP BY and ORDER BY clauses
    query += f" GROUP BY {selected_metric} ORDER BY total_spend DESC LIMIT 10"

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()

        # Check if chart_data is empty
        if chart_data.empty:
            st.warning("No data available for the selected filters.")
            return
        
        # Ensure proper casing for column names
        chart_data.columns = chart_data.columns.str.upper()

        # Convert the total spend to billions (assuming USD)
        chart_data['TOTAL_SPEND'] = chart_data['TOTAL_SPEND'] / 1e9  # Convert to billions

        # Get the color for the selected metric
        color = metric_color_mapping.get(selected_metric.upper())  # Default to blue if metric not found

        # Plotting the bar graph with the selected color
        fig = px.bar(chart_data, x='TOTAL_SPEND', y=selected_metric.upper(),
                     labels={selected_metric.upper(): selected_metric, 'TOTAL_SPEND': 'Total Spend (in Billion $)'},
                     text='TOTAL_SPEND',
                     color_discrete_sequence=[color])  # Use the color based on the selected metric

        fig.update_traces(texttemplate='$%{text:.5f}B', textposition='outside')

        # Custom layout for the figure (setting fixed height and width)
        fig.update_layout(
            height=300,  # Smaller height to fit alongside pie chart
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(
                title=f"<b>{selected_metric}</b>",
                title_font=dict(size=14, family='Arial', weight='bold',color='black'),
                tickfont=dict(size=12),
                tickmode='linear',
            ),
            xaxis=dict(
                title='<b>Total Spend (in Billion $)</b>',
                title_font=dict(size=14, family='Arial', weight='bold',color='black'),
                tickfont=dict(size=12)
            ),
            # Remove the legend by not including the legend definition
        )

        # Display the bar graph
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")


def plot_spend_per_supplier_classification_month(filters):
    # Base query to get Spend per Supplier Classification by Month
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_CLASSIFICATION, SPEND_MONTH, SUM(INV_LINE_AMT_USD) as SPEND_AMOUNT 
    FROM ({base_query}) 
    GROUP BY SUPPLIER_CLASSIFICATION, SPEND_MONTH
    """

    try:
        # Execute the query and fetch the data
        df = get_session().sql(query).toPandas()
        
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        
        df['SPEND_MONTH'] = pd.Categorical(df['SPEND_MONTH'], categories=month_order, ordered=True)

        # Add a Category column for grouping
        df['Category'] = df['SUPPLIER_CLASSIFICATION'].apply(lambda x: 'Qualified' if x == 'Qualified' else 'S&P')

        # Group data for plotting
        monthly_spend = df.groupby(['SPEND_MONTH', 'Category'])['SPEND_AMOUNT'].sum().reset_index()

        # Create the bar chart using Plotly Express
        fig = px.bar(
            monthly_spend,
            x='SPEND_MONTH',
            y='SPEND_AMOUNT',
            color='Category',  # Differentiate bars by category
            labels={
                'SPEND_MONTH': 'Month',
                'SPEND_AMOUNT': 'Spend Amount (USD)',
                'Category': 'Supplier Classification'
            },
            barmode='group',  # Group bars by classification
            text_auto=True,  # Display spend values on the bars
            # color_discrete_map={
            #     'Qualified': '#e9724d',  # Orange for 'Qualified'
            #     'S&P': '#d6d727'        # Blue for 'S&P'
            # }
        )

        # Customize layout and axes
        fig.update_layout(
            xaxis=dict(
                title='<b>Month</b>',
                title_font=dict(size=16, color='black', family='Arial'),
                title_font_weight='bold'
            ),
            yaxis=dict(
                title='<b>Spend Amount (USD)</b>',
                title_font=dict(size=16, color='black', family='Arial'),
                title_font_weight='bold'
            ),
            legend_title_text='Classification',
            legend=dict(font=dict(size=12), title_font=dict(size=14, family='Arial'))
        )

        # Display the bar chart in Streamlit
        # st.markdown("#### Monthly Spend: Qualified vs S&P")
        fig.update_layout(
            margin=dict(t=10, b=20),  # Reduce top and bottom margins for the chart
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")


def plot_supplier_classification_trend(filters):
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_CLASSIFICATION, SPEND_MONTH, UPPER(SUPPLIER_NAME) as SUPPLIER_NAME FROM ({base_query}) 
    """

    try:
        # Execute the query and fetch the data
        df = get_session().sql(query).toPandas()

        # Group the data by month and classification (Qualified vs S&P)
        df['Category'] = df['SUPPLIER_CLASSIFICATION'].apply(lambda x: 'Qualified' if x == 'Qualified' else 'S&P')

        # Count distinct suppliers per month and per category
        monthly_supplier_count = df.groupby(['SPEND_MONTH', 'Category'])['SUPPLIER_NAME'].nunique().unstack(fill_value=0).reset_index()

        # Ensure both 'Qualified' and 'S&P' columns exist in the DataFrame
        if 'Qualified' not in monthly_supplier_count.columns:
            monthly_supplier_count['Qualified'] = 0
        if 'S&P' not in monthly_supplier_count.columns:
            monthly_supplier_count['S&P'] = 0

        # Create a line chart using Plotly Express
        fig = px.line(
            monthly_supplier_count,
            x='SPEND_MONTH',
            y=['Qualified', 'S&P'],
            labels={
                'value': 'Supplier Count',
                'SPEND_MONTH': 'Month',
                'variable': 'Category'
            },
            markers=True,  # Add markers to the line chart
            # color_discrete_map={
            #     'Qualified': '#e9724d',  # Orange for 'Qualified'
            #     'S&P': '#d6d727'       # Blue for 'S&P'
            # }
        )

        # Customize layout, labels, and line styles
        fig.update_traces(line=dict(width=2), marker=dict(size=8))  # Thicker lines, larger markers
        fig.update_layout(
            xaxis=dict(
                title='<b>Month</b>',
                title_font=dict(size=16, color='black', family='Arial'),
                title_font_weight='bold',
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title='<b>Supplier Count</b>',
                title_font=dict(size=16, color='black', family='Arial'),
                title_font_weight='bold',
                tickfont=dict(size=12)
            ),
            legend_title=dict(
                text='Category',
                font=dict(size=14, family='Arial')
            ),
            legend=dict(font=dict(size=12)),
        )

        # Display the line chart in Streamlit
        # st.markdown("#### Supplier Count Trend: Qualified vs S&P")
        fig.update_layout(
            margin=dict(t=10, b=20),  # Reduce top and bottom margins for the chart
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")


def plot_spend_by_diversity_cert_type(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_DIV_CERT_TYPE, SUM(INV_LINE_AMT_USD) AS SPEND_AMOUNT, COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS SUPPLIER_COUNT 
    FROM ({base_query}) where SUPPLIER_DIV_CERT_TYPE is not null and SUPPLIER_DIV_CERT_TYPE <> ''
    GROUP BY SUPPLIER_DIV_CERT_TYPE
    """

    # Debug: Print the SQL query
    #st.write("Executing Query for Spend by Certification Type:", query)

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()

        # Debug: Print the DataFrame to ensure data is retrieved correctly
        #st.write("Retrieved Data:", chart_data)

        if chart_data.empty:
            st.warning("No data available for the selected filters.")
            return

        # Calculate the percentage spend for each certification type
        total_spend = chart_data['SPEND_AMOUNT'].sum()
        chart_data['SPEND_PERCENTAGE'] = (chart_data['SPEND_AMOUNT'] / total_spend) * 100

        # Create the pie chart using numerical values for SPEND_AMOUNT
        fig = px.pie(chart_data, values='SPEND_AMOUNT', names='SUPPLIER_DIV_CERT_TYPE',
                     labels={'SPEND_AMOUNT': 'Spend Amount'},
                     width=200,height=200)
        # st.markdown("#### Spend by Supplier Diversity Certification Type")
        
        fig.update_layout(
            margin=dict(t=5, b=5),  # Reduce top and bottom margins for the chart
        )
        # Display the pie chart in Streamlit
        st.plotly_chart(fig,use_container_width=True)

        # Format Spend Amount and Percentage for display in the DataFrame (after plotting)
        chart_data['SPEND_AMOUNT'] = chart_data['SPEND_AMOUNT'].apply(lambda x: f"${x:,.2f}")
        chart_data['SPEND_PERCENTAGE'] = chart_data['SPEND_PERCENTAGE'].apply(lambda x: f"{x:.2f}%")

        # Display the DataFrame
        
        #st.dataframe(chart_data, hide_index=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")

def display_spend_by_supplier_ethnicity(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT DISTINCT a.SUPPLIER_ETHNICITY, SUM(a.INV_LINE_AMT_USD) AS SPEND_AMOUNT, COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS SUPPLIER_COUNT 
    FROM ({base_query}) a 
    WHERE a.INV_LINE_AMT_USD::string <> '' and SUPPLIER_ETHNICITY <> '' 
    GROUP BY a.SUPPLIER_ETHNICITY
    """

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
        
        chart_data = chart_data.rename(columns={"SUPPLIER_ETHNICITY": "SUPPLIER ETHNICITY", "SPEND_AMOUNT": "SPEND AMOUNT",
                                                "SUPPLIER_COUNT":"SUPPLIER COUNT"})

        # Calculate total spend for percentage calculation
        total_spend = chart_data["SPEND AMOUNT"].sum()

        # Add a new column for % Spend
        chart_data["% Spend"] = (chart_data["SPEND AMOUNT"] / total_spend) * 100

        # Format the SPEND_AMOUNT and % Spend columns
        chart_data["SPEND AMOUNT"] = chart_data["SPEND AMOUNT"].apply(lambda x: round(x / 1_000_000, 2))
        chart_data["% Spend"] = chart_data["% Spend"].apply(lambda x: f"{x:.2f}%")

        # Reset index and display the DataFrame
        chart_data = chart_data.reset_index(drop=True)
        # st.markdown("#### Spend Analysis by Supplier Ethnicity")
        st.dataframe(chart_data)

    except Exception as e:
        st.error(f"Error executing query: {e}")


def display_spend_by_diversity_subtype(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT DISTINCT a.SUPPLIER_DIV_SUBTYPE, SUM(a.INV_LINE_AMT_USD) AS SPEND_AMOUNT, COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS SUPPLIER_COUNT 
    FROM ({base_query}) a 
    WHERE a.INV_LINE_AMT_USD::string <> ''  
    GROUP BY a.SUPPLIER_DIV_SUBTYPE
    """

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()
        
        chart_data["SUPPLIER_DIV_SUBTYPE"] = chart_data["SUPPLIER_DIV_SUBTYPE"].fillna("Not Specified")
        # Calculate total spend for percentage calculation
        total_spend = chart_data["SPEND_AMOUNT"].sum()

        # Add a new column for % Spend
        chart_data["% Spend"] = (chart_data["SPEND_AMOUNT"] / total_spend) * 100

        # Format the SPEND_AMOUNT and % Spend columns
        chart_data["SPEND_AMOUNT"] = chart_data["SPEND_AMOUNT"].apply(lambda x: round(x / 1_000_000, 2))
        chart_data["% Spend"] = chart_data["% Spend"].apply(lambda x: f"{x:.2f}%")

        # Reset index and display the DataFrame
        chart_data = chart_data.reset_index(drop=True)
        chart_data.rename(
            columns={
                "SUPPLIER_DIV_SUBTYPE": "Supplier Diversity Subtype",
                "SPEND_AMOUNT": "Spend (in Million USD)",
                "SUPPLIER_COUNT": "Number of Suppliers",
                "% Spend": "Percentage of Total Spend"
            },
            inplace=True
        )
        # st.markdown("#### Spend by Category")
        # st.markdown("#### Spend by Diversity Subtype")
        # st.markdown("<div style='margin-bottom: 64px;'></div>", unsafe_allow_html=True)
        st.dataframe(chart_data, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")


def plot_diverse_spend_by_supplier(filters):
    # SQL query to get Spend by Supplier Name for diverse spend
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_NAME, SUM(INV_LINE_AMT_USD) AS DIVERSE_SPEND 
    FROM ({base_query}) 
    WHERE SUPPLIER_DIV_CERT_TYPE IS NOT NULL
    GROUP BY SUPPLIER_NAME
    ORDER BY DIVERSE_SPEND DESC
    LIMIT 20  -- Show only top 20 suppliers for better visibility
    """

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()

        # Create a bar chart with an increased bar width
        fig = px.bar(
            chart_data, 
            x='DIVERSE_SPEND', 
            y='SUPPLIER_NAME', 
            orientation='h',
            
            labels={'DIVERSE_SPEND': 'Diverse Spend (USD)', 'SUPPLIER_NAME': 'Supplier Name'},
            color='DIVERSE_SPEND',
            # color_continuous_scale=px.colors.sequential.RdBu,
            width = 350
        )

        # Customize chart layout and bar size
        fig.update_layout(
            yaxis=dict(
                title='Supplier Name', 
                automargin=True,
                categoryorder='total ascending',
                ticksuffix='',
                autorange='reversed',
                title_font=dict(color='black', family='Arial', weight='bold') 
            ),
            xaxis=dict(
                title='Diverse Spend (USD)', 
                tickprefix="$",
                title_font=dict(color='black', family='Arial', weight='bold'),
                automargin=True
            ),
            height=500,
            margin=dict(l=200, r=20, t=50, b=20)
        )

        # Increase bar width
        fig.update_traces(marker=dict(line=dict(width=0.5)))
        
        # st.markdown("#### Top 20 Suppliers by Diverse Spend")
        fig.update_layout(
            margin=dict(t=5, b=20),  # Reduce top and bottom margins for the chart
        )
        # Display the bar chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")

def plot_spend_by_sust_rating(filters):
    # SQL query to get Spend by Category
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_SUST_RATING, SUM(INV_LINE_AMT_USD) AS SPEND_AMOUNT, COUNT(DISTINCT UPPER(SUPPLIER_NAME)) AS SUPPLIER_COUNT 
    FROM ({base_query}) where SUPPLIER_SUST_RATING is not null and SUPPLIER_SUST_RATING <> ''
    GROUP BY SUPPLIER_SUST_RATING
    """

    # Debug: Print the SQL query
    #st.write("Executing Query for Spend by Certification Type:", query)

    try:
        # Execute the query and fetch the data
        chart_data = get_session().sql(query).toPandas()

        # Debug: Print the DataFrame to ensure data is retrieved correctly
        #st.write("Retrieved Data:", chart_data)

        if chart_data.empty:
            st.warning("No data available for the selected filters.")
            return

        # Calculate the percentage spend for each certification type
        total_spend = chart_data['SPEND_AMOUNT'].sum()
        chart_data['SPEND_PERCENTAGE'] = (chart_data['SPEND_AMOUNT'] / total_spend) * 100
        
        # st.markdown(
        #         "<h4 style='margin-bottom: 0px;'>Spend Distribution by Supplier Sustainability Rating</h4>",
        #         unsafe_allow_html=True
        #     )

        # Create the pie chart using numerical values for SPEND_AMOUNT
        fig = px.pie(chart_data, values='SPEND_AMOUNT', names='SUPPLIER_SUST_RATING',
                    #  title='Spend Distribution by Supplier Sustainability Rating',
                     labels={'SPEND_AMOUNT': 'Spend Amount'},
                     width = 300,height = 300)

        # st.markdown("#### Spend Distribution by Supplier Sustainability Rating")
        # st.markdown("<div style='margin-bottom: 0px;'></div>", unsafe_allow_html=True)
        # Display the pie chart in Streamlit
        fig.update_layout(
            margin=dict(t=10, b=20),  # Reduce top and bottom margins for the chart
        )
        st.plotly_chart(fig,use_container_width=True)

        # Format Spend Amount and Percentage for display in the DataFrame (after plotting)
        chart_data['SPEND_AMOUNT'] = chart_data['SPEND_AMOUNT'].apply(lambda x: f"${x:,.2f}")
        chart_data['SPEND_PERCENTAGE'] = chart_data['SPEND_PERCENTAGE'].apply(lambda x: f"{x:.2f}%")

        # Display the DataFrame
        
        #st.dataframe(chart_data, hide_index=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")

def plot_sustainable_suppliers_spend(filters):
    # Build query for top suppliers
    base_query = build_query(filters)
    query = f"""
    SELECT SUPPLIER_NAME, SUM(INV_LINE_AMT_USD) AS TOTAL_SPEND 
    FROM ({base_query}) AS subquery
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> '' and SUPPLIER_SUST_OVERALL_SCORE >=60
    GROUP BY SUPPLIER_NAME 
    ORDER BY TOTAL_SPEND DESC LIMIT 10
    
    """

    # Debug: Print the generated SQL query
    #st.write("Executing Query for Top Suppliers:", query)
    
    try:
        top_suppliers_df = get_session().sql(query).toPandas()
        #st.subheader("Top 10 Suppliers by Spend")
        # fig = px.bar(top_suppliers_df, x='TOTAL_SPEND', y='SUPPLIER_NAME', labels={'TOTAL_SPEND': 'Total Spend ($)', 'SUPPLIER_NAME': 'Supplier Name'})
        fig = px.bar(
            top_suppliers_df,
            x='TOTAL_SPEND',
            y='SUPPLIER_NAME',
            labels={'TOTAL_SPEND': 'Total Spend ($)', 'SUPPLIER_NAME': 'Supplier Name'}
        )

        
        

  

        
        fig.update_layout(
            margin=dict(t=5, b=20),  # Reduce top and bottom margins for the chart
        )
        st.plotly_chart(fig, use_container_width=True)
       # st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error executing query: {e}")



def display_dynamic_Sustainable_table(selected_metric, filters):
    # Base query with filters applied
    base_query = build_query(filters)
    query = f"""
    SELECT {selected_metric}, SUM(INV_LINE_AMT_USD) AS total_spend, COUNT(DISTINCT SUPPLIER_NAME) AS supplier_count
    FROM ({base_query})
    WHERE INV_LINE_AMT_USD IS NOT NULL AND INV_LINE_AMT_USD::string <> '' AND SUPPLIER_SUST_OVERALL_SCORE >= 60
    """
    
    # Add filters (example with SUPPLIER_NAME filter)
    if 'SUPPLIER_NAME' in st.session_state.filters:
        query += f" AND SUPPLIER_NAME IN ({', '.join([repr(name) for name in st.session_state.filters['SUPPLIER_NAME']])})"
    
    # Complete the query with GROUP BY and ORDER BY clauses
    query += f" GROUP BY {selected_metric} ,client ORDER BY total_spend DESC LIMIT 10"

    try:
        # Execute the query and fetch the data
        table_data = get_session().sql(query).toPandas()
        
        
        # Check if table_data is empty
        if table_data.empty:
            st.warning("No data available for the selected filters.")
            return

        # Ensure proper casing for column names
        
        table_data.columns = table_data.columns.str.replace('_', ' ').str.title()
        table_data.columns = table_data.columns.str.upper()
        total_spend_value = table_data['TOTAL SPEND'].values[0] if not table_data.empty else 0

        table_data['% SPEND'] = (table_data['TOTAL SPEND'] / total_spend_value) * 100

        # Convert the total spend to billions for display
        table_data['TOTAL SPEND'] = table_data['TOTAL SPEND'] / 1e9  # Convert to billions

        # st.markdown("<div style='margin-bottom: 0px;'></div>", unsafe_allow_html=True)

        # Display the table
        st.dataframe(table_data,use_container_width=True)  # You can also use st.table for a static table without scrollbars

    except Exception as e:
        st.error(f"Error executing query: {e}")



