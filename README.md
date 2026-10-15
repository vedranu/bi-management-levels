# Business Intelligence Across Hierarchical Levels of Management

Reproducible research package for the paper

> Jurić Gubeljić, S., Uroš, V., & Martinović, A. (2026). *Business intelligence across hierarchical levels of management: Perceived contribution to business planning and the human factor.* Manuscript submitted to EMC Review - Economy and Market Communication Review.

The paper is based on a survey of 53 employees at five hierarchical levels (operational employees, first-line, middle and top management, owners/directors) in organisations from eleven industries, mostly in Croatia and nine other countries, carried out February-June 2026.

## Repository structure

```
.
├── analysis/
│   ├── prepare_data.py      # cleans the raw Google Forms export -> data/survey_clean.csv
│   ├── analyze.py           # all statistics reported in the paper -> results/
│   └── figures.py           # Figures 1-3 of the paper -> results/figures/ (PNG, 300 dpi)
├── data/
│   ├── raw/survey_raw.csv   # anonymised Google Forms export (bilingual labels, timestamps removed)
│   ├── survey_clean.csv     # English-coded analysis dataset (53 x 32)
│   └── codebook.md          # variable names, question wording, coding
├── results/
│   ├── table1_sample.csv ... table13_croatia_vs_other.csv, tableA1_spearman_matrix.csv
│   ├── figures/             # fig1_levels_stacked, fig2_level_purpose_heatmap, fig3_likert_network (+ data)
│   ├── summary.json         # reliability, correlations, group sizes
│   └── results.md           # all tables in one Markdown report
├── references/
│   ├── references.bib       # BibTeX (import into Zotero / JabRef / Word)
│   ├── references.ris       # RIS (import into Mendeley / EndNote / Word "References")
│   └── references_apa.txt   # APA 7 reference list as used in the paper
├── questionnaire/
│   └── questionnaire_hr_en.md   # the survey instrument (Croatian / English)
├── requirements.txt
├── LICENSE
└── README.md
```

## Reproducing the analysis

```bash
pip install -r requirements.txt
python analysis/prepare_data.py   # writes data/survey_clean.csv
python analysis/analyze.py        # writes results/*.csv, results/results.md, results/summary.json
python analysis/figures.py        # writes results/figures/*.png
```

Tested with Python 3.11+, pandas 2.x, SciPy 1.11+, tabulate, matplotlib 3.x, networkx 3.x.

## Hypotheses and tests

| Hypothesis | Test | Output |
|---|---|---|
| H1a Share of respondents able to assess BI declines from operational to strategic level | Cochran's Q on "able to judge" (no N/A in the level block) + exact McNemar pairs; N/A share by group (Fisher) | `table10_H1a_H1b_tests.csv`, `table5b_na_by_level.csv`, `table5c_na_by_group.csv` |
| H1b Among those able to assess, perceived contribution declines with level | Friedman test on per-respondent level scores (Yes = 2, Partially = 1, No = 0, N/A excluded) + pairwise Wilcoxon | `table4_levels.csv`, `table5_H1_level_gradient.csv`, `table10_H1a_H1b_tests.csv` |
| H2 Managers rate BI contribution higher than operational staff | Primary: Mann-Whitney U on the BI benefit index (6 Likert items), rank-biserial r, Kruskal-Wallis (5 levels), post-hoc power; item-level U tests with Holm correction; sensitivity for users/non-users; Croatia vs other | `table7_indices_H2_H3.csv`, `table6_likert.csv`, `table11_H2_holm.csv`, `table12_users_sensitivity.csv`, `table13_croatia_vs_other.csv`, `summary.json` |
| H3 Human factors are a barrier independent of hierarchical level | Same tests on the human-factor barrier index (2 Likert items); Spearman ρ with frequency of use | `table7_indices_H2_H3.csv`, `summary.json` |

Reliability: Cronbach's α = 0.83 (8 Likert items), 0.85 (6 benefit items); two barrier items: inter-item r = 0.61, Spearman-Brown = 0.76.

## Data and ethics

Participation was voluntary and anonymous. The raw export contains no names, e-mail addresses or IP addresses; the submission timestamps were removed before publication. Free-text answers (country, sector, "other" tools) are kept as entered.

## Citation

A Zenodo DOI will be added on acceptance of the paper.

### BibTeX / RIS

See `references/`.

If you use the data or code, please cite the paper above and this repository.

## License

Code: MIT License. Data and text: CC BY 4.0.
