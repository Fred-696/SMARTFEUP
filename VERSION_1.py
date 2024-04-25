import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout = "wide", initial_sidebar_state = "collapsed")

# #Hide Deploy Button
# st.markdown(
#     r"""
#     <style>
#     .stDeployButton {
#             visibility: hidden;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )

# #Hide "Stop" and "Running"
# st.markdown(
#     r"""
#     <style>
#     [data-testid="stStatusWidget"] {
#             visibility: hidden;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )

# #DELETE BLACK SPACES
# st.markdown("""
#     <style>
    
#            /* Remove blank space at top and bottom */ 
#            .block-container {
#                padding-top: 3.75rem;                                     
#                padding-bottom: 0rem;
#             }
           
#            /* Remove blank space at the center canvas */ 
#            .st-emotion-cache-z5fcl4 {
#                position: relative;
#                top: -62px;
#                }
           
#            /* Make the toolbar transparent and the content below it clickable */ 
#            .st-emotion-cache-18ni7ap {
#                pointer-events: none;
#                background: rgba(255, 255, 255, 0); /* Transparent background */
#                }
#            .st-emotion-cache-zq5wmm {
#                pointer-events: auto;
#                background: rgba(255, 255, 255, 0); /* Transparent background */
#                border-radius: 5px;
#                }
#     </style>
#     """, unsafe_allow_html=True)


st.sidebar.image("LOGO_1.png", use_column_width = True)

st.sidebar.divider()

st.sidebar.header("PROJECT `version 1`")

st.sidebar.caption("""*SmartFEUP is an innovative environmental monitoring system designed 
                    to provide real-time insights into key environmental variables. Our project 
                    focuses on monitoring wind speed and direction, particulate matter (dust) 
                    levels, solar exposure, and noise levels, offering users a comprehensive 
                    understanding of their surrounding environment. By deploying a network of 
                    sensors and leveraging advanced data processing algorithms, SmartFEUP delivers 
                    accurate and reliable data to users through an intuitive user interface. Whether 
                    you're a researcher, environmental enthusiast, or simply curious about your 
                    surroundings, SmartFEUP empowers you to make informed decisions and take proactive 
                    measures to promote a healthier and more sustainable environment""")

st.sidebar.divider()

st.sidebar.markdown("Created by ***Team F***")
##################################################################################################

# Initialize the location data and colors
if 'DCUs' not in st.session_state:
        print("Database reloaded")
        st.session_state.DCUs = pd.DataFrame({
            "LATITUDE": [41.17760, 41.17781, 41.17632, 41.17818],
            "LONGITUDE": [-8.59466, -8.59736, -8.59538, -8.59537],
            "COLOR": ["red", "red", "red", "red"]  # Default color
        }, index=["BIBLIOTECA", "JUNIFEUP", "CANTINA", "DEEC"])

COLUNAS = st.columns((3, 5, 2), gap = "small" )
    
with COLUNAS[0]:
    COLUNAS_0 = st.columns((1, 1))

    with COLUNAS_0[0]:
        #Clock
        clock_placeholder = st.empty()
        st.image('FEUP_CAMPUS.png', use_column_width=True)

    # Apply custom CSS to reduce gap between checkboxes in the first column
    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)
    ####################

    with COLUNAS_0[1]:
        with st.container(border = True):
                st.markdown("**Selected DCUs:**", unsafe_allow_html=True)
                # Create checkboxes
                biblioteca = st.checkbox("BIBLIOTECA")
                junifeup = st.checkbox("JUNIFEUP")
                cantina = st.checkbox("CANTINA")
                deec = st.checkbox("DEEC")
                if biblioteca == True:
                    st.session_state.DCUs.loc['BIBLIOTECA', 'COLOR'] = 'green'
                else:
                    st.session_state.DCUs.loc['BIBLIOTECA', 'COLOR'] = 'red'
                if junifeup == True:
                    st.session_state.DCUs.loc['JUNIFEUP', 'COLOR'] = 'green'
                else:
                    st.session_state.DCUs.loc['JUNIFEUP', 'COLOR'] = 'red'
                if cantina == True:
                    st.session_state.DCUs.loc['CANTINA', 'COLOR'] = 'green'
                else:
                    st.session_state.DCUs.loc['CANTINA', 'COLOR'] = 'red'
                if deec == True:
                    st.session_state.DCUs.loc['DEEC', 'COLOR'] = 'green'
                else:
                    st.session_state.DCUs.loc['DEEC', 'COLOR'] = 'red'


    # Plot the map with colors corresponding to checkbox states
    fig = px.scatter_mapbox(st.session_state.DCUs, lat="LATITUDE", lon="LONGITUDE", color=st.session_state.DCUs['COLOR'], 
                            color_discrete_map={color: color for color in st.session_state.DCUs['COLOR'].unique()},
                            hover_name=st.session_state.DCUs.index, zoom=15)
    fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend = False)
    fig.update_traces(marker={'size': 20},
                 hovertemplate="<b>%{hovertext}</b><br>Longitude: %{lon}<br>Latitude: %{lat}") # Customize hover information
    st.plotly_chart(fig, use_container_width=True)


