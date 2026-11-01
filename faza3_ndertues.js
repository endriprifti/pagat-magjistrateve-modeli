// Ndërton punimin .docx nga skedarët me shënjim të thjeshtë (faza3a_tekst.txt, faza3b_tekst.txt).
// Shënjimi:
//   #  Titull            -> titulli i punimit (qendër, kapitale)
//   @  Autor            -> rreshti i autorit
//   ## KREU             -> Heading 1 (kapitale)
//   ### Nënkreu         -> Heading 2
//   #### Pikë           -> Heading 3 (pjerrët)
//   > tekst             -> citim i ndarë (i futur, pjerrët)
//   $$ formulë          -> formulë e veçuar, në qendër
//   | a | b |           -> tabelë (rreshti i parë = kokë; rreshti |---| shpërfillet)
//   [[TOC]]             -> përmbajtja
//   [[PAGEBREAK]]       -> faqe e re
//   [[IMG: f.png | 15]] -> figurë PNG me gjerësi 15 cm
//   **x** *x*           -> theksim; [[fn: tekst]] -> fusnotë
// Përdorimi: node faza3_ndertues.js dalja.docx skedari1.txt [skedari2.txt ...]
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, FootnoteReferenceRun, PageNumber, Footer, TableOfContents,
  PageBreak, LevelFormat, ImageRun,
} = require("docx");

const [, , out, ...inputs] = process.argv;
const src = inputs.map((f) => fs.readFileSync(f, "utf8")).join("\n\n");
const FONT = "Times New Roman";
const footnotes = {};
let fnId = 0;

function inlineRuns(text, base = {}) {
  // ndan fusnotat, pastaj theksimet
  const runs = [];
  const parts = text.split(/(\[\[fn:[\s\S]*?\]\])/);
  for (const p of parts) {
    if (!p) continue;
    const m = p.match(/^\[\[fn:\s*([\s\S]*?)\]\]$/);
    if (m) {
      fnId += 1;
      footnotes[fnId] = { children: [new Paragraph({ children: emph(m[1].trim(), { size: 20 }),
        alignment: AlignmentType.JUSTIFIED, spacing: { after: 40 } })] };
      runs.push(new FootnoteReferenceRun(fnId));
    } else {
      runs.push(...emph(p, base));
    }
  }
  return runs;
}
function emph(text, base = {}) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) runs.push(new TextRun({ text: text.slice(last, m.index), font: FONT, ...base }));
    const t = m[0];
    if (t.startsWith("**")) runs.push(new TextRun({ text: t.slice(2, -2), bold: true, font: FONT, ...base }));
    else runs.push(new TextRun({ text: t.slice(1, -1), italics: true, font: FONT, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) runs.push(new TextRun({ text: text.slice(last), font: FONT, ...base }));
  return runs;
}

const CONTENT_W = 9026; // A4 me kufij 1 inç
function table(rows) {
  const cells = rows.filter((r) => !/^\|\s*:?-{2,}/.test(r)).map((r) =>
    r.replace(/^\|/, "").replace(/\|\s*$/, "").split("|").map((c) => c.trim()));
  const ncol = Math.max(...cells.map((r) => r.length));
  // gjerësi proporcionale me gjatësinë mesatare të tekstit, me minimum
  const len = Array.from({ length: ncol }, (_, j) =>
    Math.max(6, ...cells.map((r) => Math.min((r[j] || "").length, 60))));
  const tot = len.reduce((a, b) => a + b, 0);
  let widths = len.map((l) => Math.floor((CONTENT_W * l) / tot));
  // minimumi 700 DXA për kolonë; pjesa tjetër rishpërndahet proporcionalisht
  const MIN_W = 700, low = widths.map((w) => w < MIN_W);
  if (low.some(Boolean)) {
    const fixed = low.filter(Boolean).length * MIN_W;
    const restTot = widths.reduce((a, w, j) => a + (low[j] ? 0 : w), 0);
    widths = widths.map((w, j) => low[j] ? MIN_W : Math.floor(w * (CONTENT_W - fixed) / restTot));
  }
  widths[widths.length - 1] += CONTENT_W - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "808080" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: cells.map((r, i) => new TableRow({
      tableHeader: i === 0,
      children: Array.from({ length: ncol }, (_, j) => new TableCell({
        borders, width: { size: widths[j], type: WidthType.DXA },
        shading: i === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: "E7E6E6" } : undefined,
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
        children: [new Paragraph({ spacing: { after: 0 },
          children: inlineRuns(r[j] || "", { size: 18, bold: i === 0 ? true : undefined }) })],
      })),
    })),
  });
}

