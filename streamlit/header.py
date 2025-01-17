import streamlit as st
from skimage import io
import plotly.express as px
from util import *
# from utils import run_engine


def triggerEngine():
    with st.spinner("Executing Engine..."):
        # dao.run_calculate_measures()
        st.success("Engine Triggered Succesfully")


def Header(
        show_rerun_engine=False
        
        
):
    
    image_png("./SupplierSpendAnalytics.png")
    # logo_path = "SupplierSpendAnalytics.png"
    # st.image(logo_path, width=100) 
    # # Load the SVG file content
    # with open(logo_path, 'r') as file:
    #     svg_code = file.read()

    # # Display the SVG with inline CSS styling
    # st.markdown(
    #     f"<div style='width: 100px; height: 100px;'>{svg_code}</div>", 
    #     unsafe_allow_html=True
    # )    # if show_rerun_engine:
    # col2.button("Run Engine", use_container_width=True, on_click=run_engine, args=("INSIGHTS",))


# col12.markdown("last run")

# cs2.button("Rerun", on_click=triggerEngine)
# if (status.size > 0):
#     last_run_time = pd.to_datetime(status['RUN_START'][0])
#     last_run_time = last_run_time.strftime("%b %d %Y %H:%M:%S")
#     c2.caption(f"Last Run : **{last_run_time}**")
    st.divider()
    st.info(f"""
This is a trial version to demonstrate the data features and functionality using placeholder data. For customization and to meet your specific requirements, please contact our support team at *appsupport@anblicks.com*
""")
    st.divider()
