"""
Faza 2d — §9: analiza fiskale 2027–2031, testi historik 2019–2026, testet K1–K18, vlera reale,
korridori, ndjeshmëria/stresi dhe kontrolli përfundimtar i konsistencës së Fazës 2.

Dalja:
  faza2d_fiskale_grid.csv     72 kombinime skenarësh × 5 vjet
  faza2d_historik.csv         testi kundërfaktik 1.2019–8.2026 (muaj pas muaji)
  faza2d_stresi.csv           skenarët e stresit
  faza2d_K.csv                testet numerike të matricës K
  faza2d_konsistenca.csv      çdo numër i §§6–9 dhe a gjendet në CSV
  faza2d_rezultatet.csv       çdo shifër e përdorur në §9
Ekzekutimi: python3 faza2d_testet.py
"""
import csv, itertools, re, subprocess, sys
from pathlib import Path
from faza2a_model import (DIR, R_V35, R_33, R_95, R_95_2026, R_33_2026, R_KESH, I2, SHTESA_GRUP, ICHK, N_R, KONTRIBUTE,
                          muajt, muaji_para, korridori, faktori_W)
from faza2c_paketa import R0_PAKETE
import faza2c_lp as lp

PAGA_SHTET_2026 = 120.3e9   # fondi i pagave i buxhetit të shtetit 2026 (AN 2/2026) (c)
DEFICITI_2026 = 63.7e9      # deficiti 2026 (AN 2/2026) (c)
L, U = korridori()
I_BAZA = ICHK["2023-03"]
F_ICHK_2026 = ICHK["2025-12"] / I_BAZA
REF0 = I2["2023-04"] + SHTESA_GRUP
VITET = [2027, 2028, 2029, 2030, 2031]
RISH_VITET = (2028, 2030)

# ---------------------------------------------------------------------------
# Indeksi i çmimeve në fund të çdo viti, sipas skenarit: real deri 8.2026, pastaj π vjetore
# ---------------------------------------------------------------------------
def I_dhj(viti, pi_seq):
    """pi_seq: dict viti → π vjetore (2026 përdoret për 9–12.2026)."""
    I = ICHK["2026-08"] * (1 + pi_seq[2026]) ** (4 / 12)
    for y in range(2027, viti + 1):
        I *= 1 + pi_seq[y]
    return I if viti >= 2026 else None

def I_muaj(m, pi_seq):
    if m in ICHK:
        return ICHK[m]
    y, mm = map(int, m.split("-"))
    I_prev = I_dhj(y - 1, pi_seq) if y > 2026 else ICHK["2026-08"]
    k = mm if y > 2026 else mm - 8
    return I_prev * (1 + pi_seq[y]) ** (k / 12)

def rruget_vjetore(pi_seq, rho, rish_shtese=None):
    """R mesatare vjetore (konstante brenda vitit) e paketës dhe e L95 për 2027–2031."""
    R_p, R_l = {}, {}
    f_I = F_ICHK_2026
    Rp_prev, Rl_prev, Il_rish = 243_538.6221, R_95_2026, ICHK["2025-12"]
    for y in VITET:
        ref_y = I2["2026-01"] * (1 + rho) ** (y - 2026) + SHTESA_GRUP
        if y in RISH_VITET or (rish_shtese and y in rish_shtese):
            f_I = I_dhj(y - 1, pi_seq) / I_BAZA
        Rp = max(Rp_prev, R0_PAKETE * max(f_I, ref_y / REF0))
        Rl = Rl_prev
        # L95: R = 0,38 × P; P indeksohet çdo vit me VKM (2026: 2,5%, si pagat civile). Supozim (d):
        # P ndjek ρ, brenda tavanit 4% të L95.
        Rl = Rl_prev * (1 + min(rho, 0.04))
        R_p[y], R_l[y] = Rp, Rl
        Rp_prev, Rl_prev = Rp, Rl
    return R_p, R_l

