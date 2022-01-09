# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\upadh\Desktop\final plot\spacex_launch_dash.csv")
z=spacex_df['Launch Site'].unique()
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[{'label':'All','value':'All'},{'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],value='All',placeholder='Enter launch site here',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                marks={0: '0',
                                100: '100'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart','figure'),Input('site-dropdown','value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'All':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total successful launch by site')
        return fig 
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
        count = filtered_df['class'].value_counts().reset_index()
        count.columns=['value','count']

        fig = px.pie(count, values='count', 
        names='value', 
        title='Total successful launches for'+ entered_site)
        return fig
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart','figure'),[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def scatter_plot(entered_site,payload_mass):
    if entered_site=='All':
        spacex_df2=spacex_df[(spacex_df['Payload Mass (kg)']>payload_mass[0]) & (spacex_df['Payload Mass (kg)']<payload_mass[1])]
        fig = px.scatter(spacex_df2,x='Payload Mass (kg)',y='class',color="Booster Version Category")
        return fig 
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        spacex_df2=filtered_df[(filtered_df['Payload Mass (kg)']>payload_mass[0]) & (filtered_df['Payload Mass (kg)']<payload_mass[1])]
        fig = px.scatter(spacex_df2,x='Payload Mass (kg)',y='class',color="Booster Version Category")
        return fig 


# Run the app
if __name__ == '__main__':
    app.run_server()