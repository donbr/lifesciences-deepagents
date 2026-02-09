# Validation Scripts

Scripts for multi-CQ validation with worktree isolation and automated scoring.

---

## Scripts Overview

### 1. `run_multi_cq_validation.sh`

**Purpose**: Setup isolated git worktrees for parallel CQ validation

**Usage**:
```bash
./scripts/run_multi_cq_validation.sh
```

**What it does**:
1. Creates timestamp-based worktree directory (`cq-validation-{timestamp}/`)
2. Creates 4 isolated worktrees (cq1, cq7, cq11, cq8)
3. Creates empty output directories for each CQ
4. Generates agent instruction files with CQ-specific requirements
5. Displays parallel execution instructions

**Output**:
```
/home/donbr/ai2026/lifesciences-deepagents-worktrees/
└── cq-validation-2026-02-08T14-20/
    ├── cq1-fop-mechanism/
    │   ├── agent-instructions.md
    │   └── output/cq1-2026-02-08T14-20/
    ├── cq7-ngly1-repurposing/
    ├── cq11-p53-mdm2-nutlin/
    └── cq8-arid1a-synleth/
```

**Notes**:
- Uses detached HEAD worktrees to avoid branch conflicts
- All worktrees share git objects (space-efficient)
- Clean environments prevent LLM contamination

---

### 2. `generate_cq_scorecard.py`

**Purpose**: Generate validation scorecard for a single CQ

**Usage**:
```bash
./scripts/generate_cq_scorecard.py cq1 /path/to/output/dir/ --save
```

**Parameters**:
- `cq_id`: Competency question ID (cq1, cq7, cq11, cq8)
- `output_dir`: Directory containing report files
- `--json`: Output JSON instead of markdown (optional)
- `--save`: Save scorecard to output directory (optional)

**What it does**:
1. Reads report markdown file
2. Evaluates 5 dimensions (CURIE coverage, source attribution, LOCATE→RETRIEVE, evidence grading, GoF filtering)
3. Calculates total score (/20 points)
4. Generates scorecard markdown and JSON

**Output Files**:
- `{cq_id}-scorecard.md` - Human-readable scorecard
- `{cq_id}-scorecard.json` - Machine-readable results

**Example Output**:
```
# CQ1 Validation Scorecard

**Timestamp**: 2026-02-08T14:30:00
**Total**: 19/20 (95.0%) ✅ PASS

## Protocol Compliance

| Dimension | Score | Max | Evidence |
|-----------|-------|-----|----------|
| CURIE Coverage | 4 | 4 | CURIEs found in report |
| Source Attribution | 4 | 4 | [Source:...] citations |
| LOCATE→RETRIEVE | 4 | 4 | Protocol adherence |
| Evidence Grading | 4 | 4 | L1-L4 presence |
| GoF Filtering | 3 | 4 | BMP agonist exclusion |
```

**Scoring Criteria**:

| Dimension | 4 pts | 3 pts | 2 pts | 1 pt | 0 pts |
|-----------|-------|-------|-------|------|-------|
| **CURIE Coverage** | ≥10 CURIEs | 7-9 | 5-6 | 3-4 | <3 |
| **Source Attribution** | ≥15 citations | 10-14 | 5-9 | 2-4 | <2 |
| **LOCATE→RETRIEVE** | Both ≥5 | Both ≥3 | Both ≥1 | One ≥1 | Neither |
| **Evidence Grading** | L1-L4 + median + L3-L4 | L1-L4 + L3 | 2+ levels | 1 level | None |
| **GoF Filtering** | Palo + Exclusion + ≥10 GoF | Palo + Exclusion + ≥5 GoF | Palo + Exclusion | Palo or Exclusion | Neither |

---

### 3. `generate_comparison_dashboard.py`

**Purpose**: Aggregate results from multiple CQs into comparison dashboard

**Usage**:
```bash
./scripts/generate_comparison_dashboard.py /path/to/worktree-base/
```

**Parameters**:
- `validation_run_dir`: Base directory containing all CQ worktrees
- `--output-dir`: Custom output directory (optional, defaults to validation_run_dir)

**What it does**:
1. Finds all CQ scorecards in validation run directory
2. Calculates aggregate statistics (average score, pass rate, dimension averages)
3. Generates comparison table
4. Analyzes terminology usage across reports
5. Provides insights and recommendations

**Output Files**:
- `aggregate-results.json` - Combined scores and statistics
- `comparison-dashboard.md` - Cross-CQ comparison markdown

**Example Output**:
```
# Multi-CQ Validation Dashboard

**Run**: cq-validation-2026-02-08T14-20
**Status**: 4/4 PASS ✅

## Score Summary

| CQ | Name | Score | Percentage | Status |
|----|------|-------|------------|--------|
| cq1 | FOP Mechanism | 19/20 | 95.0% | ✅ PASS |
| cq7 | NGLY1 Repurposing | 18/20 | 90.0% | ✅ PASS |
| cq11 | p53-MDM2-Nutlin | 20/20 | 100.0% | ✅ PASS |
| cq8 | ARID1A SynLeth | 17/20 | 85.0% | ✅ PASS |

**Average Score**: 18.5/20 (92.5%)
```

---

