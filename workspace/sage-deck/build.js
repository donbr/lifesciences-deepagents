const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const pptxgen = require('pptxgenjs');

const SKILL_DIR = '/home/donbr/.claude/plugins/cache/anthropic-agent-skills/document-skills/69c0b1a06741/skills/pptx';
const html2pptx = require(path.join(SKILL_DIR, 'scripts', 'html2pptx'));

const PROJECT = '/home/donbr/ai2026/lifesciences-deepagents-worktrees/deepagents-0312-upgrade-spike';
const SLIDES = path.join(PROJECT, 'workspace', 'sage-deck', 'slides');
const ASSETS = path.join(PROJECT, 'workspace', 'sage-deck', 'assets');
const OUTPUT = path.join(PROJECT, 'output', 'sage-bionetworks-collaboration-deck.pptx');

// Colors (CSS with #, PptxGenJS without #)
const NAVY = '#1B2A4A';
const TEAL = '#2E8B8B';
const WHITE = '#FFFFFF';
const LGRAY = '#F0F2F5';
const MGRAY = '#6B7280';
const NAVY_P = '1B2A4A';
const TEAL_P = '2E8B8B';
const WHITE_P = 'FFFFFF';
const LGRAY_P = 'F0F2F5';

// Common HTML wrapper
function slide(bodyStyle, content) {
  return `<!DOCTYPE html>
<html><head><style>
html { background: #ffffff; }
body { width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; flex-direction: column; ${bodyStyle} }
</style></head><body>${content}</body></html>`;
}

// Header bar for content slides
function header(title, subtitle) {
  const sub = subtitle ? `<p style="color: #94A3B8; font-size: 11pt; margin: 4pt 0 0 0;">${subtitle}</p>` : '';
  return `<div style="background: ${NAVY}; padding: 14pt 28pt; min-height: 44pt; flex-shrink: 0;">
  <h1 style="color: ${WHITE}; font-size: 22pt; margin: 0; font-weight: bold;">${title}</h1>${sub}
</div>`;
}

// Speaker notes
const NOTES = {
  1: "Thank you for the productive initial meeting. This deck summarizes what we heard, what we've built, and a concrete path forward for collaboration. The core insight from our conversation: Sage lacks a baseline process for evaluating LLM tools apples-to-apples — and we believe we've built the foundation for that baseline.",
  2: "These four themes emerged consistently across the conversation. They shaped how we structured this follow-up — moving from technical capabilities to researcher-centric value propositions.",
  3: "This is the core problem Sage articulated. Without a baseline, every new LLM tool evaluation starts from scratch. Our competency questions catalog and quality framework provide the missing foundation.",
  4: "We reframe 'competency questions' as 'research evaluation benchmarks' — same rigor, business-friendly language. Each benchmark has a known answer path expressed as entity CURIEs and relationship types. This is the missing test suite for LLM evaluation.",
  5: "This framework moves evaluation from 'does it work?' to 'how well does it work across 10 specific dimensions?' Dimensions 1-4 are non-negotiable safety dimensions — hallucination risk alone can disqualify a tool. Dimensions 5-10 measure depth and utility.",
  6: "Each phase has a dedicated specialist agent with only the tools it needs — this is tool isolation, not a monolithic prompt. The protocol transforms a fuzzy natural-language question into a structured, validated knowledge graph. 13 biomedical APIs are orchestrated across the 7 phases.",
  7: "These are real production results, not cherry-picked demos — exactly the kind of reproducible evidence Sage asked for. Zero hallucinations means every entity, relationship, and trial ID was verified against primary sources.",
  8: "This case study was chosen because NF1 is core to Sage BioNetworks' mission. The platform discovered three complementary cardioprotective strategies — not just one. It then grounded findings against 8 Synapse.org datasets, creating a direct bridge between our validated knowledge graph and Sage's data repository.",
  9: "These three personas came directly from the Sage conversation. Each has different needs, different benchmark questions, and different definitions of 'useful.' The platform serves all three through the same protocol.",
  10: "These three propositions map to Sage's expressed needs. The first addresses the baseline gap directly. The second shows how our platform enhances Sage's existing data assets. The third addresses the fragmentation problem.",
  11: "Evidence grading is what separates a validated knowledge graph from a hallucinated one. Every claim in our output gets an L1-L4 tag with a numeric confidence range. Sage's Synapse datasets create a unique upgrade path.",
  12: "This is designed to be lightweight and deliverable-driven. Phase 1 proves value with Sage's own data. Phase 2 expands the test suite with Sage domain expertise. Phase 3 puts real researchers in front of the tool.",
  13: "Section 2 is the most important — we need Sage to identify which questions matter to them. Section 3 is a live demo, not a recorded one — demonstrating the protocol's reproducibility in real time.",
  14: "Thank you for the productive conversation. We believe the combination of Sage's domain expertise and data assets with our structured validation platform creates something neither organization could build alone."
};