def stres_mujor(pi_seq, rho, theta_jashtezak=None, deri="2031-12"):
    """Rruga mujore e paketës 1.2026–12.2031. Rishikime të rregullta 1.2028, 1.2030; opsionalisht
    rishikim i jashtëzakonshëm në muajin pas atij kur π kumulative nga matja e fundit kalon θ.
    Kthen humbjen reale maksimale ndaj 231.000 të indeksuar plotësisht dhe muajt e rishikimeve."""
    m_mat = "2025-12"; f_I = F_ICHK_2026; R_prev = 243_538.6221
    rishikime, humbja_maks, muaji_maks = [], 0.0, None
    for m in muajt("2026-01", deri):
        y, mm = map(int, m.split("-"))
        mp = muaji_para(m)
        i_mp = I_muaj(mp, pi_seq)
        rregull = mm == 1 and y in RISH_VITET
        jashtez = (theta_jashtezak is not None and not rregull and m != "2026-01"
                   and i_mp / I_muaj(m_mat, pi_seq) - 1 > theta_jashtezak)
        if rregull or jashtez:
            f_I = i_mp / I_BAZA; m_mat = mp; rishikime.append(m + ("*" if jashtez else ""))
        ref = I2["2026-01"] * (1 + rho) ** (y - 2026) + SHTESA_GRUP if y > 2026 else I2["2026-01"] + SHTESA_GRUP
        R = max(R_prev, R0_PAKETE * max(f_I, ref / REF0))
        h = R / (R0_PAKETE * I_muaj(m, pi_seq) / I_BAZA) - 1
        if h < humbja_maks:
            humbja_maks, muaji_maks = h, m
        R_prev = R
    return humbja_maks, muaji_maks, rishikime

# ---------------------------------------------------------------------------
# Prapambetjet dhe kompensimi sipas vitit (nga LP i 2c)
# ---------------------------------------------------------------------------
_lp_cache = {}
def prapambetje_vjetore(n_r, pi_seq, B=5e9, vitet=(2027, 2028, 2029)):
    key = (n_r, B, vitet)
    if key not in _lp_cache:
        _lp_cache[key] = lp.zgjidh(list(vitet), {y: B for y in vitet}, 0.10, n_r=n_r)
    r = _lp_cache[key]
    pag = {y: 0.0 for y in VITET}; komp = {y: 0.0 for y in VITET}
    for m, y, v in r["kalendari"]:
        pag[y] += v
        komp[y] += v * (I_muaj(f"{y}-07", pi_seq) / I_muaj(m, pi_seq) - 1)
    return pag, komp, r["hendeku"], r["A"]

