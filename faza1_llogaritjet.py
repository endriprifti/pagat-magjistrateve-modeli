"""
Faza 1 — Baza e llogaritjes për pagën referuese bazë (R) të magjistratëve.
Të gjitha shifrat hyrëse janë marrë nga dokumentet primare të bashkëngjitura;
burimi jepet pranë çdo vlere. Nuk ka asnjë shifër të vlerësuar nga kujtesa.

Ekzekutimi:  python3 faza1_llogaritjet.py   (krijon faza1_rezultatet.csv)
"""
import csv
from datetime import date

# ---------------------------------------------------------------------------
# 1. TË DHËNA HYRËSE (burimi në koment)
# ---------------------------------------------------------------------------
P_2022 = 257_000          # Paga e Presidentit para 1.4.2023 — V15 §42, §46
P_2023 = 425_000          # Paga e Presidentit nga 1.4.2023 — V15 §6, §46 (ligji 34/2023)
R_35_2022 = 152_700       # R si e drejtë e fituar sipas V35/2022 — V15 §44, §95
R_KLSH = 132_100          # R sipas rekomandimit KLSH 2021 (14.000 + 118.100) — V15 §38
R_ZBATIM_GABUAR = 118_100 # R e zbatuar gabimisht 2019–2021 — V15 §35
K_33_2023 = 0.36          # Ligji 33/2023 (i shfuqizuar) — V15 §6
K_95_2026 = 0.38          # Ligji 95/2026, neni 1
RRITJA_570 = 570          # "R u shtua me 570 lekë" — V15 §49
RRITJA_0192 = 0.00192     # "rritja prej 0.192%" — pretendim i kërkuesit, V15 §17.2
REF_SHC_2025 = 231_000    # Drejtor DP në KM, kat. I: 217.000 + 14.000 — pretendim i kërkuesit, V15 §17.2, §17.6
SHTESA_SHOQ = 52_000      # +52.000 lekë (34%) sipas Shoqatës, kat. 1 kl. 1–3 — V15 §21.1
SHTESA_78300 = 78_300     # +78.300 lekë sipas Shoqatës — V15 §21.3
G_SHC_2019_23 = 0.44      # rritja e pagës për pozicion të kategorisë referuese 2019–2023, "afërsisht" — V15 §100
G_PRES = P_2023 / P_2022 - 1   # rritja e pagës së Presidentit (Gjykata: "afërsisht 65%") — V15 §100
KOSTO_SHOQ = 3_700_875_000     # kosto vjetore e pranimit të kërkesës, pretendim i Shoqatës — V15 §21.4

# Treguesit INSTAT 2016 -> 2023, siç citohen nga Gjykata — V15 §99 (lekë/muaj)
INSTAT = {
    "Paga minimale zyrtare":            (22_000, 40_000),
    "Paga mesatare, sektori privat":    (43_662, 65_566),
    "Paga mesatare, sektori shtetëror": (54_488, 81_887),
    "Paga mesatare mujore bruto":       (47_552, 70_539),
}

# Struktura e pagës — L96/2016 neni 2 shkr. "j", neni 12 pikat 3 e 5, neni 14
GAMMA = {"G1": 0.90, "G2": 0.98, "G3": 1.06}   # shtesa për pagën në grup
VJETERSI_NE_VIT = 0.02                          # 2% e R për vit, maks. 25 vjet
DREJTUES = {"pa": 0.0, "zv/kryetar seksioni": 0.05, "kryetar": 0.10}  # % e pagës bruto fillestare
VESHTIRESI_ANTIKORR = 0.80                      # % e pagës bruto fillestare (GJKKO/SPAK)

# Datat — V15 dispozitivi; L95/2026 neni 3; Dekreti 495
D_EFEKTI = date(2023, 4, 1)
D_VENDIMI_NE_FUQI = date(2026, 4, 17)   # FZ nr. 80, 17.4.2026
D_AFATI = date(2026, 7, 31)
D_L95 = date(2026, 9, 18)


