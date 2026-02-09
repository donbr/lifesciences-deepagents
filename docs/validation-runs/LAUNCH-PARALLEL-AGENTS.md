# Launch Parallel Agents - Multi-CQ Validation

**Validation Run**: `cq-validation-2026-02-08T14-20`
**Timestamp**: 2026-02-08T14:20
**Worktree Base**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20`

---

## Agent Launch Instructions

Launch 4 agents in parallel by sending a **SINGLE MESSAGE** with **4 Task tool calls**.

Each agent will read its instruction file and execute the Fuzzy-to-Fact protocol independently in its isolated worktree.

---

## Agent Assignments

### Agent 1: cq1 (FOP Mechanism)

**Worktree**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq1-fop-mechanism`

**Instructions File**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq1-fop-mechanism/agent-instructions.md`

**Output Directory**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq1-fop-mechanism/output/cq1-2026-02-08T14-20`

**Question**: By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?

**Critical Requirement**: Apply gain-of-function filtering to exclude BMP agonists

---

### Agent 2: cq7 (NGLY1 Drug Repurposing)

**Worktree**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq7-ngly1-repurposing`

**Instructions File**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq7-ngly1-repurposing/agent-instructions.md`

**Output Directory**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq7-ngly1-repurposing/output/cq7-2026-02-08T14-20`

**Question**: For NGLY1 deficiency, what are the associated genes, and what existing drugs target proteins in those pathways?

**Critical Requirement**: Multi-hop pathway expansion with federated evidence

---

### Agent 3: cq11 (p53-MDM2-Nutlin)

**Worktree**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq11-p53-mdm2-nutlin`

**Instructions File**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq11-p53-mdm2-nutlin/agent-instructions.md`

**Output Directory**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq11-p53-mdm2-nutlin/output/cq11-2026-02-08T14-20`

**Question**: How do we build and validate a knowledge graph for the p53-MDM2-Nutlin therapeutic axis?

**Critical Requirement**: Validate TP53↔MDM2 interaction with STRING (expect score 0.999)

---

### Agent 4: cq8 (ARID1A Synthetic Lethality)

**Worktree**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq8-arid1a-synleth`

**Instructions File**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq8-arid1a-synleth/agent-instructions.md`

**Output Directory**: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq8-arid1a-synleth/output/cq8-2026-02-08T14-20`

**Question**: How can we identify therapeutic strategies for ARID1A-deficient Ovarian Cancer using synthetic lethality?

**Critical Requirement**: SWI/SNF complex expansion + EZH2 inhibitor discovery

---

## Monitoring Progress

### Real-time Progress Monitor

```bash
watch -n 5 'for dir in /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq*; do echo "$dir:"; ls -lh "$dir/output/" 2>/dev/null | wc -l; done'
```

### Check Individual Agent Output

```bash
# cq1
ls -lh /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq1-fop-mechanism/output/cq1-2026-02-08T14-20/

# cq7
ls -lh /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq7-ngly1-repurposing/output/cq7-2026-02-08T14-20/

# cq11
ls -lh /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq11-p53-mdm2-nutlin/output/cq11-2026-02-08T14-20/

# cq8
ls -lh /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq8-arid1a-synleth/output/cq8-2026-02-08T14-20/
```

---

## Expected Outputs (Per Agent)

Each agent should generate:

1. **Report**: `{cq}-{name}-report-{timestamp}.md`
   - Professional format with evidence grading (L1-L4)
   - CURIE identifiers for all entities
   - Source attribution with [Source:...] citations

2. **Knowledge Graph**: `{cq}-{name}-knowledge-graph-{timestamp}.json`
   - Nodes with CURIEs
   - Edges with evidence sources
   - Metadata

3. **Quality Review**: `{cq}-{name}-quality-review-{timestamp}.md`
   - 10-dimension evaluation
   - Protocol compliance check

4. **Metadata**: `validation-metadata.json`
   - Start/end timestamps
   - Git commit info
   - Execution environment

---

## Post-Execution Steps

After all 4 agents complete:

### 1. Generate Scorecards

```bash
cd /home/donbr/ai2026/lifesciences-deepagents

# cq1
./scripts/generate_cq_scorecard.py cq1 /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq1-fop-mechanism/output/cq1-2026-02-08T14-20/ --save

# cq7
./scripts/generate_cq_scorecard.py cq7 /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq7-ngly1-repurposing/output/cq7-2026-02-08T14-20/ --save

# cq11
./scripts/generate_cq_scorecard.py cq11 /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq11-p53-mdm2-nutlin/output/cq11-2026-02-08T14-20/ --save

# cq8
./scripts/generate_cq_scorecard.py cq8 /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/cq8-arid1a-synleth/output/cq8-2026-02-08T14-20/ --save
```

### 2. Generate Comparison Dashboard

```bash
./scripts/generate_comparison_dashboard.py /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/
```

### 3. Review Results

```bash
# View comparison dashboard
cat /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/comparison-dashboard.md

# View aggregate JSON
cat /home/donbr/ai2026/lifesciences-deepagents-worktrees/cq-validation-2026-02-08T14-20/aggregate-results.json
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
- ❌ Worktree contamination (agents read other CQ outputs)

---

## Notes

- All worktrees are at commit `481a1c7` (detached HEAD)
- Each worktree has an empty output directory (isolation_status: CLEAN)
- Agent instructions include CQ-specific success criteria
- Total estimated execution time: ~45 minutes (parallel)
