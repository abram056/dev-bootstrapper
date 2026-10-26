"""Template manifest model, parsing, context building, and file resolution."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Name-derivation helpers
# ---------------------------------------------------------------------------

def snake_case(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\s\-]+", "_", text)  # spaces / dashes → underscore
    text = re.sub(r"[^\w_]", "", text)  # strip remaining special chars (keep _)
    return text


def kebab_case(text: str) -> str:
    return snake_case(text).replace("_", "-")


def pascal_case(text: str) -> str:
    parts = re.split(r"[\s_\-]+", text.lower())
    return "".join(p.capitalize() for p in parts if p)


def camel_case(text: str) -> str:
    p = pascal_case(text)
    return p[0].lower() + p[1:] if p else ""


def pascal_nounderscore(text: str) -> str:
    return pascal_case(text).replace("_", "")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


DERIVATIONS = {
    "snake_case": snake_case,
    "kebab_case": kebab_case,
    "pascal_case": pascal_case,
    "camel_case": camel_case,
    "pascal_nounderscore": pascal_nounderscore,
    "slug": slugify,
}


# ---------------------------------------------------------------------------
# Pattern matching (supports **)
# ---------------------------------------------------------------------------

def matches_pattern(rel_path: str, pattern: str) -> bool:
    """Match a relative POSIX-style path against a glob pattern.

    Supports ``**`` for recursive directory matching.
    """
    if "**" not in pattern:
        import fnmatch

        return fnmatch.fnmatch(rel_path, pattern)

    # Convert glob → regex by scanning left-to-right so that a later
    # ``*``/``?`` replacement can never clobber an already-converted ``**``.
    regex: list[str] = []
    i = 0
    n = len(pattern)
    while i < n:
        if pattern.startswith("**/", i):
            regex.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            regex.append(".*")
            i += 2
        elif pattern[i] == "*":
            regex.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            regex.append("[^/]")
            i += 1
        else:
            regex.append(re.escape(pattern[i]))
            i += 1
    return bool(re.match("".join(regex) + r"\Z", rel_path))


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class VariableSpec:
    name: str
    required: bool = False
    default: str | None = None
    derive: str | None = None
    source: str | None = None
    prompt: str | None = None


@dataclass
class OptionSpec:
    name: str
    default: bool = True
    help: str = ""


@dataclass
class FileRule:
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    when: str | None = None
    equals: Any = True


@dataclass
class TemplateManifest:
    name: str
    aliases: list[str] = field(default_factory=list)
    language: str = ""
    description: str = ""
    variables: dict[str, VariableSpec] = field(default_factory=dict)
    options: dict[str, OptionSpec] = field(default_factory=dict)
    file_exclude: list[str] = field(default_factory=list)
    file_rules: list[FileRule] = field(default_factory=list)
    git_init: bool = True
    install_commands: list[list[str]] = field(default_factory=list)
    source_path: Path | None = None

    @property
    def all_names(self) -> list[str]:
        return [self.name, *self.aliases]


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def _parse_variable(name: str, spec: Any) -> VariableSpec:
    if isinstance(spec, str):
        return VariableSpec(name=name, default=spec)
    if isinstance(spec, dict):
        return VariableSpec(
            name=name,
            required=spec.get("required", False),
            default=spec.get("default"),
            derive=spec.get("derive"),
            source=spec.get("from") or spec.get("source"),
            prompt=spec.get("prompt"),
        )
    raise ValueError(f"Invalid variable spec for {name!r}: {spec!r}")


def _parse_option(name: str, spec: Any) -> OptionSpec:
    if isinstance(spec, bool):
        return OptionSpec(name=name, default=spec)
    if isinstance(spec, dict):
        return OptionSpec(
            name=name,
            default=spec.get("default", True),
            help=spec.get("help", ""),
        )
    raise ValueError(f"Invalid option spec for {name!r}: {spec!r}")


def _parse_file_rule(rule: dict) -> FileRule:
    return FileRule(
        include=rule.get("include", []),
        exclude=rule.get("exclude", []),
        when=rule.get("when"),
        equals=rule.get("is", rule.get("equals", True)),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_manifest(template_dir: Path) -> TemplateManifest:
    """Load and parse ``template.toml`` from *template_dir*."""
    manifest_path = template_dir / "template.toml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No template.toml in {template_dir}")

    with open(manifest_path, "rb") as f:
        data = tomllib.load(f)

    variables = {
        name: _parse_variable(name, spec)
        for name, spec in data.get("variables", {}).items()
    }
    options = {
        name: _parse_option(name, spec)
        for name, spec in data.get("options", {}).items()
    }

    files_section = data.get("files", {})
    file_exclude = files_section.get("exclude", [])
    file_rules = [_parse_file_rule(r) for r in files_section.get("rules", [])]

    commands_section = data.get("commands", {})
    git_init = commands_section.get("git", True)
    install_commands = commands_section.get("install", [])

    return TemplateManifest(
        name=data["name"],
        aliases=data.get("aliases", []),
        language=data.get("language", ""),
        description=data.get("description", ""),
        variables=variables,
        options=options,
        file_exclude=file_exclude,
        file_rules=file_rules,
        git_init=git_init,
        install_commands=install_commands,
        source_path=template_dir,
    )


def build_context(
    manifest: TemplateManifest,
    project_name: str,
    package_name: str | None = None,
    extra_vars: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build the render context from a manifest and CLI inputs."""
    if package_name is None:
        package_name = snake_case(project_name)

    context: dict[str, str] = {
        "project_name": project_name,
        "package_name": package_name,
        "project_slug": kebab_case(project_name),
        "pascal_name": pascal_case(project_name),
        "pascal_nounderscore": pascal_nounderscore(project_name),
        "camel_name": camel_case(project_name),
    }

    for name, spec in manifest.variables.items():
        if spec.derive and spec.source:
            if spec.source in context:
                context[name] = DERIVATIONS[spec.derive](context[spec.source])
            else:
                context[name] = DERIVATIONS[spec.derive](project_name)
        elif spec.default is not None:
            context[name] = spec.default
        elif spec.required and name not in context:
            raise ValueError(f"Required variable {name!r} not provided")

    if extra_vars:
        context.update(extra_vars)

    return context


def resolve_options(
    manifest: TemplateManifest,
    cli_options: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Merge manifest option defaults with CLI-provided values."""
    options: dict[str, Any] = {
        name: spec.default for name, spec in manifest.options.items()
    }
    if cli_options:
        for key, value in cli_options.items():
            if key not in manifest.options:
                raise ValueError(f"Unknown option: {key}")
            if value.lower() == "true":
                options[key] = True
            elif value.lower() == "false":
                options[key] = False
            else:
                options[key] = value
    return options


def resolve_files(
    manifest: TemplateManifest,
    rel_paths: list[str],
    options: dict[str, Any],
) -> list[str]:
    """Return the subset of *rel_paths* that should be included.

    *rel_paths* are POSIX-relative paths (e.g. ``"alembic/env.py"``).
    """
    result: list[str] = []
    for rel in rel_paths:
        if any(matches_pattern(rel, pat) for pat in manifest.file_exclude):
            continue

        include = True
        for rule in manifest.file_rules:
            if rule.when is not None:
                opt_val = options.get(rule.when, False)
                condition_met = opt_val == rule.equals
            else:
                condition_met = True

            if condition_met:
                if rule.exclude and any(
                    matches_pattern(rel, pat) for pat in rule.exclude
                ):
                    include = False
            else:
                if rule.include and any(
                    matches_pattern(rel, pat) for pat in rule.include
                ):
                    include = False

        if include:
            result.append(rel)

    return result
