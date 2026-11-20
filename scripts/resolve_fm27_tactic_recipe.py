#!/usr/bin/env python3
"""Resolve FM27 build inputs for push, workflow_dispatch, and repository_dispatch."""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


def safe_stem(value: Any) -> str:
    stem = re.sub(r"[^\w.-]+", "_", str(value or "FM27_Tactic"), flags=re.UNICODE).strip("._-")
    return stem or "FM27_Tactic"


def _existing_recipe_path(raw_path: str, repo_root: Path) -> Path:
    if not raw_path:
        raise ValueError("recipe_path is empty")
    raw = Path(raw_path)
    if raw.is_absolute():
        raise ValueError("recipe_path must be repository-relative")
    recipe = (repo_root / raw).resolve()
    build_dir = (repo_root / "build_requests").resolve()
    if recipe.parent != build_dir:
        raise ValueError("recipe_path must point directly inside build_requests/")
    if recipe.suffix.lower() not in {".json", ".txt"}:
        raise ValueError("recipe_path must end in .json or .txt")
    if not recipe.is_file():
        raise FileNotFoundError(f"Recipe path is missing: {raw_path}")
    return recipe


def _inline_recipe(
    recipe_data: Any, label: str, run_number: str
) -> dict[str, str | bool]:
    """Keep the recipe as a compact JSON object string; never create a temp file."""
    if not isinstance(recipe_data, dict):
        raise ValueError("Direct recipe payload must be a JSON object.")
    stem = safe_stem(recipe_data.get("name"))
    compact_json = json.dumps(recipe_data, ensure_ascii=False, separators=(",", ":"))
    if "\n" in compact_json or "\r" in compact_json:
        raise ValueError("Compact JSON unexpectedly contains a literal line break")
    return {
        "recipe_json": compact_json,
        "output_stem": f"{stem}_run{run_number}",
        "recipe_label": label,
        "skip_build": False,
    }


def resolve_recipe_input(
    *,
    event_name: str,
    event_data: dict[str, Any],
    recipe_path_input: str = "",
    recipe_json_input: str = "",
    changed_files: list[str] | None = None,
    repo_root: Path,
    runner_temp: Path,
    run_number: str = "0",
) -> dict[str, str | bool]:
    """Return either an existing recipe path or an inline JSON object string."""
    if event_name == "repository_dispatch":
        client_payload = event_data.get("client_payload") or {}
        if not isinstance(client_payload, dict):
            raise ValueError("repository_dispatch client_payload must be an object")
        return _inline_recipe(
            client_payload.get("recipe"),
            "repository_dispatch direct JSON payload",
            run_number,
        )

    if event_name == "workflow_dispatch":
        path_input = recipe_path_input.strip()
        json_input = recipe_json_input.strip()
        if bool(path_input) == bool(json_input):
            raise ValueError("Provide exactly one of recipe_path or recipe_json.")
        if json_input:
            try:
                recipe_data = json.loads(json_input)
            except json.JSONDecodeError as exc:
                raise ValueError(f"recipe_json is invalid JSON: {exc}") from exc
            return _inline_recipe(
                recipe_data,
                "workflow_dispatch inline JSON payload",
                run_number,
            )
        recipe = _existing_recipe_path(path_input, repo_root)
        return {
            "recipe_path": recipe.relative_to(repo_root.resolve()).as_posix(),
            "output_stem": f"{safe_stem(recipe.stem)}_run{run_number}",
            "recipe_label": recipe.relative_to(repo_root.resolve()).as_posix(),
            "skip_build": False,
        }

    if event_name == "push":
        recipes = sorted({
            item.strip()
            for item in (changed_files or [])
            if item.strip().startswith("build_requests/")
            and Path(item.strip()).suffix.lower() in {".json", ".txt"}
        })
        if not recipes:
            raise RuntimeError(f"No build_requests recipe found in push paths: {changed_files!r}")
        if len(recipes) != 1:
            raise ValueError(
                "Each push build must target exactly one JSON or legacy GEN1 TXT under build_requests/. "
                f"Detected: {recipes}"
            )
        recipe = _existing_recipe_path(recipes[0], repo_root)
        relative = recipe.relative_to(repo_root.resolve()).as_posix()
        return {
            "recipe_path": relative,
            "output_stem": f"{safe_stem(recipe.stem)}_run{run_number}",
            "recipe_label": relative,
            "skip_build": False,
        }

    raise ValueError(f"Unsupported GitHub event: {event_name}")


