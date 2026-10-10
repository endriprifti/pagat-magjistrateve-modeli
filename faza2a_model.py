"""
Faza 2a — Modeli matematikor bazë (§6 i detyrës).

Ky skedar është njëkohësisht:
  (1) modul që importohet nga nënhapat 2b–2d (from faza2a_model import *), dhe
  (2) skript që, kur ekzekutohet, prodhon:
        faza2a_fjalori.csv      — fjalori i simboleve
        faza2a_rezultatet.csv   — çdo shifër e përdorur në §6 të tekstit
        faza2a_rruget_min.csv   — rrugët minimale të realizueshme të R, muaj pas muaji
        faza2a_shembuj.csv      — shembujt e riprodhueshëm për çdo formulë

Shënimet (a)–(e) ndjekin §3 e detyrës. Asnjë alternativë nuk vlerësohet këtu (kjo është 2b).
Ekzekutimi:  python3 faza2a_model.py
"""
from __future__ import annotations
import csv
from pathlib import Path

DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 1. Parametrat (me burim)
# ---------------------------------------------------------------------------
R_V35 = 152_700          # R si e drejtë e fituar, shtator 2022: I-b 138.700 + 14.000 (VKM 621/2022; V15 §95) (c)
R_33 = 153_000           # R e paguar nga 1.4.2023: 0,36 × 425.000 (ligji 33/2023) (c)
R_95 = 161_500           # R sipas L95 me P = 425.000 (2023–2025): 0,38 × 425.000 (c)
P_2026 = 435_625         # P nga 1.1.2026: 425.000 × 1,025 (VKM 92/2026; ligji 87/2025 neni 13) (c)
R_33_2026 = 156_825      # R e paguar nga 1.1.2026: 0,36 × 435.625 (VKM 93/2026) (c)
R_95_2026 = 0.38 * P_2026   # 165.537,5: L95 me P të indeksuar (c për aritmetikën; d për zbatimin nga 9.2026)
R_KESH = 236_425         # R e Këshillave nga 1.8.2026 (KLGJ 435; KLP 144) (c)
SHTESA_GRUP = 14_000     # paga në grup, diploma 1 (VKM 325 Lidhja 2) (c)
P_2022, P_2023 = 257_000, 425_000   # paga e Presidentit (V15 §§42, 46) (c)

G_CIV = 0.44             # "afërsisht 44%", V15 §100 (a për shifrën; b për përdorimin si kufi)
G_CIV_EKZAKT = 170_000 / 118_100 - 1   # gjurma II-a → I-5 që e riprodhon (c)
G_PRES = P_2023 / P_2022 - 1           # "afërsisht 65%", V15 §100 (c)

# Paga për pozicion I-2 (pasardhëse e I-b; Faza 1 §4.2a) (c)
I2 = {"2022-09": 138_700, "2023-04": 217_000, "2026-01": 222_425}

# Struktura e pagës totale (L96 nenet 2/j, 12, 14; validuar me KLSH-GJL, Faza 1 §4.3) (c)
GAMMA = {"G1": 0.90, "G2": 0.98, "G3": 1.06}
LAMBDA = {"pa": 0.0, "zv/kryetar seksioni": 0.05, "kryetar": 0.10}
DELTA_ANTIKORR = 0.80
VJETERSI = 0.02

# Kalibrimi fiskal pa N (Faza 1 §4.5): njësi-R = Σ W_i / R (d)
N_R = {"i_ulet": 3_000, "qendror": 3_954, "i_larte": 4_902}
KONTRIBUTE = 0.166       # kontributet e punëdhënësit, mesatare agregat (AN 2/2026) (c, përafërsisht)

# Datat kyçe (muaj "YYYY-MM")
M_BAZA = "2023-04"       # efektet financiare, V15 §110 (a)
M_KESH = "2026-08"       # nga ky muaj vepron R e Këshillave (KLGJ 435, KLP 144) (c)
M_L95 = "2026-09"        # muaji i parë i paguar sipas L95 (Thesari, Faza 1 §4.6) (c)
RISHIKIMET = ["2026-01"] # datat e rishikimit: çdo ≤ 2 vjet, i pari jo para 1.1.2026 (ligji 33/2023; L95) (c)

