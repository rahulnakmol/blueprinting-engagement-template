**Working map — not evidence, approval or a client baseline.**

# Engagement knowledge graph

This vault is the engagement's brain from first contact to closeout. Every person, goal, process, requirement, system, piece of evidence, decision, risk and deliverable is one note in `notes/`. Links between notes are typed properties, so Obsidian's Graph view, Backlinks and Bases show how evidence becomes requirements, decisions and deliverables, and where that chain is broken.

The graph is how you navigate and reason. It is not the evidence itself: retained, reviewed revisions live in `records/` and are written only by Blueprinting's helpers. A property value, a link or a closed status never establishes client acceptance, permission to share or delivery.

## How the graph is built

- **A node is a note.** Create it in `notes/` from the template for its kind. Its `kind` property says what it is; the graph and every Base filter on it. Keep exactly one `engagement` note: the charter every engagement starts from.
- **An edge is a property.** Each relationship is a list of quoted wikilinks in frontmatter, such as `sources: ["[[SRC-003-planner-interview]]"]`. Most edges are named after the kind they point to: `goals` holds goals, `findings` holds findings and `data` holds data objects. Five have their own meaning: `parent` (the broader note of the same kind), `supersedes` (the earlier version this note replaces), `replaces` (the as-is processes a to-be process changes), `contradicts` (a competing finding) and `affects` (any note a RAID item, question or action bears on).
- **Direction is fixed by the schema.** An edge exists only on the kinds the schema lists for it, and each relationship is recorded once, on that side. Obsidian shows the reverse in Backlinks and the Connections view, so never add a return link by hand; two copies drift apart. In general a note lists what it rests on, serves or contains: a finding lists its sources, a requirement its goals and findings, a decision what it decides, a deliverable what it presents, and a lifecycle note the nodes it produced or used. Two edges need a definition: on a `question`, `findings` are the evidence that raised it, and on a `finding`, `questions` are the questions that finding answers.

## Naming

Name each note `<PREFIX>-<NNN>-<slug>`: the kind's prefix from the schema, a three-digit number, and a short lowercase slug with hyphens, such as `REQ-014-credit-hold-release`. Numbers run per prefix: take the highest existing number for that prefix in `notes/` and add one; use four digits after 999. The whole name is at most 80 characters and starts with a letter. Put the human-readable name in `aliases`. Never rename or reuse an ID once a deliverable, retained record or client message has cited it.

## Status, owner and agreement

- **`status`** is one of four values. `open`: work on the node is still needed, such as an unanswered question, an unconfirmed requirement or an unaccepted risk. `active`: the node describes something established and in current use, such as a registered source, a recorded finding or a confirmed stakeholder. `closed`: no further work, with the reason in the body, such as an answered question, a withdrawn requirement or a held workshop. `superseded`: replaced by a newer node that lists it in `supersedes`.
- **`owner`** is the role accountable for moving the node forward: the consultant role for questions, actions and drafts, and the accountable client role for goals, decisions, data and risks the client must manage. Use a role, not a personal name, and leave `unassigned` until someone has accepted it.
- **Agreement is never a property.** A requirement or design becomes agreed only when a `decision` lists it in `requirements` and that decision's `record` names the retained decision record that passed Blueprinting's `baseline` check, covering the named client authority's written confirmation of that exact version. A `handover` then lists those decisions and requirements. Until then the requirement stays `open`, however complete it looks.
- **`record`** fields hold a retained record as `<record-id>@<64-character revision>`, exactly as Blueprinting reports it. Leave `record` empty until the record exists.

## Changing the graph

- **Supersede rather than delete.** When a node changes materially, create a new note with the next number, set its `supersedes` to the old note, and set the old note's `status` to `superseded`. Do not rewrite links in other notes to point at the successor: notes that cite the old version, such as decisions with retained records, must keep pointing at what they actually cited. New links point to the successor. Open a `question` that `affects` the notes still linked to the superseded node so someone checks each one.
- **Which notes you may edit.** You may edit the note you are creating, set `status: superseded` on a node you supersede, and add links to lifecycle notes, decisions and deliverables that collect the nodes they contain. Change another note's content only when the evidence or the owner's instruction requires it, and say so in that note's body.
- **Keep unknowns explicit.** Leave `owner: unassigned`, a rating of `unknown`, `fit: unresolved` or an empty date rather than guessing. An empty link list is a visible gap, not an error to hide.
- **The evidence chain** runs source → finding → goal, process, requirement or decision → deliverable. `source` notes cite their retained record in `record`, which ties the working graph to Blueprinting's immutable lineage.

