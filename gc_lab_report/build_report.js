// Builds GC_Fruit_Ester_PostLab_Report.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, ImageRun,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  Math: OMath, MathRun, MathFraction, MathSubScript, Footer, PageNumber,
} = require("docx");

const FONT = "Calibri";
const W = 9360; // content width (DXA), 1" margins on US Letter

// Text helpers ---------------------------------------------------------------
// Parse a string with [[placeholder]] (yellow highlight), _{sub}, ^{sup}, *italic*
function runs(text, base = {}) {
  const out = [];
  const re = /(\[\[[^\]]+\]\]|_\{[^}]+\}|\^\{[^}]+\}|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("[[")) out.push(new TextRun({ text: "[" + t.slice(2, -2) + "]", highlight: "yellow", ...base }));
    else if (t.startsWith("_{")) out.push(new TextRun({ text: t.slice(2, -1), subScript: true, ...base }));
    else if (t.startsWith("^{")) out.push(new TextRun({ text: t.slice(2, -1), superScript: true, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const P = (text, opts = {}) => new Paragraph({ children: runs(text), spacing: { after: 160, line: 276 }, alignment: AlignmentType.JUSTIFIED, ...opts });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const caption = (label, text) => new Paragraph({
  alignment: label ? AlignmentType.LEFT : AlignmentType.CENTER, spacing: { before: 60, after: label ? 200 : 100 },
  children: [...(label ? [new TextRun({ text: label + " ", bold: true, size: 20 })] : []), ...runs(text, { size: 20, italics: !label })],
});
const tableTitle = (label, text) => new Paragraph({
  keepNext: true, spacing: { before: 120, after: 80 },
  children: [new TextRun({ text: label + " ", bold: true, size: 20 }), ...runs(text, { size: 20 })],
});
function image(path, widthIn) {
  const buf = fs.readFileSync(path);
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const px = widthIn * 96;
  return new Paragraph({
    alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 80, after: 40 },
    children: [new ImageRun({ type: "png", data: buf, transformation: { width: px, height: px * h / w } })],
  });
}

// Tables ---------------------------------------------------------------------
const border = { style: BorderStyle.SINGLE, size: 4, color: "808080" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, rows, { header = true } = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    alignment: AlignmentType.CENTER,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: header && i === 0,
      children: r.map((cell, j) => new TableCell({
        borders, width: { size: widths[j], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        shading: header && i === 0 ? { type: ShadingType.CLEAR, fill: "D9E2F3", color: "auto" } : undefined,
        children: [new Paragraph({
          alignment: j === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
          children: runs(String(cell), { size: 20, bold: header && i === 0 }),
        })],
      })),
    })),
  });
}
const spacer = () => new Paragraph({ spacing: { after: 120 }, children: [] });

// Equations (native Word equations) -----------------------------------------
const mr = (t) => new MathRun(t);
const sub = (b, s) => new MathSubScript({ children: [mr(b)], subScript: [mr(s)] });
const eqPara = (children, num) => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 120, after: 160 },
  children: [new OMath({ children }), new TextRun({ text: `\t(${num})` })],
});

const eqSM = eqPara([
  mr("% starting material = "),
  new MathFraction({
    numerator: [sub("A", "alcohol"), mr(" + "), sub("A", "acetic acid")],
    denominator: [sub("A", "total")],
  }),
  mr(" × 100"),
], 1);
const eqDensity = eqPara([
  mr("ρ = "), new MathFraction({ numerator: [mr("m")], denominator: [mr("V")] }),
], 2);

