#!/usr/bin/env python3
"""
Generate validation scorecard for competency question reports.

Evaluates reports against protocol requirements:
- CURIE coverage
- Source attribution
- Evidence grading (L1-L4)
- LOCATE→RETRIEVE pattern
- Gain-of-function filtering (cq1 only)
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class CQScorecard:
    """Scorecard for evaluating CQ validation results."""

    def __init__(self, cq_id: str, output_dir: Path):
        self.cq_id = cq_id
        self.output_dir = output_dir
        self.report_path = self._find_report()
        self.kg_path = self._find_knowledge_graph()
        self.metadata_path = output_dir / "validation-metadata.json"
        self.scores = {}
        self.total_score = 0
        self.max_score = 20

    def _find_report(self) -> Optional[Path]:
        """Find report markdown file."""
        report_files = list(self.output_dir.glob("*-report-*.md"))
        return report_files[0] if report_files else None

    def _find_knowledge_graph(self) -> Optional[Path]:
        """Find knowledge graph JSON file."""
        kg_files = list(self.output_dir.glob("*-knowledge-graph-*.json"))
        return kg_files[0] if kg_files else None

    def evaluate(self) -> Dict:
        """Run all evaluations and return scorecard."""
        if not self.report_path or not self.report_path.exists():
            return {
                "error": "Report file not found",
                "output_dir": str(self.output_dir),
            }

        report_text = self.report_path.read_text()

        # Evaluate dimensions
        self.scores["curie_coverage"] = self._evaluate_curie_coverage(report_text)
        self.scores["source_attribution"] = self._evaluate_source_attribution(
            report_text
        )
        self.scores["locate_retrieve"] = self._evaluate_locate_retrieve(report_text)
        self.scores["evidence_grading"] = self._evaluate_evidence_grading(report_text)

        # CQ-specific evaluations
        if self.cq_id == "cq1":
            self.scores["gof_filtering"] = self._evaluate_gof_filtering(report_text)

        # Calculate total
        self.total_score = sum(self.scores.values())

        return self._generate_scorecard()

    def _evaluate_curie_coverage(self, text: str) -> int:
        """Evaluate CURIE coverage (4 points)."""
        # Find all entity references
        curie_patterns = [
            r"HGNC:\d+",
            r"CHEMBL:\d+",
            r"MONDO:\d+",
            r"UniProtKB:[A-Z0-9]+",
            r"STRING:9606\.\w+",
            r"NCT:\d+",
            r"WP:WP\d+",
        ]

        curie_count = 0
        for pattern in curie_patterns:
            curie_count += len(re.findall(pattern, text))

        # Expect at least 10 CURIEs for full score
        if curie_count >= 10:
            return 4
        elif curie_count >= 7:
            return 3
        elif curie_count >= 5:
            return 2
        elif curie_count >= 3:
            return 1
        else:
            return 0

    def _evaluate_source_attribution(self, text: str) -> int:
        """Evaluate source attribution (4 points)."""
        # Count [Source:...] citations
        source_citations = len(re.findall(r"\[Source:.*?\]", text))

        # Expect at least 15 citations for full score
        if source_citations >= 15:
            return 4
        elif source_citations >= 10:
            return 3
        elif source_citations >= 5:
            return 2
        elif source_citations >= 2:
            return 1
        else:
            return 0

    def _evaluate_locate_retrieve(self, text: str) -> int:
        """Evaluate LOCATE→RETRIEVE pattern (4 points)."""
        locate_count = len(re.findall(r"\bLOCATE\b", text, re.IGNORECASE))
        retrieve_count = len(re.findall(r"\bRETRIEVE\b", text, re.IGNORECASE))

        # Both should appear multiple times
        if locate_count >= 5 and retrieve_count >= 5:
            return 4
        elif locate_count >= 3 and retrieve_count >= 3:
            return 3
        elif locate_count >= 1 and retrieve_count >= 1:
            return 2
        elif locate_count >= 1 or retrieve_count >= 1:
            return 1
        else:
            return 0

    def _evaluate_evidence_grading(self, text: str) -> int:
        """Evaluate evidence grading (4 points)."""
        # Check for L1-L4 evidence levels
        l1_count = len(re.findall(r"\bL1\b", text))
        l2_count = len(re.findall(r"\bL2\b", text))
        l3_count = len(re.findall(r"\bL3\b", text))
        l4_count = len(re.findall(r"\bL4\b", text))

        total_levels = l1_count + l2_count + l3_count + l4_count

        # Check for median calculation
        has_median = bool(
            re.search(r"median.*?(L\d|evidence|grade)", text, re.IGNORECASE)
        )

        # Full score: all 4 levels present + median calculated
        if total_levels >= 4 and has_median and l3_count >= 1:
            return 4
        elif total_levels >= 3 and l3_count >= 1:
            return 3
        elif total_levels >= 2:
            return 2
        elif total_levels >= 1:
            return 1
        else:
            return 0

    def _evaluate_gof_filtering(self, text: str) -> int:
        """Evaluate gain-of-function filtering (4 points, cq1 only)."""
        # Check for Palovarotene (should be present)
        has_palovarotene = bool(
            re.search(r"palovarotene", text, re.IGNORECASE)
        ) or bool(re.search(r"CHEMBL:2105648", text))

        # Check for explicit exclusion of BMP agonists
        has_exclusion = bool(
            re.search(r"exclude.*?(eptotermin|dibotermin|BMP.*?agonist)", text, re.IGNORECASE)
        ) or bool(
            re.search(r"(eptotermin|dibotermin).*?worsen", text, re.IGNORECASE)
        )

        # Check for GoF terminology
        gof_count = len(re.findall(r"gain[- ]of[- ]function", text, re.IGNORECASE))

        if has_palovarotene and has_exclusion and gof_count >= 10:
            return 4
        elif has_palovarotene and has_exclusion and gof_count >= 5:
            return 3
        elif has_palovarotene and has_exclusion:
            return 2
        elif has_palovarotene or has_exclusion:
            return 1
        else:
            return 0

    def _generate_scorecard(self) -> Dict:
        """Generate final scorecard dictionary."""
        return {
            "cq_id": self.cq_id,
            "timestamp": datetime.now().isoformat(),
            "output_dir": str(self.output_dir),
            "report_file": str(self.report_path) if self.report_path else None,
            "scores": {
                "curie_coverage": {
                    "score": self.scores.get("curie_coverage", 0),
                    "max": 4,
                },
                "source_attribution": {
                    "score": self.scores.get("source_attribution", 0),
                    "max": 4,
                },
                "locate_retrieve": {
                    "score": self.scores.get("locate_retrieve", 0),
                    "max": 4,
                },
                "evidence_grading": {
                    "score": self.scores.get("evidence_grading", 0),
                    "max": 4,
                },
                "gof_filtering": {
                    "score": self.scores.get("gof_filtering", 0),
                    "max": 4 if self.cq_id == "cq1" else 0,
                },
            },
            "total_score": self.total_score,
            "max_score": self.max_score,
            "percentage": round((self.total_score / self.max_score) * 100, 1),
            "status": "PASS" if self.total_score >= 17 else "PARTIAL"
            if self.total_score >= 14
            else "FAIL",
        }

    def generate_markdown(self, scorecard: Dict) -> str:
        """Generate markdown scorecard report."""
        md = f"""# {scorecard['cq_id'].upper()} Validation Scorecard

