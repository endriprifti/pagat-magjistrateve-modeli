"""
Faza 1 — Indeksi i Çmimeve të Harmonizuara të Konsumit (IÇHK / HICP, ECOICOP v2), INSTAT, 2016-01 → 2026-08.
Burimi: databaza statistikore e INSTAT, eksport "Instat1" (7.10.2026), rreshti "0000 Gjithsej".

Ekzekutimi: python3 faza1_hicp.py <eksporti.xlsx> [dalja.csv]
  IÇHK: python3 faza1_hicp.py Instat1.xlsx faza1_hicp_mujor.csv
  IÇK kombëtar (ECOICOP v2, eksport 7.10.2026): python3 faza1_hicp.py Instat_IChK.xlsx faza1_ichk_mujor.csv
Shënim: IÇHK nuk është identik me IÇK kombëtare (objektivi i BSH matet me IÇK). Për 2024–2025,
IÇK mesatare = 2,2%/vit (INSTAT), ndërsa IÇHK mesatare = 2,5%/2,3%.
"""
import sys
import openpyxl
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "Instat1.xlsx"
dalja = sys.argv[2] if len(sys.argv) > 2 else "faza1_hicp_mujor.csv"
rows = list(openpyxl.load_workbook(src, read_only=True).active.iter_rows(values_only=True))
var, mon, tot = rows[2], rows[3], rows[4]
assert tot[1] == "Gjithsej"
cur, recs = None, []
for j in range(2, len(mon)):
    cur = var[j] or cur
    recs.append((cur, mon[j], tot[j]))
df = pd.DataFrame(recs, columns=["var", "m", "v"])
idx = df[df["var"].str.startswith("Indeksi")].set_index("m").v.astype(float)
yoy = pd.to_numeric(df[df["var"].str.startswith("Ndryshimi vjetor")].set_index("m").v, errors="coerce")
idx.index = pd.PeriodIndex(idx.index, freq="M")
yoy.index = pd.PeriodIndex(yoy.index, freq="M")
pd.DataFrame({"IChK_indeksi": idx, "ndryshimi_vjetor_%": yoy}).to_csv(dalja)

ann = idx.groupby(idx.index.year).mean()
print("Viti | muaj | indeksi mesatar | inflacioni mesatar vjetor | dhjetor a/a")
for y in ann.index:
    n = int((idx.index.year == y).sum())
    infl = f"{ann[y] / ann[y - 1] - 1:+.2%}" if (y - 1) in ann.index and n == 12 else "—"
    print(y, n, round(ann[y], 2), infl, yoy.get(pd.Period(f"{y}-12", "M")))


def g(a, b):
    return idx[pd.Period(b, "M")] / idx[pd.Period(a, "M")] - 1


print("\nNdryshime kumulative të indeksit:")
for a, b, lab in [("2016-10", "2026-08", "miratimi i L96 → sot"),
                  ("2019-01", "2026-08", "zbatimi i L96 → sot"),
                  ("2022-09", "2026-08", "VKM 621 / R = 152.700 → sot"),
                  ("2023-04", "2026-08", "R = 153.000 (ligji 33/2023) → sot"),
                  ("2023-04", "2025-12", "R = 153.000 → para indeksimit 2026"),
                  ("2026-01", "2026-08", "2026 deri në gusht")]:
    print(f"  {a} → {b} ({lab}): {g(a, b):+.2%}")

print("\nVlera reale e R (lekë të gushtit 2026):")
for lab, R, m in [("R2 = 152.700, shtator 2022", 152_700, "2022-09"), ("R3 = 153.000, prill 2023", 153_000, "2023-04")]:
    print(f"  {lab}: {R * (1 + g(m, '2026-08')):,.0f}")
print(f"  L95 = 161.500 kundrejt R2 të indeksuar: {161_500 / (152_700 * (1 + g('2022-09', '2026-08'))) - 1:+.2%}")
print(f"  Këshillat = 236.425 kundrejt R2 të indeksuar: {236_425 / (152_700 * (1 + g('2022-09', '2026-08'))) - 1:+.2%}")

y = yoy.dropna()
mbi4 = [str(p) for p, v in y.items() if v > 4]
print(f"\nMuaj me inflacion vjetor > 4% (mbi tavanin e L95): {len(mbi4)}; i pari {mbi4[0]}, i fundit {mbi4[-1]}")
print(f"Maksimumi: {y.idxmax()} = {y.max()}%")