def W(R, grupi, vjet, drejtues="pa", antikorr=False):
    """Paga mujore bruto: lineare në R.
    W = R + γR + 0.02·min(y,25)·R + λ(R+γR) + δ(R+γR)"""
    bruto_fillestare = R * (1 + GAMMA[grupi])
    return (R + GAMMA[grupi] * R + VJETERSI_NE_VIT * min(vjet, 25) * R
            + DREJTUES[drejtues] * bruto_fillestare
            + (VESHTIRESI_ANTIKORR * bruto_fillestare if antikorr else 0))


def muaj(d1, d2):
    """Muaj kalendarikë të plotë nga d1 (përfshirë) deri në d2 (përjashtuar)."""
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)


rows = []
def out(seksioni, treguesi, vlera, burimi, shenim=""):
    rows.append({"seksioni": seksioni, "treguesi": treguesi,
                 "vlera": vlera, "burimi": burimi, "shenim": shenim})


# ---------------------------------------------------------------------------
# 2. KONTROLL I KONSISTENCËS SË SHIFRAVE NË VENDIM
# ---------------------------------------------------------------------------
R_33 = K_33_2023 * P_2023
out("A. Konsistenca", "0.36 × 425.000", R_33, "V15 §6; llogaritje")
out("A. Konsistenca", "Diferenca 0.36×P − 152.700", R_33 - R_35_2022, "llogaritje",
    "Gjykata (§49) thotë +570 lekë; aritmetika jep +300")
out("A. Konsistenca", "R e nënkuptuar nga '+570'", R_33 - RRITJA_570, "llogaritje",
    "152.430 ≠ 152.700")
out("A. Konsistenca", "570 / 152.700", RRITJA_570 / R_35_2022, "llogaritje",
    "0,373% ≠ 0,192% e pretenduar (§17.2)")
out("A. Konsistenca", "300 / 152.700", (R_33 - R_35_2022) / R_35_2022, "llogaritje",
    "0,196% ≈ 0,192% → pretendimi 0,192% përputhet me +300, jo me +570")
out("A. Konsistenca", "152.700 + 78.300", R_35_2022 + SHTESA_78300, "V15 §21.3", "= 231.000 ✓")
out("A. Konsistenca", "52.000 / 152.700", SHTESA_SHOQ / R_35_2022, "V15 §21.1", "≈ 34% ✓")
out("A. Konsistenca", "231.000 / 153.000 − 1", REF_SHC_2025 / R_33 - 1, "V15 §103",
    "Gjykata shkruan '30% më e lartë'; aritmetika jep 51%")
out("A. Konsistenca", "1 − 153.000 / 231.000", 1 - R_33 / REF_SHC_2025, "llogaritje",
    "33,8%: ndoshta '30%' i referohet kësaj ane të raportit")
out("A. Konsistenca", "Rritja e pagës së Presidentit", G_PRES, "V15 §100", "Gjykata: 'afërsisht 65%' ✓")
out("A. Konsistenca", "152.700 / 257.000 (raporti para 2023)", R_35_2022 / P_2022, "V15 §21.2",
    "Shoqata: 59% ✓")

# ---------------------------------------------------------------------------
# 3. BAZA E LLOGARITJES: SERITË E R
# ---------------------------------------------------------------------------
R_95 = K_95_2026 * P_2023
seri = {
    "R0  — zbatim i gabuar 2019–2021": R_ZBATIM_GABUAR,
    "R1  — sipas KLSH 2021": R_KLSH,
    "R2  — e drejtë e fituar sipas V35/2022": R_35_2022,
    "R3  — ligji 33/2023 (0,36×P), i shfuqizuar": R_33,
    "R4  — ligji 95/2026 (0,38×P)": R_95,
    "K1  — kundërfaktik: R2 × (1+44%), kategoria e shërbimit civil": R_35_2022 * (1 + G_SHC_2019_23),
    "K2  — kundërfaktik: R2 + 52.000 (Shoqata, kat. 1 kl. 1–3)": R_35_2022 + SHTESA_SHOQ,
    "K3  — kundërfaktik: 231.000 (kërkuesi, referenca 2025)": REF_SHC_2025,
    "K4  — kundërfaktik: R2 × P2023/P2022 (raporti 0,594 me Presidentin)": R_35_2022 * P_2023 / P_2022,
}
for k, v in seri.items():
    out("B. Seritë e R", k, round(v), "shih kodin",
        f"κ = R/425.000 = {v / P_2023:.4f}; ndryshimi ndaj R2 = {v / R_35_2022 - 1:+.1%}")