# ---------------------------------------------------------------------------
# 2. Seritë mujore
# ---------------------------------------------------------------------------
def lexo_ichk(path=DIR / "faza1_ichk_mujor.csv") -> dict[str, float]:
    with open(path, encoding="utf-8") as f:
        return {r["m"]: float(r["IChK_indeksi"]) for r in csv.DictReader(f)}

ICHK = lexo_ichk()

def muajt(nga: str, deri: str) -> list[str]:
    """Lista e muajve nga 'nga' deri 'deri', përfshirë të dy."""
    y, m = map(int, nga.split("-")); y2, m2 = map(int, deri.split("-"))
    out = []
    while (y, m) <= (y2, m2):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out

def muaji_para(m: str) -> str:
    y, mm = map(int, m.split("-"))
    return f"{y-1:04d}-12" if mm == 1 else f"{y:04d}-{mm-1:02d}"

def ref_civile(m: str) -> int:
    """Ref_civ(t) = I-2(t) + 14.000: referenca civile e formulës së vjetër (§109, opsioni 1)."""
    if m < "2023-04":
        return I2["2022-09"] + SHTESA_GRUP
    if m < "2026-01":
        return I2["2023-04"] + SHTESA_GRUP
    return I2["2026-01"] + SHTESA_GRUP

def ref_presidenti(m: str) -> int:
    """Ref_P(t) = P(t): 257.000 → 425.000 (4.2023; ligjet e buxhetit 2024, 2025) → 435.625 (1.2026; VKM 92/2026)."""
    if m < "2023-04":
        return P_2022
    return P_2023 if m < "2026-01" else P_2026

def R_L95(m: str) -> float:
    """R sipas L95 (κ = 0,38 × P), me efekt nga 1.4.2023."""
    return R_95 if m < "2026-01" else R_95_2026

REFERENCAT = {"civile": ref_civile, "presidenti": ref_presidenti}

def R_paguar(m: str) -> int:
    """R e paguar faktikisht: 153.000 (4.2023–12.2025); 156.825 (1–7.2026, VKM 93/2026);
    gushti 2026 me vendim gjyqësor në nivelin e Këshillave; nga 9.2026 L95 = 0,38 × 435.625 (d)."""
    if m < "2026-01":
        return R_33
    if m < M_KESH:
        return R_33_2026
    if m == M_KESH:
        return R_KESH
    return R_95_2026

# ---------------------------------------------------------------------------
# 3. Formulat e modelit
# ---------------------------------------------------------------------------
def W(R, grupi="G2", vjet=0, drejtues="pa", antikorr=False):
    """(F1) W = R·[(1+γ)(1+λ+δ) + 0,02·min(y,25)] — paga mujore bruto totale."""
    return R * ((1 + GAMMA[grupi]) * (1 + LAMBDA[drejtues] + (DELTA_ANTIKORR if antikorr else 0))
                + VJETERSI * min(vjet, 25))

def faktori_W(grupi="G2", vjet=0, drejtues="pa", antikorr=False):
    """ω = W/R: shumëzuesi i profilit (konstant në R)."""
    return W(1.0, grupi, vjet, drejtues, antikorr)

def korridori(R_baze=R_V35):
    """(F2) [L, U] = [R_V35·(1+g_civ), R_V35·(1+g_P)] — riparimi i bazës (K6–K7). Konstruksion analitik (b)."""
    return R_baze * (1 + G_CIV), R_baze * (1 + G_PRES)

def pi_kumul(m_nga: str, m_deri: str) -> float:
    """π: inflacioni kumulativ nga m_nga në m_deri (jo normë vjetore)."""
    return ICHK[m_deri] / ICHK[m_nga] - 1

def rho_kumul(ref: str, m_nga: str, m_deri: str) -> float:
    """ρ: ndryshimi kumulativ i referencës së zgjedhur."""
    f = REFERENCAT[ref]
    return f(m_deri) / f(m_nga) - 1

