# Repository guidance

This repository is the public source of the Blueprinting engagement template. It holds reusable definitions only; engagements are created from it in separate private repositories.

- Never commit client names, client data, transcripts or anything from a real engagement. Examples stay fictional and say so.
- `navigation/Knowledge-graph.md` is the single source of truth for node kinds, properties, allowed values and edges. Change the schema there first, then the templates and Bases that use it.
- Each kind has exactly one `templates/<kind>.md`. Its frontmatter lists every property the schema defines for that kind, each starting at the schema's `defaults` value, with empty edges. Template bodies contain no wikilinks. `scripts/check.py` enforces this.
- Engagement vaults receive only the files listed in `template.json`. Anything an agent working in a vault needs to know belongs in `navigation/Knowledge-graph.md`, not in this file or the README.
- `template.json` lists every file under `templates/`, `views/` and `navigation/`. Only single-level `templates/<id>.md`, `views/<id>.base` and `navigation/<id>.md` files can be shipped; Blueprinting rejects anything else.
- Bump `version` in `template.json` for any change to a shipped file. Never rename or remove a kind, property or allowed value that existing vaults may use; add a new one and document the migration in the README.
- Run `python3 scripts/check.py` and `python3 -m unittest discover -s tests` before committing. CI runs both.
- Rendering in Obsidian is a separate check: open the example or a disposable Start vault and inspect the changed views.
- Branches follow dev, then main; publish a change to `main` only after it is tested on `dev`.
