# Pagat e magjistratëve pas Vendimit nr. 15/2026 — Faza 2

**Nënhapi 2a: §6 Modeli matematikor dhe kodi bazë**

Data e verifikimit: **7 tetor 2026**. Kodi: `faza2a_model.py`. Ai prodhon `faza2a_rezultatet.csv` (çdo shifër e këtij seksioni), `faza2a_rruget_min.csv` (rrugët mujore), `faza2a_shembuj.csv` (shembujt e riprodhueshëm) dhe `faza2a_fjalori.csv`. Skedari është edhe modul: nënhapat 2b–2d e importojnë dhe nuk i rillogaritin formulat.

Shënimet (a)–(e) ndjekin §3 të detyrës. Ky nënhap ndërton vetëm mekanizmin. **Asnjë alternativë nuk vlerësohet këtu**; vlerësimi i tyre është në 2b.

**Të konfirmuara nga autori më 8.10.2026 (Faza 1, "Vendimet e autorit").** Parazgjedhjet e përdorura për pikat P1–P9 të Fazës 1: P1 sipas supozimit të autorit, me dy skenarë paralelë A/B; P2 korridori si konstruksion analitik (b); P3 tavani i indeksimit si parametër θ, i patestuar ende; P4 riparimi nga 2023; P5 dhe P6 jashtë modelit bazë; P7 model alternativ i plotë; P8 të dyja referencat si parametër; P9 198.963 vetëm si alternativë krahasuese.

---

## 6.0 Çfarë duhet të zgjidhë modeli

Modeli i përgjigjet katër pyetjeve, secila me formulën e vet:

1. **Baza:** cila R është ligjërisht e mbrojtshme në 1.4.2023, data nga e cila V15 §110 kërkon efektet? (F2)
2. **Dinamika:** si duhet të lëvizë R pas 1.4.2023 që të mos ketë "ulje të fshehtë" (K4–K5) dhe të ruhet vlera reale (K9)? (F3–F5)
3. **E kaluara:** sa është detyrimi i prapambetur ndaj asaj që u pagua faktikisht? (F6)
4. **Kostoja:** sa kushton çdo zgjidhje, edhe pa numrin e magjistratëve sipas profilit (D8)? (F7)

Pyetja e pestë, nëse një rrugë konkrete e R i plotëson të gjitha kufizimet, i përgjigjet testit F8. Ky test përdoret në 2b dhe 2d.

**Pse ky model dhe jo një më kompleks.** Paga totale është lineare në R (Faza 1 §4.3, e validuar me KLSH). Prandaj problemi reduktohet në një seri të vetme kohore R_t. Mjaftojnë kufizime të thjeshta "R duhet të jetë të paktën…", të llogaritura muaj pas muaji. Mjetet e tjera të shqyrtuara jepen në §6.6.

---

## 6.1 Fjalori i simboleve

Ky fjalor vlen për gjithë punimin (`faza2a_fjalori.csv`).

| Simboli | Kuptimi | Njësia | Burimi |
|---|---|---|---|
| t | muaji kalendarik | muaj | — |
| R_t | paga referuese bazë e magjistratit në muajin t | lekë/muaj bruto | L96 neni 12 |
| R*_0 | baza e riparuar në 1.4.2023 | lekë/muaj bruto | V15 §§109–110 |
| R_V35 | e drejta e fituar, shtator 2022 = 152.700 | lekë/muaj bruto | V15 §95; VKM 621/2022 |
| P_t | paga e Presidentit | lekë/muaj bruto | ligji 34/2023 |
| κ | koeficienti R/P | numër i pastër | L95 neni 1 |
| Ref_t | referenca e zgjedhur: civile (I-2 + 14.000) ose P_t | lekë/muaj | V15 §109 |
| W | paga mujore bruto totale e një magjistrati | lekë/muaj bruto | L96 nenet 2/j, 12, 14 |
| ω | shumëzuesi i profilit, W/R | numër i pastër | F1 |
| γ, λ, δ, y | shtesa e grupit, shtesa drejtuese, shtesa GJKKO/SPAK, vitet e vjetërsisë | numra të pastër; vite | L96 |
| g_civ, g_P | rritjet e referencave 2022→2023 (≈44% dhe 65,4%) | përqindje kumulative | V15 §100 |
| L, U | kufiri i poshtëm dhe i sipërm i korridorit për R*_0 | lekë/muaj | F2 (b) |
| I_t | indeksi i çmimeve të konsumit (IÇK kombëtar) | indeks | INSTAT |
| π | inflacioni kumulativ ndërmjet dy muajve | përqindje kumulative | F3 |
| ρ | ndryshimi kumulativ i referencës ndërmjet dy muajve | përqindje kumulative | F3 |
| g | rritja e R në një datë rishikimi | përqindje kumulative | F4 |
| θ | tavani i indeksimit (target i BSH + 1 p.p.) | përqindje | ligji 33/2023; L95 |
| τ_k | data e rishikimit k (çdo ≤ 2 vjet; e para 1.1.2026) | muaj | ligji 33/2023; L95 |
| A | prapambetja, diferenca e papaguar e akumuluar | lekë bruto | F6 |
| N_R | njësi-R: Σ W_i / R, kosto mujore për 1 lekë rritje të R | magjistratë-ekuivalentë | Faza 1 §4.5 |
| c | norma e kontributeve të punëdhënësit | përqindje | AN 2/2026 |
| ΔC | kosto shtesë vjetore | lekë/vit | F7 |
| A / B | skenarët juridikë: A = aktet e Këshillave të vlefshme; B = Këshillat pa kompetencë | — | Faza 1, P1 |

**Konventa.** "Përqindje kumulative" do të thotë ndryshim i plotë midis dy datave, jo normë vjetore. Kur flitet për diferencë normash (p.sh. "target + 1"), përdoret "pikë përqindjeje" (p.p.).

---

## 6.2 Arkitektura: kufizime të detyrueshme, jo pikë të ponderuara

Modeli ka tri **variabla zgjedhjeje** të ligjvënësit:
- baza R*_0;
- referenca (civile ose Presidenti);
- rregulli i indeksimit.

Kushtetutshmëria hyn si **bashkësi kufizimesh** C1–C6. Një zgjidhje që shkel ndonjërin prej tyre nuk "kompensohet" me kursim buxhetor. Prandaj modeli nuk maksimizon asnjë shumë të ponderuar "kushtetutshmëri + kosto" (§3 i detyrës).

| Kufizimi | Përmbajtja | Kërkesa | Statusi |
|---|---|---|---|
| **C1** | R*_0 ≥ L | K6–K7, V15 §109 | (a) për detyrimin e riparimit; (b) për leximin si korridor |
| **C2** | R*_0 ≤ U | K7, "brenda limiteve të tyre" | (b) |
| **C3** | R_t ≥ R_{t−1} (pa ulje nominale) | K4, K17, neni 138 | (a) |
| **C4** | R_t ≥ R*_0 · Ref_t / Ref_0 (R ndjek referencën e vet) | K5, V15 §92 | (a) |
| **C5** | në çdo datë rishikimi τ_k: R ≥ R e rishikimit të mëparshëm · (1 + g_k) | K9, V15 §§83–85 | (a) për detyrimin; (d) për rregullin g, që testohet me variante |
| **C6** | vetëm në skenarin A: R_t ≥ 236.425 nga 8.2026 | P1, mosregresion ndaj akteve të Këshillave | (b) |

Kërkesat procedurale (K2, K3, K18: ligji, konsultimi, automatizmi) nuk janë pabarazi numerike. Ato trajtohen si garanci procedurale në dispozitat model të Fazës 3.

**Si zgjidhet brenda bashkësisë së realizueshme.** Modeli llogarit së pari **rrugën minimale të realizueshme**: vlerën më të ulët të R që plotëson njëkohësisht C1–C6 në çdo muaj (F5). Kjo është kostoja minimale e pajtueshmërisë. Krahasimi i alternativave mbi këtë kufi (kosto, qëndrueshmëri, pranueshmëri institucionale), përfshirë analizën Pareto kur ajo justifikohet, bëhet në 2b.

---

## 6.3 Formulat

### F1 — Paga totale e një magjistrati (c)

**W = R · [(1 + γ)(1 + λ + δ) + 0,02 · min(y, 25)] = ω · R**

*Me fjalë të thjeshta:* paga totale = R shumëzuar me një numër ω që varet vetëm nga profili (grupi, vjetërsia, pozicioni drejtues, GJKKO/SPAK). Nëse R rritet me 10%, paga e çdo magjistrati rritet me 10%, dhe raportet midis tyre (hierarkia, K14) nuk ndryshojnë.

*Parametrat:* γ ∈ {0,90; 0,98; 1,06}; λ ∈ {0; 0,05; 0,10}; δ = 0,80 për GJKKO/SPAK, përndryshe 0 (L96).

*Shembull i riprodhueshëm:* gjyqtar G2, 15 vjet, pa pozicion drejtues: ω = 1,98 + 0,30 = **2,28**. Me R = 219.888, W = **501.345** lekë; me R = 165.537,5 (L95 në 2026), W = **377.426** lekë. Kontroll me KLSH: G3, 25 vjet, kryetar, R = 118.100 → 326.665 (KLSH: 326.664).

### F2 — Korridori i riparimit të bazës (a/b)

**L = R_V35 · (1 + g_civ)  dhe  U = R_V35 · (1 + g_P)**, me R_V35 = 152.700, g_civ = 0,44 dhe g_P = 425.000/257.000 − 1.

*Me fjalë të thjeshta:* nga shtatori 2022 në prill 2023 pagat e referencave u rritën ≈44% (kategoria civile) dhe 65,4% (Presidenti). Riparimi i "uljes së fshehtë" kërkon që R e magjistratëve të rritet në masë të krahasueshme, brenda këtyre dy rritjeve (§109).

*Rezultati:* **L = 219.888**, **U = 252.519** lekë; κ ∈ [0,517; 0,594].

*Ndjeshmëria:* me 44% të saktë (43,95%, gjurma II-a → I-5), L = 219.805. Diferenca prej 83 lekësh nuk ndryshon asnjë përfundim. Korridori është konstruksion analitik i leximit të §109, jo rregull i shprehur i Gjykatës (korrigjimi 1). Prandaj çdo vlerë brenda tij kërkon arsyetim të veçantë juridik në 2b.

### F3 — Inflacioni dhe rritja e referencës (c)

**π = I_{t2} / I_{t1} − 1** ;  **ρ = Ref_{t2} / Ref_{t1} − 1**

*Me fjalë të thjeshta:* π tregon sa u shtrenjtua jetesa midis dy datave; ρ tregon sa u rrit paga e referencës në të njëjtën periudhë. Të dyja janë ndryshime kumulative, jo norma vjetore.

| Periudha | Vlera |
|---|---|
| π, 3.2023 → 12.2025 (para rishikimit të 1.1.2026) | **5,43%** |
| π, 3.2023 → 8.2026 | 7,62% |
| π, 8.2022 → 3.2023 (tashmë brenda korridorit) | 4,13% |
| ρ civile, 4.2023 → 1.2026 (217.000 → 222.425 në I-2) | 2,35% |
| ρ Presidenti, 4.2023 → 1.2026 | 0,00% |
| ρ civile, 9.2022 → 4.2023 (gjurma e saktë sipas V35) | 51,28% |

**Rregulli kundër numërimit të dyfishtë (kontrolli 3 i §12).** Inflacioni i periudhës 2022–2023 (4,13%) është tashmë i "përfshirë" në rritjet 44–65% të referencave, prandaj nuk shtohet mbi korridorin. Inflacioni numërohet vetëm **nga baza e riparuar e prillit 2023 e tutje**: nga muaji para bazës (3.2023) deri te muaji para rishikimit.

### F4 — Rregulli i indeksimit në një datë rishikimi (d)

**g = max(π, ρ)**, me variantet krahasuese g = π, g = ρ dhe g = min(π, θ).

