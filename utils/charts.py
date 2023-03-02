import plotly.express as px
import plotly.graph_objs as go
import dash_shap_components as dsc
import json
import pandas as pd
from dash import html


def scatter_plot(df):
    fig = go.Figure(
        px.scatter(
            df,
            x="x",
            y="y",
            color="partition",
        )
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, title=None),
        yaxis=dict(showgrid=False, zeroline=False, title=None),
        legend=dict(orientation="v", x=1.15, title="Partition"),
        showlegend=False,
        margin=dict(pad=15),
    )
    return fig


def group_feature_bar_plot(df, selection):
    data = df.groupby("partition").mean().reset_index()
    data["partition"] = data["partition"].astype(int)
    data = data.sort_values("partition")
    data["partition"] = data["partition"].astype(str)

    fig = px.bar(
        data, x=selection, y="partition", orientation="h", color="partition"
    )
    fig.update_layout(
        xaxis=dict(title=None),
        yaxis=dict(title=None),
        legend=dict(orientation="v", x=1.15, title="Partition"),
        showlegend=False,
        margin=dict(pad=15),
    )

    return fig


def feature_importance_plot(selected_loan_id, data, data_og):
    index = data_og[data_og["LoanID"] == selected_loan_id].index.values[0]

    data_values = data_og.iloc[
        index, ~data_og.columns.isin(["LoanID", "partition"])
    ]
    data_values.sort_index(inplace=True)

    shap_values = data.loc[index, ~data.columns.isin(["x", "y", "partition"])]
    shap_values.sort_index(inplace=True)

    featureNames = {i: c for i, c in enumerate(shap_values.keys())}

    features = {
        i: {
            "effect": shap_values[values_shap],
            "value": data_values[values_og],
        }
        for i, (values_og, values_shap) in enumerate(
            zip(data_values.keys(), shap_values.keys())
        )
    }
    base_value = 0.1124156
    percentage = (base_value + shap_values.sum() + 5) * 10

    if percentage > 100:
        percentage = 100
    if percentage < 0:
        percentage = 1
    percentage = 100 - percentage

    return (
        dsc.ForcePlot(
            baseValue=base_value,
            link="identity",
            featureNames=featureNames,
            outNames=["Default"],
            features=features,
            hideBars=False,
            plot_cmap=["#B77F37", "#76b900"],
        ),
        percentage,
    )


def feature_importance_plot_create_new(data_values, shap_values):
    data_values = pd.DataFrame(data_values)
    shap_values = pd.DataFrame(shap_values)
    featureNames = {
        0: "Channel",
        1: "CoCreditScore",
        2: "CreditScore",
        3: "DTIRat",
        4: "Default",
        5: "Extra",
        6: "FTHomeBuyer",
        7: "LoanPurpose",
        8: "MortInsType",
        9: "NumBorrow",
        10: "NumUnits",
        11: "OccStatus",
        12: "OrCLTV",
        13: "OrInterestRate",
        14: "OrLoanTerm",
        15: "OrUnpaidPrinc",
        16: "ProductType",
        17: "PropertyState",
        18: "PropertyType",
        19: "SellerName",
        20: "Zip",
    }
    features = {
        i: {
            "effect": shap_values[values_shap],
            "value": data_values[values_og],
        }
        for i, (values_og, values_shap) in enumerate(
            zip(data_values.keys(), shap_values.keys())
        )
    }
    base_value = 0.1124156
    percentage = (base_value + shap_values.sum() + 5) * 10
    percentage = percentage.iloc[0]

    if percentage > 100:
        percentage = 100
    if percentage < 0:
        percentage = 1
    percentage = 100 - percentage

    return (
        dsc.ForcePlot(
            baseValue=base_value,
            link="identity",
            featureNames=featureNames,
            outNames=["Default"],
            features=features,
            hideBars=False,
            plot_cmap=["#B77F37", "#76b900"],
        ),
        percentage,
    )


def feature_importance_array_plot(data, title=None):

    with open("data/demo.json", "r") as f:
        data = json.loads(f.read())

    return dsc.ForceArrayPlot(
        baseValue=data["baseValue"],
        link=data["link"],
        featureNames=data["featureNames"],
        outNames=data["outNames"],
        explanations=data["explanations"][:200],
        plot_cmap=["#76b900", "#B77F37"],
    )


def action_gauge_chart(percentage):
    """ """
    chart = go.Figure(
        go.Indicator(
            mode="gauge",
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {
                    "range": [None, 100],
                    "ticks": "",
                    "ticktext": ["DEFAULT", "AVERAGE RISK", "SAFE"],
                    "tickvals": [25, 50, 75],
                    "tickmode": "array",
                },
                "borderwidth": 2,
                "bar": {"color": "#282d33"},
                "steps": [
                    {"range": [0, 33], "color": "var(--accent_negative)"},
                    {"range": [33, 66], "color": "var(--accent)"},
                    {"range": [66, 100], "color": "var(--accent_positive)"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 14},
                    "thickness": 0.75,
                    "value": percentage,
                },
            },
        )
    )
    chart.update_xaxes(visible=False)
    chart.update_yaxes(visible=False)
    chart.update_layout(
        font={"color": "var(--header_text)", "family": "Arial"},
        xaxis={"showgrid": False, "showticklabels": False, "range": [-1, 1]},
        yaxis={"showgrid": False, "showticklabels": False, "range": [0, 1]},
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return chart


def default_data_card(percentage):
    percentage = 100 - percentage
    if percentage > 66:
        color = "var(--accent_negative)"
    elif percentage > 33:
        color = "var(--accent)"
    else:
        color = "var(--accent_positive)"
    return html.Div()  # data card
