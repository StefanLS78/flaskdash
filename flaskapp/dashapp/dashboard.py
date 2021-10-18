from dash import Dash
from re import A, X
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# data extraction
from flask_login import login_required

xls = pd.ExcelFile(r'C:\Users\stefa\Code\projects\flaks_dash_app\flaskdash\flaskapp\assets\voortgang.xls')
vulling = pd.read_excel(xls, 'vulling')  # tabblad vulling van de excelfile binnen halen
training = pd.read_excel(xls, 'training')  # tabblad training van de excelfile binnen halen
# data cleansing & wrangling
vulling['vullingspercentage'] = (vulling['feitelijk'] / vulling['norm']) * 100  # vullingspercentage berekenen
vulling['vacaturepercentage'] = 100 - (vulling['vullingspercentage'])  # vacaturepercentage berekenen
# pie_data = vulling.drop(columns=['norm', 'feitelijk']) #data voor pie chart voorbereiden

vulling["asic"] = vulling["asic"].apply(lambda _: _.strip())
vulling.reset_index()
vulling.set_index("asic", inplace=True)
vulling.drop(columns=['norm', 'feitelijk'], inplace=True)
vulling.round(2)

training["asic"] = training["asic"].apply(lambda _: _.strip())
training.reset_index()
training.set_index("asic", inplace=True)

opleiding = pd.read_excel(xls, 'opleiding')
opleiding['asic'] = opleiding['asic'].str.strip()

print(vulling)
print(training)
# print(opleiding)

asics = vulling.index


# options = [{'label': a, 'value': a} for a in asics]


def init_dashboard(server):
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashboard/',
                         external_stylesheets=['flaskapp/assets/layout.css']
                         )

    for view_func in dash_app.server.view_functions:
        if view_func.startswith('/dashboard/'):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])

    colors = {
        'background': '#111111',
        'text': "#909090"
    }

    dash_app.layout = html.Div([
        html.Div([
            html.H3(
                children='Dashboard 106 Inlichtingen compagnie',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            html.H4(id='app-1-display-value',
                    style=dict({
                        'textAlign': 'center',
                        'color': colors['text']
                    })
                    ),
            html.Div([
                dcc.Dropdown(
                    id='dropdown-asic',
                    options=[{'label': a, 'value': a} for a in asics],
                    value='A',
                    style={
                        'width': '30%'
                    }

                )
            ], className='dropdown'),
        ], className='header'),
        html.Div([

            html.Div([
                dcc.Graph(id='graph-1',
                          style={'width': '100%'}),
            ], className='container shadowbox-1'),

            html.Div([
                dcc.Graph(id='graph-2',
                          style={'width': '100%'})
            ], className='container shadowbox-1'),

            # dcc.Link('Go to App 2', href='/apps/app2')
        ], className='grid-container'),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-3',
                          style={'width': '100%',
                                 'align': 'center'})
            ], className='shadowbox-2')
        ])
    ], className='body bg-radial'
    )

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('app-1-display-value', 'children'),
        Input('dropdown-asic', 'value'))
    def display_value(value):
        return 'Je hebt asic {} geselecteerd'.format(value)

    @dash_app.callback(
        [
            Output('graph-1', 'figure'),
            Output('graph-2', 'figure'),
            Output('graph-3', 'figure')
        ],
        Input('dropdown-asic', 'value'))
    def generate_chart(slctd_asic):
        pie_data = vulling[vulling.index == slctd_asic]
        print(pie_data)
        # fig = px.bar(vulling, x='asic', y=['vullingspercentage', 'vacaturepercentage'], title='vullingspercentage')

        horbar_data = training[training.index == slctd_asic]
        print(horbar_data)

        verbar_data = opleiding[opleiding['asic'] == slctd_asic]
        print(verbar_data)

        fig1 = px.pie(
            data_frame=pie_data,
            values=pie_data.loc[pie_data.index[0]],  # [['vullingspercentage', 'vacaturepercentage']],
            # names=vulling.index,
            title='Vullingsgraad per asic',
            hole=.6

        )

        fig1.update_layout(
            height=315,
            margin=dict(l=20, r=30, t=100, b=30),
            paper_bgcolor='rgb(0,0,0,0)',
            font_color='#909090'
        )

        fig1.update_traces(
            marker_colors=('green', 'red'),
            text=['Gevuld', 'Vacature'],
            hovertemplate='%{text}',
            # labels=pie_data,
            hoverlabel=dict(
                bgcolor='thistle',
                font_size=14,
                font_family='Rockwell'
            ),
            selector=dict(type='pie')

        )
        fig2 = px.bar(horbar_data,
                      x=['staftraining 1', 'staftraining 2', 'staftraining 3'],
                      y=horbar_data.index,
                      # width=600,
                      # height=300,
                      color_discrete_map={
                          'staftraining 1': '#cc00cc',
                          'staftraining 2': '#990099',
                          'staftraining 3': '#660066'},
                      title='Trainigsgraad per asic'
                      )
        fig2.add_shape(
            type='line',
            line_color='crimson',
            line_width=2,
            opacity=1,
            line_dash='dash',
            # x0=-0.5, x1=4.4, y0=2, y1=2
            x0=2, x1=2, y0=-0.5, y1=4.4
        )

        fig2.update_layout(
            height=315,
            width=600,
            margin=dict(l=20, r=30, t=100, b=30),
            plot_bgcolor='rgb(0,0,0,0)',
            legend_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgb(0,0,0,0)',
            font_color='#909090'
        )

        fig3 = px.bar(verbar_data,
                      y=['VTO', 'opleiding 2', 'opleiding 3', 'opleiding 4', 'opleiding 5', 'opleiding 6',
                         'opleiding 7', 'opleiding 8', 'opleiding 9', 'opleiding 10', 'opleiding 11', 'opleiding 12',
                         'opleiding 13'],
                      x=verbar_data.functie,
                      color_discrete_map={
                          'VTO': '#ff80ff',
                          'opleiding 2': '#ff66ff',
                          'opleiding 3': '#ff4dff',
                          'opleiding 4': '#ff33ff',
                          'opleiding 5': '#ff1aff',
                          'opleiding 6': '#ff00ff',
                          'opleiding 7': '#e600e6',
                          'opleiding 8': '#cc00cc',
                          'opleiding 9': '#b300b3',
                          'opleiding 10': '#990099',
                          'opleiding 11': '#800080',
                          'opleiding 12': '#660066',
                          'opleiding 13': '#4d004d',

                      },
                      title='Opleidingsgraad per asic'
                      )
        fig3.update_layout(
            margin=dict(l=20, r=30, t=100, b=30),
            plot_bgcolor='rgb(0,0,0,0)',
            legend_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgb(0,0,0,0)',
            font_color='#909090'
        )

        return fig1, fig2, fig3
