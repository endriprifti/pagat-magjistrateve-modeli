# Pagat e magjistratëve pas Vendimit nr. 15/2026 — Faza 1

**Matrica e kërkesave, kronologjia, baza e llogaritjes dhe inventari i të dhënave**

Data përfundimtare e verifikimit: **7 tetor 2026**. Versioni 4: i rishikuar pas shtatë akteve zyrtare shtesë (KLGJ, KLP, VKM, raporte parlamentare, akt normativ), Vendimit 35/2022, katër raporteve të KLSH dhe materialeve të ligjit 33/2023 dhe VKM 325/2023 (origjinale), 337/2025, 131/2026. Versioni 6 shton evidencën e pagesave të Thesarit (BIG_TABLE, financa.gov.al, 2024–5.10.2026; skripti `faza1_thesari.py`). Llogaritjet: `faza1_llogaritjet.py` → `faza1_rezultatet.csv` (çdo shifër më poshtë del nga ky skedar).

> **Errata (8.10.2026), pas ligjeve të buxhetit 2024–2026 dhe VKM 92–93/2026.** Tri shifra të kësaj faze ndryshojnë. Faza 2 është rillogaritur plotësisht me vlerat e reja.
> 1. **P në 2026 = 435.625**, jo 425.000. Ligji 87/2025 (neni 13) e vendos P në 425.000 "dhe indeksohet në masën e përcaktuar me VKM". VKM 92, datë 6.2.2026, e indeksoi 2,5% nga 1.1.2026. Raporti i KDNJMIP citoi vetëm nenin 13 pa VKM-në. Në 2023–2025, P = 425.000 (ligjet 97/2023 dhe 115/2024). **Në §0 e kisha refuzuar 435.625 të bashkëngjitjes së IA-së; për këtë shifër bashkëngjitja kishte të drejtë.**
> 2. **R e paguar nga 1.1.2026 = 156.825** (VKM 93/2026: 0,36 × 435.625), jo 153.000 (D3 e zgjidhur). Prapambetjet e §4.4–4.5 për 1–7.2026 janë pak më të ulëta.
> 3. **L95 në 2026 = 0,38 × 435.625 = 165.537,5**, jo 161.500. Testi i fuqisë blerëse (§4.2, përfundimi 13) bëhet **−2,6%** nën vlerën reale të 152.700 (jo −5,0%); ulja nominale në skenarin A bëhet −30,0% (jo −31,7%). Përfundimet cilësore nuk ndryshojnë.

Shënimet (a)–(e) në tekst ndjekin hierarkinë e §3 të detyrës: **(a)** kërkesë e shprehur e Gjykatës · **(b)** interpretim i argumentuar në këtë punim · **(c)** fakt/e dhënë e verifikuar · **(d)** supozim modeli · **(e)** rekomandim.

---

## 0. Burimet e shqyrtuara dhe kufizimet

| Dokumenti | Statusi | Shënim |
|---|---|---|
| Vendimi nr. 15, datë 17.2.2026 (V15), përfshirë mendimin e pakicës | Burim primar | Lexuar i plotë (§§1–112, dispozitivi, mendimi i pakicës i gjyqtarit G. Ibrahimi). |
| Fletorja Zyrtare nr. 80, datë 17.4.2026 | Burim primar | Përmban V15; data e botimit = data e hyrjes në fuqi. U ngarkua **dy herë** (skedarë identikë). |
| Ligji nr. 95/2026, datë 18.9.2026 (L95) | Burim primar | Lexuar i plotë. |
| Dekreti nr. 495, datë 18.9.2026 | Burim primar | Shpallje + pëlqim për hyrje në fuqi menjëherë (neni 84/4 Kushtetutës). |
| Ligji nr. 96/2016, i përditësuar deri te L95 | Burim primar (tekst i konsoliduar jozyrtar) | Lexuar nenet 2, 11–22, 173–175. |
| Vendimi nr. 35, datë 22.11.2022 (V35) | Burim primar | Lexuar i plotë (njëzëri; shpallur 30.12.2022). Përcakton standardin e R (§§62–76), shfuqizon edhe tavanin e pensionit suplementar me pagën e Presidentit (disp. 3), dhe §104. **Shuma 152.700 nuk gjendet në V35.** |
| **Vendimi i KLGJ nr. 435, datë 26.8.2026** | Akt administrativ i organit të qeverisjes | R = 222.425 + 14.000 = **236.425** nga 1.8.2026; rillogaritje 1.4.2023–31.7.2026 sipas VKM 325; pagesa e diferencave e shtrirë në 2027–2028. |
| **Vendimi i KLP nr. 144, datë 28.8.2026** (kopje e skanuar, e lexuar vizualisht) | Akt administrativ i organit të qeverisjes | E njëjta R dhe e njëjta skemë për prokurorët dhe anëtarët e KLP. Arsyetim i plotë (§§7–31) se §110 i V15 u aktivizua *ipso iure* më 31.7.2026. |
| VKM nr. 325/2023, i përditësuar deri te VKM 544/2026 | Burim primar (akt nënligjor) | Lidhja 1: I-2 = 222.425; Lidhja 2: grupi i diplomës 1 = 14.000; Lidhja 7: klasifikimi i pozicioneve. |
| VKM nr. 187/2017, versioni deri te VKM 620/2022 | Burim primar (akt nënligjor, i shfuqizuar) | Lidhja 1: I-a 141.900, I-b 129.800, II-a 118.100; Lidhja 4: drejtor DP = II-a. |
| Raporti i Komisionit për Çështjet Ligjore, 15.9.2026 | Dokument parlamentar | Historiku i L95, amendamentet, dëgjesa, vlerësimi i vonesës. |
| Raporti i Komisionit për të Drejtat e Njeriut (KDNJMIP), 15.9.2026 | Dokument parlamentar | Vlerësimi financiar i KM, P = 425.000 në 2026, dëgjesa, të dhëna CEPEJ. |
| Akti normativ nr. 2, datë 30.6.2026 (buxheti 2026) | Burim primar | Buxheti i KLGJ, PP, KLP; numri i punonjësve; fondi i pagave i shtetit. |
| KLSH, auditim tematik në KLGJ (janar 2021) | Raport auditimi | Rekomandimi R = 14.000 + 118.100 = 132.100 (mbi II-a); kundërshtimi i KLGJ për efektin financiar dhe efektin zinxhir. |
| KLSH, auditim financiar në GJL (shkurt 2023), i cituar në V15 §111 | Raport auditimi | Tabela e pagave të gjyqtarëve të GJL në tre kategori (f. 34): **6 shifra reale page** që përdoren për të validuar W(R). |
| KLSH, auditim në KLGJ (janar 2024) | Raport auditimi | Fond shtesë 170 mln lekë në 2023 (140 mln paga + 25 mln kontribute) për efektet e ligjit 33/2023 dhe VKM 325/326; s'ka gjetje për R. |
| KLSH, auditim financiar në KLP (maj 2024) | Raport auditimi | VKM 755, datë 20.12.2023: fond shtesë për pagesën e **një pjese** të diferencave sipas V35. U ngarkua dy herë (skedarë identikë). |
| Ligji nr. 33/2023, RIA (7.4.2023), raportet e Komisionit të Ekonomisë dhe të Komisionit Ligjor (22.5.2023) | Burim primar dhe dokumente parlamentare | **Zgjidhin origjinën e 152.700**; kosto 959 mln lekë/vit; amendamenti i refuzuar κ = 0,46. RIA u ngarkua tri herë (skedarë identikë). |
| VKM 325/2023 origjinale; VKM 337/2025; VKM 131/2026 | Burime primare | Lidhja 1 nga 1.4.2023: I-1 235.000, **I-2 217.000**, I-3 205.000, I-4 180.000, I-5 170.000. VKM 337/2025 shton I-1/1 (226.000) pa ndryshuar I-2. VKM 131/2026: indeksim 2,5% për të gjitha klasat e larta, **me efekt nga 1.1.2026** (ndarja III/b). |
| Pagesat e Thesarit (BIG_TABLE.xlsx, 10 kode institucionesh, 1.2024–5.10.2026) | Burim primar (regjistra transaksionesh) | 9.656 rreshta; 599 dyfishime të hequra. Përshkrimet e listëpagesave përmbajnë muajin, numrin e punonjësve dhe bazën ligjore ose gjyqësore. Përfshin vetëm aparatin e PP, jo gjithë prokurorinë; KLGJ si aparat nuk është në listë. |
| **VKM 755, datë 20.12.2023** | Burim primar | 1 mld lekë nga fondi i kontingjencës për "një pjesë" të diferencës sipas V35, nga 1.1.2019; afati i pagesës 15.1.2024. Ndarja: 876 mln sistemi i drejtësisë; 107 mln institucionet e vetingut; 17 mln KQZ dhe Avokati i Popullit. |
| **KLGJ nr. 233, datë 23.4.2025** | Akt i organit të qeverisjes | Numri i përgjithshëm i gjyqtarëve: **417** (pozicione në organikë, jo të emëruar faktikisht). |
| Ligji 115/2016, i përditësuar deri te ligji 47/2019 | Burim primar (tekst i konsoliduar jozyrtar) | Anëtarët e KLGJ/KLP kanë statusin e magjistratit dhe pagën e gjyqtarit të GJL (nenet 4, 102); kryetarët, pagën e Kryetarit të GJL (nenet 59, 157); ILD dhe Drejtori i Shkollës, pagën e gjyqtarit të GJL (nenet 198, 250); Këshilltari për Etikën, sipas L96 (neni 83); inspektorët magjistratë, pagën e gjyqtarit të apelit (neni 210). |
| Ligji 8577/2000 (GJK), i përditësuar deri te ligji 45/2021 | Burim primar | Neni 17: gjyqtari i GJK = paga e Kryetarit të GJL; Kryetari i GJK +20%; paga "nuk mund të ulet". Neni 15: këshilltarët ligjorë juristë = paga bruto fillestare e gjyqtarit të shkallës së parë. |
| RPM e BSH 2025/I – 2026/III; material teknik për inflacionin bazë (2024) | Burim zyrtar | Objektivi 3% i konfirmuar në të shtatë raportet; **asnjë brez toleruese ±1 p.p.** RPM 2026/III (të dhëna deri 29.7.2026): inflacioni mesatar 3% në T2/2026, pritet përkohësisht mbi objektiv. Inflacioni bazë është tregues i politikës monetare, jo i kostos së jetesës. |
| VKM 495/2022 (harta gjyqësore); KLGJ 505/2022 (Apeli i Juridiksionit të Përgjithshëm) | Burime primare | Pa ndikim në pagë; shpjegojnë ndryshimet organizative 2023 në Thesar. |
| Dy dalje të Gemini (7.10.2026): organika 386 gjyqtarë / 341 prokurorë, trupa aktive ≈ 430, tabela e vjetërsisë | Tekst i IA-së, pa burim | **Nuk përdoret.** Mjedisi i tij nuk kishte asnjë dokument të KLGJ/KLP. Shifrat kundërshtojnë njëra-tjetrën (386 / 402–412 / 417; 727 / 753 / 770) dhe kundërshtojnë KLGJ 233/2025 (417). Vendimi 505/2022 që citon nuk përmban numra (neni 2/1: "me akt të veçantë"). Tabela e vjetërsisë pranohet nga vetë teksti si modelim. Rregulli i vjetërsisë ("2% mbi 3 vite") dhe shtesat drejtuese 10–20% kundërshtojnë L96 dhe validimin me KLSH (§4.3). |
| Opinioni i gjyqtarit Bega; punimi në Academia.edu; dokumenti i modelit të negocimit | Analiza dytësore | Nuk u përdorën në këtë fazë (nuk u bashkëngjitën). |

