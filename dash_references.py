import dash
from dash import html

dash.register_page(__name__, path="/Reference-list", name="References")

layout = html.Div([
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
        html.Li("""
        [3]: Anosova, Olga, Vitaliy Kurlin, and Marjorie Senechal. 2024.
          'The Importance of Definitions in Crystallography'.
            IUCrJ 11 (4): 453-63. https://doi.org/10.1107/S2052252524004056.
        """),
        html.Li("""
        [4]: Kurlin, Vitaliy. 2022. 'Mathematics of 2-Dimensional Lattices'.
          Foundations of Computational Mathematics 24 (3): 805-63.
            https://doi.org/10.1007/s10208-022-09601-8.
        """),
        html.Li("""
        [5]: Gražulis, Saulius, Daniel Chateigner, Robert T. Downs, et al. 2009.
          'Crystallography Open Database - an Open-Access Collection of Crystal Structures'.
          Journal of Applied Crystallography 42 (4): 726-29.
          https://doi.org/10.1107/S0021889809016690.
        """),
        html.Li("""
        [6]: Gražulis, Saulius, Adriana Daškevič, Andrius Merkys, et al. 2012.
         'Crystallography Open Database (COD): An Open-Access Collection of Crystal Structures
          and Platform for World-Wide Collaboration'. Nucleic Acids Research 40 (D1): D420-27.
          https://doi.org/10.1093/nar/gkr900.
        """)
    ])
])