def norma_indeksimit(pi: float, rho: float, rregulli="max", theta=None) -> float:
    """(F4) g = rritja e R në një datë rishikimi.
         'max'  : g = max(π, ρ)  — mbron njëkohësisht vlerën reale dhe ndjekjen e referencës;
                   NUK mblidhen (π + ρ) sepse rritja e referencës e përmban vetë inflacionin.
         'ichk' : g = π
         'ref'  : g = ρ
         'tavan': g = min(π, θ) — rregulli i L95 (θ = target BSH + 1 p.p., ne parametër)."""
    if rregulli == "max":
        return max(pi, rho)
    if rregulli == "ichk":
        return pi
    if rregulli == "ref":
        return rho
    if rregulli == "tavan":
        return min(pi, theta)
    raise ValueError(rregulli)

def rruga_minimale(R0: float, ref: str, skenari: str, deri="2026-12",
                   rregulli="max", theta=None) -> list[dict]:
    """(F5) Rruga më e ulët e R që plotëson të gjitha kufizimet, duke nisur nga R*_0 në 4.2023:
        R_t = max( R_{t-1},                                  [C3 mosregresion nominal, K4/K17]
                   R*_0 · Ref_t / Ref_0,                     [C4 ndjekja e referencës, K5/§92]
                   R_{τ_{k-1}} · (1+g_k)  në datën τ_k,      [C5 vlera reale në rishikim, K9/§§83–85]
                   236.425 nga 8.2026 vetëm në skenarin A )  [C6 dysheme e skenarit A]
    Inflacioni matet nga muaji para bazës (3.2023) deri në muajin para rishikimit, që të mos
    numërohet dy herë inflacioni 2022–23, i cili është tashmë brenda korridorit."""
    rows, R_prev = [], None
    m_rish_prev = M_BAZA
    R_rish_prev = R0
    for m in muajt(M_BAZA, deri):
        kandidatet = {"C4_referenca": R0 * REFERENCAT[ref](m) / REFERENCAT[ref](M_BAZA)}
        if R_prev is not None:
            kandidatet["C3_mosregresion"] = R_prev
        else:
            kandidatet["C1_baza"] = R0
        if m in RISHIKIMET:
            pi = pi_kumul(muaji_para(m_rish_prev), muaji_para(m))
            rho = rho_kumul(ref, m_rish_prev, m)
            g = norma_indeksimit(pi, rho, rregulli, theta)
            kandidatet["C5_rishikimi"] = R_rish_prev * (1 + g)
        if skenari == "A" and m >= M_KESH:
            kandidatet["C6_skenari_A"] = R_KESH
        lidhese = max(kandidatet, key=kandidatet.get)
        R_t = kandidatet[lidhese]
        if m in RISHIKIMET:
            m_rish_prev, R_rish_prev = m, R_t
        rows.append({"muaji": m, "R_min": R_t, "kufizimi_lidhes": lidhese,
                     "R_paguar": R_paguar(m), **{k: round(v, 2) for k, v in kandidatet.items()}})
        R_prev = R_t
    return rows

def prapambetja(rruga: list[dict], deri: str, omega=1.0) -> float:
    """(F6) A = ω · Σ_t (R_t − R_paguar_t)⁺, nga 4.2023 deri 'deri' (përfshirë). ω = 1 → në njësi R."""
    return omega * sum(max(r["R_min"] - r["R_paguar"], 0) for r in rruga if r["muaji"] <= deri)

def kosto_vjetore(R_e_re: float, R_aktuale: float = R_95_2026, n_r: float = N_R["qendror"],
                  kontribute: float = 0.0) -> float:
    """(F7) ΔC = 12 · N_R · (R_e_re − R_L95,2026) · (1 + c); krahasuesi: L95 me P = 435.625."""
    return 12 * n_r * (R_e_re - R_aktuale) * (1 + kontribute)

