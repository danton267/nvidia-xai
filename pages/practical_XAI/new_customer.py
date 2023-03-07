import dash, random, time
from dash import Input, Output, State, html, dcc, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px
import dash_ag_grid as dag
import pandas as pd

from constants import shap_xpl, shap_predictor, CONTROLS
import utils.figures as figs

dash.register_page(__name__, path="/practical-XAI/new-customer")


def create_tooltip(tooltip_text):
    return dmc.FloatingTooltip(
        label=tooltip_text,
        position="bottom",
        radius="xl",
        color="green",
        children=DashIconify(icon="bi:info-circle-fill", color="green", width=25),
    )


def manage_control_items(_type):
    if _type == "create_components":
        control_items = []

        for component in CONTROLS:
            if component["component"] is not None:
                tooltip = (
                    create_tooltip(component["info"])
                    if component["info"] is not None
                    else None
                )
                control_items.append(
                    dmc.Card(
                        [
                            dmc.Group(
                                position="apart",
                                mt="md",
                                mb="xs",
                                children=[
                                    dmc.Title(
                                        component["label"], style={"color": "#76b900"}
                                    ),
                                    tooltip,
                                ],
                            ),
                            component["component"],
                        ]
                    )
                )

        control_items = [dmc.Col(x, span=6) for x in control_items]
        return dmc.Grid(
            control_items,
            style={"overflow-y": "scroll", "height": ""},
        )

    ## if random_values
    random_values = []
    for component in CONTROLS:
        if component["component"] is not None:
            random_values.append(component["random"]())
    return random_values


def layout():
    controls = manage_control_items("create_components")
    return dmc.Grid(
        [
            dmc.Col(
                dmc.LoadingOverlay(
                    controls,
                    loaderProps={"variant": "bars", "color": "green", "size": "xl"},
                ),
                span=5,
                # style={"overflow": "scroll"},
            ),
            dmc.Col(
                dmc.Stack(
                    align="center",
                    spacing="xl",
                    children=[
                        dmc.Button(
                            "Analyze the new customer",
                            id="create-new-customer",
                            color="green",
                            variant="outline",
                            size="xl",
                            radius="lg",
                        ),
                        dmc.Space(h="sm"),
                        dmc.Title("Generate Customer", order=2),
                        dmc.Select(
                            data=[
                                {"label": "Potentially safe customer", "value": "safe"},
                                {
                                    "label": "Potentially risky customer",
                                    "value": "risky",
                                },
                            ],
                            placeholder="Select a predefined customer",
                            id="select-pre-defined-customer",
                            style={"width": 300},
                        ),
                        dmc.Title("OR", order=3),
                        dmc.Button(
                            "Generate Random data",
                            id="generate-random-customer",
                            color="green",
                            compact=True,
                            variant="light",
                        ),
                    ],
                ),
                span=2,
            ),
            dmc.Col(
                dcc.Graph(
                    figure=figs.create_empty("Please create a new customer first"),
                    id="new-customer-graph",
                    config={"displayModeBar": False},
                ),
                span=5,
            ),
        ],
        id="modal-control-items",
    )


@callback(
    Output("select-pre-defined-customer", "value"),
    Output("input-Channel", "value"),
    Output("input-SellerName", "value"),
    Output("input-OrInterestRate", "value"),
    Output("input-OrUnpaidPrinc", "value"),
    Output("input-OrLoanTerm", "value"),
    Output("input-OrLTV", "value"),
    Output("input-OrCLTV", "value"),
    Output("input-NumBorrow", "value"),
    Output("input-DTIRat", "value"),
    Output("input-CreditScore", "value"),
    Output("input-FTHomeBuyer", "value"),
    Output("input-LoanPurpose", "value"),
    Output("input-PropertyType", "value"),
    Output("input-NumUnits", "value"),
    Output("input-OccStatus", "value"),
    Output("input-PropertyState", "value"),
    Output("input-Zip", "value"),
    Output("input-RelMortInd", "value"),
    Output("input-OrDateMonth", "value"),
    Output("input-FirstPaymentMonth", "value"),
    Input("generate-random-customer", "n_clicks"),
    Input("select-pre-defined-customer", "value"),
    prevent_initial_call=True,
)
def generate_customer(n_clicks, pre_defined_customer):
    time.sleep(1)
    ctx = dash.callback_context.triggered[0]["prop_id"]
    if ctx == "generate-random-customer.n_clicks":
        random = manage_control_items("random_values")
        return [None] + random
    elif ctx == "select-pre-defined-customer.value":
        if pre_defined_customer == "safe":
            return [
                dash.no_update,
                "C",
                "PNC BANK, N.A.",
                4.5,
                0,
                360,
                80,
                80,
                1,
                45,
                750,
                "N",
                "C",
                "SF",
                1,
                "P",
                "CA",
                94105,
                "N",
                1,
                1,
            ]
        elif pre_defined_customer == "risky":
            return [
                dash.no_update,
                "C",
                "PNC BANK, N.A.",
                4.5,
                0,
                360,
                80,
                80,
                1,
                45,
                750,
                "N",
                "C",
                "SF",
                1,
                "P",
                "CA",
                94105,
                "N",
                1,
                1,
            ]


@callback(
    Output("new-customer-graph", "figure"),
    Input("create-new-customer", "n_clicks"),
    State("input-Channel", "value"),
    State("input-SellerName", "value"),
    State("input-OrInterestRate", "value"),
    State("input-OrUnpaidPrinc", "value"),
    State("input-OrLoanTerm", "value"),
    State("input-OrLTV", "value"),
    State("input-OrCLTV", "value"),
    State("input-NumBorrow", "value"),
    State("input-DTIRat", "value"),
    State("input-CreditScore", "value"),
    State("input-FTHomeBuyer", "value"),
    State("input-LoanPurpose", "value"),
    State("input-PropertyType", "value"),
    State("input-NumUnits", "value"),
    State("input-OccStatus", "value"),
    State("input-PropertyState", "value"),
    State("input-Zip", "value"),
    State("input-RelMortInd", "value"),
    State("input-OrDateMonth", "value"),
    State("input-FirstPaymentMonth", "value"),
    prevent_initial_call=True,
)
def create_new_customer_figure(n_clicks, *args):
    new_customer = {
        "Channel": str(args[0]),
        "SellerName": str(args[1]),
        "OrInterestRate": float(args[2]),
        "OrUnpaidPrinc": float(args[3]),
        "OrLoanTerm": int(args[4]),
        "OrLTV": int(args[5]),
        "OrCLTV": int(args[6]),
        "NumBorrow": int(args[7]),
        "DTIRat": int(args[8]),
        "CreditScore": int(args[9]),
        "FTHomeBuyer": str(args[10]),
        "LoanPurpose": str(args[11]),
        "PropertyType": str(args[12]),
        "NumUnits": int(args[13]),
        "OccStatus": str(args[14]),
        "PropertyState": str(args[15]),
        "Zip": int(args[16]),
        "RelMortInd": str(args[17]),
        "OrDateMonth": int(args[18]),
        "FirstPaymentYear": 2007,
        "FirstPaymentMonth": int(args[19]),
        "OrDateYear": 2007,
    }

    print(new_customer)
    try:
        shap_predictor.add_input(x=new_customer)
    except Exception as e:
        print(e)
    # fig = shap_xpl.plot.local_plot(index=999999)
    return figs.create_empty("here")