**Burimi i tre shumave të përmendura në detyrë (P9, i zgjidhur):**
- **236.425** = 222.425 (I-2) + 14.000. Është R e miratuar nga KLGJ 435 dhe KLP 144. (c)
- **220.320** = 153.000 × 1,44 saktësisht, pra R3 e rritur me "afërsisht 44%" të §100. Është rindërtim aritmetik, jo shifër e gjetur në burim. (c)
- **198.963** = (236.425 + 161.500) / 2 = 198.962,5, pra mesi i Nash-it me peshë të barabartë ndërmjet R të Këshillave dhe R të L95. Vjen nga punimi i mëparshëm i autorit në Academia.edu (nr. 176599887). Sipas §2 të promptit është burim dytësor, jo autoritativ. Vlera bie 9,5% nën dyshemenë e korridorit të §109 (219.888) dhe 10,5% nën I-2 2026 (222.425). Ajo përzien gjithashtu një R të vitit 2026 (236.425) me bazën e L95. Prandaj në Fazën 2 trajtohet vetëm si alternativë krahasuese "ndarje e diferencës", jo si zgjidhje. (c) për aritmetikën; vetë burimi është dytësor.

---

## 1. Fusha e zbatimit

| Kategoria | Lidhja me R | Burimi | Statusi |
|---|---|---|---|
| Gjyqtarët dhe prokurorët G1, G2, G3 | Paga totale lineare në R (shih §4.3) | L96 nenet 2/j, 12, 14 | (c) |
| Magjistratët e GJKKO/SPAK | R + 80% e pagës bruto fillestare | L96 neni 12/5/d | (c) |
| Anëtarët dhe kryetari i Gjykatës Kushtetuese | Ndjekin R të re | L96 neni 12/1, par. 1 (shtuar me L95); neni 17 i ligjit 8577/2000 | (c); teksti i nenit 17 **nuk** është bashkëngjitur |
| **Të gjithë funksionarët/nëpunësit e tjerë që referojnë te paga e gjyqtarit ose prokurorit** | **Të ngrirë te R para V15** (pra 153.000) | L96 neni 12/1, par. 2 | (c). Kategoritë konkrete (p.sh. anëtarë të KLGJ/KLP, ILD, të tjerë) dhe numri i tyre **nuk** dalin nga dokumentet. |
| Pensionet suplementare | Lidhen me pagën përmes ligjit për pensionet suplementare | L96 neni 21 | (c) për lidhjen; formula dhe efekti **nuk** dalin nga dokumentet. |
| Magjistratët e komanduar | Paga më e lartë ndërmjet dy pagave | L96 neni 13 | (c) |

**Konstatim (b):** neni 12/1, par. 2, i krijuar me L95, e shkëput efektin zinxhir me ligj. Kjo ul koston, por ngre pyetjen nëse ngrirja bie nën nenin 138 për përfituesit që janë vetë magjistratë. Sipas KLP 144 (§2/a, §17), anëtari i KLP ka statusin e magjistratit dhe paguhet drejtpërdrejt si G3 mbi R. Nëse kjo vlen, anëtarët e Këshillave nuk janë "funksionarë të tjerë që referojnë" dhe nuk bien nën ngrirjen e nenit 12/1. Kategoritë e tjera të lidhura dhe numri i tyre mbeten të panjohura.

**Përmasat e institucioneve (c, AN 2/2026, Tab. 2, gjithë punonjësit, jo vetëm magjistratët):** KLGJ (sistemi gjyqësor) 1.992; Prokuroria e Përgjithshme 979; SPAK/BKH 339; Gjykata Kushtetuese 101; KLP 77.

---

## 2. Matrica e kërkesave të Vendimit nr. 15/2026

Shkurtime: V15 = Vendimi 15/2026; R = paga referuese bazë; W = paga mujore bruto totale.

| # | Kërkesa | Burimi | Statusi | Kuptimi juridik | Formalizimi / verifikimi | Të dhënat e nevojshme | Elementi i propozimit (Faza 2) | Pasiguria |
|---|---|---|---|---|---|---|---|---|
| K1 | Detyrim i Kuvendit për ndryshime ligjore brenda 31.7.2026 | Disp. 3; §109 | (a) | Afat kushtetues detyrues (neni 132 Kushtetutës) | Nisma u depozitua më 30.7.2026; L95 u miratua më 18.9.2026: **49 ditë vonesë**. Kuvendi e pranon vonesën dhe e justifikon me sesionet dhe me botimin e V15 më 17.4 (Raporti i Komisionit Ligjor, II). | — | Rregull kalimtar për periudhën e vonesës | E lartë: pasojat e vonesës (P1) |
| K2 | Rregullat themelore të pagës caktohen **me ligj**, objektive, të parashikueshme, të qëndrueshme, transparente | §§71, 76–77 | (a) | Rezervë ligjore materiale, jo vetëm formale | Kontroll: asnjë parametër i R nuk varet nga akt diskrecional pa kritere | — | Formula + parametrat në ligj; burimi statistikor i caktuar me ligj | E ulët |
| K3 | **Konsultim efektiv** me magjistratët ose grupimet përfaqësuese; analizë e qëllimit dhe pasojave | §§76, 98 | (a) | Kërkesë procedurale e kushtetutshmërisë; mungesa e saj ishte pjesë e arsyetimit | Për L95 (c): konsultim online 8–15.9.2026 (1 koment); dëgjesa me KLP, GJL, Unionin dhe shoqatat **më 15.9, në të njëjtën ditë me votimin në komision**, pas kërkesës së 1/3 së anëtarëve. PP deklaroi se nuk ishte njohur zyrtarisht me projektligjin. Të gjithë të dëgjuarit e kundërshtuan κ = 0,38; teksti përfundimtar nuk reflektoi asnjë vërejtje. Kryetarja e KDNJMIP shënoi shkelje procedurale: komisioni përgjegjës votoi para përfundimit të komisionit për mendim. | Procesverbalet e plota (mungojnë) | Procedurë konsultimi në ligj, me afat minimal dhe përgjigje të arsyetuar | E mesme → **e ulët**: faktet e raporteve i ngjajnë situatës që Gjykata e quajti joefektive në §98 |
| K4 | Ndalim i uljes së **hapur ose të fshehtë**, përfshirë **ngrirjen e shënjestruar** | §§57, 60/vii, 80–82, 94, 104–105, 108 | (a) | "Ulje" ≠ vetëm rënie nominale. Ndryshimi i referencës që lë R të pandryshuar ndërsa referencat rriten = ulje e fshehtë | Test dinamik: rritja e R krahasohet me rritjen e referencës së vjetër dhe të re në të njëjtën periudhë | Seritë e pagave referuese (§4) | Formula dinamike + klauzolë mosregresioni | E mesme: masa e "mjaftueshme" e rritjes nuk caktohet nga Gjykata |
| K5 | Paga ndjek "fatin e pagës në të cilën është referuar" | §92 | (a) | Simetri: rritet dhe ulet bashkë me referencën; ulja vetëm sipas nenit 138/a | Elasticitet ≈ 1 ndaj referencës | Seri e referencës | Indeksim te referenca | E ulët |
| K6 | Riparimi i **uljes së fshehtë** dhe përshtatja e pagës "në raport të drejtë me rritjet e tjera" | §109 | (a) | Detyrim rezultati | R e re ≥ kufiri i poshtëm i korridorit (K7) | Seria e kategorisë civile dhe e Presidentit | Baza e riparuar R* | E lartë: P2 |
| K7 | Opsionet e lejuara: referim te ndryshimi i **kategorisë civile** të formulës së vjetër, ose te ndryshimi i **pagës së Presidentit**, ose zgjidhje tjetër "e krahasueshme me ndryshimet e kategoritë e mësipërme dhe **brenda limiteve të tyre**" | §109 | (a) për tekstin; (b) për leximin si korridor | Lexim (b): rritja e R ndaj 152.700 duhet të bjerë në intervalin e rritjeve të dy referencave: **~44% deri në ~65,4%** | 219.888 ≤ R* ≤ 252.519 lekë (baza 2023) | §4.2 | Kalibrimi i R* | **E lartë**: shih P2 |
| K8 | Referenca duhet të jetë pagë që **rritet herë pas here dhe indeksohet**; jo një pagë që ndryshon rrallë ose është "vlerë e plotë e pastrukturuar" si ajo e Presidentit | §108 | (a), por e formuluar si udhëzim ("për të realizuar një formulë sa më të drejtë") | Preferencë e fortë kundër referencës te Presidenti si e vetmja ankorë | Kontroll: a ka mekanizëm që e lëviz R kur paga e referencës nuk lëviz? | Historiku i pagës së Presidentit | Referencë e dyfishtë ose indeks i pagave publike | E mesme: §109 e lejon gjithsesi referencën te Presidenti |
| K9 | Mbrojtje nga **inflacioni**: indeksim ose rishikim periodik, që ruan vlerën reale sipas IÇK | §§83–85 | (a) | Kriter i tretë kushtetues | Testi i fuqisë blerëse: R_t / IÇK_t jo-rënëse (ose rënie e kufizuar) | Seria IÇK (INSTAT) | Rregulli i indeksimit | E mesme: tavani "≤ target + 1 p.p." (P3) |
| K10 | Ligjvënësi mban parasysh zhvillimin e të ardhurave të magjistratëve me IÇK, "njëlloj siç vepron për kategoritë e tjera" | §84 | (a) | Barazi trajtimi me punonjësit e tjerë shtetërorë për mbrojtjen nga inflacioni | Krahasim i indeksimeve të pagave publike me ato të R | Indeksimet e VKM-ve për pagat publike | Klauzolë barazie indeksimi | E mesme |
| K11 | Paga të ecë "në të njëjtën linjë me zhvillimet ekonomike e financiare dhe standardin e jetesës", duke u përshtatur me situatën financiare të shtetit | §§94, 102 | (a) | Jo vetëm inflacion; edhe rritja reale e pagave | Krahasim me pagën mesatare dhe pagat publike | Seria e pagës mesatare (INSTAT) | Korrigjim periodik | E lartë: pakica (§§9–11) e quan detyrim pozitiv rritjeje pa bazë kushtetuese |
| K12 | **Efektet financiare nga 1.4.2023**; "skemë e arsyeshme përshtatjeje" për prapambetjet deri në hyrjen në fuqi të ligjit të ri | §110 | (a) | Detyrim kompensimi retroaktiv; kalendari mund të shtyhet, e drejta jo | Diferencë W(R*) − W(R paguar) × muaj | N, struktura e pagave, pagesat e kryera | Plani i prapambetjeve | E mesme. L95 nuk përmban skemë; KM e paralajmëroi pagesën "në disa vite" vetëm në relacion. KLGJ/KLP e shtrinë në 2027–2028. |
| K13 | Nëse ndryshimet nuk bëhen deri më 31.7.2026: prapambetjet llogariten me formulën që referon te **funksionari i administratës së lartë publike sipas V35** | §110 | (a) në arsyetim; jo në dispozitiv | Rregull i paracaktuar në rast mosveprimi | **KLGJ 435 dhe KLP 144 e zbatuan si të vetë-ekzekutueshëm**: R = 236.425 nga 1.8.2026 dhe rillogaritje 1.4.2023–31.7.2026 sipas vlerave të VKM 325 për çdo nënperiudhë. Kuvendi dhe KM e kundërshtojnë kompetencën e Këshillave (KDNJMIP; Ministri i Drejtësisë). | Seria e I-2 sipas nënperiudhave; nëse pagat u paguan me 236.425 | Rregull kalimtar | **E lartë**: P1 tani është konflikt real mes akteve |
| K14 | Përshtatshmëria vlerësohet në **pagën totale** dhe në **hierarkinë brenda gjyqësorit** | §§87–88, 111 | (a) | R mjafton si objekt kur W është lineare në R; hierarkia kërkon kontroll të veçantë | W = R·[(1+γ)(1+λ+δ) + 0,02·min(y,25)] (§4.3) | Shpërndarja e magjistratëve | Ruajtja e koeficientëve | E ulët |
| K15 | Pagat e GJKKO/SPAK **nuk** janë pikë referimi për analizën | §87 | (a) | Pagë "atipike" | Përjashtohen nga krahasimet | — | — | E ulët |
| K16 | Pagat e gjyqtarëve të Gjykatës së Lartë (tre nivele): rekomandim i KLSH "për t'u konsideruar" | §111 | (a) si rekomandim, jo detyrim | Jo kusht kushtetutshmërie | — | Raporti KLSH 2023 | Opsion ndihmës | E ulët |
| K17 | Ulje e lejuar vetëm sipas nenit 138/a: masë e përgjithshme, jo e shënjestruar, e justifikuar, objektive, proporcionale, e kufizuar në kohë, pa cenuar dinjitetin | §§78–81 | (a) | Rezervë absolute kushtetuese | Kontroll me 6 kushte kumulative | — | Mekanizmi i jashtëzakonshëm | E ulët |
| K18 | Ndalimi i përdorimit të pagës si mjet presioni; formula pa hapësira ndikimi | §§77, 81 | (a) | — | Asnjë parametër i lënë në diskrecion pa kriter | — | Formula automatike | E ulët |

