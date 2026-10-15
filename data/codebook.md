# Codebook

Dataset: `data/survey_clean.csv` (53 respondents x 32 variables). Column order follows the questionnaire.

| # | Variable | Question (HR / EN) | Coding / values |
|---|---|---|---|
| 1 | `gender` | Spol ?/ Gender? | Female, Male |
| 2 | `age` | Dob ?/ Age? | 26–35 years, 36–45 years, 46–55 years, 56 and above |
| 3 | `education` | Najviši stupanj obrazovanja ? / Highest level of education? | Bachelor’s degree, High school, Master’s degree, Postgraduate degree, Specialized in nautical industry |
| 4 | `experience` | Koliko godina radnog iskustva imate ?/ How many years of work experience do you have? | 11–20 years, 6–10 years, More than 20 years, up to 5 years |
| 5 | `level` | Na kojoj se hijerarhijskoj razini u organizaciji trenutno nalazite? / What hierarchical level do you currently hold within your organization? | First-line management, Middle management, Operational employee, Owner / Director, Top management |
| 6 | `sector` | U kojoj djelatnosti (industrijskom sektoru) posluje organizacija u kojoj radite?/ In which industry sector does your organization operate? | free text, recoded |
| 7 | `country` | U kojoj državi se nalazi Vaš ured? / In which country is your office located? | free text, recoded |
| 8 | `org_uses_bi` | Koristi li Vaša organizacija BI alate? / Does your organization use BI tools? | No, Not sure, Yes |
| 9 | `bi_tools` | Koje BI alate ili analitička rješenja koristite u poslovanju (moguće više odgovora) ?/ Which BI tools or analytical solutions are used in your organization? (Multiple answers possible) | multiple answers separated by ';' |
| 10 | `bi_purposes` | U koju svrhu najčešće koristite BI alate (moguće više odgovora) ?/ For what purposes are BI tools most frequently used? (Multiple answers possible) | multiple answers separated by ';' |
| 11 | `bi_frequency` | Koliko često koristite BI alate u planiranju i praćenju ciljeva?/ How frequently do you use BI tools for planning and performance monitoring? | Daily, Frequently, Never, Occasionally, Rarely |
| 12 | `plan_data_prep` | BI alati omogućuju bolju pripremu podataka za poslovno planiranje? / BI tools enable better data preparation for business planning? | No, Partially, Yes |
| 13 | `plan_time` | BI alati skraćuju vrijeme izrade planova i analiza? / BI tools reduce the time required to prepare plans and analyses? | No, Partially, Yes |
| 14 | `plan_efficiency` | Korištenje BI sustava doprinosi povećanju učinkovitosti poslovanja?/ The use of BI systems contributes to increased business efficiency? | No, Partially, Yes |
| 15 | `plan_coordination` | BI alati poboljšavaju koordinaciju između različitih razina upravljanja? / BI tools improve coordination between different management levels? | No, Partially, Yes |
| 16 | `plan_investment` | Implementacija BI sustava zahtijeva značajna financijska ulaganja? / The implementation of BI systems requires significant financial investment? | No, Partially, Yes |
| 17 | `op_monitor` | BI alati pomažu u praćenju svakodnevnih operativnih aktivnosti? / BI tools help monitor daily operational activities? | No, Not applicable, Partially, Yes |
| 18 | `op_reports` | Operativni zaposlenici koriste BI izvještaje za kratkoročno planiranje?/ Operational employees use BI reports for short-term planning? | No, Not applicable, Partially, Yes |
| 19 | `tac_dept` | BI alati pomažu srednjem menadžmentu u analizi performansi odjela? / BI tools assist middle management in analyzing departmental performance? | No, Not applicable, Partially, Yes |
| 20 | `tac_compare` | BI sustavi omogućuju usporedbu planiranih i ostvarenih rezultata? / BI systems enable comparison between planned and actual results? | No, Not applicable, Partially, Yes |
| 21 | `tac_kpi` | Taktičke odluke temelje se na BI analizama i pokazateljima uspješnosti (KPI)?/ Tactical decisions are based on BI analyses and key performance indicators (KPIs)? | No, Not applicable, Partially, Yes |
| 22 | `str_longterm` | BI sustavi podržavaju donošenje dugoročnih strateških odluka? / BI systems support long-term strategic decision-making? | No, Not applicable, Partially, Yes |
| 23 | `str_integrated` | Strateško planiranje u poduzeću temelji se na integriranim BI izvještajima? / Strategic planning in the organization is based on integrated BI reports? | No, Not applicable, Partially, Yes |
| 24 | `str_trends` | BI alati omogućuju bolje prepoznavanje trendova i budućih prilika? / BI tools enable better identification of trends and future opportunities? | No, Not applicable, Partially, Yes |
| 25 | `lik_data_driven` | Poslovne odluke u mojoj organizaciji sve se više temelje na analizi podataka, a ne na intuiciji / Business decisions in my organization are increasingly based on data analysis rather than intuition. | 1 = strongly disagree ... 5 = strongly agree |
| 26 | `lik_changed_planning` | Primjena BI-ja promijenila je način poslovnog planiranja u organizaciji kojoj pripadam. / The implementation of BI has changed the way business planning is conducted in my organization. | 1 = strongly disagree ... 5 = strongly agree |
| 27 | `lik_lack_knowledge` | Nedostatak znanja zaposlenika otežava korištenje BI alata./ Lack of employee knowledge makes the use of BI tools more difficult. | 1 = strongly disagree ... 5 = strongly agree |
| 28 | `lik_resistance` | Otpor zaposlenika prema promjenama predstavlja prepreku korištenju BI-a./ Employee resistance to change represents a barrier to BI adoption. | 1 = strongly disagree ... 5 = strongly agree |
| 29 | `lik_advantage` | Poduzeće koje koristi BI sustave ima konkurentsku prednost./ Organizations that use BI systems have a competitive advantage. | 1 = strongly disagree ... 5 = strongly agree |
| 30 | `lik_quality` | Korištenje BI sustava poboljšava kvalitetu poslovnog planiranja kroz bolju pripremu podataka i veću točnost planova./ The use of BI systems improves the quality of business planning through better data preparation and greater plan accuracy. | 1 = strongly disagree ... 5 = strongly agree |
| 31 | `lik_faster` | BI alati omogućuju brže i kvalitetnije donošenje odluka na različitim hijerarhijskim razinama./ BI tools enable faster and higher-quality decision-making across different hierarchical levels. | 1 = strongly disagree ... 5 = strongly agree |
| 32 | `lik_future` | Uloga poslovne inteligencije u poslovnom planiranju u budućnosti će se dodatno povećavati./ The role of Business Intelligence in business planning will further increase in the future. | 1 = strongly disagree ... 5 = strongly agree |