*Me fjalë të thjeshta:* në datën e rishikimit, R rritet me më të madhen nga dy rritjet: sa u shtrenjtua jetesa, ose sa u rrit paga e referencës. Nuk i mblidhen të dyja: rritja e referencës është vetë, pjesërisht, kompensim për inflacionin, dhe mbledhja do ta numëronte atë dy herë.

*Shembull (1.1.2026, referenca civile):* π = 5,43%, ρ = 2,35%, pra **g = 5,43%**. Mbledhja e gabuar do të jepte 7,78%. Me tavanin e L95 (θ = 4%, nëse indeksimi kryhet në masën maksimale të lejuar) g = 4,00%.

Asnjë nga variantet nuk shpallet paraprakisht kushtetues (korrigjimi 5). Ato krahasohen në 2b dhe 2d.

*Shënim nga 2c:* në paketën përfundimtare, max(π, ρ) zbatohet mbi **nivelet kumulative që nga baza**, jo rishikim pas rishikimi, që të shmanget efekti i çikrikut (§8.2–8.3). Me vetëm një rishikim deri në 2026, dy shkrimet japin të njëjtat shifra në §§6–7.

### F5 — Rruga minimale e realizueshme (d, mbi kufizimet a/b)

Duke nisur nga R*_0 në 4.2023, për çdo muaj t:

**R_t = max{ R_{t−1} [C3];  R*_0 · Ref_t / Ref_0 [C4];  R_{τ_{k−1}} · (1 + g_k) në datën τ_k [C5];  236.425 nga 8.2026, vetëm në A [C6] }**

*Me fjalë të thjeshta:* çdo muaj, R duhet të jetë të paktën sa më e madhja nga këto katër "dysheme": muaji i kaluar; referenca e vet; vlera reale e ruajtur në datën e rishikimit; dhe, në skenarin A, niveli i Këshillave. Rruga që del është më e lira e mundshme pa shkelur asnjë kufizim. Kolona `kufizimi_lidhes` në `faza2a_rruget_min.csv` tregon cili kufizim vendos në çdo muaj.

*Rezultati për R*_0 = L = 219.888, me rregullin g = max(π, ρ):*

| Muaji | Skenari A | Skenari B | Kufizimi që vendos |
|---|---|---|---|
| 4.2023 – 12.2025 | 219.888 | 219.888 | C4 (referenca e pandryshuar 2023–2025) |
| 1.2026 | **231.823** | **231.823** | C5 (vlera reale, π = 5,43%) |
| 7.2026 | 231.823 | 231.823 | C3 |
| 8.2026 – 12.2026 | **236.425** | 231.823 | A: C6; B: C3 |

Rezultati është i njëjtë për të dyja referencat. Arsyeja: në 1.2026 inflacioni (5,43%) e kalon si rritjen civile (2,35%) ashtu edhe atë të Presidentit (0%), prandaj kufizimi lidhës është C5.

*Ndjeshmëria ndaj tavanit:* me g = min(π; 4%), R_min në 1.2026 është 228.684, pra **1,35% më pak** se me ruajtje të plotë të vlerës reale. Kjo është masa e erozionit real që tavani i L95 do të kishte prodhuar në rishikimin e parë (P3).

### F6 — Prapambetja (d)

**A = ω · Σ_t max(R_t − R_paguar,t; 0)**, nga 4.2023 deri në muajin para hyrjes në fuqi të zgjidhjes.

*Me fjalë të thjeshta:* për çdo muaj, merret diferenca midis R që duhej paguar dhe R që u pagua, shumëzohet me ω të profilit dhe mblidhet. Për gjithë sistemin, ω zëvendësohet me N_R.

*R e paguar (c, Faza 1 §4.6; d për 2026):* 153.000 për 4.2023–12.2025; 156.825 për 1–7.2026 (VKM 93/2026: indeksim 2,5%); 236.425 në gusht 2026 (me vendim gjyqësor); 165.537,5 nga shtatori 2026 (L95 me P = 435.625; d). Muajt kur R e paguar e kalon R të detyrueshme nuk krijojnë detyrim negativ: modeli nuk parashikon kthim pagash, sepse kjo do të ishte vetë ulje (C3).

*Shembull i riprodhueshëm:* G2, 15 vjet, rruga minimale nga L, 4.2023–7.2026: A = 2,28 × 2.732.293 = **6.229.629 lekë bruto**.

*Në nivel sistemi (N_R = 3.954, rruga minimale nga L):*

| Periudha | Skenari A | Skenari B |
|---|---|---|
| 4.2023 – 7.2026 | **10,80 mld lekë** | **10,80 mld lekë** |
| 4.2023 – 12.2026 (nëse zgjidhja hyn në fuqi më 1.1.2027; d) | 11,92 mld lekë | 11,85 mld lekë |

Këto janë vlerat e **kufirit të poshtëm të realizueshëm**, jo propozim. Për krahasim, skema e Këshillave (A1, §7.5) jep 12,38 mld për 4.2023–7.2026. Kalendari i shlyerjes modelohet në 2c.

### F7 — Kosto shtesë vjetore (d)

**ΔC = 12 · N_R · (R_e_re − 165.537,5) · (1 + c)**

*Me fjalë të thjeshta:* sa kushton më shumë në vit, krahasuar me L95, të paguhet R e re. N_R zëvendëson numrin e munguar të magjistratëve sipas profilit (Faza 1 §4.5).

*Shembull i riprodhueshëm:* R = 236.425, N_R = 3.954, c = 0: ΔC = 12 × 3.954 × 70.887,5 = **3,36 mld lekë/vit**.

*Për rrugën minimale (R e dhjetorit 2026), sipas N_R:*

| | N_R = 3.000 | N_R = 3.954 | N_R = 4.902 | N_R = 3.954, c = 16,6% |
|---|---|---|---|---|
| Skenari A (236.425) | 2,55 mld | **3,36 mld** | 4,17 mld | 3,92 mld |
| Skenari B (231.823) | 2,39 mld | **3,15 mld** | 3,90 mld | 3,67 mld |

Nuk dihet nëse kalibrimi N_R i përfshin kontributet. Prandaj kolona e fundit është kufi i sipërm i kushtëzuar. Sipas korrigjimit 3, tavani buxhetor nuk është veto: nëse fondi nuk mjafton, raportohet hendeku i financimit.

### F8 — Testi i realizueshmërisë

Për çdo rrugë të propozuar R_t, testi kontrollon: C1–C2 (baza brenda korridorit), C3 (asnjë muaj me rënie) dhe C4–C6 (R_t nuk bie nën rrugën minimale të llogaritur nga e njëjta bazë). Rezultati varet nga rregulli C5 i zgjedhur, prandaj raportohet për secilin variant.

*Shembull i riprodhueshëm, rruga e Këshillave (231.000 për 4.2023–12.2025; 236.425 nga 1.2026; skenari A):*

| Rregulli C5 | C1–C2 | C3 | C4–C6 | Dyshemeja në 1.2026 | Mungesa |
|---|---|---|---|---|---|
| g = max(π, ρ) | ✓ | ✓ | ✗ | 243.539 | 7.114 |
| g = ρ (vetëm referenca) | ✓ | ✓ | ✓ | — | — |
| g = min(π; 4%) | ✓ | ✓ | ✗ | 240.240 | 3.815 |

Ky është vetëm shembull i funksionimit të testit, jo vlerësim i skemës së Këshillave (2b). Megjithatë, ai nxjerr një veti strukturore të rëndësishme: **ndjekja e referencës civile (C4) nuk garanton vetvetiu ruajtjen e vlerës reale (C5)**. Gjatë 2023–2025 paga I-2 nuk lëvizi, ndërkohë që inflacioni kumulativ arriti 5,43%. K5 dhe K9 janë kërkesa të dallueshme të V15 (§92 dhe §§83–85), dhe modeli i trajton veçmas.

---

## 6.4 Vetitë strukturore që dalin nga modeli (b, mbi llogaritjet c)

1. **Kufiri i poshtëm i korridorit nuk mbetet 219.888.** Pas rishikimit të parë (1.1.2026), ruajtja e vlerës reale e çon rrugën minimale në **231.823**. Pra, një ligj që riparon bazën në kufirin më të ulët dhe e ruan atë realisht arrin brenda 2,0% të nivelit të Këshillave (236.425) që në 2026.
2. **Skenarët A dhe B ndryshojnë vetëm nga 8.2026 dhe vetëm me 4.602 lekë/muaj në R** (236.425 kundrejt 231.823). Prapambetja 4.2023–7.2026 është identike në të dy skenarët. Kjo e bën P1 shumë më pak vendimtare për koston nga sa dukej në Fazën 1.
3. **Referenca civile dhe ajo e Presidentit japin të njëjtën rrugë minimale deri në 2026**, sepse asnjëra nuk u rrit mjaftueshëm sa të kalonte inflacionin. Zgjedhja e referencës (P8) bëhet vendimtare vetëm në vitet pasuese, kur referencat lëvizin.
4. **Rregulli g = max(π, ρ)** është i vetmi nga variantet që plotëson njëkohësisht K5 dhe K9 pa numërim të dyfishtë. Varianti "vetëm referenca" kalon testin për skemën e Këshillave vetëm sepse nuk mat vlerën reale. Kjo nuk e bën automatikisht atë rregull kushtetues (korrigjimi 5); krahasimi i plotë bëhet në 2b–2d.
5. **Tavani θ = 4% kushton 1,35% vlerë reale në rishikimin e parë.** Gjykata nuk e shfuqizoi tavanin (§106), por §§83–84 kërkojnë mbrojtje nga inflacioni. Tensioni është tani i matur (P3).

---

## 6.5 Negocimi Nash: pse nuk përdoret për R

**Pika e mosmarrëveshjes (b).** Pika e mosmarrëveshjes është ajo që ndodh nëse palët nuk bien dakord. Ajo nuk zgjidhet nga pozicionet e palëve; atë e cakton vetë Gjykata. §110 thotë se, në mungesë të ligjit, prapambetjet llogariten me formulën e funksionarit të administratës së lartë sipas V35. Me identifikimin I-2 të Fazës 1 (§4.2a), kjo jep rrugën 231.000 / 236.425. Kjo pikë **nuk është rrethore**: nuk varet nga asnjë dysheme e modelit dhe as nga oferta e ndonjë pale. Përmbajtja është e njëjtë në A dhe B; ndryshon vetëm kush e zbaton (Këshillat apo gjykatat).

**Pse zgjidhja Nash është e papërcaktuar këtu.** Gjyqësori preferon R më të lartë, ekzekutivi R më të ulët. Nash kërkon një marrëveshje ku asnjë palë nuk del më keq se në pikën e mosmarrëveshjes. Për gjyqësorin kjo do të thotë R ≥ R_d, për ekzekutivin R ≤ R_d. E vetmja vlerë që i plotëson të dyja është **R = R_d**. Me një variabël të vetme dhe me interesa të kundërta, Nash thjesht e kthen pikën e mosmarrëveshjes dhe nuk shton asgjë.

**Pse mesi 198.963 përjashtohet si zgjidhje.** Ai merr si pikë mosmarrëveshjeje R e L95 (161.500). Kjo është gjendje që shkel C1 (161.500 < 219.888), prandaj sipas korrigjimit 6 nuk mund të jetë pikë mosmarrëveshjeje. Vetë mesi bie nën L. Në 2b ai paraqitet vetëm si alternativë krahasuese.

**Ku mund të ketë hapësirë për marrëveshje.** Hapësirë reale për shkëmbim ekziston në **kalendarin e prapambetjeve**, p.sh. pagesë më e shpejtë kundrejt pagesës me këste. Por funksionet e dobisë për kohën (normat e skontimit të palëve) nuk kanë bazë në të dhëna. Prandaj kalendari modelohet në 2c me programim linear me kufizime transparente, jo me Nash.

---

## 6.6 Mjetet e shqyrtuara dhe të përjashtuara