# ---------------------------------------------------------------------------
# 4. KRAHASIMI ME TREGUESIT E VENDIMIT (§§99–100)
# ---------------------------------------------------------------------------
for k, (a, b) in INSTAT.items():
    out("C. Tregues 2016–2023", k, b / a - 1, "V15 §99 (INSTAT)")
out("C. Tregues 2016–2023", "Kategoria referuese e shërbimit civil 2019–2023", G_SHC_2019_23, "V15 §100")
out("C. Tregues 2016–2023", "Paga e Presidentit 2022→2023", G_PRES, "V15 §100")
out("C. Tregues 2016–2023", "R e magjistratëve: R2→R4 (ligji 95/2026)", R_95 / R_35_2022 - 1, "llogaritje")

# ---------------------------------------------------------------------------
# 5. KORRIDORI I §109 (interpretim, jo kërkesë e shprehur)
# ---------------------------------------------------------------------------
korr_min, korr_max = R_35_2022 * (1 + G_SHC_2019_23), R_35_2022 * P_2023 / P_2022
out("D. Korridori §109", "Kufiri i poshtëm (shërbimi civil, ~44%)", round(korr_min), "interpretim (b)",
    f"κ = {korr_min / P_2023:.3f}")
out("D. Korridori §109", "Kufiri i sipërm (Presidenti, +65,4%)", round(korr_max), "interpretim (b)",
    f"κ = {korr_max / P_2023:.3f}")
out("D. Korridori §109", "R4 (0,38×P) brenda korridorit?", korr_min <= R_95 <= korr_max, "llogaritje",
    f"R4 = {R_95:,.0f}; mungesa ndaj kufirit të poshtëm = {korr_min - R_95:,.0f} lekë/muaj")

# ---------------------------------------------------------------------------
# 6. PRAPAMBETJET PËR NJË MAGJISTRAT (parametrike; N mungon)
# ---------------------------------------------------------------------------
n_muaj = muaj(D_EFEKTI, date(2026, 10, 1))   # 1.4.2023 – 30.9.2026
out("E. Prapambetjet", "Muaj nga 1.4.2023 deri 30.9.2026", n_muaj, "llogaritje")
shembuj = [("G1", 5, "pa", False), ("G2", 15, "pa", False), ("G3", 25, "kryetar", False), ("G2", 10, "pa", True)]
for R_lab, R_val in [("R4 (95/2026)", R_95), ("K1 (+44%)", seri[list(seri)[5]]), ("K4 (raporti 0,594)", korr_max)]:
    for g, y, d, a in shembuj:
        diff = W(R_val, g, y, d, a) - W(R_33, g, y, d, a)
        out("E. Prapambetjet", f"{R_lab} | {g}, {y} vjet, {d}{', antikorr.' if a else ''}",
            round(diff * n_muaj), "llogaritje bruto",
            f"diferencë mujore {diff:,.0f} lekë × {n_muaj} muaj; pa interes, pa indeksimin 2026")

# Shkalla: kosto vjetore e Shoqatës → ekuivalenti i pagës totale vjetore
out("E. Prapambetjet", "Kosto vjetore e pretenduar nga Shoqata", KOSTO_SHOQ, "V15 §21.4",
    "pretendim i palës; baza, N dhe elementet e përfshira nuk dihen")

# ---------------------------------------------------------------------------
# 7. AFATET
# ---------------------------------------------------------------------------
out("F. Afatet", "Ditë vonesë L95/2026 pas afatit 31.7.2026", (D_L95 - D_AFATI).days, "V15 disp. 3–4; L95")
out("F. Afatet", "Ditë nga hyrja në fuqi e V15 deri në L95", (D_L95 - D_VENDIMI_NE_FUQI).days, "FZ 80; L95")