def _changed_files_from_push(event_data: dict[str, Any]) -> list[str]:
    """Resolve changed paths from the GitHub push payload first, then Git history.

    GitHub's push payload is the authoritative event record. The git fallback
    covers unusual/empty payloads and shallow-checkout edge cases.
    """
    changed: set[str] = set()
    head_commit = event_data.get("head_commit") or {}
    if isinstance(head_commit, dict):
        changed.update(head_commit.get("added") or [])
        changed.update(head_commit.get("modified") or [])

    for commit in event_data.get("commits") or []:
        if isinstance(commit, dict):
            changed.update(commit.get("added") or [])
            changed.update(commit.get("modified") or [])

    normalized = {
        path.strip().replace("\\\\", "/").removeprefix("./")
        for path in changed if isinstance(path, str) and path.strip()
    }
    recipe_paths = sorted(
        path for path in normalized
        if path.startswith("build_requests/") and Path(path).suffix.lower() in {".json", ".txt"}
    )
    if recipe_paths:
        return recipe_paths

    before = str(event_data.get("before") or "").strip()
    after = str(event_data.get("after") or "").strip()
    commands = []
    if before and after and set(before) != {"0"}:
        commands.append([
            "git", "diff", "--name-only", "--diff-filter=AM",
            before, after, "--", "build_requests/",
        ])
    commands.extend([
        ["git", "diff", "--name-only", "--diff-filter=AM", "HEAD^", "HEAD", "--", "build_requests/"],
        ["git", "show", "--format=", "--name-only", "HEAD", "--", "build_requests/"],
    ])
    for command in commands:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode == 0:
            paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            if paths:
                recipe_paths = sorted(
                    path for path in paths
                    if path.startswith("build_requests/") and Path(path).suffix.lower() in {".json", ".txt"}
                )
                if recipe_paths:
                    return recipe_paths

    # Some GitHub push deliveries omit the changed-file arrays and the
    # checkout can expose no usable parent diff. In that case, accept only a
    # single request whose filename is explicitly identified by the commit
    # message; never guess from file timestamps or choose an old recipe.
    commit_message = str((event_data.get("head_commit") or {}).get("message") or "")
    build_dir = Path.cwd() / "build_requests"
    message_matches = []
    if build_dir.is_dir():
        for candidate in sorted(build_dir.iterdir()):
            if candidate.is_file() and candidate.suffix.lower() in {".json", ".txt"}:
                relative = candidate.relative_to(repo_root).as_posix()
                if relative in commit_message or candidate.stem in commit_message:
                    message_matches.append(relative)
    if len(message_matches) == 1:
        return message_matches

    raise RuntimeError(
        "Push event contained no resolvable added/modified recipe path and the commit message "
        f"did not identify exactly one build request (matches={message_matches!r})."
    )


def main() -> int:
    event_name = os.environ["EVENT_NAME"]
    event_path = Path(os.environ["EVENT_PATH"])
    event_data = json.loads(event_path.read_text(encoding="utf-8"))
    changed_files = _changed_files_from_push(event_data) if event_name == "push" else None
    result = resolve_recipe_input(
        event_name=event_name,
        event_data=event_data,
        recipe_path_input=os.environ.get("RECIPE_PATH_INPUT", ""),
        recipe_json_input=os.environ.get("RECIPE_JSON_INPUT", ""),
        changed_files=changed_files,
        repo_root=Path.cwd(),
        runner_temp=Path(os.environ["RUNNER_TEMP"]),
        run_number=os.environ.get("GITHUB_RUN_NUMBER", "0"),
    )
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        for key in ("recipe_path", "recipe_json", "output_stem", "recipe_label", "skip_build"):
            if key in result:
                output.write(f"{key}={str(result[key]).lower() if isinstance(result[key], bool) else result[key]}\n")
    if result.get("skip_build"):
        print("No added or modified build request in this push; skipping build.")
    else:
        print(f"Recipe selected: {result['recipe_label']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(f"Recipe input resolution failed: {type(exc).__name__}: {exc}") from exc