**Vërejtje mbi statusin e kërkesave.** Dispozitivi (pika 3) e lidh detyrimin me "arsyetimin e këtij vendimi". Prandaj K6–K13 janë detyruese si pjesë e arsyetimit mbështetës, por shkalla e detyrueshmërisë së formulimeve udhëzuese (K8, K11) është më e ulët se ajo e konstatimeve thelbësore (K4, K12). Ky dallim është (b).

**Mendimi i pakicës (G. Ibrahimi)** nuk krijon kërkesa, por shënon pikat ku propozimi do të sulmohet: (i) neni 138 nuk garanton diferencë me pagat e tjera (§§7, 10); (ii) mungon analiza financiare e përshtatshmërisë së pagës totale (§9); (iii) referenca te VKM-të mund të cenojë kriterin "me ligj" (§12); (iv) indeksimi dyvjeçar mjafton kundër inflacionit (§13). Propozimi i Fazës 2 duhet t'u përgjigjet këtyre katër pikave.

---

## 3. Kronologjia juridike dhe financiare

| Data | Ngjarja | R (lekë/muaj) | Burimi |
|---|---|---|---|
| 6.10.2016 | L96: R = "pagë për funksion", kategoria I, klasa III, drejtor i DP në Kryeministri | — | V15 §§2, 35 |
| 1.1.2019 | Fillon zbatimi; R llogaritet gabimisht te kategoria II-a, vetëm "shtesa për pozicion" | 118.100 | V15 §§35, 37 |
| 2021 | KLSH rekomandon R = 14.000 + 118.100, me efekt që nga fillimi | 132.100 | V15 §38 |
| 23.3.2021 | Ligji 50/2021 kodifikon referencën më të ulët | — | V15 §§4, 39 |
| 17.10 / 25.11.2022 | Projektbuxheti 2023 / Ligji i buxhetit 2023: fond 2.300 mln lekë për politika të reja pagash; P = 257.000 | — | V15 §42 |
| 22.11.2022 | V35 (njëzëri) shfuqizon ligjin 50/2021 dhe tavanin e pensionit suplementar; standardi I-b + 14.000 | 143.800 sipas standardit të V35 (VKM 187); **152.700** sipas relacionit 2023 dhe V15 §95 | V35 §§76–77, disp.; V15 §§44, 95 |
| 28.9.2022 | VKM 621/2022: I-b 138.700; II-a 126.300 | standardi i V35: 152.700 | RIA 2023 |
| 30.12.2022 | V35 shpallet | — | V35 |
| 9.1.2023 | V35 hyn në fuqi (FZ nr. 3) | 152.700 | V15 §§5, 40 |
| 1.4.2023 | Data e efekteve financiare të ligjeve 33/2023 dhe 34/2023 dhe të VKM 325/2023 | — | V15 §§46–47 |
| Shkurt 2023 | KLSH, auditimi i GJL: R ende 118.100; tre nivele page brenda GJL | 118.100 (e paguar në GJL) | KLSH GJL, f. 34 |
| 7.4.2023 | RIA e projektligjit (pa konsultim publik): 152.700 si e drejtë e fituar; κ = 0,36 jep 153.000; kosto 959 mln lekë/vit, përfshirë funksionarët e lidhur | — | RIA |
| 22.5.2023 | Komisionet: refuzohet amendamenti κ = 0,46 (195.500); MF krahason me raportin 1:4 të Gjermanisë | — | Raportet e komisioneve |
| 25.5.2023 | Ligji 33/2023: R = 0,36 × P; indeksim ≤ 2 vjet, ≤ target BSH + 1 p.p.; i pari jo para 1.1.2026. Ligji 34/2023: P = 425.000 | **153.000** | V15 §§6, 43, 46 |
| 31.5.2023 | VKM 325/2023: rritje e pagave të administratës, efekt nga 1.4.2023 | — | V15 §47 |
| 18.10.2023 | Akti normativ nr. 5 rikonfirmon P = 425.000 | — | V15 §46 |
| 2026 | "Indeksimi i parë" i R | **e panjohur** | V15 §105 (vetëm përmendje) |
| 17.2.2026 | V15 merret (7–1) | — | V15 |
| 15.4 / 17.4.2026 | V15 shpallet / botohet në FZ nr. 80 dhe hyn në fuqi | — | V15; FZ 80 |
| 20.12.2023 | VKM 755/2023: fond për pagesën e një pjese të diferencave sipas V35 | — | KLSH KLP 2024 |
| 27.2.2026 | VKM 131/2026: pagat civile +2,5% **me efekt nga 1.1.2026** (I-2: 217.000 → 222.425) | (referenca civile: 231.000 → 236.425) | VKM 131/2026 |
| 4.5.2026 | Këshilli i Legjislacionit; sipas Unionit, nismëtarja pranoi se mosmiratimi deri më 31.7 aktivizon §110 | — | Raporti KDNJMIP (pretendim i palës) |
| 30.6.2026 | Akti normativ 2/2026 rishikon buxhetin 2026 pa fond të identifikueshëm për zbatimin e V15 | — | AN 2/2026 |
| 30.7.2026 | Nisma e deputetëve depozitohet në Kuvend | — | Raportet e komisioneve |
| **31.7.2026** | **Afati i Gjykatës; efektet e shfuqizimit hyjnë në fuqi** | — | V15 disp. 3–4 |
| 1.8.2026 | Data nga e cila KLGJ/KLP aplikojnë R e re | **236.425** | KLGJ 435; KLP 144 |
| 26.8 / 28.8.2026 | Vendimet KLGJ 435 dhe KLP 144 | 236.425 | idem |
| 14.9.2026 | Mendimi i KM: efekt shtesë 2023–2026 rreth 1,5 mld lekë; rreth 500 mln lekë/vit në vazhdim | — | Raporti KDNJMIP |
| 14.9.2026 | Amendamentet e relatorit heqin shtesat e reja për GJL/PP (80% + 5% dhe vjetërsia) | — | Raporti i Komisionit Ligjor |
| 15.9.2026 | Dëgjesat dhe votimi në të dy komisionet (KDNJMIP: 5 pro, 3 kundër) | — | Raportet |
| Gusht–shtator 2026 | Pretendime në Kuvend se magjistratët ishin "dy muaj pa pagë" dhe se pagat u bllokuan në thesar; padi individuale në gjykatën administrative | ? | Raporti KDNJMIP (pretendime, të paverifikuara) |
| 2–4.9.2026 | Pagat e gushtit paguhen në kohë në SPAK, GJK dhe ILD, pa ndryshim. **Në GJL, gjykatat administrative të Tiranës, PP dhe KLP nuk paguhen.** | — | Thesari |
| 11–15.9.2026 | Gjykata Administrative e Shkallës së Parë Tiranë: vendimet nr. 10878, 10902, 10941, 31154-01494-89-2026, me ekzekutim të menjëhershëm, për pagat e gushtit | — | Thesari (përshkrimet e pagesave); vendimet vetë nuk janë parë |
| 17–21.9.2026 | Pagat e gushtit të magjistratëve paguhen **në bazë të vendimeve gjyqësore**, me shuma dukshëm më të larta | ≈ 236.425 (e nënkuptuar, shih §4.6) | Thesari |
| 18.9.2026 | L95: R = 0,38 × P, efekte nga 1.4.2023; neni 12/1; dekreti 495, hyrje në fuqi menjëherë | **161.500** (P = 425.000 në 2026, sipas nenit 13 të ligjit të buxhetit, KDNJMIP) | L95; Dekreti 495 |