# ---------------------------------------------------------------------------
# 8. DOKUMENTET E REJA (KLGJ 435/2026, KLP 144/2026, VKM 187/2017, VKM 325/2023,
#    raportet parlamentare 15.9.2026, Akti normativ 2/2026)
# ---------------------------------------------------------------------------
I2_2025 = 217_000        # paga për pozicion I-2 "aktualisht" (2025) — V15 §17.2
I2_2026 = 222_425        # paga për pozicion I-2 më 1.8.2026 — VKM 325 Lidhja 1; KLGJ 435; KLP 144 §23
I4_2026, I5_2026 = 184_500, 174_250   # Drejtor DP përmbajtjes / mbështetëse — VKM 325 Lidhja 7
SHTESA_KUAL = 14_000     # grupi i diplomës 1 — VKM 325 Lidhja 2; VKM 187 Lidhja 2
IB_187, IA_187, IIA_187 = 129_800, 141_900, 118_100   # VKM 187/2017 Lidhja 1 (versioni deri 22.9.2022)
R_KESHILLAT = I2_2026 + SHTESA_KUAL   # 236.425 — KLGJ 435 pika 1; KLP 144 pika 1

out("G. Dokumentet e reja", "I-2 2026 / I-2 2025", I2_2026 / I2_2025 - 1, "VKM 325; V15 §17.2",
    "= 2,50% saktësisht → indeksim 2026 i pagave civile (VKM 131/2026)")
out("G. Dokumentet e reja", "R e Këshillave (I-2 + 14.000) nga 1.8.2026", R_KESHILLAT, "KLGJ 435; KLP 144",
    f"κ = {R_KESHILLAT / P_2023:.4f}; ndaj 152.700: {R_KESHILLAT / R_35_2022 - 1:+.1%}")
out("G. Dokumentet e reja", "R e Këshillave para indeksimit 2026 (I-2 2025 + 14.000)", I2_2025 + SHTESA_KUAL,
    "V15 §17.2", "= 231.000 = 152.700 + 78.300 ✓")
out("G. Dokumentet e reja", "Lexim titullor: Drejtor DP përmbajtjes (I-4) + 14.000", I4_2026 + SHTESA_KUAL,
    "VKM 325 Lidhja 7", "alternativë interpretuese; nën korridor")
out("G. Dokumentet e reja", "Lexim titullor: Drejtor DP mbështetëse (I-5) + 14.000", I5_2026 + SHTESA_KUAL,
    "VKM 325 Lidhja 7", "")
out("G. Dokumentet e reja", "VKM 187: I-b + 14.000", IB_187 + SHTESA_KUAL, "VKM 187 Lidhja 1, 4",
    "≠ 152.700 → baza e V35 nuk riprodhohet nga teksti përfundimtar i VKM 187")
out("G. Dokumentet e reja", "VKM 187: I-a + 14.000", IA_187 + SHTESA_KUAL, "VKM 187 Lidhja 1", "≠ 152.700")
out("G. Dokumentet e reja", "L95 ndaj R e Këshillave (ndryshim nominal)", R_95 / R_KESHILLAT - 1, "llogaritje",
    "nëse R = 236.425 ishte në fuqi 1.8–18.9.2026, L95 e ul nominalisht")
out("G. Dokumentet e reja", "220.320 = 153.000 × 1,44 ?", abs(R_33 * 1.44 - 220_320) < 0.5, "llogaritje",
    "PO: R3 e rritur me 44%")
out("G. Dokumentet e reja", "198.963 / 153.000", 198_963 / R_33, "llogaritje", "nuk riprodhohet nga asnjë burim")

# Kalibrimi i kostos nga dy burime (d): "njësi-R" = Σ_i (W_i / R) e kostos mujore për 1 lekë R
KOSTO_KM_VJETORE = 500_000_000       # efekt vjetor i përsëritshëm i projektligjit — raporti KDNJMIP, mendimi i KM
DR_L95 = R_95 - R_33                 # 8.500 lekë
njesi_KM = KOSTO_KM_VJETORE / 12 / DR_L95
njesi_SHOQ = KOSTO_SHOQ / 12 / (REF_SHC_2025 - R_33)
out("H. Kalibrimi fiskal", "Njësi-R të nënkuptuara nga KM (0,38 vs 0,36; me shtesat e GJL në draft)", round(njesi_KM),
    "KDNJMIP; llogaritje", "mbivlerësim: drafti fillestar kishte edhe 80%+5% për GJL/PP")
