"""
Faza 2c — kalendari i shlyerjes së prapambetjeve me programim linear (scipy.optimize.linprog).

E drejta (ekzistenca dhe masa) llogaritet veçmas: a_m = N_R · (R_paketës,m − R_paguar,m)⁺ për çdo
muaj m nga 4.2023 deri 12.2026 (supozim d: paketa hyn në fuqi më 1.1.2027).
Kalendari vendos vetëm KUR paguhet, jo SA.

Variablat: x[m,y] ≥ 0 = shuma e muajit m e paguar në vitin y; h[m] ≥ 0 = hendeku (e papaguar deri 2029).
Kufizimet:
  (K-a) Σ_y x[m,y] + h[m] = a_m                     shlyerje e plotë; hendeku raportohet, detyrimi nuk ulet
  (K-b) Σ_m x[m,y] ≤ B_y                            tavani buxhetor vjetor (parametër)
  (K-c) Σ_m x[m,y] ≥ min(p_min · A, B_y)            asnjë vit pa pagesë
  (K-d) pjesa e paguar e muajit më të vjetër ≥ pjesa e paguar e muajit pasardhës, në çdo vit (prioritet)
Objektivi: min [ Σ x[m,y] · vonesa(m,y)² ] / A  +  M · Σ h[m]
  (çdo lek peshohet me vonesën e vet: një muaj shtesë pritjeje kushton më shumë për detyrimin më të vjetër)
  vonesa = muajt nga muaji i detyrimit deri në mes të vitit të pagesës (1 korrik).
Dalja: faza2c_lp_kalendari.csv, faza2c_lp_skenaret.csv, faza2c_lp_rezultatet.csv
"""
import csv
import numpy as np
from scipy.optimize import linprog
from faza2a_model import DIR, N_R, ICHK, muajt
from faza2c_paketa import rruga_paketes

def muaj_indeks(m):
    y, mm = map(int, m.split("-")); return y * 12 + (mm - 1)

def detyrimet(n_r=N_R["qendror"]):
    rr = rruga_paketes("2026-12")
    return [(r["muaji"], n_r * max(r["R"] - r["R_paguar"], 0.0)) for r in rr if r["R"] - r["R_paguar"] > 0.5]

def zgjidh(vitet, B, p_min, n_r=N_R["qendror"], M=1e3):
    det = detyrimet(n_r)
    muajt_d = [m for m, _ in det]; a = np.array([v for _, v in det]) / 1e9; A = a.sum()   # në mld lekë (shkallëzim numerik)
    B = {y: b / 1e9 for y, b in B.items()}
    nM, nY = len(det), len(vitet)
    nx = nM * nY
    idx = lambda i, j: i * nY + j
    vonesa = np.array([[muaj_indeks(f"{y}-07") - muaj_indeks(m) for y in vitet] for m in muajt_d])
    c = np.concatenate([(vonesa.flatten() ** 2) / A, np.full(nM, M * 100 / A)])   # vonesa e ponderuar me vetveten: pritjet e gjata kushtojnë më shumë
    # Barazimet (K-a)
    Aeq = np.zeros((nM, nx + nM)); beq = a.copy()
    for i in range(nM):
        for j in range(nY):
            Aeq[i, idx(i, j)] = 1
        Aeq[i, nx + i] = 1
    Aub, bub = [], []
    for j, y in enumerate(vitet):
        r = np.zeros(nx + nM)
        for i in range(nM):
            r[idx(i, j)] = 1
        Aub.append(r.copy()); bub.append(B[y])                       # (K-b)
        Aub.append(-r); bub.append(-min(p_min * A, B[y]))             # (K-c)
    for j in range(nY):                                                # (K-d)
        for i in range(nM - 1):
            r = np.zeros(nx + nM)
            for jj in range(j + 1):
                r[idx(i, jj)] = -a[i + 1]
                r[idx(i + 1, jj)] = a[i]
            Aub.append(r); bub.append(0.0)
    res = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * (nx + nM), method="highs")
    assert res.status == 0, res.message
    x = res.x[:nx].reshape(nM, nY); h = res.x[nx:]
    paguar = x.sum(axis=0)
    vonesa_mes = (x * vonesa).sum() / max(x.sum(), 1)
    # Kompensimi i vlerës reale (d): faktori IÇK nga muaji i detyrimit deri në pagesë;
    # IÇK reale deri 8.2026, pastaj 3%/vit (objektivi i BSH).
    def I_at(m):
        if m in ICHK:
            return ICHK[m]
        k = muaj_indeks(m) - muaj_indeks("2026-08")
        return ICHK["2026-08"] * 1.03 ** (k / 12)
    komp = sum(x[i, j] * (I_at(f"{y}-07") / I_at(muajt_d[i]) - 1)
               for i in range(nM) for j, y in enumerate(vitet))
    x, h, paguar, komp, A = x * 1e9, h * 1e9, paguar * 1e9, komp * 1e9, A * 1e9
    return {"A": A, "paguar": dict(zip(vitet, paguar)), "hendeku": h.sum(),
            "vonesa_mesatare_muaj": vonesa_mes, "kompensimi_IÇK": komp,
            "kalendari": [(muajt_d[i], vitet[j], x[i, j]) for i in range(nM) for j in range(nY) if x[i, j] > 1]}