// Document content -------------------------------------------------------------
const children = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "Identifying an Unknown Fruity Ester by Gas Chromatography", bold: true, size: 32 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: runs("[[Your Name]] · Lab partners: [[names]] · Group [[#]]") }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: runs("[[Course / Section]] · [[Date]] · Unknown alcohol code: [[code]]") }),

  // ------------------------------------------------------------------ INTRO
  H1("Introduction"),
  P("Esters are responsible for many of the characteristic aromas of fruits, from the pear-like note of ethyl acetate to the banana scent of isopentyl acetate. The purpose of this experiment was to synthesize an ester from an unknown alcohol and acetic acid and then determine its identity using gas chromatography together with physical-property measurements. The research question was: *What is the identity of the selected unknown ester compound?*"),
  P("The ester was prepared by Fischer esterification, an acid-catalyzed condensation in which a carboxylic acid and an alcohol combine to form an ester and water. Concentrated sulfuric acid protonates the carbonyl oxygen of acetic acid, making the carbonyl carbon more electrophilic so that the alcohol oxygen can attack it; after proton transfers, water is lost and the ester is formed. Because the reaction is an equilibrium, acetic acid was used in excess to push the reaction toward the product, and the mixture was heated at about 70 °C to increase the rate. Magnesium sulfate was then added as a drying agent to remove water before analysis. Since every candidate ester comes from the same acid, the identity of the ester depends only on which alcohol was used, so identifying the product also identifies the unknown alcohol."),
  P("Gas chromatography (GC) was the key analytical technique. A very small liquid sample (0.2 µL) is injected into a heated port, vaporized, and carried by a carrier gas (the mobile phase) through a long column lined with a stationary phase. Each compound partitions between the gas and the stationary phase; compounds that are more volatile and interact less with the stationary phase spend more time in the gas and reach the detector sooner. Each component therefore appears as a peak at a characteristic retention time, and the area under the peak is proportional to the amount of that component in the mixture. Using a temperature ramp (30 °C to 130 °C at 5 °C/min) allows low-boiling compounds to separate at the start of the run while still eluting higher-boiling compounds before the run ends. In this experiment, GC answers the research question in two ways: the retention time of the main product peak, compared with the predicted elution order and with chromatograms of known esters, indicates which ester was formed, and the relative peak areas show how much unreacted starting material remains. Measurements of density and fragrance were used as independent physical evidence to support the GC assignment."),

  H2("Model of Predicted Elution Order"),
  P("Five esters are possible, one for each alcohol in the reagent set, and each is formed by joining the alcohol oxygen to the carbonyl carbon of acetic acid with loss of water (Figure 1): methyl acetate (Ester 1), ethyl acetate (Ester 2), n-butyl acetate (Ester 3), isobutyl acetate (Ester 4), and isopentyl acetate (Ester 5)."),
  image("figures/rxn_ester1.png", 4.2), caption("", "Ester 1: acetic acid + methanol → methyl acetate + water"),
  image("figures/rxn_ester2.png", 4.6), caption("", "Ester 2: acetic acid + ethanol → ethyl acetate + water"),
  image("figures/rxn_ester3.png", 4.8), caption("", "Ester 3: acetic acid + 1-butanol → n-butyl acetate + water"),
  image("figures/rxn_ester4.png", 4.9), caption("", "Ester 4: acetic acid + isobutanol → isobutyl acetate + water"),
  image("figures/rxn_ester5.png", 4.8),
  caption("Figure 1.", "Balanced Fischer esterification reactions (H_{2}SO_{4} catalyst, ~70 °C) for the five possible ester products. Ester 5: acetic acid + isopentanol → isopentyl acetate + water. Each reaction is balanced 1:1:1:1."),

  P("Elution order in GC follows volatility, so the model was built by predicting the relative boiling points of the products from the reactant data in the lab manual. Two structural factors were used. First, boiling point increases with molar mass because larger molecules have more surface area and stronger London dispersion forces. Each ester has the mass of its alcohol plus 42 g/mol (the acetyl group, C_{2}H_{2}O), so the esters keep the same mass order as their parent alcohols: methyl acetate (74 g/mol) < ethyl acetate (88 g/mol) < n-butyl acetate = isobutyl acetate (116 g/mol) < isopentyl acetate (130 g/mol). Second, branching lowers the boiling point at constant mass because branched molecules are more compact and have less contact between neighbors. This effect is seen in the reactants, where isobutanol boils at 107.9 °C compared with 117.3 °C for 1-butanol, so isobutyl acetate was predicted to boil below, and elute before, its unbranched isomer n-butyl acetate."),
  P("Polarity was also considered. The alcohols and acetic acid contain O–H groups and can hydrogen bond with each other, which raises their boiling points well above what their mass alone would suggest. Esters have polar C=O and C–O bonds but no O–H bond, so they cannot act as hydrogen-bond donors. As a result, converting an alcohol into its ester removes hydrogen bonding at the same time as it adds mass. For the small alcohols, the loss of hydrogen bonding is expected to dominate, so methyl acetate should boil at or below methanol and ethyl acetate should be close to ethanol. For the larger alcohols, the added mass dominates, so butyl, isobutyl, and isopentyl acetate should boil above their parent alcohols. The predicted relative properties are summarized in Table 1 and shown as a model chromatogram in Figure 2."),

  tableTitle("Table 1.", "Predicted relative boiling points and densities of the five possible esters (1 = lowest)."),
  table([2400, 1392, 1392, 1392, 1392, 1392], [
    ["Property", "Ester 1 methyl acetate", "Ester 2 ethyl acetate", "Ester 3 n-butyl acetate", "Ester 4 isobutyl acetate", "Ester 5 isopentyl acetate"],
    ["Relative boiling point", "1", "2", "4", "3", "5"],
    ["Predicted elution order", "1st", "2nd", "4th", "3rd", "5th"],
    ["Relative density", "5 (highest)", "4", "3", "1–2", "1–2"],
  ]),
  spacer(),
  P("Density was predicted to decrease as the alkyl chain grows. The ester group (two oxygen atoms) is the dense part of each molecule, and it makes up a larger fraction of the mass in a small ester such as methyl acetate than in a large one such as isopentyl acetate. All esters were predicted to be denser than their parent alcohols (about 0.79–0.81 g/mL) but less dense than acetic acid (1.05 g/mL). Branched esters were expected to pack slightly less efficiently than n-butyl acetate and so be slightly less dense."),
  image("figures/model_chromatogram.png", 6.2),
  caption("Figure 2.", "Model chromatogram showing the predicted elution order of the five possible esters (solid peaks) and the expected positions of the starting materials (dashed lines). Positions are based on the relative boiling points of the compounds and are qualitative, not measured retention times."),

  H2("Hypothesis"),
  P("(1) If the unknown alcohol is one of methanol, ethanol, 1-butanol, isobutanol, or isopentanol, then reaction with acetic acid will produce the corresponding acetate ester (methyl, ethyl, n-butyl, isobutyl, or isopentyl acetate), and the product chromatogram will show one major peak at the retention time expected for that ester. (2) If GC separation is controlled mainly by boiling point, then the esters will elute in the order methyl acetate < ethyl acetate < isobutyl acetate < n-butyl acetate < isopentyl acetate. Relative to the reactants, methyl acetate is expected to elute before methanol and ethyl acetate to elute very close to ethanol, while the three larger esters are expected to elute after their parent alcohols. Because excess acetic acid was used, a smaller acetic acid peak (boiling point 118 °C) is also expected, appearing after the small esters but close to isobutyl acetate and 1-butanol, and before n-butyl and isopentyl acetate."),

  // ------------------------------------------------------------------ DATA
  H1("Data and Results"),
  P("The gas chromatogram of the product sample, plotted in Excel from the exported Mini GC data, is shown in Figure 3. Retention times and peak areas for each peak are listed in Table 2."),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 200 }, border: { top: border, bottom: border, left: border, right: border },
    children: runs("[[Paste the Excel chromatogram here: GC_ester_data.xlsx → Chromatogram sheet]]") }),
  caption("Figure 3.", "Gas chromatogram of the unknown ester product (0.2 µL injection; 30 °C to 130 °C at 5 °C/min; 13 kPa). Peaks are labeled with their assignments."),

  tableTitle("Table 2.", "Retention times, peak areas, and assignments for the product sample chromatogram."),
  table([1000, 2000, 1800, 1760, 2800], [
    ["Peak", "Retention time (min)", "Peak area", "% of total area", "Assignment"],
    ["1", "[[ ]]", "[[ ]]", "[[ ]]", "[[e.g., unknown ester product]]"],
    ["2", "[[ ]]", "[[ ]]", "[[ ]]", "[[e.g., acetic acid (starting material)]]"],
    ["3", "[[ ]]", "[[ ]]", "[[ ]]", "[[e.g., unreacted alcohol]]"],
    ["Total", "", "[[ ]]", "100.0", ""],
  ]),
  spacer(),
  P("The percentage of starting material remaining in the product sample was calculated by dividing the combined area of the starting-material peaks (unreacted alcohol and acetic acid) by the total area of all peaks (Equation 1)."),
  eqSM,
  P("% starting material = ([[alcohol area]] + [[acetic acid area]]) / [[total area]] × 100 = [[ ]]%", { alignment: AlignmentType.CENTER }),
  P("The density of the product sample was measured in three trials by pipetting approximately 0.2 mL into a tared container and recording the mass (Equation 2; Table 3). Observations from Part A and Part D are summarized in Table 4."),
  eqDensity,
  tableTitle("Table 3.", "Density of the product sample."),
  table([1400, 2400, 2400, 3160], [
    ["Trial", "Volume (mL)", "Mass (g)", "Density (g/mL)"],
    ["1", "[[ ]]", "[[ ]]", "[[ ]]"],
    ["2", "[[ ]]", "[[ ]]", "[[ ]]"],
    ["3", "[[ ]]", "[[ ]]", "[[ ]]"],
    ["Mean ± SD", "", "", "[[ ]] ± [[ ]]"],
  ]),
  spacer(),
  tableTitle("Table 4.", "Qualitative observations of the product sample."),
  table([3000, 6360], [
    ["Observation", "Result"],
    ["Unknown alcohol code", "[[ ]]"],
    ["On adding H_{2}SO_{4} (Part A)", "[[e.g., slight warming, no color change]]"],
    ["Appearance after heating and drying", "[[e.g., clear, colorless liquid]]"],
    ["Fragrance (Part D)", "[[e.g., sweet, banana-like with a faint vinegar note]]"],
    ["Mean density", "[[ ]] g/mL"],
  ]),
  spacer(),

  // ------------------------------------------------------------------ DISCUSSION
  H1("Discussion"),
  P("The chromatogram of the product sample (Figure 3) shows a major peak at [[ ]] min that accounts for [[ ]]% of the total peak area, which is assigned to the ester product. When this retention time is compared with the overlaid chromatograms of the known esters provided in the lab, it matches [[ester name]], which eluted at [[ ]] min, and does not match the other four esters, which eluted at [[ ]], [[ ]], [[ ]], and [[ ]] min. The position of the peak is also consistent with the model chromatogram (Figure 2), in which [[ester name]] was predicted to be the [[1st/2nd/3rd/4th/5th]] ester to elute. The smaller peaks at [[ ]] min and [[ ]] min are assigned to unreacted [[alcohol]] and acetic acid. Using Equation 1, these starting materials made up [[ ]]% of the sample, meaning the product was mostly ester but not pure. Some leftover acetic acid was expected because it was used in excess and because Fischer esterification is an equilibrium that does not go to completion in 20 minutes. It should also be noted that the Mini GC detector does not respond equally to every compound, so the area percentages are approximate rather than exact mole percentages."),
  P("The physical-property observations support the GC assignment. The product had a [[describe]] odor, which matches the reported [[banana / pear / solvent-like / etc.]] scent of [[ester name]] (Table 5). The measured density was [[ ]] ± [[ ]] g/mL, compared with the literature value of [[ ]] g/mL, a [[ ]]% difference. [[Choose: The measured density is slightly higher than the literature value, which is consistent with the presence of residual acetic acid (1.05 g/mL) and traces of water / The measured density agrees closely with the literature value.]] Because density varies only slightly among the esters (0.876–0.932 g/mL), density alone could not distinguish between them, but it helps rule out [[e.g., methyl acetate, whose density is noticeably higher]] and is consistent with the GC result."),
  tableTitle("Table 5.", "Literature properties of the five candidate esters used for comparison."),
  table([2160, 1400, 1300, 1300, 1300, 1900], [
    ["Ester", "Formula", "Molar mass (g/mol)", "Boiling point (°C)", "Density (g/mL)", "Odor"],
    ["Methyl acetate", "C_{3}H_{6}O_{2}", "74.08", "57", "0.932", "Sweet, solvent/glue-like"],
    ["Ethyl acetate", "C_{4}H_{8}O_{2}", "88.11", "77", "0.902", "Nail-polish remover, pear"],
    ["n-Butyl acetate", "C_{6}H_{12}O_{2}", "116.16", "126", "0.882", "Sweet, apple/banana"],
    ["Isobutyl acetate", "C_{6}H_{12}O_{2}", "116.16", "117", "0.875", "Fruity, pear/raspberry"],
    ["Isopentyl acetate", "C_{7}H_{14}O_{2}", "130.19", "142", "0.876", "Strong banana"],
  ]),
  spacer(),
  P("Taken together, the evidence indicates that the unknown alcohol was [[alcohol name]] and that it reacted with acetic acid according to the balanced reaction below (Figure 4). In this condensation, the alcohol loses the hydrogen from its O–H group and acetic acid loses its –OH group; these combine to form water, and the alcohol oxygen bonds to the carbonyl carbon of the acid to form the ester. One molecule of each reactant gives one molecule of ester and one of water, so the reaction is balanced with all coefficients equal to 1."),
  P("CH_{3}COOH + R–OH ⇌ CH_{3}COOR + H_{2}O   (H_{2}SO_{4}, 70 °C)", { alignment: AlignmentType.CENTER }),
  P("[[Replace R with your alkyl group, e.g., isopentyl: R = CH2CH2CH(CH3)2]]", { alignment: AlignmentType.CENTER }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 }, border: { top: border, bottom: border, left: border, right: border },
    children: runs("[[Copy the matching reaction image from Figure 1 here (rxn_esterX.png)]]") }),
  caption("Figure 4.", "Balanced Fischer esterification of [[alcohol name]] with acetic acid to form [[ester name]]."),
  P("The properties of these reactants agree with the predictions of the initial model. [[Alcohol name]] has a molar mass of [[ ]] g/mol and a boiling point of [[ ]] °C, placing it [[relative position]] among the five alcohols. Adding the acetyl group raises the molar mass of the product to [[ ]] g/mol, and the model therefore predicted that [[ester name]] would elute [[1st–5th]] among the esters, [[before/after]] its parent alcohol. The observed chromatogram followed this prediction: the ester peak appeared at [[ ]] min, [[before/after]] the remaining [[alcohol]] peak at [[ ]] min, and [[before/after]] the acetic acid peak at [[ ]] min. [[If relevant: The model correctly predicted that the branched isomer isobutyl acetate elutes before the straight-chain n-butyl acetate because branching reduces surface contact and dispersion forces.]] [[If any order differed from the model, explain why, e.g., interactions with the stationary phase or peak overlap between compounds with similar boiling points such as acetic acid and 1-butanol.]] The measured density of [[ ]] g/mL also falls between that of the parent alcohol and acetic acid, as predicted for an ester."),

  // ------------------------------------------------------------------ CONCLUSION
  H1("Conclusion"),
  P("The unknown ester synthesized in this experiment was identified as [[ester name]], formed from [[alcohol name]] and acetic acid. This conclusion is supported by three independent lines of evidence. First, the major chromatogram peak at [[ ]] min matched the retention time of the [[ester name]] standard and its position agreed with the elution order predicted by the boiling-point model. Second, the product had a [[ ]] odor characteristic of [[ester name]]. Third, the measured density of [[ ]] g/mL was close to the literature value of [[ ]] g/mL, with the small difference explained by residual acetic acid. The sample still contained about [[ ]]% unreacted starting material, so the product was mostly but not completely converted; extracting the crude product with aqueous sodium bicarbonate to remove the excess acid would give a purer sample and a more accurate density in future experiments."),
];

const doc = new Document({
  creator: "", title: "Gas Chromatography of Fruit Esters - Post-lab Report",
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 28, bold: true, color: "1F3864" },
        paragraph: { spacing: { before: 280, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true, color: "2F5496" },
        paragraph: { spacing: { before: 200, after: 100 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync("GC_Fruit_Ester_PostLab_Report.docx", b);
  console.log("written");
});