## Node kinds

Evidence:
- `source` (SRC): a transcript, recording, notes, questionnaire, document, RFP, email or observation, with its processing restrictions and retained record.
- `finding` (FND): one attributed statement, observation or interpretation from a source, with its location and verification state.

Business:
- `engagement` (ENG): the single charter note for the engagement: client, journey, sponsors and decision authority.
- `goal` (GOL): a business driver, objective, outcome or KPI, with metric, baseline, target and date.
- `capability` (CAP): what the business must be able to do, in a level 1–3 hierarchy.
- `process` (PRC): an as-is or to-be process or step; a to-be process `replaces` the as-is processes it changes.
- `requirement` (REQ): one testable business requirement, with rule, exceptions, acceptance example and fit against the named product. An RFP obligation becomes a `finding` (clause in `location`, the RFP as its source) that the requirement cites.

People and organization:
- `stakeholder` (STK): a named person or group: their role, decision authority and stated concerns. Rate the role's influence and interest, not the person; keep ratings internal and out of client deliverables.
- `role` (ROL): a business role that performs work and holds responsibilities.
- `organization` (ORG): a business unit, legal entity, team, vendor, partner or customer segment.

Systems and data:
- `system` (SYS): an ERP or CRM module, SaaS product, legacy tool, spreadsheet or manual system, as functional context only.
- `data-object` (DAT): master, transactional, reference or report data, with its system of record and sensitivity.

Control:
- `decision` (DEC): an item that needs a named authority's response: a decision, an action they must take, a review or information.
- `question` (QST): missing evidence, a clarification, a contradiction to resolve or a decision still needed.
- `risk` (RSK), `assumption` (ASM), `issue` (ISS), `dependency` (DEP): the RAID log, each linked with `affects` to what it threatens or conditions.
- `action` (ACT): an owned task with a due date, usually created by a decision or question.

Outputs and learning:
- `deliverable` (DLV): a document, deck, workbook or package and what it contains.
- `estimate` (EST): an effort range with its inputs, assumptions and risks.
- `lesson` (LSN): a retrospective lesson and its reuse permission.

Lifecycle notes record the work of each stage and link to the nodes above: `opportunity` (OPP), `rfp` (RFP), `workshop` (WSH), `functional-design` (FDS), `handover` (HND), `debrief` (DBF) and `closeout` (CLS).

## Find your way around

- [Knowledge graph](../views/Knowledge-graph.base): every node by kind, the process map, capabilities, stakeholders, systems and data, and evidence.
- [Traceability](../views/Traceability.base): goals, requirements with their evidence and fit, decisions, deliverables and estimates.
- [Gaps](../views/Gaps.base): requirements with no evidence or goal, findings with no source, unverified or contested findings, open items without an owner, overdue work, the open RAID log and open questions. An empty view means nothing matches its rule, not that discovery is complete.
- [Connections](../views/Connections.base): drag this Base into the right sidebar. It then lists every note that links to the note you are reading, grouped by kind. Obsidian's core Backlinks pane shows the same links with the property that holds each one.
- [Working notes](../views/Working-notes.base): lifecycle notes, questions and actions that need a response.

### Set up the Graph view

Open **Graph view**. Under **Filters**, enter `path:notes/` so templates, views and records stay out of the picture. Under **Groups**, add one colour per layer:

- Evidence: `[kind:source] OR [kind:finding]`
- Business: `[kind:engagement] OR [kind:goal] OR [kind:capability] OR [kind:process] OR [kind:requirement]`
- People: `[kind:stakeholder] OR [kind:role] OR [kind:organization]`
- Systems and data: `[kind:system] OR [kind:data-object]`
- Control: `[kind:decision] OR [kind:question] OR [kind:risk] OR [kind:assumption] OR [kind:issue] OR [kind:dependency] OR [kind:action]`
- Outputs: `[kind:deliverable] OR [kind:estimate] OR [kind:lesson]`
- Lifecycle: `[kind:opportunity] OR [kind:rfp] OR [kind:workshop] OR [kind:functional-design] OR [kind:handover] OR [kind:debrief] OR [kind:closeout]`

