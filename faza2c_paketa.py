"""
Faza 2c — §8: përbërja e paketës së rekomanduar (A4 nga 2b), pa kalendarin e prapambetjeve
(ai është te faza2c_lp.py).

Dalja:
  faza2c_paketa_rruga.csv     R e paketës muaj pas muaji 4.2023–12.2026, me burimin e çdo vlere
  faza2c_testet_kumulative.csv testet e efekteve kumulative (max, min, mesatare, tavan, rrumbullakim,
                               rishikime statistikore, 138/a)
  faza2c_rezultatet.csv        çdo shifër e përdorur në §8
Ekzekutimi: python3 faza2c_paketa.py
"""
import csv, math
from faza2a_model import (DIR, R_V35, R_33, R_95, R_KESH, I2, SHTESA_GRUP, ICHK, N_R,
                          muajt, muaji_para, ref_civile, R_paguar, faktori_W, W, kosto_vjetore)
from faza2b_alternativat import R0_PAKETE, rruga_A4

M0, M0_IÇK = "2023-04", "2023-03"   # baza dhe muaji i matjes së saj
RISH = ["2026-01"]                  # rishikimet deri në 2026; pastaj çdo 2 vjet: 2028-01, 2030-01 ...

# ---------------------------------------------------------------------------
# 1. Formula afatgjatë e paketës (rregulli i niveleve)
#    R_t = max{ R_{t-1};  R*_0 · max( I(τ(t)−1)/I(3.2023);  Ref_t/Ref_{4.2023} ) }
#    τ(t) = data e fundit e rishikimit ≤ t. Referenca kalon menjëherë; IÇK vetëm në rishikim.
# ---------------------------------------------------------------------------
def R_paketa(m, R_prev=None, rish=RISH, R0=R0_PAKETE):
    tau = max([r for r in rish if r <= m], default=None)
    f_ichk = ICHK[muaji_para(tau)] / ICHK[M0_IÇK] if tau else 1.0
    f_ref = ref_civile(m) / ref_civile(M0)
    kand = {"ICK": R0 * f_ichk, "referenca": R0 * f_ref}
    if R_prev is not None:
        kand["mosregresion"] = R_prev
    burimi = max(kand, key=kand.get)
    return kand[burimi], burimi, f_ichk, f_ref

def rruga_paketes(deri="2026-12"):
    out, R_prev = [], None
    for m in muajt(M0, deri):
        R, b, fi, fr = R_paketa(m, R_prev)
        out.append({"muaji": m, "R": R, "R_pagese": round(R), "burimi": b,
                    "faktori_ICK": round(fi, 6), "faktori_ref": round(fr, 6), "R_paguar": R_paguar(m)})
        R_prev = R
    return out

# ---------------------------------------------------------------------------
# 2. Testet e efekteve kumulative (rrugë të stilizuara; d)
# ---------------------------------------------------------------------------
def rregull_periodik(pi_list, rho_list, operatori, theta=None):
    """Zbaton g_k në çdo rishikim mbi R e rishikimit të mëparshëm (produkt i normave periodike)."""
    R = 1.0
    for p, r in zip(pi_list, rho_list):
        g = {"max": max(p, r), "min": min(p, r), "mes": (p + r) / 2, "pi": p, "rho": r,
             "tavan": min(p, theta if theta is not None else p)}[operatori]
        R *= 1 + g
    return R

def rregull_nivelesh(pi_list, rho_list):
    """Rregulli i paketës: R = R0 · max(Π(1+π), Π(1+ρ)) — maksimumi i niveleve, jo i normave."""
    I = math.prod(1 + p for p in pi_list); Rf = math.prod(1 + r for r in rho_list)
    return max(I, Rf), I, Rf

