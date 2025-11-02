# app.py — reads projects.csv and politicians.csv,
# prints clean summaries, saves flagged CSVs, and exports charts.

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent

# ---------- helpers ----------
def to_number(x):
    """Convert strings like '6,048,486' or '$400,000' to float."""
    if pd.isna(x):
        return 0.0
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).replace(',', '').replace('$', '').strip()
    return float(s) if s else 0.0

def norm_outcome(x):
    return str(x).strip().lower()

# ---------- load data ----------
projects = pd.read_csv(ROOT / "projects.csv", dtype=str).fillna("")
pols      = pd.read_csv(ROOT / "politicians.csv", dtype=str).fillna("")

# numeric conversions
projects["Budget_Declared"] = projects["Budget_Declared"].map(to_number)
projects["Actual_Spent"]    = projects["Actual_Spent"].map(to_number)
projects["Outcome"]         = projects["Outcome"].map(norm_outcome)

pols["Declared_Income"]  = pols["Declared_Income"].map(to_number)
pols["Project_Spending"] = pols["Project_Spending"].map(to_number)

# ---------- rules / flags ----------
projects["Budget_Gap"] = projects["Budget_Declared"] - projects["Actual_Spent"]

# Ghost project = very large gap OR incomplete with very low spend
projects["Ghost_Risk"] = (
    (projects["Budget_Gap"] >= 1_000_000) |
    ((projects["Outcome"] != "completed") & (projects["Actual_Spent"] <= projects["Budget_Declared"] * 0.10))
)

pols["Spend_to_Income"] = pols["Project_Spending"] / pols["Declared_Income"].replace(0, pd.NA)
pols["Overspend_Flag"]  = pols["Spend_to_Income"] > 3.0

# ---------- pretty print to terminal ----------
def money(series):
    return series.map(lambda v: f"${v:,.0f}")

print("\n=== SUMMARY ===")
print(f"Projects flagged (ghost risk): {int(projects['Ghost_Risk'].sum())} of {len(projects)}")
print(f"Politicians flagged (spending > 3× income): {int(pols['Overspend_Flag'].sum())} of {len(pols)}")

print("\n— Project Details —")
proj_view = projects.copy()
proj_view["Budget_Declared"] = money(proj_view["Budget_Declared"])
proj_view["Actual_Spent"]    = money(proj_view["Actual_Spent"])
proj_view["Budget_Gap"]      = money(proj_view["Budget_Gap"])
proj_view["Outcome"]         = proj_view["Outcome"].str.title()
print(proj_view[["Project","Budget_Declared","Actual_Spent","Outcome","Budget_Gap","Ghost_Risk"]].to_string(index=False))

print("\n— Politician Details —")
pol_view = pols.copy()
pol_view["Declared_Income"]  = money(pol_view["Declared_Income"])
pol_view["Project_Spending"] = money(pol_view["Project_Spending"])
pol_view["Spend_to_Income"]  = pol_view["Spend_to_Income"].round(2)
print(pol_view[["Name","Declared_Income","Project_Spending","Spend_to_Income","Overspend_Flag"]].to_string(index=False))

# ---------- save flagged CSVs ----------
projects.to_csv(ROOT / "project_flags.csv", index=False)
pols.to_csv(ROOT / "politician_flags.csv", index=False)
print("\nSaved: project_flags.csv and politician_flags.csv")

# ---------- charts ----------
# 1) Declared vs Actual by project
plt.figure()
ax = projects.set_index("Project")[["Budget_Declared","Actual_Spent"]].plot(kind="bar")
ax.set_ylabel("USD")
ax.set_title("Declared vs Actual Spending by Project")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(ROOT / "declared_vs_actual.png")
plt.close()

# 2) Budget Gap (positive gaps only)
gaps = projects[projects["Budget_Gap"] > 0].set_index("Project")["Budget_Gap"].sort_values()
plt.figure()
ax = gaps.plot(kind="barh")
ax.set_xlabel("USD Gap (Declared - Actual)")
ax.set_title("Projects with Positive Budget Gaps")
plt.tight_layout()
plt.savefig(ROOT / "budget_gaps.png")
plt.close()

print("Saved charts: declared_vs_actual.png, budget_gaps.png")





