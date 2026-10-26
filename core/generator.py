"""Project generation from template manifests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

from core.manifest import TemplateManifest, resolve_files
from engine.file_manager import write_file
from engine.renderer import find_unrendered, render_content, render_path
from templates.loader import load_template_files


def create_project(
    manifest: TemplateManifest,
    context: dict[str, str],
    options: dict[str, Any],
    output_dir: Path,
    force: bool = False,
    dry_run: bool = False,
    git: bool = True,
    install: bool = False,
) -> Path:
    """Create a project from *manifest* into *output_dir*.

    Returns the path to the created (or would-be-created) directory.
    """
    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        raise FileExistsError(
            f"Directory {output_dir} exists and is not empty. Use --force to overwrite."
        )

    template_files = load_template_files(manifest)
    all_rels = [tf["rel_path"] for tf in template_files]
    included_rels = set(resolve_files(manifest, all_rels, options))
    files_to_write = [tf for tf in template_files if tf["rel_path"] in included_rels]

    if dry_run:
        return _dry_run(
            manifest, context, files_to_write, output_dir, git=git, install=install
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    for tf in files_to_write:
        rel = Path(tf["rel_path"])
        rendered_path = render_path(rel, context)
        if tf["is_binary"]:
            full_path = output_dir / rendered_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_bytes(tf["content"])
        else:
            rendered_content = render_content(tf["content"], context)
            unrendered = find_unrendered(rendered_content)
            if unrendered:
                print(
                    f"Warning: unrendered placeholders in {rendered_path}: "
                    f"{', '.join(unrendered)}",
                    file=sys.stderr,
                )
            write_file(output_dir, rendered_path, rendered_content)

    if git and manifest.git_init:
        _run_git_init(output_dir)

    if install:
        _run_install(manifest, output_dir)

    return output_dir


def _dry_run(
    manifest: TemplateManifest,
    context: dict[str, str],
    files_to_write: list[dict],
    output_dir: Path,
    *,
    git: bool,
    install: bool,
) -> Path:
    print(f"Would create {len(files_to_write)} files in {output_dir}/:")
    for tf in files_to_write:
        rendered = render_path(Path(tf["rel_path"]), context)
        print(f"  {output_dir}/{rendered}")
    if git and manifest.git_init:
        print("  [run] git init")
    if install:
        for cmd in manifest.install_commands:
            print(f"  [run] {' '.join(cmd)}")
    return output_dir


def _run_git_init(output_dir: Path) -> None:
    try:
        subprocess.run(
            ["git", "init"],
            cwd=output_dir,
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        print("Warning: git not found on PATH, skipping git init.", file=sys.stderr)
    except subprocess.CalledProcessError as exc:
        print(f"Warning: git init failed: {exc}", file=sys.stderr)


def _run_install(manifest: TemplateManifest, output_dir: Path) -> None:
    for cmd in manifest.install_commands:
        if not cmd:
            continue
        try:
            subprocess.run(cmd, cwd=output_dir, check=True)
        except FileNotFoundError:
            print(
                f"Warning: command not found, skipping: {cmd[0]}",
                file=sys.stderr,
            )
        except subprocess.CalledProcessError as exc:
            print(f"Warning: command failed ({' '.join(cmd)}): {exc}", file=sys.stderr)
