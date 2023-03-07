import dash
from dash import Input, Output, State, dcc, html, dash_table, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    title="Nvidia XAI",
    update_title=None,
)
server = app.server


app.layout = dmc.MantineProvider(
    children=[
        dmc.Header(
            height=60,
            # mb=120,
            children=[
                dmc.Container(
                    fluid=True,
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                    },
                    children=[
                        dmc.Group(
                            [
                                dmc.Image(
                                    src=dash.get_asset_url("images/nvidia_logo.png"),
                                    alt="nvidia-logo",
                                    width=200,
                                ),
                                dmc.Title("Explainable AI", style={"color": "#76b900"}),
                            ]
                        ),
                        dmc.Group(
                            spacing="lg",
                            children=[
                                dmc.Menu(
                                    trigger="hover",
                                    transition="skew-up",
                                    transitionDuration=250,
                                    children=[
                                        dmc.MenuTarget(
                                            dmc.Button(
                                                "Machine Learning",
                                                color="green",
                                                variant="outline",
                                            )
                                        ),
                                        dmc.MenuDropdown(
                                            [
                                                dmc.MenuItem(
                                                    "Clustering",
                                                    icon=DashIconify(
                                                        icon="tabler:photo"
                                                    ),
                                                    href="/clustering",
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                dmc.Menu(
                                    trigger="hover",
                                    transition="skew-down",
                                    transitionDuration=250,
                                    children=[
                                        dmc.MenuTarget(
                                            dmc.Button(
                                                "Practical XAI",
                                                color="green",
                                                variant="outline",
                                            )
                                        ),
                                        dmc.MenuDropdown(
                                            [
                                                dmc.MenuItem(
                                                    "Loan Default Dataset",
                                                    icon=DashIconify(
                                                        icon="majesticons:data"
                                                    ),
                                                    href="/practical-XAI/loan-default-dataset",
                                                ),
                                                dmc.MenuItem(
                                                    "New Loan Application",
                                                    icon=DashIconify(icon="mdi:bank"),
                                                    href="/practical-XAI/new-customer",
                                                ),
                                                dmc.MenuItem(
                                                    "Customer Comparison",
                                                    icon=DashIconify(
                                                        icon="pajamas:comparison"
                                                    ),
                                                    href="/practical-XAI/customer-comparison",
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Image(
                                    alt="plotly-logo",
                                    width=200,
                                    src=dash.get_asset_url(
                                        "images/light_plotly_dash_logo.png"
                                    ),
                                ),
                                # icon
                                dmc.Menu(
                                    trigger="hover",
                                    transition="rotate-right",
                                    transitionDuration=250,
                                    children=[
                                        dmc.MenuTarget(
                                            dmc.Button(
                                                "More Info",
                                                color="green",
                                                variant="outline",
                                            )
                                        ),
                                        dmc.MenuDropdown(
                                            [
                                                dmc.MenuLabel(
                                                    "Nvidia", style={"color": "green"}
                                                ),
                                                dmc.MenuItem(
                                                    "Website",
                                                    icon=DashIconify(
                                                        icon="bi:nvidia",
                                                        color="green",
                                                    ),
                                                    href="https://nvidia.com",
                                                    target="_blank",
                                                ),
                                                dmc.MenuItem(
                                                    "Contact",
                                                    icon=DashIconify(
                                                        icon="tabler:message"
                                                    ),
                                                    href="https://www.linkedin.com/in/jochenpapenbrock/",
                                                    target="_blank",
                                                ),
                                                dmc.MenuItem(
                                                    "Explainabel AI",
                                                    icon=DashIconify(
                                                        icon="carbon:machine-learning-model"
                                                    ),
                                                    href="https://developer.nvidia.com/blog/accelerating-trustworthy-ai-for-credit-risk-management/",
                                                    target="_blank",
                                                ),
                                                dmc.MenuDivider(),
                                                dmc.MenuLabel(
                                                    "Plotly", style={"color": "purple"}
                                                ),
                                                dmc.MenuItem(
                                                    "Website",
                                                    icon=DashIconify(
                                                        icon="simple-icons:plotly",
                                                        color="purple",
                                                    ),
                                                    href="https://plotly.com",
                                                    target="_blank",
                                                ),
                                                dmc.MenuItem(
                                                    "Contact",
                                                    icon=DashIconify(
                                                        icon="tabler:message"
                                                    ),
                                                    href="https://plotly.com/get-demo/",
                                                    target="_blank",
                                                ),
                                                dmc.MenuDivider(),
                                                dmc.MenuLabel("Other"),
                                                dmc.MenuItem(
                                                    "App Code",
                                                    icon=DashIconify(icon="mdi:github"),
                                                    href="github.com/plotly/dash",
                                                    target="_blank",
                                                ),
                                                dmc.MenuItem(
                                                    "Shapash",
                                                    icon=DashIconify(
                                                        icon="tabler:code"
                                                    ),
                                                    href="https://github.com/MAIF/shapash",
                                                    target="_blank",
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
        dmc.Container(
            dash.page_container,
            fluid=True,
            style={"paddingTop": 20, "paddingBottom": 20},
        ),
        # dmc.Footer(
        #     height=60,
        #     children=[dmc.Text("Company Name")],
        #     style={"backgroundColor": "#9c86e2"},
        # ),
    ],
    theme={
        "colorScheme": "dark",
        "fontFamily": "Merriweather Sans",
        "headings": {
            "fontFamily": "Open Sans",
        },
        "primaryColor": "green",
        "colors": {  # #6f992
            "green": [
                "#76b900",
                "#76b900",
                "#76b900",
                "#76b900",
                "#76b900",
                "#76b900",
                "#76b900",
                "#76b900",
                "#76b900",
                "#76b900",
            ],
            "dark": [
                "#C1C2C5",
                "#A6A7AB",
                "#909296",
                "#5c5f66",
                "#373A40",
                "#2C2E33",
                "#25262b",
                "#101113",
                "#101113",
                "#101113",
            ],
        }
        # "components": {
        #     "Button": {"styles": {"root": {"fontWeight": 400}}},
        #     "Alert": {"styles": {"title": {"fontWeight": 500}}},
        #     "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        # },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
)


if __name__ == "__main__":
    app.run_server(
        debug=True,
    )
