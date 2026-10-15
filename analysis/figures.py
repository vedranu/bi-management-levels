#!/usr/bin/env python3
"""
Figures for the paper (PNG, 300 dpi) -> results/figures/
  fig1_levels_stacked.png   perceived contribution by planning level (Yes / Partially / No / N/A)
  fig2_level_purpose_heatmap.png   heatmap: hierarchical level x purpose of BI use (% of respondents at the level)
  fig3_likert_network.png   correlation network of the eight attitude items
Usage: python analysis/figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "survey_clean.csv")
OUT = ROOT / "results" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
N = len(df)

plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9, "axes.edgecolor": "#8a8984",
                     "axes.linewidth": 0.6, "xtick.color": "#52514e", "ytick.color": "#52514e"})
INK, INK2, SURF = "#0b0b0b", "#52514e", "#ffffff"
CAT = {"Operational employee": "#2a78d6", "First-line management": "#eb6834", "Middle management": "#1baf7a",
       "Top management": "#eda100", "Owner / Director": "#e87ba4"}   # validated categorical palette, fixed order
LEVEL_ORDER = list(CAT)

# ------------------------------------------------------------------ Figure 1
items = [
    ("Operational", "op_monitor", "BI tools help monitor daily operational activities"),
    ("Operational", "op_reports", "Operational employees use BI reports for short-term planning"),
    ("Tactical", "tac_dept", "BI assists middle management in analysing departmental performance"),
    ("Tactical", "tac_compare", "BI enables comparison of planned and actual results"),
    ("Tactical", "tac_kpi", "Tactical decisions are based on BI analyses and KPIs"),
    ("Strategic", "str_longterm", "BI supports long-term strategic decision-making"),
    ("Strategic", "str_integrated", "Strategic planning is based on integrated BI reports"),
    ("Strategic", "str_trends", "BI enables better identification of trends and opportunities"),
]
cats = ["Yes", "Partially", "No", "Not applicable"]
cols = {"Yes": "#1f4e8c", "Partially": "#5a8fd0", "No": "#b9c9df", "Not applicable": "#e6e4df"}  # one hue, light->dark + neutral
fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=300)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)
y = np.arange(len(items))[::-1]
lefts = np.zeros(len(items))
for cat in cats:
    vals = np.array([100 * (df[c] == cat).sum() / N for _, c, _ in items])
    bars = ax.barh(y, vals, left=lefts, height=0.62, color=cols[cat], edgecolor=SURF, linewidth=1.2,
                   hatch="///" if cat == "Not applicable" else None, label=cat)
    for yi, v, l in zip(y, vals, lefts):
        if v >= 8:
            ax.text(l + v / 2, yi, f"{v:.0f}", ha="center", va="center", fontsize=7,
                    color="white" if cat in ("Yes", "Partially") else INK2)
    lefts += vals
ax.set_yticks(y)
ax.set_yticklabels([t for _, _, t in items], fontsize=7.5, color=INK)
ax.set_xlim(0, 100)
ax.set_xlabel("Share of respondents (%)", color=INK2)
ax.xaxis.grid(True, color="#e6e4df", linewidth=0.5)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
# level group labels on the right + separators
for lvl, (a, b) in {"Operational": (0, 1), "Tactical": (2, 4), "Strategic": (5, 7)}.items():
    ax.text(102, (y[a] + y[b]) / 2, lvl, rotation=270, ha="left", va="center", fontsize=8, color=INK, clip_on=False)
    if b < 7:
        ax.axhline(y[b] - 0.5, color="#c9c7c0", lw=0.6, xmin=0, xmax=1, clip_on=False)
ax.legend(ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.01), frameon=False, fontsize=7.5, handlelength=1.2)
fig.tight_layout()
fig.savefig(OUT / "fig1_levels_stacked.png", facecolor=SURF)
plt.close(fig)

# ------------------------------------------------------------------ Figure 2
purposes = ["Reporting", "Monitoring business performance", "Operational planning",
            "Business decision-making", "Strategic planning", "Tactical planning"]
rows = []
for lvl, s in zip(df["level"], df["bi_purposes"].fillna("")):
    for p in s.split(";"):
        p = p.strip()
        if p in purposes:
            rows.append((lvl, p))
ct = pd.DataFrame(rows, columns=["level", "purpose"]).groupby(["level", "purpose"]).size().unstack(fill_value=0)
ct = ct.reindex(index=LEVEL_ORDER, columns=purposes, fill_value=0)
n_lvl = df["level"].value_counts()
share = ct.div(n_lvl, axis=0) * 100  # % of respondents at that level naming the purpose

fig, ax = plt.subplots(figsize=(7.0, 3.3), dpi=300)
fig.patch.set_facecolor(SURF)
M = share.loc[LEVEL_ORDER, purposes].values
im = ax.imshow(M, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("blue", ["#f3f6fb", "#1f4e8c"]),
               vmin=0, vmax=100, aspect="auto")
ax.set_xticks(range(len(purposes)))
ax.set_xticklabels(["Reporting", "Performance\nmonitoring", "Operational\nplanning", "Decision-\nmaking",
                    "Strategic\nplanning", "Tactical\nplanning"], fontsize=7.5, color=INK)
ax.set_yticks(range(len(LEVEL_ORDER)))
ax.set_yticklabels([f"{l} (n = {n_lvl[l]})" for l in LEVEL_ORDER], fontsize=7.5, color=INK)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        ax.text(j, i, f"{v:.0f}%", ha="center", va="center", fontsize=7.5,
                color="white" if v >= 55 else INK)
# 2px surface gap between cells
ax.set_xticks(np.arange(-0.5, len(purposes), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(LEVEL_ORDER), 1), minor=True)
ax.grid(which="minor", color=SURF, linewidth=2)
ax.tick_params(which="minor", length=0)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cb.set_label("% of respondents at the level", fontsize=7, color=INK2)
cb.ax.tick_params(labelsize=6.5, colors=INK2)
cb.outline.set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "fig2_level_purpose_heatmap.png", facecolor=SURF)
plt.close(fig)
share.round(1).to_csv(OUT / "fig2_data_share_by_level.csv")

# ------------------------------------------------------------------ Figure 3
lik = {
    "lik_data_driven": "Data over\nintuition", "lik_changed_planning": "BI changed\nplanning",
    "lik_lack_knowledge": "Lack of\nknowledge", "lik_resistance": "Resistance\nto change",
    "lik_advantage": "Competitive\nadvantage", "lik_quality": "Planning\nquality",
    "lik_faster": "Faster\ndecisions", "lik_future": "Future role\nof BI",
}
barrier = {"lik_lack_knowledge", "lik_resistance"}
C = df[list(lik)].corr(method="spearman")
G = nx.Graph()
for k in lik:
    G.add_node(k)
for a in lik:
    for b in lik:
        if a < b and abs(C.loc[a, b]) >= 0.30:
            G.add_edge(a, b, w=C.loc[a, b])
order = ["lik_future", "lik_quality", "lik_faster", "lik_advantage", "lik_data_driven", "lik_changed_planning",
         "lik_resistance", "lik_lack_knowledge"]
ang = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, len(order), endpoint=False)
pos = {k: np.array([np.cos(t), np.sin(t)]) for k, t in zip(order, ang)}
fig, ax = plt.subplots(figsize=(6.4, 5.4), dpi=300)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)
ax.axis("off")
ax.set_aspect("equal")
for a_, b_, d in sorted(G.edges(data=True), key=lambda e: abs(e[2]["w"])):
    strong = abs(d["w"]) >= 0.5
    ax.plot([pos[a_][0], pos[b_][0]], [pos[a_][1], pos[b_][1]], color="#52514e" if strong else "#b9b7b0",
            lw=0.6 + 7 * (abs(d["w"]) - 0.28), alpha=0.9, zorder=1, solid_capstyle="round")
    if strong:
        mx, my = (pos[a_][0] + pos[b_][0]) / 2, (pos[a_][1] + pos[b_][1]) / 2
        ax.text(mx, my, f"{d['w']:.2f}", fontsize=6.5, color=INK, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc=SURF, ec="none", alpha=0.9), zorder=2)
for k in lik:
    m = df[k].mean()
    ax.scatter(*pos[k], s=140 + 160 * (m - 3), color="#eb6834" if k in barrier else "#2a78d6",
               edgecolor=SURF, linewidth=1.5, zorder=3)
    lx, ly = pos[k] * 1.3
    ha = "center" if abs(lx) < 0.3 else ("left" if lx > 0 else "right")
    va = "center" if abs(ly) < 0.3 else ("bottom" if ly > 0 else "top")
    ax.text(lx, ly, f"{lik[k]}\nM = {m:.2f}", ha=ha, va=va, fontsize=7, color=INK, zorder=4)
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-1.75, 1.75)
ax.scatter([], [], color="#2a78d6", label="Benefit items")
ax.scatter([], [], color="#eb6834", label="Barrier items")
ax.legend(loc="upper left", frameon=False, fontsize=7.5)
ax.text(0.5, 0.0, "Edges: Spearman's ρ ≥ 0.30; dark edges and labels: ρ ≥ 0.50 (width proportional to ρ). Node size proportional to item mean.",
        transform=ax.transAxes, ha="center", fontsize=6.3, color=INK2)
fig.tight_layout()
fig.savefig(OUT / "fig3_likert_network.png", facecolor=SURF)
plt.close(fig)
C.round(2).to_csv(OUT / "fig3_data_spearman_matrix.csv")
print("figures written to", OUT)
print(share.round(1))
print(C.round(2))