| Mjeti | Vendimi | Arsyeja |
|---|---|---|
| Kufizime + rrugë minimale (F5) | **Përdoret** | Zgjidh drejtpërdrejt pyetjen "sa është minimumi i pajtueshëm" |
| Programim linear (LP) | **Përdoret në 2c** | Kalendari i prapambetjeve nën kufij buxhetorë dhe mosregresion |
| Analizë Pareto | **Në 2b**, vetëm nëse alternativat formojnë bashkësi të realizueshme të krahasueshme | Prompti ndalon etiketën "Pareto" për krahasime thjesht përshkruese |
| Skenarë transparentë | **Përdoren** | N_R (3.000 / 3.954 / 4.902), c (0 / 16,6%), θ, A/B |
| Monte Carlo | Jo | Shpërndarjet e propozuara (1 mld ±100 mln; 500 mln ±50 mln) nuk kanë bazë në të dhëna dhe i referohen koeficientit 0,38, jo skenarit të riparimit (korrigjimi 7) |
| Zinxhirët Markov / programimi dinamik i karrierës | Jo | Kërkojnë N dhe probabilitetet e kalimit (D8), që mungojnë. Duke qenë W lineare në R, vjetërsia nuk ndryshon renditjen e alternativave |
| Entropia e Shannon-it, K-Means, Isolation Forest | Jo | Pagesat e Thesarit janë klasifikuar tashmë me rregulla transparente (Faza 1 §4.6) |
| Rrjetet Petri | Jo | Kronologjia mbulohet nga grafi i varësisë së akteve (figurë në Fazën 3) |

---

## 6.7 Supozimet e modelit dhe varësia nga të dhënat

| Supozimi (d) | Ku ndikon | Çfarë e zëvendëson |
|---|---|---|
| ~~153.000 nuk u indeksua në 2026~~ → **e zgjidhur:** R e paguar 1–7.2026 = 156.825 (VKM 93/2026) | F6 (A) | — |
| ~~P = 425.000 e pandryshuar 2023–2026~~ → **e zgjidhur:** 425.000 në 2023–2025 (ligjet 97/2023, 115/2024); 435.625 nga 1.2026 (ligji 87/2025 neni 13; VKM 92/2026) | F3, referenca e Presidentit | — |
| Rishikimi i parë më 1.1.2026; inflacioni deri në muajin para tij | F5, C5 | Zgjedhje e ligjvënësit (data e rishikimit) |
| N_R ∈ {3.000; 3.954; 4.902} | F6, F7 | D8: numri sipas profilit |
| Gushti 2026 i paguar me 236.425 | F6 | D16: natyra e vendimeve gjyqësore |
| Zgjidhja hyn në fuqi më 1.1.2027 | F6, kolona deri në 12.2026 | Data reale e miratimit |

Asnjë nga këto supozime nuk e ndryshon **mekanizmin**. Ato ndryshojnë vetëm kalibrimin numerik.

---

## 6.8 Kontrolli i konsistencës për nënhapin 2a (§12)

| # | Kontrolli | Rezultati |
|---|---|---|
| 1 | Asnjë rregull indeksimi në kundërshtim me mosregresionin | ✓ C3 është pjesë e çdo rruge (F5). Varianti me tavan nuk prodhon ulje nominale, por prodhon erozion real (1,35%), i shënuar si P3. |
| 2 | Asnjë dysheme rrethore nga pika e mosmarrëveshjes | ✓ Dyshemetë C1–C6 vijnë nga V15, nga inflacioni ose nga aktet ekzistuese, jo nga pozicionet e palëve. Pika e mosmarrëveshjes (§110) nuk përdoret si dysheme (§6.5). |
| 3 | Pa numërim të dyfishtë të inflacionit | ✓ π matet nga 3.2023; inflacioni 2022–23 (4,13%) mbetet brenda korridorit; g = max, jo shumë (F3–F4). |
| 4 | Çdo shifër në tekst = skedari | ✓ `faza2a_rezultatet.csv` dhe `faza2a_shembuj.csv` |
| 5 | Argumentet e atribuuara Gjykatës | ✓ §§83–85, 92, 95, 100, 106, 109–110, të gjitha nga shumica |
| 6 | Simbolet njëtrajtësisht | ✓ Fjalori §6.1; i njëjtë me Fazën 1 (R, P, κ, W, γ, λ, δ, y) me shtesat e reja |

---

## 6.9 Përditësim nga burimet shtesë (7.10.2026, mbrëmje)

Skript: `faza2_burimet_shtese.py` → `faza2_burimet_shtese.csv`. Mekanizmi i §6.3 nuk ndryshon; ndryshon leximi i disa parametrave.

**1. Çfarë mat në të vërtetë N_R (c për të dhënat, b për përfundimin).** KLGJ 233/2025 cakton 417 pozicione gjyqtarësh. Me ω ∈ [1,90; 4,414] (F1), gjyqtarët zënë nga **792 deri në 1.841 njësi-R**. Kufiri i sipërm është teorik, sepse supozon që të gjithë janë kryetarë të GJKKO-së me 25 vjet. Nëse N_R = 3.954 do t'u përkiste vetëm gjyqtarëve, ω mesatar do të ishte 9,48, gjë e pamundur. Pra, **2.113–3.162 njësi-R** u përkasin prokurorëve, kategorive të lidhura dhe/ose kontributeve. Pasojat:
- N_R qendror është kosto e **gjithë sistemit me efektin zinxhir**, jo vetëm e magjistratëve. Kjo është baza e duhur për krahasimin me L95 vetëm nëse ngrirja e nenit 12/1 nuk zbatohet.
- Kolona F7 me c = 16,6% mund të numërojë kontributet dy herë, nëse ato janë tashmë brenda N_R. Ajo mbetet kufi i sipërm.
- Ndarja e N_R midis magjistratëve dhe kategorive të lidhura (P5) kërkon numrin e prokurorëve (D8).

**2. Kategoritë e lidhura (D10, P5; c).**
- Anëtarët e KLGJ dhe KLP kanë **statusin e magjistratit** dhe pagën e gjyqtarit të GJL (L115, nenet 4 dhe 102). Kjo vlen edhe për anëtarët jomagjistratë. Prandaj ata nuk janë "funksionarë të tjerë që referojnë" në kuptimin e nenit 12/1, par. 2, të L96 (b). Kjo përputhet me faktin që KLP i pagoi anëtarët sipas L95 në gusht (Faza 1 §4.6).
- ILD dhe Drejtori i Shkollës së Magjistraturës marrin pagën e gjyqtarit të GJL; inspektorët magjistratë, pagën e gjyqtarit të apelit (L115, nenet 198, 210, 250); këshilltarët ligjorë juristë të GJK, pagën bruto fillestare të gjyqtarit të shkallës së parë (L8577, neni 15). Për ta ligji nuk shprehet për statusin e magjistratit, prandaj janë kandidatë për ngrirjen e nenit 12/1 (b).
- Gjyqtarët e GJK marrin pagën e Kryetarit të GJL, Kryetari i GJK +20% (L8577, neni 17), me klauzolë mosuljeje (neni 17/3). Ligji nuk e përcakton vjetërsinë e "Kryetarit të GJL" që shërben si ankorë (d).
- **VKM 755/2023** ndau 1 mld lekë për "një pjesë" të diferencave sipas V35: 87,6% për sistemin e drejtësisë, 10,7% për institucionet e vetingut (KPK, KPA, Komisionerët) dhe 1,7% për KQZ dhe Avokatin e Popullit. Pra, **vetë ekzekutivi e ka trajtuar efektin zinxhir si real** (c). Kjo është gjithashtu shuma e parë e njohur e paguar për P6/D17.

**3. Tavani i indeksimit (P3; c).** Të shtatë RPM-të e BSH (2025/I–2026/III) e konfirmojnë objektivin 3% dhe asnjëra nuk përmban brez tolerance ±1 p.p. Pra, θ = 4% është **zgjedhje e ligjvënësit**, jo parametër i politikës monetare. Në T2/2026 inflacioni ishte mesatarisht 3%, dhe BSH e pret përkohësisht mbi objektiv. Seria jonë e IÇK jep 3,0–3,4% a/a për maj–gusht 2026, pra afër tavanit. Në 2b–2d, inflacioni i ardhshëm modelohet me skenarë transparentë rreth objektivit (BSH nuk boton parashikim numerik vjetor), jo me shpërndarje probabilistike.

**4. Inflacioni bazë (b).** Materiali teknik i BSH e përkufizon inflacionin bazë si tregues të prirjes për politikën monetare, ku përjashtohen artikujt me luhatje të lartë. V15 §84 i referohet IÇK-së, dhe qëllimi i K9 është kostoja e jetesës. Prandaj modeli përdor IÇK-në totale; inflacioni bazë nuk përdoret për indeksim.

**Ndikimi në §6.7:** supozimi N_R mbetet, por tani interpretohet si "sistem + kategori të lidhura". D8 dhe D10 janë pjesërisht të plotësuara; D7 është e mbyllur.

**Fundi i nënhapit 2a.** Nënhapi tjetër (2b, §7: alternativat) nis vetëm pas miratimit tuaj.


---

# §7 Alternativat dhe zgjedhja e paketës kryesore (nënhapi 2b)

Kodi: `faza2b_alternativat.py` (importon F1–F8 nga `faza2a_model.py`). Rezultatet: `faza2b_rruget.csv` (rrugët mujore), `faza2b_testet.csv` (F8), `faza2b_profilet.csv` (F1), `faza2b_kosto.csv` (F6–F7), `faza2b_projeksion.csv` dhe `faza2b_rezultatet.csv`. Çdo shifër e këtij seksioni del nga këto skedarë.

**Horizonti.** Rrugët llogariten muaj pas muaji për 4.2023–12.2026, periudhën për të cilën kemi të dhëna të verifikuara. Sjellja e rregullave të indeksimit pas 2026 testohet me dy skenarë të stilizuar (§7.6), të shënuar (d). Analiza fiskale shumëvjeçare bëhet në 2d.

## 7.1 Alternativat

| | Alternativa | R*_0 | κ = R*_0/P | Ndryshimi ndaj 152.700 | Referenca | Rregulli i indeksimit |
|---|---|---|---|---|---|---|
| **A0** | L95 (skema ekzistuese) | 161.500 → 165.537,5 (1.2026) | 0,380 | +5,76% | Presidenti | ndjek P (indeksim me VKM); tavan min(π; 4%) |
| **A1** | Këshillat | 231.000 → 236.425 (1.2026) | 0,544 | +51,28% | civile (I-2 + 14.000) | vetëm ρ |
| **A2** | Mesi 198.963 (punimi i autorit) | 198.963 | 0,468 | +30,30% | — | asnjë |
| **A3** | Ankora e Presidentit | 252.519 → 258.832 (1.2026) | 0,594 | +65,37% | Presidenti | vetëm ρ (ndjek P) |
| **A4** | Referenca e dyfishtë | 231.000 | 0,544 | +51,28% | civile | max(π, ρ) + ndjekje e referencës |
| **A5** | Vetëm IÇK | 231.000 | 0,544 | +51,28% | — | π |
| A4L, A5L | Ndjeshmëri: A4, A5 me R*_0 = L | 219.888 | 0,517 | +44,00% | si A4, A5 | si A4, A5 |

Shënime (c): A0 = 0,38 × P: 161.500 deri në 12.2025 dhe 165.537,5 nga 1.2026, sepse P u indeksua 2,5% (VKM 92/2026). A3 ndjek gjithashtu P. Për A3 përdoret raporti ekzakt i 2022 (152.700/257.000), që jep κ = 0,5942; me κ = 0,594 të rrumbullakuar, R do të ishte 252.450.

## 7.2 Pse R*_0 = 231.000 për A4 dhe A5 (b)

Vlera nuk zgjidhet brenda korridorit si numër i lirë. Ajo është **rezultati i zbatimit të rregullit që V35 e shpalli kushtetues** mbi strukturën e re të VKM 325:

1. **§109, opsioni i parë, i llogaritur saktë.** §109 lejon referimin te "ndryshimi i kategorisë civile të formulës së vjetër". Sipas V35 (§§72, 76), formula e vjetër referon te I-b, pasardhësja e së cilës në VKM 325 është I-2 (Faza 1 §4.2a). Rritja e saj nga shtatori 2022 në prill 2023 është **+51,28%**. Kjo jep 231.000.
2. **"Afërsisht 44%" e §100 vjen nga gjurma e gabuar.** Ajo riprodhohet saktë nga II-a → I-5, që është referenca e zbatuar gabimisht në 2019–2021 dhe e dënuar nga Gjykata (V15 §§37, 40–41; V35 §84). Nëse riparimi ndërtohet mbi L = 219.888, ai ankorohet te gabimi që synon të riparojë.
3. **§110 përdor të njëjtën formulë** si rregull të paracaktuar për prapambetjet. Me R*_0 = 231.000, formula e ardhshme dhe llogaritja e së kaluarës përputhen; nuk ka dy llogaritje paralele.
4. **Mbyll konfliktin A/B.** A4 jep në çdo muaj të paktën sa A1 (§7.3). Në skenarin A, aktet e Këshillave krijuan të drejta për prapambetje me 231.000 për 4.2023–7.2026. A4L do t'i ulte ato: prapambetja 4.2023–7.2026 do të ishte 10,80 mld në vend të 12,38 mld (N_R qendror). Ky është zgjerimi i logjikës së C6 te prapambetjet (b).

L mbetet ndjeshmëri (A4L), e mbrojtshme vetëm në skenarin B. U (A3) është i mundshëm si nivel, por §108 e kritikon pikërisht referencën e Presidentit si statike.

## 7.3 Testi i realizueshmërisë F8

✓ = plotëson C1–C6; ✗ = shkel, me mungesën maksimale ndaj rrugës minimale në lekë/muaj (skenari B për standardet e C5). Standardi i C5 është testi i matjes, jo rregulli i vetë alternativës.

| | C1–C2 (korridori) | C6 (vetëm A) | C5: max(π, ρ) | C5: π | C5: ρ | C5: min(π; 4%) | Përfundimi |
|---|---|---|---|---|---|---|---|
| A0 | ✗ (−26,6% nën L) | ✗ (ulje −30,0%) | ✗ 4.729 | ✗ 4.729 | ✓ | ✗ 2.423 | **E parealizueshme** |
| A1 | ✓ | ✓ | ✗ 7.114 | ✗ 7.114 | ✓ | ✗ 3.815 | E realizueshme vetëm nëse K9 lexohet si "ndjek referencën" |
| A2 | ✗ (−9,5% nën L) | ✗ | ✗ 10.800 | ✗ 10.800 | ✗ 4.673 | ✗ 7.959 | **E parealizueshme** |
| A3 | ✓ | ✓ | ✗ 7.394 | ✗ 7.394 | ✓ | ✗ 3.788 | E realizueshme vetëm me standardin ρ |
| **A4** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **E realizueshme me çdo standard, në A dhe B** |
| A5 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | E realizueshme deri në 2026 (por shih §7.6) |
| A4L | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | E realizueshme (në A falë C6 nga 8.2026) |
| A5L | ✓ | ✗ (−4.602 nga 8.2026) | ✓ | ✓ | ✓ | ✓ | E realizueshme vetëm në B |

**Lexim (b).** A0 dhe A2 dështojnë në riparimin e bazës (C1), pavarësisht standardit, dhe prandaj nuk renditen kundrejt të tjerave. A1 dhe A3 kalojnë vetëm nëse mbrojtja nga inflacioni kuptohet si "ndjekja e referencës". Në 2023–2025 kjo do të thoshte 0% rritje përballë 5,43% inflacion, dhe 2,5% në 2026. Vetëm A4, A5 dhe A4L kalojnë me standardin më të rreptë në të dy skenarët.

## 7.4 Paga totale (F1), dhjetor 2026, lekë/muaj bruto

| Profili | A0 (L95) | A1 | A2 | A3 | **A4** | A4L (B) |
|---|---|---|---|---|---|---|
| G1, 5 vjet | 331.075 | 472.850 | 397.926 | 517.665 | **487.077** | 463.647 |
| G2, 15 vjet | 377.426 | 539.049 | 453.636 | 590.138 | **555.268** | 528.558 |
| G3, 25 vjet, kryetar | 457.877 | 653.952 | 550.332 | 715.931 | **673.628** | 641.224 |
| G2, 10 vjet, GJKKO/SPAK | 623.083 | 889.904 | 748.897 | 974.245 | **916.679** | 872.584 |
| Ndryshimi ndaj L95 (165.537,5) | — | +42,8% | +20,2% | +56,4% | **+47,1%** | +40,0% |

Meqë W është lineare në R, ndryshimi relativ është i njëjtë për çdo profil, dhe hierarkia e brendshme (K14) nuk prishet nga asnjë alternativë.

## 7.5 Kosto dhe prapambetje (F6–F7), skenari B

N_R qendror 3.954; në kllapa N_R 3.000–4.902. N_R përfshin edhe kategoritë e lidhura dhe ndoshta kontributet (§6.9), prandaj këto janë kosto sistemi, jo vetëm të magjistratëve.

| | R dhjetor 2026 | ΔC/vit kundrejt L95 (mld lekë) | A 4.2023–7.2026 (mld) | A 4.2023–12.2026 (mld) |
|---|---|---|---|---|
| A0 | 165.537,5 | 0 | 1,35 | 1,35 |
| A1 | 236.425 | 3,36 (2,55–4,17) | 12,38 | 13,50 |
| A2 | 198.963 | 1,59 (1,20–1,97) | 7,16 | 7,69 |
| A3 | 258.832 | 4,43 (3,36–5,49) | 15,81 | 17,37 |
| **A4** | **243.539** | **3,70 (2,81–4,59)** | **12,58** | **13,84** |
| A5 | 243.539 | 3,70 | 12,58 | 13,84 |
| A4L | 231.823 (A: 236.425) | 3,15 (2,39–3,90); A: 3,36 | 10,80 | 11,85 (A: 11,92) |

ΔC e A4 është **3,08%** e fondit të pagave të shtetit 2026 (120,3 mld, AN 2/2026). A4 kushton **0,56 mld/vit** më shumë se A4L, dhe prapambetja e saj deri në 12.2026 është **1,99 mld** më e lartë. Ky është çmimi i qartë i zgjedhjes juridike të §7.2. Prapambetja e A0 (1,35 mld) është vetë detyrimi i L95 nga 1.4.2023, afër vlerësimit 1,5 mld të KM.

Kostoja e pensioneve suplementare (D11) nuk kuantifikohet, sepse mungon formula. Ajo ndjek pagën e muajit të fundit (V35 §§97–101), prandaj e rrit koston afatgjatë proporcionalisht me R në të gjitha alternativat; renditja nuk ndryshon.

## 7.6 Mbrojtja pas 2026: dy skenarë të stilizuar (d, hipotetikë)

Për të parë si sillen rregullat kur inflacioni dhe referenca ndahen: S1 = referenca civile e ngrirë, inflacion 3%/vit; S2 = referenca civile +5%/vit, inflacion 2%/vit. Rishikimet bëhen më 1.2028 dhe 1.2030. Ndryshimi matet nga dhjetori 2026 deri në janar 2030.

| | S1: vlera reale | S1: ndaj referencës | S2: vlera reale | S2: ndaj referencës |
|---|---|---|---|---|
| A0 (L95) | **−3,9%** | +8,2% | −0,1% | **−10,1%** |
| A1 (Këshillat) | **−11,2%** | 0 | +11,1% | 0 |
| A3 (Presidenti) | **−11,2%** | 0 | **−7,6%** | **−16,9%** |
| **A4** | **0** | +12,6% | +11,1% | **0** |
| A5 (vetëm IÇK) | 0 | +12,6% | 0 | **−10,0%** |

**Lexim (b).**
- A1 dhe A3 humbasin vlerë reale kur referenca ngrin. Kjo është pikërisht "ulja e fshehtë" përmes inflacionit (K9; V15 §§83–85).
- A5 dhe A0 mbeten pas referencës kur pagat civile rriten realisht. Kjo është pikërisht ulja e fshehtë që Gjykata konstatoi në 2023 (K4–K5; §§93–96).
- **Vetëm A4 nuk humbet në asnjërin tregues, në asnjërin skenar.** Kjo është veti e rregullit max(π, ρ), jo e nivelit të bazës. Prandaj A4L ka të njëjtat rezultate.

Rreziku i A4 në S1 është rritja 12,6% ndaj pagave civile kur ato janë të ngrira. Kjo ngre pyetjen e barazisë me kategoritë e tjera (K10, §84; pakica, pika i). Përgjigja nuk është të hiqet mbrojtja, por mekanizmi i nenit 138/a: një ngrirje e përgjithshme, e justifikuar dhe e kufizuar në kohë mund ta pezullojë indeksimin edhe për magjistratët. Ky mekanizëm hartohet në 2c.

## 7.7 Krahasimi i alternativave të realizueshme: pse nuk ka "frontierë Pareto" me kuptim

Bashkësia e realizueshme në të dy skenarët, me standardin më të rreptë, është {A4, A4L, A5}. Me tre kritere numerike, ku sa më pak aq më mirë (ΔC/vit, humbja maksimale reale dhe humbja maksimale ndaj referencës në §7.6):
- A5 dominohet nga A4 dhe A4L, sepse ka të njëjtën kosto dhe humbje −10,0% ndaj referencës.
- A4 dominohet nga A4L **vetëm nga kostoja**, sepse rregulli është i njëjtë.
- A4L është e vetmja e padominuar.

Ky rezultat **nuk është zgjedhje**. Ndryshimi i vetëm midis A4 dhe A4L është niveli i riparimit të bazës. "Riparimi i mjaftueshëm" është kriter juridik (K6, §§109–110) pa shkallë numerike të pavarur nga kostoja, prandaj nuk mund të hyjë si dimension i tretë pa peshë arbitrare. Prandaj kjo është **krahasim përshkrues me test dominimi**, jo frontierë Pareto. Zgjedhja midis A4 dhe A4L bëhet me argumentin e §7.2.

## 7.8 Vlerësimi cilësor (b)

| | Administrimi | Gjyqësori | Ekzekutivi | Kuvendi | Dobësitë juridike / rreziku i kontestimit |
|---|---|---|---|---|---|
| A0 | Shumë i thjeshtë | Humbje e madhe; ulje nominale −30,0% në A | Kosto minimale | Ruan ligjin e miratuar | **I lartë:** C1, K3 (konsultimi), K12 pa skemë, ulje e hapur në A |
| A1 | I thjeshtë (ndjek VKM-në) | Përputhet me aktet e Këshillave | Kosto e njohur; ruan kontrollin mbi rrjetën civile | E kthen çështjen nga Këshillat në ligj | **I mesëm:** pa mbrojtje nga inflacioni kur rrjeta civile ngrin (K9); varësia nga VKM (pakica iii) |
| A2 | I thjeshtë | Nën korridor | Kosto e mesme | "Kompromis" i dukshëm | **I lartë:** C1; pika e mosmarrëveshjes e papranueshme (korrigjimi 6) |
| A3 | Shumë i thjeshtë | Nivel më i lartë | Kosto më e lartë | Ruan strukturën e L95 me κ tjetër | **I mesëm–lartë:** §108 kritikon pikërisht këtë referencë; erozion real kur P nuk lëviz |
| **A4** | I thjeshtë: dy seri publike (VKM, IÇK e INSTAT), rishikim çdo 2 vjet | ≥ Këshillat në çdo muaj; mbrojtje e plotë | Formulë automatike me ligj; kosto e parashikueshme; VKM-ja nuk mund ta ulë R | Rikthen kompetencën ligjore; mbyll konfliktin me KLGJ 435/KLP 144 dhe kontestimet | **I ulët–mesëm:** kosto më e lartë se A1 (+3,01% në 2026); identifikimi I-2 mund të kontestohet nga leximi titullor I-4 (Faza 1 §4.2a); barazia në ngrirje të përgjithshme → 138/a |
| A5 | I thjeshtë | Mbrojtje reale, por jo relative | Shkëputet nga rrjeta civile | — | **I mesëm:** ulje e fshehtë ndaj referencës në S2 (K4–K5) |