### 4. `cleanup_validation_worktrees.sh`

**Purpose**: Archive old validation worktrees and clean up disk space

**Usage**:
```bash
./scripts/cleanup_validation_worktrees.sh [days_to_keep]
```

**Parameters**:
- `days_to_keep`: Number of days to retain (default: 7)

**What it does**:
1. Finds worktrees older than cutoff date
2. Archives output directories to `.tar.gz`
3. Removes worktrees from git
4. Displays summary

**Example**:
```bash
# Keep last 7 days
./scripts/cleanup_validation_worktrees.sh 7

# Keep last 30 days
./scripts/cleanup_validation_worktrees.sh 30
```

**Archive Location**:
```
archives/validation-runs/
├── cq-validation-2026-02-01T10-30.tar.gz
├── cq-validation-2026-02-02T14-20.tar.gz
└── cq-validation-2026-02-08T14-20.tar.gz
```

---

## Complete Validation Workflow

### Step 1: Setup Worktrees

```bash
# Create isolated worktrees for 4 CQs
./scripts/run_multi_cq_validation.sh
```

**Output**: Worktree directories with agent instructions

---

### Step 2: Launch Parallel Agents

Send a **single message** with 4 Task tool calls to launch agents in parallel.

Each agent reads its instruction file:
```
/path/to/worktree/agent-instructions.md
```

Agents execute:
1. Fuzzy-to-Fact protocol
2. Report generation with evidence grading
3. Quality review
4. Metadata creation

---

### Step 3: Generate Scorecards

After agents complete:

```bash
# Generate scorecard for each CQ
for cq in cq1 cq7 cq11 cq8; do
  output_dir=$(find /path/to/worktree-base/${cq}-*/output -type d -name "${cq}-*" | head -1)
  ./scripts/generate_cq_scorecard.py ${cq} ${output_dir} --save
done
```

**Output**: Individual scorecards in each output directory

---

### Step 4: Generate Comparison Dashboard

```bash
# Aggregate all CQ results
./scripts/generate_comparison_dashboard.py /path/to/worktree-base/
```

**Output**:
- `aggregate-results.json`
- `comparison-dashboard.md`

---

### Step 5: Review Results

```bash
# View comparison dashboard
cat /path/to/worktree-base/comparison-dashboard.md

# View individual scorecards
cat /path/to/output/cq1-scorecard.md
```

---

### Step 6: Cleanup (Optional)

```bash
# Archive old worktrees (keep last 7 days)
./scripts/cleanup_validation_worktrees.sh 7
```

---

## Monitoring Progress

### Real-time Monitoring

```bash
# Watch output directory creation
watch -n 5 'for dir in /path/to/worktree-base/cq*; do echo "$dir:"; ls -lh "$dir/output/" 2>/dev/null | wc -l; done'
```

### Check File Sizes

```bash
# Find all report files
find /path/to/worktree-base -name "*-report-*.md" -exec ls -lh {} \;

# Find all knowledge graphs
find /path/to/worktree-base -name "*-knowledge-graph-*.json" -exec ls -lh {} \;
```

---

## Troubleshooting

### Scorecard Generation Fails

**Problem**: Script can't find report file

**Solution**:
```bash
# List files in output directory
ls -la /path/to/output/

# Verify report exists with expected name pattern
find /path/to/output -name "*-report-*.md"
```

### Comparison Dashboard Missing CQs

**Problem**: Some scorecards not found

**Solution**:
```bash
# Manually generate missing scorecards
./scripts/generate_cq_scorecard.py cq7 /path/to/output/ --save

# Re-run dashboard generator
./scripts/generate_comparison_dashboard.py /path/to/worktree-base/
```

### Worktree Conflicts

**Problem**: Git worktree add fails

**Solution**:
```bash
# List existing worktrees
git worktree list

# Remove stale worktrees
git worktree remove /path/to/stale/worktree --force

# Re-run setup
./scripts/run_multi_cq_validation.sh
```

---

## Integration with Validation Protocol

These scripts implement the **Multi-CQ Validation Protocol** documented in:
`docs/multi-cq-validation-protocol.md`

Key principles:
1. **Worktree isolation** - Prevent LLM contamination
2. **Parallel execution** - Run multiple CQs concurrently
3. **Automated scoring** - Consistent validation criteria
4. **Timestamp tracking** - Full ISO 8601 timestamps
5. **Archive management** - Keep disk space under control

---

## Success Criteria

**PASS** if:
- ✅ 3/4 CQs score ≥17/20
- ✅ All CQs have CURIE coverage ≥95%
- ✅ No anti-pattern drugs (for cq1)
- ✅ All metadata files have ISO timestamps
- ✅ Worktree isolation maintained

**PARTIAL** if:
- ⚠️ 2/4 CQs score ≥17/20
- ⚠️ 1 CQ has CURIE coverage <95%

**FAIL** if:
- ❌ <2 CQs score ≥17/20
- ❌ Anti-pattern drugs present
- ❌ Hallucinated entities detected

---

## References

- **Protocol**: `docs/multi-cq-validation-protocol.md`
- **CQ Catalog**: `reference/competency_questions/competency-questions-catalog.md`
- **Output Isolation**: `docs/output-directory-isolation-best-practice.md`