out("H. Kalibrimi fiskal", "Njësi-R të nënkuptuara nga Shoqata (231.000 vs 153.000)", round(njesi_SHOQ),
    "V15 §21.4; llogaritje", "pretendim i palës")
for lab, u in [("Shoqata", njesi_SHOQ), ("KM", njesi_KM)]:
    out("H. Kalibrimi fiskal", f"Kosto vjetore R=236.425 kundrejt 161.500 (baza {lab})",
        round(12 * u * (R_KESHILLAT - R_95)), "llogaritje (d)", "lekë/vit, përfshirë çfarëdo kontributi që përmban baza")
    # Prapambetjet 1.4.2023–31.7.2026: 231.000 deri 2025, 236.425 për 2026 (data e VKM 131/2026 e panjohur → supozim 1.1.2026)
    m_1 = muaj(date(2023, 4, 1), date(2026, 1, 1)); m_2 = muaj(date(2026, 1, 1), date(2026, 8, 1))
    prap_K = u * ((231_000 - R_33) * m_1 + (R_KESHILLAT - R_33) * m_2)
    prap_L95 = u * (R_95 - R_33) * (m_1 + m_2)
    out("H. Kalibrimi fiskal", f"Prapambetje 4.2023–7.2026 sipas Këshillave (baza {lab})", round(prap_K),
        "llogaritje (d)", f"{m_1}+{m_2} muaj; seri e verifikuar: VKM 325 orig., VKM 131/2026")
    out("H. Kalibrimi fiskal", f"Prapambetje 4.2023–7.2026 sipas L95 (baza {lab})", round(prap_L95), "llogaritje (d)", "")
# Kontroll i kryqëzuar: shifrat periodike të KM (raporti KDNJMIP) → njësi-R të nënkuptuara
for lab, shuma, m in [("KM prill–dhjetor 2023 (260 mln)", 260e6, 9),
                      ("KM 2024–2025 (740 mln)", 740e6, 24),
                      ("KM 2023–2026 total (1,5 mld)", 1.5e9, 45)]:
    out("H. Kalibrimi fiskal", f"Njësi-R të nënkuptuara: {lab}", round(shuma / m / DR_L95), "KDNJMIP; llogaritje",
        "baza konvergon me atë të Shoqatës (~3.950)")
PAGA_SHTET_2026, KONTRIB_2026 = 120_348e6, 19_973e6   # AN 2/2026, tabela makro (milionë lekë)
out("H. Kalibrimi fiskal", "Kontributet / pagat, buxheti i shtetit 2026", KONTRIB_2026 / PAGA_SHTET_2026, "AN 2/2026", "≈ norma mesatare e kontributeve të punëdhënësit")
out("H. Kalibrimi fiskal", "Kosto vjetore (baza Shoqata) / fondi i pagave i shtetit 2026",
    12 * njesi_SHOQ * (R_KESHILLAT - R_95) / PAGA_SHTET_2026, "llogaritje", "")

# ---------------------------------------------------------------------------
# 9. VENDIMI 35/2022 DHE AUDITIMET E KLSH
# ---------------------------------------------------------------------------
R_V35_2016 = 118_000 + 14_000   # I-b (VKM 545/2011) + paga në grup — V35 §§68, 72, 76
R_V35_2019 = 129_800 + 14_000   # I-b (VKM 187/2017) + paga në grup — V35 §§77, 80
out("I. V35 dhe KLSH", "R sipas standardit të V35, 2016 (I-b 118.000 + 14.000)", R_V35_2016, "V35 §§68, 76")
out("I. V35 dhe KLSH", "R sipas standardit të V35, 2019 (I-b 129.800 + 14.000)", R_V35_2019, "V35 §§77, 80")
out("I. V35 dhe KLSH", "152.700 − R(V35, 2019)", R_35_2022 - R_V35_2019, "llogaritje",
    "8.900 lekë pa shpjegim: 152.700 nuk gjendet në V35; vjen nga relacioni i 2023 (V15 §44)")
