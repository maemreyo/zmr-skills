import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const COLORS = {
  navy: "#17324D",
  terracotta: "#B85435",
  teal: "#2B746F",
  sand: "#F4EEE4",
  mist: "#DCEAF2",
  charcoal: "#202B33",
  white: "#FFFFFF",
};

function addText(slide, name, text, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: "Arial",
    color: COLORS.charcoal,
    fontSize: 24,
    autoFit: "shrinkText",
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
    ...style,
  };
  return shape;
}

function addRect(slide, name, position, fill, radius = "none", lineFill = "none") {
  return slide.shapes.add({
    geometry: radius === "none" ? "rect" : "roundRect",
    name,
    position,
    fill,
    line: { style: "solid", fill: lineFill, width: lineFill === "none" ? 0 : 2 },
    ...(radius === "none" ? {} : { borderRadius: radius }),
  });
}

function addBrand(slide, slideNumber, audience = "CLASSROOM") {
  addText(slide, `wordmark-${slideNumber}`, "zamery", { left: 72, top: 32, width: 150, height: 30 }, {
    fontSize: 20,
    bold: true,
    color: COLORS.navy,
  });
  addText(slide, `tagline-${slideNumber}`, "rooted in strength", { left: 176, top: 35, width: 170, height: 24 }, {
    fontSize: 12,
    italic: true,
    color: COLORS.terracotta,
  });
  addText(slide, `audience-${slideNumber}`, audience, { left: 1000, top: 36, width: 208, height: 24 }, {
    fontSize: 12,
    bold: true,
    alignment: "right",
    color: COLORS.teal,
  });
  addRect(slide, `footer-rule-${slideNumber}`, { left: 72, top: 676, width: 1136, height: 3 }, COLORS.terracotta);
  addText(slide, `page-${slideNumber}`, String(slideNumber), { left: 1152, top: 686, width: 56, height: 20 }, {
    fontSize: 11,
    alignment: "right",
    color: COLORS.navy,
  });
}

function addSlideTitle(slide, slideNumber, eyebrow, title) {
  addBrand(slide, slideNumber);
  addText(slide, `eyebrow-${slideNumber}`, eyebrow.toUpperCase(), { left: 72, top: 84, width: 460, height: 28 }, {
    fontSize: 14,
    bold: true,
    color: COLORS.terracotta,
  });
  addText(slide, `title-${slideNumber}`, title, { left: 72, top: 118, width: 1050, height: 62 }, {
    fontSize: 38,
    bold: true,
    color: COLORS.navy,
  });
}

async function writeBlob(target, blob) {
  await fs.writeFile(target, new Uint8Array(await blob.arrayBuffer()));
}

