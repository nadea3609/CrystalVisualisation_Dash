# CrystalVisualisation_Dash
Code repository for MSc project "Interactive Visualisation of Crystals"

Main stable branch

## Required packages:

Dash v4.2.0

Numpy v2.4.3

Plotly v6.7.0

plotly_gif (third party, needs to be installed separately from plotly official packages) v0.0.4

https://github.com/dylanwal/plotly_gif/blob/master/README.md

Sqlite3 (requires SQLite third party library to be installed) v3.14 (optional package included on many python installations be default)

os (only for database_scan.py, which is not required for core operation of app) (default package)

glob (only required for database_scan.py) (default package)
## Installation
1)Install the packages required for the app as listed above

2)Extract the database from "cod_complete.zip" and place in working python directory alongside the app's python scripts and the assets folder

3)Run the "Dash_app.py" in any python interpreter and paste the IP output into the terminal into any browser (although interpreters such as VScode support native running of the app)

