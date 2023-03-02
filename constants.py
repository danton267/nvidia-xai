import os
import dash


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    pages=True,
    title="Nvidia XAI",
    update_title=None,
)
