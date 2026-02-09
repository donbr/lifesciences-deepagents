# Multi-CQ Validation Protocol

**Version**: 1.0
**Date**: 2026-02-08
**Purpose**: Validate multiple competency questions in parallel using isolated worktree environments

---

## Overview

This protocol enables parallel validation of multiple competency questions (CQs) using:

1. **Worktree isolation** - Separate git worktrees per CQ to prevent cross-contamination
2. **Multi-agent execution** - Run 3-4 CQs concurrently with dedicated agents
3. **Timestamp tracking** - Full ISO 8601 timestamps for precise execution tracking
4. **Automated validation** - Scorecard generation and comparison dashboards

**Critical Insight**: Fresh environments prevent LLM contamination from prior runs (14 vs 4 GoF mentions in isolated tests)

---

## Quick Start

### 1. Setup Worktrees

```bash
./scripts/run_multi_cq_validation.sh
```

This creates:
- `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-{timestamp}/`
  - `cq1-fop-mechanism/`
  - `cq7-ngly1-repurposing/`
  - `cq11-p53-mdm2-nutlin/`
  - `cq8-arid1a-synleth/`

Each worktree contains:
- Isolated codebase (detached HEAD from main)
- Empty `output/cq{N}-{timestamp}/` directory
- `agent-instructions.md` with CQ-specific requirements

### 2. Launch Parallel Agents

Launch 4 agents in parallel by sending a **single message** with 4 Task tool calls.

Read each agent's instructions file and execute:
- `/path/to/worktree/agent-instructions.md`

Each agent will:
1. Execute Fuzzy-to-Fact protocol
2. Generate professional report with evidence grading
3. Run quality review
4. Save metadata with timestamps

### 3. Generate Scorecards

After agents complete, generate scorecards for each CQ:

```bash
./scripts/generate_cq_scorecard.py cq1 /path/to/worktree/output/cq1-{timestamp}/ --save
./scripts/generate_cq_scorecard.py cq7 /path/to/worktree/output/cq7-{timestamp}/ --save
./scripts/generate_cq_scorecard.py cq11 /path/to/worktree/output/cq11-{timestamp}/ --save
./scripts/generate_cq_scorecard.py cq8 /path/to/worktree/output/cq8-{timestamp}/ --save
```

### 4. Generate Comparison Dashboard

Aggregate results across all CQs:

```bash
./scripts/generate_comparison_dashboard.py /path/to/worktree-base/
```

This creates:
- `aggregate-results.json` - Combined scores
- `comparison-dashboard.md` - Cross-CQ comparison

### 5. Cleanup

Archive old worktrees (default: keep last 7 days):

```bash
./scripts/cleanup_validation_worktrees.sh [days_to_keep]
```

---

## Selected Competency Questions

### cq1: FOP Mechanism (DrugMechDB Style)
**Type**: Drug mechanism validation (single-hop)
**Critical Test**: Gain-of-function filtering (Palovarotene vs BMP agonists)
**Expected**: Palovarotene→RARG→ACVR1→FOP path, agonists excluded

### cq7: NGLY1 Drug Repurposing (BioThings Explorer)
**Type**: Multi-hop federated drug discovery
**Critical Test**: Pathway expansion + drug traversal
**Expected**: NGLY1→N-glycanase pathway→pathway proteins→druggable targets

### cq11: p53-MDM2-Nutlin (Pathway Validation)
**Type**: Validated therapeutic axis
**Critical Test**: TP53↔MDM2 interaction (STRING score 0.999), Nutlin-3 mechanism
**Expected**: Clean PPI graph with validated drug mechanism

### cq8: ARID1A Synthetic Lethality
**Type**: Complex reasoning (synthetic lethality + druggability)
**Critical Test**: SWI/SNF complex expansion + EZH2 inhibitor discovery
**Expected**: Synthetic lethality graph with FDA-approved drug

---

## Validation Scorecard Criteria (20 points)

| Dimension | Points | Criteria |
|-----------|--------|----------|
| **CURIE Coverage** | 4 | 100% of entities have database identifiers (HGNC, CHEMBL, etc.) |
| **Source Attribution** | 4 | All claims cited with [Source:...] references (≥15 citations) |
| **LOCATE→RETRIEVE** | 4 | 2-step pattern documented (≥5 occurrences each) |
| **Evidence Grading** | 4 | L1-L4 present, median calculated, L3-L4 for key claims |
| **GoF Filtering** | 4 | BMP agonists excluded with rationale (cq1 only) |

**Pass Threshold**: ≥17/20 points
**Partial**: 14-16 points
**Fail**: <14 points

---

## Worktree Architecture

### Directory Structure

