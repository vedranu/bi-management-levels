#!/usr/bin/env python3
"""
Cleans the raw Google Forms export (bilingual labels, free-text country/sector)
into an anonymised, English-coded dataset.

Input : data/raw/survey_raw.csv   (Google Forms export, timestamps removed)
Output: data/survey_clean.csv

Usage : python analysis/prepare_data.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "survey_raw.csv"
OUT = ROOT / "data" / "survey_clean.csv"

df = pd.read_csv(RAW)
if "Vremenska oznaka" in df.columns:
    df = df.drop(columns=["Vremenska oznaka"])

cols = list(df.columns)
names = ["gender", "age", "education", "experience", "level", "sector", "country",
         "org_uses_bi", "bi_tools", "bi_purposes", "bi_frequency",
         "plan_data_prep", "plan_time", "plan_efficiency", "plan_coordination", "plan_investment",
         "op_monitor", "op_reports",
         "tac_dept", "tac_compare", "tac_kpi",
         "str_longterm", "str_integrated", "str_trends",
         "lik_data_driven", "lik_changed_planning", "lik_lack_knowledge", "lik_resistance",
         "lik_advantage", "lik_quality", "lik_faster", "lik_future"]
assert len(cols) == len(names), f"expected {len(names)} columns, got {len(cols)}"
df.columns = names


def en(s):
    """Keep the English half of a 'Croatian / English' label."""
    if pd.isna(s):
        return s
    return str(s).split("/")[-1].strip()


for c in ["gender", "age", "education", "experience", "org_uses_bi", "bi_frequency"]:
    df[c] = df[c].map(en)

level_map = {
    "Operativni zaposlenik / Operational employee": "Operational employee",
    "Operativni menadžment / Supervisor / Team leader": "First-line management",
    "Srednji menadžment / Middle management": "Middle management",
    "Viši menadžment / Top management": "Top management",
    "Vlasnik / direktor / Owner / Director": "Owner / Director",
}
df["level"] = df["level"].map(level_map)

sector_map = {
    "Turizam i ugostiteljstvo / Tourism & hospitality": "Tourism & hospitality",
    "IT / Information Technology": "Information technology",
    "Zdravstvo / Healthcare": "Healthcare",
    "Healtcare industry": "Healthcare",
    "Clinical Trials": "Healthcare",
    "Financijske usluge / Financial services": "Financial services",
    "Obrazovanje / Education": "Education",
    "Trgovina / Trade (wholesale/retail)": "Trade",
    "Logistika i transport / Logistics & transport": "Logistics & transport",
    "Proizvodnja / Manufacturing": "Manufacturing",
    "Javni sektor / Public sector": "Public sector",
    "Ngo": "Non-governmental organisation",
    "Ribarstvo": "Fisheries",
}
df["sector"] = df["sector"].map(sector_map).fillna(df["sector"])

country_map = {
    "hrvatska": "Croatia", "croatia": "Croatia",
    "spain": "Spain", "in spain": "Spain", "spanjolska": "Spain",
    "greece": "Greece", "norway": "Norway",
    "serbia": "Serbia", "srbija": "Serbia",
    "njemačka": "Germany", "hong kong": "Hong Kong", "doha qatar": "Qatar",
    "france": "France",
}
df["country"] = (df["country"].astype(str).str.strip().str.lower()
                 .map(country_map).fillna("Not stated"))

tri = {"Da / Yes": "Yes", "Ne / No": "No", "Djelomično / Partially": "Partially", "NP / NA": "Not applicable"}
for c in names[11:24]:
    df[c] = df[c].map(tri)

df["bi_tools"] = df["bi_tools"].map(lambda s: s if pd.isna(s) else ";".join(
    en(x) if "/" in x and "SAP" not in x else x.strip() for x in str(s).split(";")))
df["bi_purposes"] = df["bi_purposes"].map(lambda s: s if pd.isna(s) else ";".join(
    en(x) if "/" in x else ("Do not use" if x.strip().lower().startswith(("ne ", "not", "nisam")) else x.strip())
    for x in str(s).split(";")))

OUT.parent.mkdir(exist_ok=True)
df.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(df)} rows, {df.shape[1]} columns)")
