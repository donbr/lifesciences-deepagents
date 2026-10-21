#!/usr/bin/env python3
"""Sync .claude/skills into .deepagents/skills with runtime-safe transforms."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ABSOLUTE_HOME_RE = re.compile(r"/home/[A-Za-z0-9._/-]+")
CLAUDE_SKILL_PATH_RE = re.compile(
    r"(?:/home/[A-Za-z0-9._/-]+/)?\.claude/skills/([a-z0-9-]+)/SKILL\.md"
)
FRONTMATTER_RE = re.compile(
    r"\A---\s*\n(?P<frontmatter>.*?)\n---\s*\n?(?P<body>.*)\Z",
    re.DOTALL,
)


DEFAULT_MEMORY = """# Life Sciences DeepAgents Runtime Memory

## Core Discipline
- Follow LOCATE -> RETRIEVE workflow for ID resolution and strict lookups.
- Use MCP tools as primary source of truth; use query_api_direct only as fallback.
- Ground claims in tool output. If evidence is missing, state uncertainty explicitly.

## Graph and Report Contract
- Always emit `workspace/graph.json` and `workspace/report.md`.
- Use relative paths only (never absolute system paths).
- Graphiti persistence is optional and best-effort.

## Safety
- For gain-of-function diseases, prioritize inhibitors/antagonists and exclude agonists.
- Validate trial IDs and mechanism claims before final reporting.
"""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _extract_http_url(block: str) -> str | None:
    patterns = [
        r'"(https?://[^"]+)"',
        r"'(https?://[^']+)'",
        r"(https?://\\S+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, block)
        if match:
            return match.group(1)
    return None


def _convert_curl_blocks(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if "curl " not in stripped:
            out.append(line)
            i += 1
            continue

        indent = line[: len(line) - len(stripped)]
        block_lines = [line]
        i += 1
        while block_lines[-1].rstrip().endswith("\\") and i < len(lines):
            block_lines.append(lines[i])
            i += 1
        block = "\n".join(block_lines)
        method = "POST" if re.search(r"-X\\s+POST", block, re.IGNORECASE) else "GET"
        url = _extract_http_url(block) or "<set-url>"
        out.append(
            f'{indent}query_api_direct(url="{url}", method="{method}")  # runtime fallback (no shell)'
        )

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def _transform_skill_text(text: str, skill_name: str) -> str:
    transformed = ABSOLUTE_HOME_RE.sub("<repo-root>", text)
    transformed = CLAUDE_SKILL_PATH_RE.sub(r"\1", transformed)

    match = FRONTMATTER_RE.match(transformed)
    if match:
        frontmatter = match.group("frontmatter")
        body = match.group("body")
    else:
        frontmatter = ""
        body = transformed

    # Frontmatter: textual replacements only (never command conversion).
    frontmatter = frontmatter.replace("Falls back to curl", "Falls back to query_api_direct")
    frontmatter = frontmatter.replace("curl", "query_api_direct")

    # Body: textual replacements + curl command conversion.
    body = body.replace("curl only", "query_api_direct fallback")
    body = body.replace("curl (fallback)", "query_api_direct (fallback)")
    body = body.replace("Falls back to curl", "Falls back to query_api_direct")
    body = body.replace("curl command output", "query_api_direct output")
    body = body.replace("DIRECT API (curl", "DIRECT API (query_api_direct")
    body = body.replace("FALLBACK (curl", "FALLBACK (query_api_direct")
    body = body.replace("use curl directly", "use query_api_direct directly")
    body = body.replace("Use curl for reliable access.", "Use query_api_direct for reliable access.")
    body = _convert_curl_blocks(body)

    if frontmatter:
        transformed = f"---\n{frontmatter}\n---\n\n{body.lstrip()}"
    else:
        transformed = body

    if "Runtime constraints" not in transformed:
        runtime_note = (
            "\n## Runtime constraints (DeepAgents)\n"
            "- Prefer MCP tools first; use query_api_direct for HTTP fallbacks.\n"
            "- Do not run shell curl in this runtime.\n"
            "- Use relative file paths under `workspace/`.\n"
            "- Graphiti persistence is optional/best-effort.\n"
        )
        match = FRONTMATTER_RE.match(transformed)
        if match:
            transformed = (
                f"---\n{match.group('frontmatter')}\n---\n\n"
                f"{runtime_note}\n{match.group('body').lstrip()}"
            )
        else:
            transformed = runtime_note + "\n" + transformed.lstrip()

    if skill_name == "lifesciences-graph-builder":
        note = (
            "\n## Runtime Note\n"
            "- Graphiti persistence is OPTIONAL and best-effort.\n"
            "- Core completion requires local artifact writes to `workspace/graph.json` and `workspace/report.md`.\n"
        )
        if "Graphiti persistence is OPTIONAL and best-effort." not in transformed:
            transformed = transformed.rstrip() + "\n" + note

    return transformed


def sync(check_only: bool = False) -> list[str]:
    repo = _repo_root()
    src_root = repo / ".claude" / "skills"
    dst_root = repo / ".deepagents" / "skills"
    memory_file = repo / ".deepagents" / "AGENTS.md"

    if not src_root.exists():
        raise FileNotFoundError(f"Source skills directory not found: {src_root}")

    planned_outputs: list[str] = []
    for skill_dir in sorted(path for path in src_root.iterdir() if path.is_dir()):
        dst_skill_dir = dst_root / skill_dir.name
        planned_outputs.append(str(dst_skill_dir))
        if check_only:
            continue

        if dst_skill_dir.exists():
            shutil.rmtree(dst_skill_dir)
        shutil.copytree(skill_dir, dst_skill_dir)

        skill_md = dst_skill_dir / "SKILL.md"
        if skill_md.exists():
            original = skill_md.read_text(encoding="utf-8")
            transformed = _transform_skill_text(original, skill_dir.name)
            skill_md.write_text(transformed, encoding="utf-8")

    if not check_only:
        dst_root.mkdir(parents=True, exist_ok=True)
        if not memory_file.exists():
            memory_file.write_text(DEFAULT_MEMORY, encoding="utf-8")

    return planned_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only print planned sync targets without writing files.",
    )
    args = parser.parse_args()

    outputs = sync(check_only=args.check)
    mode = "CHECK" if args.check else "SYNC"
    print(f"[{mode}] skills targets:")
    for path in outputs:
        print(f"- {path}")


if __name__ == "__main__":
    main()