async function createGradients() {
  // Title slide gradient
  const titleSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540">
    <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1B2A4A"/><stop offset="100%" style="stop-color:#0F1A2E"/>
    </linearGradient></defs>
    <rect width="100%" height="100%" fill="url(#g)"/>
    <rect x="0" y="300" width="960" height="4" fill="#2E8B8B" opacity="0.8"/>
  </svg>`;
  await sharp(Buffer.from(titleSvg)).png().toFile(path.join(ASSETS, 'title-bg.png'));

  // Thank you slide gradient
  const thanksSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540">
    <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1B2A4A"/><stop offset="100%" style="stop-color:#152238"/>
    </linearGradient></defs>
    <rect width="100%" height="100%" fill="url(#g)"/>
  </svg>`;
  await sharp(Buffer.from(thanksSvg)).png().toFile(path.join(ASSETS, 'thanks-bg.png'));
}

function writeSlides() {
  // SLIDE 1: Title
  fs.writeFileSync(path.join(SLIDES, 'slide01.html'), slide(
    `background-image: url('${path.join(ASSETS, 'title-bg.png')}'); background-size: cover;`,
    `<div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40pt;">
  <h1 style="color: ${WHITE}; font-size: 30pt; margin: 0 0 8pt 0; text-align: center; font-weight: bold;">Structured Validation for Life Sciences AI</h1>
  <div style="width: 80pt; height: 3pt; background: ${TEAL};"></div>
  <p style="color: #94A3B8; font-size: 16pt; margin: 16pt 0 0 0; text-align: center;">A Collaboration Framework</p>
  <p style="color: #94A3B8; font-size: 13pt; margin: 6pt 0 0 0; text-align: center;">Sage BioNetworks Follow-Up</p>
  <p style="color: ${MGRAY}; font-size: 11pt; margin: 40pt 0 0 0; text-align: center;">Don B. | February 2026</p>
</div>`
  ));

  // SLIDE 2: Meeting Takeaways
  const takeaways = [
    ['No Baseline Exists', 'There is no standardized process for comparing LLM tool outputs in life sciences. Teams evaluate tools ad hoc, making procurement and adoption decisions on anecdote rather than evidence.'],
    ['Use Cases Must Be Persona-Driven', 'Different researchers need different things. A trainee learning pathway biology has fundamentally different needs than a PI orchestrating a multi-site collaboration.'],
    ['Structured Testing Matters', 'Sage teams want reproducible test cases with known answers — not cherry-picked demos. Gold-standard questions with verifiable paths are the currency of trust.'],
    ['Language Needs Translation', 'Technical capabilities must be expressed in terms researchers actually use: "Can it find drugs for my target?" not "Does it resolve HGNC IDs?"']
  ];
  const takeawayCards = takeaways.map(([title, desc]) =>
    `<div style="flex: 1; background: ${LGRAY}; border-left: 4pt solid ${TEAL}; padding: 10pt 12pt; border-radius: 0 4pt 4pt 0;">
      <p style="color: ${NAVY}; font-size: 10pt; font-weight: bold; margin: 0 0 4pt 0;">${title}</p>
      <p style="color: #374151; font-size: 8pt; margin: 0; line-height: 1.3;">${desc}</p>
    </div>`
  ).join('');
  fs.writeFileSync(path.join(SLIDES, 'slide02.html'), slide('',
    `${header('What We Heard')}
<div style="flex: 1; padding: 16pt 28pt; display: flex; flex-direction: column; gap: 8pt;">
  <div style="display: flex; gap: 12pt; flex: 1;">
    ${takeaways.slice(0, 2).map(([t, d]) =>
      `<div style="flex: 1; background: ${LGRAY}; border-left: 4pt solid ${TEAL}; padding: 12pt 14pt; border-radius: 0 4pt 4pt 0;">
        <p style="color: ${NAVY}; font-size: 11pt; font-weight: bold; margin: 0 0 6pt 0;">${t}</p>
        <p style="color: #374151; font-size: 8.5pt; margin: 0; line-height: 1.4;">${d}</p>
      </div>`
    ).join('')}
  </div>
  <div style="display: flex; gap: 12pt; flex: 1;">
    ${takeaways.slice(2, 4).map(([t, d]) =>
      `<div style="flex: 1; background: ${LGRAY}; border-left: 4pt solid ${TEAL}; padding: 12pt 14pt; border-radius: 0 4pt 4pt 0;">
        <p style="color: ${NAVY}; font-size: 11pt; font-weight: bold; margin: 0 0 6pt 0;">${t}</p>
        <p style="color: #374151; font-size: 8.5pt; margin: 0; line-height: 1.4;">${d}</p>
      </div>`
    ).join('')}
  </div>
</div>`
  ));

  // SLIDE 3: Baseline Challenge
  fs.writeFileSync(path.join(SLIDES, 'slide03.html'), slide('',
    `${header('The Baseline Challenge')}
<div style="flex: 1; padding: 14pt 28pt; display: flex; gap: 16pt;">
  <div style="flex: 1; display: flex; flex-direction: column;">
    <div style="background: #FEE2E2; padding: 8pt 12pt; border-radius: 4pt 4pt 0 0;">
      <p style="color: #991B1B; font-size: 11pt; font-weight: bold; margin: 0;">Current State</p>
    </div>
    <div style="background: ${LGRAY}; flex: 1; padding: 12pt;">
      <ul style="margin: 0; padding-left: 16pt; color: #374151; font-size: 9pt; line-height: 1.8;">
        <li>Ad hoc tool evaluation</li>
        <li>Cherry-picked demos</li>
        <li>No reproducible test cases</li>
        <li>Subjective quality assessment</li>
        <li>No cross-tool comparison framework</li>
      </ul>
    </div>
  </div>
  <div style="flex: 1; display: flex; flex-direction: column;">
    <div style="background: #D1FAE5; padding: 8pt 12pt; border-radius: 4pt 4pt 0 0;">
      <p style="color: #065F46; font-size: 11pt; font-weight: bold; margin: 0;">What a Baseline Requires</p>
    </div>
    <div style="background: ${LGRAY}; flex: 1; padding: 12pt;">
      <ul style="margin: 0; padding-left: 16pt; color: #374151; font-size: 9pt; line-height: 1.8;">
        <li>Standardized questions with known answers</li>
        <li>Entity resolution to canonical IDs (CURIEs)</li>
        <li>Multi-dimensional quality scoring</li>
        <li>Evidence grading with confidence levels</li>
        <li>Reproducible across tools, models, and time</li>
      </ul>
    </div>
  </div>
</div>
<div style="background: ${TEAL}; padding: 8pt 28pt; flex-shrink: 0;">
  <p style="color: ${WHITE}; font-size: 9pt; margin: 0; text-align: center;">The gap between these columns is exactly what our platform addresses.</p>
</div>`
  ));

  // SLIDE 4: Research Evaluation Benchmarks (header + placeholder for table)
  fs.writeFileSync(path.join(SLIDES, 'slide04.html'), slide('',
    `${header('Research Evaluation Benchmarks', 'Competency Questions as Standardized Test Cases')}
<div style="flex: 1; padding: 10pt 28pt;">
  <div id="benchmarks-table" class="placeholder" style="width: 664pt; height: 220pt;"></div>
</div>
<div style="padding: 0 28pt 10pt 28pt;">
  <p style="color: ${MGRAY}; font-size: 8pt; margin: 0; text-align: center;">15 benchmarks spanning 8 therapeutic domains — each with gold-standard paths and verifiable answers</p>
</div>`
  ));

  // SLIDE 5: Quality Framework (header + placeholder for table)
  fs.writeFileSync(path.join(SLIDES, 'slide05.html'), slide('',
    `${header('10-Dimension Quality Framework')}
<div style="flex: 1; padding: 6pt 28pt;">
  <div id="quality-table" class="placeholder" style="width: 664pt; height: 270pt;"></div>
</div>
<div style="padding: 0 28pt 8pt 28pt;">
  <p style="color: ${MGRAY}; font-size: 8pt; margin: 0; text-align: center; font-weight: bold;">Pass threshold: 35/40 on dimensions 1-4 (non-negotiable) + 30/60 on dimensions 5-10</p>
</div>`
  ));

  // SLIDE 6: Fuzzy-to-Fact Protocol
  const phases = [
    ['1', 'ANCHOR', 'Resolve entities to canonical IDs'],
    ['2', 'ENRICH', 'Cross-reference functional metadata'],
    ['3', 'EXPAND', 'Discover interaction networks'],
    ['4a', 'DRUGS', 'Find therapeutics for targets'],
    ['4b', 'TRIALS', 'Find clinical trials'],
    ['5', 'VALIDATE', 'Verify claims, grade evidence'],
    ['6', 'PERSIST', 'Generate knowledge graph']
  ];
  const phaseBoxes = phases.map(([num, name, desc], i) => {
    const arrow = i < phases.length - 1 ? `<div style="display: flex; align-items: center; flex-shrink: 0;"><p style="color: ${TEAL}; font-size: 14pt; margin: 0; font-weight: bold;">&#8594;</p></div>` : '';
    return `<div style="flex: 1; background: ${NAVY}; border-radius: 4pt; padding: 6pt 3pt; text-align: center;">
      <p style="color: ${TEAL}; font-size: 7pt; margin: 0; font-weight: bold;">${num}</p>
      <p style="color: ${WHITE}; font-size: 8pt; margin: 2pt 0; font-weight: bold;">${name}</p>
      <p style="color: #94A3B8; font-size: 5.5pt; margin: 0;">${desc}</p>
    </div>${arrow}`;
  }).join('');

  const apis = ['HGNC', 'ChEMBL', 'UniProt', 'Ensembl', 'STRING', 'BioGRID', 'Open Targets', 'PubChem', 'WikiPathways', 'ClinicalTrials.gov', 'PubMed', 'Entrez', 'IUPHAR'];
  const apiBadges = apis.map(a =>
    `<div style="background: ${LGRAY}; border: 1pt solid #D1D5DB; border-radius: 10pt; padding: 3pt 7pt;">
      <p style="color: ${NAVY}; font-size: 6pt; margin: 0; white-space: nowrap;">${a}</p>
    </div>`
  ).join('');

  fs.writeFileSync(path.join(SLIDES, 'slide06.html'), slide('',
    `${header('The Fuzzy-to-Fact Protocol', '7-Phase Structured Workflow')}
<div style="flex: 1; padding: 16pt 14pt 8pt 14pt; display: flex; flex-direction: column; justify-content: center; gap: 16pt;">
  <div style="display: flex; align-items: stretch; gap: 3pt;">
    ${phaseBoxes}
  </div>
  <div style="display: flex; flex-wrap: wrap; gap: 4pt; justify-content: center; padding: 8pt 0;">
    ${apiBadges}
  </div>
  <p style="color: ${MGRAY}; font-size: 7pt; margin: 0; text-align: center;">13 biomedical APIs orchestrated across 7 phases with dedicated specialist agents</p>
</div>`
  ));

  // SLIDE 7: Production Results
  const metrics = [
    ['5', 'Reports Generated'],
    ['9.3/10', 'Median Quality'],
    ['9.7/10', 'Protocol Execution'],
    ['0', 'Hallucinations'],
    ['100%', 'NCT Verification']
  ];
  const metricCards = metrics.map(([val, label]) =>
    `<div style="flex: 1; background: ${LGRAY}; border-radius: 6pt; padding: 16pt 8pt; text-align: center; border-top: 3pt solid ${TEAL};">
      <p style="color: ${NAVY}; font-size: 26pt; margin: 0; font-weight: bold;">${val}</p>
      <p style="color: ${MGRAY}; font-size: 8pt; margin: 6pt 0 0 0;">${label}</p>
    </div>`
  ).join('');

  fs.writeFileSync(path.join(SLIDES, 'slide07.html'), slide('',
    `${header('Production Results')}
<div style="flex: 1; padding: 30pt 28pt; display: flex; flex-direction: column; justify-content: center;">
  <div style="display: flex; gap: 12pt;">
    ${metricCards}
  </div>
  <p style="color: ${MGRAY}; font-size: 8pt; margin: 16pt 0 0 0; text-align: center;">Across 5 production reports covering drug mechanisms, synthetic lethality, gene networks, doxorubicin toxicity, and clinical landscape analysis</p>
</div>`
  ));

  // SLIDE 8: NF1 Case Study
  fs.writeFileSync(path.join(SLIDES, 'slide08.html'), slide('',
    `${header('Case Study: Doxorubicin Cardiotoxicity in NF1', 'Directly relevant to Sage BioNetworks\' Neurofibromatosis research')}
<div style="flex: 1; padding: 10pt 28pt; display: flex; gap: 16pt;">
  <div style="flex: 1;">
    <div style="background: ${LGRAY}; border-radius: 4pt; padding: 10pt; height: 100%;">
      <p style="color: ${NAVY}; font-size: 10pt; font-weight: bold; margin: 0 0 6pt 0;">Knowledge Graph Summary</p>
      <ul style="margin: 0; padding-left: 14pt; color: #374151; font-size: 8pt; line-height: 1.6;">
        <li><b>18 nodes</b> (11 genes, 3 compounds, 3 pathways, 2 diseases)</li>
        <li><b>20 edges</b> (verified relationships)</li>
      </ul>
      <p style="color: ${NAVY}; font-size: 8.5pt; font-weight: bold; margin: 8pt 0 4pt 0;">3 Cardioprotective Axes:</p>
      <ul style="margin: 0; padding-left: 14pt; color: #374151; font-size: 7.5pt; line-height: 1.6;">
        <li><span style="color: ${TEAL}; font-weight: bold;">TOP2B</span> degradation via Dexrazoxane (L4)</li>
        <li><span style="color: ${TEAL}; font-weight: bold;">NRF2/KEAP1</span> antioxidant response (L2)</li>
        <li><span style="color: ${TEAL}; font-weight: bold;">MEK inhibition</span> via Selumetinib (L4)</li>
      </ul>
    </div>
  </div>
  <div style="flex: 1;">
    <div style="background: ${LGRAY}; border-radius: 4pt; padding: 10pt; height: 100%;">
      <p style="color: ${NAVY}; font-size: 10pt; font-weight: bold; margin: 0 0 6pt 0;">Synapse Grounding</p>
      <ul style="margin: 0; padding-left: 14pt; color: #374151; font-size: 8pt; line-height: 1.6;">
        <li><b>8 Synapse datasets</b> identified</li>
        <li><b>56% node coverage</b> (10/18 grounded)</li>
        <li><b>35% edge coverage</b> (7/20 grounded)</li>
      </ul>
      <p style="color: ${NAVY}; font-size: 8.5pt; font-weight: bold; margin: 8pt 0 4pt 0;">Key Datasets:</p>
      <ul style="margin: 0; padding-left: 14pt; color: #374151; font-size: 7.5pt; line-height: 1.6;">
        <li><b>syn200548</b>: Rat heart doxorubicin/dexrazoxane</li>
        <li><b>syn44222814</b>: NF1 Schwann cell + selumetinib</li>
        <li><b>syn61259950</b>: Phase II Selumetinib (NCT02407405)</li>
      </ul>
    </div>
  </div>
</div>
<div style="background: ${NAVY}; padding: 6pt 28pt; flex-shrink: 0;">
  <p style="color: #94A3B8; font-size: 8pt; margin: 0; text-align: center;">6 verified clinical trials  |  Quality score: 35/40 (PASS)  |  All 3 drugs FDA-approved</p>
</div>`
  ));

  // SLIDE 9: Three Personas
  const personas = [
    ['Educational / Trainee', '"I\'m learning pathway biology and need to understand how drugs connect to diseases"',
     'FOP Drug Mechanism — 4-node linear path', 'Structured learning with verified relationships', '"Show me the mechanism step by step"'],
    ['Independent Investigator', '"I need to validate my hypothesis about synthetic lethal targets before writing a grant"',
     'ARID1A Synthetic Lethality — multi-source validation', 'Multi-database triangulation with evidence grading', '"Cross-reference my targets against all data"'],
    ['Project Manager', '"I need to understand the clinical landscape to prioritize resources"',
     'Health Emergency Landscape — 18,636+ trials', 'Rapid clinical landscape with structured output', '"Give me an evidence-based overview for leadership"']
  ];
  const personaCols = personas.map(([name, quote, bench, value, need]) =>
    `<div style="flex: 1; background: ${LGRAY}; border-radius: 4pt; padding: 10pt; border-top: 3pt solid ${TEAL};">
      <p style="color: ${NAVY}; font-size: 10pt; font-weight: bold; margin: 0 0 4pt 0;">${name}</p>
      <p style="color: ${MGRAY}; font-size: 7pt; margin: 0 0 6pt 0; font-style: italic;">${quote}</p>
      <p style="color: ${NAVY}; font-size: 7.5pt; font-weight: bold; margin: 0 0 2pt 0;">Benchmark:</p>
      <p style="color: #374151; font-size: 7pt; margin: 0 0 4pt 0;">${bench}</p>
      <p style="color: ${NAVY}; font-size: 7.5pt; font-weight: bold; margin: 0 0 2pt 0;">Value:</p>
      <p style="color: #374151; font-size: 7pt; margin: 0 0 4pt 0;">${value}</p>
      <div style="background: ${NAVY}; border-radius: 3pt; padding: 4pt 6pt; margin-top: 4pt;">
        <p style="color: ${WHITE}; font-size: 7pt; margin: 0; text-align: center;">${need}</p>
      </div>
    </div>`
  ).join('');

  fs.writeFileSync(path.join(SLIDES, 'slide09.html'), slide('',
    `${header('Three Research Personas')}
<div style="flex: 1; padding: 14pt 28pt; display: flex; gap: 12pt;">
  ${personaCols}
</div>`
  ));

  // SLIDE 10: Three Value Propositions
  const vps = [
    ['Structured Validation & Testing', [
      '15 benchmark questions with gold-standard answers',
      '10-dimension quality scoring framework',
      'Reproducible test suite for any LLM tool comparison'
    ], 'The baseline Sage has been looking for'],
    ['Data Context & Curation', [
      'Automated Synapse dataset grounding',
      'Knowledge graph overlay on existing Sage data',
      'Evidence-graded relationships with CURIE provenance'
    ], 'Turn Synapse data into structured knowledge'],
    ['Unifying the Research Pipeline', [
      'Fuzzy question to validated knowledge graph',
      '13 APIs in reproducible 7-phase protocol',
      'Persona-driven entry points for researchers'
    ], 'One protocol, from bench question to clinical context']
  ];
  const vpCols = vps.map(([title, items, tagline]) =>
    `<div style="flex: 1; background: ${LGRAY}; border-radius: 4pt; padding: 12pt; display: flex; flex-direction: column;">
      <p style="color: ${NAVY}; font-size: 10pt; font-weight: bold; margin: 0 0 8pt 0;">${title}</p>
      <ul style="margin: 0; padding-left: 14pt; color: #374151; font-size: 8pt; line-height: 1.7; flex: 1;">
        ${items.map(i => `<li>${i}</li>`).join('')}
      </ul>
      <div style="background: ${TEAL}; border-radius: 3pt; padding: 6pt 8pt; margin-top: 8pt;">
        <p style="color: ${WHITE}; font-size: 8pt; margin: 0; text-align: center; font-weight: bold;">${tagline}</p>
      </div>
    </div>`
  ).join('');

  fs.writeFileSync(path.join(SLIDES, 'slide10.html'), slide('',
    `${header('Three Value Propositions for Sage')}
<div style="flex: 1; padding: 14pt 28pt; display: flex; gap: 12pt;">
  ${vpCols}
</div>`
  ));

  // SLIDE 11: Evidence Pyramid
  const levels = [
    ['L4 — Clinical Evidence', '0.90-1.00', 'Drug-target confirmed by trials or FDA approval', '55%', NAVY],
    ['L3 — Functional Evidence', '0.70-0.89', 'Validated by experimental data (STRING, BioGRID)', '65%', '#2D4A6A'],
    ['L2 — Multi-Database', '0.50-0.69', 'Confirmed across 2+ databases', '78%', '#3D5A7A'],
    ['L1 — Single Database', '0.30-0.49', 'Found in one source only', '90%', '#5A7A9A']
  ];
  const pyramidBars = levels.reverse().map(([label, conf, desc, width, color]) =>
    `<div style="width: ${width}; background: ${color}; border-radius: 3pt; padding: 6pt 10pt; text-align: center;">
      <p style="color: ${WHITE}; font-size: 8pt; font-weight: bold; margin: 0;">${label} (${conf})</p>
      <p style="color: #CBD5E1; font-size: 6.5pt; margin: 2pt 0 0 0;">${desc}</p>
    </div>`
  ).reverse().join('');

  fs.writeFileSync(path.join(SLIDES, 'slide11.html'), slide('',
    `${header('Evidence Grading: L1-L4 Pyramid')}
<div style="flex: 1; padding: 10pt 20pt; display: flex; gap: 14pt;">
  <div style="flex: 3; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4pt;">
    ${pyramidBars}
  </div>
  <div style="flex: 2; display: flex; align-items: center;">
    <div style="background: #ECFDF5; border: 2pt solid ${TEAL}; border-radius: 6pt; padding: 12pt;">
      <p style="color: ${NAVY}; font-size: 9pt; font-weight: bold; margin: 0 0 6pt 0;">Synapse Grounding Upgrade</p>
      <p style="color: #374151; font-size: 7.5pt; margin: 0; line-height: 1.5;">When a KG node or edge is grounded in a Synapse dataset, its evidence level can be upgraded.</p>
      <p style="color: ${TEAL}; font-size: 7.5pt; margin: 6pt 0 0 0; font-weight: bold;">Example:</p>
      <p style="color: #374151; font-size: 7pt; margin: 2pt 0 0 0; line-height: 1.4;">NRF2/KEAP1 at L2 &#8594; grounded by syn205590 (Nrf2 KO mouse) &#8594; upgradeable to L3</p>
    </div>
  </div>
</div>`
  ));

  // SLIDE 12: Collaboration Framework
  const colPhases = [
    ['Phase 1', 'Proof of Concept', 'Weeks 1-4', [
      'Run 3-5 NF1-relevant benchmarks end-to-end',
      'Evaluate against 10-dimension quality framework',
      'Validate Synapse grounding on NF1 datasets',
      'Deliverable: Quality report + knowledge graphs'
    ]],
    ['Phase 2', 'Benchmark Expansion', 'Weeks 5-8', [
      'Co-develop 5-10 Sage-specific competency questions',
      'Add Synapse-native data sources to API orchestration',
      'Train evidence grading on Sage domain expertise',
      'Deliverable: Expanded catalog + Synapse integration spec'
    ]],
    ['Phase 3', 'Integration Pilot', 'Weeks 9-12', [
      'Deploy platform for 3-5 Sage researchers',
      'Collect structured feedback on usability and accuracy',
      'Measure: time-to-insight, evidence quality, coverage',
      'Deliverable: Pilot report + roadmap for 2026 H2'
    ]]
  ];
  const phaseCols = colPhases.map(([phase, title, weeks, items]) =>
    `<div style="flex: 1; border: 2pt solid ${TEAL}; border-radius: 6pt; padding: 10pt; display: flex; flex-direction: column;">
      <div style="background: ${TEAL}; border-radius: 3pt; padding: 4pt 8pt; margin: 0 0 6pt 0; text-align: center;">
        <p style="color: ${WHITE}; font-size: 8pt; font-weight: bold; margin: 0;">${phase}: ${title}</p>
      </div>
      <p style="color: ${MGRAY}; font-size: 8pt; margin: 0 0 6pt 0; text-align: center; font-weight: bold;">${weeks}</p>
      <ul style="margin: 0; padding-left: 12pt; color: #374151; font-size: 7.5pt; line-height: 1.6; flex: 1;">
        ${items.map(i => `<li>${i}</li>`).join('')}
      </ul>
    </div>`
  ).join('');

  fs.writeFileSync(path.join(SLIDES, 'slide12.html'), slide('',
    `${header('Proposed Collaboration: 3 Phases, 12 Weeks')}
<div style="flex: 1; padding: 14pt 28pt; display: flex; gap: 12pt; align-items: stretch;">
  ${phaseCols}
</div>`
  ));

  // SLIDE 13: Meeting Agenda (header + placeholder for table)
  fs.writeFileSync(path.join(SLIDES, 'slide13.html'), slide('',
    `${header('Proposed Next Meeting Agenda')}
<div style="flex: 1; padding: 10pt 28pt;">
  <div id="agenda-table" class="placeholder" style="width: 664pt; height: 220pt;"></div>
</div>
<div style="padding: 0 28pt 10pt 28pt;">
  <p style="color: ${MGRAY}; font-size: 8pt; margin: 0; text-align: center;">Flexible format — happy to adjust based on Sage's priorities and available time</p>
</div>`
  ));

  // SLIDE 14: Thank You
  fs.writeFileSync(path.join(SLIDES, 'slide14.html'), slide(
    `background-image: url('${path.join(ASSETS, 'thanks-bg.png')}'); background-size: cover;`,
    `<div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 30pt 60pt;">
  <h1 style="color: ${WHITE}; font-size: 32pt; margin: 0 0 6pt 0; text-align: center;">Thank You</h1>
  <div style="width: 60pt; height: 3pt; background: ${TEAL};"></div>
  <p style="color: #94A3B8; font-size: 13pt; margin: 14pt 0 20pt 0; text-align: center;">Let's build the baseline for life sciences AI evaluation</p>
  <div style="display: flex; gap: 20pt; margin-top: 10pt;">
    <div style="text-align: center;">
      <p style="color: ${TEAL}; font-size: 8pt; font-weight: bold; margin: 0 0 3pt 0;">Benchmark Catalog</p>
      <p style="color: #94A3B8; font-size: 7pt; margin: 0;">15 questions across 8 domains</p>
    </div>
    <div style="text-align: center;">
      <p style="color: ${TEAL}; font-size: 8pt; font-weight: bold; margin: 0 0 3pt 0;">Quality Framework</p>
      <p style="color: #94A3B8; font-size: 7pt; margin: 0;">10-dimension L1-L4 grading</p>
    </div>
    <div style="text-align: center;">
      <p style="color: ${TEAL}; font-size: 8pt; font-weight: bold; margin: 0 0 3pt 0;">NF1 Case Study</p>
      <p style="color: #94A3B8; font-size: 7pt; margin: 0;">18 nodes, 20 edges, 8 Synapse datasets</p>
    </div>
  </div>
  <p style="color: ${MGRAY}; font-size: 7pt; margin: 24pt 0 0 0; text-align: center;">Built on open standards: BioLink model, CURIEs, ClinicalTrials.gov v2, Synapse.org</p>
  <p style="color: #64748B; font-size: 8pt; margin: 8pt 0 0 0; text-align: center;">Don B. | LangGraph + 13 Biomedical APIs + Synapse Integration</p>
</div>`
  ));
}

