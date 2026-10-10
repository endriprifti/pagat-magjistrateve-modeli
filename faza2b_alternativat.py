"""
Faza 2b — §7: alternativat dhe zgjedhja e paketës kryesore.
Importon formulat nga faza2a_model.py (F1–F8); nuk i rishkruan.

Dalja:
  faza2b_rruget.csv       rrugët mujore R_t, 4.2023–12.2026, për çdo alternativë dhe skenar
  faza2b_testet.csv       testi F8 (C1–C6) për çdo alternativë × skenar × standard C5
  faza2b_profilet.csv     paga totale W (F1) e 4 profileve standarde, dhjetor 2026
  faza2b_kosto.csv        ΔC vjetore (F7) dhe prapambetja (F6), me N_R 3.000 / 3.954 / 4.902
  faza2b_projeksion.csv   projeksion stilizuar 2027–2030 (d, hipotetik) për rregullat e indeksimit
  faza2b_rezultatet.csv   çdo shifër e përdorur në §7
Ekzekutimi: python3 faza2b_alternativat.py
"""
import csv
from faza2a_model import (DIR, R_V35, R_33, R_95, R_95_2026, R_L95, ref_presidenti, R_KESH, P_2023, I2, SHTESA_GRUP, N_R,
                          korridori, muajt, R_paguar, rruga_minimale, prapambetja, kosto_vjetore,
                          kontrollo, faktori_W, W, pi_kumul, ICHK)

L, U = korridori()
MUAJT = muajt("2023-04", "2026-12")
SKENARET = ("A", "B")

# ---------------------------------------------------------------------------
# 1. Alternativat si rrugë mujore R_t (lekë/muaj bruto)
# ---------------------------------------------------------------------------
def rruga_A0():
    """L95: R = 0,38 × P; P = 425.000 deri 12.2025, 435.625 nga 1.2026 (VKM 92/2026)."""
    return {m: R_L95(m) for m in MUAJT}

def rruga_A1():
    """Këshillat: R = I-2 + 14.000 (VKM 325 orig.; VKM 131/2026)."""
    return {m: (I2["2023-04"] if m < "2026-01" else I2["2026-01"]) + SHTESA_GRUP for m in MUAJT}

def rruga_A2():
    """Mesi i Nash-it nga punimi i autorit: (236.425 + 161.500)/2, i rrumbullakuar 198.963."""
    return {m: 198_963 for m in MUAJT}

def rruga_A3():
    """Ankora e Presidentit: raporti 2022 R/P ruhet (κ ≈ 0,594) dhe ndjek P: U deri 12.2025, U × 1,025 nga 1.2026."""
    return {m: U * ref_presidenti(m) / P_2023 for m in MUAJT}

def rruga_A4(R0, skenari):
    """Referenca e dyfishtë: R*_0, pastaj ndjek referencën civile dhe në rishikim g = max(π, ρ)."""
    return {r["muaji"]: r["R_min"] for r in rruga_minimale(R0, "civile", skenari, rregulli="max")}

def rruga_A5(R0):
    """Vetëm IÇK: R*_0, pastaj në rishikim g = π; nuk ndjek referencën ndërmjet rishikimeve."""
    pi = pi_kumul("2023-03", "2025-12")
    return {m: (R0 if m < "2026-01" else R0 * (1 + pi)) for m in MUAJT}

R0_PAKETE = I2["2023-04"] + SHTESA_GRUP   # 231.000: standardi i V35 i zbatuar mbi VKM 325 (b)

ALTERNATIVAT = {
    # emri: (përshkrimi, funksioni(skenari) → rruga, R*_0, referenca e deklaruar, rregulli i vet i indeksimit)
    "A0": ("L95 (κ = 0,38)", lambda s: rruga_A0(), R_95, "presidenti", "tavan"),
    "A1": ("Këshillat (I-2 + 14.000)", lambda s: rruga_A1(), 231_000, "civile", "ref"),
    "A2": ("Mesi 198.963", lambda s: rruga_A2(), 198_963, "civile", "asnjë"),
    "A3": ("Ankora e Presidentit (κ ≈ 0,594)", lambda s: rruga_A3(), U, "presidenti", "ref"),
    "A4": ("Referenca e dyfishtë, R*_0 = 231.000", lambda s: rruga_A4(R0_PAKETE, s), R0_PAKETE, "civile", "max"),
    "A5": ("Vetëm IÇK, R*_0 = 231.000", lambda s: rruga_A5(R0_PAKETE), R0_PAKETE, "civile", "ichk"),
    "A4L": ("Referenca e dyfishtë, R*_0 = L (ndjeshmëri)", lambda s: rruga_A4(L, s), L, "civile", "max"),
    "A5L": ("Vetëm IÇK, R*_0 = L (ndjeshmëri)", lambda s: rruga_A5(L), L, "civile", "ichk"),
}