# ---------------------------------------------------------------------------
def main():
    rez = []
    def out(s, t, v, sh=""):
        rez.append({"seksioni": s, "treguesi": t, "vlera": round(v, 6) if isinstance(v, float) else v, "shenim": sh})
    def shkruaj(emri, rreshtat):
        with open(DIR / emri, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rreshtat for k in r)))
            w.writeheader(); w.writerows(rreshtat)

    # ============ 1. Analiza fiskale ============
    grid = []
    for pi, rho, (nk, nr), c in itertools.product((0.02, 0.03, 0.04, 0.05), (0.0, 0.025, 0.05),
                                                  N_R.items(), (0.0, KONTRIBUTE)):
        pi_seq = {y: pi for y in range(2026, 2032)}
        Rp, Rl = rruget_vjetore(pi_seq, rho)
        pag, komp, hend, A = prapambetje_vjetore(nr, pi_seq)
        for y in VITET:
            perm = 12 * nr * (Rp[y] - Rl[y]) * (1 + c)
            kal = (pag[y] + komp[y]) * (1 + c)
            grid.append({"pi": pi, "rho": rho, "N_R": nk, "c": c, "viti": y,
                         "R_paketa": round(Rp[y]), "R_L95": round(Rl[y]),
                         "kosto_e_perhershme": round(perm), "kosto_kalimtare": round(kal),
                         "totali": round(perm + kal), "pjesa_e_fondit_2026": round((perm + kal) / PAGA_SHTET_2026, 5),
                         "hendeku_prapambetjes_pas_2029": round(hend * (1 + c)) if y == 2029 else 0})
    shkruaj("faza2d_fiskale_grid.csv", grid)
    qend = [g for g in grid if g["pi"] == 0.03 and g["rho"] == 0.025 and g["N_R"] == "qendror" and g["c"] == 0.0]
    for g in qend:
        y = g["viti"]
        out("9.1", f"Qendror | {y} | R paketa", g["R_paketa"]); out("9.1", f"Qendror | {y} | R L95", g["R_L95"])
        out("9.1", f"Qendror | {y} | e përhershme (mld)", g["kosto_e_perhershme"] / 1e9)
        out("9.1", f"Qendror | {y} | kalimtare (mld)", g["kosto_kalimtare"] / 1e9)
        out("9.1", f"Qendror | {y} | totali (mld)", g["totali"] / 1e9)
        out("9.1", f"Qendror | {y} | pjesa e fondit 2026", g["pjesa_e_fondit_2026"])
    out("9.1", "Qendror | 5 vjet | totali (mld)", sum(g["totali"] for g in qend) / 1e9)
    out("9.1", "Qendror | 5 vjet | e përhershme (mld)", sum(g["kosto_e_perhershme"] for g in qend) / 1e9)
    out("9.1", "Qendror | 5 vjet | kalimtare (mld)", sum(g["kosto_kalimtare"] for g in qend) / 1e9)
    for y in VITET:
        gy = [g for g in grid if g["viti"] == y]
        out("9.1", f"Gama | {y} | totali min (mld)", min(g["totali"] for g in gy) / 1e9)
        out("9.1", f"Gama | {y} | totali maks (mld)", max(g["totali"] for g in gy) / 1e9)
        out("9.1", f"Gama | {y} | pjesa maks e fondit", max(g["pjesa_e_fondit_2026"] for g in gy))
    maks = max(grid, key=lambda g: g["totali"])
    out("9.1", "Viti dhe skenari i kulmit", f'{maks["viti"]}: π {maks["pi"]}, ρ {maks["rho"]}, N_R {maks["N_R"]}, c {maks["c"]}')
    out("9.1", "Kulmi (mld)", maks["totali"] / 1e9)
    out("9.1", "Kulmi / deficiti 2026", maks["totali"] / DEFICITI_2026)
    hendeqe = [g for g in grid if g["hendeku_prapambetjes_pas_2029"] > 0]
    out("9.1", "Kombinime me hendek prapambetjesh pas 2029 (B = 5 mld/vit)", len({(g["N_R"], g["c"]) for g in hendeqe}))
    out("9.1", "Hendeku maks (mld)", max([g["hendeku_prapambetjes_pas_2029"] for g in grid] + [0]) / 1e9)
    # ndjeshmëria e kostos së përhershme 2031 ndaj ρ (π 3%, N_R qendror)
    for rho in (0.0, 0.025, 0.05):
        g = next(g for g in grid if g["pi"] == 0.03 and g["rho"] == rho and g["N_R"] == "qendror" and g["c"] == 0 and g["viti"] == 2031)
        out("9.1", f"2031 | ρ {rho} | e përhershme (mld)", g["kosto_e_perhershme"] / 1e9)
        out("9.1", f"2031 | ρ {rho} | R paketa", g["R_paketa"])

    # ============ 2. Testi historik kundërfaktik 1.2019–8.2026 ============
    R0_h = 129_800 + SHTESA_GRUP          # 143.800 = standardi i V35 më 1.1.2019 (V35 §§77, 80) (c)
    def ref_hist(m):
        if m < "2022-09": return 129_800 + SHTESA_GRUP
        if m < "2023-04": return 138_700 + SHTESA_GRUP
        if m < "2026-01": return I2["2023-04"] + SHTESA_GRUP
        return I2["2026-01"] + SHTESA_GRUP
    def paguar_hist(m):
        if m < "2023-01": return 118_100         # zbatimi i gabuar (V15 §35); KLSH GJL 2023
        if m < "2023-04": return 152_700 if False else 118_100
        if m < "2026-01": return R_33
        if m < "2026-08": return R_33_2026
        return R_KESH if m == "2026-08" else R_95_2026
    rish_h = ["2021-01", "2023-01", "2025-01"]
    hist, R_prev = [], None
    for m in muajt("2019-01", "2026-08"):
        tau = max([r for r in rish_h if r <= m], default=None)
        fI = ICHK[muaji_para(tau)] / ICHK["2018-12"] if tau else 1.0
        fr = ref_hist(m) / ref_hist("2019-01")
        Rk = R0_h * max(fI, fr)
        Rk = max(Rk, R_prev) if R_prev else Rk
        hist.append({"muaji": m, "R_kunderfaktike": round(Rk, 2), "R_paguar_faktike": paguar_hist(m),
                     "R_V35_standardi": ref_hist(m), "R_vlera_reale_143800": round(R0_h * ICHK[m] / ICHK["2018-12"], 2)})
        R_prev = Rk
    shkruaj("faza2d_historik.csv", hist)
    H = {h["muaji"]: h for h in hist}
    for m in ("2019-01", "2021-01", "2022-12", "2023-01", "2023-03", "2023-04", "2025-01", "2026-01", "2026-08"):
        for k in ("R_kunderfaktike", "R_paguar_faktike", "R_vlera_reale_143800"):
            out("9.2", f"{m} | {k}", H[m][k])
    out("9.2", "Kundërfaktike 3.2023 / 152.700 − 1", H["2023-03"]["R_kunderfaktike"] / R_V35 - 1)
    out("9.2", "Kundërfaktike 4.2023 = R*_0 e paketës?", H["2023-04"]["R_kunderfaktike"] == R0_PAKETE)
    out("9.2", "Kundërfaktike 8.2026 / paketa 8.2026 − 1", H["2026-08"]["R_kunderfaktike"] / 243_538.6221 - 1)
    out("9.2", "Mungesa maksimale e R të paguar ndaj kundërfaktikes, lekë/muaj",
        max(h["R_kunderfaktike"] - h["R_paguar_faktike"] for h in hist))
    out("9.2", "Pikat ku kundërfaktikja ra nën vlerën reale të 143.800 (muaj)",
        sum(1 for h in hist if h["R_kunderfaktike"] < h["R_vlera_reale_143800"] - 0.5))
    out("9.2", "Mungesa maksimale reale e kundërfaktikes ndaj 143.800 të indeksuar",
        min(h["R_kunderfaktike"] / h["R_vlera_reale_143800"] - 1 for h in hist))

    # ============ 4. Vlera reale dhe korridori ============
    v152 = R_V35 * ICHK["2026-08"] / ICHK["2022-09"]
    v231 = R0_PAKETE * ICHK["2026-08"] / I_BAZA
    out("9.4", "Vlera e 152.700 (9.2022) në çmimet e 8.2026", v152)
    out("9.4", "Vlera e 231.000 (3.2023) në çmimet e 8.2026", v231)
    out("9.4", "Paketa 8.2026 / vlera reale e 152.700 − 1", 243_538.6221 / v152 - 1)
    out("9.4", "Paketa 8.2026 / vlera reale e 231.000 − 1", 243_538.6221 / v231 - 1)
    out("9.4", "L95 / vlera reale e 152.700 − 1", R_95_2026 / v152 - 1)
    out("9.4", "L95 / vlera reale e 231.000 − 1", R_95_2026 / v231 - 1)
    out("9.4", "Paketa: R*_0 brenda [L, U]", L <= R0_PAKETE <= U)
    out("9.4", "L95: R brenda [L, U]", L <= R_95 <= U)
    out("9.4", "Paketa 8.2026 ≥ 236.425 (C6, skenari A)", 243_538.6221 >= R_KESH)

    # ============ 5. Stresi ============
    stres = []
    baza_pi = {y: 0.03 for y in range(2026, 2032)}
    sken = {
        "S-a: episod si 2022–23 (7% në 2027, 5% në 2028), ρ 2,5%": ({**baza_pi, 2027: 0.067, 2028: 0.048}, 0.025, None),
        "S-b: ngrirje e pagave civile (ρ 0), π 3%": (baza_pi, 0.0, None),
        "S-c: bazë (π 3%, ρ 2,5%)": (baza_pi, 0.025, None),
    }
    for emri, (ps, rho, ext) in sken.items():
        Rp, Rl = rruget_vjetore(ps, rho, rish_shtese=ext)
        for y in VITET:
            # humbja reale në fund të vitit, ndaj vlerës reale të R*_0 (231.000 e indeksuar plotësisht)
            reale = Rp[y] / (R0_PAKETE * I_dhj(y, ps) / I_BAZA) - 1
            ref_y = I2["2026-01"] * (1 + rho) ** (y - 2026) + SHTESA_GRUP
            stres.append({"skenari": emri, "viti": y, "R_paketa": round(Rp[y]), "R_L95": round(Rl[y]),
                          "humbja_reale_ne_fund_te_vitit": round(reale, 4),
                          "raporti_me_referencen": round(Rp[y] / ref_y, 4),
                          "humbja_reale_L95": round(Rl[y] / (R_95_2026 * I_dhj(y, ps) / ICHK["2025-12"]) - 1, 4)})
        worst = min(s["humbja_reale_ne_fund_te_vitit"] for s in stres if s["skenari"] == emri)
        out("9.5", f"{emri} | humbja reale maks e paketës (fund viti)", worst)
        out("9.5", f"{emri} | humbja reale maks e L95 (fund viti)",
            min(s["humbja_reale_L95"] for s in stres if s["skenari"] == emri))
        out("9.5", f"{emri} | raporti R/referencë 2031", stres[-1]["raporti_me_referencen"])
    for emri, ps, rho, th in [
        ("Mujor | bazë π 3%", baza_pi, 0.025, None),
        ("Mujor | episod 2022–23, pa rishikim të jashtëzakonshëm", {**baza_pi, 2027: 0.067, 2028: 0.048}, 0.025, None),
        ("Mujor | episod 2022–23, rishikim i jashtëzakonshëm θ = 4%", {**baza_pi, 2027: 0.067, 2028: 0.048}, 0.025, 0.04),
        ("Mujor | bazë π 3%, rishikim i jashtëzakonshëm θ = 4%", baza_pi, 0.025, 0.04),
    ]:
        hm, mm_, rish = stres_mujor(ps, rho, th)
        out("9.5", f"{emri} | humbja reale maks (mujore)", hm)
        out("9.5", f"{emri} | muaji i humbjes maks", mm_)
        out("9.5", f"{emri} | rishikimet", " ".join(rish))
        stres.append({"skenari": emri, "humbja_reale_maks_mujore": round(hm, 4), "muaji": mm_, "rishikimet": " ".join(rish)})
    # S-c: rënie e të ardhurave → tavan 3 mld/vit për prapambetjet
    for vitet in ((2027, 2028, 2029), (2027, 2028, 2029, 2030, 2031)):
        r = lp.zgjidh(list(vitet), {y: 3e9 for y in vitet}, 0.10)
        tag = f"S-c: tavan 3 mld/vit, {vitet[0]}–{vitet[-1]}"
        out("9.5", f"{tag} | hendeku (mld)", r["hendeku"] / 1e9)
        out("9.5", f"{tag} | vonesa mesatare (muaj)", r["vonesa_mesatare_muaj"])
        out("9.5", f"{tag} | kompensimi IÇK (mld)", r["kompensimi_IÇK"] / 1e9)
        stres.append({"skenari": tag, "hendeku_mld": round(r["hendeku"] / 1e9, 4),
                      "vonesa_mesatare_muaj": round(r["vonesa_mesatare_muaj"], 2)})
    shkruaj("faza2d_stresi.csv", stres)

    # ============ 3. Testet numerike K ============
    K = [
        ("K4/K5", "R ndjek referencën (rritja e R ≥ rritja e Ref nga 4.2023 në 1.2026)",
         243_538.6221 / R0_PAKETE >= (I2["2026-01"] + SHTESA_GRUP) / REF0, R_95_2026 / R_95 >= (I2["2026-01"] + SHTESA_GRUP) / REF0),
        ("K6/K7", "R*_0 brenda korridorit [219.888; 252.519]", L <= R0_PAKETE <= U, L <= R_95 <= U),
        ("K9", "R 8.2026 ≥ vlera reale e 152.700", 243_538.6221 >= v152, R_95_2026 >= v152),
        ("K13/C6", "R nga 8.2026 ≥ 236.425 (skenari A)", 243_538.6221 >= R_KESH, R_95_2026 >= R_KESH),
        ("K14", "Raportet e hierarkisë të pandryshuara (W lineare)", True, True),
    ]
    shkruaj("faza2d_K.csv", [{"K": k, "testi": t, "paketa": p, "L95": l} for k, t, p, l in K])

    shkruaj("faza2d_rezultatet.csv", rez)
    # Konstantet burimore (c), që teksti i citon drejtpërdrejt
    shkruaj("faza2d_konstantet.csv", [
        {"konstantja": "P 2023–2026", "vlera": 425_000, "burimi": "ligji 34/2023; KDNJMIP"},
        {"konstantja": "P 2022", "vlera": 257_000, "burimi": "V15 §42"},
        {"konstantja": "R_V35", "vlera": R_V35, "burimi": "VKM 621/2022; V15 §95"},
        {"konstantja": "I-2 2023", "vlera": I2["2023-04"], "burimi": "VKM 325/2023"},
        {"konstantja": "I-2 2026", "vlera": I2["2026-01"], "burimi": "VKM 131/2026"},
        {"konstantja": "R e Këshillave", "vlera": R_KESH, "burimi": "KLGJ 435; KLP 144"},
        {"konstantja": "Fondi i pagave 2026", "vlera": PAGA_SHTET_2026, "burimi": "AN 2/2026"},
        {"konstantja": "Deficiti 2026", "vlera": DEFICITI_2026, "burimi": "AN 2/2026"},
        {"konstantja": "0,594 × 425.000", "vlera": 0.594 * 425_000, "burimi": "llogaritje"},
        {"konstantja": "I-b 2019", "vlera": 129_800, "burimi": "VKM 187/2017"},
        {"konstantja": "I-b 9.2022", "vlera": 138_700, "burimi": "VKM 621/2022"},
        {"konstantja": "R 2019 sipas V35", "vlera": 129_800 + SHTESA_GRUP, "burimi": "V35 §§77, 80"},
        {"konstantja": "R e zbatuar gabimisht", "vlera": 118_100, "burimi": "V15 §35"},
        {"konstantja": "P 2026", "vlera": 435_625, "burimi": "VKM 92/2026"},
        {"konstantja": "I-5 nga 1.4.2023", "vlera": 170_000, "burimi": "VKM 325/2023 Lidhja 1"},
        {"konstantja": "Diferenca 231.000 − 152.700 sipas Shoqatës", "vlera": 78_300, "burimi": "V15 §21.3"},
        {"konstantja": "R e paguar 1–7.2026", "vlera": R_33_2026, "burimi": "VKM 93/2026"},
        {"konstantja": "L95 me P 2026", "vlera": R_95_2026, "burimi": "0,38 × 435.625"},
    ])

    # ============ 6. Kontrolli përfundimtar i konsistencës ============
    konsistenca(out_csv=True)
    for r in rez:
        print(f'{r["seksioni"]:6s} {r["treguesi"]:95s} {r["vlera"]}')

