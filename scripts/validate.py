#!/usr/bin/env python3
"""Validate the public andashi marketplace without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
PLUGIN = ROOT / "plugins/andashi"
MANIFEST = PLUGIN / ".codex-plugin/plugin.json"
SKILL = PLUGIN / "skills/andashi/SKILL.md"
OPENAI_YAML = PLUGIN / "skills/andashi/agents/openai.yaml"
CLAUDE_SKILL_DIR = ROOT / ".claude/skills/andashi"
CLAUDE_SKILL = CLAUDE_SKILL_DIR / "SKILL.md"
TEST_CASES = ROOT / "submission/test-cases.json"


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def validate_marketplace() -> None:
    data = load_json(MARKETPLACE)
    if not isinstance(data, dict) or data.get("name") != "andashi":
        fail("marketplace name must be 'andashi'")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("marketplace must expose exactly one plugin")
    entry = plugins[0]
    expected = {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }
    if entry.get("name") != "andashi" or entry.get("policy") != expected:
        fail("marketplace plugin name or policy is invalid")
    source = entry.get("source", {})
    if source.get("source") != "local" or source.get("path") != "./plugins/andashi":
        fail("marketplace source must point to ./plugins/andashi")


def validate_manifest() -> None:
    data = load_json(MANIFEST)
    required = ("name", "version", "description", "skills", "interface")
    missing = [key for key in required if not data.get(key)]
    if missing:
        fail(f"plugin manifest is missing: {', '.join(missing)}")
    if data["name"] != PLUGIN.name:
        fail("plugin folder name and manifest name must match")
    if not re.fullmatch(r"\d+\.\d+\.\d+", data["version"]):
        fail("plugin version must use plain semantic versioning")
    if data["skills"] != "./skills/":
        fail("plugin skills path must be ./skills/")
    if "hooks" in data or "mcpServers" in data or "apps" in data:
        fail("skills-only plugin must not declare hooks, MCP servers, or apps")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        fail("SKILL.md frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def validate_skill() -> None:
    text = SKILL.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if set(fields) != {"name", "description"}:
        fail("SKILL.md frontmatter may contain only name and description")
    if fields["name"] != SKILL.parent.name:
        fail("skill folder name and frontmatter name must match")
    if not fields["description"]:
        fail("skill description must not be empty")
    for rel in sorted(set(re.findall(r"`(references/[^`]+\.md)`", text))):
        if not (SKILL.parent / rel).is_file():
            fail(f"missing referenced skill file: {rel}")
    if not OPENAI_YAML.is_file():
        fail("missing agents/openai.yaml")
    ui = OPENAI_YAML.read_text(encoding="utf-8")
    for field in ("display_name:", "short_description:", "default_prompt:"):
        if field not in ui:
            fail(f"agents/openai.yaml is missing {field}")


def validate_claude_skill() -> None:
    text = CLAUDE_SKILL.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if set(fields) != {"name", "description"}:
        fail("Claude SKILL.md frontmatter may contain only name and description")
    if fields["name"] != CLAUDE_SKILL_DIR.name:
        fail("Claude skill folder name and frontmatter name must match")
    if not fields["description"]:
        fail("Claude skill description must not be empty")
    for rel in sorted(set(re.findall(r"`(references/[^`]+\.md)`", text))):
        if not (CLAUDE_SKILL_DIR / rel).is_file():
            fail(f"missing referenced Claude skill file: {rel}")

    canonical = SKILL.parent
    shared_files = ["SKILL.md"] + [
        path.relative_to(canonical).as_posix()
        for path in sorted((canonical / "references").glob("*.md"))
    ]
    for rel in shared_files:
        codex_file = canonical / rel
        claude_file = CLAUDE_SKILL_DIR / rel
        if not claude_file.is_file():
            fail(f"missing Claude skill file: {rel}")
        if codex_file.read_bytes() != claude_file.read_bytes():
            fail(f"Codex and Claude skill copies differ: {rel}")


def validate_submission_cases() -> None:
    cases = load_json(TEST_CASES)
    if not isinstance(cases, list):
        fail("submission test cases must be a JSON array")
    positives = [case for case in cases if case.get("type") == "positive"]
    negatives = [case for case in cases if case.get("type") == "negative"]
    if len(positives) != 5 or len(negatives) != 3:
        fail("submission requires exactly five positive and three negative cases")
    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)) or any(not item for item in ids):
        fail("submission test case IDs must be present and unique")
    required = {"id", "type", "user_prompt", "expected_behavior", "expected_result_shape"}
    for case in cases:
        missing = sorted(required - case.keys())
        if missing:
            fail(f"test case {case.get('id')} is missing: {', '.join(missing)}")


def validate_public_tree() -> None:
    forbidden_parts = {"__pycache__", ".pytest_cache"}
    local_path_markers = ("/" + "Users/", "/" + "home/", "cache/" + "personal")
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "dist" in path.parts:
            continue
        if forbidden_parts.intersection(path.parts) or path.suffix in {".pyc", ".pyo"}:
            fail(f"generated cache must not be published: {path.relative_to(ROOT)}")
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(marker in text for marker in local_path_markers):
                fail(f"local absolute path leaked into {path.relative_to(ROOT)}")
            if re.search(r"\bsk-[A-Za-z0-9_-]{16,}\b", text):
                fail(f"possible API secret in {path.relative_to(ROOT)}")


def main() -> int:
    checks = (
        validate_marketplace,
        validate_manifest,
        validate_skill,
        validate_claude_skill,
        validate_submission_cases,
        validate_public_tree,
    )
    try:
        for check in checks:
            check()
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("OK: marketplace, Codex plugin, Claude skill, submission cases, and public tree are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
