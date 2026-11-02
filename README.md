# Paga e magjistratëve pas Vendimit të Gjykatës Kushtetuese №15/2026 — modeli dhe llogaritjet

Kodi i riprodhueshëm i studimit *« Paga e magjistratëve pas Vendimit të Gjykatës Kushtetuese me №15/2026: një propozim juridiko-matematikor për riparimin e uljes së fshehtë, indeksimin dhe shlyerjen e prapambetjeve »* (Endri Prifti, tetor 2026).

Shifrat e tekstit të studimit dalin nga këto skripte dhe gjenden në skedarët CSV; `faza3_kontrolli.py` e kontrollon këtë heuristikisht (prania e shifrës, jo kuptimi i saj). Të dhënat janë verifikuar deri më 7.10.2026.

## Versioni i cituar në punim

Commit-i i cituar në punim jepet në Shtojcën B të tij dhe përmban kodin, të dhënat hyrëse (përfshirë PDF-të e INSTAT-it) dhe rezultatet e cituara. Commit-et pasuese ndryshojnë vetëm këtë README. Për ta riprodhuar saktësisht:

```bash
git clone https://github.com/endriprifti/pagat-magjistrateve-modeli
cd pagat-magjistrateve-modeli
git checkout <commit-i nga Shtojca B>
```

## Instalimi

Rezultatet u prodhuan me Python 3.13 dhe versionet e fiksuara në `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
```

## Riprodhimi

```bash
python3 faza1_llogaritjet.py      # seritë e R, korridori, validimi me KLSH, kalibrimi N_R
python3 faza2d_testet.py          # rillogarit radhazi gjithë Fazën 2 (2a–2d)
python3 faza3_rishikim.py         # ndjeshmëria, projeksioni, shkasi, menyja e vendimit
python3 faza3_prapambetje.py      # prapambetja për magjistrat
python3 faza3_grafik.py           # Figura 1
python3 faza3_kontrolli.py teksti/Faza3_punimi_perfundimtar.md   # kontrolli heuristik i shifrave të tekstit përfundimtar
```

Skriptet `faza1_thesari.py`, `faza1_hicp.py` dhe `faza1_instat.py` përpunojnë eksportet origjinale (Thesari, INSTAT), të cilat gjenden në dosjen `te_dhena/`, bashkë me datat e shkarkimit dhe komandat e riprodhimit (`te_dhena/README.md`). Rezultatet e tyre (`faza1_*.csv`) janë gjithashtu në depo, prandaj fazat e tjera ekzekutohen edhe pa to.

Skripti `faza3_kontrolli.py` verifikon heuristikisht që shifrat e tekstit (me ndarës mijëshe, përfshirë hapësirën e shumave të projektligjit, ose me presje dhjetore) të gjenden në skedarët e rezultateve; ai nuk verifikon prejardhjen ose kuptimin e shifrës, të cilat dokumentohen në skriptin që e prodhon (shih kolonën « Rezultati » më poshtë dhe mbishkrimet e tabelave në punim).

## Struktura

| Skripti | Çfarë llogarit | Rezultati |
|---|---|---|
| faza1_llogaritjet.py | Seritë e R, korridori, struktura W, validimi me KLSH, kalibrimi N_R | faza1_rezultatet.csv |
| faza1_thesari.py | Pagesat e Thesarit dhe paga neto për frymë | faza1_thesari*.csv |
| faza1_instat.py, faza1_hicp.py | Paga mesatare dhe indekset e çmimeve | faza1_instat_pagat_tremujore.csv, faza1_ichk_mujor.csv |
| faza2a_model.py | Kufizimet, rruga minimale, prapambetja, kostoja | faza2a_*.csv |
| faza2_burimet_shtese.py | Kategoritë e lidhura, pensioni suplementar | faza2_burimet_shtese.csv |
| faza2b_alternativat.py | Alternativat A0–A5 | faza2b_*.csv |
| faza2c_paketa.py, faza2c_lp.py | Formula e niveleve; kalendari « së pari muajt më të vjetër » (Neni 6/2) | faza2c_*.csv |
| faza2d_testet.py | Analiza fiskale, testi historik, stresi, konsistenca | faza2d_*.csv |
| faza3_rishikim.py | Seksionet (a)–(k) të rishikimit | faza3_rishikim.csv, faza3_projeksion.csv, faza3_rruget_grafik.csv |
| faza3_grafik.py | Figura 1 (R e paguar e rindërtuar: nivelet e akteve deri 12.2023, nivelet që përputhen me pagesat e agreguara të Thesarit 1.2024–9.2026, e supozuar 10–12.2026) | faza3_figura1.png |
| faza3_prapambetje.py, faza3_kontrolli.py | Prapambetja individuale; kontrolli i tekstit | faza3_*.csv |

Teksti burimor i versionit të 8 tetorit 2026 është në `faza3a_tekst.txt` dhe `faza3b_tekst.txt`; `faza3_ndertues.js` (Node.js + paketa `docx`) e ndërton prej tyre dokumentin Word. Versioni përfundimtar i punimit u redaktua më pas drejtpërdrejt në Word dhe është ai që bën autoritet. Teksti i tij, i nxjerrë me `pandoc Faza3_punimi_perfundimtar.docx -t markdown --wrap=none -o teksti/Faza3_punimi_perfundimtar.md`, ruhet në `teksti/` (gjurma SHA256 në `teksti/SHA256SUMS`), dhe mbi të u prodhua `faza3_konsistenca.csv`. Commit-i i cituar në Shtojcën B përmban kodin, të dhënat dhe rezultatet; teksti përfundimtar, i cili e citon atë, dhe regjistri i kontrollit mbi këtë tekst shtohen në commit-in pasardhës, i cili nuk ndryshon asnjë skript ose rezultat.

```bash
npm install docx
node faza3_ndertues.js punimi.docx faza3a_tekst.txt faza3b_tekst.txt
```

`Faza1_pagat_magjistrateve.md` dhe `Faza2_pagat_magjistrateve.md` janë dokumentet e punës të fazave të mëparshme (burimet, vendimet metodologjike, erratat).
