"""
Faza 2c — kalendari i shlyerjes së prapambetjeve sipas rregullit « së pari muajt më të vjetër » (Neni 6/2 i projektligjit).

E drejta (ekzistenca dhe masa) llogaritet veçmas: a_m = N_R · (R_paketës,m − R_paguar,m)⁺ për çdo
muaj m nga 4.2023 deri 12.2026 (supozim d: paketa hyn në fuqi më 1.1.2027).
Kalendari vendos vetëm KUR paguhet, jo SA.

Rregulli (përcaktues, pa optimizim): në çdo vit y, kufiri vjetor i kryegjësë B_y shpenzohet për detyrimin e
muajit më të vjetër ende të pashlyer; një muaj i mëvonshëm fillon të paguhet vetëm pasi muaji paraardhës
është shlyer plotësisht. Kufiri vjetor nuk mund të jetë më i ulët se p_min · A (Neni 6/2: 10% e detyrimit);
kufiri efektiv kthehet në rezultat. Kjo dysheme nuk detyron pagesë minimale kur detyrimi shlyhet më herët.
Pjesa që mbetet pas vitit të fundit raportohet si « hendek para shlyerjes përfundimtare »; sipas Nenit 6/2 ajo
shlyhet në vitin 2029 mbi kufirin (faza2d_testet.py e përfshin këtë pagesë në gamën fiskale).
Vonesa mesatare = muajt nga muaji i detyrimit deri në 1 korrik të vitit të pagesës, vetëm për kryegjënë e paguar.
Kompensimi i vlerës reale (d): faktori IÇK nga muaji i detyrimit deri në korrikun e vitit të pagesës;
IÇK reale deri 8.2026, pastaj 3%/vit (objektivi i BSH).
Dalja: faza2c_lp_kalendari.csv, faza2c_lp_skenaret.csv, faza2c_lp_rezultatet.csv
"""
import csv
from faza2a_model import DIR, N_R, ICHK, muajt
from faza2c_paketa import rruga_paketes

def muaj_indeks(m):
    y, mm = map(int, m.split("-")); return y * 12 + (mm - 1)

def detyrimet(n_r=N_R["qendror"]):
    rr = rruga_paketes("2026-12")
    return [(r["muaji"], n_r * max(r["R"] - r["R_paguar"], 0.0)) for r in rr if r["R"] - r["R_paguar"] > 0.5]

def I_at(m):
    if m in ICHK:
        return ICHK[m]
    k = muaj_indeks(m) - muaj_indeks("2026-08")
    return ICHK["2026-08"] * 1.03 ** (k / 12)

def zgjidh(vitet, B, p_min, n_r=N_R["qendror"]):
    """Kalendari sipas rregullit « së pari muajt më të vjetër ». B: viti → kufiri vjetor i kryegjësë (lekë)."""
    det = detyrimet(n_r)
    A = sum(v for _, v in det)
    B_ef = {y: max(B[y], p_min * A) for y in vitet}          # dyshemeja e kufirit (Neni 6/2)
    mbetja = [[m, v] for m, v in det]
    kal = []
    for y in vitet:
        b = B_ef[y]
        for d in mbetja:
            if b <= 0:
                break
            if d[1] <= 0:
                continue
            x = min(d[1], b); d[1] -= x; b -= x
            kal.append((d[0], y, x))
    paguar = {y: sum(x for _, yy, x in kal if yy == y) for y in vitet}
    tot = sum(paguar.values())
    vonesa_mes = (sum(x * (muaj_indeks(f"{y}-07") - muaj_indeks(m)) for m, y, x in kal) / tot) if tot > 0 else 0.0
    komp = sum(x * (I_at(f"{y}-07") / I_at(m) - 1) for m, y, x in kal)
    return {"A": A, "paguar": paguar, "hendeku": sum(v for _, v in mbetja), "kufiri_efektiv": B_ef,
            "vonesa_mesatare_muaj": vonesa_mes, "kompensimi_IÇK": komp,
            "kalendari": [(m, y, x) for m, y, x in kal if x > 1]}

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
               "vonesa_mesatare_muaj": round(r["vonesa_mesatare_muaj"], 2),  # vetëm kryegjëja e paguar
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
