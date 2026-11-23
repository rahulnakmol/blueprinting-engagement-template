"""Tests for scripts/check.py: the shipped template passes and seeded defects are caught."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORD = "src-interview@" + "a" * 64
CHECK = ROOT / "scripts" / "check.py"
SCHEMA = ROOT / "navigation" / "Knowledge-graph.md"


def run(*args, cwd=ROOT):
    result = subprocess.run([sys.executable, str(CHECK), *args], cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout


def note(kind, **values):
    lines = ["---", f"kind: {kind}", "status: open", "owner: unassigned"]
    for key, value in values.items():
        if isinstance(value, list):
            lines.append(f"{key}: [" + ", ".join(f'"{item}"' for item in value) + "]")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines + ["---", "Body.", ""])


class TemplateRepository(unittest.TestCase):
    def copy(self):
        temporary = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, temporary)
        for name in ("template.json", "templates", "views", "navigation"):
            source = ROOT / name
            (shutil.copytree if source.is_dir() else shutil.copy)(source, temporary / name)
        return temporary

    def test_shipped_template_passes(self):
        code, output = run()
        self.assertEqual(code, 0, output)
        self.assertIn("0 errors", output)

    def test_unlisted_template_fails(self):
        root = self.copy()
        (root / "templates" / "stray.md").write_text(note("stray"))
        code, output = run(cwd=root)
        self.assertEqual(code, 1)
        self.assertIn("templates/stray.md exists but is not listed", output)

    def test_template_missing_schema_property_fails(self):
        root = self.copy()
        path = root / "templates" / "requirement.md"
        path.write_text(path.read_text().replace("goals: []\n", ""))
        code, output = run(cwd=root)
        self.assertEqual(code, 1)
        self.assertIn("templates/requirement.md: missing property goals", output)

    def test_template_with_prefilled_edge_fails(self):
        root = self.copy()
        path = root / "templates" / "finding.md"
        path.write_text(path.read_text().replace("sources: []", 'sources: ["[[SRC-001]]"]'))
        code, output = run(cwd=root)
        self.assertEqual(code, 1)
        self.assertIn("edge sources must start empty", output)

    def test_template_with_invalid_value_fails(self):
        root = self.copy()
        path = root / "templates" / "requirement.md"
        path.write_text(path.read_text().replace("fit: unresolved", "fit: maybe"))
        code, output = run(cwd=root)
        self.assertEqual(code, 1)
        self.assertIn("fit 'maybe' is not one of", output)

    def test_template_default_must_match_schema(self):
        root = self.copy()
        path = root / "templates" / "finding.md"
        path.write_text(path.read_text().replace("evidence: unverified", "evidence: clarified"))
        code, output = run(cwd=root)
        self.assertEqual(code, 1)
        self.assertIn("evidence must start as 'unverified'", output)

    def test_manifest_keys_and_nested_assets_fail(self):
        root = self.copy()
        (root / "templates" / "sub").mkdir()
        (root / "templates" / "sub" / "x.md").write_text(note("goal"))
        manifest = (root / "template.json").read_text().replace('"version": 2', '"version": "2"')
        (root / "template.json").write_text(manifest)
        code, output = run(cwd=root)
        self.assertEqual(code, 1)
        self.assertIn("must have integer schema 1", output)
        root = self.copy()
        (root / "templates" / "sub").mkdir()
        (root / "templates" / "sub" / "x.md").write_text(note("goal"))
        code, output = run(cwd=root)
        self.assertIn("templates/sub/x.md exists but is not listed", output)

    def test_base_filtering_on_unknown_kind_fails(self):
        root = self.copy()
        path = root / "views" / "Gaps.base"
        path.write_text(path.read_text().replace('note.kind == "question"', 'note.kind == "questions"', 1))
        code, output = run(cwd=root)
        self.assertEqual(code, 1)
        self.assertIn("filters on unknown kind 'questions'", output)


class Vault(unittest.TestCase):
    def vault(self, notes):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        (root / "notes").mkdir()
        for name, text in notes.items():
            (root / "notes" / f"{name}.md").write_text(text)
        return root

    def check(self, notes):
        return run("--vault", str(self.vault(notes)), "--schema", str(SCHEMA))

    def test_connected_graph_passes_without_warnings(self):
        code, output = self.check({
            "ENG-001-charter": note("engagement"),
            "SRC-001-interview": note("source", record=RECORD),
            "FND-001-credit-hold": note("finding", evidence="source-checked", sources=["[[SRC-001-interview]]"]),
            "GOL-001-cash": note("goal"),
            "REQ-001-release": note("requirement", goals=["[[GOL-001-cash]]"],
                                    findings=["[[FND-001-credit-hold]]"]),
        })
        self.assertEqual(code, 0, output)
        self.assertIn("5 nodes: 0 errors, 0 warnings", output)

    def test_edge_to_wrong_kind_fails(self):
        code, output = self.check({
            "GOL-001-cash": note("goal"),
            "REQ-001-release": note("requirement", goals=["[[GOL-001-cash]]"], findings=["[[GOL-001-cash]]"]),
        })
        self.assertEqual(code, 1)
        self.assertIn("findings must link to finding, but GOL-001-cash is goal", output)

    def test_dangling_link_fails(self):
        code, output = self.check({"FND-001-claim": note("finding", sources=["[[SRC-404-missing]]"])})
        self.assertEqual(code, 1)
        self.assertIn("sources links to missing note SRC-404-missing", output)

    def test_edge_not_defined_for_kind_fails(self):
        code, output = self.check({
            "GOL-001-cash": note("goal"),
            "SRC-001-interview": note("source", goals=["[[GOL-001-cash]]"]),
        })
        self.assertEqual(code, 1)
        self.assertIn("goals is not a property of source", output)

    def test_plain_text_edge_fails(self):
        code, output = self.check({"FND-001-claim": note("finding", sources=["the interview"])})
        self.assertEqual(code, 1)
        self.assertIn("is not a quoted [[wikilink]]", output)

    def test_aliased_and_pathed_links_resolve(self):
        code, output = self.check({
            "SRC-001-interview": note("source", record=RECORD),
            "FND-001-claim": note("finding", sources=["[[notes/src-001-INTERVIEW|Planner interview]]"]),
        })
        self.assertEqual(code, 0, output)

    def test_gaps_are_warnings_not_errors(self):
        code, output = self.check({
            "REQ-001-orphan": note("requirement"),
            "FND-001-claim": note("finding", evidence="contested"),
            "QST-001-who": note("question"),
        })
        self.assertEqual(code, 0, output)
        for expected in ("requirement has no supporting evidence", "requirement serves no goal",
                         "finding has no source", "contested finding names no competing finding",
                         "open item has no owner"):
            self.assertIn(expected, output)

    def test_closed_requirement_gap_is_not_reported(self):
        text = note("requirement").replace("status: open", "status: closed")
        code, output = self.check({"REQ-001-done": text})
        self.assertEqual(code, 0)
        self.assertNotIn("requirement has no supporting evidence", output)

    def test_invalid_date_and_unknown_kind_fail(self):
        code, output = self.check({
            "QST-001-when": note("question", due="next Friday"),
            "XYZ-001-mystery": note("mystery"),
        })
        self.assertEqual(code, 1)
        self.assertIn("due must be a valid YYYY-MM-DD date", output)
        self.assertIn("kind 'mystery' is not in the schema", output)

    def test_supersedes_must_point_to_same_kind(self):
        code, output = self.check({
            "GOL-001-old": note("goal"),
            "REQ-002-new": note("requirement", supersedes=["[[GOL-001-old]]"]),
        })
        self.assertEqual(code, 1)
        self.assertIn("supersedes must link to requirement, but GOL-001-old is goal", output)


    def raw(self, frontmatter, bom=""):
        return self.check({"ENG-001-charter": note("engagement"), "QST-001-raw": bom + "---\n" + frontmatter + "\n---\nBody.\n"})

    def test_empty_scalars_do_not_crash_and_empty_owner_warns(self):
        code, output = self.raw("kind: issue\nstatus: open\nowner:\nseverity:")
        self.assertEqual(code, 0, output)
        self.assertIn("open item has no owner", output)
        code, output = self.raw("kind:\nstatus:")
        self.assertEqual(code, 1)
        self.assertIn("kind None is not in the schema", output)

    def test_list_valued_kind_is_an_error_not_a_crash(self):
        code, output = self.raw("kind: [action]")
        self.assertEqual(code, 1)
        self.assertIn("is not in the schema", output)

    def test_block_list_links_must_be_quoted(self):
        code, output = self.check({
            "ENG-001-charter": note("engagement"),
            "SRC-001-a": note("source", record=RECORD),
            "FND-001-ok": "---\nkind: finding\nstatus: open\nowner: unassigned\nsources:\n  - \"[[SRC-001-a]]\"\n---\n",
            "FND-002-bad": "---\nkind: finding\nstatus: open\nowner: unassigned\nsources:\n  - [[SRC-001-a]]\n---\n",
        })
        self.assertEqual(code, 1)
        self.assertIn("FND-002-bad.md: line 6: unquoted link", output)
        self.assertNotIn("FND-001-ok.md: line", output)

    def test_yaml_forms_obsidian_accepts(self):
        code, output = self.raw(bom="\ufeff", frontmatter="kind: question # gap\nstatus: open\nowner: \"Finance: AP lead\"\nquestion_type: clarification\naliases:\n  - Who approves?")
        self.assertEqual(code, 0, output)
        code, output = self.check({"ENG-001-charter": note("engagement"),
                                   "SRC-001-a": "---\nkind: source\nstatus: open\nowner: unassigned\nrecord: " + RECORD + "\nrestrictions: |\n  Synthetic only.\n  No sharing.\n---\n"})
        self.assertEqual(code, 0, output)

    def test_unquoted_colon_value_fails_like_yaml(self):
        code, output = self.raw("kind: question\nstatus: open\nowner: Finance: AP lead")
        self.assertEqual(code, 1)
        self.assertIn("contains ': '", output)

    def test_impossible_date_and_bad_record_fail(self):
        code, output = self.check({"ENG-001-charter": note("engagement"),
                                   "QST-001-when": note("question", due="2026-13-45"),
                                   "SRC-001-a": note("source", record="interview@rev1")})
        self.assertEqual(code, 1)
        self.assertIn("due must be a valid YYYY-MM-DD date", output)
        self.assertIn("record must be <record-id>@<64-character revision>", output)

    def test_misspelled_property_warns(self):
        code, output = self.raw("kind: question\nstatus: open\nowner: unassigned\nquestoin_type: clarification")
        self.assertIn("property questoin_type is not in the schema", output)

    def test_property_of_another_kind_fails(self):
        code, output = self.check({"ENG-001-charter": note("engagement"), "SYS-001-erp": note("system"),
                                   "CAP-001-x": note("capability", systems=["[[SYS-001-erp]]"])})
        self.assertEqual(code, 1)
        self.assertIn("systems is not a property of capability", output)

    def test_superseded_target_must_be_marked(self):
        code, output = self.check({"ENG-001-charter": note("engagement"),
                                   "GOL-001-old": note("goal"),
                                   "GOL-002-new": note("goal", supersedes=["[[GOL-001-old]]"])})
        self.assertIn("supersedes GOL-001-old, which is not marked superseded", output)

    def test_one_current_engagement(self):
        code, output = self.check({"ENG-001-a": note("engagement"), "ENG-002-b": note("engagement")})
        self.assertEqual(code, 1)
        self.assertIn("more than one current engagement note", output)

    def test_non_utf8_note_is_an_error(self):
        root = self.vault({"ENG-001-charter": note("engagement")})
        (root / "notes" / "SRC-001-bad.md").write_bytes(b"---\nkind: source\nowner: \xff\n---\n")
        code, output = run("--vault", str(root), "--schema", str(SCHEMA))
        self.assertEqual(code, 1)
        self.assertIn("not UTF-8 text", output)


if __name__ == "__main__":
    unittest.main()
