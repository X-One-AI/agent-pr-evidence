from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def changed_paths(repo: Path, base: str, head: str) -> dict[str, str]:
    output = run_git(repo, "diff", "--name-status", f"{base}..{head}")
    changes: dict[str, str] = {}
    for line in output.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        changes[path] = status
    return changes


def numstat(repo: Path, base: str, head: str) -> dict[str, tuple[int, int]]:
    output = run_git(repo, "diff", "--numstat", f"{base}..{head}")
    stats: dict[str, tuple[int, int]] = {}
    for line in output.splitlines():
        if not line:
            continue
        additions, deletions, path = line.split("\t", 2)
        stats[path] = (_parse_count(additions), _parse_count(deletions))
    return stats


def file_at_ref(repo: Path, ref: str, path: str) -> str:
    return run_git(repo, "show", f"{ref}:{path}")


def _parse_count(value: str) -> int:
    return 0 if value == "-" else int(value)
