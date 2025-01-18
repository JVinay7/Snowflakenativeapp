import streamlit as st
from skimage import io
import plotly.express as px
import os
import base64
import plotly.graph_objects as go

def triggerEngine():
    with st.spinner("Executing Engine..."):
        # dao.run_calculate_measures()
        st.success("Engine Triggered Succesfully")


def Header(
        show_rerun_engine=False
        
        
):
    def image_png(file,img_width=500, img_height=80):
        fully_qualified = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(fully_qualified, "rb") as f:
            png_data = f.read()
    
        png = "data:image/png;base64," + base64.b64encode(png_data).decode("utf-8")
    
        fig = go.Figure()
    
        scale_factor=1
        fig.add_trace(
            go.Scatter(
                x=[0, img_width * scale_factor],
                y=[0, img_height * scale_factor],
                mode="markers",
                marker_opacity=0
            )
        )
    
        # Configure axes
        fig.update_xaxes(
            visible=False,
            range=[0, img_width * scale_factor],
            fixedrange = True
        )
    
        fig.update_yaxes(
            visible=False,
            range=[0, img_height * scale_factor],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor="x",
            fixedrange = True
        )
    
        # Add image
        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=img_height * scale_factor,
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="above",
                sizing="stretch",
                source=png)
        )
    
        # Configure other layout
        fig.update_layout(
            width=img_width *scale_factor,
            height=img_height *scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )
        st.plotly_chart(fig,config={"displayModeBar": False})
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
