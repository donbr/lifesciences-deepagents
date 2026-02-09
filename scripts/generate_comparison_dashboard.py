#!/usr/bin/env python3
"""
Generate multi-CQ comparison dashboard from validation scorecards.

Aggregates results from multiple CQ validations and creates:
- Aggregate results JSON
- Comparison dashboard markdown
- Cross-CQ insights
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict


class ComparisonDashboard:
    """Generate comparison dashboard from multiple CQ scorecards."""

    def __init__(self, validation_run_dir: Path):
        self.validation_run_dir = validation_run_dir
        self.run_name = validation_run_dir.name
        self.scorecards = {}
        self.aggregate_data = {}

    def load_scorecards(self):
        """Load all CQ scorecards from validation run directory."""
        # Find all cq directories
        cq_dirs = [d for d in self.validation_run_dir.iterdir() if d.is_dir() and d.name.startswith("cq")]

        for cq_dir in cq_dirs:
            # Find scorecard JSON files in nested output directories
            scorecard_files = list(cq_dir.rglob("*-scorecard.json"))

            if scorecard_files:
                scorecard_path = scorecard_files[0]
                with open(scorecard_path) as f:
                    scorecard = json.load(f)
                    self.scorecards[scorecard["cq_id"]] = scorecard
                    print(f"Loaded scorecard: {scorecard['cq_id']} from {scorecard_path}")
            else:
                print(f"Warning: No scorecard found for {cq_dir.name}")

    def calculate_aggregate(self) -> Dict:
        """Calculate aggregate statistics across all CQs."""
        if not self.scorecards:
            return {"error": "No scorecards loaded"}

        total_cqs = len(self.scorecards)
        passed = sum(1 for s in self.scorecards.values() if s["status"] == "PASS")
        partial = sum(1 for s in self.scorecards.values() if s["status"] == "PARTIAL")
        failed = sum(1 for s in self.scorecards.values() if s["status"] == "FAIL")

        # Calculate average scores
        avg_score = sum(s["total_score"] for s in self.scorecards.values()) / total_cqs
        avg_percentage = sum(s["percentage"] for s in self.scorecards.values()) / total_cqs

        # Dimension-specific averages
        dimension_scores = {}
        for scorecard in self.scorecards.values():
            for dim, data in scorecard["scores"].items():
                if data["max"] > 0:
                    if dim not in dimension_scores:
                        dimension_scores[dim] = []
                    dimension_scores[dim].append(data["score"] / data["max"])

        dimension_averages = {
            dim: round(sum(scores) / len(scores) * 100, 1)
            for dim, scores in dimension_scores.items()
        }

        self.aggregate_data = {
            "validation_run": self.run_name,
            "timestamp": datetime.now().isoformat(),
            "cqs_tested": total_cqs,
            "cqs_passed": passed,
            "cqs_partial": partial,
            "cqs_failed": failed,
            "average_score": round(avg_score, 1),
            "average_percentage": round(avg_percentage, 1),
            "dimension_averages": dimension_averages,
            "detailed_results": {
                cq_id: {
                    "score": f"{s['total_score']}/{s['max_score']}",
                    "percentage": s["percentage"],
                    "status": s["status"],
                }
                for cq_id, s in sorted(self.scorecards.items())
            },
        }

        return self.aggregate_data

    def generate_markdown_dashboard(self) -> str:
        """Generate markdown comparison dashboard."""
        if not self.aggregate_data:
            self.calculate_aggregate()

        agg = self.aggregate_data

        md = f"""# Multi-CQ Validation Dashboard

**Run**: `{agg['validation_run']}`
**Timestamp**: {agg['timestamp']}
**Status**: {agg['cqs_passed']}/{agg['cqs_tested']} PASS {'✅' if agg['cqs_passed'] == agg['cqs_tested'] else '⚠️'}

## Score Summary

| CQ | Name | Score | Percentage | Status |
|----|------|-------|------------|--------|
"""

        # CQ names for display
        cq_names = {
            "cq1": "FOP Mechanism",
            "cq7": "NGLY1 Repurposing",
            "cq11": "p53-MDM2-Nutlin",
            "cq8": "ARID1A SynLeth",
        }

        for cq_id, result in agg["detailed_results"].items():
            status_emoji = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "PARTIAL" else "❌"
            cq_name = cq_names.get(cq_id, cq_id)
            md += f"| {cq_id} | {cq_name} | {result['score']} | {result['percentage']}% | {status_emoji} {result['status']} |\n"

        md += f"""
**Average Score**: {agg['average_score']}/20 ({agg['average_percentage']}%)

## Dimension Performance

| Dimension | Average Score |
|-----------|---------------|
"""

        for dim, avg in sorted(agg["dimension_averages"].items()):
            dim_display = dim.replace("_", " ").title()
            md += f"| {dim_display} | {avg}% |\n"

        md += """
## Validation Language Coverage

Analysis of key terminology usage across reports:

