#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("./spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

def assign_launch_outcome(launch_outcome):
    if launch_outcome == 1:
        return 'success'
    else:
        return 'failure'


app = dash.Dash(__name__)


app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),


                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                html.P("Payload range (Kg):"),

                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                    value=[min_payload, max_payload]
                                ),


                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
            ])


@app.callback(  Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
    total_launch_count = filtered_df['class'].count()
    successful_launch_count = filtered_df['class'].sum()
    failed_launch_count = total_launch_count - successful_launch_count
    dict_test = {'names':[0,1], 'values':[failed_launch_count,successful_launch_count]}
    new_df = pd.DataFrame(dict_test)
    values = list(new_df['values'])
    names = list(new_df['names'])
    title = f'Total Success Launches for site {entered_site} '
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        fig = px.pie(filtered_df, values=values, names=names, title=title)
        return fig


@app.callback(  Output(component_id='success-payload-scatter-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value'))

def get_scatter_plot(entered_site, slider_range_list):
    min_value = slider_range_list[0]
    max_value = slider_range_list[1]
    filtered_df = spacex_df.loc[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'] >= min_value) & (spacex_df['Payload Mass (kg)'] <= max_value)]
    title = f'Correlation between Payload and Success for {entered_site} '
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

