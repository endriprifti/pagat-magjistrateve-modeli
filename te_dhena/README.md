# Të dhënat hyrëse

Eksportet origjinale nga të cilat skriptet e Fazës 1 ndërtojnë seritë. Ato u shkarkuan më **7 tetor 2026** (data e verifikimit të studimit), përveç tabelës 3 të IÇK-së me saktësi të plotë, e cila u shkarkua më 2 nëntor 2026 për ndjeshmërinë e Shtojcës B. Çdo skedar CSV i Fazës 1 në rrënjën e depos riprodhohet saktësisht nga këto skedarë me komandat e mëposhtme.

| Dosja / skedari | Burimi | Mbulimi | Skripti | Rezultati |
|---|---|---|---|---|
| `thesari/BIG_TABLE.xlsx` | Ministria e Financave, « Pagesa të kryera nga Drejtoria e Përgjithshme e Thesarit » (financa.gov.al), regjistrat ditorë për dhjetë kode institucionesh të sistemit të drejtësisë | janar 2024 – 5 tetor 2026 | `faza1_thesari.py` | `faza1_thesari.csv`, `faza1_thesari_per_fryme.csv` |
| `instat/Instat_IChK_20261007.xlsx` | INSTAT, « Indeksi i Çmimeve të Konsumit », seria mujore, ECOICOP v2 (eksport i databazës, 7.10.2026, ora 20:43) | janar 2016 – gusht 2026 | `faza1_hicp.py` | `faza1_ichk_mujor.csv` |
| `instat/Instat_IHCK_20261007.xlsx` | INSTAT, « Indeksi i Harmonizuar i Çmimeve të Konsumit », seria mujore (eksport, 7.10.2026, ora 20:36) | janar 2016 – gusht 2026 | `faza1_hicp.py` | `faza1_hicp_mujor.csv` |
| `instat/Instat_IChK_tab3_20261102.xlsx` | INSTAT, « Indeksi i Çmimeve të Konsumit », tabela 3, indekset me saktësi të plotë (shkarkuar më 2.11.2026; bazë tjetër nga eksporti i databazës) | janar 2017 – dhjetor 2025 | `faza3_rishikim.py`, seksioni (k) | R 1.2026 me saktësi të plotë (ndjeshmëri) |
| `instat_pagat/pdf/*.pdf` (31 skedarë) | INSTAT, « Paga mesatare mujore bruto », njoftimet tremujore për shtyp | T4/2018 – T2/2026 | — | — |
| `instat_pagat/txt/*.txt` | tekstet e PDF-ve të mësipërme, nxjerrë me `pdftotext -layout` | po aty | `faza1_instat.py` | `faza1_instat_pagat_tremujore.csv` |

## Riprodhimi

```bash
python3 faza1_thesari.py te_dhena/thesari/BIG_TABLE.xlsx
python3 faza1_hicp.py te_dhena/instat/Instat_IChK_20261007.xlsx faza1_ichk_mujor.csv
python3 faza1_hicp.py te_dhena/instat/Instat_IHCK_20261007.xlsx faza1_hicp_mujor.csv
python3 faza1_instat.py te_dhena/instat_pagat/txt
```

Për të rinxjerrë tekstet nga PDF-të: `for f in te_dhena/instat_pagat/pdf/*.pdf; do pdftotext -layout "$f" "te_dhena/instat_pagat/txt/$(basename "$f").txt"; done`.

## Shënime

- Regjistri i Thesarit përmban vetëm pagesat e ekzekutuara; muaji i pagës nxirret nga përshkrimi i faturës (`faza1_thesari.py`). Paga e shtatorit 2026 (paguar më 2.10.2026) është e fundit e regjistruar. Rruga e R së paguar në figurën 1 është e rindërtuar: nivelet e akteve deri në dhjetor 2023, nivelet që përputhen me pagesat e agreguara të Thesarit nga janari 2024 deri në shtator 2026 dhe supozim për tetor–dhjetor 2026. Regjistrat e Thesarit nuk e tregojnë drejtpërdrejt pagën referuese të çdo magjistrati.
- Aktet normative, vendimet e Gjykatës Kushtetuese, raportet e KLSH-së dhe dokumentet parlamentare që citon studimi nuk përfshihen këtu: ato janë dokumente publike, të renditura në bibliografinë e punimit.