def main():
    rez, sken, kal = [], [], []
    def out(t, v, sh=""):
        rez.append({"treguesi": t, "vlera": round(v, 4) if isinstance(v, float) else v, "shenim": sh})
    V3, V2 = [2027, 2028, 2029], [2027, 2028]
    for emri, vitet, B_v, p in [
        ("Bazë: 5 mld/vit, 2027–2029, p_min 10%", V3, 5e9, 0.10),
        ("4 mld/vit (i pamjaftueshëm)", V3, 4e9, 0.10),
        ("7 mld/vit", V3, 7e9, 0.10),
        ("Pa tavan", V3, 1e12, 0.10),
        ("5 mld/vit, p_min 0%", V3, 5e9, 0.0),
        ("5 mld/vit, p_min 20%", V3, 5e9, 0.20),
        ("Skema e Këshillave: 2027–2028, 7 mld/vit", V2, 7e9, 0.10),
        ("Skema e Këshillave: 2027–2028, 5 mld/vit", V2, 5e9, 0.10),
    ]:
        r = zgjidh(vitet, {y: B_v for y in vitet}, p)
        row = {"skenari": emri, "A_total_mld": round(r["A"] / 1e9, 4),
               **{f"paguar_{y}_mld": round(r["paguar"][y] / 1e9, 4) for y in vitet},
               "hendeku_mld": round(r["hendeku"] / 1e9, 4),
               "vonesa_mesatare_muaj": round(r["vonesa_mesatare_muaj"], 2),
               "kompensimi_IÇK_mld": round(r["kompensimi_IÇK"] / 1e9, 4),
               "kompensimi_si_pjese_e_A": round(r["kompensimi_IÇK"] / r["A"], 4)}
        sken.append(row)
        for k, v in row.items():
            if k != "skenari":
                out(f"{emri} | {k}", v)
        if emri.startswith("Bazë"):
            kal = [{"muaji_detyrimit": m, "viti_pageses": y, "shuma_lek": round(v)} for m, y, v in r["kalendari"]]
            # muaji i fundit i paguar plotësisht në 2027
            out("Bazë | muaji i fundit i shlyer plotësisht në 2027",
                max((m for m, y, v in r["kalendari"] if y == 2027 and
                     not any(mm == m and yy > 2027 for mm, yy, _ in r["kalendari"])), default=""))
    det = detyrimet(); A = sum(v for _, v in det)
    out("Vonesa mesatare nëse gjithçka paguhet në mes të 2027 (kufiri i poshtëm, muaj)",
        sum(v * (muaj_indeks("2027-07") - muaj_indeks(m)) for m, v in det) / A)
    out("Muajt e detyrimit (numri)", len(det))
    # ndjeshmëria ndaj N_R
    for k in ("i_ulet", "i_larte"):
        r = zgjidh(V3, {y: 5e9 for y in V3}, 0.10, n_r=N_R[k])
        out(f"N_R {k}, 5 mld/vit | A_total_mld", r["A"] / 1e9)
        out(f"N_R {k}, 5 mld/vit | hendeku_mld", r["hendeku"] / 1e9)
        out(f"N_R {k}, 5 mld/vit | vonesa_mesatare_muaj", r["vonesa_mesatare_muaj"])

    def shkruaj(emri, rreshtat):
        with open(DIR / emri, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rreshtat for k in r)))
            w.writeheader(); w.writerows(rreshtat)
    shkruaj("faza2c_lp_skenaret.csv", sken); shkruaj("faza2c_lp_kalendari.csv", kal)
    shkruaj("faza2c_lp_rezultatet.csv", rez)
    for s in sken:
        print(s)
    for r in rez[-7:]:
        print(r)

if __name__ == "__main__":
    main()
