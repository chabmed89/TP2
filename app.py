
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''


import dash
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output, State

import pandas as pd

import preprocess
import bar_chart

from template import create_template
from modes import MODES


app = dash.Dash(__name__)
app.title = 'TP2 | INF8808'


def prep_data():
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    dataframe = pd.read_csv(r"C:\Users\LENOVO\OneDrive\Documents\TP2_viz\code\code\src\assets\data\romeo_and_juliet.csv")

    proc_data = preprocess.summarize_lines(dataframe)
    proc_data = preprocess.replace_others(proc_data)
    proc_data = preprocess.clean_names(proc_data)


    return proc_data


def init_app_layout(figure):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Who\'s Speaking?'),
            html.H2('An analysis of Shakespeare\'s Romeo and Juliet')
        ]),
        html.Main(children=[
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figure,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='line-chart'
                )
            ])
        ]),
        html.Footer(children=[
            html.Div(className='panel', children=[
                html.Div(id='info', children=[
                    html.P('Use the radio buttons to change the display.'),
                    html.P(children=[
                        html.Span('The current mode is : '),
                        html.Span(MODES['count'], id='mode')
                    ])
                ]),
                html.Div(children=[
                    dcc.RadioItems(
                        id='radio-items',
                        options=[
                            dict(
                                label=MODES['count'],
                                value=MODES['count']),
                            dict(
                                label=MODES['percent'],
                                value=MODES['percent']),
                        ],
                        value=MODES['count']
                    )
                ])
            ])
        ])
    ])


@app.callback(
    [Output('line-chart', 'figure'), Output('mode', 'children')],
    [Input('radio-items', 'value')],
    [State('line-chart', 'figure')]
)
def radio_updated(mode, figure):
    '''
        Updates the application after the radio input is modified.

        Args:
            mode: The mode selected in the radio input.
            figure: The figure as it is currently displayed
        Returns:
            new_fig: The figure to display after the change of radio input
            mode: The new mode
    '''
    # TODO : Update the figure's data and y axis, as well as the informational
    # text indicating the mode
    # Vérifier si le mode est valide

    global data  # Utiliser la variable globale `data`

    # Vérifier si le mode est valide
    mode = mode.lower()  # Uniformiser le mode en minuscule

    if mode not in ['count', 'percent']:
        raise ValueError(f"Invalid mode: {mode}. Choose 'count' or 'percent'.")

    # Créer une copie de la figure pour éviter de modifier l'original
    new_fig = go.Figure(figure)

    # Mettre à jour les données de la figure avec le mode sélectionné
    new_fig = bar_chart.draw(new_fig, data, mode)

    # Mettre à jour le titre de l'axe Y
    new_fig = bar_chart.update_y_axis(new_fig, mode)

    return new_fig, mode


data = prep_data()

create_template()

fig = bar_chart.init_figure()

app.layout = init_app_layout(fig)