def kontrollo(rruga_R: dict[str, float], R0: float, ref: str, skenari: str,
              rregulli="max", theta=None) -> dict[str, bool]:
    """(F8) Testi i realizueshmërisë për çdo rrugë të propozuar R_t (përdoret në 2b dhe 2d).
    Rezultati varet nga rregulli i indeksimit të zgjedhur për C5: asnjë variant nuk etiketohet
    paraprakisht si kushtetues (korrigjimi metodologjik 5)."""
    L, U = korridori()
    minr = {r["muaji"]: r["R_min"] for r in rruga_minimale(R0, ref, skenari, deri=max(rruga_R),
                                                            rregulli=rregulli, theta=theta)}
    mujore = sorted(rruga_R)
    return {
        "C1_korridori": L <= R0 <= U,
        "C3_mosregresion": all(rruga_R[b] >= rruga_R[a] for a, b in zip(mujore, mujore[1:])),
        "C4_C5_C6_mbi_rrugen_min": all(rruga_R[m] >= minr[m] - 0.5 for m in mujore if m in minr),
    }

# ---------------------------------------------------------------------------
# 4. Fjalori i simboleve
# ---------------------------------------------------------------------------
FJALORI = [
    ("t", "muaji kalendarik (YYYY-MM)", "muaj", "—"),
    ("R_t", "paga referuese bazë e magjistratit në muajin t", "lekë/muaj bruto", "L96 neni 12"),
    ("R*_0", "baza e riparuar në 1.4.2023", "lekë/muaj bruto", "V15 §§109–110"),
    ("R_V35", "e drejta e fituar, shtator 2022 = 152.700", "lekë/muaj bruto", "V15 §95; VKM 621/2022"),
    ("P_t", "paga e Presidentit", "lekë/muaj bruto", "ligji 34/2023"),
    ("κ", "koeficienti R/P", "numër i pastër", "L95 neni 1"),
    ("Ref_t", "referenca e zgjedhur: civile (I-2 + 14.000) ose P_t", "lekë/muaj", "V15 §109"),
    ("W", "paga mujore bruto totale e një magjistrati", "lekë/muaj bruto", "L96 nenet 2/j, 12, 14"),
    ("ω", "shumëzuesi i profilit, W/R", "numër i pastër", "F1"),
    ("γ, λ, δ, y", "shtesa e grupit, shtesa drejtuese, shtesa GJKKO/SPAK, vitet e vjetërsisë", "numra të pastër; vite", "L96"),
    ("g_civ, g_P", "rritjet e referencave 2022→2023: 44% dhe 65,4%", "përqindje kumulative", "V15 §100"),
    ("L, U", "kufiri i poshtëm dhe i sipërm i korridorit për R*_0", "lekë/muaj", "F2 (konstruksion b)"),
    ("I_t", "indeksi i çmimeve të konsumit (IÇK kombëtar)", "indeks", "INSTAT"),
    ("π", "inflacioni kumulativ ndërmjet dy muajve", "përqindje kumulative", "F3"),
    ("ρ", "ndryshimi kumulativ i referencës ndërmjet dy muajve", "përqindje kumulative", "F3"),
    ("g", "rritja e R në një datë rishikimi", "përqindje kumulative", "F4"),
    ("θ", "tavani i indeksimit (target BSH + 1 p.p.)", "pikë përqindjeje / përqindje", "ligji 33/2023; L95"),
    ("τ_k", "data e rishikimit k (çdo ≤ 2 vjet, e para 1.1.2026)", "muaj", "ligji 33/2023; L95"),
    ("A", "prapambetja (diferenca e papaguar e akumuluar)", "lekë bruto", "F6"),
    ("N_R", "njësi-R: Σ W_i / R, kosto mujore për 1 lekë rritje të R", "numër (magjistratë-ekuivalentë)", "Faza 1 §4.5"),
    ("c", "norma e kontributeve të punëdhënësit", "përqindje", "AN 2/2026"),
    ("ΔC", "kosto shtesë vjetore", "lekë/vit", "F7"),
    ("A/B", "skenarët juridikë: A = aktet e Këshillave të vlefshme; B = pa kompetencë", "—", "Faza 1, P1"),
]

