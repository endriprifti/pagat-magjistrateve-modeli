"""Figura 1: rrugët e pagës referuese bazë 2019–2026 (nga faza3_rruget_grafik.csv)."""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import date
rows = list(csv.DictReader(open("faza3_rruget_grafik.csv", encoding="utf-8")))
x = [date(int(r["muaji"][:4]), int(r["muaji"][5:]), 1) for r in rows]
def s(k): return [float(r[k]) / 1000 if r[k] not in ("", "None") else None for r in rows]
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9})
fig, ax = plt.subplots(figsize=(6.3, 3.6), dpi=300)
ser = [("R_paguar", "R e paguar faktikisht", "#52514e", "-", 1.6, "steps-post"),
       ("V35_152700_IÇK", "152.700 (shtator 2022) e indeksuar me IÇK", "#8a8984", "--", 1.4, "default"),
       ("L95", "Ligji №95/2026", "#eb6834", "-", 2.0, "steps-post"),
       ("Kesh_A1", "Këshillat (A1)", "#1baf7a", "-.", 2.0, "steps-post"),
       ("Paketa", "Paketa e propozuar (A4)", "#2a78d6", "-", 2.2, "steps-post")]
CUT = date(2026, 9, 1)   # paga e fundit e vrojtuar në Thesar: shtatori 2026 (paguar 2.10.2026)
for k, lab, col, ls, lw, ds in ser:
    if k == "R_paguar":
        continue
    ax.plot(x, s(k), color=col, ls=ls, lw=lw, drawstyle=ds, label=lab)
k, lab, col, ls, lw, ds = ser[0]
y = s(k)
ax.plot(x, [v if d <= CUT else None for d, v in zip(x, y)], color=col, ls=ls, lw=lw, drawstyle=ds,
        label=lab + " (Thesari, deri 9.2026)", zorder=5)
ax.plot(x, [v if d >= CUT else None for d, v in zip(x, y)], color=col, ls=(0, (1, 1.2)), lw=2.6, drawstyle=ds,
        label="R e paguar, e supozuar 10–12.2026 (= L95)", zorder=6)
ax.axvline(date(2026, 10, 1), color="#b5b4ae", lw=0.8, ls=":", zorder=1)
ax.annotate("të dhënat\nderi 5.10.2026", (date(2026, 10, 1), 118), xytext=(-3, 0), textcoords="offset points",
            ha="right", va="bottom", fontsize=6.5, color="#52514e")
ax.set_ylabel("mijë lekë në muaj, bruto", color="#52514e")
ax.set_ylim(100, 260)
ax.grid(axis="y", color="#e6e5e1", lw=0.6); ax.set_axisbelow(True)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"): ax.spines[sp].set_color("#b5b4ae")
ax.tick_params(colors="#52514e")
end = x[-1]
for k, lab, col, *_ in ser:
    v = [y for y in s(k) if y is not None][-1]
    short = {"R_paguar": "", "V35_152700_IÇK": "152.700 + IÇK", "L95": "L95", "Kesh_A1": "", "Paketa": "Paketa"}[k]
    if short:
        dy = {"V35_152700_IÇK": 7, "L95": -4}.get(k, 0)
        ax.annotate(short, (end, v), xytext=(4, dy), textcoords="offset points", va="center", fontsize=7.5, color="#0b0b0b")
h, l = ax.get_legend_handles_labels(); order = [4, 5, 0, 1, 2, 3]
ax.legend([h[i] for i in order], [l[i] for i in order], loc="upper left", frameon=False, fontsize=7.5)
fig.tight_layout()
fig.savefig("faza3_figura1.png", facecolor="white")
print("OK")
