#!/usr/bin/env python3
"""
Forward-test harness for the youversion-platform-api skill.

This script runs Codex non-interactively against a prompt suite and scores the
final answer using simple substring checks. It is intentionally lightweight:
the goal is to catch obvious regressions in skill behavior, not to prove full
correctness.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path("/Users/david.fedor/Projects/platform-skills")
SKILL_PATH = ROOT / "skills/youversion-platform-api/SKILL.md"
WORKDIR = ROOT
CODEX_BIN = "codex"


@dataclass(frozen=True)
class Case:
    name: str
    prompt: str
    must_contain: tuple[str, ...] = ()
    must_not_contain: tuple[str, ...] = ()
    notes: str = ""


def tail_lines(text: str, max_lines: int = 40) -> str:
    lines = text.strip().splitlines()
    if len(lines) <= max_lines:
        return text.strip()
    return "\n".join(lines[-max_lines:])


CASES: tuple[Case, ...] = (
    Case(
        name="curl_list_french_bibles",
        prompt=(
            f"Use $youversion-platform-api at {SKILL_PATH} to show me a cURL command "
            "that lists the French Bibles available to my app key."
        ),
        must_contain=(
            "curl",
            "https://api.youversion.com/v1/bibles",
            "language_ranges[]=fr",
            "X-YVP-App-Key",
        ),
        must_not_contain=(
            "@youversion/platform-core",
            "BibleClient",
        ),
        notes="Simple happy-path discovery prompt.",
    ),
    Case(
        name="browser_js_fetch",
        prompt=(
            f"Use $youversion-platform-api at {SKILL_PATH} to give me a browser "
            "JavaScript fetch example for Genesis 1:3 from Bible version 3034."
        ),
        must_contain=(
            "fetch",
            "document.body.dataset.yvpAppKey",
            "/v1/bibles/3034/passages/GEN.1.3",
            "X-YVP-App-Key",
        ),
        must_not_contain=(
            "process.env.YVP_APP_KEY",
        ),
        notes="Checks the browser-specific guidance rather than Node-only env vars.",
    ),
    Case(
        name="python_list_english_bibles",
        prompt=(
            f"Use $youversion-platform-api at {SKILL_PATH} to give me a Python "
            "requests example that lists English Bibles and prints id, abbreviation, and title."
        ),
        must_contain=(
            "requests",
            "https://api.youversion.com/v1/bibles",
            "language_ranges[]",
            "X-YVP-App-Key",
        ),
        must_not_contain=(
            "@youversion/platform-core",
            "BibleClient",
        ),
        notes="Checks Python example quality and REST-only behavior.",
    ),
    Case(
        name="german_passage_requires_discovery",
        prompt=(
            f"Use $youversion-platform-api at {SKILL_PATH} to show me John 1:1 in "
            "German using a raw HTTP example."
        ),
        must_contain=(
            "https://api.youversion.com/v1/bibles?language_ranges[]=de",
            "JHN.1.1",
            "/v1/bibles/",
            "/passages/JHN.1.1?format=text",
        ),
        must_not_contain=(
            '"content": "',
            "The response content is:",
            "version `51`",
            "/v1/bibles/51/passages/JHN.1.1",
        ),
        notes="This should stay discovery-first and never invent verse text or a concrete id.",
    ),
    Case(
        name="bds_id_requires_request_first_wording",
        prompt=(
            f"Use $youversion-platform-api at {SKILL_PATH} to tell me the id of the "
            "BDS Bible version in French and show the request you would use to find it."
        ),
        must_contain=(
            "language_ranges[]=fr",
            "fields[]",
            "abbreviation",
            "BDS",
        ),
        must_not_contain=(
            "The French BDS Bible version id is",
            '"id":21',
            "`21`",
            "bible.com/versions/",
            "I inferred",
        ),
        notes="The skill should not claim a live id unless it actually executed the lookup.",
    ),
)


def run_case(case: Case, model: str, codex_home: str | None = None) -> dict:
    output_file = Path("/tmp") / f"{case.name}.last-message.txt"
    if output_file.exists():
        output_file.unlink()

    cmd = [
        CODEX_BIN,
        "exec",
        "--skip-git-repo-check",
        "--ephemeral",
        "--color",
        "never",
        "-s",
        "read-only",
        "-C",
        str(WORKDIR),
        "-m",
        model,
        "-o",
        str(output_file),
        case.prompt,
    ]

    env = os.environ.copy()
    if codex_home:
        Path(codex_home).mkdir(parents=True, exist_ok=True)
        env["CODEX_HOME"] = codex_home

    shell_cmd = shlex.join(cmd)
    if codex_home:
        shell_cmd = f"CODEX_HOME={shlex.quote(codex_home)} {shell_cmd}"

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    answer = output_file.read_text() if output_file.exists() else ""
    missing = [s for s in case.must_contain if s not in answer]
    forbidden = [s for s in case.must_not_contain if s in answer]
    passed = proc.returncode == 0 and not missing and not forbidden and bool(answer.strip())

    return {
        "name": case.name,
        "passed": passed,
        "returncode": proc.returncode,
        "missing": missing,
        "forbidden": forbidden,
        "notes": case.notes,
        "prompt": case.prompt,
        "cmd": cmd,
        "shell_cmd": shell_cmd,
        "output_file": str(output_file),
        "answer": answer,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def iter_cases(selected: Iterable[str] | None) -> list[Case]:
    if not selected:
        return list(CASES)
    wanted = set(selected)
    return [case for case in CASES if case.name in wanted]


def print_human(results: list[dict], debug: bool = False) -> None:
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    print(f"Forward tests: {passed}/{total} passed")
    print()
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {result['name']}")
        if result["notes"]:
            print(f"  note: {result['notes']}")
        if result["missing"]:
            print(f"  missing: {', '.join(result['missing'])}")
        if result["forbidden"]:
            print(f"  forbidden: {', '.join(result['forbidden'])}")
        if result["returncode"] != 0:
            print(f"  codex exit code: {result['returncode']}")
        if debug and not result["passed"]:
            print(f"  prompt: {result['prompt']}")
            print(f"  output file: {result['output_file']}")
            print(f"  repro command: {result['shell_cmd']}")
            if result["answer"].strip():
                print("  answer tail:")
                print(indent_block(tail_lines(result["answer"])))
            if result["stdout"].strip():
                print("  stdout tail:")
                print(indent_block(tail_lines(result["stdout"])))
            if result["stderr"].strip():
                print("  stderr tail:")
                print(indent_block(tail_lines(result["stderr"])))
        print()


def indent_block(text: str, prefix: str = "    ") -> str:
    return "\n".join(prefix + line for line in text.splitlines())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="gpt-5.4-mini",
        help="Codex model to use for each exec run.",
    )
    parser.add_argument(
        "--case",
        action="append",
        dest="cases",
        help="Run only the named case. Repeatable.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of a human summary.",
    )
    parser.add_argument(
        "--codex-home",
        help="Override CODEX_HOME for the codex exec subprocess. Default: inherit current environment.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print prompt, command, and stderr details for failing cases.",
    )
    parser.add_argument(
        "--no-fail-fast",
        action="store_true",
        help="Run every selected case even after a failure.",
    )
    args = parser.parse_args()

    cases = iter_cases(args.cases)
    if not cases:
        print("No matching cases selected.", file=sys.stderr)
        return 2

    results: list[dict] = []
    for case in cases:
        result = run_case(case, args.model, codex_home=args.codex_home)
        results.append(result)
        if not result["passed"] and not args.no_fail_fast:
            break

    if args.json:
        json.dump(results, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_human(results, debug=args.debug)

    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