# ---------------------------------------------------------------------------
def konsistenca(out_csv=False):
    """Rillogarit të gjithë skriptet e Fazës 2 dhe kontrollon çdo numër në §§6–9 të tekstit
    kundrejt vlerave në CSV (me tolerancë rrumbullakimi sipas numrit të shifrave të shfaqura)."""
    for s in ("faza2a_model.py", "faza2_burimet_shtese.py", "faza2b_alternativat.py",
              "faza2c_paketa.py", "faza2c_lp.py"):
        subprocess.run([sys.executable, s], cwd=DIR, check=True, capture_output=True)
    vals = []
    for f in sorted(DIR.glob("faza2*.csv")) + [DIR / "faza1_rezultatet.csv"]:
        if f.name == "faza2d_konsistenca.csv":
            continue
        for row in csv.reader(open(f, encoding="utf-8")):
            for cell in row:
                for tok in re.findall(r"-?\d+(?:\.\d+)?(?:e[+-]?\d+)?", cell):
                    try:
                        vals.append(abs(float(tok)))
                    except ValueError:
                        pass
    vals = sorted(set(vals))
    import bisect
    def gjendet(x, tol):
        cands = [x, x / 100, x * 1e9, x * 1e6]
        for c in cands:
            t = tol * (c / x if x else 1)
            i = bisect.bisect_left(vals, c - t)
            if i < len(vals) and vals[i] <= c + t:
                return True
        return False
    tekst = open(DIR / "Faza2_pagat_magjistrateve.md", encoding="utf-8").read()
    rreshtat = []
    for nr, line in enumerate(tekst.splitlines(), 1):
        for tok in re.findall(r"(?<![\w§/.-])\d{1,3}(?:\.\d{3})+(?:,\d+)?(?![\d.])|(?<![\w§/.-])\d+,\d+(?!\d)", line):
            if re.fullmatch(r"\d{1,2}\.20\d\d", tok):      # data muaj.vit, jo shifër
                continue
            s = tok.replace(".", "").replace(",", ".")
            x = float(s)
            dec = len(s.split(".")[1]) if "." in s else 0
            tol = 0.5 * 10 ** (-dec) + 1e-9
            ok = gjendet(x, tol) or gjendet(x, tol * 1.0001 + 0.5)
            rreshtat.append({"rreshti": nr, "numri": tok, "gjendet_ne_CSV": ok, "konteksti": line.strip()[:140]})
    if out_csv:
        with open(DIR / "faza2d_konsistenca.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["rreshti", "numri", "gjendet_ne_CSV", "konteksti"])
            w.writeheader(); w.writerows(rreshtat)
    return rreshtat

if __name__ == "__main__":
    main()