**Përgjigje ndaj mendimit të pakicës (G. Ibrahimi):**
1. *Neni 138 nuk garanton diferencë me pagat e tjera.* A4 nuk mbështetet te diferenca, por te riparimi i uljes së fshehtë (§109) dhe te ruajtja e vlerës reale (§§83–85).
2. *Mungon analiza financiare e pagës totale.* §7.4 dhe §7.5 e japin për katër profile dhe për sistemin.
3. *Referenca te VKM-të mund të cenojë kriterin "me ligj".* Në A4, formula, referenca, burimi statistikor dhe datat janë në ligj. VKM-ja mund ta rrisë R vetëm përmes ρ dhe nuk mund ta ulë, sepse max(π, ρ) dhe C3 mbrojnë nga poshtë. Diskrecioni i ekzekutivit është asimetrik.
4. *Indeksimi dyvjeçar mjafton kundër inflacionit.* A4 e ruan frekuencën dyvjeçare. Ndryshimi është vetëm se rishikimi nuk kufizohet nga tavani 4%, i cili sipas §6.9 është zgjedhje ligjore, jo e BSH.

## 7.9 Paketa kryesore: A4

**Rekomandimi (e).** **Baza R*_0 = 231.000 lekë nga 1.4.2023, d.m.th. standardi i V35 i zbatuar mbi VKM 325; ndjekje e vazhdueshme e referencës civile (I-2 + 14.000); rishikim çdo 2 vjet me g = max(π, ρ); asnjë ulje nominale përveç mekanizmit të nenit 138/a.** Me të dhënat e verifikuara, kjo jep R = 243.539 nga 1.1.2026, rreth 3,01% mbi nivelin e Këshillave.

**Pse preferohet:**
- është e vetmja alternativë e realizueshme me çdo standard të C5 dhe në të dy skenarët juridikë;
- është e vetmja që nuk humbet as vlerë reale, as raport me referencën, në asnjërin skenar të stilizuar;
- baza e saj nuk është numër i zgjedhur, por rezultat i rregullit të V35;
- u përgjigjet katër pikave të pakicës.

**Zgjidhja nuk është unike.** Dy variante mbeten të mbrojtshme dhe varen nga vendimet e hapura:
- **A4θ**, nëse P3 vendoset në favor të tavanit (V15 §106): rishikimi i parë me min(π; 4%) jep 240.240 nga 1.2026. Kjo ka erozion real 1,35% në rishikimin e parë.
- **A4L**, vetëm nëse pranohet skenari B dhe leximi i 44% si kufi: kushton 0,56 mld/vit më pak, por ankorohet te gjurma e gabuar dhe ul prapambetjet e njohura nga Këshillat.

**Kalon në 2c:** rregullat e rishikimit (burimi, data, rrumbullakosja, rishikimet statistikore), korrigjimi periodik (K11), mekanizmi 138/a, rregullat kalimtare, kategoritë e lidhura dhe kalendari i prapambetjeve (12,58 mld deri në 7.2026; 13,84 mld deri në 12.2026, N_R qendror).

## 7.10 Kontrolli i konsistencës për nënhapin 2b (§12)

| # | Kontrolli | Rezultati |
|---|---|---|
| 1 | Asnjë rregull indeksimi në kundërshtim me mosregresionin | ✓ A4 përfshin C3. Tavani (A0, A4θ) nuk prodhon ulje nominale, por erozion real, i raportuar. |
| 2 | Asnjë dysheme rrethore | ✓ R*_0 e A4 vjen nga V35, jo nga pozicioni i palëve. A2 përjashtohet pikërisht për rrethshmëri (pika e mosmarrëveshjes = L95, e parealizueshme). |
| 3 | Pa numërim të dyfishtë | ✓ g = max(π, ρ), jo shuma. Inflacioni matet nga 3.2023. Korridori nuk indeksohet me IÇK. |
| 4 | Shifrat = skedarët | ✓ `faza2b_*.csv` |
| 5 | Argumentet e Gjykatës nga shumica | ✓ §§83–85, 92–96, 100, 106, 108–110; pakica shënohet veçmas (§7.8). |
| 6 | Simbolet | ✓ fjalori §6.1; shtohen vetëm A0–A5, S1–S2 si emërtime. |

**Fundi i nënhapit 2b.** Nënhapi 2c (§8: përbërja e paketës) nis vetëm pas miratimit tuaj.


---

# §8 Përbërja e paketës së rekomanduar (nënhapi 2c)

Kodi: `faza2c_paketa.py` (formula, testet kumulative, 138/a, K11) dhe `faza2c_lp.py` (kalendari i prapambetjeve). Rezultatet: `faza2c_paketa_rruga.csv`, `faza2c_testet_kumulative.csv`, `faza2c_rezultatet.csv`, `faza2c_lp_skenaret.csv`, `faza2c_lp_kalendari.csv` dhe `faza2c_lp_rezultatet.csv`. Paketa është A4 e §7.9. Elementet ndërtohen veçmas, por përdorin të njëjtat simbole dhe seri.

## 8.1 Baza e riparuar (e)

**R*_0 = 231.000 lekë/muaj bruto nga 1.4.2023** = paga për pozicion e klasës I-2 të VKM 325/2023 (217.000) + paga në grup (14.000). Kjo është rritje 51,28% ndaj të drejtës së fituar 152.700. Arsyetimi është në §7.2: standardi i V35 i zbatuar mbi strukturën e re dhe i njëjti rregull që V15 §110 përcakton për prapambetjet.

Në ligj, baza shkruhet si **shumë e caktuar në lekë**, jo si referencë dinamike te një VKM. Kështu baza nuk varet nga riklasifikimet e ardhshme (K2; pakica, pika iii).

## 8.2 Formula afatgjatë (e)

**R_t = max{ R_{t−1} ;  R*_0 · max( I(τ−1) / I(3.2023) ;  Ref_t / Ref_{4.2023} ) }**

ku τ është data e fundit e rishikimit para ose në muajin t, I është IÇK kombëtar i INSTAT dhe Ref = I-2 + 14.000.

*Me fjalë të thjeshta:* R është baza e vitit 2023 e shumëzuar me më të madhin nga dy "shumëzues": sa u shtrenjtua jetesa që nga 2023 (i matur vetëm në datat e rishikimit), ose sa u rrit paga e referencës civile që nga 2023 (kalon menjëherë). R nuk zbret kurrë nën muajin e kaluar.

**Pse "maksimumi i niveleve" dhe jo "maksimumi i normave".** Në 2a dhe 2b rregulli u shkrua si g = max(π, ρ) në çdo rishikim. Nëse ky rregull zbatohet rishikim pas rishikimi, ai krijon efekt "çikriku": merr herë rritjen e njërës seri, herë të tjetrës, dhe R del mbi të dyja. Testi (§8.3) e tregon këtë. Formula e mësipërme krahason **nivelet kumulative që nga baza**, prandaj R nuk mund të dalë kurrë mbi seritë e veta. Deri në 2026, ku ka vetëm një rishikim, dy shkrimet japin të njëjtin rezultat (devijimi 0 lekë ndaj A4).

*Shembull i riprodhueshëm (1.1.2026):* faktori IÇK = I(12.2025)/I(3.2023) = 1,05428; faktori i referencës = 222.425+14.000 / 217.000+14.000 = 1,02349. R = 231.000 × 1,05428 = 243.538,62, pra **243.539 lekë** për pagesë. Kufizimi që vendos është IÇK.

**Referenca.** Ref = paga për pozicion e klasës që i korrespondon funksionalisht nivelit I-b të VKM 187/2017 (sot I-2), + paga në grup e diplomës 1. Ligji e përcakton referencën me **kriter funksional**, jo me emrin e klasës (V35 §§72, 76, 84).

## 8.3 Indeksimi (e)

| Elementi | Rregulli i propozuar | Arsyeja |
|---|---|---|
| Rregulli | Formula e §8.2; IÇK vepron vetëm në rishikime, referenca vepron menjëherë | K5 (§92) dhe K9 (§§83–85), pa numërim të dyfishtë |
| Datat τ_k | 1 janari i çdo viti çift: 2026 (i kryer), 2028, 2030… | Ruan frekuencën ≤ 2 vjet të ligjit 33/2023 dhe të L95, që Gjykata e vlerësoi (§106) |
| Burimi | IÇK kombëtar total i INSTAT (jo inflacioni bazë, jo IÇHK) | §84 i referohet IÇK-së; inflacioni bazë është tregues i politikës monetare (§6.9) |
| Muaji i matjes | Dhjetori para rishikimit, kundrejt marsit 2023 | I fundit i publikuar para datës; baza 3.2023 shmang numërimin e inflacionit 2022–23 |
| Vintazhi | Të dyja vlerat merren nga **i njëjti botim i fundit** i INSTAT | Rishikimet statistikore përthithen automatikisht në rishikimin pasardhës; ndryshimi i bazës së indeksit nuk e prek raportin |
| Rrumbullakimi | R llogaritet me saktësi të plotë; paguhet e rrumbullakuar në lekë të plota; indeksimi pasardhës zbatohet mbi R të parrumbullakuar | Shmang zhvendosjen kumulative |
| Përgjegjësia | Ministria e Financave publikon R të re brenda 15 janarit me akt deklarativ, pa diskrecion. Nëse nuk e publikon, KLGJ dhe KLP e zbatojnë drejtpërdrejt formulën | K18: automatizëm; asnjë hapësirë presioni |
| Ndryshimi i referencës | Riklasifikimi me VKM ndiqet te klasa pasardhëse funksionalisht ekuivalente. Nëse referenca ulet ose shfuqizohet, R nuk ulet (C3), dhe vazhdon vetëm komponenti IÇK | V35 §84: akti nënligjor ndjek ligjin; C3 |

**Testet e efekteve kumulative (d, rrugë të stilizuara; `faza2c_testet_kumulative.csv`).** Shifrat janë ndryshime kumulative të R.

| Rasti | Paketa (maks. i niveleve) | Teprica e "max" periodik mbi paketën | Humbja reale e tavanit 4% | Humbja reale e mesatares (π+ρ)/2 | Humbja ndaj referencës e "min" |
|---|---|---|---|---|---|
| R1: ρ 6%, pastaj π 6% | +8,12% | **+3,92%** | −1,89% | −0,92% | −3,77% |
| R3: alternim në 4 rishikime | +16,90% | **+8,00%** | −3,74% | −1,84% | −7,40% |
| R4: të dyja 3% çdo herë | +12,55% | 0 | 0 | 0 | 0 |
| R5: si 2022–23 (π 12%, ρ 0) | +12,00% | 0 | **−7,14%** | −5,36% | 0 |

Përfundimet (b):
- "max" periodik e kalon të dyja seritë kur ato alternojnë, deri në +8,00% në katër rishikime. Kjo është numërim i dyfishtë i fshehtë, prandaj paketa përdor maksimumin e niveleve.
- Mesatarja dhe minimumi humbasin gjithmonë kundrejt njërës nga seritë.
- Tavani 4% humbet 7,14% vlerë reale në një episod si 2022–23, i cili zgjati 18 muaj mbi 4% (Faza 1 §4.2). Prandaj tavani nuk hyn në rregullin e zakonshëm, por vetëm në §8.8.
- *Rrumbullakimi:* në 10 rishikime me 3%, rrumbullakimi lart në 100 lekë mbi bazë të rrumbullakuar zhvendoset 504 lekë; rregulli i paketës zhvendoset më pak se 1 lek.
- *Rishikimi statistikor:* nëse IÇK e dhjetorit 2025 rishikohet +0,2 pikë, metoda periodike me vintazhe të përziera humbet 0,20% në 2028. Rregulli i niveleve me një vintazh nuk humbet asgjë.

## 8.4 Korrigjimi periodik (K11)