**Pika kronologjike me pasoja (b):** gjatë 49 ditëve 31.7–18.9.2026 fjalia që përcaktonte R ishte e shfuqizuar. KLGJ dhe KLP e mbushën boshllëkun me R = 236.425, duke e mbështetur drejtpërdrejt në §110 dhe në nenin 132 të Kushtetutës. Pastaj L95 vendosi R = 161.500 prapavepruese. Nëse aktet e Këshillave ishin të vlefshme, **L95 sjell ulje nominale prej 31,7%** të R në fuqi. Kjo do të ishte "ulje" edhe sipas leximit më të ngushtë të nenit 138, atij të mendimit të pakicës (§11). Nëse aktet e Këshillave ishin jashtë kompetencës, R ishte e papërcaktuar në atë periudhë. Kjo është pika më e rëndë e gjithë çështjes (P1).

---

## 4. Baza e llogaritjes

### 4.1 Mospërputhje në shifrat e vendimit (c)

| Shifra në vendim | Kontrolli aritmetik | Përfundimi |
|---|---|---|
| "R u shtua me **570 lekë**" (§49) | 0,36 × 425.000 − 152.700 = **300** | Nuk përputhet. +570 do të kërkonte R para 2023 = 152.430. |
| "rritja prej **0,192%**" (kërkuesi, §17.2) | 300 / 152.700 = 0,196%; 570 / 152.700 = 0,373% | 0,192% përputhet me +300, jo me +570. |
| "231.000 lekë, që do të thotë **30% më e lartë**" (§103) | 231.000 / 153.000 − 1 = **51,0%**; 1 − 153.000 / 231.000 = 33,8% | "30%" nuk përputhet me asnjë drejtim të raportit. |
| 152.700 + 78.300 = 231.000 (§21.3) | ✓ | Konsistente. |
| 52.000 / 152.700 = 34% (§21.1) | 34,05% ✓ | Konsistente. |
| Presidenti "afërsisht 65%" (§100) | 425.000 / 257.000 − 1 = 65,4% ✓ | Konsistente. |

**Origjina e 152.700 (c, e verifikuar me V35):** V35 **nuk e përmban** këtë shumë. Standardi i V35 është: paga për pozicion e klasës më të ulët të kategorisë I, të barasvlershme me drejtorin e DP në KM, plus paga në grup 14.000 (§§65, 71–76). Sipas këtij standardi:

| Momenti | Akti | I-b | R sipas V35 |
|---|---|---|---|
| 2016 (miratimi i L96) | VKM 545/2011 | 118.000 | **132.000** (V35 §76) |
| 1.1.2019 (zbatimi) | VKM 187/2017 | 129.800 | **143.800** (V35 §§77, 80) |
| 28.9.2022 (VKM 621/2022, para V35) | VKM 187 e ndryshuar | **138.700** | **152.700** (RIA e ligjit 33/2023; Raporti KEF, 22.5.2023) |

**E zgjidhur (c):** 152.700 është saktësisht standardi i V35 i aplikuar me vlerat në fuqi në datën e vendimit. VKM 621, datë 28.9.2022, e ngriti I-b nga 129.800 në 138.700 (+6,86%) dhe II-a nga 118.100 në 126.300 (+6,94%). Kopja e VKM 187 që kemi është e përditësuar vetëm deri te VKM 620/2022, prandaj nuk e tregonte. Si rrjedhojë, **152.700 është njëkohësisht dysheme juridike (V15 §95) dhe pikënisje e saktë metodologjikisht** për rritjet e §109. Pika P10 bie. Për krahasim, KLSH (2021) rekomandoi 132.100 = 118.100 + 14.000, duke përdorur II-a; V35 më pas e zhvendosi referencën te I-b.

**Pasoja:** vlera e saktë e R të paguar para dhe pas 1.4.2023 duhet marrë nga listëpagesat e KLGJ/KLP, jo nga teksti i vendimit. Gabimi është i vogël në vlerë (270 lekë/muaj), por prek bazën e prapambetjeve dhe besueshmërinë e çdo llogaritjeje që citon vendimin.

### 4.2 Seritë e R

Të gjitha vlerat janë lekë/muaj bruto, baza 2023; κ = R / 425.000.

| Seria | Përshkrimi | R | κ | Ndryshimi ndaj 152.700 | Statusi |
|---|---|---|---|---|---|
| R0 | Zbatimi i gabuar 2019–2021 | 118.100 | 0,278 | −22,7% | (c) |
| R1 | Sipas KLSH 2021 | 132.100 | 0,311 | −13,5% | (c) |
| **R2** | **E drejtë e fituar (V35)** | **152.700** | 0,359 | — | (c), V35 i paverifikuar drejtpërdrejt |
| R3 | **E paguar faktikisht** nga 1.4.2023 (ligji 33/2023) | 153.000 | 0,360 | +0,2% | (c), para indeksimit të 2026 |
| R4 | L95/2026 | **161.500** | 0,380 | **+5,8%** | (c), nëse P nuk ka ndryshuar pas 2023 |
| K1 | Kundërfaktik: kategoria civile e formulës së vjetër (+44%) | 219.888 | 0,517 | +44,0% | (c) për burimin e 44%: II-a 2019 (118.100) → I-5 2023 (170.000) = +43,95%; (b) për përdorimin |
| K2 | Kundërfaktik i Shoqatës (kat. 1, kl. 1–3) | 204.700 | 0,482 | +34,1% | pretendim pale |
| K3 | Kundërfaktik i kërkuesit (referenca 2025) | 231.000 | 0,544 | +51,3% | pretendim pale |
| K4 | Ruajtja e raportit 0,594 me Presidentin | 252.519 | 0,594 | +65,4% | (c) aritmetikë; (b) si opsion |
| **RK** | **R e Këshillave (KLGJ 435, KLP 144), nga 1.8.2026** | **236.425** | 0,556 | +54,8% | (c) |
| RK′ | E njëjta referencë, 1.4.2023–31.12.2025 (I-2 = 217.000) | 231.000 | 0,544 | +51,3% | (c) VKM 325 orig.; VKM 337/2025 |

**Seria e INSTAT, e rindërtuar nga 31 botime tremujore (c), mesatare vjetore në lekë.** Kemi 41 tremujorë, nga I/2016 deri në II/2026. Ndarja sipas sektorit ekziston deri në IV/2024; nga 2025 INSTAT boton vetëm totalin. Botimet nuk kanë asnjë konflikt për tremujorët e përbashkët, përfshirë botimin e rishikuar T4/2023. Seria përputhet saktë me §99: sektori shtetëror 2016 = 54.488 dhe privati 2016 = 43.662 janë identike, ndërsa 2023 ndryshon nën 0,1%. Pra, Gjykata përdori pikërisht këto mesatare.

| Viti | Gjithsej | Sektori shtetëror | Sektori privat |
|---|---|---|---|
| 2016 | 47.511 | 54.488 | 43.662 |
| 2019 | 52.376 | 63.082 | 47.529 |
| 2022 | 61.884 | 70.083 | 58.194 |
| 2023 | 70.530 | 81.898 | 65.555 |
| 2024 | 77.456 | 92.043 | 71.162 |
| 2025 | 84.100 | — | — |
| I–II/2026 | 91.134 | — | — |

**Rritjet kryesore (c):**
- Sektori shtetëror: 2016→2024 **+68,9%**; 2019→2024 +45,9%; III/2022→IV/2024 +42,3%.
- Paga mesatare gjithsej: 2016→2025 +77,0%; III/2022→II/2026 **+49,6%**.
- R e magjistratëve: shtator 2022 (152.700) → L95 (161.500) **+5,8%**.

Paga minimale u rrit nga 40.000 në 50.000 lekë më 1.1.2026.

**Inflacioni (IÇK kombëtar, ECOICOP v2, INSTAT; c).** Seria mujore 2016-01 → 2026-08. Është validuar me burime të pavarura: dhjetor 2022 = 7,4% a/a, e njëjtë me MF; 2024 dhe 2025 = 2,2%, e njëjtë me INSTAT. Inflacioni mesatar vjetor: 2017 +2,0%; 2018 +2,0%; 2019 +1,4%; 2020 +1,7%; 2021 +2,0%; **2022 +6,7%; 2023 +4,8%**; 2024 +2,2%; 2025 +2,2%. Kulmi ishte në tetor 2022, 8,3% a/a. Inflacioni vjetor ishte **mbi tavanin 4% të L95 për 18 muaj rresht** (mars 2022 – shtator 2023).