Open **Local graph** from a note's menu to see only its neighbourhood. These settings stay on your machine.

## Agent workflow

Agents working in an engagement vault follow this section; the schema block below is the authority for kinds, properties and allowed values.

1. Run Blueprinting `resume` with the expected engagement ID. Read this file from the active bundle path it reports, not a newer-looking folder.
2. Create each node with `template-create <kind> <ID>`, which copies the active template into `notes/<ID>.md` and never replaces an existing note. Then edit only that note's frontmatter values and body. Keep every property the template defines, even when empty.
3. When ingesting evidence, retain it through Blueprinting's intake first. Then create one `source` note per source, with `record` set to its retained record ID and revision, and one `finding` per material attributed claim. Keep speaker uncertainty, location and verification state; set `evidence: contested` and fill `contradicts` when accounts disagree, without choosing a winner.
4. Before creating a node, search `notes/` for an existing node about the same thing, including its `aliases`. Extend or supersede it rather than creating a duplicate.
5. Link every new node only through the edges the schema lists for its kind. Open a `question` for each material gap: missing evidence, an unknown owner, an unresolved contradiction or an unconfirmed rule.
6. If the vault lacks a template for a kind you need, stop and ask to add it through Blueprinting's template upgrade (`template-preview`, `template-stage`, `template-activate`); do not hand-write a note for a kind without its template.
7. Before reporting progress, run `python3 <template-clone>/scripts/check.py --vault <engagement-root>` if a template clone is available, or else check the Gaps views' rules against the notes you changed. Fix every error and report the warnings that remain open.
8. Never edit `records/`, `.blueprinting/` or the active bundle's templates while working on an engagement. Never treat a property as approval: business acceptance needs the retained decision record and Blueprinting's `baseline` check. Client communication, sharing and cross-client reuse of lessons need their own approval.

## Schema

