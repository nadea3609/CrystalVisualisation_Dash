import dash
from dash import html

dash.register_page(__name__, path="/Reference-list", name="References")

layout=html.Div([
    html.H1("References"),
    html.Ul([
        html.Li("""
        [1]: Bright, Matthew, Andrew I. Cooper, and Vitaliy Kurlin. 2023.
        'Geographic Style Maps for Two-Dimensional Lattices'. Acta Crystallographica
         Section A Foundations and Advances 79 (1): 1-13.
         https://doi.org/10.1107/S2053273322010075.
        """),
        html.Li("""
        [2]: Pulido, Angeles, Linjiang Chen, Tomasz Kaczorowski, et al. 2017.
         'Functional Materials Discovery Using Energy-Structure-Function Maps'.
         Nature 543 (7647): 657-64. https://doi.org/10.1038/nature21419.
        """),
    ])
])