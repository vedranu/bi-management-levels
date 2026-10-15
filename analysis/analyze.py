#!/usr/bin/env python3
"""
Reproducible analysis for:
"Business Intelligence Across Hierarchical Levels of Management:
 Perceived Contribution to Business Planning and the Human Factor"

Input : data/survey_clean.csv  (produced by prepare_data.py)
Output: results/*.csv, results/results.md

Usage : python analysis/analyze.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "survey_clean.csv"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
N = len(df)
md = []  # markdown report lines


def pct(x, n=N):
    return f"{100 * x / n:.1f}"


def save(name, frame):
    frame.to_csv(OUT / f"{name}.csv", index=False)
    md.append(f"\n### {name}\n")
    md.append(frame.to_markdown(index=False))


# ---------------------------------------------------------------- 1. Sample
rows = []
for var, label in [("gender", "Gender"), ("age", "Age"), ("education", "Education"),
                   ("experience", "Work experience"), ("level", "Hierarchical level"),
                   ("sector", "Industry sector"), ("country", "Country of office")]:
    vc = df[var].value_counts(dropna=False)
    for k, v in vc.items():
        rows.append({"Variable": label, "Category": k, "n": v, "%": pct(v)})
save("table1_sample", pd.DataFrame(rows))

# ---------------------------------------------------------------- 2. BI use
rows = []
for k, v in df["org_uses_bi"].value_counts().items():
    rows.append({"Item": "Organisation uses BI tools", "Category": k, "n": v, "%": pct(v)})
for k, v in df["bi_frequency"].value_counts().items():
    rows.append({"Item": "Personal frequency of BI use", "Category": k, "n": v, "%": pct(v)})
tools = df["bi_tools"].fillna("").str.split(";").explode().str.strip()
tools = tools[tools != ""].value_counts()
for k, v in tools.items():
    rows.append({"Item": "BI tools used (multiple)", "Category": k, "n": v, "%": pct(v)})
purp = df["bi_purposes"].fillna("").str.split(";").explode().str.strip()
purp = purp[purp != ""].value_counts()
for k, v in purp.items():
    rows.append({"Item": "Purpose of BI use (multiple)", "Category": k, "n": v, "%": pct(v)})
save("table2_bi_use", pd.DataFrame(rows))

# ---------------------------------------------------------------- 3. Planning contribution (Yes/Partially/No)
plan_items = {
    "plan_data_prep": "BI tools enable better data preparation for planning",
    "plan_time": "BI tools reduce the time to prepare plans and analyses",
    "plan_efficiency": "BI systems increase business efficiency",
    "plan_coordination": "BI tools improve coordination between management levels",
    "plan_investment": "BI implementation requires significant financial investment",
}
rows = []
for col, lab in plan_items.items():
    vc = df[col].value_counts()
    rows.append({"Statement": lab,
                 "Yes n": vc.get("Yes", 0), "Yes %": pct(vc.get("Yes", 0)),
                 "Partially n": vc.get("Partially", 0), "Partially %": pct(vc.get("Partially", 0)),
                 "No n": vc.get("No", 0), "No %": pct(vc.get("No", 0))})
save("table3_planning_contribution", pd.DataFrame(rows))

# ---------------------------------------------------------------- 4. Level-specific items
level_items = {
    "Operational": {
        "op_monitor": "BI tools help monitor daily operational activities",
        "op_reports": "Operational employees use BI reports for short-term planning",
    },
    "Tactical": {
        "tac_dept": "BI tools assist middle management in analysing departmental performance",
        "tac_compare": "BI systems enable comparison of planned and actual results",
        "tac_kpi": "Tactical decisions are based on BI analyses and KPIs",
    },
    "Strategic": {
        "str_longterm": "BI systems support long-term strategic decision-making",
        "str_integrated": "Strategic planning is based on integrated BI reports",
        "str_trends": "BI tools enable better identification of trends and opportunities",
    },
}
rows = []
for lvl, items in level_items.items():
    for col, lab in items.items():
        vc = df[col].value_counts()
        valid = N - vc.get("Not applicable", 0)
        rows.append({"Level": lvl, "Statement": lab,
                     "Yes %": pct(vc.get("Yes", 0)), "Partially %": pct(vc.get("Partially", 0)),
                     "No %": pct(vc.get("No", 0)), "NA %": pct(vc.get("Not applicable", 0)),
                     "Yes % of valid": f"{100 * vc.get('Yes', 0) / valid:.1f}",
                     "Valid n": valid})
save("table4_levels", pd.DataFrame(rows))

# H1: per-respondent level score (Yes=2, Partially=1, No=0; NA excluded)
code = {"Yes": 2, "Partially": 1, "No": 0}
lvl_scores = pd.DataFrame({
    lvl: df[list(items)].replace(code).apply(pd.to_numeric, errors="coerce").mean(axis=1)
    for lvl, items in level_items.items()
})
complete = lvl_scores.dropna()
fried = stats.friedmanchisquare(complete["Operational"], complete["Tactical"], complete["Strategic"])
w_ot = stats.wilcoxon(complete["Operational"], complete["Tactical"])
w_os = stats.wilcoxon(complete["Operational"], complete["Strategic"])
w_ts = stats.wilcoxon(complete["Tactical"], complete["Strategic"])
kendall_w = fried.statistic / (len(complete) * (3 - 1))
h1 = pd.DataFrame([{
    "n (complete cases)": len(complete),
    "Mean score Operational": round(complete["Operational"].mean(), 2),
    "Mean score Tactical": round(complete["Tactical"].mean(), 2),
    "Mean score Strategic": round(complete["Strategic"].mean(), 2),
    "Friedman chi2": round(fried.statistic, 2), "Friedman p": round(fried.pvalue, 4),
    "Kendall W": round(kendall_w, 3),
    "Wilcoxon Op vs Tac p": round(w_ot.pvalue, 4),
    "Wilcoxon Op vs Str p": round(w_os.pvalue, 4),
    "Wilcoxon Tac vs Str p": round(w_ts.pvalue, 4),
}])
save("table5_H1_level_gradient", h1)

# NA share per level (also relevant to H1 / visibility)
na_share = pd.DataFrame([{
    "Level": lvl,
    "Mean NA %": round(100 * (df[list(items)] == "Not applicable").mean().mean(), 1),
    "Mean Yes %": round(100 * (df[list(items)] == "Yes").mean().mean(), 1),
} for lvl, items in level_items.items()])
save("table5b_na_by_level", na_share)


# NA share by respondent group (management vs operational) per level block
rows = []
for lvl, items in level_items.items():
    na = (df[list(items)] == "Not applicable").any(axis=1)
    ct = pd.crosstab(df["level"].isin(["Middle management", "Top management", "Owner / Director"]), na)
    fe = stats.fisher_exact(ct.values) if ct.shape == (2, 2) else (np.nan, np.nan)
    rows.append({"Level": lvl,
                 "Any NA, management %": round(100 * na[df["level"].isin(["Middle management", "Top management", "Owner / Director"])].mean(), 1),
                 "Any NA, operational/first-line %": round(100 * na[~df["level"].isin(["Middle management", "Top management", "Owner / Director"])].mean(), 1),
                 "Fisher p": round(float(fe[1]), 3)})
save("table5c_na_by_group", pd.DataFrame(rows))

# ---------------------------------------------------------------- 5. Likert items
likert = {
    "lik_data_driven": "Decisions in my organisation are increasingly based on data rather than intuition",
    "lik_changed_planning": "BI has changed the way business planning is conducted in my organisation",
    "lik_lack_knowledge": "Lack of employee knowledge makes the use of BI tools more difficult",
    "lik_resistance": "Employee resistance to change is a barrier to BI adoption",
    "lik_advantage": "Organisations that use BI systems have a competitive advantage",
    "lik_quality": "BI improves planning quality through better data preparation and plan accuracy",
    "lik_faster": "BI tools enable faster and higher-quality decisions across hierarchical levels",
    "lik_future": "The role of BI in business planning will further increase in the future",
}
L = df[list(likert)].astype(float)


def cronbach(frame):
    k = frame.shape[1]
    return k / (k - 1) * (1 - frame.var(ddof=1).sum() / frame.sum(axis=1).var(ddof=1))


benefit_cols = ["lik_data_driven", "lik_changed_planning", "lik_advantage",
                "lik_quality", "lik_faster", "lik_future"]
barrier_cols = ["lik_lack_knowledge", "lik_resistance"]
alpha_all = cronbach(L)
alpha_benefit = cronbach(L[benefit_cols])
df["benefit_index"] = L[benefit_cols].mean(axis=1)
df["barrier_index"] = L[barrier_cols].mean(axis=1)

mgmt_levels = ["Middle management", "Top management", "Owner / Director"]
df["group"] = np.where(df["level"].isin(mgmt_levels), "Management", "Operational / first-line")
is_m = df["group"] == "Management"
uses = df["org_uses_bi"] == "Yes"


def rank_biserial(a, b):
    u = stats.mannwhitneyu(a, b).statistic
    return 1 - 2 * u / (len(a) * len(b))


rows = []
for col, lab in likert.items():
    x = L[col]
    mw_g = stats.mannwhitneyu(x[is_m], x[~is_m])
    mw_u = stats.mannwhitneyu(x[uses], x[~uses])
    kw = stats.kruskal(*[x[df["level"] == g] for g in df["level"].unique()])
    rows.append({
        "Statement": lab,
        "Mean": round(x.mean(), 2), "SD": round(x.std(ddof=1), 2), "Median": x.median(),
        "Agree (4-5) %": pct((x >= 4).sum()),
        "Mean mgmt": round(x[is_m].mean(), 2), "Mean oper": round(x[~is_m].mean(), 2),
        "MW p (mgmt vs oper)": round(mw_g.pvalue, 3),
        "r (rank-biserial)": round(rank_biserial(x[is_m], x[~is_m]), 2),
        "KW p (5 levels)": round(kw.pvalue, 3),
        "Mean BI users": round(x[uses].mean(), 2), "Mean non-users": round(x[~uses].mean(), 2),
        "MW p (users vs non)": round(mw_u.pvalue, 3),
    })
tab6 = pd.DataFrame(rows)
save("table6_likert", tab6)

# composite indices
rows = []
for idx, lab in [("benefit_index", "BI benefit index (6 items)"), ("barrier_index", "Human-factor barrier index (2 items)")]:
    x = df[idx]
    mw_g = stats.mannwhitneyu(x[is_m], x[~is_m])
    mw_u = stats.mannwhitneyu(x[uses], x[~uses])
    kw = stats.kruskal(*[x[df["level"] == g] for g in df["level"].unique()])
    rows.append({"Index": lab, "Mean": round(x.mean(), 2), "SD": round(x.std(ddof=1), 2),
                 "Mean mgmt": round(x[is_m].mean(), 2), "Mean oper": round(x[~is_m].mean(), 2),
                 "MW p (mgmt vs oper)": round(mw_g.pvalue, 3),
                 "r": round(rank_biserial(x[is_m], x[~is_m]), 2),
                 "KW p (5 levels)": round(kw.pvalue, 3),
                 "Mean BI users": round(x[uses].mean(), 2), "Mean non-users": round(x[~uses].mean(), 2),
                 "MW p (users vs non)": round(mw_u.pvalue, 3)})
save("table7_indices_H2_H3", pd.DataFrame(rows))

# means by 5 levels
by_level = df.groupby("level")[list(likert) + ["benefit_index", "barrier_index"]].mean().round(2).reset_index()
by_level["n"] = df.groupby("level").size().values
save("table8_means_by_level", by_level)

# BI use by level (crosstab)
ct = pd.crosstab(df["level"], df["org_uses_bi"]).reset_index()
save("table9_bi_use_by_level", ct)

# Spearman: benefit index vs frequency of use
freq_code = {"Never": 0, "Rarely": 1, "Occasionally": 2, "Frequently": 3, "Daily": 4}
f = df["bi_frequency"].map(freq_code)
rho = stats.spearmanr(f, df["benefit_index"])
rho_b = stats.spearmanr(f, df["barrier_index"])

summary = {
    "N": int(N),
    "cronbach_alpha_8_items": round(float(alpha_all), 3),
    "cronbach_alpha_6_benefit_items": round(float(alpha_benefit), 3),
    "cronbach_alpha_2_barrier_items": round(float(cronbach(L[barrier_cols])), 3),
    "spearman_frequency_vs_benefit": {"rho": round(float(rho.statistic), 3), "p": round(float(rho.pvalue), 4)},
    "spearman_frequency_vs_barrier": {"rho": round(float(rho_b.statistic), 3), "p": round(float(rho_b.pvalue), 4)},
    "n_management": int(is_m.sum()), "n_operational": int((~is_m).sum()),
    "n_bi_users": int(uses.sum()),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
md.insert(0, "# Results\n\n```json\n" + json.dumps(summary, indent=2) + "\n```")
(OUT / "results.md").write_text("\n".join(md), encoding="utf-8")
print(json.dumps(summary, indent=2))
print(h1.T)
print(tab6[["Statement", "Mean", "SD", "MW p (mgmt vs oper)", "MW p (users vs non)"]])

# ---------------------------------------------------------------- Revision round 1 additions
from itertools import combinations

# H1a: share of respondents able to judge (no N/A in the level block) by level; Cochran's Q + exact McNemar
able = pd.DataFrame({lvl: (~(df[list(items)] == "Not applicable").any(axis=1)).astype(int)
                     for lvl, items in level_items.items()})
X = able.values
k = X.shape[1]
Tj, Ti, T = X.sum(0), X.sum(1), X.sum()
Q = (k - 1) * (k * np.sum(Tj ** 2) - T ** 2) / (k * T - np.sum(Ti ** 2))
rows = [{"Test": "Cochran's Q (able to judge, 3 levels)", "Statistic": round(float(Q), 2), "df": 2,
         "p": round(float(1 - stats.chi2.cdf(Q, k - 1)), 4),
         "Note": "; ".join(f"{l}: {100 * able[l].mean():.1f}% able to judge" for l in able)}]
for a, b in combinations(able.columns, 2):
    n01 = int(((able[a] == 1) & (able[b] == 0)).sum())
    n10 = int(((able[a] == 0) & (able[b] == 1)).sum())
    p = stats.binomtest(min(n01, n10), n01 + n10).pvalue if n01 + n10 else 1.0
    rows.append({"Test": f"Exact McNemar {a} vs {b}", "Statistic": f"discordant {n01}/{n10}", "df": "",
                 "p": round(float(p), 3), "Note": ""})
# H1b: Wilcoxon pairs with statistics
for a, b in combinations(complete.columns, 2):
    w = stats.wilcoxon(complete[a], complete[b])
    rows.append({"Test": f"Wilcoxon signed-rank {a} vs {b} (valid cases)", "Statistic": round(float(w.statistic), 1),
                 "df": "", "p": round(float(w.pvalue), 3), "Note": f"n = {len(complete)}"})
save("table10_H1a_H1b_tests", pd.DataFrame(rows))

# H2: Holm correction over the eight item-level Mann-Whitney tests; KW with H and df
pvals = tab6["MW p (mgmt vs oper)"].values.astype(float)
order = np.argsort(pvals)
holm = np.empty_like(pvals)
prev = 0.0
for rank, i in enumerate(order):
    prev = max(prev, (len(pvals) - rank) * pvals[i])
    holm[i] = min(prev, 1.0)
tab6h = tab6[["Statement", "MW p (mgmt vs oper)"]].copy()
tab6h["Holm-adjusted p"] = holm.round(3)
tab6h["KW H(4)"] = [round(float(stats.kruskal(*[L.loc[df["level"] == g, c] for g in df["level"].unique()]).statistic), 2) for c in likert]
save("table11_H2_holm", tab6h)

# Power for the composite effect (rank-biserial r treated as a correlation; Fisher z approximation)
r_obs = abs(rank_biserial(df.loc[is_m, "benefit_index"], df.loc[~is_m, "benefit_index"]))
z = np.arctanh(r_obs)
power = float(stats.norm.cdf(z * np.sqrt(N - 3) - stats.norm.ppf(0.975)))
n_req = float(((stats.norm.ppf(0.975) + stats.norm.ppf(0.80)) / z) ** 2 + 3)
u_b = stats.mannwhitneyu(df.loc[is_m, "benefit_index"], df.loc[~is_m, "benefit_index"])
u_r = stats.mannwhitneyu(df.loc[is_m, "barrier_index"], df.loc[~is_m, "barrier_index"])
kw_b = stats.kruskal(*[df.loc[df["level"] == g, "benefit_index"] for g in df["level"].unique()])
kw_r = stats.kruskal(*[df.loc[df["level"] == g, "barrier_index"] for g in df["level"].unique()])
summary.update({
    "H2_benefit_index": {"U": float(u_b.statistic), "p": round(float(u_b.pvalue), 3), "r": round(r_obs, 2),
                         "KW_H": round(float(kw_b.statistic), 2), "KW_df": 4, "KW_p": round(float(kw_b.pvalue), 3),
                         "post_hoc_power_approx": round(power, 2), "n_required_80pct_power": int(np.ceil(n_req))},
    "H3_barrier_index": {"U": float(u_r.statistic), "p": round(float(u_r.pvalue), 3),
                         "KW_H": round(float(kw_r.statistic), 2), "KW_df": 4, "KW_p": round(float(kw_r.pvalue), 3)},
})

# BI users vs non-users: definition and sensitivity (No + Not sure vs No only)
rows = []
for lab, non in [("Non-users = No + Not sure (n=17)", df["org_uses_bi"] != "Yes"), ("Non-users = No only (n=10)", df["org_uses_bi"] == "No")]:
    for idx in ("benefit_index", "barrier_index"):
        a, b = df.loc[uses, idx], df.loc[non, idx]
        u = stats.mannwhitneyu(a, b)
        rows.append({"Definition": lab, "Index": idx, "Mean users": round(a.mean(), 2), "Mean non-users": round(b.mean(), 2),
                     "U": float(u.statistic), "p": round(float(u.pvalue), 3), "r": round(abs(rank_biserial(a, b)), 2)})
save("table12_users_sensitivity", pd.DataFrame(rows))
save("table12b_use_by_frequency", pd.crosstab(df["org_uses_bi"], df["bi_frequency"]).reset_index())

# Robustness: Croatia vs other countries
hr = df["country"] == "Croatia"
rows = []
for idx in ("benefit_index", "barrier_index"):
    u = stats.mannwhitneyu(df.loc[hr, idx], df.loc[~hr, idx])
    rows.append({"Index": idx, "Croatia M (n=30)": round(df.loc[hr, idx].mean(), 2), "Other M (n=23)": round(df.loc[~hr, idx].mean(), 2),
                 "U": float(u.statistic), "p": round(float(u.pvalue), 3)})
u = stats.mannwhitneyu(df.loc[hr & is_m, "benefit_index"], df.loc[hr & ~is_m, "benefit_index"])
rows.append({"Index": "benefit_index, management vs operational within Croatia", "Croatia M (n=30)": round(df.loc[hr & is_m, "benefit_index"].mean(), 2),
             "Other M (n=23)": round(df.loc[hr & ~is_m, "benefit_index"].mean(), 2), "U": float(u.statistic), "p": round(float(u.pvalue), 3)})
save("table13_croatia_vs_other", pd.DataFrame(rows))

# Two-item barrier scale: inter-item correlation and Spearman-Brown
rp = float(L[barrier_cols].corr().iloc[0, 1])
summary["barrier_items_pearson_r"] = round(rp, 3)
summary["barrier_items_spearman_brown"] = round(2 * rp / (1 + rp), 3)
summary["barrier_items_spearman_rho"] = round(float(L[barrier_cols].corr(method="spearman").iloc[0, 1]), 3)

# Full Spearman matrix of the eight items (appendix)
save("tableA1_spearman_matrix", L.corr(method="spearman").round(2).rename(columns=lambda c: c.replace("lik_", "")).reset_index().rename(columns={"index": "item"}))
(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
md[0] = "# Results\n\n```json\n" + json.dumps(summary, indent=2) + "\n```"
(OUT / "results.md").write_text("\n".join(md), encoding="utf-8")
print(json.dumps(summary, indent=2))
