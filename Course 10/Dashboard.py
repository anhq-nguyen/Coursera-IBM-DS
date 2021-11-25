# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_site_list = spacex_df['Launch Site'].unique()
launch_site_list.sort()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'all'}] +\
                                        [{'label': i, 'value': i} for i in launch_site_list],
                                    value='all',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={i: '{}'.format(i) for i in range(0, 10001, 1000)},
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def get_pie_chart(selected_site):
    if selected_site == 'all':
        return px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        return px.pie(spacex_df[spacex_df['Launch Site'] == selected_site], names='class', title='Successful Launches for {}'.format(selected_site))


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def get_scatter_chart(selected_site, payload_range):
    if selected_site == 'all':
        return px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                          range_x=payload_range, title='Correlation between Payload and Success for all sites')
    else:
        return px.scatter(spacex_df[spacex_df['Launch Site'] == selected_site], range_x=payload_range,
                          x='Payload Mass (kg)', y='class', color="Booster Version Category",
                          title='Correlation between Payload and Success for %s' % selected_site)

# Run the app
if __name__ == '__main__':
    app.run_server()
