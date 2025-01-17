import os
import base64
import plotly.graph_objects as go
import streamlit as st
import urllib.parse
from pandas import DataFrame
from datetime import timedelta, datetime
from snowflake.connector import SnowflakeConnection
# from config import is_running_externally
 
# def request_permissions(permissions = ["EXECUTE TASK", "CREATE WAREHOUSE"]):
#     if is_running_externally == False:
#         import snowflake.permissions as permission
#         privileges_missing = permission.get_missing_account_privileges(
#             permissions
#         )
#         if len(privileges_missing) > 0:
#             permission.request_account_privileges(privileges_missing)
#             raise Exception("Please provide required Execution Privilleges before proceeding...")
 
def add_to_list_if_session_state_not_present(list, key):
    value = st.session_state.get(key,None)
    if (value is None or len(str(value).strip()) == 0) and len(list) != 0:
        st.session_state[key] = list[0]
        return list 
    
    if  value not in list:
        list.append(value)
    return list
 
def add_to_list_if_session_state_list_not_present(list, key):
    values  = st.session_state.get(key,[])
    for value in values:
        if  value not in list:
            list.append(value)
    return list
 
def get_date_display_string_from_datetime(datetime:datetime):
    return datetime.strftime("%Y-%m-%d")
 
def download_pandas_df_as_csv(df, name):
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
                #converting the sample dataframe
    csv = convert_df(df)
                #adding a download button to download csv file
    st.download_button( 
        label="Export",
        data=csv,
        file_name=f'{name}.csv',
        mime='text/csv',
        use_container_width=True
    )
 
 
def download_yaml(file_name: str, conn: SnowflakeConnection) -> str:
    """util to download a semantic YAML from a stage."""
    import os
    import tempfile
 
    with tempfile.TemporaryDirectory() as temp_dir:
        # Downloads the YAML to {temp_dir}/{file_name}.
        download_yaml_sql = f"GET {file_name} file://{temp_dir}"
        conn.cursor().execute(download_yaml_sql)
 
        tmp_file_path = os.path.join(temp_dir, f"{file_name}")
        with open(tmp_file_path, "r") as temp_file:
            # Read the raw contents from {temp_dir}/{file_name} and return it as a string.
            yaml_str = temp_file.read()
            return yaml_str
 
 
def add_vertical_space(lines=1):
    for _ in range(lines):
        st.write(" ")
 
# Show a streamlit image without using st.image (since it is disabled)
# Uses plotly and writes a png to the background.
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
 
 
    
def image_svg(file,img_width=200, img_height=60):
    fully_qualified = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(fully_qualified, "r") as f:
        svg_image = urllib.parse.quote(f.read())
 
    png = "data:image/svg+xml;charset=utf-8," + svg_image
 
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
    
 
def getDisplayDateStringFromString(date_str):
    return date_str
 
 
supported_colors = ['blue', 'green', 'orange', 'red', 'violet', 'gray', 'rainbow']
 
 
def ContainerTable(
    df:DataFrame,
    columnDetails:list,
    render_expanded=None,
    key="None",
    hide_expand_icon=False
    
):
    
    def get_key(name):
        return f"{key}_{name}"
    
    expanded_index_key_state_name = get_key('expanded_index')
    
    def on_toggle_expand(index):
        if st.session_state.get(expanded_index_key_state_name) == index:
            st.session_state[expanded_index_key_state_name] = None
        else:
            st.session_state[expanded_index_key_state_name] = index
    
    container_widths = [1,16]
    container = st.container()
    if render_expanded != None and hide_expand_icon == False:
        _, container = st.columns(container_widths)
        
    column_widths = [ item.get("width",1) for item in columnDetails]
 
    header_columns = container.columns(column_widths)
 
    for hc, detail in zip(header_columns, columnDetails):
        if detail.get('name','') == '':
            hc.write(" ")
        else:
            hc.caption(f"**{detail.get('name','')}**")
 
    for index, row in df.iterrows():
        main_container = st.container()
        if render_expanded != None and hide_expand_icon == False:
            expand_button, main_container = st.columns(container_widths)
            expand_button_text = "🔼" if st.session_state.get(expanded_index_key_state_name,None) == index else "🔽"
            expand_button.button(
                expand_button_text, 
                on_click=on_toggle_expand, 
                args=(index,),
                key=get_key(f"expand_button_{index}")
            )
            
        data_columns = main_container.columns(column_widths)
        for column_index, (dc, detail) in enumerate(zip(data_columns, columnDetails)):
            render_row(detail, index, row, column_index, dc,get_key,on_toggle_expand,expanded_index_key_state_name)
            
        with main_container.container():
            expanded_index_key_state_name = get_key('expanded_index')
            if render_expanded != None and st.session_state.get(expanded_index_key_state_name,None) == index:
                render_expanded(index, row)
 
def render_row(detail, index, row, column_index, dc,get_key,on_toggle_expand,expanded_index_key_state_name):
    text = ''
    if detail['key'] == 'index':
        text = index+1
    else:
        text = row[detail['key']]
                
    if detail.get('mapper',None) is not None:
        text = detail.get('mapper')(text)
                
    if(detail.get('type','') == 'link'):
        link_text = detail.get("link_text","link")
        dc.write(f"[{link_text}]({text})")
    elif detail.get('type','') == 'timestamp':
        date_string = getDisplayDateStringFromString(text)
        color = detail.get('color','')
        if color in supported_colors:
            dc.caption(f"**:{color}[{date_string}]**")
        else:
            dc.text(date_string)
    elif detail.get('type','') == 'button':
        if detail.get('toggle_expand',None) is not None:
            dc.button(
                    detail.get('label_expanded',None) if st.session_state.get(expanded_index_key_state_name,None) == index else detail.get('label','') , 
                    on_click=on_toggle_expand,
                    args=(index),
                    key=get_key(f"{row[detail['key']]}_{index}_{column_index}")
                )
        else:
            dc.button(
                    detail.get('label',''), 
                    on_click=detail.get("on_click",None),
                    args=(row[detail['key']],row),
                    key=get_key(f"{row[detail['key']]}_{index}_{column_index}")
                )
    elif detail.get('type','') == 'code':
         dc.code(text)
    elif detail.get('type','') =='write':
        dc.write(text)
    elif detail.get('type','') == 'custom':
        with dc.container():
            if detail.get('render',None) != None:
                detail.get('render')(index, row, detail.get('key',""))
                 
    else:
        color = detail.get('color','')
        if color in supported_colors:
            dc.write(f"**:{color}[{text}]**")
        else:
            dc.text(text)