```
/home/donbr/ai2026/lifesciences-deepagents/                    # Main repo
/home/donbr/ai2026/lifesciences-deepagents-worktrees/
├── cq-validation-2026-02-08T14-20/                           # Parent timestamp
│   ├── cq1-fop-mechanism/                                    # Worktree 1
│   │   ├── output/cq1-2026-02-08T14-20/                      # Isolated output
│   │   │   ├── fop-mechanism-report.md
│   │   │   ├── fop-mechanism-knowledge-graph.json
│   │   │   ├── fop-mechanism-quality-review.md
│   │   │   ├── cq1-scorecard.md
│   │   │   ├── cq1-scorecard.json
│   │   │   └── validation-metadata.json
│   │   ├── agent-instructions.md
│   │   └── .git/ (linked to main repo)
│   ├── cq7-ngly1-repurposing/
│   ├── cq11-p53-mdm2-nutlin/
│   ├── cq8-arid1a-synleth/
│   ├── aggregate-results.json
│   └── comparison-dashboard.md
```

### Timestamp Format

**ISO 8601 Extended**: `YYYY-MM-DDTHH-MM-SS` (sortable, filesystem-safe)

**Examples**:
- Parent directory: `cq-validation-2026-02-08T14-20`
- Output subdirs: `cq1-2026-02-08T14-20-45`
- Metadata: `"start_time": "2026-02-08T14:20:45-08:00"` (with timezone)

---

## Metadata Schema

Each CQ generates `validation-metadata.json`:

```json
{
  "cq_id": "cq1",
  "start_time": "2026-02-08T14:20:45-08:00",
  "end_time": "2026-02-08T14:27:33-08:00",
  "duration_seconds": 408,
  "git": {
    "branch": "main",
    "commit": "481a1c7",
    "worktree": "/path/to/worktree"
  },
  "skills_version": "v2.0-evidence-grading",
  "environment": {
    "output_directory": "/path/to/output",
    "prior_reports_count": 0,
    "isolation_status": "CLEAN"
  },
  "validation_scores": {
    "curie_coverage": 1.0,
    "gof_filtering": "PASS",
    "evidence_grading": "PASS",
    "overall": "19/20"
  }
}
```

---

## Success Criteria

**PASS** if:
- ✅ 3/4 CQs score ≥17/20
- ✅ All CQs have CURIE coverage ≥95%
- ✅ No anti-pattern drugs (for cq1)
- ✅ All metadata files have ISO timestamps
- ✅ Worktree isolation maintained (no cross-contamination)

**PARTIAL** if:
- ⚠️ 2/4 CQs score ≥17/20
- ⚠️ 1 CQ has CURIE coverage <95%
- ⚠️ Timestamp format inconsistent

**FAIL** if:
- ❌ <2 CQs score ≥17/20
- ❌ Anti-pattern drugs present in cq1
- ❌ Hallucinated entities detected
- ❌ Worktree contamination

---

## Monitoring

### Real-time Progress

```bash
watch -n 5 'for dir in /path/to/worktree-base/cq*; do echo "$dir:"; ls -lh "$dir/output/" 2>/dev/null | wc -l; done'
```

### Check Agent Status

```bash
# List active agents (if using Task tool)
/tasks

# Check output file sizes
find /path/to/worktree-base -name "*.md" -exec ls -lh {} \;
```

---

## Troubleshooting

### Agent Timeout

If an agent times out (>15 minutes):
1. Check output directory for partial results
2. Review error logs in agent transcript
3. Restart agent with checkpoint resume (if supported)

### Worktree Conflicts

If git worktree add fails:
1. Run `git worktree list` to see existing worktrees
2. Remove stale worktrees: `git worktree remove /path/to/worktree --force`
3. Re-run setup script

### Missing Scorecards

If scorecard generation fails:
1. Verify report files exist: `ls /path/to/output/*.md`
2. Check report format (must contain CURIE identifiers)
3. Run scorecard script with `--json` for debug output

---

## Process Improvements

### 1. Timestamp Tracking Enhancement

**Current**: Date-only (`2026-02-08`)
**Improved**: Full ISO 8601 with timezone
**Benefits**: Precise execution tracking, duration calculations, timezone awareness

### 2. Worktree Cleanup Automation

Archive worktrees older than 7 days automatically:
```bash
./scripts/cleanup_validation_worktrees.sh 7
```

### 3. Parallel Execution Optimization

Launch 4 agents in **single message** with 4 tool calls for maximum efficiency.

### 4. Validation Report Archive

All validation runs stored in:
```
archives/validation-runs/
├── cq-validation-2026-02-08T14-20.tar.gz
├── cq-validation-2026-02-09T10-30.tar.gz
└── index.json  # All validation runs metadata
```

---

## Timeline Estimate

**Setup**: 5 minutes (create worktrees, prepare environment)
**Execution**: 45 minutes (4 agents in parallel, longest CQ = ~15 min)
**Validation**: 10 minutes (run scripts, generate scorecards)
**Review**: 15 minutes (analyze results, document insights)

**Total**: ~75 minutes (1 hour 15 minutes)

---

## References

- **Competency Questions**: `reference/competency_questions/competency-questions-catalog.md`
- **Fuzzy-to-Fact Protocol**: `.claude/skills/lifesciences-graph-builder/SKILL.md`
- **Evidence Grading**: `.claude/skills/lifesciences-reporting/SKILL.md`
- **Quality Review**: `.claude/skills/lifesciences-reporting-quality-review/SKILL.md`
- **Output Isolation**: `docs/output-directory-isolation-best-practice.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial protocol with 4 CQs, worktree isolation, automated scorecards |