async function build() {
  console.log('Creating gradients...');
  await createGradients();

  console.log('Writing HTML slides...');
  writeSlides();

  console.log('Building PPTX...');
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Don B.';
  pptx.title = 'Structured Validation for Life Sciences AI';

  // Slide 1: Title
  const { slide: s1 } = await html2pptx(path.join(SLIDES, 'slide01.html'), pptx);
  s1.addNotes(NOTES[1]);

  // Slide 2: Meeting Takeaways
  const { slide: s2 } = await html2pptx(path.join(SLIDES, 'slide02.html'), pptx);
  s2.addNotes(NOTES[2]);

  // Slide 3: Baseline Challenge
  const { slide: s3 } = await html2pptx(path.join(SLIDES, 'slide03.html'), pptx);
  s3.addNotes(NOTES[3]);

  // Slide 4: Benchmarks with table
  const { slide: s4, placeholders: p4 } = await html2pptx(path.join(SLIDES, 'slide04.html'), pptx);
  s4.addNotes(NOTES[4]);
  const benchData = [
    [
      { text: 'Benchmark', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 8 } },
      { text: 'Domain', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 8 } },
      { text: 'Key Entities (CURIEs)', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 8 } },
      { text: 'Complexity', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 8 } }
    ],
    [
      { text: 'FOP Drug Mechanism', options: { bold: true, fontSize: 7 } },
      { text: 'Drug Mechanisms', options: { fontSize: 7 } },
      { text: 'Palovarotene (CHEMBL:2105648)\nRARG (HGNC:9866), ACVR1 (HGNC:171)', options: { fontSize: 6.5 } },
      { text: 'Low\n4-node linear path', options: { fontSize: 7 } }
    ],
    [
      { text: 'ARID1A Synthetic Lethality', options: { bold: true, fontSize: 7 } },
      { text: 'Precision Oncology', options: { fontSize: 7 } },
      { text: 'ARID1A (HGNC:11110)\nEZH2 (HGNC:3527), Tazemetostat (CHEMBL:3414621)', options: { fontSize: 6.5 } },
      { text: 'Medium\nProtein complex + drug + trial', options: { fontSize: 7 } }
    ],
    [
      { text: 'TP53 Synthetic Lethal Pairs', options: { bold: true, fontSize: 7 } },
      { text: 'Scalable Validation', options: { fontSize: 7 } },
      { text: 'TP53 (HGNC:11998)\nTYMS (HGNC:12441), 5-FU (CHEMBL:185)', options: { fontSize: 6.5 } },
      { text: 'High\n209 SL pairs, CRISPR validation', options: { fontSize: 7 } }
    ],
    [
      { text: 'Health Emergency Landscape', options: { bold: true, fontSize: 7 } },
      { text: 'Clinical Landscape', options: { fontSize: 7 } },
      { text: '18,636+ recruiting trials across\noncology, diabetes, Alzheimer\'s, Long COVID', options: { fontSize: 6.5 } },
      { text: 'Medium\nReal-time trend detection', options: { fontSize: 7 } }
    ]
  ];
  if (p4.length > 0) {
    s4.addTable(benchData, { ...p4[0], colW: [2.1, 1.5, 3.5, 2.1], border: { pt: 0.5, color: 'D1D5DB' }, valign: 'middle', rowH: [0.35, 0.55, 0.55, 0.55, 0.55] });
  }

  // Slide 5: Quality Framework with table
  const { slide: s5, placeholders: p5 } = await html2pptx(path.join(SLIDES, 'slide05.html'), pptx);
  s5.addNotes(NOTES[5]);
  const dims = [
    ['1', 'CURIE Resolution', 'Entities mapped to canonical identifiers (HGNC, CHEMBL, MONDO)'],
    ['2', 'Source Attribution', 'Every claim traceable to a named API + identifier'],
    ['3', 'Evidence Grading', 'Claims tagged L1-L4 with confidence ranges'],
    ['4', 'Hallucination Risk', 'Zero fabricated entities, relationships, or trial IDs'],
    ['5', 'Multi-Source Triangulation', 'Findings confirmed across 2+ independent databases'],
    ['6', 'Clinical Relevance', 'Results connect to actionable drugs or active trials'],
    ['7', 'Pathway Completeness', 'Full mechanistic paths discovered (drug > target > disease)'],
    ['8', 'Contradiction Handling', 'Conflicting sources identified and resolved transparently'],
    ['9', 'Temporal Currency', 'Data reflects current trial status and approval landscape'],
    ['10', 'Knowledge Graph Density', 'Captured interaction breadth (nodes, edges, cross-refs)']
  ];
  const qualData = [
    [
      { text: '#', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 7, align: 'center' } },
      { text: 'Dimension', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 7 } },
      { text: 'What It Measures', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 7 } },
      { text: 'Range', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 7, align: 'center' } }
    ],
    ...dims.map(([n, dim, desc], i) => [
      { text: n, options: { fontSize: 7, align: 'center', fill: i < 4 ? { color: 'FEF3C7' } : undefined } },
      { text: dim, options: { fontSize: 7, bold: true, fill: i < 4 ? { color: 'FEF3C7' } : undefined } },
      { text: desc, options: { fontSize: 6.5, fill: i < 4 ? { color: 'FEF3C7' } : undefined } },
      { text: '0-10', options: { fontSize: 7, align: 'center', fill: i < 4 ? { color: 'FEF3C7' } : undefined } }
    ])
  ];
  if (p5.length > 0) {
    s5.addTable(qualData, { ...p5[0], colW: [0.4, 1.8, 5.5, 0.6], border: { pt: 0.5, color: 'D1D5DB' }, valign: 'middle', rowH: [0.3, ...Array(10).fill(0.22)] });
  }

  // Slide 6: Protocol
  const { slide: s6 } = await html2pptx(path.join(SLIDES, 'slide06.html'), pptx);
  s6.addNotes(NOTES[6]);

  // Slide 7: Results
  const { slide: s7 } = await html2pptx(path.join(SLIDES, 'slide07.html'), pptx);
  s7.addNotes(NOTES[7]);

  // Slide 8: NF1 Case Study
  const { slide: s8 } = await html2pptx(path.join(SLIDES, 'slide08.html'), pptx);
  s8.addNotes(NOTES[8]);

  // Slide 9: Personas
  const { slide: s9 } = await html2pptx(path.join(SLIDES, 'slide09.html'), pptx);
  s9.addNotes(NOTES[9]);

  // Slide 10: Value Props
  const { slide: s10 } = await html2pptx(path.join(SLIDES, 'slide10.html'), pptx);
  s10.addNotes(NOTES[10]);

  // Slide 11: Evidence Pyramid
  const { slide: s11 } = await html2pptx(path.join(SLIDES, 'slide11.html'), pptx);
  s11.addNotes(NOTES[11]);

  // Slide 12: Collaboration Framework
  const { slide: s12 } = await html2pptx(path.join(SLIDES, 'slide12.html'), pptx);
  s12.addNotes(NOTES[12]);

  // Slide 13: Meeting Agenda with table
  const { slide: s13, placeholders: p13 } = await html2pptx(path.join(SLIDES, 'slide13.html'), pptx);
  s13.addNotes(NOTES[13]);
  const agendaData = [
    [
      { text: 'Section', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 9 } },
      { text: 'Topic', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 9 } },
      { text: 'Time', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 9, align: 'center' } },
      { text: 'Lead', options: { fill: { color: NAVY_P }, color: WHITE_P, bold: true, fontSize: 9, align: 'center' } }
    ],
    ['1', 'Review this deck + Q&A on platform capabilities', '20 min', 'Don B.'],
    ['2', 'Sage priorities: Which NF1 questions matter most?', '20 min', 'Sage team'],
    ['3', 'Live demo: Run one Sage-chosen question through the protocol', '25 min', 'Don B.'],
    ['4', 'Discuss collaboration framework + next steps', '15 min', 'Joint'],
    [
      { text: '', options: { fill: { color: TEAL_P } } },
      { text: 'Total', options: { fill: { color: TEAL_P }, color: WHITE_P, bold: true, fontSize: 9 } },
      { text: '80 min', options: { fill: { color: TEAL_P }, color: WHITE_P, bold: true, fontSize: 9, align: 'center' } },
      { text: '', options: { fill: { color: TEAL_P } } }
    ]
  ];
  if (p13.length > 0) {
    s13.addTable(agendaData, { ...p13[0], colW: [0.8, 5.2, 1.2, 1.2], border: { pt: 0.5, color: 'D1D5DB' }, valign: 'middle', fontSize: 9, rowH: [0.4, 0.45, 0.45, 0.45, 0.45, 0.4] });
  }

  // Slide 14: Thank You
  const { slide: s14 } = await html2pptx(path.join(SLIDES, 'slide14.html'), pptx);
  s14.addNotes(NOTES[14]);

  console.log('Saving PPTX...');
  await pptx.writeFile({ fileName: OUTPUT });
  console.log('Done! Output:', OUTPUT);
}

build().catch(err => { console.error('Build failed:', err); process.exit(1); });