const body = [];
const lines = src.split(/\r?\n/);
let i = 0, para = [];
function flush() {
  if (!para.length) return;
  body.push(new Paragraph({ children: inlineRuns(para.join(" ")), alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 160, line: 312 }, indent: { firstLine: 0 } }));
  para = [];
}
while (i < lines.length) {
  const l = lines[i];
  if (/^\s*$/.test(l)) { flush(); i++; continue; }
  if (l.startsWith("|")) {
    flush(); const rows = [];
    while (i < lines.length && lines[i].startsWith("|")) rows.push(lines[i++]);
    body.push(table(rows)); body.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    continue;
  }
  if (l === "[[TOC]]") { flush(); body.push(new TableOfContents("PËRMBAJTJA", { hyperlink: true, headingStyleRange: "1-2" })); i++; continue; }
  if (l.startsWith("[[IMG:")) { flush();
    const [file, wcm] = l.slice(6, -2).split("|").map((x) => x.trim());
    const data = fs.readFileSync(file);
    const pxW = data.readUInt32BE(16), pxH = data.readUInt32BE(20);
    const w = Math.round(parseFloat(wcm) / 2.54 * 96), h = Math.round(w * pxH / pxW);
    body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, keepNext: true,
      children: [new ImageRun({ type: "png", data, transformation: { width: w, height: h },
        altText: { title: "Figura", description: file, name: file } })] })); i++; continue; }
  if (l === "[[PAGEBREAK]]") { flush(); body.push(new Paragraph({ children: [new PageBreak()] })); i++; continue; }
  if (l.startsWith("#### ")) { flush(); body.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: emph(l.slice(5)) })); i++; continue; }
  if (l.startsWith("### ")) { flush(); body.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: emph(l.slice(4)) })); i++; continue; }
  if (l.startsWith("## ")) { flush(); body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: emph(l.slice(3)) })); i++; continue; }
  if (l.startsWith("# ")) { flush(); body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1200, after: 360 },
    children: [new TextRun({ text: l.slice(2), bold: true, size: 30, font: FONT })] })); i++; continue; }
  if (l.startsWith("@ ")) { flush(); body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
    children: [new TextRun({ text: l.slice(2), bold: true, size: 24, font: FONT })] })); i++; continue; }
  if (l.startsWith("- ")) { flush(); body.push(new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 567, hanging: 283 },
    spacing: { after: 80, line: 276 }, children: inlineRuns("–\t" + l.slice(2), { size: 22 }) })); i++; continue; }
  if (l.startsWith("> ")) { flush(); body.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, indent: { left: 567, right: 567 },
    spacing: { after: 160, line: 276 }, children: inlineRuns(l.slice(2), { italics: true, size: 22 }) })); i++; continue; }
  if (l.startsWith("$$ ")) { flush(); body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 200 },
    children: [new TextRun({ text: l.slice(3), font: "Cambria Math", italics: true, size: 24 })] })); i++; continue; }
  para.push(l.trim()); i++;
}
flush();

const doc = new Document({
  creator: "Endri Prifti",
  title: "Paga e magjistratëve pas Vendimit me №15/2026",
  styles: {
    default: { document: { run: { font: FONT, size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 26, bold: true, allCaps: true }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, italics: true }, paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 2 } },
    ],
  },
  footnotes,
  features: { updateFields: true },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(out, b); console.log(`OK: ${out}, fusnota: ${fnId}`); });
