"""Prapambetja individuale sipas profilit për paketën (Kreu V, Tabela 10a). Dalja: faza3_prapambetje_individuale.csv"""
import csv
from faza2a_model import faktori_W
from faza2c_paketa import rruga_paketes
rr = rruga_paketes("2026-12")
prof = {"G1, 5 vjet": ("G1", 5, "pa", False), "G2, 15 vjet": ("G2", 15, "pa", False),
        "G3, 25 vjet, kryetar": ("G3", 25, "kryetar", False), "G2, 10 vjet, GJKKO/SPAK": ("G2", 10, "pa", True)}
rows = []
for p, a in prof.items():
    om = faktori_W(*a)
    A77 = sum(max(r["R"] - r["R_paguar"], 0) for r in rr if r["muaji"] <= "2026-07") * om
    A12 = sum(max(r["R"] - r["R_paguar"], 0) for r in rr) * om
    rows.append({"profili": p, "omega": round(om, 4), "A_4.2023_7.2026": round(A77), "A_4.2023_12.2026": round(A12)})
with open("faza3_prapambetje_individuale.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