# ---------------------------------------------------------------------------
# 5. Ekzekutimi
# ---------------------------------------------------------------------------
def main():
    rez = []
    def out(seksioni, treguesi, vlera, shenim=""):
        rez.append({"seksioni": seksioni, "treguesi": treguesi,
                    "vlera": round(vlera, 4) if isinstance(vlera, float) else vlera, "shenim": shenim})

    # F2 korridori
    L, U = korridori()
    out("F2", "L = 152.700 × 1,44", L, "(b) kufi i poshtëm")
    out("F2", "U = 152.700 × 425.000/257.000", U, "(b) kufi i sipërm")
    out("F2", "g_civ ekzakt (II-a 118.100 → I-5 170.000)", G_CIV_EKZAKT)
    out("F2", "L me g_civ ekzakt", R_V35 * (1 + G_CIV_EKZAKT), "ndjeshmëri e rrumbullakimit të 44%")
    out("F2", "κ në L", L / P_2023); out("F2", "κ në U", U / P_2023)

    # F3 inflacioni dhe referencat
    out("F3", "π 3.2023→12.2025 (rishikimi 1.1.2026)", pi_kumul("2023-03", "2025-12"))
    out("F3", "π 3.2023→8.2026", pi_kumul("2023-03", "2026-08"))
    out("F3", "π 8.2022→3.2023 (tashmë brenda korridorit)", pi_kumul("2022-08", "2023-03"))
    out("F3", "ρ civile 4.2023→1.2026", rho_kumul("civile", "2023-04", "2026-01"))
    out("F3", "ρ Presidenti 4.2023→1.2026", rho_kumul("presidenti", "2023-04", "2026-01"))
    out("F3", "ρ civile 9.2022→4.2023", rho_kumul("civile", "2022-09", "2023-04"), "gjurma e saktë sipas V35")

    # F4 shembull i rregullit të indeksimit
    pi26 = pi_kumul("2023-03", "2025-12"); rho26 = rho_kumul("civile", "2023-04", "2026-01")
    for rr, th in [("max", None), ("ichk", None), ("ref", None), ("tavan", 0.04)]:
        out("F4", f"g në 1.1.2026, rregulli '{rr}'", norma_indeksimit(pi26, rho26, rr, th))
    out("F4", "g e gabuar me mbledhje (π + ρ)", pi26 + rho26, "numërim i dyfishtë — përjashtohet")

    # F5 rrugët minimale nga L
    rruget = []
    for ref in ("civile", "presidenti"):
        for sk in ("A", "B"):
            rr = rruga_minimale(L, ref, sk)
            for r in rr:
                rruget.append({"R0": round(L, 2), "referenca": ref, "skenari": sk, **r})
            byM = {r["muaji"]: r for r in rr}
            for m in ("2023-04", "2025-12", "2026-01", "2026-07", "2026-08", "2026-12"):
                out("F5", f"R_min {m} | ref {ref} | skenari {sk}", byM[m]["R_min"], byM[m]["kufizimi_lidhes"])
            # F6 prapambetja deri 7.2026 dhe deri 12.2026
            for deri in ("2026-07", "2026-12"):
                a = prapambetja(rr, deri)
                out("F6", f"A në njësi R, 4.2023–{deri} | ref {ref} | sk {sk}", a)
                out("F6", f"A agregat (N_R qendror), 4.2023–{deri} | ref {ref} | sk {sk}", a * N_R["qendror"])
            # F7 kosto vjetore nga 2027 (R e dhjetorit 2026 kundrejt L95)
            R_dhj = byM["2026-12"]["R_min"]
            for k, n in N_R.items():
                out("F7", f"ΔC/vit kundrejt L95, N_R {k} | ref {ref} | sk {sk}", kosto_vjetore(R_dhj, n_r=n))
            out("F7", f"ΔC/vit me kontribute 16,6%, N_R qendror | ref {ref} | sk {sk}",
                kosto_vjetore(R_dhj, kontribute=KONTRIBUTE))

    # Ndjeshmëria: rruga minimale nga L me rregullin e tavanit θ = 4% (L95), ref civile, skenari B
    rr_t = rruga_minimale(L, "civile", "B", rregulli="tavan", theta=0.04)
    rr_m = rruga_minimale(L, "civile", "B", rregulli="max")
    out("F5-ndj", "R 2026-01 me tavan 4% (ref civile, B)", rr_t[33]["R_min"], rr_t[33]["kufizimi_lidhes"])
    out("F5-ndj", "R 2026-01 me max(π,ρ) (ref civile, B)", rr_m[33]["R_min"], rr_m[33]["kufizimi_lidhes"])
    out("F5-ndj", "Erozioni real nga tavani 4%, 1.2026", rr_t[33]["R_min"] / rr_m[33]["R_min"] - 1)

    # Vetitë strukturore (§6.4)
    Rb = rruga_minimale(L, "civile", "B")[-1]["R_min"]
    out("6.4", "Diferenca A − B në R nga 8.2026 (rruga minimale)", R_KESH - Rb)
    out("6.4", "R e Këshillave mbi rrugën minimale B, 2026", R_KESH / Rb - 1)
    out("F7", "R_Këshillave − R_L95 (2026)", R_KESH - R_95_2026)

    # Shembuj të riprodhueshëm
    shembuj = []
    def sh(formula, hyrja, rezultati):
        shembuj.append({"formula": formula, "hyrja": hyrja,
                        "rezultati": round(rezultati, 4) if isinstance(rezultati, float) else rezultati})
    sh("F1", "W(R=219.888; G2; y=15; pa drejtues)", W(L, "G2", 15))
    sh("F1", "ω(G2; y=15)", faktori_W("G2", 15))
    sh("F1", "W(R=165.537,5; G2; y=15)", W(R_95_2026, "G2", 15))
    sh("F1", "W(R=118.100; G3; y=25; kryetar) — kontroll KLSH 326.664", W(118_100, "G3", 25, "kryetar"))
    sh("F2", "L = 152.700 × 1,44", L)
    sh("F3", "π = I(2025-12)/I(2023-03) − 1", pi26)
    sh("F4", "g = max(π, ρ) në 1.1.2026, ref civile", norma_indeksimit(pi26, rho26))
    sh("F5", "R_min 2026-01, R*_0 = L, ref civile, B", rr_m[33]["R_min"])
    sh("F6", "A për G2 y=15, 4.2023–7.2026, R*_0 = L, ref civile",
       prapambetja(rr_m, "2026-07", faktori_W("G2", 15)))
    sh("F7", "ΔC/vit, R = 236.425 kundrejt 165.537,5, N_R = 3.954", kosto_vjetore(R_KESH))
    # Rruga e Këshillave (KLGJ 435): 231.000 për 4.2023–12.2025; 236.425 nga 1.2026 (c)
    kesh = {m: (231_000 if m < "2026-01" else R_KESH) for m in muajt("2023-04", "2026-12")}
    for rr, th in [("max", None), ("ref", None), ("tavan", 0.04)]:
        sh("F8", f"kontrollo(rruga e Këshillave; R*_0 = 231.000; civile; A; C5 = '{rr}')",
           str(kontrollo(kesh, 231_000, "civile", "A", rr, th)))
    for rr, th in [("max", None), ("tavan", 0.04)]:
        mn = {r["muaji"]: r["R_min"] for r in rruga_minimale(231_000, "civile", "A", rregulli=rr, theta=th)}
        out("F8", f"Dyshemeja C5 në 1.2026 për R*_0 = 231.000, rregulli '{rr}'", mn["2026-01"])
        out("F8", f"Mungesa e rrugës së Këshillave ndaj dyshemesë C5 në 1.2026, '{rr}'", mn["2026-01"] - R_KESH)

    # Shkrimi
    def shkruaj(emri, rreshtat):
        with open(DIR / emri, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(dict.fromkeys(k for r in rreshtat for k in r)))
            w.writeheader(); w.writerows(rreshtat)
    shkruaj("faza2a_rezultatet.csv", rez)
    shkruaj("faza2a_rruget_min.csv", rruget)
    shkruaj("faza2a_shembuj.csv", shembuj)
    shkruaj("faza2a_fjalori.csv", [dict(zip(("simboli", "kuptimi", "njesia", "burimi"), r)) for r in FJALORI])
    for r in rez:
        print(f'{r["seksioni"]:7s} {r["treguesi"]:70s} {r["vlera"]!s:>18s}  {r["shenim"]}')
    print("\nShembuj:")
    for s in shembuj:
        print(f'{s["formula"]:4s} {s["hyrja"]:70s} {s["rezultati"]}')

if __name__ == "__main__":
    main()