dcu_files = ['DCU1_airquality_data.csv', 'DCU2_airquality_data.csv', 'DCU3_airquality_data.csv', 'DCU4_airquality_data.csv']
checkbox_names = ["BIBLIOTECA", "JUNIFEUP", "CANTINA", "DEEC"]
checkboxes = [biblioteca, junifeup, cantina, deec]

dfs = []
# Iterate over the checkboxes and load the selected DCUs' data into DataFrames
for i in range(4):
    if checkboxes[i] == True:
        df_dcu = pd.read_csv(dcu_files[dcu_files.index(f'{dcu_files[i]}')])
        df_dcu.name = checkbox_names[i]  # Assign checkbox name as dataframe name
        dfs.append(df_dcu)
                        # # Concatenate the selected DCUs' DataFrames into a single DataFrame
                        # if df == []:
                        #     df = pd.DataFrame()
                        # else:
                        #     df = pd.concat(df, ignore_index=True)

if dfs == []: #if no dcu selected, select empty data
    df_dcu = pd.read_csv('DCU0_airquality_data.csv')
    df_dcu.name = 'No_DCU_Selected'
    dfs.append(df_dcu)


# Convert seconds to datetime for better handling of dates
for df in dfs:
    # Perform operations on each DataFrame
    df['datetime'] = pd.to_datetime(df['seconds'], unit='s')
    df['days'] = df['datetime'].dt.date



with COLUNAS[1]:
    with st.container(border = True):
        COLUNAS_1 = st.columns((1, 1, 1))
        with COLUNAS_1[0]:
            data_type = st.selectbox(
                'Data Type',
                options=['particles_p1', 'particles_p2', 'o3_data'],
                index=0  # default value
            )
        min_dates = [df['days'].min() for df in dfs] #minimum day of all dcus
        max_dates = [df['days'].max() for df in dfs] #maximum day of all dcus
        with COLUNAS_1[1]:
            min_day = st.date_input('Start Date', min(min_dates), key='start_date')
        with COLUNAS_1[2]:
            max_day = st.date_input('End Date', max(max_dates), key='end_date')


    with st.container(border = True):
        ######################GRAPH_OR NOT####################################
        # Check if the first DataFrame in dfs has the name 'No_DCU_Selected'
        if dfs and dfs[0].name == 'No_DCU_Selected':
            # Create an empty figure with the desired size
            fig_no_dcu = go.Figure(layout=dict(width=655, height=455))

            # Add a scatter plot with no data, just to set the layout
            fig_no_dcu.add_trace(go.Scatter(x=[], y=[], mode='markers', marker=dict(color='white')))

            # Add a text annotation in the middle with 'No DCU Selected'
            fig_no_dcu.update_layout(
                title=dict(text='<b>No DCU Selected</b>', y=0.5, x=0.5, xanchor='center', yanchor='middle', font=dict(size=24))
            )

            # Show the plot
            st.plotly_chart(fig_no_dcu)

        else:
            # Create an empty figure
            fig_graph = go.Figure(layout=dict(width=655, height=455))

            # Iterate over each selected dataframe
            for df in dfs:
                # Filter the dataframe based on the selected date range
                mask = (df['days'] >= min_day) & (df['days'] <= max_day)
                filtered_df = df.loc[mask]

                # Add a scatter plot trace to the figure
                fig_graph.add_trace(go.Scatter(x=filtered_df['days'], y=filtered_df[data_type], mode='lines', name=df.name))

            # Customize the layout of the figure
            fig_graph.update_layout(
                xaxis_title='Days',
                yaxis_title=data_type,
                title={
                    'text': f'<b>{data_type} over Time</b>',
                    'y': 0.9,  # new
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis=dict(tickmode='linear', dtick='D5'),  # Show a date every 5 days
                showlegend=True,
                legend=dict(
                    x=1,  # Set the x position of the legend (0-1, with 0 being left and 1 being right)
                    xanchor='right',  # align with right
                    y=1.35,  # Set the y position of the legend (0-1, with 0 being bottom and 1 being top)
                    bgcolor='rgba(255, 255, 255, 0.5)',  # Set the background color of the legend
                    bordercolor='rgba(0, 0, 0, 0.5)',  # Set the border color of the legend
                    borderwidth=1  # Set the border width of the legend
                )
            )

            fig_graph.update_layout(autosize=True)  # adjust automatically, maybe not needed
            # Show the plot
            st.plotly_chart(fig_graph)

    

with COLUNAS[2]:
    with st.container(border = True):
        st.code(body = """
                    _f
                    _
                    # _
                    _
                    _
                    _
                    _
                    _
                    _
                    """)
    
    with st.container(border = True):
        st.code(body = """
                    _g
                    _
                    _
                    _
                    _
                    _
                    _
                    _
                    """)
    
    with st.container(border = True):
        st.code(body = """
                    _h
                    _
                    _
                    _
                    _
                    _
                    _
                    _
                    _
                    """)