**Timestamp**: {scorecard['timestamp']}
**Output Directory**: `{scorecard['output_dir']}`
**Report File**: `{scorecard['report_file']}`

## Protocol Compliance ({scorecard['total_score']}/{scorecard['max_score']} points)

| Dimension | Score | Max | Evidence |
|-----------|-------|-----|----------|
| CURIE Coverage | {scorecard['scores']['curie_coverage']['score']} | {scorecard['scores']['curie_coverage']['max']} | CURIEs found in report |
| Source Attribution | {scorecard['scores']['source_attribution']['score']} | {scorecard['scores']['source_attribution']['max']} | [Source:...] citations |
| LOCATE→RETRIEVE | {scorecard['scores']['locate_retrieve']['score']} | {scorecard['scores']['locate_retrieve']['max']} | Protocol adherence |
| Evidence Grading | {scorecard['scores']['evidence_grading']['score']} | {scorecard['scores']['evidence_grading']['max']} | L1-L4 presence |
"""

        if scorecard["cq_id"] == "cq1":
            md += f"""| GoF Filtering | {scorecard['scores']['gof_filtering']['score']} | {scorecard['scores']['gof_filtering']['max']} | BMP agonist exclusion |
"""

        status_emoji = "✅" if scorecard["status"] == "PASS" else "⚠️" if scorecard["status"] == "PARTIAL" else "❌"
        md += f"""
**Total**: {scorecard['total_score']}/{scorecard['max_score']} ({scorecard['percentage']}%) {status_emoji} {scorecard['status']}

## Status

"""

        if scorecard["status"] == "PASS":
            md += "- ✅ Report meets protocol requirements\n"
            md += "- ✅ All validation dimensions passed\n"
        elif scorecard["status"] == "PARTIAL":
            md += "- ⚠️ Report partially meets requirements\n"
            md += "- ⚠️ Some dimensions need improvement\n"
        else:
            md += "- ❌ Report does not meet minimum requirements\n"
            md += "- ❌ Multiple dimensions failed\n"

        md += "\n## Recommendations\n\n"

        # Generate recommendations based on scores
        for dim, data in scorecard["scores"].items():
            if data["max"] > 0 and data["score"] < data["max"]:
                if dim == "curie_coverage":
                    md += "- Improve CURIE coverage by adding database identifiers to all entities\n"
                elif dim == "source_attribution":
                    md += "- Add more [Source:...] citations for claims\n"
                elif dim == "locate_retrieve":
                    md += "- Document LOCATE→RETRIEVE pattern more explicitly\n"
                elif dim == "evidence_grading":
                    md += "- Include L1-L4 evidence grading for key claims\n"
                elif dim == "gof_filtering":
                    md += "- Explicitly exclude BMP agonists with gain-of-function rationale\n"

        return md


def main():
    parser = argparse.ArgumentParser(
        description="Generate CQ validation scorecard"
    )
    parser.add_argument(
        "cq_id", help="Competency question ID (e.g., cq1, cq7, cq11, cq8)"
    )
    parser.add_argument(
        "output_dir", type=Path, help="Output directory containing report files"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of markdown",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save scorecard to output directory",
    )

    args = parser.parse_args()

    # Create scorecard
    scorecard = CQScorecard(args.cq_id, args.output_dir)
    result = scorecard.evaluate()

    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        md = scorecard.generate_markdown(result)
        print(md)

    # Save to file if requested
    if args.save:
        output_file = args.output_dir / f"{args.cq_id}-scorecard.md"
        scorecard_md = scorecard.generate_markdown(result)
        output_file.write_text(scorecard_md)
        print(f"\nScorecard saved to: {output_file}")

        # Also save JSON
        json_file = args.output_dir / f"{args.cq_id}-scorecard.json"
        json_file.write_text(json.dumps(result, indent=2))
        print(f"JSON saved to: {json_file}")


if __name__ == "__main__":
    main()