STANDARDET_C5 = {"max": (None, "g = max(π, ρ)"), "ichk": (None, "g = π"),
                 "ref": (None, "g = ρ"), "tavan": (0.04, "g = min(π; 4%)")}

PROFILET = {"G1, 5 vjet": ("G1", 5, "pa", False), "G2, 15 vjet": ("G2", 15, "pa", False),
            "G3, 25 vjet, kryetar": ("G3", 25, "kryetar", False),
            "G2, 10 vjet, GJKKO/SPAK": ("G2", 10, "pa", True)}

# ---------------------------------------------------------------------------
# 2. Testet F8 me diagnostikë (muaji i parë i shkeljes dhe mungesa maksimale)
# ---------------------------------------------------------------------------
def diagnostiko(rruga, R0, ref, skenari, standardi, theta):
    rez = kontrollo(rruga, R0, ref, skenari, standardi, theta)
    minr = {r["muaji"]: r["R_min"] for r in rruga_minimale(R0, ref, skenari, deri=MUAJT[-1],
                                                            rregulli=standardi, theta=theta)}
    mungesat = {m: minr[m] - rruga[m] for m in MUAJT}
    shkelje = [m for m in MUAJT if mungesat[m] > 0.5]
    # C6 veçmas (dysheme absolute e skenarit A), që të dallohet nga C4/C5
    c6 = all(rruga[m] >= R_KESH - 0.5 for m in MUAJT if m >= "2026-08") if skenari == "A" else True
    return {**rez, "C6_veças": c6,
            "realizueshme": all(rez.values()),
            "muaji_i_pare_shkeljes_C4_C6": shkelje[0] if shkelje else "",
            "mungesa_maks_lek": round(max(0.0, max(mungesat.values())), 2)}

# ---------------------------------------------------------------------------
# 3. Projeksioni i stilizuar 2027–2030 (d): si sillen rregullat kur referenca dhe inflacioni ndahen
# ---------------------------------------------------------------------------
SKENARET_STIL = {"S1: referenca e ngrirë, π = 3%/vit": (0.03, 0.00),
                 "S2: referenca +5%/vit, π = 2%/vit": (0.02, 0.05)}

def projekto(alt, R_dhj26, pi_v, rho_v):
    """Hapa vjetorë 1.2027–1.2030; rishikimet çdo 2 vjet: 1.2028 dhe 1.2030 (d).
    Kthen R më 1.2030, indeksin e çmimeve dhe referencën civile (2026-12 = 1)."""
    I2_t = I2["2026-01"]; ref0 = I2_t + SHTESA_GRUP
    R, R_rish, I, I_rish, ref_rish = R_dhj26, R_dhj26, 1.0, 1.0, ref0
    for viti in (2027, 2028, 2029, 2030):
        I *= 1 + pi_v
        I2_t *= 1 + rho_v
        ref = I2_t + SHTESA_GRUP
        rishikim = viti in (2028, 2030)
        pi_c = I / I_rish - 1
        rho_c = ref / ref_rish - 1
        if alt == "A0" and rishikim:
            R = R_rish * (1 + min(pi_c, 0.04))
        elif alt == "A1":
            R = ref
        elif alt == "A3":
            R = R  # P konstante (d); ndryshon vetëm me ligj buxheti
        elif alt == "A4":
            R = max(R, R_dhj26 * ref / ref0)              # C4 ndërmjet rishikimeve
            if rishikim:
                R = max(R, R_rish * (1 + max(pi_c, rho_c)))
        elif alt == "A5" and rishikim:
            R = R_rish * (1 + pi_c)
        if rishikim:
            R_rish, I_rish, ref_rish = R, I, ref
    return R, I, (I2_t + SHTESA_GRUP) / ref0

