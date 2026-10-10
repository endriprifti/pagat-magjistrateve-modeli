"""
Burimet shtesë (7.10.2026, mbrëmje): VKM 755/2023, KLGJ 233/2025, ligji 115/2016, ligji 8577/2000,
RPM e BSH 2025/I–2026/III. Llogarit vetëm shifrat që përdoren në tekst.
Dalja: faza2_burimet_shtese.csv
"""
import csv
from pathlib import Path
from faza2a_model import faktori_W, N_R

DIR = Path(__file__).resolve().parent
rez = []
def out(t, v, burimi, shenim=""):
    rez.append({"treguesi": t, "vlera": round(v, 4) if isinstance(v, float) else v,
                "burimi": burimi, "shenim": shenim})

# VKM 755, datë 20.12.2023: 1 mld lekë për "një pjesë" të diferencës sipas V35, nga 1.1.2019
vkm755 = {"PP": 400e6, "KLP": 10e6, "KLGJ": 350e6, "SPAK": 60e6, "ILD": 2e6, "Shkolla e Magjistraturës": 54e6,
          "KPK": 60e6, "KPA": 25e6, "Komisionerët Publikë": 22e6, "KQZ": 13e6, "Avokati i Popullit": 4e6}
grupet = {"Sistemi i drejtësisë (PP, KLP, KLGJ, SPAK, ILD, Shkolla)": ["PP", "KLP", "KLGJ", "SPAK", "ILD", "Shkolla e Magjistraturës"],
          "Institucionet e vetingut (KPK, KPA, Komisionerët)": ["KPK", "KPA", "Komisionerët Publikë"],
          "Institucione të tjera kushtetuese (KQZ, Avokati i Popullit)": ["KQZ", "Avokati i Popullit"]}
tot = sum(vkm755.values())
out("VKM 755/2023: totali", tot, "VKM 755 pika 1")
for g, ks in grupet.items():
    s = sum(vkm755[k] for k in ks)
    out(f"VKM 755/2023: {g}", s, "VKM 755 pika 2")
    out(f"VKM 755/2023: pesha e {g}", s / tot, "llogaritje")

# KLGJ 233/2025: 417 pozicione gjyqtarësh (organika, jo të emëruar faktikisht)
N_GJ = 417
om_min = faktori_W("G1", 0)
om_max_pa_antikorr = faktori_W("G3", 25, "kryetar")
om_max = faktori_W("G3", 25, "kryetar", antikorr=True)
out("Gjyqtarë (pozicione), KLGJ 233/2025", N_GJ, "KLGJ 233 pika 1")
out("ω min (G1, 0 vjet)", om_min, "F1")
out("ω maks pa GJKKO (G3, 25 vjet, kryetar)", om_max_pa_antikorr, "F1")
out("ω maks absolut (G3, 25 vjet, kryetar, GJKKO)", om_max, "F1")
out("Njësi-R të gjyqtarëve: kufiri i poshtëm (417 × ω min)", N_GJ * om_min, "llogaritje")
out("Njësi-R të gjyqtarëve: kufiri i sipërm (417 × ω maks absolut)", N_GJ * om_max, "llogaritje", "kufi teorik, jo realist")
out("Pjesa e N_R qendror (3.954) që mbetet për prokurorët, kategoritë e lidhura dhe/ose kontributet, min",
    N_R["qendror"] - N_GJ * om_max, "llogaritje")
out("idem, maks", N_R["qendror"] - N_GJ * om_min, "llogaritje")
out("ω mesatar i nënkuptuar nëse N_R qendror do t'u përkiste vetëm 417 gjyqtarëve", N_R["qendror"] / N_GJ,
    "llogaritje", "i pamundur: > ω maks absolut")

# Ligji 8577/2000, neni 17: gjyqtari i GJK = paga e Kryetarit të GJL; Kryetari i GJK = +20%
w_kr_gjl_25 = faktori_W("G3", 25, "kryetar")
out("ω i Kryetarit të GJL me 25 vjet (ankora e gjyqtarit të GJK)", w_kr_gjl_25, "F1; ligji 8577 neni 17/1",
    "vjetërsia e ankorës nuk përcaktohet në ligj (d)")
out("ω i Kryetarit të GJK (= 1,20 × ankora)", 1.20 * w_kr_gjl_25, "ligji 8577 neni 17/2")

# Ligji 8097/1996 (i përditësuar me ligjin 166/2020): pensioni suplementar ∝ paga referuese (paga e muajit të fundit)
# Magjistratët: grupi i dytë "a" → 1,5% × vite × paga referuese, maks. 40% (neni 11).
# Gjyqtarët e GJL/GJK, anëtarët e KLGJ/KLP: grupi i parë "b" → 20% për 2 vite + 5% për çdo vit tjetër, maks. 50% (neni 9).
from faza2a_model import W, R_95_2026
R_PAK = 243_538.6221
def pension_g2(R, grupi, vjet, drejtues="pa"):
    return min(0.015 * vjet, 0.40) * W(R, grupi, vjet, drejtues)
def pension_g1b(R, vjet_funksion, vjet_total):
    return min(0.20 + 0.05 * max(vjet_funksion - 2, 0), 0.50) * W(R, "G3", vjet_total)
for emri, f in [("G2, 25 vjet (grupi i dytë)", lambda R: pension_g2(R, "G2", 25)),
                ("G1, 30 vjet (grupi i dytë, tavan 40%)", lambda R: pension_g2(R, "G1", 30)),
                ("Gjyqtar GJL, 9 vjet në GJL, 25 vjet gjithsej (grupi i parë b, tavan 50%)", lambda R: pension_g1b(R, 9, 25))]:
    out(f"Pensioni suplementar mujor | {emri} | L95 2026", f(R_95_2026), "ligji 8097/1996 nenet 9, 11")
    out(f"Pensioni suplementar mujor | {emri} | paketa 2026", f(R_PAK), "idem")
    out(f"Pensioni suplementar mujor | {emri} | diferenca", f(R_PAK) - f(R_95_2026), "idem")
out("W i G3, 25 vjet, kryetar, me paketën, kundrejt P 2026", W(R_PAK, "G3", 25, "kryetar") / 435_625 - 1,
    "tavani P i nenit 1/7/b do të kufizonte pagën referuese nëse do të ishte në fuqi; V35 e shfuqizoi")

with open(DIR / "faza2_burimet_shtese.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["treguesi", "vlera", "burimi", "shenim"])
    w.writeheader(); w.writerows(rez)
for r in rez:
    print(f'{r["treguesi"]:105s} {r["vlera"]!s:>14s}  {r["shenim"]}')
