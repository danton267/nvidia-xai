import dash
from dash import Input, Output, dcc, callback
import dash_mantine_components as dmc

from constants import shap_xpl
import utils.figures as figs

dash.register_page(__name__, path="/practical-XAI/customer-comparison")


def layout():
    initial_values = [
        [
            {"value": "37", "label": "37", "group": "Safe Loan"},
            {"value": "24", "label": "24", "group": "Likely Default"},
        ],
        [
            {"value": "43", "label": "43", "group": "Likely Default"},
            {"value": "13", "label": "13", "group": "Safe Loan"},
        ],
    ]

    initial_loan_selection = [int(item["value"]) for item in initial_values[1]]

    fig_comparison = shap_xpl.plot.compare_plot(
        row_num=initial_loan_selection, max_features=8
    )
    fig_feature_importance_comparison = shap_xpl.plot.features_importance(
        selection=initial_loan_selection
    )

    feature_comparison_controls = [
        dmc.Chip(
            x,
            value=str(x),
            variant="outline",
        )
        for x in initial_loan_selection
    ]
    feature_comparison_controls_values = [str(x) for x in initial_loan_selection]

    return dmc.Grid(
        [
            dmc.Col(
                dmc.TransferList(
                    value=initial_values,
                    id="customer-comparison-transfer",
                    # showTransferAll=False,
                    titles=["Loan Selection ", "Displayed Loan(s)"],
                    placeholder="No laons left",
                ),
                span=4,
            ),
            dmc.Col(
                [
                    dcc.Graph(
                        figure=fig_comparison,
                        id="customer-comparison-figure",
                        config={"displayModeBar": False},
                        responsive=True,
                    ),
                ],
                span=4,
            ),
            dmc.Col(
                [
                    dmc.Center(
                        dmc.ChipGroup(
                            children=feature_comparison_controls,
                            value=feature_comparison_controls_values,
                            id="feature-comparison-selection",
                            multiple=True,
                        )
                    ),
                    dcc.Graph(
                        figure=fig_feature_importance_comparison,
                        id="customer-feature-comparison-figure",
                        config={"displayModeBar": False},
                        responsive=True,
                    ),
                ],
                span=4,
            ),
        ],
    )


@callback(
    Output("customer-comparison-figure", "figure"),
    Output("feature-comparison-selection", "children"),
    Output("feature-comparison-selection", "value"),
    Input("customer-comparison-transfer", "value"),
    prevent_initial_call=True,
)
def update_comparison_figure(comparison_choices):
    """
    Updates the comparison figure based on the transfer list selection.
    Create chip selection for feature importance figure, and automatically select all of them.
    """
    loan_selection = [int(item["value"]) for item in comparison_choices[1]]

    ## if no loanns are selected, create empty figure notifying user to select at least one loan, and remove all chips
    if len(loan_selection) == 0:
        return (
            figs.create_empty("Please select at least one loan."),
            [],
            [],
        )

    fig_comparison = shap_xpl.plot.compare_plot(row_num=loan_selection, max_features=8)

    feature_importance_controls = [
        dmc.Chip(
            x,
            value=str(x),
            variant="outline",
        )
        for x in loan_selection
    ]
    feature_importance_controls_values = [str(x) for x in loan_selection]
    return (
        fig_comparison,
        feature_importance_controls,
        feature_importance_controls_values,
    )


@callback(
    Output("customer-feature-comparison-figure", "figure"),
    Input("feature-comparison-selection", "value"),
    prevent_initial_call=True,
)
def update_feature_importance_figure(feature_importance_controls_values):
    """
    Updates the feature importance figure based on the chip selection.
    """
    feature_importance_controls_values = [
        int(x) for x in feature_importance_controls_values
    ]

    ## if no features are selected return global feature importance
    if len(feature_importance_controls_values) == 0:
        return shap_xpl.plot.features_importance()

    return shap_xpl.plot.features_importance(
        selection=feature_importance_controls_values
    )
