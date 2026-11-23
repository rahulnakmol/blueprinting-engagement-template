# Blueprinting engagement template

**Public reusable template, licensed under GPL-3.0. Never commit client material to this repository.**

An Obsidian-compatible Markdown vault that is one engagement's complete brain, from first contact to closeout. Every stakeholder, goal, capability, process, requirement, system, piece of evidence, decision, risk, deliverable and lesson is a linked note, so the vault is a knowledge graph you can navigate, query and check. Evidence, working notes, decisions, debriefs and handoffs live in its Markdown files and Git history. Notion is not required; connect it only if you separately choose and authorize it for cross-engagement summaries.

Use it with Blueprinting's shared helper contract 1. No client data, external integrations, community plugins, approval receipts or brand assets are bundled. Create a separate private Git repository per engagement and configure its backup and access explicitly.

## Get the template

Clone this repository onto the machine running the engagement thread, then give Blueprinting that clone's absolute path. Pin a commit for each engagement so its active bundle is reproducible:

```sh
git clone https://github.com/rahulnakmol/blueprinting-engagement-template.git
```

Each engagement vault is a separate private repository, not a fork of this public one. A GitHub fork of a public repository is public. GPL-3.0 conditions apply when you convey this template or a modified version; take legal advice before relying on how they apply to a client deliverable.

## How the knowledge graph works

[navigation/Knowledge-graph.md](navigation/Knowledge-graph.md) is the guide and the authority. It defines every node kind, the typed relationships between them and their allowed values, how to set up Obsidian's Graph view, and the workflow agents follow. In short:

- **A node is a note** in `notes/`, created from the template for its kind and named by a stable ID such as `REQ-014-credit-hold-release`.
- **An edge is a property** holding quoted wikilinks, such as `goals: ["[[GOL-002-cash-conversion]]"]`. The schema fixes which side each relationship lives on; Obsidian shows the reverse in Backlinks.
- **The evidence chain** runs source → finding → goal, process, requirement or decision → deliverable, and `record` fields cite Blueprinting's immutable retained records. A requirement is agreed only through a decision whose retained record passed Blueprinting's baseline check, never through a property.
- **Gaps are visible.** The Gaps Base lists requirements without evidence or goals, unverified or contested findings, open items with no owner and overdue work.

### Node kinds

| Layer | Kinds |
| --- | --- |
| Evidence | `source`, `finding` |
| Business | `engagement`, `goal`, `capability`, `process`, `requirement` |
| People | `stakeholder`, `role`, `organization` |
| Systems and data | `system`, `data-object` |
| Control | `decision`, `question`, `risk`, `assumption`, `issue`, `dependency`, `action` |
| Outputs and learning | `deliverable`, `estimate`, `lesson` |
| Lifecycle | `opportunity`, `rfp`, `workshop`, `functional-design`, `handover`, `debrief`, `closeout` |

### Views

| Base | Shows |
| --- | --- |
| Knowledge-graph | Every node by kind, the process map, capabilities, stakeholders, systems and data, evidence |
| Traceability | Goals, requirements with evidence and fit, decisions, deliverables, estimates |
| Gaps | Missing evidence or goals, findings to verify, unowned open items, overdue work, RAID log, open questions |
| Connections | In the right sidebar: every note linking to the note you are reading |
| Working-notes | Lifecycle notes, questions and actions that need a response |
| Retained-index | Derived navigation of retained records |

## Start an engagement

Ask Blueprinting to Start with an explicit destination, engagement identity, journey, policy and selected template IDs. Review the no-write preview before confirming it. For a complete brain, select every kind; for a short pre-sales pursuit, the evidence, people, goal, control and `opportunity` kinds may be enough. Add kinds later with a template upgrade. Start creates only definitions and navigation, not a note for every possible activity. Create a note when it serves an actual question, beginning with one `engagement` charter. Unresolved policy is not permission.

## Open in Obsidian

Open the **instantiated engagement directory**, not this source repository, as a vault. Core Bases and Graph view are sufficient; no community plugins, Obsidian Sync or external account is needed. `resume <engagement-id>` reports the active bundle and its exact navigation and view paths. Open that bundle's `navigation/Start-here.md`. A staged or historical bundle may be visible in the file explorer but must not be used as the current template.

Retained `records/` are immutable; never change their properties with Bases. `Indexes/` contains helper-generated projections, when requested. They are navigation, not evidence or approval.

## Upgrade an existing engagement

Template version 2 adds the knowledge graph. Upgrading a version 1 vault uses Blueprinting's normal path: `template-preview` with the template IDs to keep or add, inspect baseline, local and incoming text, resolve conflicts explicitly, then `template-stage` and `template-activate`. Definitions, Bases and navigation are the entire upgrade allowlist; existing notes, policy, evidence and approvals are never changed. Existing notes keep working: add the new properties to a note when you next link it into the graph. Update Obsidian's optional core Templates folder to the newly reported active `templates/` path, or use `template-create`.

An asset edit is not acceptance of a business requirement. Retain material changes through explicit intake and review. Sharing, client communication and cross-client reuse need separate permission. Follow the engagement's retention policy; do not infer deletion authority.

## Check the template and a vault

`scripts/check.py` uses only the Python standard library:

```sh
python3 scripts/check.py                    # this repository: schema, manifest and templates agree
python3 scripts/check.py --vault <root>     # an engagement vault: kinds, values and typed links
python3 -m unittest discover -s tests       # the checker's own tests
```

A vault check reads the schema from the active bundle. It reports invalid values, unquoted or broken links, links to the wrong kind of note and more than one engagement charter as errors, and lists gaps such as requirements without evidence as warnings. Copy the script into the engagement repository, or run it from a template clone. It reads only `notes/` and never writes. A clean check means the graph is structurally consistent, not that discovery is complete or anything is approved.

The host `ampcode` repository tests the template, Start and Resume contracts. Rendering in Obsidian is a separate check. `examples/` holds an isolated synthetic graph for practice; it is excluded from template selection.
