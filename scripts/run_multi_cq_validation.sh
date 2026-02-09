#!/bin/bash
set -euo pipefail

# Multi-Agent Competency Question Validation
# Creates isolated git worktrees and launches parallel CQ validation agents

# Configuration
TIMESTAMP=$(date +%Y-%m-%dT%H-%M)
WORKTREE_BASE="/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-${TIMESTAMP}"
MAIN_REPO="/home/donbr/ai2026/lifesciences-deepagents"

# CQ Definitions
declare -A CQ_NAMES=(
  ["cq1"]="fop-mechanism"
  ["cq7"]="ngly1-repurposing"
  ["cq11"]="p53-mdm2-nutlin"
  ["cq8"]="arid1a-synleth"
)

declare -A CQ_QUESTIONS=(
  ["cq1"]="By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"
  ["cq7"]="For NGLY1 deficiency, what are the associated genes, and what existing drugs target proteins in those pathways?"
  ["cq11"]="How do we build and validate a knowledge graph for the p53-MDM2-Nutlin therapeutic axis?"
  ["cq8"]="How can we identify therapeutic strategies for ARID1A-deficient Ovarian Cancer using synthetic lethality?"
)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Phase 1: Setup Worktrees
setup_worktrees() {
  log_info "Creating worktree base directory: ${WORKTREE_BASE}"
  mkdir -p "${WORKTREE_BASE}"

  cd "${MAIN_REPO}"

  # Verify main branch is clean
  if [[ -n $(git status --porcelain) ]]; then
    log_warning "Main repo has uncommitted changes. Continuing anyway..."
  fi

  # Get current commit
  CURRENT_COMMIT=$(git rev-parse HEAD)

  # Create worktrees for each CQ
  for cq in "${!CQ_NAMES[@]}"; do
    worktree_path="${WORKTREE_BASE}/${cq}-${CQ_NAMES[$cq]}"
    log_info "Creating worktree: ${worktree_path}"

    # Create worktree at current commit (detached HEAD) to avoid branch conflict
    git worktree add --detach "${worktree_path}" "${CURRENT_COMMIT}"

    # Create output directory
    output_dir="${worktree_path}/output/${cq}-${TIMESTAMP}"
    mkdir -p "${output_dir}"

    log_success "Worktree created: ${worktree_path}"
    log_info "Output directory: ${output_dir}"
  done

  log_success "All worktrees created successfully"
}