| Term | cq1 | cq7 | cq11 | cq8 | Notes |
|------|-----|-----|------|-----|-------|
"""

        # Read reports and count terminology
        term_counts = {
            "gain-of-function": {},
            "LOCATE": {},
            "RETRIEVE": {},
            "L1-L4": {},
            "[Source:": {},
        }

        for cq_id, scorecard in self.scorecards.items():
            report_path = Path(scorecard.get("report_file", ""))
            if report_path.exists():
                report_text = report_path.read_text()
                for term in term_counts:
                    if term == "L1-L4":
                        count = report_text.count("L1") + report_text.count("L2") + report_text.count("L3") + report_text.count("L4")
                    else:
                        count = report_text.count(term)
                    term_counts[term][cq_id] = count

        for term, counts in term_counts.items():
            cq1_count = counts.get("cq1", 0)
            cq7_count = counts.get("cq7", 0)
            cq11_count = counts.get("cq11", 0)
            cq8_count = counts.get("cq8", 0)

            # Add notes
            notes = ""
            if term == "gain-of-function":
                notes = "cq1 only (FOP mechanism)"
            elif term in ["LOCATE", "RETRIEVE"]:
                notes = "Protocol adherence"
            elif term == "L1-L4":
                notes = "Evidence grading"
            elif term == "[Source:":
                notes = "Citation count"

            md += f"| {term} | {cq1_count} | {cq7_count} | {cq11_count} | {cq8_count} | {notes} |\n"

        md += """
## Insights

"""

        # Generate insights
        if agg["cqs_passed"] == agg["cqs_tested"]:
            md += "1. **Baseline reproducibility**: All CQs passed validation ✅\n"
        else:
            md += f"1. **Validation success**: {agg['cqs_passed']}/{agg['cqs_tested']} CQs passed\n"

        if "curie_coverage" in agg["dimension_averages"]:
            curie_avg = agg["dimension_averages"]["curie_coverage"]
            if curie_avg >= 90:
                md += f"2. **CURIE coverage**: Excellent ({curie_avg}%)\n"
            else:
                md += f"2. **CURIE coverage**: Needs improvement ({curie_avg}%)\n"

        if "evidence_grading" in agg["dimension_averages"]:
            ev_avg = agg["dimension_averages"]["evidence_grading"]
            if ev_avg >= 75:
                md += f"3. **Evidence grading**: Strong L1-L4 usage ({ev_avg}%)\n"
            else:
                md += f"3. **Evidence grading**: Inconsistent application ({ev_avg}%)\n"

        if "gof_filtering" in agg["dimension_averages"]:
            gof_avg = agg["dimension_averages"]["gof_filtering"]
            if gof_avg >= 75:
                md += f"4. **Gain-of-function filtering**: Properly applied ({gof_avg}%)\n"
            else:
                md += f"4. **Gain-of-function filtering**: Needs attention ({gof_avg}%)\n"

        md += f"""
## Files

- **Aggregate results**: `aggregate-results.json`
- **Comparison dashboard**: `comparison-dashboard.md`
- **Individual scorecards**: `cq*/output/*/cq*-scorecard.md`

## Next Steps

"""

        if agg["cqs_passed"] < agg["cqs_tested"]:
            md += "- Review failed/partial CQs and identify root causes\n"
            md += "- Improve protocol adherence in weak dimensions\n"
        else:
            md += "- Document validation protocol for reproducibility\n"
            md += "- Expand to additional competency questions\n"

        md += "- Archive validation run for future reference\n"
        md += "- Update baseline scores for regression detection\n"

        return md

    def save_results(self, output_dir: Path):
        """Save aggregate results and dashboard."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save aggregate JSON
        json_path = output_dir / "aggregate-results.json"
        with open(json_path, "w") as f:
            json.dump(self.aggregate_data, f, indent=2)
        print(f"Saved aggregate results: {json_path}")

        # Save markdown dashboard
        md_path = output_dir / "comparison-dashboard.md"
        dashboard = self.generate_markdown_dashboard()
        md_path.write_text(dashboard)
        print(f"Saved comparison dashboard: {md_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate multi-CQ comparison dashboard"
    )
    parser.add_argument(
        "validation_run_dir",
        type=Path,
        help="Validation run directory containing CQ worktrees",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for results (default: validation_run_dir)",
    )

    args = parser.parse_args()

    output_dir = args.output_dir or args.validation_run_dir

    # Create dashboard
    dashboard = ComparisonDashboard(args.validation_run_dir)
    dashboard.load_scorecards()
    dashboard.calculate_aggregate()
    dashboard.save_results(output_dir)

    # Print summary
    print("\n" + "=" * 50)
    print("COMPARISON DASHBOARD GENERATED")
    print("=" * 50)
    print(f"Validation run: {dashboard.run_name}")
    print(f"CQs tested: {dashboard.aggregate_data['cqs_tested']}")
    print(f"CQs passed: {dashboard.aggregate_data['cqs_passed']}")
    print(f"Average score: {dashboard.aggregate_data['average_score']}/20")
    print(f"Output: {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()
