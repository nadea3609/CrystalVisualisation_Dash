import dash
from dash import Dash, html, dcc

app = Dash("Lattice visualiser",
           use_pages=True,
           pages_folder="app_lattices_python")

app.layout = html.Div([
    html.H1("Continuous 2D lattices"),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)
