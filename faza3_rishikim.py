"""
Faza 3 — rishikimi: llogaritjet shtesë që kërkoi rishikimi kritik i punimit.
  (a) korridori i § 109 me baza të ndryshme (ndjeshmëri)
  (b) projeksioni 2027–2030 me rregullin e niveleve dhe krahasues të njëtrajtshëm për L95
  (c) shkasi i rishikimit të jashtëzakonshëm: rregulli "shtegu 4% në vit" kundrejt pragut fiks 4%;
      testimi mbi IÇK reale 2019–2026 dhe kosto shtesë në skenarët me inflacion të lartë
  (d) kosto vetëm për gjyqtarët (417 pozicione)
  (e) detyrimi i trashëguar 1.2019–3.2023 sipas V35 (vlerësim i kushtëzuar)
  (f) shembull i plotë i prapambetjes për një magjistrat G2, 15 vjet, sipas viteve
  (g) efekti i bazës së IÇK (2019 kundrejt 2023)
  (h) menyja e vendimit për Kuvendin (A4, A4θ, A4L, A1)
  (i) tabela e parametrave 2019→2026 (krahasim me tregues të ekonomisë)
  (j) koeficientët e pensionit suplementar për 1 lek R
Dalja: faza3_rishikim.csv (+ faza3_rruget_grafik.csv për grafikun)
"""
import csv, math
from faza2a_model import (DIR, R_V35, R_33, R_33_2026, R_95, R_95_2026, R_KESH, I2, SHTESA_GRUP, ICHK, N_R,
                          P_2023, P_2026, muajt, muaji_para, faktori_W, R_paguar, kosto_vjetore, korridori)
from faza2c_paketa import R0_PAKETE, rruga_paketes

rez = []
def out(s, t, v, sh=""):
    rez.append({"seksioni": s, "treguesi": t, "vlera": round(v, 6) if isinstance(v, float) else v, "shenim": sh})

L, U = korridori()
I0 = ICHK["2023-03"]
REF0 = I2["2023-04"] + SHTESA_GRUP
R26 = R0_PAKETE * ICHK["2025-12"] / I0

# ---------------- (a) korridori me baza të ndryshme ----------------
kor = {
    "V15 §100 (44%) mbi bazën 2022 (152.700) — leximi i përdorur": R_V35 * 1.44,
    "Gjurma II-a→I-5 2019→2023 mbi bazën 2019 të V35 (143.800)": 143_800 * 170_000 / 118_100,
    "Gjurma e Gjykatës mbi bazën 2022: (I-5+14.000)/(II-a 2022+14.000)": R_V35 * (170_000 + 14_000) / (126_300 + 14_000),
    "Gjurma funksionale V35 mbi bazën 2022: I-b→I-2": R_V35 * 231_000 / 152_700,
}
for k, v in kor.items():
    out("a", f"L | {k}", v)
out("a", "U = 152.700 × 425.000/257.000 (P 2022→2023)", U)
Lmin = min(kor.values())
out("a", "L më e ulëta", Lmin)
out("a", "198.963 / L më e ulëta − 1", 198_963 / Lmin - 1)
out("a", "161.500 / L më e ulëta − 1", R_95 / Lmin - 1)
out("a", "231.000 / L më e ulëta − 1", R0_PAKETE / Lmin - 1)

# ---------------- (b) projeksioni me rregullin e niveleve ----------------
def I_fund(viti, pi):
    """IÇK në dhjetor të vitit; real deri 8.2026, pastaj π vjetore."""
    I = ICHK["2026-08"] * (1 + pi) ** (4 / 12)
    for _ in range(2027, viti + 1):
        I *= 1 + pi
    return I