out("I. V35 dhe KLSH", "R sipas rekomandimit KLSH 2021 (II-a + 14.000)", R_KLSH, "KLSH, auditim tematik 2021",
    "KLSH përdori II-a; V35 e korrigjoi më pas te I-b")
# Lexime të standardit të V35 në strukturën e VKM 325
for lab, v in [("klasa më e ulët e kategorisë I (I-5)", I5_2026), ("drejtor DP përmbajtjeje (I-4)", I4_2026),
               ("pozicionet e barasvlershme me I-b (I-2)", I2_2026)]:
    out("I. V35 dhe KLSH", f"V35 në VKM 325: {lab} + 14.000", v + SHTESA_KUAL, "V35 §§65, 72; VKM 325",
        f"κ = {(v + SHTESA_KUAL) / P_2023:.3f}; brenda korridorit: {korr_min <= v + SHTESA_KUAL <= korr_max}")

# Validimi i W(R) me tabelën e pagave të GJL (KLSH, shkurt 2023), R = 118.100
R_GJL = 118_100
validim = [  # (përshkrimi, grupi, vjet, drejtues, paga totale sipas KLSH)
    ("Kryetar, 15 vjet", "G3", 15, "kryetar", 303_044), ("Kryetar, 25 vjet", "G3", 25, "kryetar", 326_664),
    ("Zv/kryetar, 15 vjet", "G3", 15, "zv/kryetar seksioni", 290_880), ("Zv/kryetar, 25 vjet", "G3", 25, "zv/kryetar seksioni", 314_500),
    ("Gjyqtar nga magjistratët, 25 vjet", "G3", 25, "pa", 302_336), ("Gjyqtar nga juristët, 15 vjet", "G3", 15, "pa", 278_716)]
maks_dev = 0
for lab, g, y, d, w_klsh in validim:
    dev = round(W(R_GJL, g, y, d)) - w_klsh
    maks_dev = max(maks_dev, abs(dev))
    out("I. V35 dhe KLSH", f"Validim W(R): {lab}", dev, "KLSH GJL 2023, f. 34", f"W model = {W(R_GJL, g, y, d):,.0f}; KLSH = {w_klsh:,}")
out("I. V35 dhe KLSH", "Devijimi maksimal i modelit W(R) nga të dhënat e KLSH (lekë)", maks_dev, "llogaritje",
    "modeli linear riprodhon 6/6 rreshta; R e paguar në GJL në periudhën e audituar = 118.100")
out("I. V35 dhe KLSH", "Vështirësia e vërejtur (gjyqtarët nga gjykatat e posaçme) / paga bruto fillestare",
    145_972 / (2.06 * R_GJL), "KLSH GJL 2023", "60%, jo 80% si në ligj → mospërputhje për t'u verifikuar")
out("I. V35 dhe KLSH", "Kontributet/pagat, fondi shtesë KLGJ 2023 (25 mln / 140 mln)", 25 / 140, "KLSH KLGJ 2024", "")

# ---------------------------------------------------------------------------
# 10. MATERIALET E LIGJIT 33/2023 (RIA, raportet e komisioneve, maj 2023)
# ---------------------------------------------------------------------------
IB_621, IIA_621 = 138_700, 126_300    # VKM 621, datë 28.9.2022 — RIA f. 11, 13; Raporti KEF f. 3
R_PARA_REFORMES = 107_100             # R para reformës — Raporti KEF f. 2
out("J. Ligji 33/2023", "I-b pas VKM 621/2022 + 14.000", IB_621 + SHTESA_KUAL, "RIA; Raporti KEF",
    "= 152.700 ✓ → origjina e R2 e zgjidhur")
out("J. Ligji 33/2023", "Rritja e I-b nga VKM 621/2022", IB_621 / IB_187 - 1, "llogaritje", "")
out("J. Ligji 33/2023", "Rritja e II-a nga VKM 621/2022", IIA_621 / IIA_187 - 1, "llogaritje", "")
out("J. Ligji 33/2023", "R para reformës", R_PARA_REFORMES, "Raporti KEF", "")
out("J. Ligji 33/2023", "Amendamenti i refuzuar κ = 0,46 (Alibeaj)", 0.46 * P_2023, "Raporti i Komisionit Ligjor 2023",
    f"nën korridor: {0.46 * P_2023 < korr_min}")
