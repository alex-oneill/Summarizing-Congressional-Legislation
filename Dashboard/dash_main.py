import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from db_functions import *
import pandas as pd

money_hits = pd.DataFrame(get_money_hits(), columns=['hit_type', 'row_number', 'row_text'])
money_hits.drop_duplicates(subset=['row_number'], inplace=True)
hit_list = money_hits.to_dict('records')
print(money_hits)

# SECTION: HITS TABLE CARD
hits_table = dbc.Card(
    [
        dbc.CardHeader('Money Hits',
                       style={'fontWeight': 'Bold', 'backgroundColor': '#D5D8DC', 'textTransform': 'uppercase',
                              'fontFamily': 'monospace', 'fontSize': '.875rem'}),
        dbc.CardBody(
            dash_table.DataTable(
                id='bill-title',
                data=hit_list,
                columns=[{'name': 'Hit Type', 'id': 'hit_type'},
                         {'name': 'Row Number', 'id': 'row_number'},
                         {'name': 'Text', 'id': 'row_text'}],
                style_header={'fontWeight': 'Bold', 'backgroundColor': '#D5D8DC',
                              'whiteSpace': 'normal', 'height': 'auto',
                              'textAlign': 'left'},
                style_data={'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'left'},
                style_table={'height': 500, 'overflowY': 'auto'},
                row_selectable='single',
                page_size=15
            ), id='hits-body')
    ], id='bill-card')

# SECTION: HITS DRILL-DOWN CARD
hits_drill_table = dbc.Card(
    [
        dbc.CardHeader('Drill Down - 5 rows',
                       style={'fontWeight': 'Bold', 'backgroundColor': '#D5D8DC', 'textTransform': 'uppercase',
                              'fontFamily': 'monospace', 'fontSize': '.875rem'}),
        dbc.CardBody(
            dash_table.DataTable(
                data=[],
                id='fin-drill-table',
                columns=[{'name': 'Row Number', 'id': 'Row Number'},
                         {'name': 'Text', 'id': 'Text'}],
                style_header={'fontWeight': 'Bold', 'backgroundColor': '#D5D8DC',
                              'whiteSpace': 'normal', 'height': 'auto',
                              'textAlign': 'left'},
                style_data={'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'left'},
                style_table={'height': 500, 'overflowY': 'auto'},
                page_size=15
            ), id='drill-body')
    ], id='hits-drill-card')

# SECTION: SIMILARITY CHART
sim_chart = dbc.Card(
    [
        dbc.CardHeader('Similarity Chart',
                       style={'fontWeight': 'Bold', 'backgroundColor': '#D5D8DC', 'textTransform': 'uppercase',
                              'fontFamily': 'monospace', 'fontSize': '.875rem'}),
        dbc.CardBody('something', id='sim-chart-body')
    ], id='sim-chart-card')

# SECTION: SIMILARITY DRILL DOWN
sim_drill = dbc.Card(
    [
        dbc.CardHeader('Similarity Drill Down',
                       style={'fontWeight': 'Bold', 'backgroundColor': '#D5D8DC', 'textTransform': 'uppercase',
                              'fontFamily': 'monospace', 'fontSize': '.875rem'}),
        dbc.CardBody(
            dash_table.DataTable(
                data=[],
                id='sim-drill-table',
                columns=[{'name': 'Row Number', 'id': 'Row Number'},
                         {'name': 'Text', 'id': 'Text'}],
                style_header={'fontWeight': 'Bold', 'backgroundColor': '#D5D8DC',
                              'whiteSpace': 'normal', 'height': 'auto',
                              'textAlign': 'left'},
                style_data={'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'left'},
                style_table={'height': 500, 'overflowY': 'auto'},
                page_size=15), id='sim-drill-body')
    ], id='sim-drill-card')


# SECTION: MAIN LAYOUT
app = dash.Dash()
app.layout = dbc.Container([
                            html.H1('Enter'),
                            dbc.Row(
                                [
                                    dbc.Col(hits_table, width=5),
                                    dbc.Col(sim_chart, width=7)
                                ]),
                            dbc.Row(
                                [
                                    dbc.Col(hits_drill_table, width=5),
                                    dbc.Col(sim_drill, width=7)
                                ]
                            )
            ], fluid=True)


# SECTION: DRILL DOWN CALLBACK
@app.callback(
    # Output('drill-body', 'children'),
    Output('fin-drill-table', 'data'),
    Input('bill-title', 'selected_rows')
)
def drill_down(selected_rows):
    if selected_rows:
        index = selected_rows[0]
        row_number = hit_list[index]['row_number']
        drilled = get_drill_rows(row_number)
        table_list = []
        for row, text in drilled:
            out_dict = {'Row Number': row, 'Text': text}
            table_list.append(out_dict)
        return table_list
#
# """
# Dash port of Shiny iris k-means example:
#
# https://shiny.rstudio.com/gallery/kmeans-example.html
# """
# import dash
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html
# import pandas as pd
# import plotly.graph_objs as go
# from dash.dependencies import Input, Output
# from sklearn import datasets
# from sklearn.cluster import KMeans
#
# iris_raw = datasets.load_iris()
# iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])
#
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# controls = dbc.Card(
#     [
#         dbc.FormGroup(
#             [
#                 dbc.Label("X variable"),
#                 dcc.Dropdown(
#                     id="x-variable",
#                     options=[
#                         {"label": col, "value": col} for col in iris.columns
#                     ],
#                     value="sepal length (cm)",
#                 ),
#             ]
#         ),
#         dbc.FormGroup(
#             [
#                 dbc.Label("Y variable"),
#                 dcc.Dropdown(
#                     id="y-variable",
#                     options=[
#                         {"label": col, "value": col} for col in iris.columns
#                     ],
#                     value="sepal width (cm)",
#                 ),
#             ]
#         ),
#         dbc.FormGroup(
#             [
#                 dbc.Label("Cluster count"),
#                 dbc.Input(id="cluster-count", type="number", value=3),
#             ]
#         ),
#     ],
#     body=True,
# )
#
# app.layout = dbc.Container(
#     [
#         html.H1("Iris k-means clustering"),
#         html.Hr(),
#         dbc.Row(
#             [
#                 dbc.Col(controls, md=4),
#                 dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
#             ],
#             align="center",
#         ),
#     ],
#     fluid=True,
# )
#
#
# @app.callback(
#     Output("cluster-graph", "figure"),
#     [
#         Input("x-variable", "value"),
#         Input("y-variable", "value"),
#         Input("cluster-count", "value"),
#     ],
# )
# def make_graph(x, y, n_clusters):
#     # minimal input validation, make sure there's at least one cluster
#     km = KMeans(n_clusters=max(n_clusters, 1))
#     df = iris.loc[:, [x, y]]
#     km.fit(df.values)
#     df["cluster"] = km.labels_
#
#     centers = km.cluster_centers_
#
#     data = [
#         go.Scatter(
#             x=df.loc[df.cluster == c, x],
#             y=df.loc[df.cluster == c, y],
#             mode="markers",
#             marker={"size": 8},
#             name="Cluster {}".format(c),
#         )
#         for c in range(n_clusters)
#     ]
#
#     data.append(
#         go.Scatter(
#             x=centers[:, 0],
#             y=centers[:, 1],
#             mode="markers",
#             marker={"color": "#000", "size": 12, "symbol": "diamond"},
#             name="Cluster centers",
#         )
#     )
#
#     layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}
#
#     return go.Figure(data=data, layout=layout)
#
#
# # make sure that x and y values can't be the same variable
# def filter_options(v):
#     """Disable option v"""
#     return [
#         {"label": col, "value": col, "disabled": col == v}
#         for col in iris.columns
#     ]
#
#
# # functionality is the same for both dropdowns, so we reuse filter_options
# app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
#     filter_options
# )
# app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
#     filter_options
# )

# cur.close()
# conn.close()


if __name__ == "__main__":
    app.run_server(debug=True)

    # dcc.Checklist(id='match-type',
    #               options=[
    #                   {'label': '$ Symbol', 'value': 'ds'},
    #                   {'label': 'Keyword', 'value': 'kw'},
    #                   {'label': 'Pattern', 'value': 're_phrase'}
    #               ],
    #               style={}),
    # dcc.Dropdown(id='bill-title',
    #              options=[
    #                  {'label': row[2], 'value': row[2]} for row in get_money_hits()],
    #              # style={'height': 100},
    #              optionHeight=80,
    #              placeholder='Select a bill')