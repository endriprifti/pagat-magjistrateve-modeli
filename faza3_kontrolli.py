"""Kontrolli i konsistencës për tekstin e Fazës 3: çdo numër me ndarës mijëshe ose presje dhjetore
duhet të gjendet (brenda tolerancës së rrumbullakimit) në CSV-të e Fazave 1–2.
Përdorimi: python3 faza3_kontrolli.py faza3a_tekst.txt [faza3b_tekst.txt ...]"""
import csv, re, sys, bisect
from pathlib import Path
DIR = Path(__file__).resolve().parent
vals = set()
for f in sorted(DIR.glob("faza*.csv")):
    if f.name.endswith("konsistenca.csv"):
        continue
    for row in csv.reader(open(f, encoding="utf-8")):
        for cell in row:
            for tok in re.findall(r"-?\d+(?:\.\d+)?(?:e[+-]?\d+)?", cell):
                try: vals.add(abs(float(tok)))
                except ValueError: pass
vals = sorted(vals)
def gjendet(x, tol):
    for c in (x, x / 100, x * 1e9, x * 1e6):
        t = tol * (c / x if x else 1)
        i = bisect.bisect_left(vals, c - t)
        if i < len(vals) and vals[i] <= c + t:
            return True
    return False
pat = re.compile(r"(?<![\w§/.№-])\d{1,3}(?:\.\d{3})+(?:,\d+)?(?![\d.])|(?<![\w§/.№-])\d+,\d+(?!\d)")
rez, gabime = [], 0
for fp in sys.argv[1:]:
    for nr, line in enumerate(open(fp, encoding="utf-8"), 1):
        for tok in pat.findall(line):
            s = tok.replace(".", "").replace(",", ".")
            x = float(s); dec = len(s.split(".")[1]) if "." in s else 0
            ok = gjendet(x, 0.5 * 10 ** (-dec) + 1e-9) or gjendet(x, 0.5 * 10 ** (-dec) * 1.0001 + 0.5)
            rez.append({"skedari": fp, "rreshti": nr, "numri": tok, "gjendet": ok})
            if not ok:
                gabime += 1; print(f"{fp}:{nr}  {tok}  |  {line.strip()[:120]}")
with open(DIR / "faza3_konsistenca.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["skedari", "rreshti", "numri", "gjendet"]); w.writeheader(); w.writerows(rez)
print(f"Numra të kontrolluar: {len(rez)}; pa përputhje: {gabime}")