async function main() {
  const args = process.argv.slice(2);
  const outIndex = args.indexOf("--out");
  const previewIndex = args.indexOf("--preview-dir");
  if (outIndex < 0 || previewIndex < 0) {
    throw new Error("usage: build_presentation_template.mjs --out FILE.pptx --preview-dir DIR");
  }
  const out = path.resolve(args[outIndex + 1]);
  const previewDir = path.resolve(args[previewIndex + 1]);
  await fs.mkdir(path.dirname(out), { recursive: true });
  await fs.mkdir(previewDir, { recursive: true });

  const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });

  // 1. Title layout: minimal, strong brand field.
  const titleSlide = presentation.slides.add();
  titleSlide.background.fill = COLORS.navy;
  addRect(titleSlide, "title-accent", { left: 72, top: 76, width: 14, height: 520 }, COLORS.terracotta);
  addText(titleSlide, "title-wordmark", "zamery", { left: 112, top: 76, width: 190, height: 42 }, {
    fontSize: 28,
    bold: true,
    color: COLORS.white,
  });
  addText(titleSlide, "title-tagline", "rooted in strength", { left: 112, top: 116, width: 220, height: 28 }, {
    fontSize: 14,
    italic: true,
    color: COLORS.sand,
  });
  addText(titleSlide, "title-heading", "{{ lesson title }}", { left: 112, top: 236, width: 930, height: 150 }, {
    fontSize: 58,
    bold: true,
    color: COLORS.white,
    autoFit: "shrinkText",
  });
  addText(titleSlide, "title-subheading", "{{ grade · topic · classroom promise }}", { left: 112, top: 420, width: 860, height: 70 }, {
    fontSize: 26,
    color: COLORS.mist,
  });
  addText(titleSlide, "title-audience", "CLASSROOM DECK", { left: 976, top: 642, width: 232, height: 24 }, {
    fontSize: 13,
    bold: true,
    alignment: "right",
    color: COLORS.sand,
  });

  // 2. Notice layout: compare two examples with generous whitespace.
  const notice = presentation.slides.add();
  notice.background.fill = COLORS.white;
  addSlideTitle(notice, 2, "Notice", "What feels wrong here?");
  addText(notice, "notice-example-a", "{{ plausible but wrong example }}", { left: 92, top: 236, width: 500, height: 130 }, {
    fontSize: 32,
    bold: true,
    color: COLORS.charcoal,
    verticalAlignment: "middle",
  });
  addRect(notice, "notice-divider", { left: 628, top: 220, width: 4, height: 300 }, COLORS.terracotta);
  addText(notice, "notice-example-b", "{{ contrasting example }}", { left: 680, top: 236, width: 500, height: 130 }, {
    fontSize: 32,
    bold: true,
    color: COLORS.charcoal,
    verticalAlignment: "middle",
  });
  addText(notice, "notice-prompt", "Which clue forces your choice?", { left: 280, top: 506, width: 720, height: 62 }, {
    fontSize: 28,
    bold: true,
    alignment: "center",
    color: COLORS.teal,
  });

  // 3. Decision layout: a memorable two-part rule.
  const rule = presentation.slides.add();
  rule.background.fill = COLORS.sand;
  addSlideTitle(rule, 3, "Build the rule", "Ask two questions");
  addRect(rule, "rule-left", { left: 72, top: 226, width: 520, height: 330 }, COLORS.white, "rounded-xl", COLORS.navy);
  addText(rule, "rule-left-number", "1", { left: 104, top: 250, width: 70, height: 70 }, {
    fontSize: 52,
    bold: true,
    color: COLORS.terracotta,
  });
  addText(rule, "rule-left-question", "Is the past time finished or named?", { left: 188, top: 252, width: 360, height: 110 }, {
    fontSize: 30,
    bold: true,
    color: COLORS.navy,
  });
  addText(rule, "rule-left-answer", "{{ choice and clue }}", { left: 188, top: 404, width: 340, height: 72 }, {
    fontSize: 24,
    color: COLORS.charcoal,
  });
  addRect(rule, "rule-right", { left: 656, top: 226, width: 552, height: 330 }, COLORS.white, "rounded-xl", COLORS.teal);
  addText(rule, "rule-right-number", "2", { left: 690, top: 250, width: 70, height: 70 }, {
    fontSize: 52,
    bold: true,
    color: COLORS.teal,
  });
  addText(rule, "rule-right-question", "Does the result or experience matter now?", { left: 774, top: 252, width: 390, height: 110 }, {
    fontSize: 30,
    bold: true,
    color: COLORS.navy,
  });
  addText(rule, "rule-right-answer", "{{ choice and clue }}", { left: 774, top: 404, width: 360, height: 72 }, {
    fontSize: 24,
    color: COLORS.charcoal,
  });

  // 4. Practice layout: one high-value prompt, not a dashboard.
  const practice = presentation.slides.add();
  practice.background.fill = COLORS.white;
  addSlideTitle(practice, 4, "Test the clue", "Choose — then defend it");
  addRect(practice, "practice-prompt-band", { left: 72, top: 216, width: 1136, height: 190 }, COLORS.mist, "rounded-xl", COLORS.teal);
  addText(practice, "practice-prompt", "{{ one classroom-sized prompt }}", { left: 116, top: 254, width: 1048, height: 116 }, {
    fontSize: 34,
    bold: true,
    alignment: "center",
    verticalAlignment: "middle",
    color: COLORS.navy,
  });
  addText(practice, "practice-clue", "CLUE", { left: 120, top: 462, width: 150, height: 34 }, {
    fontSize: 18,
    bold: true,
    color: COLORS.terracotta,
  });
  addText(practice, "practice-clue-line", "________________________________________", { left: 120, top: 504, width: 430, height: 42 }, {
    fontSize: 24,
    color: COLORS.charcoal,
  });
  addText(practice, "practice-choice", "CHOICE", { left: 680, top: 462, width: 160, height: 34 }, {
    fontSize: 18,
    bold: true,
    color: COLORS.teal,
  });
  addText(practice, "practice-choice-line", "________________________________________", { left: 680, top: 504, width: 430, height: 42 }, {
    fontSize: 24,
    color: COLORS.charcoal,
  });

  // 5. Exit layout: three compact prompts with clear completion rhythm.
  const exit = presentation.slides.add();
  exit.background.fill = COLORS.white;
  addSlideTitle(exit, 5, "Exit", "Show what you can decide now");
  const prompts = ["{{ quick choice }}", "{{ find the clue }}", "{{ one-sentence rule }}"];
  for (let index = 0; index < prompts.length; index += 1) {
    const top = 220 + index * 128;
    addText(exit, `exit-number-${index}`, String(index + 1), { left: 84, top, width: 54, height: 54 }, {
      fontSize: 34,
      bold: true,
      alignment: "center",
      color: index === 1 ? COLORS.teal : COLORS.terracotta,
    });
    addText(exit, `exit-prompt-${index}`, prompts[index], { left: 168, top: top + 4, width: 880, height: 48 }, {
      fontSize: 25,
      bold: true,
      color: COLORS.navy,
    });
    addRect(exit, `exit-line-${index}`, { left: 168, top: top + 70, width: 940, height: 2 }, COLORS.mist);
  }

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    await writeBlob(path.join(previewDir, `${stem}.png`), await presentation.export({ slide, format: "png", scale: 1 }));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(previewDir, `${stem}.layout.json`), await layout.text());
  }
  await writeBlob(path.join(previewDir, "template-montage.webp"), await presentation.export({ format: "webp", montage: true, scale: 1 }));
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(out);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
