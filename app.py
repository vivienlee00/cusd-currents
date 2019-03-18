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
        width=900,
        height=550,
         title='Room Air Temperature vs. Time',
         xaxis=dict(
         title='Time (minutes)',
         titlefont=dict(
         family='Helvetica',
         size=18,
         color='black'
         )
         ),
         yaxis=dict(
         title='Room Air Temperature (F)',
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
        dcc.Graph(id='graph', figure=fig),
    ],style={'float':'left','display': 'inline'}),

    html.Div(children=[
    dash_table.DataTable(
        id='table',
        columns=[{'name': 'Time (minutes)', 'id': 'time'},
                 {'name': 'Temp (F)', 'id': 'temp'}
             #{'name': 'Status', 'id': 'Status', 'hidden': True}
             ],
        data=df.to_dict("rows"),
        style_cell={'fontWeight': 'lighter','textAlign': 'left', 'font-family':'Helvetica', 'fontSize':'16px','padding':'5px', 'width':'50px'},
        style_cell_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
                }
        ]+ [
            {
                'if': {'column_id': c},
                'textAlign': 'left'
                } for c in ['time', 'temp']
        ],
        style_data={'whiteSpace': 'normal'},
        style_header={
        'backgroundColor': '#ABE2FB',
        'color':'black',
        'fontWeight': 'normal'
        },
        n_fixed_rows=1,
        style_as_list_view=True,
        css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_table={
        'maxHeight': '550',
        'overflowY': 'scroll'
        },
    )], style={'width':'calc(100% - 1100px)','display':'inline','float':'right'}),

        daq.Thermometer(
            id='my-thermometer',
            value=61,
            min=60,
            max=76,
            size=300,
            style={
                'margin-top': '5%','margin-bottom': '5%','margin-right':'80px','float':'right'
            }
        ),

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