def projekto(alt, pi, rho):
    """Vlera në 1.2030 (pas rishikimit) dhe dy treguesit ndaj bazës së vet (C4, C5)."""
    ref = lambda y: I2["2026-01"] * (1 + rho) ** (y - 2026) + SHTESA_GRUP
    P = lambda y: P_2026 * (1 + min(rho, 0.04)) ** (y - 2026)
    I_r = I_fund(2029, pi)                    # matja për rishikimin e 1.2030
    if alt == "A0":
        R0, R = R_95, 0.38 * P(2030)
    elif alt == "A1":
        R0, R = R0_PAKETE, ref(2030)
    elif alt == "A3":
        R0, R = U, U * P(2030) / P_2023
    elif alt == "A4":
        R0, R = R0_PAKETE, R0_PAKETE * max(I_r / I0, ref(2030) / REF0)
    elif alt == "A5":
        R0, R = R0_PAKETE, R0_PAKETE * I_r / I0
    reale = R / (R0 * I_r / I0) - 1
    ndaj_ref = R / (R0 * ref(2030) / REF0) - 1
    return R, reale, ndaj_ref

proj = []
for alt in ("A0", "A1", "A3", "A4", "A5"):
    for s, (pi, rho) in {"S1": (0.03, 0.0), "S2": (0.02, 0.05)}.items():
        R, re_, rf = projekto(alt, pi, rho)
        proj.append({"alt": alt, "skenari": s, "R_1_2030": round(R), "vlera_reale_ndaj_bazes": round(re_, 4),
                     "ndaj_references_ndaj_bazes": round(rf, 4)})
        out("b", f"{alt} | {s} | R 1.2030", R)
        out("b", f"{alt} | {s} | ndaj vlerës reale të bazës", re_)
        out("b", f"{alt} | {s} | ndaj referencës së bazës", rf)

# ---------------- (c) shkasi i rishikimit të jashtëzakonshëm ----------------
def I_m(m, pi_seq):
    if m in ICHK:
        return ICHK[m]
    y, mm = map(int, m.split("-"))
    I = ICHK["2026-08"] * (1 + pi_seq[2026]) ** (4 / 12)
    for yy in range(2027, y):
        I *= 1 + pi_seq[yy]
    return I * (1 + pi_seq[y]) ** (mm / 12) if y > 2026 else ICHK["2026-08"] * (1 + pi_seq[2026]) ** ((mm - 8) / 12)

def sim(pi_seq, rho, rregulli=None, nga="2026-01", deri="2031-12", m_mat0="2025-12", R_start=None,
        I_baza=I0, R0=R0_PAKETE, rish_vitet=(2028, 2030), ref_fn=None):
    """Rruga mujore. rregulli: None | 'fiks' (π kumulative > 4%) | 'vjetor' (π kumulative > 4% dhe inflacioni vjetor > 4%)."""
    m_mat = m_mat0
    f_I = I_m(m_mat, pi_seq) / I_baza
    R_prev = R_start if R_start is not None else R0 * f_I
    shtegu, humbja, kur, rish = [], 0.0, None, []
    for m in muajt(nga, deri):
        y, mm = map(int, m.split("-"))
        mp = muaji_para(m)
        rregull = mm == 1 and y in rish_vitet
        k = (int(mp[:4]) - int(m_mat[:4])) * 12 + int(mp[5:]) - int(m_mat[5:])
        cum = I_m(mp, pi_seq) / I_m(m_mat, pi_seq) - 1
        y_m, mm_m = int(mp[:4]), int(mp[5:])
        mp12 = f"{y_m - 1:04d}-{mm_m:02d}"
        vjetor = I_m(mp, pi_seq) / I_m(mp12, pi_seq) - 1
        if rregulli == "fiks":
            jasht = not rregull and k > 0 and cum > 0.04
        elif rregulli == "vjetor":      # π kumulative > 4% DHE inflacioni vjetor > 4% (target + 1 p.p.)
            jasht = not rregull and k > 0 and cum > 0.04 and vjetor > 0.04
        else:
            jasht = False
        if rregull or jasht:
            f_I = I_m(mp, pi_seq) / I_baza; m_mat = mp; rish.append(m + ("*" if jasht else ""))
        ref = ref_fn(m) if ref_fn else (I2["2026-01"] * (1 + rho) ** (y - 2026) + SHTESA_GRUP)
        R = max(R_prev, R0 * max(f_I, ref / REF0))
        h = R / (R0 * I_m(m, pi_seq) / I_baza) - 1
        if h < humbja:
            humbja, kur = h, m
        shtegu.append((m, R)); R_prev = R
    return shtegu, humbja, kur, rish

