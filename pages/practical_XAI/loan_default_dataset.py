import dash, pickle
from dash import Input, Output, html, dcc, State, callback
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd
import numpy as np

from constants import shap_xpl, shap_explained_data
import utils.figures as figs

dash.register_page(__name__, path="/practical-XAI/loan-default-dataset")


def layout():
    columnDefs = [{"field": col} for col in shap_explained_data.columns]

    # with open("assets/models/shap_explainer.pkl", "rb") as f:
    #     shap_xpl = pickle.load(f)

    # fig_feature_importnace = shap_xpl.plot.features_importance()
    # fig_feature_importnace.data[0].marker.color = [
    #     "rgba(118,185,0,1)"
    #     for _ in range(len(fig_feature_importnace.data[0].marker.color))
    # ]

    fig_feature_contrib = shap_xpl.plot.contribution_plot(col="CreditScore", proba=True)
    # fig_feature_contrib.update_layout(
    #     coloraxis=dict(
    #         colorbar=dict(title={"text": "test"}),
    #         colorscale=[[0, "#76b900"], [1, "#B77F37"]],
    #     )
    # )

    DEFAULT_IDX = "1"
    individual_shap_prediction = shap_xpl.plot.local_plot(index=DEFAULT_IDX)
    # for trace in individual_shap_prediction.data:
    #     if trace.x[0] > 0:
    #         trace.marker.color = "rgba(183,127,55,1)"
    #     else:
    #         trace.marker.color = "rgba(118,185,0,1)"
    print("here 2")
    # percentage = shap_xpl.proba_values.iloc[DEFAULT_IDX]["class_1"] * 100
    fig_default_gauge = figs.action_gauge_chart(0)

    layout = dmc.SimpleGrid(
        cols=2,
        children=[
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dcc.Graph(
                    # figure=fig_feature_importnace,
                    config={"displayModeBar": False},
                    id="fig-feature-importnace",
                    responsive=True,
                ),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dcc.Graph(
                    figure=figs.style(fig_feature_contrib),
                    config={"displayModeBar": False},
                    id="fig-feature-contrib",
                    responsive=True,
                ),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dcc.Graph(
                    figure=figs.style(individual_shap_prediction),
                    config={"displayModeBar": False},
                    id="individual-shap-prediction",
                    responsive=True,
                ),
            ),
            # dmc.Card(
            #     withBorder=True,
            #     shadow="sm",
            #     radius="md",
            #     children=dcc.Graph(
            #         figure=shap_xpl.plot.top_interactions_plot(nb_top_interactions=5),
            #     ),
            # ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dcc.Graph(
                    figure=figs.style(fig_default_gauge),
                    config={"displayModeBar": False},
                    id="gauge-default-prediction",
                    responsive=True,
                ),
            ),
            dmc.Card(
                withBorder=True,
                shadow="sm",
                radius="md",
                children=dag.AgGrid(
                    id="ag-grid-shap-explained-data",
                    columnDefs=columnDefs,
                    rowData=shap_explained_data.to_dict("records"),
                    # columnSize="autoSizeAll",
                    defaultColDef={"resizable": True, "sortable": True, "filter": True},
                ),
            ),
        ],
    )

    return layout


@callback(
    Output("individual-shap-prediction", "figure"),
    Output("gauge-default-prediction", "figure"),
    Input("fig-feature-contrib", "clickData"),
    prevent_initial_call=True,
)
def update_individual_shap_prediction(clickData):
    if clickData is not None:
        point_idx = str(clickData["points"][0]["customdata"][1])
        fig = shap_xpl.plot.local_plot(index=point_idx)
        fig_default_gauge = figs.action_gauge_chart(
            shap_xpl.proba_values.iloc[point_idx]["class_1"]
        )
        return figs.style(fig), figs.style(fig_default_gauge)
    else:
        return dash.no_update, dash.no_update


@callback(
    Output("fig-feature-contrib", "figure"),
    Input("fig-feature-importnace", "clickData"),
    prevent_initial_call=True,
)
def update_individual_shap_prediction(clickData):
    if clickData is not None:
        print(clickData)
        point_col = clickData["points"][0]["customdata"]
        print(point_col)
        fig = shap_xpl.plot.contribution_plot(col=point_col, proba=True)
        return fig
    else:
        return dash.no_update
