import pandas as pd
import dash_mantine_components as dmc
import random, dash, pickle

from shapash.explainer.smart_explainer import SmartExplainer
from shapash.utils.load_smartpredictor import load_smartpredictor

# shap_xpl = SmartExplainer.load(dash.get_asset_url("models/shap_explainer.pkl"))
# spah_predictor = load_smartpredictor(dash.get_asset_url("models/shap_predictor.pkl"))
# shap_explained_data = pd.read_csv(dash.get_asset_url("models/shap_explained_data.csv"))
# df_embedding = pd.read_csv(dash.get_asset_url("data/shap_clusters.csv"), index_col=0).sample(10_000, random_state=42)

with open("assets/models/shap_explainer.pkl", "rb") as f:
    shap_xpl = pickle.load(f)

with open("assets/models/shap_predictor.pkl", "rb") as f:
    shap_predictor = pickle.load(f)

shap_explained_data = pd.read_csv("assets/models/shap_explained_data.csv")

df_embedding = pd.read_parquet("assets/models/shap_clusters.parquet").sample(
    10_000, random_state=42
)
df_embedding["partition"] = df_embedding["partition"].astype(str)
df_embedding["Default"] = df_embedding["Default"].astype(str)


CONTROLS = [
    {
        "label": "Channel",
        "info": "The channel through which the loan was originated.",
        "component": dmc.Center(
            dmc.SegmentedControl(
                id="input-Channel",
                color="green",
                data=[
                    {"label": "Retail", "value": "R"},
                    {"label": "Call Center", "value": "C"},
                    {"label": "Branch", "value": "B"},
                ],
                value="R",
            )
        ),
        "random": lambda: random.choice(["R", "C", "B"]),
    },
    {
        "label": "Seller Name",
        "info": None,
        "component": dmc.Select(
            id="input-SellerName",
            placeholder="Select SellerName",
            data=[
                "JPMORGAN CHASE BANK, NATIONAL ASSOCIATION",
                "PNC BANK, N.A.",
                "BANK OF AMERICA, N.A.",
                "GMAC MORTGAGE, LLC",
                "OTHER",
                "WELLS FARGO BANK, N.A.",
                "CITIMORTGAGE, INC.",
                "AMTRUST BANK",
                "FDIC, RECEIVER, INDYMAC FEDERAL BANK FSB",
                "FLAGSTAR CAPITAL MARKETS CORPORATION",
                "SUNTRUST MORTGAGE INC.",
                "CHASE HOME FINANCE, LLC",
                "FIRST TENNESSEE BANK NATIONAL ASSOCIATION",
            ],
            value="JPMORGAN CHASE BANK, NATIONAL ASSOCIATION",
        ),
        "random": lambda: random.choice(
            [
                "JPMORGAN CHASE BANK, NATIONAL ASSOCIATION",
                "PNC BANK, N.A.",
                "BANK OF AMERICA, N.A.",
                "GMAC MORTGAGE, LLC",
                "OTHER",
                "WELLS FARGO BANK, N.A.",
                "CITIMORTGAGE, INC.",
                "AMTRUST BANK",
                "FDIC, RECEIVER, INDYMAC FEDERAL BANK FSB",
                "FLAGSTAR CAPITAL MARKETS CORPORATION",
                "SUNTRUST MORTGAGE INC.",
                "CHASE HOME FINANCE, LLC",
                "FIRST TENNESSEE BANK NATIONAL ASSOCIATION",
            ]
        ),
    },
    {
        "label": "Original Interest Rate",
        "info": "The interest rate of the loan at origination",
        "component": dmc.Slider(
            id="input-OrInterestRate",
            min=4,
            max=10,
            step=0.1,
            value=4.5,
            marks=[{"value": str(i), "label": str(i)} for i in range(0, 11, 1)],
        ),
        "random": lambda: random.uniform(4, 10),
    },
    {
        "label": "Original UPB",
        "info": "The unpaid principal balance of the loan at origination. This is the principal balance excluding any late fees, penalties, or additional principal payments that may have been applied to the loan.",
        "component": dmc.Slider(
            id="input-OrUnpaidPrinc",
            min=0,
            max=900000,
            step=1000,
            value=100000,
            marks=[
                {"value": str(i), "label": f"{i:,}"} for i in range(0, 900_001, 150_000)
            ],
        ),
        "random": lambda: random.randint(0, 1000000),
    },
    {
        "label": "Original Loan Term",
        "info": "The original term of the mortgage at origination in months",
        "component": dmc.Slider(
            id="input-OrLoanTerm",
            min=0,
            max=360,
            step=1,
            value=360,
            marks=[{"value": str(i), "label": str(i)} for i in range(0, 360, 30)],
        ),
        "random": lambda: random.randint(0, 360),
    },
    {
        "label": "Original LTV Ratio",
        "info": "The combined loan-to-value ratio of the mortgage at origination. This is the ratio of the combined first and second mortgage balance to the property value.",
        "component": dmc.Slider(
            id="input-OrLTV",
            min=0,
            max=100,
            step=1,
            value=80,
            marks=[{"value": str(i), "label": f"{i}%"} for i in range(0, 101, 10)],
        ),
        "random": lambda: random.randint(0, 100),
    },
    {
        "label": "LTV Ratio",
        "info": "The combined loan-to-value ratio of the mortgage at origination. This is the ratio of the combined first and second mortgage balance to the property value.",
        "component": dmc.Slider(
            id="input-OrCLTV",
            min=0,
            max=100,
            step=1,
            value=80,
            marks=[{"value": str(i), "label": f"{i}%"} for i in range(0, 101, 10)],
        ),
        "random": lambda: random.randint(0, 100),
    },
    {
        "label": "Borrowers",
        "info": "The number of borrowers on the loan.",
        "component": dmc.Slider(
            id="input-NumBorrow",
            min=1,
            max=4,
            step=1,
            value=1,
            marks=[{"value": str(i), "label": str(i)} for i in range(1, 5, 1)],
        ),
        "random": lambda: random.randint(1, 4),
    },
    {
        "label": "Debt to Income Ratio",
        "info": "The debt-to-income ratio of the borrower(s). This is the total monthly debt payments divided by the total monthly income.",
        "component": dmc.Slider(
            id="input-DTIRat",
            min=1,
            max=100,
            step=1,
            value=40,
            marks=[{"value": str(i), "label": str(i)} for i in range(0, 100, 10)],
        ),
        "random": lambda: random.randint(1, 100),
    },
    {
        "label": "Credit Score",
        "info": "The credit score of the borrower. This is the FICO credit score of the borrower.",
        "component": dmc.Slider(
            id="input-CreditScore",
            min=400,
            max=850,
            step=1,
            value=700,
            marks=[{"value": str(i), "label": str(i)} for i in range(0, 850, 100)],
        ),
        "random": lambda: random.randint(400, 850),
    },
    {
        "label": "First Time Buyer",
        "info": "A borrower who is purchasing a home as their first home.",
        "component": dmc.Center(
            dmc.SegmentedControl(
                id="input-FTHomeBuyer",
                color="green",
                data=[
                    {"label": "Yes", "value": "Y"},
                    {"label": "No", "value": "N"},
                ],
                value="Y",
            )
        ),
        "random": lambda: random.choice(["Y", "N"]),
    },
    {
        "label": "Loan Purpose",
        "info": None,
        "component": dmc.Select(
            id="input-LoanPurpose",
            data=[
                {"label": "Purchase", "value": "P"},
                {"label": "Cash-out Refinance", "value": "C"},
                {"label": "No Cash-out Refinance", "value": "N"},
                {"label": "Not Available", "value": "U"},
            ],
            value="P",
        ),
        "random": lambda: random.choice(["P", "C", "N", "U"]),
    },
    {
        "label": "Property Type",
        "info": "The type of property associated with the loan.",
        "component": dmc.Select(
            id="input-PropertyType",
            data=[
                {"label": "Single Family", "value": "SF"},
                {"label": "PUD (Planned Unit Development)", "value": "PU"},
                {"label": "Condo", "value": "CO"},
                {"label": "Manufactured Housing", "value": "MH"},
                {"label": "Cooperative", "value": "CP"},
            ],
            value="SF",
        ),
        "random": lambda: random.choice(["SF", "PU", "CO", "MH", "CP"]),
    },
    {
        "label": "Units",
        "info": "The number of units in the property.",
        "component": dmc.Slider(
            id="input-NumUnits",
            min=1,
            max=4,
            step=1,
            value=1,
            marks=[{"value": str(i), "label": str(i)} for i in range(1, 5, 1)],
        ),
        "random": lambda: random.randint(1, 4),
    },
    {
        "label": "Occupancy Status",
        "info": "The occupancy status of the property at the time of application.",
        "component": dmc.Center(
            dmc.SegmentedControl(
                id="input-OccStatus",
                color="green",
                data=[
                    {"label": "Principal Residence", "value": "P"},
                    {"label": "Second Residence", "value": "S"},
                    {"label": "Investment", "value": "I"},
                ],
                value="P",
            )
        ),
        "random": lambda: random.choice(["P", "S", "I"]),
    },
    {
        "label": "State",
        "info": "The state where the property is located.",
        "component": dmc.Select(
            id="input-PropertyState",
            data=[
                {"label": state, "value": state}
                for state in [
                    "DE",
                    "OH",
                    "MN",
                    "WI",
                    "ID",
                    "TN",
                    "NM",
                    "MA",
                    "RI",
                    "NV",
                    "WA",
                    "GA",
                    "VA",
                    "MT",
                    "AL",
                    "FL",
                    "MD",
                    "NY",
                    "PA",
                    "KS",
                    "CA",
                    "IL",
                    "UT",
                    "IA",
                    "OK",
                    "WY",
                    "ME",
                    "TX",
                    "AR",
                    "NJ",
                    "MS",
                    "OR",
                    "LA",
                    "WV",
                    "SC",
                    "MI",
                    "KY",
                    "IN",
                    "AZ",
                    "NC",
                    "NE",
                    "CO",
                    "MO",
                    "ND",
                    "NH",
                    "SD",
                    "HI",
                    "CT",
                    "DC",
                    "PR",
                    "AK",
                    "VT",
                ]
            ],
            value="CA",
        ),
        "random": lambda: random.choice(
            [
                "DE",
                "OH",
                "MN",
                "WI",
                "ID",
                "TN",
                "NM",
                "MA",
                "RI",
                "NV",
                "WA",
                "GA",
                "VA",
                "MT",
                "AL",
                "FL",
                "MD",
                "NY",
                "PA",
                "KS",
                "CA",
                "IL",
                "UT",
                "IA",
                "OK",
                "WY",
                "ME",
                "TX",
                "AR",
                "NJ",
                "MS",
                "OR",
                "LA",
                "WV",
                "SC",
                "MI",
                "KY",
                "IN",
                "AZ",
                "NC",
                "NE",
                "CO",
                "MO",
                "ND",
                "NH",
                "SD",
                "HI",
                "CT",
                "DC",
                "PR",
                "AK",
                "VT",
            ]
        ),
    },
    {
        "label": "Zip",
        "info": "The zip code of the property.",
        "component": dmc.Slider(
            id="input-Zip",
            min=0,
            max=1000,
            step=1,
            value=90000,
            marks=[{"value": str(i), "label": str(i)} for i in range(0, 1000, 100)],
        ),
        "random": lambda: random.randint(0, 1000),
    },
    {
        "label": "Relief Refinance Mortgage",
        "info": "A flag indicating whether the loan is a Freddie Mac Relief Refinance Mortgage (RRM).",
        "component": dmc.Center(
            dmc.SegmentedControl(
                id="input-RelMortInd",
                color="green",
                data=[
                    {"label": "Yes", "value": "Y"},
                    {"label": "No", "value": "N"},
                ],
                value="Y",
            )
        ),
        "random": lambda: random.choice(["Y", "N"]),
    },
    {
        "label": "Loan Start Month",
        "info": "The month the loan was originated.",
        "component": dmc.Select(
            id="input-OrDateMonth",
            data=[
                {"label": "January", "value": 1},
                {"label": "February", "value": 2},
                {"label": "March", "value": 3},
                {"label": "April", "value": 4},
                {"label": "May", "value": 5},
                {"label": "June", "value": 6},
                {"label": "July", "value": 7},
                {"label": "August", "value": 8},
                {"label": "September", "value": 9},
                {"label": "October", "value": 10},
                {"label": "November", "value": 11},
                {"label": "December", "value": 12},
            ],
            value=1,
        ),
        "random": lambda: random.randint(1, 12),
    },
    {
        "label": "First Payment Month",
        "info": "The first month of the loan.",
        "component": dmc.Select(
            id="input-FirstPaymentMonth",
            data=[
                {"label": "January", "value": 1},
                {"label": "February", "value": 2},
                {"label": "March", "value": 3},
                {"label": "April", "value": 4},
                {"label": "May", "value": 5},
                {"label": "June", "value": 6},
                {"label": "July", "value": 7},
                {"label": "August", "value": 8},
                {"label": "September", "value": 9},
                {"label": "October", "value": 10},
                {"label": "November", "value": 11},
                {"label": "December", "value": 12},
            ],
            value=1,
        ),
        "random": lambda: random.randint(1, 12),
    },
]