```json
{
  "schema": "blueprinting-knowledge-graph",
  "version": 1,
  "folder": "notes",
  "common": {"fields": {"kind": "kind", "status": "status", "owner": null, "aliases": "list"}, "edges": ["supersedes"]},
  "values": {
    "status": ["open", "active", "closed", "superseded"],
    "disposition": ["decision", "action", "review", "information"],
    "journey": ["opportunity", "pre-sales", "rfp", "discovery", "kickoff", "post-engagement"],
    "rating": ["high", "medium", "low", "unknown"],
    "organization_type": ["business-unit", "legal-entity", "team", "vendor", "partner", "customer-segment", "unknown"],
    "goal_type": ["driver", "objective", "outcome", "kpi"],
    "capability_level": ["L1", "L2", "L3", "unknown"],
    "maturity": ["1", "2", "3", "4", "5", "unknown"],
    "process_state": ["as-is", "to-be"],
    "requirement_type": ["functional", "business-rule", "reporting", "data", "integration-need", "non-functional", "compliance"],
    "priority": ["must", "should", "could", "wont", "unknown"],
    "fit": ["supported", "configuration", "extension", "process-change", "integration", "unresolved"],
    "system_type": ["erp", "crm", "saas", "legacy", "spreadsheet", "manual", "other"],
    "system_lifecycle": ["current", "target", "retire", "unknown"],
    "data_type": ["master", "transactional", "reference", "report"],
    "sensitivity": ["public", "internal", "confidential", "restricted", "unknown"],
    "source_type": ["transcript", "recording", "notes", "questionnaire", "document", "rfp", "email", "observation"],
    "claim_type": ["statement", "observation", "interpretation"],
    "evidence": ["unverified", "source-checked", "clarified", "contested"],
    "question_type": ["missing-evidence", "clarification", "contradiction", "decision-needed"],
    "risk_response": ["avoid", "mitigate", "transfer", "accept", "unknown"],
    "validation": ["unvalidated", "validated", "invalid"],
    "dependency_type": ["internal", "client", "third-party", "decision"],
    "deliverable_format": ["md", "docx", "pptx", "xlsx", "pdf-document", "pdf-deck", "zip"],
    "reuse": ["engagement-only", "review-for-reuse", "approved-for-reuse", "prohibited"],
    "outcome": ["won", "lost", "paused", "completed", "unknown"]
  },
  "defaults": {
    "status": "open",
    "owner": "unassigned",
    "disposition": {"decision": "decision", "rfp": "decision", "workshop": "action", "debrief": "information"},
    "disposition_default": "review",
    "rating": "unknown",
    "priority": "unknown",
    "fit": "unresolved",
    "evidence": "unverified",
    "validation": "unvalidated",
    "reuse": "engagement-only",
    "capability_level": "unknown",
    "maturity": "unknown",
    "organization_type": "unknown",
    "system_lifecycle": "unknown",
    "sensitivity": "unknown",
    "risk_response": "unknown",
    "outcome": "unknown"
  },
  "edges": {
    "sources": "source",
    "findings": "finding",
    "stakeholders": "stakeholder",
    "roles": "role",
    "organizations": "organization",
    "goals": "goal",
    "capabilities": "capability",
    "processes": "process",
    "requirements": "requirement",
    "systems": "system",
    "data": "data-object",
    "decisions": "decision",
    "questions": "question",
    "risks": "risk",
    "assumptions": "assumption",
    "issues": "issue",
    "dependencies": "dependency",
    "actions": "action",
    "deliverables": "deliverable",
    "estimates": "estimate",
    "lessons": "lesson",
    "parent": "same",
    "supersedes": "same",
    "replaces": "process",
    "contradicts": "finding",
    "affects": "any"
  },
  "kinds": {
    "source": {"prefix": "SRC", "layer": "evidence", "fields": {"source_type": "source_type", "captured": "date", "record": "record", "location": null, "restrictions": null}, "edges": ["stakeholders", "organizations"]},
    "finding": {"prefix": "FND", "layer": "evidence", "fields": {"claim_type": "claim_type", "evidence": "evidence", "location": null, "speaker": null, "record": "record"}, "edges": ["sources", "stakeholders", "contradicts", "questions"]},
    "engagement": {"prefix": "ENG", "layer": "business", "fields": {"client": null, "journey": "journey", "start": "date", "end": "date"}, "edges": ["stakeholders", "organizations", "goals"]},
    "goal": {"prefix": "GOL", "layer": "business", "fields": {"goal_type": "goal_type", "metric": null, "baseline": null, "target": null, "target_date": "date"}, "edges": ["parent", "stakeholders", "findings", "sources"]},
    "capability": {"prefix": "CAP", "layer": "business", "fields": {"level": "capability_level", "maturity_current": "maturity", "maturity_target": "maturity"}, "edges": ["parent", "goals", "organizations", "findings"]},
    "process": {"prefix": "PRC", "layer": "business", "fields": {"state": "process_state", "trigger": null, "outcome": null}, "edges": ["parent", "replaces", "capabilities", "goals", "roles", "organizations", "systems", "data", "findings", "sources"]},
    "requirement": {"prefix": "REQ", "layer": "business", "fields": {"req_type": "requirement_type", "priority": "priority", "fit": "fit", "record": "record", "product": null, "location": null}, "edges": ["parent", "goals", "processes", "roles", "systems", "data", "findings", "sources", "questions"]},
    "stakeholder": {"prefix": "STK", "layer": "people", "fields": {"title": null, "influence": "rating", "interest": "rating", "authority": null, "record": "record"}, "edges": ["organizations", "roles"]},
    "role": {"prefix": "ROL", "layer": "people", "fields": {}, "edges": ["parent", "organizations", "findings"]},
    "organization": {"prefix": "ORG", "layer": "people", "fields": {"org_type": "organization_type"}, "edges": ["parent"]},
    "system": {"prefix": "SYS", "layer": "systems", "fields": {"system_type": "system_type", "vendor": null, "module": null, "lifecycle": "system_lifecycle"}, "edges": ["organizations", "capabilities", "findings"]},
    "data-object": {"prefix": "DAT", "layer": "systems", "fields": {"data_type": "data_type", "sensitivity": "sensitivity"}, "edges": ["systems", "organizations", "findings"]},
    "decision": {"prefix": "DEC", "layer": "control", "fields": {"disposition": "disposition", "due": "date", "record": "record"}, "edges": ["stakeholders", "goals", "processes", "requirements", "findings", "questions", "risks", "assumptions"]},
    "question": {"prefix": "QST", "layer": "control", "fields": {"question_type": "question_type", "due": "date"}, "edges": ["affects", "findings", "sources", "stakeholders"]},
    "risk": {"prefix": "RSK", "layer": "control", "fields": {"likelihood": "rating", "impact": "rating", "response": "risk_response", "due": "date"}, "edges": ["affects", "findings", "sources"]},
    "assumption": {"prefix": "ASM", "layer": "control", "fields": {"validation": "validation", "due": "date"}, "edges": ["affects", "sources"]},
    "issue": {"prefix": "ISS", "layer": "control", "fields": {"severity": "rating", "due": "date"}, "edges": ["affects", "findings", "sources"]},
    "dependency": {"prefix": "DEP", "layer": "control", "fields": {"dependency_type": "dependency_type", "due": "date"}, "edges": ["affects", "organizations"]},
    "action": {"prefix": "ACT", "layer": "control", "fields": {"due": "date"}, "edges": ["affects", "decisions", "questions"]},
    "deliverable": {"prefix": "DLV", "layer": "output", "fields": {"format": "deliverable_format", "version": null, "record": "record"}, "edges": ["stakeholders", "goals", "processes", "requirements", "decisions", "findings", "estimates", "assumptions", "risks"]},
    "estimate": {"prefix": "EST", "layer": "output", "fields": {"unit": null, "low": null, "likely": null, "high": null, "confidence": "rating", "record": "record"}, "edges": ["requirements", "assumptions", "risks", "sources"]},
    "lesson": {"prefix": "LSN", "layer": "output", "fields": {"reuse": "reuse"}, "edges": ["findings", "decisions", "sources"]},
    "opportunity": {"prefix": "OPP", "layer": "lifecycle", "fields": {"disposition": "disposition", "due": "date"}, "edges": ["stakeholders", "organizations", "goals", "findings", "sources", "risks", "estimates", "deliverables"]},
    "rfp": {"prefix": "RFP", "layer": "lifecycle", "fields": {"disposition": "disposition", "due": "date", "record": "record"}, "edges": ["sources", "requirements", "questions", "risks", "assumptions", "estimates", "findings", "deliverables"]},
    "workshop": {"prefix": "WSH", "layer": "lifecycle", "fields": {"disposition": "disposition", "due": "date", "held": "date"}, "edges": ["stakeholders", "sources", "questions", "processes"]},
    "functional-design": {"prefix": "FDS", "layer": "lifecycle", "fields": {"disposition": "disposition", "due": "date"}, "edges": ["goals", "processes", "requirements", "roles", "systems", "decisions", "questions"]},
    "handover": {"prefix": "HND", "layer": "lifecycle", "fields": {"disposition": "disposition", "due": "date"}, "edges": ["requirements", "decisions", "deliverables", "roles", "issues", "dependencies", "actions"]},
    "debrief": {"prefix": "DBF", "layer": "lifecycle", "fields": {"disposition": "disposition", "due": "date", "period": null}, "edges": ["findings", "decisions", "questions", "actions", "sources"]},
    "closeout": {"prefix": "CLS", "layer": "lifecycle", "fields": {"disposition": "disposition", "due": "date", "outcome": "outcome"}, "edges": ["goals", "decisions", "deliverables", "actions", "lessons"]}
  }
}
```

In `fields`, a value names its allowed list in `values`; `date` takes a valid `YYYY-MM-DD` date, `list` takes text items, `record` takes `<record-id>@<64-character revision>`, and `null` takes free text. `defaults` gives each new note's starting value by field or value list; fields without one start empty. Every edge is a list of quoted wikilinks. `same` means the edge points to another note of the same kind; `any` means any kind. A node is stored only once in `notes/`; subfolders are allowed, but names must be unique across them.