| Periudha | IÇK (bazë) | IÇHK (kontroll) |
|---|---|---|
| Tetor 2016 (miratimi i L96) → gusht 2026 | +32,0% | +35,3% |
| Janar 2019 (zbatimi) → gusht 2026 | +24,1% | +25,4% |
| **Shtator 2022 (R = 152.700) → gusht 2026** | **+11,3%** | +12,2% |
| Prill 2023 (R = 153.000) → gusht 2026 | +7,6% | +7,6% |

**Testi i fuqisë blerëse (§§83–84; c për aritmetikën, b për pasojën).** Vlera e 152.700 lekëve të shtatorit 2022, në çmimet e gushtit 2026, është **170.015 lekë** sipas IÇK (171.371 sipas IÇHK). L95 jep 161.500, pra **5,0% nën vlerën reale të së drejtës së fituar** (V15 §95); sipas IÇHK, 5,8%. Edhe me indeksimin maksimal të lejuar nga L95 (+4%), R do të ishte 167.960, përsëri 1,2% nën vlerën reale. Pra, L95 dështon jo vetëm në testin relativ të §109, por edhe në testin absolut të ruajtjes së vlerës reale (§83). Ky dështim nuk varet nga leximi i korridorit (P2). R e Këshillave (236.425) është 39,1% mbi vlerën reale të 152.700. Skript: `faza1_hicp.py`; seritë: `faza1_ichk_mujor.csv` (bazë) dhe `faza1_hicp_mujor.csv` (kontroll). Skedari: `faza1_instat_pagat_tremujore.csv`.

Për krahasim, rritjet 2016–2023 sipas INSTAT, siç i citon Gjykata (§99): paga minimale +81,8%; paga mesatare në sektorin privat +50,2%; në sektorin shtetëror +50,3%; paga mesatare bruto +48,3%.

**Konstatim kryesor (b):** nëse §109 lexohet si korridor ndërmjet rritjes së dy referencave (K7), atëherë R e pranueshme në bazën 2023 ndodhet në **[219.888; 252.519] lekë**, pra κ ∈ [0,517; 0,594]. L95 jep **161.500 lekë (κ = 0,38)**. Kjo është **58.388 lekë/muaj nën kufirin e poshtëm** dhe +5,8% ndaj 2022, kundrejt +44% deri në +65% të referencave. Edhe me leximin më të butë (K2 e Shoqatës, +34%), L95 mbetet larg. Nëse ky lexim pranohet, L95 nuk duket se e përmbush K6. Ky është vlerësim paraprak dhe do të testohet në Fazën 2.

R e Këshillave (236.425; κ = 0,556) **bie brenda korridorit**. Ajo është gjithashtu kufiri i poshtëm natyror i "opsionit të parë" të §109, i cili e lidh R me ndryshimin e kategorisë civile.

**Burimi i "afërsisht 44%" (c dhe b):** shifra e §100 riprodhohet saktë nga rritja e pagës për pozicion II-a (118.100, vlera e zbatuar në 2019) → I-5 (170.000, nga 1.4.2023) = **+43,95%**. Pra, Gjykata mati rritjen e kategorisë që u zbatua *faktikisht* për magjistratët ("drejtor i DP", tani pozicion mbështetës I-5), jo të kategorisë së saktë sipas V35. Rritjet e krahasueshme sipas gjurmëve të tjera:

| Gjurma 2019 → 2023 (paga për pozicion) | Rritja |
|---|---|
| II-a → I-5 (gjurma e zbatuar faktikisht; "≈44%" e Gjykatës) | +43,95% |
| II-a → I-4 | +52,41% |
| I-b → I-2 (gjurma e saktë sipas V35) | +67,18% |
| I-b → I-2, me pagën në grup (143.800 → 231.000) | +60,64% |
| Shtator 2022 → 2023, me pagën në grup (152.700 → 231.000) | +51,28% |

**Pasoja (b):** kufiri i poshtëm i korridorit (+44%) është **konservativ**, sepse bazohet në gjurmën më të ulët. Rritja sipas gjurmës funksionale të V35 nga data e vendimit (+51,3%) bie brenda korridorit. Nga 2019 ajo është madje mbi rritjen e pagës së Presidentit (+65,4%).

### 4.2a Identifikimi i kategorisë referuese në VKM 325/2023 (c) dhe (b)

Formula e vitit 2016 referonte te "drejtori i drejtorisë së përgjithshme në Kryeministri ose çdo pozicion i barasvlershëm". Kalimi nga VKM 187/2017 te VKM 325/2023 e ndau këtë pozicion:

| VKM 187/2017 | Pozicionet | VKM 325/2023 | Paga për pozicion 2026 | R = + 14.000 |
|---|---|---|---|---|
| I-b | Sekretar i përgjithshëm në ministri; drejtor departamenti në KM; drejtor i DAP | **I-2** | 222.425 | **236.425** |
| II-a | "Drejtor i Drejtorisë së Përgjithshme" (titulli) | I-4 (DP përmbajtjeje) / I-5 (DP mbështetëse) | 184.500 / 174.250 | 198.500 / 188.250 |

- **Leximi funksional (KLGJ/KLP, b):** V35 konstatoi se referenca e saktë ishte kategoria e parë, klasa e tretë, pra niveli i pozicioneve I-b, dhe se zbatimi te II-a ishte pikërisht gabimi kushtetues (V15 §§37, 40–41). Ekuivalenti i I-b në strukturën e re është I-2. **Ky lexim është më konsistent me V35 dhe V15.**
- **Leximi titullor (alternativë, b):** referenca te titulli "drejtor DP" (I-4) jep R = 198.500. Ky lexim riprodhon logjikën e zbatimit të gabuar të viteve 2019–2021 dhe bie nën korridor (198.500 < 219.888). Duhet njohur si argument i mundshëm i Qeverisë, por është i dobët.
- **Leximi "klasa më e ulët e kategorisë I" (b):** V35 §65 e përshkruan referencën si "pozicionimi më i ulët brenda nivelit më të lartë". Në VKM 545 dhe VKM 187 klasa më e ulët e kategorisë I (I-b) dhe pozicionet e barasvlershme me drejtorin e DP përputheshin. Në VKM 325 ato ndahen: klasa më e ulët është **I-5** (174.250 + 14.000 = 188.250; κ = 0,443), ndërsa pozicionet e barasvlershme janë në I-2. Ky lexim bie gjithashtu nën korridor.

| Leximi i standardit të V35 në VKM 325 | R 2026 | κ | Brenda korridorit të §109? |
|---|---|---|---|
| Pozicionet e barasvlershme me I-b → I-2 (KLGJ/KLP) | 236.425 | 0,556 | **Po** |
| Titulli "drejtor DP përmbajtjeje" → I-4 | 198.500 | 0,467 | Jo |
| Klasa më e ulët e kategorisë I → I-5 | 188.250 | 0,443 | Jo |

**Përfundim (b):** vetëm leximi i Këshillave është i pajtueshëm njëkohësisht me V35 (barasvlershmëria funksionale, §§72, 76) dhe me V15 (korridori i §109). Dy leximet e tjera, që ulin referencën, përsërisin mekanizmin e uljes që të dy vendimet e dënuan. Gjykata gjithashtu theksoi se "është akti nënligjor që duhet të ndjekë konceptet e ligjit dhe jo anasjelltas" (V35 §84), pra një riorganizim i klasave me VKM nuk mund ta ulë referencën.

**Precedent për veprimin administrativ të Këshillave (c):** V35 §78 vëren, pa e kritikuar, se pas raportit të KLSH-së "disa organe kushtetuese administrativisht kanë kryer rillogaritjen e pagave", ndërsa të tjera vepruan sipas vendimeve gjyqësore të formës së prerë.

Indeksimi i pagave civile në 2026 ishte **2,50% saktësisht** (217.000 × 1,025 = 222.425). Kjo është e dhënë e vlefshme për rregullin e indeksimit në Fazën 2.

### 4.3 Struktura e pagës totale (c)

Nga nenet 2/j, 12/3, 12/5 dhe 14 të L96:

W = R · [ (1 + γ_G) · (1 + λ + δ) + 0,02 · min(y, 25) ]

ku γ_G ∈ {0,90; 0,98; 1,06} për G1, G2 dhe G3; λ ∈ {0; 0,05; 0,10} është shtesa për pozicion drejtues; δ = 0,80 për GJKKO/SPAK, përndryshe 0; y janë vitet e vjetërsisë.

**Validimi me të dhëna reale (c):** tabela e KLSH-së për pagat e GJL (raporti i shkurtit 2023, f. 34) jep pagat totale të gjashtë profileve. Me R = 118.100, formula riprodhon **të gjashtë rreshtat me devijim maksimal 1 lekë** (rrumbullakim):

| Profili (KLSH) | W sipas KLSH | W sipas modelit |
|---|---|---|
| Kryetar, 15 vjet | 303.044 | 303.045 |
| Kryetar, 25 vjet | 326.664 | 326.665 |
| Zv/kryetar, 15 vjet | 290.880 | 290.880 |
| Zv/kryetar, 25 vjet | 314.500 | 314.500 |
| Gjyqtar nga magjistratët, 25 vjet | 302.336 | 302.336 |
| Gjyqtar nga juristët, 15 vjet | 278.716 | 278.716 |

Dy konstatime anësore: (i) në periudhën e audituar GJL ende paguante R = 118.100, pra vlerën e zbatimit të gabuar; (ii) shtesa për vështirësi e gjyqtarëve që vinin nga gjykatat e posaçme rezulton **60%** e pagës bruto fillestare, jo 80% si në ligj. Kjo duhet verifikuar, por nuk prek R.

**Pasoja për modelin:** W është **lineare në R**. Çdo ndryshim relativ i R përcillet njësoj në pagën totale të çdo magjistrati, dhe raportet e brendshme të hierarkisë (K14) mbeten të pandryshuara. Kështu i jepet përgjigje kritikës së pakicës (§9) se analiza ndalet vetëm te R: për çdo kategori, ndryshimi i R ka efekt proporcional mbi W.

### 4.4 Prapambetjet: shembuj për një magjistrat (d)

**Skema e Këshillave, me seri të verifikuar (c):** 1.4.2023–31.12.2025 me R = 231.000 (33 muaj); 1.1.2026–31.7.2026 me R = 236.425 (7 muaj); kundrejt R = 153.000 të paguar. Shifrat janë bruto, pa interes dhe pa indeksimin eventual të R në 2026.

