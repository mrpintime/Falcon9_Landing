## there are a few screenshots of virtual computer that i ran this code on it and visualize dataset and pull out insights of data.
# we answered some question with visualization that you can see that questions and related screenshots in pictures folder 
# Import required libraries
import pandas as pd
import dash
from dash import html, dcc 
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# print(spacex_df['Launch Site'].unique())

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label':'All Sites', 'value':'All'},
                                {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}]
                                , placeholder='Select a Launch Site here',searchable=True,
                                value='All', style={'textAlign':'center'}),
                                html.Br(),

                                # TASK 2
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                value=[min_payload, max_payload],
                                marks={
                                    0:'0', 1000:'1000',2000:'2000',3000:'3000',
                                    4000:'4000',5000:'5000',6000:'6000',7000:'7000',
                                    8000:'8000',9000:'9000',10000:'10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# print(spacex_df.head(1))
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def pie_chart(cSite):
    filtered_df = spacex_df
    if cSite == 'All':
        filtered_df = filtered_df[['Launch Site', 'class']]
        filtered_df.columns = ['Launch Site', 'Success Launch']
        fig = px.pie(filtered_df, values='Success Launch', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == cSite]
        filtered_df = filtered_df[['Launch Site', 'class']]
        filtered_df = filtered_df.groupby('class', as_index=False).count()
        filtered_df.columns = ['class', 'count']
        fig = px.pie(filtered_df, values='count', 
        names='class', 
        title=f'Total Success Launches for site {cSite}')
        return fig 
# # TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def scatter_chart(site, rangeval):
    low, high = rangeval
    if site == 'All':
        dfs = spacex_df[['Booster Version Category','Payload Mass (kg)','class']]
        dfs = dfs[(dfs['Payload Mass (kg)']>low) & (dfs['Payload Mass (kg)']<=high)]
        dfs = dfs.groupby(['Booster Version Category','Payload Mass (kg)'], as_index=False).mean()
        fg = px.scatter(data_frame=dfs, 
        x='Payload Mass (kg)', y='class', 
        color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites')
        return fg
    else:
        dfs = spacex_df[spacex_df['Launch Site'] == site]
        dfs = dfs[['Booster Version Category','Payload Mass (kg)','class']]
        dfs = dfs[(dfs['Payload Mass (kg)']>low) & (dfs['Payload Mass (kg)']<=high)]
        dfs = dfs.groupby(['Booster Version Category','Payload Mass (kg)'], as_index=False).mean()
        fg = px.scatter(data_frame=dfs, 
        x='Payload Mass (kg)', y='class', 
        color='Booster Version Category',
        title = f'Correlation between Payload and Success for site {site}')
        return fg

# Run the app
if __name__ == '__main__':
    app.run_server()
