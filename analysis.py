# Marimo interactive notebook (script mode)
# Author email for verification: 24ds1000121@ds.study.iitm.ac.in
# How to run:
#   pip install marimo numpy pandas matplotlib
#   marimo edit analysis.py   # interactive editor UI
#   # or:
#   marimo run analysis.py    # run as a lightweight app

import marimo as mo

# Define the app object expected by Marimo
app = mo.App()

# --- Cell 1: Imports --------------------------------------------------------
# This cell provides libraries to downstream cells.
@app.cell
def imports():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    return np, pd, plt

# --- Cell 2: Widgets --------------------------------------------------------
# UI widgets (sliders) are inputs used by computation cells.
@app.cell
def widgets(mo=mo):
    n = mo.ui.slider(start=50, stop=2000, step=50, value=500, label="Sample size (n)")
    sigma = mo.ui.slider(start=0.1, stop=5.0, step=0.1, value=1.0, label="Noise σ")
    # Display both sliders vertically
    controls = mo.vstack([n, sigma])
    controls
    return n, sigma

# --- Cell 3: Data generation ------------------------------------------------
# Depends on: imports, widgets
# Creates a synthetic dataset whose noise is controlled by the sigma slider
# and whose length is controlled by the n slider.
@app.cell
def data(np, pd, n, sigma):
    rng = np.random.default_rng(42)
    size = int(n.value)
    x = rng.normal(0.0, 1.0, size=size)
    # Linear relation + Gaussian noise controlled by sigma
    y = 2.0 * x + rng.normal(0.0, float(sigma.value), size=size)
    df = pd.DataFrame({"x": x, "y": y})
    df
    return df

# --- Cell 4: Analysis -------------------------------------------------------
# Depends on: data, imports
# Computes correlation; downstream cells (markdown and plot) depend on this.
@app.cell
def analysis(np, df):
    corr = float(np.corrcoef(df["x"], df["y"])[0, 1])
    return corr

# --- Cell 5: Dynamic Markdown ----------------------------------------------
# Depends on: widgets, analysis
# Renders live documentation that reacts to the UI state.
@app.cell
def summary(mo=mo, n=None, sigma=None, corr=None):
    mo.md(f"""
# Interactive correlation demo

**Email:** `24ds1000121@ds.study.iitm.ac.in`  

- Current sample size **n = {int(n.value)}**
- Current noise **σ = {float(sigma.value):.2f}**
- Estimated Pearson correlation **r = {corr:.3f}**

> Increase σ to add noise and reduce correlation. Increase n to stabilize the estimate.

*Data flow:* `widgets → data → analysis → (summary + plot + preview)`
""")

# --- Cell 6: Visualization --------------------------------------------------
# Depends on: data, imports
# Uses matplotlib only (no seaborn), with default colors.
@app.cell
def plot(df, plt):
    fig, ax = plt.subplots()
    ax.scatter(df["x"], df["y"])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Scatter plot of y vs x")
    fig  # display
    return fig

# --- Cell 7: Data preview ---------------------------------------------------
# Depends on: data
# Shows a quick preview table of the current dataset.
@app.cell
def preview(df):
    df.head(12)

# Allow running via `python analysis.py` (optional)
if __name__ == "__main__":
    app.run()