| Profili | Prapambetje 4.2023–7.2026 sipas Këshillave |
|---|---|
| G1, 5 vjet | 6.315.950 |
| G2, 15 vjet | 7.200.183 |
| G3, 25 vjet, kryetar | 8.734.959 |
| G2, 10 vjet, GJKKO/SPAK | 11.886.618 |

**Skenarë krahasues:** periudha 1.4.2023–30.9.2026, 42 muaj. Baza: R3 = 153.000 e paguar. Vlerat janë bruto, pa interes dhe pa indeksimin e 2026.

| Profili | Sipas L95 (R4) | Sipas K1 (+44%) | Sipas K4 (raporti 0,594) |
|---|---|---|---|
| G1, 5 vjet | 714.000 | 5.618.592 | 8.359.634 |
| G2, 15 vjet | 813.960 | 6.405.195 | 9.529.983 |
| G3, 25 vjet, kryetar | 987.462 | 7.770.513 | 11.561.374 |
| G2, 10 vjet, GJKKO/SPAK | 1.343.748 | 10.574.190 | 15.732.832 |

### 4.5 Kalibrimi fiskal pa N (d)

N mungon, por kostoja agregate mund të kalibrohet nga dy burime të pavarura. Përdor "njësi-R" = Σ (W_i / R), që është kostoja mujore e sistemit për çdo 1 lekë rritje të R.

| Burimi | Shifra | Njësi-R të nënkuptuara |
|---|---|---|
| Shoqata (V15 §21.4): 3,70 mld lekë/vit për 231.000 kundrejt 153.000 | pretendim pale | **3.954** |
| KM (KDNJMIP): prill–dhjetor 2023, rreth 260 mln për 0,38 kundrejt 0,36 | vlerësim qeveritar | 3.399 |
| KM: 2024–2025, rreth 740 mln | idem | 3.627 |
| KM: 2023–2026, rreth 1,5 mld | idem | **3.922** |
| KM: rreth 500 mln/vit në vazhdim | idem; përfshin shtesat e GJL që u hoqën më pas | 4.902 (mbivlerësim) |

Dy burime me interesa të kundërta **konvergojnë në rreth 3.900–4.000 njësi-R**. Kjo bazë mjafton për vlerësime të kushtëzuara në Fazën 2:

| Skenari | Baza 3.954 | Baza 4.902 |
|---|---|---|
| Kosto vjetore, R = 236.425 kundrejt 161.500 | **3,55 mld lekë/vit** | 4,41 mld |
| Prapambetje 4.2023–7.2026 sipas Këshillave | **12,5 mld lekë** | 15,5 mld |
| Prapambetje 4.2023–7.2026 sipas L95 | 1,34 mld lekë | 1,67 mld |

Burim i tretë (RIA 2023): 959 mln lekë/vit për kalimin te 153.000, përfshirë funksionarët e lidhur. Kjo jep 2.290–3.824 njësi-R, në varësi të bazës buxhetore të vitit 2023 (118.100, 126.300 ose 132.100), e cila nuk specifikohet. RIA ka edhe shifra të brendshme të papajtueshme (48,9 dhe 79,9 mln në tabelat 3- dhe 10-vjeçare). Pra, kufiri i poshtëm i bazës mund të jetë rreth 3.000. Skenarët e mësipërm janë konservativë nga ana e kostos.

Seria e prapambetjeve është tani e verifikuar: I-2 = 217.000 nga 1.4.2023 (VKM 325 origjinale, e pandryshuar nga VKM 337/2025) dhe 222.425 nga 1.1.2026 (VKM 131/2026).

Për krahasim (c, AN 2/2026): fondi i pagave i buxhetit të shtetit 2026 është 120,3 mld lekë; deficiti 63,7 mld; shpenzimet korrente të KLGJ 5,9 mld. Kosto vjetore prej 3,55 mld është rreth **3,0% e fondit të pagave të shtetit**. Kontributet e punëdhënësit janë rreth 16,6% e pagave në nivel agregat. Nuk dihet nëse bazat e mësipërme i përfshijnë.

---


### 4.6 Evidenca nga Thesari: si u paguan gushti dhe shtatori 2026 (c), me interpretim (b)

Pagat neto të paguara sipas muajit të pagës, në milionë lekë. Datat e ekzekutimit janë në kllapa.

| Institucioni | Korrik (4.8) | Gusht | Shtator (2–5.10) | Baza e pagës së gushtit sipas përshkrimit |
|---|---|---|---|---|
| Gjykata e Lartë | 23,41 | **26,15** (18.9) | 20,86 | Vendimi nr. 10878, 15.9.2026, i GJ. Adm. Shk. I Tiranë, "ekz. i menjëhershëm" |
| GJ. Adm. e Apelit Tiranë | 13,23 | **15,65** = 8,53 administrata (14.9) + 7,12 magjistratët (21.9) | 13,75 | Magjistratët: vendimi nr. 10902, 11.9.2026 |
| GJ. Adm. Shk. I Tiranë | 11,41 | **13,95** (17.9) | 11,62 | Vendimi 31154-01494-89-2026, 15.9.2026, "kërkesë për ekzekutim të menjëhershëm" |
| Aparati i PP | 18,81 | **23,93** = 7,62 administrata + 16,31 prokurorë/këshilltarë (17.9) | 19,11 | Prokurorët: vendimi nr. 10941, 15.9.2026 |
| KLP (aparati) | 8,79 | 8,64 = 5,52 administrata (17.9) + 3,12 anëtarë (22.9) | 8,76 | Anëtarët: "ligji nr. 96/2026 dt 18.09.2026" (sic, d.m.th. L95) |
| SPAK | 28,83 | 29,23 (2.9, në kohë) | 29,66 | Listëpagesë e zakonshme |
| Gjykata Kushtetuese | 14,20 | 13,63 (2.9, në kohë) | 13,95 | Listëpagesë e zakonshme |
| ILD | 12,13 | 11,85 (2–3.9) | 11,55 | Listëpagesë e zakonshme |

**Një rresht homogjen që lejon krahasim për frymë.** Te GJ. Adm. Shk. I Tiranë, rreshti "plan/fakt 104/20–23" përsëritet çdo muaj me të njëjtin grup prej 20–23 personash; me gjasë janë gjyqtarët (d). Paga neto për frymë:

| Muaji | Neto/frymë | Ndryshimi ndaj korrikut |
|---|---|---|
| Qershor | 157.625 | — |
| Korrik | 157.125 | — |
| **Gusht** (me vendim gjyqësor) | **222.228** | **+41,4%** |
| **Shtator** (pas L95) | **169.875** | +8,1% |

Për krahasim, raportet bruto të pritshme janë: 236.425 / 153.000 = 1,545 (+54,5%) dhe 161.500 / 153.000 = 1,056 (+5,6%). Tatimi progresiv dhe kontributet e kufizuara e ngushtojnë rritjen neto, prandaj +41% neto **përputhet në rend madhësie me R = 236.425**. Ndryshimet e numrit të personave dhe shtesat individuale e bëjnë krahasimin të përafërt. (b)

**Konstatime:**
1. **Pagat e gushtit të magjistratëve u paguan, me vonesë dhe në bazë të vendimeve të gjykatës administrative me ekzekutim të menjëhershëm**, në nivel që përputhet me R e Këshillave. Pretendimi në Kuvend se magjistratët ishin "dy muaj pa pagë" (KDNJMIP, 15.9) del i saktë vetëm për gushtin: korriku u pagua më 4.8 dhe gushti më 17–22.9. (c)
2. **Pagat e shtatorit, të paguara pas L95, u kthyen afër nivelit të vjetër.** Për grupin homogjen, kjo është **rënie nominale prej 23,6% neto nga gushti në shtator**. Nuk është më skenar hipotetik: është ulje faktike e pagës së paguar nga një muaj në tjetrin. Mbetet çështje juridike nëse pagesa e gushtit krijoi të drejtë të fituar, sepse varet nga natyra e vendimeve gjyqësore (masë e përkohshme apo vendim themeli), e cila nuk dihet (D16). (b)
3. **Zbatimi nuk ishte uniform.** SPAK, që ka edhe prokurorë, pagoi gushtin në kohë dhe pa rritje; nuk e zbatoi KLP 144. KLP pagoi anëtarët e vet sipas L95, pra nuk zbatoi vendimin e vet nr. 144 për gushtin. GJK dhe ILD nuk shfaqin ndryshim. (c)
4. **Gjykimet individuale për diferenca page janë fenomen i vazhdueshëm 2024–2026.** Në aparatin e PP: 0,6 / 15,9 / 42,7 mln lekë në 2024, 2025 dhe 2026 (2026 përfshin gushtin). Te GJ. Adm. Shk. I: rreth 98 / 118 / 105 mln lekë në të njëjtat vite (p.sh. "diferencë page shtator 2021–tetor 2024, vendim nr. 60 dt 20.11.2024"). Kjo e lidh P6 (prapambetjet 2019–2023) me një kosto gjyqësore që po paguhet tashmë, pjesë-pjesë. (c)
5. Korriku (4.8) në GJL është 13% mbi qershorin, pa shpjegim në përshkrim. Nuk ndikon në përfundimet e mësipërme.

**Kufizime të të dhënave të Thesarit (c, të konfirmuara edhe nga kontrolli i bisedës së mëparshme):**
- **598 grupe** kanë të njëjtin institucion, faturë, përfitues, datë dhe shumë, por kode ekonomike të ndryshme (kryesisht 6001001/6002001). Pa heqjen e tyre, raportet mujore dalin të paqëndrueshme. P.sh. për aparatin e PP, gushti/korriku del 0,73 pa heqje dhe 1,27 me heqje, sepse dyfishimi shfaqet në disa muaj dhe jo në të tjerë. Kjo tregon se janë kryesisht dyfishime raportimi, prandaj krahasimet mujore bëhen pas heqjes. Gjykata Administrative e Shkallës I Tiranë (raporti 1,22) **nuk preket** nga heqja; prandaj rreshti homogjen 104/20–23 mbetet prova më e fortë.
- Regjistri i importimit përmban 650 skedarë, nga 676 të deklaruar. 16 skedarë dështuan, përfshirë 12 ditë të marsit 2026, prandaj mbulimi i marsit 2026 është i pjesshëm. Mungesa e rreshtave nuk provon mungesë pagesash.
- Regjistrimi në Thesar nuk provon kreditimin individual. Shumat janë neto, jo bruto dhe jo kosto e punëdhënësit.