Neni 94 dhe 102 i V15 kërkojnë që paga të ecë "në linjë me zhvillimet ekonomike". Pakica e konteston këtë si detyrim pozitiv (§§9–11). Indeksimi (§8.3) mbron vetëm vlerën reale dhe lidhjen me referencën.

**Rregulli i propozuar (e):** çdo 5 vjet (i pari në 2031) INSTAT dhe MF publikojnë raport që krahason R me pagën mesatare bruto dhe me pagën mesatare në sektorin shtetëror që nga 2023. Kuvendi, pas konsultimit me KLGJ dhe KLP (K3), vendos me ligj nëse jep rritje reale shtesë. Korrigjimi:
- **nuk është automatik**, sepse një prag numerik do të ishte arbitrar (§6 i detyrës);
- **matet mbi rrugën e indeksuar**, jo mbi bazën, që të mos numërohet dy herë inflacioni ose rritja e referencës;
- **nuk mund të jetë negativ** (C3).

*Të dhënat që do t'i paraqiteshin rishikimit sot (c):* paga mesatare bruto u rrit **29,21%** nga mesatarja e 2023 (70.530,5) në I–II/2026 (91.134,5). Në të njëjtën periudhë, R e paketës u rrit 5,43%, dhe I-2 vetëm 2,50%. Rrjeta civile e referencës ka mbetur ndjeshëm pas zhvillimit të pagave. Kjo është pyetje për K11, jo për indeksimin.

## 8.5 Paga totale dhe diferencat ndërmjet kategorive

- **W = ω · R** (F1), me koeficientët e L96 të pandryshuar. Raportet e hierarkisë mbeten konstante për çdo R; p.sh. G2 me 15 vjet / G1 pa vjetërsi = 1,20; G3 me 25 vjet / G1 pa vjetërsi = 1,35 (K14).
- **Kategoritë me status magjistrati** (anëtarët e KLGJ dhe KLP, gjyqtarët e GJK, inspektorët magjistratë të ILD si të komanduar sipas nenit 13 të L96) ndjekin R e re (L115 nenet 4, 102, 210; L8577 neni 17; §6.9).
- **Kategoritë e lidhura pa status magjistrati** (p.sh. ILD si drejtues, Drejtori i Shkollës, këshilltarët juristë të GJK, si edhe institucionet e VKM 755: KPK, KPA, Komisionerët, KQZ, Avokati i Popullit): rekomandohet (e) shkëputja e ruajtur nga neni 12/1, par. 2. Por **ngrirja nominale në 153.000 zëvendësohet me rregullin e indeksimit të kategorisë së tyre**, që të mos krijohet një erozion i ri pa afat. Kjo e ul koston e paketës nën vlerat me N_R të §7.5. Masa nuk llogaritet dot pa numrat e D8 dhe D10.

## 8.6 Prapambetjet

**(i) Ekzistenca dhe masa e së drejtës (e).** E drejta lind me ligj, me efekt nga 1.4.2023 (§110). Masa e saj për çdo magjistrat është **ω · Σ (R_paketës,m − R_paguar,m)** për çdo muaj deri në hyrjen në fuqi. Për sistemin, me N_R qendror dhe hyrje në fuqi më 1.1.2027 (d), kjo jep **13,84 mld lekë** (10,50–17,16 me N_R 3.000–4.902) për 45 muaj detyrimi. Kalendari më poshtë ndryshon vetëm **kohën** e pagesës, jo masën.

**(ii) Kalendari me programim linear.** Variablat janë shumat e çdo muaji detyrimi që paguhen në 2027, 2028 dhe 2029. Kufizimet:
- çdo detyrim shlyhet plotësisht ose shfaqet si "hendek";
- pagesa vjetore nuk e kalon tavanin buxhetor;
- çdo vit ka të paktën 10% të totalit;
- muaji më i vjetër nuk mund të jetë i paguar më pak (në përqindje) se muaji pasardhës.

*Objektivi me fjalë të thjeshta:* çdo lek i papaguar "kushton" sa katrori i muajve që pret. Kështu modeli preferon të paguajë fillimisht detyrimet më të vjetra dhe shmang pritjet shumë të gjata.

| Skenari i tavanit vjetor | 2027 | 2028 | 2029 | Hendeku | Vonesa mesatare (muaj) | Kompensimi IÇK |
|---|---|---|---|---|---|---|
| **Bazë: 5 mld/vit** | 5,00 | 5,00 | 3,84 | 0 | 40,11 | 1,32 mld (9,57%) |
| 4 mld/vit | 4,00 | 4,00 | 4,00 | **1,84** | 41,12 | 1,18 mld |
| 7 mld/vit | 7,00 | 5,46 | 1,38 | 0 | 36,25 | 1,18 mld |
| Pa tavan | 11,07 | 1,38 | 1,38 | 0 | 32,72 | 1,05 mld |
| Si Këshillat: 2027–2028, 7 mld/vit | 7,00 | 6,84 | — | 0 | 35,05 | 1,14 mld |
| Si Këshillat: 2027–2028, 5 mld/vit | 5,00 | 5,00 | — | **3,84** | 35,12 | 0,82 mld |

Shifrat janë në mld lekë. Në skenarin bazë, 2027 shlyen plotësisht muajt 4.2023–7.2024. Edhe nëse gjithçka paguhet në mes të 2027, vonesa mesatare është 29,12 muaj, sepse detyrimi nis në 2023. Pjesa mbi këtë minimum është vonesa që i shton kalendari.

Kufizimi "asnjë vit pa pagesë" lidh vetëm kur nuk ka tavan: ai detyron 1,38 mld në 2028 dhe 2029 dhe e rrit vonesën nga minimumi 29,12 në 32,72 muaj. Me tavan 5 mld nuk ka efekt (p_min 0%, 10% dhe 20% japin të njëjtin rezultat). Me N_R të lartë (17,16 mld), tavani 5 mld lë hendek 2,16 mld. Sipas korrigjimit 3, hendeku raportohet dhe mbulohet; detyrimi nuk ulet.

**(iii) Vonesa dhe kompensimi (b/e).** §110 lejon "skemë të arsyeshme përshtatjeje", pra shtyrja e pagesës është e ligjshme nëse arsyetohet me planifikimin buxhetor. Por K9 vlen edhe për prapambetjen: një lek i 2023 i paguar në 2029 ka humbur vlerë. Rekomandohet (e) që çdo pagesë e shtyrë të **indeksohet me IÇK nga muaji i detyrimit deri në pagesë**. Kjo nuk është interes komercial; është ruajtje e vlerës reale. Në skenarin bazë, kjo kushton 1,32 mld (9,57% e detyrimit), me IÇK reale deri në 8.2026 dhe 3%/vit më pas (d). Në punim nuk ka burim për normën e interesit ligjor, prandaj ajo nuk propozohet.

**(iv) Gushti 2026, i paguar me vendim gjyqësor.** Në të dy skenarët, shuma e paguar (≈ 236.425) është **paradhënie** e llogaritur ndaj detyrimit të paketës (243.539). Diferenca hyn në prapambetje.
- Në A, pagesa ishte e ligjshme sipas akteve të Këshillave.
- Në B, ajo ishte masë e përkohshme gjyqësore.

Në asnjërin rast pagesa nuk kthehet: paketa është gjithmonë më e lartë, dhe kthimi do të ishte ulje (C3).

## 8.7 Rregullat kalimtare (e)

1. Paketa zëvendëson nenin e L95 për R, **me efekt nga 1.4.2023**. Periudha 31.7–18.9.2026 mbulohet nga ligji i ri, dhe vakumi mbyllet pa marrë anë në kontestin e kompetencës (A/B).
2. Shumat e paguara sipas KLGJ 435, KLP 144 ose vendimeve gjyqësore njihen si paradhënie dhe nuk kthehen. Meqë paketa ≥ A1 në çdo muaj, asnjë akt i Këshillave nuk "ulet" nga ligji.
3. Kontestimet gjyqësore në proces për diferenca page për periudhën nga 1.4.2023 zgjidhen nga kalendari i §8.6. Kalendari lind të drejtë ekzekutimi për çdo këst të papaguar në afat.
4. Rishikimi i parë pas hyrjes në fuqi bëhet më 1.1.2028.
5. Diferencat sipas V35 për 2019–2023 (P6; VKM 755/2023 pagoi 1 mld si pjesë) mbeten jashtë kësaj pakete. Rekomandohet një inventar i tyre (D17).

## 8.8 Mekanizmi i jashtëzakonshëm i nenit 138/a (e)

Ky është i vetmi vend ku lejohet kufizimi i indeksimit. Kushtet janë kumulative (K17; V15 §§78–81):

| Kushti | Testi i kontrollueshëm në ligj |
|---|---|
| 1. Masë e përgjithshme, jo e shënjestruar | E njëjta masë, ose më e rreptë, zbatohet njëkohësisht për të gjitha pagat buxhetore, përfshirë funksionarët politikë |
| 2. E justifikuar | Ligj i veçantë me të dhëna fiskale të publikuara (deficit, borxh, të ardhura) dhe me vlerësim të alternativave |
| 3. Objektive | Kriteret dhe të dhënat janë publike dhe të njëjta për të gjitha kategoritë |
| 4. Proporcionale | Pezullohet vetëm komponenti i indeksimit në **një** rishikim. R nominale nuk ulet kurrë. Masa për magjistratët nuk e kalon masën për kategoritë e tjera |
| 5. E kufizuar në kohë | Maksimumi 2 vjet; në rishikimin pasardhës, formula e niveleve e rikthen R në nivelin e plotë |
| 6. Pa cenuar dinjitetin dhe pavarësinë | Konsultim paraprak me KLGJ dhe KLP (K3); nuk zbatohet në mënyrë selektive për gjykata ose prokurori të veçanta |

*Testi (d): pezullim i rishikimit të 2028, me inflacion 4%/vit dhe referencë të ngrirë.* Gjatë 2028–2029, R mbetet 7,54% nën vlerën reale. Nga 2030, rregulli i niveleve e rikthen plotësisht (humbja 0). Kursimi buxhetor është **1,89 mld** për dy vitet (N_R qendror). Pa rikuperim, humbja 7,54% do të bëhej e përhershme, pra ulje e pakufizuar në kohë, në kundërshtim me kushtin 5 (b). Prandaj paketa nuk e lejon rivendosjen e bazës.

## 8.9 Kontrolli i konsistencës për nënhapin 2c (§12)

| # | Kontrolli | Rezultati |
|---|---|---|
| 1 | Asnjë rregull indeksimi në kundërshtim me mosregresionin | ✓ C3 është në formulë. Tavani lejohet vetëm në 138/a, pa ulje nominale dhe me rikuperim. |
| 2 | Asnjë dysheme rrethore | ✓ Baza vjen nga V35 dhe VKM 325; kalendari nuk e prek masën e detyrimit. |
| 3 | Pa numërim të dyfishtë | ✓ Maksimumi i niveleve, jo i normave (teprica e "max" periodik deri në +8,00% eliminohet); K11 matet mbi rrugën e indeksuar; vintazh i vetëm i IÇK. |
| 4 | Shifrat = skedarët | ✓ `faza2c_*.csv` |
| 5 | Argumentet e Gjykatës | ✓ §§78–85, 92, 94, 102, 106, 110 nga shumica; pakica §§9–11 shënohet veçmas. |
| 6 | Simbolet | ✓ fjalori §6.1; shtohen x, h, B_y, p_min vetëm në §8.6. |

**Fundi i nënhapit 2c.** Nënhapi 2d (§9: analiza fiskale dhe testimi) nis vetëm pas miratimit tuaj.


---

# §9 Analiza fiskale dhe testimi (nënhapi 2d)

Kodi: `faza2d_testet.py` (importon 2a–2c dhe rillogarit të gjithë skriptet e Fazës 2). Rezultatet: `faza2d_fiskale_grid.csv` (72 kombinime × 5 vjet), `faza2d_historik.csv`, `faza2d_stresi.csv`, `faza2d_K.csv`, `faza2d_konstantet.csv`, `faza2d_konsistenca.csv` dhe `faza2d_rezultatet.csv`.

