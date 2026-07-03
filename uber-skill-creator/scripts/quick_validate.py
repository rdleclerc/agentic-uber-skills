#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal runtimes.
    yaml = None

MAX_SKILL_NAME_LENGTH = 64


class FrontmatterParseError(ValueError):
    pass


def scalar_value(raw):
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_simple_frontmatter(frontmatter_text):
    """Parse the small YAML subset used by portable SKILL.md frontmatter."""
    result = {}
    lines = frontmatter_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            raise FrontmatterParseError(f"unexpected indented line: {line}")
        if ":" not in line:
            raise FrontmatterParseError(f"expected key/value line: {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise FrontmatterParseError(f"empty key in line: {line}")
        if raw_value in {">", ">-", "|", "|-"}:
            block_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block_lines.append(lines[i].strip())
                i += 1
            if raw_value.startswith(">"):
                result[key] = " ".join(part for part in block_lines if part)
            else:
                result[key] = "\n".join(block_lines).rstrip()
            continue
        if raw_value == "":
            nested = {}
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                child_line = lines[i]
                if not child_line.strip():
                    i += 1
                    continue
                if ":" not in child_line:
                    raise FrontmatterParseError(f"expected nested key/value line: {child_line}")
                child_key, child_value = child_line.split(":", 1)
                nested[child_key.strip()] = scalar_value(child_value)
                i += 1
            result[key] = nested
            continue
        result[key] = scalar_value(raw_value)
        i += 1
    return result


def load_frontmatter(frontmatter_text):
    if yaml is not None:
        try:
            return yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            raise FrontmatterParseError(str(e)) from e
    return parse_simple_frontmatter(frontmatter_text)


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = load_frontmatter(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except FrontmatterParseError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    allowed_properties = {
        "name",
        "description",
        "license",
        "allowed-tools",
        "metadata",
        "model",
        "effort",
    }

    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        allowed = ", ".join(sorted(allowed_properties))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). "
                f"Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    model = frontmatter.get("model")
    if model is not None and not isinstance(model, str):
        return False, f"Model must be a string, got {type(model).__name__}"

    effort = frontmatter.get("effort")
    if effort is not None:
        if not isinstance(effort, str):
            return False, f"Effort must be a string, got {type(effort).__name__}"
        allowed_efforts = {"low", "medium", "high", "xhigh", "max"}
        if effort not in allowed_efforts:
            allowed = ", ".join(sorted(allowed_efforts))
            return False, f"Effort must be one of: {allowed}"

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
