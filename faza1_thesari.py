"""
Faza 1 — Evidenca nga pagesat e Thesarit (BIG_TABLE.xlsx, financa.gov.al), 2024–5.10.2026.
Qëllimi: të verifikohet si u paguan pagat e gushtit dhe shtatorit 2026 (D9, D16).

Ekzekutimi: python3 faza1_thesari.py BIG_TABLE.xlsx  → faza1_thesari.csv
Shënim: tabela përmban rreshta të dyfishtë (i njëjti transaksion në dy llogari ose fletë);
ato hiqen me çelësin (përshkrimi, shuma, përfituesi, data e ekzekutimit).
"""
import sys
import re
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "BIG_TABLE.xlsx"
df = pd.read_excel(src)
df["EC"] = df["EC_ACCOUNT"].astype(str).str.strip()
df["d"] = pd.to_datetime(df["DATA_EKZEKUTIMIT"], format="%d.%m.%Y", errors="coerce")
df["desc"] = df["PERSHKRIMI_FATURES"].astype(str).str.replace(r"\s+", " ", regex=True).str.lower()
df["key"] = df.desc + "|" + df.SHUMA.astype(str) + "|" + df.FURNITORI.astype(str) + "|" + df.DATA_EKZEKUTIMIT.astype(str)
n0 = len(df)
u = df.drop_duplicates("key")
print(f"Rreshta: {n0}; pas heqjes së dyfishimeve: {len(u)}")

# Pagat (6001001 / 6002001), sipas datës së ekzekutimit, qershor–tetor 2026
pag = u[u.EC.isin(["6001001", "6002001"]) & (u.d >= "2026-05-25")].copy()
pag["muaji_pages"] = pag.desc.str.extract(r"pag[ae].*?\b(maj|qershor|korrik|gusht|shtator)\b")[0]
pag["vendim_gjyq"] = pag.desc.str.contains(r"vendim\w* (?:nr )?\d|vendim gjykat|vend gjyq", regex=True)
pag["ligji_95"] = pag.desc.str.contains(r"ligji nr 9[56]/2026", regex=True)
tab = (pag.groupby(["KODI_INSTITUCIONIT", "DATA_EKZEKUTIMIT", "muaji_pages", "vendim_gjyq", "ligji_95"], dropna=False)
          .SHUMA.sum().reset_index().sort_values(["KODI_INSTITUCIONIT", "DATA_EKZEKUTIMIT"]))
tab.to_csv("faza1_thesari.csv", index=False)
print(tab.to_string(index=False))

# Pagë neto për frymë në rreshtin homogjen të Gjykatës Administrative të Shkallës së Parë Tiranë
# (rreshti "plan/fakt 104/2x" ose "104/20": i njëjti grup punonjësish çdo muaj)
gas = u[(u.KODI_INSTITUCIONIT == 1029048) & u.EC.isin(["6001001", "6002001"]) & (u.d >= "2026-05-25")]
print("\nGjykata Adm. Shk. I Tiranë — rreshti 104/20–23:")
frymë = []
for _, r in gas.sort_values("d").iterrows():
    m = re.search(r"104/(2\d)\b", r.desc)
    if m:
        n = int(m.group(1))
        print(f"  {r.DATA_EKZEKUTIMIT}  {r.SHUMA:>12,.0f} / {n} = {r.SHUMA / n:>10,.0f} neto/frymë   {r.desc[30:95]}")
        frymë.append({"data": r.DATA_EKZEKUTIMIT, "shuma": r.SHUMA, "persona": n, "neto_per_fryme": round(r.SHUMA / n),
                      "pershkrimi": r.desc[30:95]})
pd.DataFrame(frymë).to_csv("faza1_thesari_per_fryme.csv", index=False)

# Pagesa me vendim gjyqësor për paga (diferenca, ekzekutime), 2024–2026
vg = u[u.EC.str.match(r"^600[12]|^6027") & u.desc.str.contains(r"vend\w* gjyq|vend\w* gjyk|gjyk adm|dif\w* pag|ekz\w* vend", regex=True)]
print("\nPagesa page/diferenca me vendim gjyqësor (mln lekë):")
print((vg.groupby(["KODI_INSTITUCIONIT", vg.d.dt.year]).SHUMA.sum() / 1e6).round(2).to_string())