## 9.1 Analiza fiskale 2027–2031

**Pse ky horizont.** Pesë vite mbulojnë dy rishikime të rregullta (2028, 2030), gjithë kalendarin e prapambetjeve (2027–2029) dhe dy vite "të pastra" pas tij. Pas 2031, rregulli i niveleve nuk ndryshon strukturë.

**Ndarja e kostos:**
- **e përhershme** = 12 · N_R · (R_paketës − R_L95) · (1 + c);
- **kalimtare** = pagesat e prapambetjeve sipas LP të 2c (tavan 5 mld/vit) + kompensimi IÇK për vonesën, · (1 + c);
- **detyrimet historike** = stoku i prapambetjeve 4.2023–12.2026 (13,84 mld, N_R qendror). Diferencat 2019–2023 sipas V35 (P6) janë jashtë.

**Krahasuesi.** L95 = 0,38 × P. P u indeksua 2,5% në 2026 me VKM 92/2026, njësoj si pagat civile. Supozohet (d) se P vazhdon të ndjekë ρ çdo vit, brenda tavanit 4% të L95. Nëse P ngrin (ρ 0%), kostoja e përhershme e paketës kundrejt L95 rritet.

**Skenari qendror** (π 3%, ρ 2,5%, N_R 3.954, c = 0), mld lekë:

| Viti | R paketa | R L95 | E përhershme | Kalimtare | **Totali** | % e fondit të pagave 2026 |
|---|---|---|---|---|---|---|
| 2027 | 243.539 | 169.676 | 3,50 | 5,48 | **8,99** | 7,5% |
| 2028 | 258.596 | 173.918 | 4,02 | 5,49 | **9,50** | 7,9% |
| 2029 | 258.596 | 178.266 | 3,81 | 4,20 | **8,01** | 6,7% |
| 2030 | 274.344 | 182.722 | 4,35 | 0 | **4,35** | 3,6% |
| 2031 | 274.344 | 187.290 | 4,13 | 0 | **4,13** | 3,4% |
| **2027–2031** | | | **19,81** | **15,16** | **34,98** | |

**Gama mbi 72 kombinimet** (π 2–5%, ρ 0–5%, N_R 3.000–4.902, c 0–16,6%), totali vjetor në mld:

| Viti | Min | Maks | % maks e fondit 2026 |
|---|---|---|---|
| 2027 | 8,07 | 11,86 | 9,9% |
| 2028 | 7,61 | 13,51 | 11,2% |
| 2029 | 3,88 | 13,60 | 11,3% |
| 2030 | 2,98 | 8,71 | 7,2% |
| 2031 | 2,82 | 8,71 | 7,2% |

Kulmi (13,60 mld) bie në 2029 me π 5%, ρ 0%, N_R e lartë dhe c = 16,6%. Ai është 21,4% e deficitit të 2026 (63,7 mld). Kostoja e përhershme varet nga ρ në dy drejtime, sepse ρ lëviz edhe L95 (përmes P). Në 2031 (π 3%) ajo është 5,16 mld me ρ 0% (L95 ngrin, paketa ndjek IÇK), 4,13 mld me ρ 2,5% dhe 4,58 mld me ρ 5% (paketa ndjek referencën, L95 kufizohet nga tavani 4%).

**Hendeku dhe financimi (e).** Me tavan 5 mld/vit, prapambetja shlyhet brenda 2029 në të gjitha kombinimet, përveç atyre me N_R të lartë: hendeku është 2,16 mld pa kontribute (§8.6) dhe 2,52 mld me kontribute. Sipas korrigjimit 3, kjo nuk e ul detyrimin. Mënyrat e ligjshme të mbulimit janë:
1. shtyrja e kalendarit me ligj, me kompensim IÇK (§9.5: tavan 3 mld/vit deri 2031 nuk lë hendek);
2. fondi i kontingjencës, me precedent VKM 755/2023 (1 mld);
3. rialokim brenda buxhetit;
4. vetëm si masë e përgjithshme dhe me kushtet e §8.8, pezullimi i një rishikimi sipas nenit 138/a. Asnjë masë e shënjestruar ndaj magjistratëve nuk lejohet.

## 9.2 Testi historik 2019–2026

**Çfarë teston dhe çfarë jo.** Testi pyet: *nëse paketa do të ishte zbatuar nga 1.1.2019, a do ta kishte parandaluar erozionin që Gjykata konstatoi?* Ai **nuk** pretendon që formula duhej zbatuar juridikisht atëherë (P4, P6). Kundërfaktikja nis nga R = 143.800, standardi i V35 më 1.1.2019 (V35 §§77, 80). Ajo ndjek I-b + 14.000 (VKM 187 → VKM 621/2022), pastaj I-2 + 14.000 (VKM 325 → VKM 131/2026), me rishikime IÇK më 1.2021, 1.2023 dhe 1.2025. Krahasohet me R e paguar faktikisht: 118.100 deri në 3.2023 (zbatimi i gabuar), pastaj 153.000, dhe me 143.800 të indeksuar plotësisht me IÇK.

| Muaji | Kundërfaktikja | E paguar | 143.800 e indeksuar me IÇK |
|---|---|---|---|
| 1.2019 | 143.800 | 118.100 | 146.085 |
| 1.2021 | 146.964 | 118.100 | 148.722 |
| 12.2022 | 152.700 | 118.100 | 163.665 |
| 1.2023 | 163.665 | 118.100 | 165.423 |
| **4.2023** | **231.000** | **153.000** | 168.411 |
| 1.2026 | 236.425 | 156.825 | 178.432 |
| 8.2026 | 236.425 | 236.425 | 181.244 |

**Përfundime (b):**
1. **Ulja e fshehtë e 2023 do të ishte parandaluar automatikisht.** Komponenti i referencës e çon R nga 152.700 në **231.000 në prill 2023**, pa asnjë ndërhyrje ligjore. Kjo është saktësisht R*_0 e paketës. Pra, baza e propozuar është ajo që rregulli vetë do të kishte prodhuar.
2. **Inflacioni i 2022 do të ishte kompensuar vetëm me vonesë.** Para rishikimit të 1.2023, kundërfaktikja ishte deri në **9,13%** nën vlerën reale. Gjithsej ajo ishte nën vlerën reale për 51 muaj, kryesisht brenda cikleve dyvjeçare. Rishikimi i 1.2023 e rikthen R në 163.665 (+7,18% mbi 152.700). Kjo është dobësia e rishikimit dyvjeçar në inflacion të lartë, prandaj §9.5 propozon rishikimin e jashtëzakonshëm.
3. Mungesa maksimale e R të paguar ndaj kundërfaktikes është 79.600 lekë/muaj, në 1–7.2026.
4. Kundërfaktikja e 8.2026 është 2,92% nën paketën. Paketa mat inflacionin nga baza e 2023; kundërfaktikja nga 2019, ku rritja e referencës në 2023 e kishte përthithur tashmë inflacionin e mëparshëm. Prandaj paketa nuk e numëron dy herë inflacionin 2019–2023.

## 9.3 Testet K1–K18

✓ = plotëson; ✗ = nuk plotëson; ~ = pjesërisht. Testet numerike janë në `faza2d_K.csv`.

| K | Kërkesa (burimi) | L95 | Paketa | Mënyra e verifikimit / garancia procedurale |
|---|---|---|---|---|
| K1 | Ligj brenda 31.7.2026 (disp. 3) (a) | ✗ 49 ditë vonesë | ~ | Edhe paketa vjen pas afatit; vonesa riparohet me efekt nga 1.4.2023, me kompensim IÇK dhe me rregullat kalimtare të §8.7 (b) |
| K2 | Rregullat me ligj (§§71, 76–77) (a) | ~ indeksimi "deri në" | ✓ | **Garanci:** baza në lekë, formula, referenca funksionale, burimi statistikor, datat dhe rrumbullakimi të gjitha në ligj (§8.3) |
| K3 | Konsultim efektiv (§§76, 98) (a) | ✗ dëgjesë në ditën e votimit | ✓ si procedurë | **Garanci:** detyrim ligjor për konsultim me KLGJ, KLP dhe shoqatat para çdo ndryshimi të formulës, para korrigjimit K11 dhe para masës 138/a; afat minimal i caktuar me ligj; përgjigje e arsyetuar me shkrim për çdo vërejtje; publikimi i vlerësimit të ndikimit |
| K4 | Pa ulje të fshehtë (§§80–82, 94–95, 104–108) (a) | ✗ +5,8% kundrejt 44–65% | ✓ | R/Ref nuk bie kurrë (komponenti i referencës; §9.2, pika 1) |
| K5 | Ndjek fatin e referencës (§92) (a) | ~ ndjek nivelin e P me κ të ulët | ✓ | 243.539/231.000 ≥ 236.425/231.000 |
| K6 | Riparim i uljes (§109) (a) | ✗ | ✓ | R*_0 = 231.000 |
| K7 | Brenda limiteve (§109) (a/b) | ✗ (161.500 < 219.888) | ✓ | 219.888 ≤ 231.000 ≤ 252.519 |
| K8 | Referencë që indeksohet (§108) (a) | ✗ Presidenti | ✓ | Rrjeta civile + IÇK |
| K9 | Mbrojtje nga inflacioni (§§83–85) (a) | ✗ −2,6% nën vlerën reale të 152.700 (2026) | ✓ | Rregulli i niveleve; vonesa brenda ciklit ≤ 5,82% (π 3%), 3,95% me rishikim të jashtëzakonshëm (§9.5) |
| K10 | Si kategoritë e tjera (§84) (a) | ~ | ~ | Në ngrirje civile, paketa del mbi rrjetën civile (§9.5); zgjidhja është masë e përgjithshme sipas §8.8, jo heqja e mbrojtjes (b) |
| K11 | Në linjë me zhvillimet ekonomike (§§94, 102) (a) | ✗ | ~ | Rishikim pesëvjeçar me raport të INSTAT/MF dhe vendim të Kuvendit (§8.4). Nuk mbyll automatikisht hendekun +29,2% kundrejt +5,4% (b) |
| K12 | Efekte nga 1.4.2023 + skemë (§110) (a) | ~ efekti po, skema jo | ✓ | Kalendari LP, kompensimi IÇK, e drejta e ekzekutimit të kësteve (§8.6) |
| K13 | Rregulli i paracaktuar (§110) (a) | ✗ | ✓ | R*_0 = formula e §110; ≥ 236.425 nga 8.2026 (skenari A) |
| K14 | Paga totale dhe hierarkia (§§87–88, 111) (a) | ✓ | ✓ | W lineare; raportet konstante (§8.5) |
| K15 | GJKKO/SPAK jashtë krahasimeve (§87) (a) | ✓ | ✓ | Asnjë krahasim nuk përdor profilin GJKKO si referencë |
| K16 | Tre nivelet e GJL (§111, rekomandim) (a) | — | — | Jashtë paketës; mbetet opsion për Fazën 3 |
| K17 | Ulje vetëm sipas nenit 138/a (§§78–81) (a) | ✗ tavani në rregullin e zakonshëm | ✓ | Tavani vetëm në mekanizmin me 6 kushte (§8.8) |
| K18 | Pa mjete presioni (§§77, 81) (a) | ✗ R ndjek P, që indeksohet me VKM pa kriter ligjor (VKM 92/2026) | ✓ | **Garanci:** publikim deklarativ nga MF brenda 15 janarit; nëse nuk publikohet, zbatim i drejtpërdrejtë nga KLGJ dhe KLP; asnjë parametër pa kriter |

## 9.4 Vlera reale dhe korridori (në A dhe B)

| Testi | L95 | Paketa |
|---|---|---|
| Vlera e 152.700 (9.2022) në çmimet e 8.2026 = 170.015 | **−2,63%** | **+43,25%** |
| Vlera e R*_0 = 231.000 (3.2023) në çmimet e 8.2026 = 248.602 | −33,41% | −2,04% (vonesë brenda ciklit; rikthehet më 1.2028) |
| Korridori [219.888; 252.519] (B) | ✗ | ✓ |
| Dyshemeja 236.425 nga 8.2026 (A) | ✗ | ✓ |