baza = {y: 0.03 for y in range(2026, 2032)}
episod = {**baza, 2027: 0.067, 2028: 0.048}
for emri, ps in (("bazë 3%", baza), ("episod 2022–23", episod), ("4,5% çdo vit", {y: 0.045 for y in range(2026, 2032)}),
                 ("5% çdo vit", {y: 0.05 for y in range(2026, 2032)})):
    pa, h0, k0, r0 = sim(ps, 0.025, None)
    for rr in ("fiks", "vjetor"):
        me, h1, k1, r1 = sim(ps, 0.025, rr)
        shtese = sum(12 * 0 + (b[1] - a[1]) for a, b in zip(pa, me)) * N_R["qendror"]   # lekë-muaj × N_R
        out("c", f"{emri} | rregulli {rr} | rishikime të jashtëzakonshme", sum(1 for x in r1 if x.endswith("*")))
        out("c", f"{emri} | rregulli {rr} | humbja reale maks", h1)
        out("c", f"{emri} | rregulli {rr} | kosto shtesë 2026–2031 (mld, N_R qendror)", shtese / 1e9)
    out("c", f"{emri} | pa shkas | humbja reale maks", h0)

# Testimi mbi IÇK reale 2019–2026: rregull kundërfaktik nga 1.2019, matja bazë 12.2018, rishikime 2021/2023/2025
real = {y: 0.0 for y in range(2019, 2032)}
ref_h = lambda m: (129_800 + SHTESA_GRUP) if m < "2022-10" else ((138_700 + SHTESA_GRUP) if m < "2023-04" else
                  ((I2["2023-04"] + SHTESA_GRUP) if m < "2026-01" else I2["2026-01"] + SHTESA_GRUP))
for rr in (None, "fiks", "vjetor"):
    _, h, k, rish = sim(real, 0.0, rr, nga="2019-01", deri="2026-08", m_mat0="2018-12", I_baza=ICHK["2018-12"],
                        R0=129_800 + SHTESA_GRUP, rish_vitet=(2021, 2023, 2025),
                        ref_fn=lambda m: ref_h(m) * REF0 / (129_800 + SHTESA_GRUP))
    out("c", f"Historik 2019–2026 | rregulli {rr} | rishikime të jashtëzakonshme", sum(1 for x in rish if x.endswith("*")))
    out("c", f"Historik 2019–2026 | rregulli {rr} | muajt e tyre", " ".join(x for x in rish if x.endswith("*")) or "—")
    out("c", f"Historik 2019–2026 | rregulli {rr} | humbja reale maks", h)

# ---------------- (d) kosto vetëm për gjyqtarët ----------------
for om in (2.0, 2.4, 2.8):
    out("d", f"Gjyqtarët (417) me ω mesatar {om}: njësi-R", 417 * om)
    out("d", f"Gjyqtarët (417) me ω mesatar {om}: ΔC/vit ndaj L95 2026 (mld)", kosto_vjetore(R26, n_r=417 * om) / 1e9)

# ---------------- (e) detyrimi i trashëguar 1.2019–3.2023 ----------------
diff = 0.0
for m in muajt("2019-01", "2023-03"):
    std = 143_800 if m < "2022-10" else 152_700
    diff += std - 118_100
out("e", "Σ (standardi V35 − 118.100), 1.2019–3.2023, lekë për njësi-R", diff)
out("e", "Muaj", len(muajt("2019-01", "2023-03")))
for k, n in N_R.items():
    out("e", f"Detyrimi bruto, N_R {k} (mld)", diff * n / 1e9)
    out("e", f"Detyrimi pas VKM 755 (−1 mld), N_R {k} (mld)", diff * n / 1e9 - 1.0)

# Varianti: nëse nga 10.2022 u pagua 126.300 (II-a pas VKM 621/2022) dhe nga 1.2023 152.700 (V35 në fuqi më 9.1.2023)
def paguar_var(m):
    return 118_100 if m < "2022-10" else (126_300 if m < "2023-01" else 152_700)
diff_v = sum((143_800 if m < "2022-10" else 152_700) - paguar_var(m) for m in muajt("2019-01", "2023-03"))
out("e", "II-a pas VKM 621/2022 (lekë)", 126_300.0)
out("e", "Varianti 126.300/152.700: Σ për njësi-R", diff_v)
for k, n in N_R.items():
    out("e", f"Varianti: detyrimi bruto, N_R {k} (mld)", diff_v * n / 1e9)
    out("e", f"Varianti: detyrimi pas VKM 755, N_R {k} (mld)", diff_v * n / 1e9 - 1.0)

