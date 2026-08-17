import dash
from dash import html


dash.register_page(__name__, path="/data-description", name="Data description", order=3)

layout = html.Div([
    html.H3("COD database"),
    html.P("""
            The Crystallography Open Database is an open-access database which contains
             large numbers of crsystal structures stored as cif files. These are contributed
             by researchers who submit their work to the database. The COD has over 500,000 
             structures stored on it from mineralogy, crystallogrpahy, organic, and inorganic chemistry journals.

          """),
    html.H3("Data processing"),
    html.P("""
            Each cif file from the input database contains three-dimensional structural data
             for the crystal it describes. For the database map part of this app, the three-
            dimensional data is reduced to sets of two-dimensional superbases. This is done by taking the
             side lengths of the three-dimensional unit cell and pairing them into three pairs (assuming
             all three are provided) containing the two lengths and the angle between them. A reduction to
             an obtuse superbase is then performed on these two-dimensional pairs.
           """)
])