# ---------------------------------------------------------------------------
# 4. Ekzekutimi
# ---------------------------------------------------------------------------
def main():
    rez = []
    def out(seksioni, treguesi, vlera, shenim=""):
        rez.append({"seksioni": seksioni, "treguesi": treguesi,
                    "vlera": round(vlera, 4) if isinstance(vlera, float) else vlera, "shenim": shenim})

    rruget, testet, profilet, kosto, proj = [], [], [], [], []
    for kod, (emri, f, R0, ref, rregulli) in ALTERNATIVAT.items():
        for sk in SKENARET:
            rr = f(sk)
            for m in MUAJT:
                rruget.append({"alt": kod, "skenari": sk, "muaji": m, "R": round(rr[m], 2),
                               "R_paguar": R_paguar(m)})
            # Testet
            for std, (theta, pershkrim) in STANDARDET_C5.items():
                d = diagnostiko(rr, R0, ref, sk, std, theta)
                testet.append({"alt": kod, "emri": emri, "skenari": sk, "standardi_C5": pershkrim,
                               "R0": round(R0, 2), "referenca": ref, **d})
            # Prapambetja dhe kosto
            rows = [{"muaji": m, "R_min": rr[m], "R_paguar": R_paguar(m)} for m in MUAJT]
            A_77 = prapambetja(rows, "2026-07")
            A_dhj = prapambetja(rows, "2026-12")
            R_dhj = rr["2026-12"]
            for k, n in N_R.items():
                kosto.append({"alt": kod, "skenari": sk, "N_R": k, "R_dhj_2026": round(R_dhj, 2),
                              "dC_vjetore_kundrejt_L95": round(kosto_vjetore(R_dhj, n_r=n)),
                              "A_4.2023_7.2026": round(A_77 * n), "A_4.2023_12.2026": round(A_dhj * n)})
            out("kosto", f"{kod} | {sk} | R dhjetor 2026", R_dhj)
            out("kosto", f"{kod} | {sk} | ΔC/vit, N_R qendror (mld)", kosto_vjetore(R_dhj) / 1e9)
            out("kosto", f"{kod} | {sk} | A 4.2023–12.2026, N_R qendror (mld)", A_dhj * N_R["qendror"] / 1e9)
            out("kosto", f"{kod} | {sk} | A 4.2023–7.2026, N_R qendror (mld)", A_77 * N_R["qendror"] / 1e9)
        # Profilet (skenari B; në A ndryshon vetëm A0/A2, që janë të parealizueshme)
        R_dhj = f("B")["2026-12"]
        for p, args in PROFILET.items():
            profilet.append({"alt": kod, "profili": p, "R_dhj_2026": round(R_dhj, 2),
                             "W": round(W(R_dhj, *args)), "W_L95": round(W(R_95_2026, *args)),
                             "ndryshimi_ndaj_L95": round(R_dhj / R_95_2026 - 1, 4)})
        out("baza", f"{kod} | R*_0", R0)
        out("baza", f"{kod} | κ = R*_0 / P", R0 / P_2023)
        out("baza", f"{kod} | ndryshimi ndaj 152.700", R0 / R_V35 - 1)

    # Projeksioni
    humbjet = {}
    for kod in ("A0", "A1", "A3", "A4", "A5", "A4L", "A5L"):
        R_dhj = ALTERNATIVAT[kod][1]("B")["2026-12"]
        for s, (pi_v, rho_v) in SKENARET_STIL.items():
            R30, I30, ref30 = projekto(kod.rstrip("L"), R_dhj, pi_v, rho_v)
            vr = (R30 / R_dhj) / I30 - 1
            vref = (R30 / R_dhj) / ref30 - 1
            proj.append({"alt": kod, "skenari_stil": s, "R_dhj_2026": round(R_dhj, 2), "R_1_2030": round(R30, 2),
                         "vlera_reale_ndryshim": round(vr, 4), "raporti_me_referencen_ndryshim": round(vref, 4)})
            out("projeksion", f"{kod} | {s} | ndryshimi i vlerës reale 12.2026→1.2030", vr)
            out("projeksion", f"{kod} | {s} | ndryshimi ndaj referencës civile", vref)
            h = humbjet.setdefault(kod, {"reale": 0.0, "ref": 0.0})
            h["reale"] = min(h["reale"], vr); h["ref"] = min(h["ref"], vref)

    # Dominimi brenda bashkësisë së realizueshme (standardi më i rreptë C5 = max, të dy skenarët)
    realiz = sorted({t["alt"] for t in testet if t["standardi_C5"] == "g = max(π, ρ)" and t["realizueshme"]}
                    - {t["alt"] for t in testet if t["standardi_C5"] == "g = max(π, ρ)" and not t["realizueshme"]})
    kriteret = {k: (kosto_vjetore(ALTERNATIVAT[k][1]("B")["2026-12"]), -humbjet[k]["reale"], -humbjet[k]["ref"])
                for k in realiz}   # të gjitha "më pak është më mirë"
    for k in realiz:
        dominuar_nga = [j for j in realiz if j != k and all(a <= b for a, b in zip(kriteret[j], kriteret[k]))
                        and any(a < b for a, b in zip(kriteret[j], kriteret[k]))]
        out("pareto", f"{k} | ΔC/vit (mld); humbja maks reale; humbja maks ndaj ref.",
            f"{kriteret[k][0]/1e9:.4f}; {kriteret[k][1]:.4f}; {kriteret[k][2]:.4f}")
        out("pareto", f"{k} | i dominuar nga", ", ".join(dominuar_nga) or "askush")
    out("pareto", "Alternativat e realizueshme në të dy skenarët me standardin më të rreptë", ", ".join(realiz))

    for kod in ("A1", "A4", "A4L"):
        for k in ("i_ulet", "i_larte"):
            out("kosto", f"{kod} | B | ΔC/vit, N_R {k} (mld)", kosto_vjetore(ALTERNATIVAT[kod][1]("B")["2026-12"], n_r=N_R[k]) / 1e9)
    rA4, rA4L = ALTERNATIVAT["A4"][1]("B"), ALTERNATIVAT["A4L"][1]("B")
    rows = lambda rr: [{"muaji": m, "R_min": rr[m], "R_paguar": R_paguar(m)} for m in MUAJT]
    out("A4", "ΔC A4 − A4L (mld/vit, N_R qendror, B)", (kosto_vjetore(rA4["2026-12"]) - kosto_vjetore(rA4L["2026-12"])) / 1e9)
    out("A4", "A A4 − A4L, 4.2023–12.2026 (mld, N_R qendror, B)",
        (prapambetja(rows(rA4), "2026-12") - prapambetja(rows(rA4L), "2026-12")) * N_R["qendror"] / 1e9)
    PAGA_SHTET_2026 = 120.3e9   # fondi i pagave i buxhetit të shtetit 2026 (AN 2/2026) (c)
    out("A4", "ΔC A4 / fondi i pagave të shtetit 2026", kosto_vjetore(rA4["2026-12"]) / PAGA_SHTET_2026)
    out("A4", "A4 me tavan 4% në 1.2026 (R*_0 = 231.000)", R0_PAKETE * 1.04)
    # Shifra të veçanta për tekstin
    out("baza", "L", L); out("baza", "U", U)
    out("baza", "231.000 / 152.700 − 1 (gjurma funksionale V35)", 231_000 / R_V35 - 1)
    out("baza", "κ ekzakt i A3", U / P_2023)
    out("A4", "R 1.2026 me max(π, ρ), R*_0 = 231.000", rruga_A4(R0_PAKETE, "B")["2026-01"])
    out("A4", "Diferenca A4 − A1 në 2026", rruga_A4(R0_PAKETE, "B")["2026-01"] - R_KESH)
    out("A4", "A4 mbi A1, 2026", rruga_A4(R0_PAKETE, "B")["2026-01"] / R_KESH - 1)
    out("A4", "π 3.2023→12.2025", pi_kumul("2023-03", "2025-12"))
    out("A3", "Dyshemeja C5 'max' në 1.2026 për A3", U * (1 + pi_kumul("2023-03", "2025-12")))
    out("A2", "198.963 nën L", 198_963 / L - 1)
    out("A0", "161.500 nën L", R_95 / L - 1)
    out("A0", "Ulja nominale 236.425 → 165.537,5 (skenari A)", R_95_2026 / R_KESH - 1)

    def shkruaj(emri, rreshtat):
        with open(DIR / emri, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rreshtat for k in r)))
            w.writeheader(); w.writerows(rreshtat)
    shkruaj("faza2b_rruget.csv", rruget); shkruaj("faza2b_testet.csv", testet)
    shkruaj("faza2b_profilet.csv", profilet); shkruaj("faza2b_kosto.csv", kosto)
    shkruaj("faza2b_projeksion.csv", proj); shkruaj("faza2b_rezultatet.csv", rez)

    print("TESTET (realizueshme? | muaji i parë i shkeljes | mungesa maks):")
    for t in testet:
        print(f'{t["alt"]:4s} {t["skenari"]} {t["standardi_C5"]:16s} C1={t["C1_korridori"]!s:5s} '
              f'C3={t["C3_mosregresion"]!s:5s} C456={t["C4_C5_C6_mbi_rrugen_min"]!s:5s} C6={t["C6_veças"]!s:5s} '
              f'→ {t["realizueshme"]!s:5s} {t["muaji_i_pare_shkeljes_C4_C6"]:8s} {t["mungesa_maks_lek"]}')
    print("\nREZULTATE:")
    for r in rez:
        print(f'{r["seksioni"]:10s} {r["treguesi"]:72s} {r["vlera"]}')
    print("\nPROFILET:")
    for p in profilet:
        print(p)

if __name__ == "__main__":
    main()