## 5. Konstatime paraprake për L95 kundrejt matricës

Vlerësimi i plotë bëhet në Fazën 2. Këtu jepen vetëm pikat që ndikojnë në projektim.

1. **K4/K6/K7:** κ = 0,38 jep +5,8%, ndërkohë që korridori i lexuar sipas (b) kërkon +44% deri në +65%. L95 ruan të njëjtën teknikë që Gjykata dënoi në §§93–96: koeficienti zgjidhet që të mbajë R afër vlerës nominale të mëparshme.
2. **K8:** L95 ruan referencën te paga e Presidentit, të cilën §108 e quan referencë që "ndryshon rrallë" dhe është "e pastrukturuar". §109 e lejon këtë opsion vetëm nëse ndjek *ndryshimin* që pësoi paga e Presidentit, ndërsa L95 ndjek nivelin e saj me koeficient më të ulët.
3. **K9:** L95 rimiraton tavanin e indeksimit (≤ target BSH + 1 p.p.). Gjykata **nuk e shfuqizoi** këtë fjali dhe në §106 e vlerësoi mekanizmin pozitivisht. Megjithatë, nëse inflacioni kalon tavanin, vlera reale bie, në tension me §§83–84 (P3).
4. **K12/K13:** L95 shtrin efektet nga 1.4.2023 (✓ formalisht), por nuk përmban "skemë përshtatjeje" për prapambetjet, kalendar pagese, apo trajtim të vonesës. U miratua pas afatit dhe pas vendimeve të KLGJ/KLP, të cilat nuk i adreson.
5. **K3:** nisma e deputetëve shmangu procedurën qeveritare të konsultimit. Dëgjesat u zhvilluan në ditën e votimit dhe asnjë vërejtje nuk u reflektua (§2, K3). Rreziku i kontestimit për K3 është i lartë.
6. **Neni 12/1:** ngrirja ligjore e kategorive të lidhura është zgjidhje e ligjshme për jo-magjistratët, por duhet verifikuar nëse përfshin magjistratë (P5).
7. **Ulja nominale:** nëse vendimet e Këshillave ishin të vlefshme, L95 e ul R nga 236.425 në 161.500 (−31,7%) për periudhën nga 1.8.2026. Kjo e kthen kontestin nga "ulje e fshehtë" në **ulje të hapur**. (b)
8. **Arsyetimi i nismëtarëve:** "llogaritje orientuese rreth 91 përqind e pagës së Presidentit" (KDNJMIP) duket se i referohet pagës totale të një profili, jo R. Kjo e zhvendos krahasimin nga R te W. Por, duke qenë se W është lineare në R (§4.3), kjo nuk e ndryshon krahasimin relativ me referencat e §109. (b)

---

## 6. Inventari i të dhënave dhe mungesave

| # | E dhëna | Burimi i pritshëm | Statusi | Cilat përfundime varen prej saj |
|---|---|---|---|---|
| D1 | Teksti i plotë i V35/2022 dhe llogaritja e 152.700 | Gjykata Kushtetuese; RIA 2023 | **✓** Të dyja të verifikuara (VKM 621/2022) | Baza R2 |
| D2 | Paga e Presidentit pas 1.4.2023 | Ligjet e buxhetit | **✓** 425.000 në 2024–2025 (ligjet 97/2023, 115/2024); 435.625 nga 1.1.2026 (ligji 87/2025 neni 13 + VKM 92/2026) | Vlera faktike e R4 |
| D3 | Akti dhe norma e indeksimit të parë të R (2026) | VKM | **✓** VKM 93/2026: +2,5% nga 1.1.2026 → 156.825 | R e paguar faktikisht, prapambetjet |
| D4 | Seria e pagës së kategorisë referuese civile 2019–2026 | VKM 187, 621/2022, 325/2023, 337/2025, 131/2026 | **✓** E plotë për I-b/I-2 dhe II-a/I-4/I-5 | Prapambetjet sipas nënperiudhave |
| D5 | Inflacioni 2016–2026 | INSTAT | **✓** IÇK kombëtare (ECOICOP v2) dhe IÇHK, mujore 2016-01 → 2026-08, të validuara me MF dhe me njoftimet e INSTAT | Testi K9 |
| D6 | Paga mesatare bruto 2016–2026 | INSTAT | **✓** 31 botime, I/2016–II/2026, pa konflikte. Ndarja shtetëror/privat deri IV/2024; 2025–2026 vetëm totali | Testi K11 |
| D7 | Targeti i inflacionit i BSH | BSH | **✓** 3%, i konfirmuar në 7 RPM (2025/I–2026/III). Brez toleruese ±1 p.p. nuk ekziston në asnjërin; "+1 p.p." i L95 është zgjedhje ligjore, jo parametër i BSH. Tavani i L95 = 4% | Tavani i indeksimit |
| D8 | Numri i magjistratëve sipas G1/G2/G3, vjetërsisë, pozicionit, GJKKO/SPAK | KLGJ, KLP | **Pjesërisht**: 417 pozicione gjyqtarësh (KLGJ 233/2025). Mungojnë prokurorët dhe shpërndarja sipas profilit | Kostoja kombëtare, prapambetjet totale |
| D9 | R e paguar faktikisht nga muaji në muaj, 2023–2026; **a u pagua 236.425 në gusht–shtator 2026** apo pagat u bllokuan | Listëpagesat KLGJ/KLP; Thesari | Mungon | Baza e prapambetjeve; nëse ka pasur ulje nominale faktike |
| D10 | Kategoritë e lidhura me pagën e magjistratit dhe numri i tyre | Ligji 115/2016, ligji 8577/2000 neni 17, ligje të tjera | **Pjesërisht ✓**: kategoritë në L115 dhe L8577 (shih §0); VKM 755 tregon se edhe KPK, KPA, Komisionerët, KQZ dhe Avokati i Popullit u trajtuan si të lidhura. Numrat mungojnë | Efekti zinxhir, neni 12/1 |
| D11 | Formula e pensionit suplementar | Ligji 8097/1996 | **Pjesërisht**: V35 shfuqizoi tavanin me pagën e Presidentit, prandaj pensioni ndjek pagën e muajit të fundit (V35 §§97–101); formula e plotë mungon | Kostoja afatgjatë |
| D17 | Shuma e diferencave sipas V35 të paguara deri tani (VKM 755/2023 e pasardhëse) | MF; KLGJ/KLP | **Pjesërisht ✓**: 1 mld lekë me VKM 755/2023 ("një pjesë"). Mungojnë aktet pasardhëse dhe shuma e mbetur | P6 |
| D12 | Norma e kontributeve të punëdhënësit | Legjislacioni i sigurimeve | Përafërsisht: 16,6% agregat (AN 2/2026) | Kostoja për buxhetin |
| D13 | Dokumentet parlamentare të L95 | Kuvendi | **Pjesërisht ✓**: dy raportet e komisioneve. Mungojnë: mendimi i plotë i KM, shkresat e KLGJ (3522/4, 3992, 3992/1), procesverbali i seancës plenare | K3; kostoja |
| D14 | Treguesit buxhetorë 2026–2028 | Ministria e Financave | **✓** AN 2/2026 (tabelat makro, buxhetet institucionale, punonjësit) | Analiza fiskale |
| D15 | Burimi i shumave 198.963 / 220.320 / 236.425 | — | 236.425 ✓ (KLGJ/KLP); 220.320 ✓ (153.000 × 1,44); 198.963 ✓ (mesi, punim i autorit, dytësor) | — |
| D16 | Vendimet e GJ. Adm. Shk. I Tiranë për pagat e gushtit (10878 = 31154-07804-80-2026; 10902; 10941; 31154-01494-89-2026); statusi i KLGJ 435 / KLP 144 pas L95; **kërkesa nr. 36/Sh** (e përmendur në materialet e mëparshme, me gjasë kontestim kushtetues i L95; teksti mungon, statusi i panjohur) | Gjykatat; GJK | Mungojnë tekstet. Punojmë me supozimin e autorit: masa sigurimi / ekzekutim i përkohshëm; pa revokim formal | P1 |

Faza 2 mund të nisë edhe pa D2–D14: modeli ndërtohet në mënyrë parametrike, dhe shembujt numerikë shënohen si të kushtëzuar. **D1 dhe D8 janë më me vlerë**: D1 për bazën juridike, D8 për koston.

---

## 7. Kontrolli i konsistencës (§12 i detyrës)

| # | Kontrolli | Rezultati |
|---|---|---|
| 1 | Asnjë rregull indeksimi nuk bie ndesh me mosregresionin | Nuk aplikohet ende (pa propozim). Tensioni i tavanit në L95 shënohet si P3. |
| 2 | Asnjë dysheme rrethore nga pika e mosmarrëveshjes | Nuk aplikohet ende. Korridori K7 ankorohet te ndryshimet e referencave, jo te pozicioni i palëve. ✓ |
| 3 | Pa numërim të dyfishtë të inflacionit | Korridori përdor rritje nominale të referencave 2022→2023, pa shtuar IÇK sipër tyre. ✓ |
| 4 | Çdo shifër në tekst përputhet me skedarin | ✓ (`faza1_rezultatet.csv`) |
| 5 | Argumentet e atribuuara Gjykatës janë nga shumica, në paragrafin e cituar | ✓. Pretendimet e palëve (§§17–21) dhe mendimi i pakicës janë shënuar veçmas. |
| 6 | Simbolet njëtrajtësisht | R, P, κ, W, γ, λ, δ, y. Fjalori i plotë jepet në Fazën 2. |

---

## 8. Përmbledhje e Fazës 1

### (i) Përfundimet kryesore

