#!/usr/bin/env python3
"""Check the Blueprinting engagement template, or the knowledge graph in an engagement vault.

Usage:
  python3 scripts/check.py                 Check this template repository (run from its root).
  python3 scripts/check.py --vault <root>  Check the notes/ graph of an engagement vault.

The schema lives in navigation/Knowledge-graph.md. In a vault, the checker reads it from the
active Blueprinting bundle, or from --schema. Exit status 0 means no errors; warnings list gaps
that are expected during discovery. It reads files only and uses only the standard library.
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path, PurePosixPath

SCHEMA_DOC = "navigation/Knowledge-graph.md"
LINK = re.compile(r"^\[\[([^\[\]|#]+)(?:#[^\[\]|]*)?(?:\|[^\[\]]*)?\]\]$")
RECORD = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,79}@[a-f0-9]{64}$")
ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,79}$")
KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]+(.*))?$")
OPEN = {"open", "active"}
UNOWNED = {"decision", "question", "risk", "issue", "action", "dependency", "assumption"}
ASSET_EXTENSIONS = {"templates": ".md", "views": ".base", "navigation": ".md"}


class Problems:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warn(self, where, message):
        self.warnings.append(f"{where}: {message}")


class Quoted(str):
    """A scalar that was quoted in YAML, so a [[link]] inside it is text, not a nested list."""


def load_schema(path):
    text = Path(path).read_text(encoding="utf-8")
    blocks = re.findall(r"^## Schema\n.*?^```json\n(.*?)^```", text, re.S | re.M)
    if len(blocks) != 1:
        raise SystemExit(f"{path}: expected exactly one JSON block under '## Schema'")
    return json.loads(blocks[0])


def strip_comment(raw):
    quote = None
    for index, char in enumerate(raw):
        if quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == "#" and (index == 0 or raw[index - 1] in " \t"):
            return raw[:index].rstrip()
    return raw


def scalar(raw):
    """Parse one YAML scalar of the subset Obsidian writes. Raises ValueError when YAML would."""
    raw = strip_comment(raw.strip())
    if raw in ("", "~", "null"):
        return None
    if raw[0] in "\"'":
        if len(raw) < 2 or raw[-1] != raw[0]:
            raise ValueError(f"unterminated quoted value {raw!r}")
        inner = raw[1:-1]
        return Quoted(inner.replace('\\"', '"') if raw[0] == '"' else inner.replace("''", "'"))
    if re.search(r":(\s|$)", raw):
        raise ValueError(f"unquoted value {raw!r} contains ': '; quote it")
    if raw.startswith("[[") and raw.endswith("]]"):
        raise ValueError(f"unquoted link {raw}; YAML reads it as a nested list, so quote it")
    if raw[0] in "[{":
        raise ValueError(f"unsupported flow value {raw!r}")
    return raw


def split_items(inner):
    items, current, quote, depth = [], "", None, 0
    for char in inner:
        if quote:
            current += char
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif char == "," and depth == 0:
            items.append(current)
            current = ""
            continue
        current += char
    if quote or depth:
        raise ValueError("unbalanced list")
    if current.strip():
        items.append(current)
    return [scalar(item) for item in items]


def frontmatter(text):
    """Parse the flat frontmatter subset of Obsidian properties: scalars, block and flow lists."""
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None, "missing frontmatter"
    lines = text[4:].split("\n")
    try:
        end = lines.index("---")
    except ValueError:
        return None, "unterminated frontmatter"
    values, key, block = {}, None, False
    for number, line in enumerate(lines[:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            item = re.match(r"^[ \t]*-(?:[ \t]+(.*))?$", line)
            if item and key is not None and (values[key] is None or isinstance(values[key], list)) and not block:
                if values[key] is None:
                    values[key] = []
                values[key].append(scalar(item.group(1) or ""))
                continue
            if block and line[:1] in " \t":
                values[key] += ("\n" if values[key] else "") + line.strip()
                continue
            block = False
            pair = KEY.match(line)
            if not pair:
                return None, f"line {number}: unsupported frontmatter syntax"
            key, raw = pair.group(1), strip_comment((pair.group(2) or "").strip())
            if key in values:
                return None, f"line {number}: duplicate property {key}"
            if raw in ("|", ">", "|-", ">-", "|+", ">+"):
                values[key], block = "", True
            elif raw.startswith("[") and raw.endswith("]") and not raw.startswith("[["):
                values[key] = split_items(raw[1:-1])
            else:
                values[key] = scalar(raw)
        except ValueError as error:
            return None, f"line {number}: {error}"
    return values, None


def expected_fields(schema, kind):
    spec = schema["kinds"][kind]
    fields = dict(schema["common"]["fields"])
    fields.update(spec["fields"])
    edges = list(schema["common"]["edges"]) + list(spec["edges"])
    return fields, edges


def empty(value):
    return value is None or value == [] or value == ""


def valid_date(value):
    try:
        datetime.date.fromisoformat(str(value))
        return re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value)) is not None
    except ValueError:
        return False


def check_value(problems, where, schema, name, rule, value):
    if empty(value):
        return
    if isinstance(value, list) and rule != "list":
        problems.error(where, f"{name} must be a single value")
        return
    if rule == "list":
        if not isinstance(value, list):
            problems.error(where, f"{name} must be a list")
    elif rule == "date":
        if not valid_date(value):
            problems.error(where, f"{name} must be a valid YYYY-MM-DD date, not {value!r}")
    elif rule == "record":
        if not RECORD.match(str(value)):
            problems.error(where, f"{name} must be <record-id>@<64-character revision>, not {value!r}")
    elif rule is not None:
        allowed = schema["kinds"] if rule == "kind" else schema["values"][rule]
        if str(value) not in allowed:
            problems.error(where, f"{name} {value!r} is not one of {sorted(allowed)}")


def default_for(schema, kind, name, rule):
    defaults = schema["defaults"]
    if name == "disposition":
        return defaults["disposition"].get(kind, defaults["disposition_default"])
    if rule == "list":
        return []
    for key in (name, rule):
        if key in defaults and not isinstance(defaults[key], dict):
            return defaults[key]
    return None


def check_schema(problems, schema):
    names = set(schema["values"])
    for kind, spec in schema["kinds"].items():
        if not ID.match(kind):
            problems.error(SCHEMA_DOC, f"kind {kind!r} is not a valid identifier")
        for name, rule in spec["fields"].items():
            if rule not in (None, "date", "list", "kind", "record") and rule not in names:
                problems.error(SCHEMA_DOC, f"{kind}.{name} names unknown value list {rule!r}")
        for edge in spec["edges"]:
            target = schema["edges"].get(edge)
            if target is None:
                problems.error(SCHEMA_DOC, f"{kind} uses undefined edge {edge!r}")
            elif target not in ("same", "any") and target not in schema["kinds"]:
                problems.error(SCHEMA_DOC, f"edge {edge} points to unknown kind {target!r}")
        overlap = set(spec["fields"]) & set(spec["edges"])
        if overlap:
            problems.error(SCHEMA_DOC, f"{kind} uses {sorted(overlap)} as both field and edge")
    prefixes = [spec["prefix"] for spec in schema["kinds"].values()]
    if len(set(prefixes)) != len(prefixes):
        problems.error(SCHEMA_DOC, "kind prefixes must be unique")
    for key, value in schema["defaults"].items():
        if isinstance(value, str) and key in names and value not in schema["values"][key]:
            problems.error(SCHEMA_DOC, f"default {value!r} is not an allowed {key}")


def check_manifest(problems, root):
    """Mirror the host's template package rules (Blueprinting scripts/templates.py)."""
    try:
        manifest = json.loads((root / "template.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        problems.error("template.json", f"unreadable: {error}")
        return []
    if (not isinstance(manifest, dict) or set(manifest) != {"schema", "version", "requires", "files"}
            or type(manifest["schema"]) is not int or manifest["schema"] != 1
            or type(manifest["requires"]) is not int or manifest["requires"] != 1
            or type(manifest["version"]) is not int or manifest["version"] < 1
            or not isinstance(manifest["files"], list)):
        problems.error("template.json", "must have integer schema 1, requires 1, version >= 1 and a files list")
        return []
    listed = manifest["files"]
    for name in listed:
        parts = PurePosixPath(name).parts if isinstance(name, str) else ()
        if (len(parts) != 2 or parts[0] not in ASSET_EXTENSIONS or not parts[1].endswith(ASSET_EXTENSIONS[parts[0]])
                or str(PurePosixPath(name)) != name or not ID.match(PurePosixPath(name).stem)):
            problems.error("template.json", f"{name!r} is outside the allowed asset paths")
    if len(set(map(str, listed))) != len(listed):
        problems.error("template.json", "duplicate file entries")
    on_disk = sorted(str(p.relative_to(root)) for folder in ASSET_EXTENSIONS
                     for p in (root / folder).rglob("*") if p.is_file())
    for name in sorted(set(on_disk) - set(listed)):
        problems.error("template.json", f"{name} exists but is not listed")
    for name in listed:
        if not (root / name).is_file():
            problems.error("template.json", f"{name} is listed but missing")
    return listed


def check_template_repo(root):
    problems = Problems()
    schema = load_schema(root / SCHEMA_DOC)
    check_schema(problems, schema)
    listed = check_manifest(problems, root)
    templates = {PurePosixPath(name).stem for name in listed if name.startswith("templates/")}
    for kind in sorted(set(schema["kinds"]) - templates):
        problems.error("template.json", f"kind {kind} has no templates/{kind}.md")
    for kind in sorted(templates - set(schema["kinds"])):
        problems.error(f"templates/{kind}.md", "template is not a kind in the schema")
    for kind in sorted(templates & set(schema["kinds"])):
        where = f"templates/{kind}.md"
        text = (root / where).read_text(encoding="utf-8")
        values, error = frontmatter(text)
        if error:
            problems.error(where, error)
            continue
        fields, edges = expected_fields(schema, kind)
        expected = set(fields) | set(edges)
        for name in sorted(expected - set(values)):
            problems.error(where, f"missing property {name}")
        for name in sorted(set(values) - expected):
            problems.error(where, f"property {name} is not in the schema for {kind}")
        if values.get("kind") != kind:
            problems.error(where, f"kind must be {kind!r}")
        for name, rule in fields.items():
            if name == "kind" or name not in values:
                continue
            check_value(problems, where, schema, name, rule, values[name])
            wanted = default_for(schema, kind, name, rule)
            actual = values[name] if not empty(values[name]) else ([] if rule == "list" else None)
            if actual != wanted:
                problems.error(where, f"{name} must start as {wanted!r}, the schema default")
        for name in edges:
            if not empty(values.get(name)):
                problems.error(where, f"edge {name} must start empty")
        if "[[" in text.split("\n---\n", 1)[-1]:
            problems.error(where, "template body must not contain wikilinks")
    for name in listed:
        if name.endswith(".base") and (root / name).is_file():
            text = (root / name).read_text(encoding="utf-8")
            if "\t" in text:
                problems.error(name, "tabs are not valid YAML indentation")
            for match in re.findall(r'note\.kind == "([^"]+)"', text):
                if match not in schema["kinds"]:
                    problems.error(name, f"filters on unknown kind {match!r}")
    return problems


def active_schema(root):
    activations = sorted((root / ".blueprinting" / "templates" / "activations").glob("*.json"))
    if not activations:
        raise SystemExit("No active template bundle; pass --schema <path to Knowledge-graph.md>")
    stage = json.loads(activations[-1].read_text(encoding="utf-8"))["stage"]
    path = root / "Blueprinting" / stage / SCHEMA_DOC
    if not path.is_file():
        raise SystemExit(f"Active bundle has no {SCHEMA_DOC}; upgrade the template first")
    return path


def target_name(value):
    if not isinstance(value, Quoted):
        return None
    match = LINK.match(value.strip())
    if not match:
        return None
    return match.group(1).strip().split("/")[-1].removesuffix(".md")


def check_vault(root, schema_path):
    problems = Problems()
    schema = load_schema(schema_path)
    notes, folded = {}, {}
    for path in sorted((root / schema["folder"]).rglob("*.md")):
        where = str(path.relative_to(root))
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.error(where, "not UTF-8 text")
            continue
        values, error = frontmatter(text)
        if error:
            problems.error(where, error)
            continue
        if path.stem.lower() in folded:
            problems.error(where, f"duplicate note name {path.stem}; links would be ambiguous")
            continue
        notes[path.stem] = (where, values)
        folded[path.stem.lower()] = path.stem
    known = set(schema["common"]["fields"]) | set(schema["edges"])
    for spec in schema["kinds"].values():
        known |= set(spec["fields"])
    engagements = []
    for name, (where, values) in notes.items():
        kind = values.get("kind")
        if not isinstance(kind, str) or kind not in schema["kinds"]:
            problems.error(where, f"kind {kind!r} is not in the schema")
            continue
        if kind == "engagement" and values.get("status") != "superseded":
            engagements.append(where)
        fields, edges = expected_fields(schema, kind)
        prefix = schema["kinds"][kind]["prefix"] + "-"
        if not name.startswith(prefix):
            problems.warn(where, f"name does not start with {prefix}")
        if not ID.match(name):
            problems.error(where, "name must start with a letter and use only letters, digits, - and _ (80 at most)")
        for field, rule in fields.items():
            check_value(problems, where, schema, field, rule, values.get(field))
        for field in values:
            if field not in known:
                problems.warn(where, f"property {field} is not in the schema")
            elif field not in fields and field not in edges:
                problems.error(where, f"{field} is not a property of {kind}")
        for edge in edges:
            value = values.get(edge)
            if empty(value):
                continue
            if not isinstance(value, list):
                value = [value]
            for item in value:
                if empty(item):
                    continue
                target = target_name(item)
                if target is None:
                    problems.error(where, f"{edge} item {item!r} is not a quoted [[wikilink]]")
                    continue
                target = folded.get(target.lower())
                if target is None:
                    problems.error(where, f"{edge} links to missing note {target_name(item)}")
                    continue
                expected = schema["edges"][edge]
                actual = notes[target][1].get("kind")
                if expected == "same":
                    expected = kind
                if expected != "any" and actual != expected:
                    problems.error(where, f"{edge} must link to {expected}, but {target} is {actual}")
                if target == name:
                    problems.error(where, f"{edge} links to itself")
                if edge == "supersedes" and notes[target][1].get("status") != "superseded":
                    problems.warn(where, f"supersedes {target}, which is not marked superseded")
        status = values.get("status")
        if status not in OPEN:
            continue
        if kind == "requirement":
            if empty(values.get("sources")) and empty(values.get("findings")):
                problems.warn(where, "requirement has no supporting evidence")
            if empty(values.get("goals")):
                problems.warn(where, "requirement serves no goal")
        if kind == "finding" and empty(values.get("sources")):
            problems.warn(where, "finding has no source")
        if kind == "finding" and values.get("evidence") == "contested" and empty(values.get("contradicts")):
            problems.warn(where, "contested finding names no competing finding")
        if kind == "source" and empty(values.get("record")):
            problems.warn(where, "source does not cite its retained record")
        if kind in UNOWNED and values.get("owner") in (None, "", "unassigned"):
            problems.warn(where, "open item has no owner")
    if len(engagements) > 1:
        problems.error(engagements[1], f"more than one current engagement note: {', '.join(engagements)}")
    elif notes and not engagements:
        problems.warn(schema["folder"], "no engagement charter note")
    return problems, len(notes)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vault", type=Path, help="engagement vault root to check")
    parser.add_argument("--schema", type=Path, help="Knowledge-graph.md to use for --vault")
    args = parser.parse_args()
    if args.vault:
        problems, count = check_vault(args.vault, args.schema or active_schema(args.vault))
        summary = f"{count} nodes"
    else:
        problems = check_template_repo(Path.cwd())
        summary = "template repository"
    for line in problems.errors:
        print(f"error: {line}")
    for line in problems.warnings:
        print(f"warning: {line}")
    print(f"{summary}: {len(problems.errors)} errors, {len(problems.warnings)} warnings")
    return 1 if problems.errors else 0


if __name__ == "__main__":
    sys.exit(main())
