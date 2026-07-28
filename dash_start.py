import dash
from dash import html

dash.register_page(__name__, path="/", name="Landing page")

layout = html.Div([
    html.H1("Select an operation mode from the list above to get started")
])