Paketa e kalon testin e vlerës reale të 152.700 me diferencë të madhe, sepse përfshin riparimin e §109. Kundrejt vlerës reale të bazës së vet, ajo mbetet pak pas në mes të ciklit. Ky është kostoja e rishikimit dyvjeçar, që Gjykata e pranoi (§106).

## 9.5 Ndjeshmëria dhe stresi

Humbja reale matet çdo muaj ndaj 231.000 të indeksuar plotësisht me IÇK, 1.2026–12.2031.

| Skenari (d) | Humbja reale maks | Kur | Rishikimet |
|---|---|---|---|
| Bazë: π 3%, ρ 2,5% | −5,82% | 12.2027 | 1.2028, 1.2030 |
| Bazë + rishikim i jashtëzakonshëm (θ = 4%) | −3,95% | 4.2027 | 5.2027*, 1.2028, 5.2029*, 1.2030, 5.2031* |
| **Episod si 2022–23** (π 6,7% në 2027, 4,8% në 2028) | **−9,09%** | 12.2027 | 1.2028, 1.2030 |
| Episod + rishikim i jashtëzakonshëm (θ = 4%) | −4,23% | 10.2027 | 3.2027*, 11.2027*, 1.2028, 12.2028*, 1.2030, 5.2031* |
| L95 në episodin si 2022–23 (fund viti; P ndjek ρ 2,5%) | −10,18% | | |
| L95 me ngrirje të P (ρ 0, π 3%) | −16,32% | | |
| Ngrirje e pagave civile (ρ 0, π 3%) | −5,82% | 12.2027 | R/referencë në 2031 = 1,16 |
| Rënie e të ardhurave: tavan 3 mld/vit për prapambetjet, 2027–2029 | hendek **4,84 mld** | | vonesa 41,1 muaj |
| idem, kalendari i shtyrë deri 2031 | hendek 0 | | vonesa 51,1 muaj; kompensim 1,74 mld |

\* rishikim i jashtëzakonshëm

**Kur funksionon paketa, kur dobësohet, kur kërkon ndërhyrje (b):**
- **Funksionon** kur inflacioni është afër objektivit të BSH dhe referenca civile lëviz normalisht. Humbja maksimale brenda ciklit është rreth 6%, dhe rikuperohet plotësisht në çdo rishikim.
- **Dobësohet** në një episod inflacioni si 2022–23: −9,09% para rishikimit, njësoj si humbja historike e 2022 (§9.2). **Rekomandim (e):** rishikim i jashtëzakonshëm në muajin pas atij kur inflacioni kumulativ nga matja e fundit kalon 4%. Ky prag nuk është i ri: është vetë toleranca θ që ligjvënësi zgjodhi në L95, por e përdorur si **shkas** dhe jo si tavan. Ai e përgjysmon humbjen (−4,23%). Meqë rregulli është i niveleve, rishikimi i jashtëzakonshëm vetëm e sjell më herët pagesën, nuk e ngre nivelin e rishikimeve të rregullta.
- **Ngrirja e pagave civile** e ruan vlerën reale të magjistratëve dhe i çon ata 16% mbi rrjetën civile deri në 2031. Juridikisht paketa funksionon; politikisht ngre pyetjen e barazisë (K10). Ndërhyrja e ligjshme është vetëm masa e përgjithshme e §8.8.
- **Rënia e të ardhurave** nuk e prek detyrimin. Ajo ndikon vetëm te kalendari: tavani 3 mld/vit kërkon shtyrjen deri 2031 me kompensim, ose një burim tjetër.
- **Asnjë krizë nuk e aktivizon vetvetiu nenin 138/a.** Mekanizmi kërkon ligj të veçantë që plotëson gjashtë kushtet e §8.8.

## 9.6 Kontrolli përfundimtar i konsistencës për Fazën 2 (§12)

Skripti `faza2d_testet.py` rillogarit radhazi të gjithë skriptet e Fazës 2. Pastaj nxjerr nga ky dokument çdo numër me ndarës mijëshe ose me presje dhjetore dhe kërkon nëse ai gjendet, brenda tolerancës së rrumbullakimit të shfaqur, në ndonjë CSV të Fazës 2, në `faza1_rezultatet.csv` ose te konstantet burimore (`faza2d_konstantet.csv`). Rezultati është në `faza2d_konsistenca.csv`.

**Kufizimet e këtij kontrolli.** Kontrolli verifikon që numri ekziston në skedarët e llogaritjeve, jo që është vendosur në kontekstin e duhur. Numrat e plotë pa ndarës (p.sh. 417, 45) dhe datat nuk kontrollohen. Kontrolli kontekstual u bë me dorë gjatë hartimit të çdo seksioni. Pas përditësimit të §9.7, kontrolli gjen 586 numra; i vetmi që nuk gjendet është 37,30 në kolonën "Para" të §9.7, që është vlera e versionit të mëparshëm dhe citohet qëllimisht.

| # | Kontrolli | Rezultati për gjithë Fazën 2 |
|---|---|---|
| 1 | Mosregresioni | ✓ C3 në formulë. Tavani vetëm në 138/a, pa ulje nominale dhe me rikuperim. Rishikimi i jashtëzakonshëm vetëm e përshpejton pagesën. |
| 2 | Pa dysheme rrethore | ✓ Dyshemetë vijnë nga V15, V35, IÇK dhe aktet ekzistuese. Pika e mosmarrëveshjes nuk përdoret si dysheme; A2 u përjashtua pikërisht për këtë. |
| 3 | Pa numërim të dyfishtë | ✓ Inflacioni matet nga 3.2023. Maksimumi i niveleve, jo i normave. Kundërfaktikja 2019 nuk shtohet mbi paketën. K11 matet mbi rrugën e indeksuar. |
| 4 | Shifrat = skedarët | ✓ Kontrolli automatik (shih më lart). Në 2c u korrigjua një rrumbullakim (70.530,5 / 91.134,5), që të përputhet me CSV-në. |
| 5 | Argumentet e Gjykatës | ✓ Të gjitha nga shumica, me paragraf. Pakica (§§7–13) dhe pretendimet e palëve janë shënuar veçmas. |
| 6 | Simbolet | ✓ Fjalori §6.1. Ndryshimi i shkrimit të rregullit të indeksimit (2c) shënohet te F4 dhe §8.2. Emërtimet A0–A5, S1–S2, x/h/B_y janë lokale. |

## 9.7 Përditësim nga ligjet e buxhetit 2024–2026, VKM 92–93/2026 dhe ligji 8097/1996 (8.10.2026)

**Burimet e reja (c):** ligji 97/2023 (buxheti 2024), ligji 115/2024 (buxheti 2025) dhe ligji 87/2025 (buxheti 2026), të gjithë të përditësuar me aktet normative; VKM 92 dhe 93, datë 6.2.2026; ligji 8097/1996 për pensionet suplementare, i përditësuar deri te ligji 166/2020. Vendimi 63/2026 i GJK ka të bëjë me afatin e arsyeshëm në një çështje pronësore, prandaj nuk përdoret.

**Çfarë ndryshoi (c):**
- P = 425.000 në 2024 dhe 2025. Në 2026, ligji 87/2025 (neni 13) e vendos 425.000 "dhe indeksohet në masën e përcaktuar me vendim të Këshillit të Ministrave". VKM 92/2026 e indeksoi 2,5%, në **435.625** nga 1.1.2026.
- VKM 93/2026 indeksoi R e ligjit 33/2023 me 2,5%, në **156.825** nga 1.1.2026 (D3 e zgjidhur).
- Prandaj L95 (0,38 × P) jep **165.537,5** në 2026, jo 161.500.

Të gjitha skriptet u rillogaritën dhe §§6–9 u përditësuan. Kontrolli i §9.6 nuk gjen asnjë mospërputhje. **Paketa, R e saj dhe renditja e alternativave nuk ndryshojnë.** Ndryshojnë vetëm krahasimet me L95 dhe prapambetjet e 2026:

| | Para | Pas |
|---|---|---|
| ΔC/vit e paketës kundrejt L95 2026 (N_R qendror) | 3,89 mld | 3,70 mld |
| Prapambetja 4.2023–12.2026 | 14,01 mld | 13,84 mld |
| Kostoja 2027–2031 (skenari qendror) | 37,30 mld | 34,98 mld |
| L95 kundrejt vlerës reale të 152.700 | −5,0% | −2,6% |

**Konstatim i ri për K18 dhe K2 (b).** Ligji i buxhetit nuk e fikson P; ai ia lë Këshillit të Ministrave masën e indeksimit pa asnjë kriter. Meqë L95 e lidh R me P, **ekzekutivi e cakton pagën e magjistratëve përmes indeksimit të pagës së Presidentit**. Kjo është pikërisht hapësira e ndikimit që V15 §§77 dhe 81 e quan të papranueshme, dhe e forcon pikën (iii) të pakicës kundër L95, jo kundër paketës. Në 2026 të tri indeksimet (P, R, rrjeta civile) ishin 2,5%, ndërsa inflacioni kumulativ nga 3.2023 ishte 5,43%. Kjo konfirmon K10: qeveria trajtoi njësoj të tri kategoritë, por asnjërën nuk e mbrojti plotësisht nga inflacioni.

**Pensioni suplementar (D11, ligji 8097/1996; c për formulën, d për profilet).** Paga referuese e pensionit është paga e muajit të fundit (neni 1/7), prandaj pensioni është linear në W, pra në R.
- Magjistratët (grupi i dytë "a") marrin 1,5% për çdo vit shërbimi, deri në 40% (neni 11).
- Gjyqtarët e GJL dhe GJK dhe anëtarët e KLGJ/KLP (grupi i parë "b") marrin 20% për dy vitet e para + 5% për çdo vit tjetër, deri në 50% (neni 9).

| Profili | Pensioni suplementar mujor, L95 2026 | Me paketën | Diferenca |
|---|---|---|---|
| G2, 25 vjet | 153.950 | 226.491 | +72.541 |
| G1, 30 vjet (tavan 40%) | 158.916 | 233.797 | +74.881 |
| Gjyqtar i GJL, 9 vjet në GJL, 25 vjet gjithsej (tavan 50%) | 211.888 | 311.729 | +99.841 |

Kostoja agregate nuk llogaritet, sepse mungon numri i përfituesve. Efekti është proporcional me R në të gjitha alternativat, prandaj renditja nuk ndryshon.

Teksti i konsoliduar (deri në 2020) ende përmban tavanin "jo më shumë se paga e Presidentit" (neni 1/7/b–c), të cilin V35 e shfuqizoi (Faza 1). Me paketën, W e Kryetarit të GJL me 25 vjet e kalon P 2026 me 54,6%. Duhet verifikuar nëse institucioni i sigurimeve e zbaton ende tavanin në praktikë (D11′).

---

## Përmbyllja e Fazës 2

**Formula e rekomanduar:** R_t = max{ R_{t−1} ; 231.000 · max( IÇK(τ−1)/IÇK(3.2023) ; Ref_t/231.000 ) }, me Ref = I-2 + 14.000. Rishikimet bëhen më 1 janar të çdo viti çift, plus rishikim i jashtëzakonshëm kur inflacioni kumulativ kalon 4%. Ulja lejohet vetëm me mekanizmin 138/a. Kjo jep 243.539 lekë nga 1.2026.

**Riparimi:** 13,84 mld lekë prapambetje (10,50–17,16), të shlyera 2027–2029 me kompensim IÇK.

**Kostoja:** 3,50 mld lekë/vit në 2027 kundrejt L95 (3,70 mld kundrejt nivelit të L95 në 2026). Kulmi vjetor me prapambetjet në skenarin qendror është 9,50 mld (7,9% e fondit të pagave 2026).

**Fundi i Fazës 2.** Faza 3 (punimi përfundimtar, dispozitat model, bibliografia) nis vetëm pas miratimit tuaj.
