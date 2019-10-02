import dash
#from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import dash_table
import pandas as pd
import flask
from flask_cors import CORS
import os


'''
By Vivien Lee
'''

df = pd.read_csv('data.csv')
df.head()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                        "//fonts.googleapis.com/css?family=Dosis:Medium",
                        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]

app = dash.Dash(external_stylesheets=external_stylesheets)

for css in external_stylesheets:
    app.css.append_css({"external_url": css})

server = app.server

df['text'] = '' + df['time'].astype(str) + ' minutes, ' + df['temp'].astype(str) + ' degrees'
data = [ dict(
        type = 'scatter',
        x = df['time'],
        y = df['temp'],
        hoverinfo = 'text',
        text = df['text'],
        mode = 'lines+markers',
        marker = dict(
            size = 6,
            opacity = 0.8,
            reversescale = True,
            symbol = 'diamond',
            line = dict(
                width=1,
                color='black'
            ),
            color = '#ABE2FB',

        ))]

layout = dict(
        colorbar = True,
        autosize=False,
        width=700,
        height=410,
         title='Room Air Temperature vs. Time',
         xaxis=dict(
         title='Time (minutes)',
         fixedrange = True,
         titlefont=dict(
         family='Helvetica',
         size=18,
         color='black'
         )
         ),
         yaxis=dict(
         title='Room Air Temperature (F)',
         fixedrange = True,
         titlefont=dict(
         family='Helvetica',
         size=18,
         color='black'
         )
         )
    )

fig = dict( data=data, layout=layout)


app.layout  = html.Div(children=[

    html.Div(children=
    [
        dcc.Graph(id='graph', figure=fig, config={
        'displayModeBar': False
    }),

    ],style={'width':'550px',  'backgroundColor':'white', 'float':'left','display': 'inline', 'div-align':'center', 'position':'relative'}),


    html.Div(children=
    [
        daq.Thermometer(
            id='my-thermometer',
            value=61,
            min=60,
            max=76,
            size=360,
            style={
            'float':'left','margin-top': '5%'
            }
        ),
        html.Div(children=
        [
            html.P("This is the output from one of our earlier models. We're working to model the temperature in the room, so we can predict when we need to turn the heater on and when the heater can be off. If the algorithm predicts the professor will come to their office at 2pm, the model will predict how long it will take the room to get brought up to temperature, so we know when to turn the unit on so the room is ready just before he/she arrives to maximize energy savings.",style={'fontSize':'15px','margin-left':'15px','text-align':'justify','float':'right'}),
        ],style={'width':'300px','float':'right','margin-top': '15%'})

    ],style={'margin-right':'calc(100% - 1060px)','float':'right'})

], style={'backgroundColor':'white'})

def dfRowFromHover(hoverData):
    ''' Returns row for hover point as a Pandas Series '''
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'x' in firstPoint:
                time_x = firstPoint['x']
                return df.loc[df['time'] == time_x]
    return pd.Series()

@app.callback(
    dash.dependencies.Output('my-thermometer', 'value'),
    [dash.dependencies.Input('graph', 'hoverData')])
def update_thermometer(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            value = firstPoint['y']
            return value
#server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