# Phase 2: Generate Agent Instructions
generate_agent_instructions() {
  local cq=$1
  local worktree_path="${WORKTREE_BASE}/${cq}-${CQ_NAMES[$cq]}"
  local output_dir="${worktree_path}/output/${cq}-${TIMESTAMP}"

  cat > "${worktree_path}/agent-instructions.md" <<EOF
# Agent Instructions for ${cq}

## Task
Execute Fuzzy-to-Fact protocol for competency question ${cq}:

**Question**: ${CQ_QUESTIONS[$cq]}

## Working Directory
\`${worktree_path}\`

## Output Directory
\`${output_dir}\`

## Execution Steps

1. **Set Working Directory**
   \`\`\`bash
   cd ${worktree_path}
   \`\`\`

2. **Execute Graph Builder Skill**
   Use the \`lifesciences-graph-builder\` skill to run the Fuzzy-to-Fact protocol:
   - ANCHOR: Identify key entities (genes, proteins, drugs, diseases)
   - ENRICH: Get functional annotations and metadata
   - EXPAND: Discover interactions and pathways
   - TRAVERSE_DRUGS: Find therapeutic compounds (if applicable)
   - TRAVERSE_TRIALS: Find clinical trials (if applicable)
   - VALIDATE: Verify all claims with evidence
   - PERSIST: Save to knowledge graph

3. **Generate Report**
   Use the \`lifesciences-reporting\` skill to create:
   - Professional report with evidence grading (L1-L4)
   - CURIE-prefixed identifiers for all entities
   - Source attribution for all claims

4. **Quality Review**
   Use the \`lifesciences-reporting-quality-review\` skill to validate:
   - Protocol compliance (10 dimensions)
   - LOCATE→RETRIEVE pattern adherence
   - Evidence grading presence
   - No hallucinated entities

5. **Save Metadata**
   Create \`${output_dir}/validation-metadata.json\`:
   \`\`\`json
   {
     "cq_id": "${cq}",
     "start_time": "$(date -Iseconds)",
     "end_time": "[FILL AFTER COMPLETION]",
     "duration_seconds": "[CALCULATE]",
     "git": {
       "branch": "main",
       "commit": "$(cd ${MAIN_REPO} && git rev-parse --short HEAD)",
       "worktree": "${worktree_path}"
     },
     "skills_version": "v2.0-evidence-grading",
     "environment": {
       "output_directory": "${output_dir}",
       "prior_reports_count": 0,
       "isolation_status": "CLEAN"
     }
   }
   \`\`\`

## Special Instructions for ${cq}

EOF

  # Add CQ-specific instructions
  case $cq in
    cq1)
      cat >> "${worktree_path}/agent-instructions.md" <<'EOF'
### cq1: FOP Mechanism (Gain-of-Function Filtering)

**Critical Requirement**: Apply gain-of-function filtering

- ✅ Palovarotene is a RARγ **agonist** (ACTIVATES RARG)
- ❌ Eptotermin Alfa is a BMP **agonist** (ACTIVATES ACVR1) - EXCLUDE
- ❌ Dibotermin Alfa is a BMP **agonist** (ACTIVATES ACVR1) - EXCLUDE

**Rationale**: FOP is caused by gain-of-function mutation in ACVR1 (R206H). BMP agonists would WORSEN the condition.

**Expected Output**:
- Palovarotene→RARG→ACVR1→FOP pathway
- Explicit exclusion of BMP agonists with rationale
- GoF mentions ≥10 in report
- Evidence grading L3-L4 for key claims

**Success Criteria**:
- [ ] Palovarotene identified as RARγ agonist
- [ ] BMP agonists explicitly EXCLUDED with rationale
- [ ] GoF filtering documented in report
- [ ] CURIE coverage 100%
EOF
      ;;
    cq7)
      cat >> "${worktree_path}/agent-instructions.md" <<'EOF'
### cq7: NGLY1 Multi-Hop Drug Repurposing

**Required Reasoning**:
1. NGLY1 deficiency (MONDO:0014109) → NGLY1 gene (HGNC:17646)
2. NGLY1 → N-glycanase pathway (WikiPathways)
3. Pathway → Member proteins (STRING interactions)
4. Proteins → Druggable targets (ChEMBL)
5. Targets → Drug candidates (ChEMBL compounds)

**Expected Output**:
- Multi-hop pathway: Disease→Gene→Pathway→Proteins→Drugs
- Federated evidence from ≥3 databases (HGNC, WikiPathways, STRING, ChEMBL)
- Pathway context with member proteins
- Drug candidates mapped to specific pathway targets

**Success Criteria**:
- [ ] N-glycanase pathway identified (WP:WP5078 or similar)
- [ ] Pathway proteins retrieved with STRING interactions
- [ ] Drug candidates mapped to pathway targets
- [ ] Multi-source evidence present
EOF
      ;;
    cq11)
      cat >> "${worktree_path}/agent-instructions.md" <<'EOF'
### cq11: p53-MDM2-Nutlin Pathway Validation

**Required Validation**:
1. TP53-MDM2 interaction via STRING (expect score 0.999)
2. Nutlin-3 as MDM2 inhibitor via ChEMBL
3. Clean 3-node graph (TP53, MDM2, Nutlin-3)
4. No hallucinated interactions

**Expected Output**:
- TP53 (HGNC:11998) ↔ MDM2 (HGNC:6973) interaction (STRING score ≥0.99)
- Nutlin-3 (CHEMBL:191334) → MDM2 inhibition mechanism
- Clean PPI graph with verified edges
- Evidence grading L4 (experimental validation)

**Success Criteria**:
- [ ] TP53↔MDM2 interaction validated via STRING
- [ ] Nutlin-3 confirmed as MDM2 inhibitor
- [ ] Clean 3-node graph (no extra entities)
- [ ] No hallucinated interactions
EOF
      ;;
    cq8)
      cat >> "${worktree_path}/agent-instructions.md" <<'EOF'
### cq8: ARID1A Synthetic Lethality

**Required Reasoning**:
1. ARID1A (HGNC:11110) → SWI/SNF complex member
2. SWI/SNF complex expansion via STRING
3. Synthetic lethal partners (EZH2, ATR)
4. EZH2 inhibitors (Tazemetostat)
5. Clinical trial validation (NCT03348631)

**Expected Output**:
- ARID1A → SWI/SNF complex (≥5 members)
- EZH2 identified as synthetic lethal partner (PRC2 complex)
- Tazemetostat (CHEMBL:3414621) as FDA-approved EZH2 inhibitor
- Clinical trial NCT03348631 validated

**Success Criteria**:
- [ ] SWI/SNF complex expanded (≥5 members)
- [ ] EZH2 identified as synthetic lethal target
- [ ] Tazemetostat confirmed as FDA-approved
- [ ] Clinical trial NCT03348631 validated
EOF
      ;;
  esac

  log_success "Agent instructions generated: ${worktree_path}/agent-instructions.md"
}

# Phase 3: Display Parallel Execution Instructions
display_execution_instructions() {
  log_info "Worktree setup complete. Ready for parallel agent execution."
  echo ""
  echo "=========================================="
  echo "PARALLEL AGENT EXECUTION INSTRUCTIONS"
  echo "=========================================="
  echo ""
  echo "Launch 4 agents in parallel by sending a SINGLE message with 4 Task tool calls:"
  echo ""

  for cq in cq1 cq7 cq11 cq8; do
    worktree_path="${WORKTREE_BASE}/${cq}-${CQ_NAMES[$cq]}"
    echo "Agent ${cq}: Execute ${CQ_QUESTIONS[$cq]}"
    echo "  Worktree: ${worktree_path}"
    echo "  Instructions: ${worktree_path}/agent-instructions.md"
    echo ""
  done

  echo "=========================================="
  echo "MONITORING"
  echo "=========================================="
  echo ""
  echo "Monitor agent progress with:"
  echo "  watch -n 5 'for dir in ${WORKTREE_BASE}/cq*; do echo \"\$dir:\"; ls -lh \"\$dir/output/\" 2>/dev/null | wc -l; done'"
  echo ""
  echo "=========================================="
}

# Main execution
main() {
  log_info "Starting Multi-CQ Validation Run: ${TIMESTAMP}"
  log_info "Worktree base: ${WORKTREE_BASE}"

  # Phase 1: Setup worktrees
  setup_worktrees

  # Phase 2: Generate agent instructions
  for cq in cq1 cq7 cq11 cq8; do
    generate_agent_instructions "${cq}"
  done

  # Phase 3: Display execution instructions
  display_execution_instructions

  log_success "Setup complete! Ready for parallel agent execution."
}

# Run main
main