# ---------------- (f) shembulli individual G2, 15 vjet ----------------
om = faktori_W("G2", 15)
rr = {r["muaji"]: r for r in rruga_paketes("2026-12")}
kal = list(csv.DictReader(open(DIR / "faza2c_lp_kalendari.csv", encoding="utf-8")))
sist = {}
for r in kal:
    sist.setdefault(r["muaji_detyrimit"], {})[int(r["viti_pageses"])] = float(r["shuma_lek"])
pi_bazë = {y: 0.03 for y in range(2026, 2032)}
kest, komp = {}, {}
for m, ndarja in sist.items():
    a_ind = om * max(rr[m]["R"] - rr[m]["R_paguar"], 0)
    tot = sum(ndarja.values())
    for y, v in ndarja.items():
        pj = a_ind * v / tot
        kest[y] = kest.get(y, 0) + pj
        komp[y] = komp.get(y, 0) + pj * (I_m(f"{y}-07", pi_bazë) / I_m(m, pi_bazë) - 1)
for y in sorted(kest):
    out("f", f"G2 15 vjet | {y} | kësti bruto", kest[y])
    out("f", f"G2 15 vjet | {y} | kompensimi IÇK", komp[y])
out("f", "G2 15 vjet | totali bruto", sum(kest.values()))
out("f", "G2 15 vjet | kompensimi gjithsej", sum(komp.values()))

# ---------------- (g) efekti i bazës së IÇK ----------------
out("g", "Paketa 2026 − kundërfaktikja 2019 (= A1), lekë/muaj", R26 - R_KESH)
out("g", "ΔC/vit i kësaj diference (mld, N_R qendror)", 12 * N_R["qendror"] * (R26 - R_KESH) / 1e9)

# ---------------- (h) menyja e vendimit ----------------
def rruga(fn):
    return [{"muaji": m, "R": fn(m), "R_paguar": R_paguar(m)} for m in muajt("2023-04", "2026-12")]
menu = {
    "A4 (paketa)": lambda m: R0_PAKETE if m < "2026-01" else R26,
    "A4θ (tavan 4% në rishikimin e parë)": lambda m: R0_PAKETE if m < "2026-01" else R0_PAKETE * 1.04,
    "A4L (baza 219.888, skenari B)": lambda m: L if m < "2026-01" else L * ICHK["2025-12"] / I0,
    "A1 (Këshillat)": lambda m: R0_PAKETE if m < "2026-01" else R_KESH,
}
for k, fn in menu.items():
    rr_ = rruga(fn)
    A = sum(max(r["R"] - r["R_paguar"], 0) for r in rr_) * N_R["qendror"]
    R_d = fn("2026-12")
    out("h", f"{k} | R 2026", R_d)
    out("h", f"{k} | ΔC/vit ndaj L95 2026 (mld)", kosto_vjetore(R_d) / 1e9)
    out("h", f"{k} | prapambetja 4.2023–12.2026 (mld)", A / 1e9)
    out("h", f"{k} | humbja reale në 12.2025 ndaj 231.000 të indeksuar", R0_PAKETE / (R0_PAKETE * ICHK["2025-12"] / I0) - 1)
    out("h", f"{k} | raporti me vlerën reale të bazës në 1.2026", R_d / (R0_PAKETE * ICHK["2025-12"] / I0) - 1)

