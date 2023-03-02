import dash
from dash import Input, Output, State, dcc, html, dash_table, callback


from constants import app

server = app.server


app.layout = html.Div()


if __name__ == "__main__":
    app.run_server(debug=True)
