import dash, pickle, time, re, random
from dash import Input, Output, html, dcc, State, callback
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd
import numpy as np

from constants import shap_xpl, shap_explained_data
import utils.figures as figs

dash.register_page(__name__, path="/practical-XAI/loan-default-dataset")


def layout():
    columnDefs = [{"field": col} for col in shap_explained_data.columns.tolist() + ["Idx"]]

    fig_feature_importnace = figs.shap_feature_importance()
    fig_feature_contrib = figs.shap_contribution("LoanPurpose", True)
    individual_shap_prediction = figs.shap_local_plot(1)
    fig_default_gauge = figs.action_gauge_chart(26.5)
    fig_shap_top_interactions = figs.shap_top_interactions()
    
    table_data = shap_explained_data.reset_index().rename(columns={"index":'Idx'}).to_dict("records")
    
    layout = dmc.SimpleGrid(
        cols=2,
        children=[
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dmc.LoadingOverlay(dcc.Graph(
                    figure=fig_feature_importnace,
                    config={"displayModeBar": False},
                    id="fig-feature-importnace",
                    responsive=True,
                    style= {'min-height': '300px'}
                )),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dmc.LoadingOverlay(dcc.Graph(
                    figure=fig_feature_contrib,
                    config={"displayModeBar": False},
                    id="fig-feature-contrib",
                    responsive=True,
                    style= {'min-height': '300px'}
                )),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dmc.LoadingOverlay(dcc.Graph(
                    figure=individual_shap_prediction,
                    config={"displayModeBar": False},
                    id="individual-shap-prediction",
                    responsive=True,
                    style= {'min-height': '400px'}
                )),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dmc.LoadingOverlay(dcc.Graph(
                    figure=fig_default_gauge,
                    config={"displayModeBar": False},
                    id="gauge-default-prediction",
                    responsive=True,
                    style= {'min-height': '400px'}
                )),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dmc.LoadingOverlay(dcc.Graph(
                    figure=fig_shap_top_interactions,
                    config={"displayModeBar": False},
                    responsive=True,
                    style= {'min-height': '300px'}
                )),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dag.AgGrid(
                    id="table-shap-data",
                    columnDefs=columnDefs,
                    rowData=table_data,
                    # columnSize="autoSizeAll", # needs to be fixed in the package first, it causes lag
                    className="ag-theme-alpine-dark",
                    defaultColDef={"resizable": True, "sortable": True, "filter": True},
                    dashGridOptions={"pagination": True},
                    rowSelection="single",
                ),
            ),
        ],
    )

    return layout


@callback(
    Output("individual-shap-prediction", "figure"),
    Output("gauge-default-prediction", "figure"),
    Input("fig-feature-contrib", "clickData"),
    Input("table-shap-data", "selectedRows"),
    prevent_initial_call=True,
)
def update_individual_shap_prediction(figureClickData, tableClickData):
    if figureClickData is None and tableClickData is None:
        return dash.no_update, dash.no_update
    
    time.sleep(2)
    trigger_id =  dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "fig-feature-contrib":
        idx = figureClickData["points"][0]["customdata"][1]
        fig = figs.shap_local_plot(idx)

        percentage = figureClickData["points"][0]["marker.color"] * 100
        fig_gauge = figs.action_gauge_chart(percentage)

        return fig, fig_gauge
    else:
        idx = tableClickData[0]["Idx"]
        fig = figs.shap_local_plot(idx)
        # to get percentage from figure, sample: 'Local Explanation - Id: <b>2</' ... '> - Proba: <b>0.5566</b></sup>'
        match = re.search(r"Proba: <b>(\d+\.\d+)</b>", fig["layout"]["title"]["text"])
        percentage = float(match.group(1)) if match else random.random()
        percentage = round(percentage * 100, 2)
        fig_gauge = figs.action_gauge_chart(percentage)
        return fig, fig_gauge
        


@callback(
    Output("fig-feature-contrib", "figure"),
    Input("fig-feature-importnace", "clickData"),
    prevent_initial_call=True,
)
def update_individual_shap_prediction(clickData):
    if clickData is None:
        return dash.no_update
    col = clickData["points"][0]["customdata"]
    return figs.shap_contribution(col, True)