def main():
    rez, testet = [], []
    def out(s, t, v, sh=""):
        rez.append({"seksioni": s, "treguesi": t, "vlera": round(v, 6) if isinstance(v, float) else v, "shenim": sh})

    # 1. Rruga e paketës dhe përputhja me A4 të 2b
    rr = rruga_paketes()
    a4 = rruga_A4(R0_PAKETE, "B")
    diff = max(abs(r["R"] - a4[r["muaji"]]) for r in rr)
    out("8.1", "R*_0", R0_PAKETE); out("8.1", "R*_0 / 152.700 − 1", R0_PAKETE / R_V35 - 1)
    out("8.2", "R paketës 1.2026 (e pa rrumbullakuar)", next(r["R"] for r in rr if r["muaji"] == "2026-01"))
    out("8.2", "R paketës 1.2026 për pagesë (lekë të plota)", next(r["R_pagese"] for r in rr if r["muaji"] == "2026-01"))
    out("8.2", "Burimi lidhës 1.2026", next(r["burimi"] for r in rr if r["muaji"] == "2026-01"))
    out("8.2", "Devijimi maksimal ndaj A4 (2b), lekë", diff, "rregulli i niveleve = A4 deri në 2026")
    out("8.2", "Faktori IÇK 3.2023→12.2025", ICHK["2025-12"] / ICHK["2023-03"])
    out("8.2", "Faktori i referencës 4.2023→1.2026", ref_civile("2026-01") / ref_civile("2023-04"))

    # 2. Ratchet: max periodik kundrejt max i niveleve (dy rishikime: ρ e lartë, pastaj π e lartë)
    rastet = {
        "R1: ρ 6% pastaj π 6%": ([0.02, 0.06], [0.06, 0.00]),
        "R2: π 6% pastaj ρ 6%": ([0.06, 0.02], [0.00, 0.06]),
        "R3: alternim 4 rishikime": ([0.02, 0.06, 0.02, 0.06], [0.06, 0.00, 0.06, 0.00]),
        "R4: të dyja 3% çdo herë": ([0.03] * 4, [0.03] * 4),
        "R5: inflacion 2022–23 (12% në 2 vjet), referenca 0": ([0.12], [0.00]),
    }
    for emri, (pl, rl) in rastet.items():
        niv, I, Rf = rregull_nivelesh(pl, rl)
        rreshti = {"rasti": emri, "IÇK_kumulativ": round(I - 1, 4), "ref_kumulative": round(Rf - 1, 4),
                   "niveli_max (paketa)": round(niv - 1, 4)}
        for op in ("max", "min", "mes", "tavan"):
            v = rregull_periodik(pl, rl, op, theta=0.04)
            rreshti[f"periodik_{op}"] = round(v - 1, 4)
        rreshti["teprica_max_periodik_mbi_nivelin"] = round(rregull_periodik(pl, rl, "max") / niv - 1, 4)
        rreshti["humbja_reale_tavan"] = round(rregull_periodik(pl, rl, "tavan", 0.04) / I - 1, 4)
        rreshti["humbja_reale_mes"] = round(rregull_periodik(pl, rl, "mes") / I - 1, 4)
        rreshti["humbja_ndaj_ref_min"] = round(rregull_periodik(pl, rl, "min") / Rf - 1, 4)
        testet.append({"testi": "operatorët", **rreshti})
        for k in ("teprica_max_periodik_mbi_nivelin", "humbja_reale_tavan", "humbja_reale_mes", "humbja_ndaj_ref_min"):
            out("8.3-kumul", f"{emri} | {k}", rreshti[k])
        out("8.3-kumul", f"{emri} | paketa (niveli max)", rreshti["niveli_max (paketa)"])

    # 3. Rrumbullakimi: 10 rishikime me IÇK 3%, R0 = 243.539
    R0 = next(r["R"] for r in rr if r["muaji"] == "2026-01")
    teor, lart100, afer1 = R0, R0, R0
    for _ in range(10):
        teor *= 1.03
        lart100 = math.ceil(lart100 * 1.03 / 100) * 100          # rrumbullakim lart në 100 mbi bazën e rrumbullakuar
        afer1 = round(teor)                                      # paketa: llogaritet mbi R teorike, paguhet në lekë të plota
    out("8.3-rrumb", "Drift i rrumbullakimit lart në 100 lekë mbi bazë të rrumbullakuar, 10 rishikime", lart100 - teor)
    out("8.3-rrumb", "Drift i rregullit të paketës (R teorike, pagesë në lekë të plota)", afer1 - teor)
    testet.append({"testi": "rrumbullakimi", "rasti": "10 rishikime, IÇK 3%",
                   "drift_lart_100": round(lart100 - teor, 2), "drift_paketa": round(afer1 - teor, 2)})

    # 4. Rishikimi statistikor: IÇK e 12.2025 rishikohet +0,2 pikë pas rishikimit të 1.2026
    I_bot1, I_bot2 = ICHK["2025-12"], ICHK["2025-12"] + 0.2
    I_27_12 = I_bot2 * 1.06   # hipotetike (d): +6% deri në 12.2027, në bazën e re
    R_26_a = R0_PAKETE * I_bot1 / ICHK["2023-03"]
    R_28_paketa = R0_PAKETE * I_27_12 / ICHK["2023-03"]          # niveli, me vintazhin më të fundit
    R_28_periodik_ri = R_26_a * I_27_12 / I_bot2                    # periodik me bazën e rishikuar → humbet rishikimin
    out("8.3-rish", "R 1.2028, rregulli i niveleve me vintazhin e fundit", R_28_paketa)
    out("8.3-rish", "R 1.2028, periodik me bazën e rishikuar (vintazh i përzier)", R_28_periodik_ri)
    out("8.3-rish", "Humbja nga përzierja e vintazheve me metodën periodike", R_28_periodik_ri / R_28_paketa - 1)
    testet.append({"testi": "rishikimi statistikor", "rasti": "+0,2 pikë në 12.2025",
                   "R_2028_paketa": round(R_28_paketa, 2), "R_2028_periodik_vintazh_i_perzier": round(R_28_periodik_ri, 2)})

    # 5. Mekanizmi 138/a: pezullim i komponentit IÇK për 2 vjet (rishikimi 1.2028), referenca e ngrirë, IÇK 4%/vit (d)
    I_v = [1.04 ** k for k in range(0, 7)]   # 2026 = 1
    R_dhj26 = R0
    # pa pezullim: 1.2028 dhe 1.2030 indeksohen plotësisht
    R_pa = {2028: R_dhj26 * I_v[2], 2030: R_dhj26 * I_v[4]}
    # me pezullim në 1.2028 (vetëm), rregulli i niveleve rikthen nivelin në 1.2030 (rikuperim)
    R_rik = {2028: R_dhj26, 2030: R_dhj26 * I_v[4]}
    # pa rikuperim (rivendosje e bazës): humbje e përhershme
    R_pr = {2028: R_dhj26, 2030: R_dhj26 * I_v[4] / I_v[2]}
    for emri, d in (("pa pezullim", R_pa), ("pezullim me rikuperim (paketa)", R_rik), ("pezullim pa rikuperim", R_pr)):
        out("8.8-138a", f"{emri} | humbja reale 2028–2029", d[2028] / (R_dhj26 * I_v[2]) - 1)
        out("8.8-138a", f"{emri} | humbja reale nga 2030", d[2030] / (R_dhj26 * I_v[4]) - 1)
    kursim = 2 * 12 * N_R["qendror"] * (R_dhj26 * I_v[2] - R_dhj26)
    out("8.8-138a", "Kursimi buxhetor i pezullimit 2028–2029 (mld, N_R qendror)", kursim / 1e9)

    # 6. Korrigjimi periodik K11: të dhëna (c)
    pag = {r["tremujori"]: r for r in csv.DictReader(open(DIR / "faza1_instat_pagat_tremujore.csv", encoding="utf-8"))}
    mes23 = sum(float(pag[q]["gjithsej"]) for q in ("I/23", "II/23", "III/23", "IV/23")) / 4
    h1_26 = (float(pag["I/26"]["gjithsej"]) + float(pag["II/26"]["gjithsej"])) / 2
    out("8.4", "Paga mesatare bruto: mesatarja 2023", mes23)
    out("8.4", "Paga mesatare bruto: I–II/2026", h1_26)
    out("8.4", "Rritja e pagës mesatare 2023 → I–II/2026", h1_26 / mes23 - 1)
    out("8.4", "Rritja e R të paketës 4.2023 → 2026", R0 / R0_PAKETE - 1)
    out("8.4", "Rritja e I-2 4.2023 → 2026", I2["2026-01"] / I2["2023-04"] - 1)

    # 7. Paga totale: koeficientët ω të profileve (të pandryshuar) dhe raportet e hierarkisë
    profilet = {"G1, 0 vjet": ("G1", 0), "G1, 5 vjet": ("G1", 5), "G2, 15 vjet": ("G2", 15), "G3, 25 vjet": ("G3", 25)}
    base = faktori_W("G1", 0)
    for p, (g, y) in profilet.items():
        out("8.5", f"ω {p}", faktori_W(g, y)); out("8.5", f"raporti me G1 0 vjet | {p}", faktori_W(g, y) / base)

    def shkruaj(emri, rreshtat):
        with open(DIR / emri, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rreshtat for k in r)))
            w.writeheader(); w.writerows(rreshtat)
    shkruaj("faza2c_paketa_rruga.csv", rr); shkruaj("faza2c_testet_kumulative.csv", testet)
    shkruaj("faza2c_rezultatet.csv", rez)
    for r in rez:
        print(f'{r["seksioni"]:10s} {r["treguesi"]:90s} {r["vlera"]}')

if __name__ == "__main__":
    main()
