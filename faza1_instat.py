"""
Faza 1 — Seritë e pagave nga botimet e INSTAT "Statistikat e Pagave".

1) Tab. 1 (botimet deri në T4/2024): paga mesatare mujore bruto gjithsej, sektori shtetëror,
   sektori privat, paga minimale — 13 tremujorë për botim. Rreshtat identifikohen sipas etiketës,
   jo sipas renditjes; çdo mospërputhje e së njëjtës vlerë ndërmjet botimeve raportohet si KONFLIKT.
2) Botimet 2025–2026 (format i ri) japin vetëm pagën mesatare gjithsej në tekst; ato futen me dorë
   më poshtë, me burimin përkatës.

Ekzekutimi: python3 faza1_instat.py <dosja_me_tekstet_txt>   (tekstet nga `pdftotext -layout`)
Dalja: faza1_instat_pagat_tremujore.csv
"""
import re, glob, sys, csv, os

DIR = sys.argv[1] if len(sys.argv) > 1 else "."
Q = re.compile(r"\b(IV|I{1,3})/?(\d\d)\b")
N = re.compile(r"\b\d{2,3}\.\d{3}\b")
res = {k: {} for k in ("total", "shteteror", "privat", "minimale")}
burim = {}
konflikte = []

for f in sorted(glob.glob(os.path.join(DIR, "*.txt"))):
    t = open(f, encoding="utf-8").read()
    i = t.find("Tab. 1")
    if i < 0:
        continue
    j = t.find("Tab. 2", i)
    lines = t[i: j if j > 0 else len(t)].split("\n")
    hdr = None
    rreshta = []
    for k, l in enumerate(lines):
        qs = Q.findall(l)
        if hdr is None and len(qs) >= 5:
            hdr = [f"{a}/{b}" for a, b in qs]
            continue
        if hdr:
            ns = N.findall(l)
            if len(ns) == len(hdr):
                rreshta.append([int(v.replace(".", "")) for v in ns])
    if not hdr:
        continue
    # Paga minimale: të gjitha vlerat janë mijëshe të plota dhe <= 60.000.
    # Rreshtat e tjerë ruajnë gjithmonë renditjen e INSTAT: gjithsej, sektori shtetëror, sektori privat.
    minim = [r for r in rreshta if all(v % 1000 == 0 and v <= 60000 for v in r)]
    tjeret = [r for r in rreshta if r not in minim]
    caktim = list(zip(("total", "shteteror", "privat"), tjeret[:3])) + [("minimale", r) for r in minim[:1]]
    for nm, vals in caktim:
        for q, v in zip(hdr, vals):
            if q in res[nm] and res[nm][q] != v:
                konflikte.append((nm, q, res[nm][q], v, os.path.basename(f)))
            res[nm].setdefault(q, v)
            burim.setdefault((nm, q), os.path.basename(f))

# Botimet 2025–2026: vetëm totali (tekst i botimit)
TOTALE_RE = {"I/25": (82210, "T1-2025"), "II/25": (83906, "T2-2025"), "III/25": (83300, "T3-2025"),
             "IV/25": (86984, "T4-2025"), "I/26": (90119, "T1-2026"), "II/26": (92150, "T2-2026")}
for q, (v, b) in TOTALE_RE.items():
    res["total"][q] = v
    burim[("total", q)] = b
res["minimale"].update({q: 40000 for q in ("I/25", "II/25", "III/25", "IV/25")})
res["minimale"].update({"I/26": 50000, "II/26": 50000})   # pagë minimale 50.000 nga 1.1.2026 (T1-2026)

print("Konflikte ndërmjet botimeve:", len(konflikte))
for c in konflikte:
    print("  KONFLIKT", c)


def key(q):
    r, y = q.split("/")
    return (int(y), {"I": 1, "II": 2, "III": 3, "IV": 4}[r])


qs = sorted(res["total"], key=key)
with open("faza1_instat_pagat_tremujore.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["tremujori", "gjithsej", "sektori_shteteror", "sektori_privat", "paga_minimale", "burimi_gjithsej"])
    for q in qs:
        w.writerow([q] + [res[k].get(q, "") for k in ("total", "shteteror", "privat", "minimale")] + [burim.get(("total", q), "")])

ann = {}
for y in range(16, 27):
    qq = [q for q in qs if q.endswith("/%02d" % y)]
    row = {}
    for k in ("total", "shteteror", "privat"):
        v = [res[k][q] for q in qq if q in res[k]]
        if len(v) == 4:
            row[k] = sum(v) / 4
    if row:
        ann[2000 + y] = row
print("\nMesataret vjetore (vetëm vite me 4 tremujorë):")
for y, r in ann.items():
    print(y, {k: round(v) for k, v in r.items()})
print("\nKontroll me V15 §99: shtetërore 2016 =", round(ann[2016]["shteteror"]), "(54.488);",
      "privat 2016 =", round(ann[2016]["privat"]), "(43.662);", "shtetërore 2023 =", round(ann[2023]["shteteror"]), "(81.887)")
for a, b in [(2016, 2023), (2016, 2024), (2019, 2024), (2022, 2024), (2016, 2025), (2022, 2025)]:
    out = []
    for k in ("total", "shteteror"):
        if k in ann.get(a, {}) and k in ann.get(b, {}):
            out.append(f"{k} {ann[b][k] / ann[a][k] - 1:+.1%}")
    print(f"Rritja {a}→{b}:", "; ".join(out))
print(f"Gjithsej III/22 → II/26: {res['total']['II/26'] / res['total']['III/22'] - 1:+.1%}")
print(f"Shtetërore III/22 → IV/24: {res['shteteror']['IV/24'] / res['shteteror']['III/22'] - 1:+.1%}")