1. Vendimi nuk kërkon një shumë, por kërkon **rezultat**: riparim të uljes së fshehtë "në raport të drejtë me rritjet e tjera". Opsionet e lejuara janë të ankoruara te ndryshimi i kategorisë civile (~44%) ose i pagës së Presidentit (~65,4%), "brenda limiteve të tyre" (§109).
2. Paga totale është lineare në R, prandaj problemi matematikor reduktohet në zgjedhjen e R* dhe të rregullit të dinamikës së saj.
3. L95 jep R = 161.500 lekë (+5,8%). Nën leximin si korridor, kufiri i poshtëm është 219.888 lekë. R e Këshillave (236.425) bie brenda korridorit.
4. **Situata juridike nuk është më vakum, por konflikt aktesh.** KLGJ dhe KLP e trajtuan §110 si të vetë-ekzekutueshëm dhe caktuan R = 236.425 nga 1.8.2026. L95 erdhi më pas me R = 161.500 prapavepruese. Nëse aktet e Këshillave ishin të vlefshme, L95 sjell **ulje nominale 31,7%**.
5. Identifikimi i referencës nga Këshillat (I-2 si pasardhëse e I-b) është në përputhje me logjikën e V35. Leximi alternativ titullor (I-4, R = 198.500) riprodhon gabimin e viteve 2019–2021.
6. Konsultimi për L95 ka të njëjtat tipare që Gjykata i quajti joefektive në §98: dëgjesë në ditën e votimit, asnjë vërejtje e reflektuar.
7. Kostoja mund të kalibrohet pa N: dy burime me interesa të kundërta konvergojnë në rreth 3.950 njësi-R. Kjo jep rreth 3,55 mld lekë/vit për diferencën 236.425 kundrejt 161.500 (rreth 3% e fondit të pagave të shtetit) dhe rreth 12,5 mld lekë prapambetje sipas Këshillave.
8. Vendimi përmban mospërputhje aritmetike (570 vs 300; "30%" vs 51%). Shuma **152.700 tani është e verifikuar**: standardi i V35 me vlerat e VKM 621/2022 (138.700 + 14.000).
9. **Modeli linear W(R) validohet me të dhëna reale:** riprodhon 6 pagat e GJL të raportuara nga KLSH me devijim ≤ 1 lekë.
10. Nga tri leximet e mundshme të standardit të V35 në strukturën e VKM 325 (I-2, I-4, I-5), vetëm leximi i Këshillave (I-2) qëndron brenda korridorit të V15 §109.

11. **Seritë e referencës janë tani plotësisht të verifikuara** (VKM 187, 621/2022, 325/2023, 337/2025, 131/2026). "Afërsisht 44%" e Gjykatës korrespondon me gjurmën e zbatuar faktikisht (II-a → I-5). Prandaj kufiri i poshtëm i korridorit është konservativ.
12. **Thesari konfirmon (§4.6):** gushti 2026 u pagua me vendim gjyqësor në nivelin e Këshillave (+41% neto për frymë në grupin homogjen), shtatori sipas L95 (−23,6% neto nga gushti). Ulja nominale është tani fakt, jo hipotezë. SPAK, KLP (për anëtarët), GJK dhe ILD nuk e zbatuan nivelin e Këshillave.
13. **Testi i inflacionit:** 161.500 (L95 me P 2023) është 5,0% nën [**errata:** me P 2026, L95 = 165.537,5, pra 2,6% nën] vlerën reale të 152.700 (shtator 2022) në çmimet e gushtit 2026, sipas IÇK kombëtar (5,8% sipas IÇHK). L95 nuk e ruan as fuqinë blerëse të të drejtës së fituar, pavarësisht si lexohet korridori.

### (ii) Pikat interpretuese ku kërkohet vendimi juaj

- **P1 — Statusi i vendimeve të KLGJ 435 / KLP 144 kundrejt L95.** *Supozim pune i dhënë nga autori (7.10.2026; pa dokument):* vendimet 10878, 10902 dhe 10941 janë masa sigurimi ose ekzekutim i përkohshëm, jo vendime themeli. KLGJ dhe KLP nuk kanë revokuar formalisht aktet e tyre; Thesari zbaton 0,38 nga shtatori; kontestimi ka kaluar në rrugë kushtetuese. Pasoja: në skenarin A, gushti shërben si provë faktike e nivelit 236.425; në skenarin B, si masë procedurale e tejkaluar nga L95. Ky është tani pyetja qendrore. **E dhënë e re (§4.6):** gjykata administrative urdhëroi pagesën e gushtit me ekzekutim të menjëhershëm, dhe pagesa u krye në nivelin e Këshillave. Pastaj shtatori u pagua sipas L95, pra me rënie nominale faktike. Skenari A ka tani mbështetje faktike dhe gjyqësore (të paktën në shkallë të parë ose si masë e përkohshme). Propozoj **dy skenarë juridikë paralelë** në Fazën 2: (A) Këshillat zbatuan ligjërisht §110, prandaj L95 duhet të respektojë 236.425 si dysheme mosregresioni nga 1.8.2026; (B) Këshillat vepruan pa kompetencë, prandaj vlen vetëm testi i korridorit. Propozimi duhet të qëndrojë në të dy skenarët. Kjo arrihet me R* ≥ 236.425, që njëkohësisht mbyll konfliktin.
- **P2 — "Brenda limiteve të tyre."** Pranoni leximin si korridor [+44%; +65,4%]? (Edhe deputeti G. Bardhi e lexoi kështu në KDNJMIP.) Shënim: 44% vjen nga gjurma më e ulët (II-a → I-5), ndërsa gjurma e saktë sipas V35 jep +51,3% nga shtatori 2022.
- **P3 — Tavani i indeksimit.** Gjykata nuk e shfuqizoi tavanin dhe e vlerësoi mekanizmin pozitivisht (§106). Ta respektojmë si të dhënë, ta kufizojmë vetëm në kushtet e nenit 138/a, apo ta zëvendësojmë? E dhëna e re: pagat civile u indeksuan 2,5% në 2026.
- **P4 — Periudha e riparimit.** Vetëm 2023, apo edhe 2016/2019–2023? Unë e lexoj si të kufizuar te 2023.
- **P5 — Neni 12/1.** A futet në fushë ngrirja e kategorive të lidhura? Shënim: anëtarët e Këshillave paguhen si magjistratë G3, prandaj nuk duket se bien nën ngrirjen.
- **P6 — Prapambetjet 2019–2023.** Jashtë fushës apo shtojcë?
- **P7 — Objekti i propozimit.** Ndryshim i L95, apo model alternativ i plotë që e zëvendëson?
- **P8 — Referenca.** Paga e Presidentit si ankorë (e lejuar nga §109), referenca civile I-2 (e zbatuar nga Këshillat), apo referencë e dyfishtë?
- **P9 — Shuma 198.963.** E zgjidhur: mesi (236.425 + 161.500)/2 nga punimi i autorit në Academia.edu. Përdoret vetëm si alternativë krahasuese, me shënimin se bie nën korridor.

### Vendimet e autorit për pikat interpretuese (8.10.2026)

Autori pranoi parazgjedhjet e propozuara. Ato janë tani **zgjedhje të punimit**, të shënuara (b) ose (e), jo supozime të hapura:

| Pika | Vendimi |
|---|---|
| P1 | Supozimi i punës i autorit (masa sigurimi / ekzekutim i përkohshëm; pa revokim); dy skenarë paralelë A/B |
| P2 | Korridori [+44%; +65,4%] pranohet si lexim analitik (b) i §109, jo si rregull i shprehur i Gjykatës |
| P3 | Tavani 4% nuk vepron si tavan i indeksimit të zakonshëm; përdoret si shkas për rishikim të jashtëzakonshëm dhe lejohet si kufizim vetëm brenda mekanizmit të nenit 138/a |
| P4 | Riparimi nis nga 1.4.2023 (V15 §110) |
| P5 | Kategoritë e lidhura pa status magjistrati shkëputen nga R dhe ndjekin regjimin e indeksimit të kategorisë së tyre |
| P6 | Diferencat sipas V35 për 2019–2023 mbeten jashtë paketës, me rekomandim për inventar (D17) |
| P7 | Model alternativ i plotë, me L95 si një nga alternativat |
| P8 | Referenca: rrjeta civile (I-2 + 14.000) e kombinuar me IÇK |
| P9 | 198.963 vetëm si alternativë krahasuese |

### Korrigjime metodologjike që mbarten në Fazën 2

Këto janë korrigjimet e rishikimit të mëparshëm të skeletit të punimit, të pranuara si kufizime projektimi:
1. Kufijtë e korridorit (min/maks i referencave) janë **konstruksion analitik**, jo rregull i shprehur i Gjykatës. Çdo vlerë brenda tyre duhet arsyetuar juridikisht.
2. Baza e indeksimit nuk mund të jetë R e prodhuar nga formula e shfuqizuar (153.000). Fillimisht rindërtohet baza e riparuar nga 1.4.2023, pastaj modelohet dinamika.
3. Tavani buxhetor nuk është veto. Nëse fondi nuk mjafton, raportohet hendeku i financimit dhe mënyrat e mbulimit, jo ulja e garancisë.
4. R, W dhe prapambetjet modelohen veçmas. Operatori max{…} përdoret vetëm aty ku kuptimi juridik i secilit term është i qartë.
5. Variantet e indeksimit (mesatare, korridor, max(IÇK, referenca)) testohen për efektet kumulative; asnjë nuk etiketohet paraprakisht si kushtetues.
6. Nash përdoret vetëm nëse arsyetohen dobishmëritë, pika e mosmarrëveshjes dhe peshat. Pika e mosmarrëveshjes nuk mund të jetë një gjendje juridikisht e papranueshme. Mesi 198.963 trajtohet si alternativë krahasuese, jo si zgjidhje.
7. Pa Monte Carlo me shpërndarje të pambështetura. Përdoren skenarë transparentë.

### (iii) Të dhënat që mungojnë, sipas përparësisë

1. **D16** — tekstet e vendimeve të GJ. Adm. Shk. I Tiranë nr. 10878, 10902, 10941 dhe 31154-01494-89-2026 (11–15.9.2026): masë e përkohshme apo vendim themeli? Kjo vendos nëse pagesa e gushtit krijon dysheme mosregresioni. D9 tani është kryesisht përgjigjur nga Thesari (§4.6).
2. **D8** — numri i magjistratëve sipas profilit. Me kalibrimin e §4.5 kjo e dhënë nuk është më bllokuese.
3. **D13** — mendimi i plotë i KM për projektligjin (shpërndarja e kostos).
4. **D5–D7** — IÇK, paga mesatare, targeti i BSH.