KOSTO_RIA = 959e6                      # efekt vjetor, përfshirë funksionarët e lidhur — RIA; Raporti KEF
for lab, baza in [("nga 126.300 (ligji 50/2021 pas VKM 621)", IIA_621), ("nga 132.100 (KLSH)", R_KLSH),
                  ("nga 118.100", R_ZBATIM_GABUAR)]:
    out("J. Ligji 33/2023", f"Njësi-R të nënkuptuara nga RIA 959 mln/vit, {lab}", round(KOSTO_RIA / 12 / (R_33 - baza)),
        "RIA; llogaritje (d)", "baza buxhetore e 2023 nuk është e qartë; RIA ka edhe shifra të papajtueshme (48,9; 79,9)")
out("J. Ligji 33/2023", "Rritja e referencës civile, 9.2022→2023 (231.000 / 152.700)", REF_SHC_2025 / R_35_2022 - 1,
    "llogaritje", "nëse I-2 = 217.000 që nga 1.4.2023 (e paverifikuar: VKM 325 origjinale mungon)")

# ---------------------------------------------------------------------------
# 11. VKM 325/2023 ORIGJINALE, VKM 337/2025, VKM 131/2026 — seritë e verifikuara
# ---------------------------------------------------------------------------
VKM325_2023 = {"I-1": 235_000, "I-2": 217_000, "I-3": 205_000, "I-4": 180_000, "I-5": 170_000}  # nga 1.4.2023
# VKM 337/2025: shton I-1/1 = 226.000; I-2 mbetet 217.000. VKM 131/2026: +2,5% nga 1.1.2026 (I-2 = 222.425)
out("K. Seritë e verifikuara", "I-2: 1.4.2023 → 31.12.2025 (VKM 325 orig.; VKM 337 pa ndryshim)", VKM325_2023["I-2"],
    "VKM 325 Lidhja 1, pika 7; VKM 337/2025", "supozimi i mëparshëm konfirmohet")
out("K. Seritë e verifikuara", "I-2 nga 1.1.2026 (VKM 131/2026, indeksim 2,5%)", round(VKM325_2023["I-2"] * 1.025),
    "VKM 131/2026, ndarja II/b, III/b", "efekt nga 1.1.2026, jo nga data e miratimit")
for a, x in [("II-a", IIA_187), ("I-b", IB_187)]:
    for b in ("I-2", "I-4", "I-5"):
        out("K. Seritë e verifikuara", f"Rritja e pagës për pozicion 2019→2023: {a} → {b}", VKM325_2023[b] / x - 1,
            "VKM 187; VKM 325 orig.", "≈ 44% e V15 §100" if (a, b) == ("II-a", "I-5") else "")
# Prapambetjet sipas skemës së Këshillave, me seri të verifikuar
m_23_25 = muaj(date(2023, 4, 1), date(2026, 1, 1)); m_26 = muaj(date(2026, 1, 1), date(2026, 8, 1))
R_K23, R_K26 = VKM325_2023["I-2"] + SHTESA_KUAL, round(VKM325_2023["I-2"] * 1.025) + SHTESA_KUAL
for g, y, d, a in shembuj:
    diff = (W(R_K23, g, y, d, a) - W(R_33, g, y, d, a)) * m_23_25 + (W(R_K26, g, y, d, a) - W(R_33, g, y, d, a)) * m_26
    out("K. Seritë e verifikuara", f"Prapambetje 4.2023–7.2026 sipas Këshillave | {g}, {y} vjet, {d}{', antikorr.' if a else ''}",
        round(diff), "llogaritje", f"{m_23_25} muaj me 231.000 + {m_26} muaj me 236.425, kundrejt 153.000; pa indeksimin e R në 2026")

with open("faza1_rezultatet.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

for r in rows:
    v = r["vlera"]
    vs = ("PO" if v else "JO") if isinstance(v, bool) else f"{v:.2%}" if isinstance(v, float) and abs(v) < 2 else (f"{v:,}" if isinstance(v, (int, float)) else str(v))
    print(f"{r['seksioni']:<22} | {r['treguesi']:<66} | {vs:>14} | {r['shenim']}")
