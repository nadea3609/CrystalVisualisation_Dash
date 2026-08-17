import subprocess
import sys

packages = ["numpy", "dash", "plotly", "plotly_gif"]
for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
