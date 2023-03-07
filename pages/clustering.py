import dash
from dash import Input, Output, html, dcc, callback
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go

from constants import df_embedding
import utils.figures as figs

dash.register_page(__name__, path="/clustering")


def layout():
    fig_empty = figs.create_empty("Figure is being created")

    return dmc.SimpleGrid(
        cols=2,
        children=[
            dmc.Card(
                [
                    dmc.Center(
                        dmc.SegmentedControl(
                            id="segmented-default-control",
                            value="everything",
                            data=[
                                {"value": "default", "label": "Defaulted"},
                                {"value": "safe", "label": "Safe Only"},
                                {"value": "everything", "label": "Everything"},
                            ],
                            mt=10,
                        ),
                    ),
                    dmc.Space(h=10),
                    dmc.LoadingOverlay(dcc.Graph(figure=fig_empty, id="fig-clusters")),
                ]
            ),
            dmc.Card(
                dmc.LoadingOverlay(
                    dcc.Graph(figure=fig_empty, id="fig-partition-shap")
                ),
            ),
            dcc.Location(id="url-cluster", refresh=False),
        ],
    )


@callback(
    Output("fig-partition-shap", "figure"),
    Input("fig-partition-shap", "figure"),
)
def create_partition_shap(url):
    """
    Create the partition shap plot. This one is static and does not need to be updated.
    We create it here so that the initial page load is fast, and in its place we create empty figure with a loading overlay.
    """
    return figs.partition_shap_bar_plot(df_embedding)


@callback(
    Output("fig-clusters", "figure"),
    Input("segmented-default-control", "value"),
)
def update_clusters(segmented_default_control):
    """
    Update the clusters plot based on the segmented control
    """
    return figs.partition_cluster(df_embedding, segmented_default_control)
    # if segmented_default_control == "default":
    #     df_temp = df_embedding[df_embedding["Default"] == "1"]
    # elif segmented_default_control == "safe":
    #     df_temp = df_embedding[df_embedding["Default"] == "0"]
    # else:
    #     fig = px.scatter(
    #         df_embedding, x="x", y="y", color="default_prop", custom_data=["partition"]
    #     )
    #     fig.data[
    #         0
    #     ].hovertemplate = "Partition: %{customdata[0]}<br>Parition default proportion: %{marker.color:.2f}%<extra></extra>"

    #     return fig
    # return px.scatter(df_temp, x="x", y="y", color="partition")