# ---------------- (i) tabela e parametrave 2019→2026 ----------------
pag = {r["tremujori"]: r for r in csv.DictReader(open(DIR / "faza1_instat_pagat_tremujore.csv", encoding="utf-8"))}
mes = lambda qs, col="gjithsej": sum(float(pag[q][col]) for q in qs) / len(qs)
w19 = mes(["I/19", "II/19", "III/19", "IV/19"]); w26 = mes(["I/26", "II/26"])
s19 = mes(["I/19", "II/19", "III/19", "IV/19"], "sektori_shteteror"); s24 = mes(["I/24", "II/24", "III/24", "IV/24"], "sektori_shteteror")
par = {
    "IÇK 12.2018 → 8.2026": ICHK["2026-08"] / ICHK["2018-12"] - 1,
    "Paga mesatare bruto 2019 → I–II/2026": w26 / w19 - 1,
    "Paga mesatare në sektorin shtetëror 2019 → 2024": s24 / s19 - 1,
    "Referenca civile (I-b/I-2 + 14.000) 1.2019 → 2026": (I2["2026-01"] + SHTESA_GRUP) / (129_800 + SHTESA_GRUP) - 1,
    "R e paguar 1.2019 → 1–7.2026": R_33_2026 / 118_100 - 1,
    "R e L95 2026 ndaj standardit 2019 të V35 (143.800)": R_95_2026 / 143_800 - 1,
    "R e paketës 2026 ndaj standardit 2019 të V35 (143.800)": R26 / 143_800 - 1,
}
for k, v in par.items():
    out("i", k, v)

# ---------------- (j) pensioni suplementar për 1 lek R ----------------
for emri, f in (("G2, 25 vjet (1,5% × 25)", 0.015 * 25 * faktori_W("G2", 25)),
                ("G1, 30 vjet (tavan 40%)", 0.40 * faktori_W("G1", 30)),
                ("Gjyqtar GJL, 9 vjet në GJL, 25 vjet (tavan 50%)", 0.50 * faktori_W("G3", 25))):
    out("j", f"Pensioni mujor për 1 lek R | {emri}", f)

# ---------------- (k) saktësime pas rishikimit të jashtëm (nëntor 2026) ----------------
f24 = ICHK["2023-12"] / I0
R24 = R0_PAKETE * f24
d24 = (R24 - R0_PAKETE) * 24                                   # 1.2024–12.2025, lekë për njësi-R
out("k", "Rishikim hipotetik më 1.1.2024: faktori IÇK 3.2023→12.2023", f24)
out("k", "Rishikim hipotetik më 1.1.2024: R nga 1.2024 (lekë)", R24)
for kk, n in N_R.items():
    out("k", f"Rishikim hipotetik më 1.1.2024: prapambetje shtesë 1.2024–12.2025, N_R {kk} (mld)", d24 * n / 1e9)
A_tot = 13.839449; A_l95 = 1.35
out("k", "Prapambetja e paketës 4.2023–12.2026 (mld)", A_tot)
out("k", "Prapambetja që detyron tashmë L95 (mld)", A_l95)
out("k", "Prapambetja shtesë që shton propozimi (mld)", A_tot - A_l95)
out("k", "W G2 15 vjet me R të parrumbullakuar 243.538,62", faktori_W("G2", 15) * R26)
out("k", "W G2 15 vjet me R të rrumbullakuar 243.539", faktori_W("G2", 15) * 243_539)
out("k", "R26 e parrumbullakuar", R26)
out("k", "Muaj me inflacion vjetor ≥ 4% radhazi, 3.2022–9.2023", 19)
out("k", "Muaj me inflacion vjetor > 4% në atë periudhë", 18)

# ---------------- grafiku: rrugët 2019–2026 ----------------
graf = []
for m in muajt("2019-01", "2026-12"):
    graf.append({"muaji": m,
                 "R_paguar": (118_100 if m < "2023-04" else R_paguar(m)) if m <= "2026-12" else None,
                 "Paketa": (None if m < "2023-04" else (R0_PAKETE if m < "2026-01" else R26)),
                 "L95": (None if m < "2023-04" else (R_95 if m < "2026-01" else R_95_2026)),
                 "Kesh_A1": (None if m < "2023-04" else (R0_PAKETE if m < "2026-01" else R_KESH)),
                 "V35_152700_IÇK": R_V35 * ICHK[m] / ICHK["2022-09"] if m >= "2022-09" and m in ICHK else None})

def shkruaj(emri, rr_):
    with open(DIR / emri, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rr_ for k in r))); w.writeheader(); w.writerows(rr_)
shkruaj("faza3_rishikim.csv", rez); shkruaj("faza3_projeksion.csv", proj); shkruaj("faza3_rruget_grafik.csv", graf)
for r in rez:
    print(f'{r["seksioni"]} | {r["treguesi"]:85s} {r["vlera"]}')
