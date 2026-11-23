# Blueprinting engagement template

**Public reusable template, licensed under GPL-3.0. Never commit client material to this repository.**

A selectable working vault for one opportunity or engagement. The vault is the engagement's
complete record: evidence, working notes, decisions, debriefs and handoffs live in its Markdown
files and Git history. Notion is not required. Connect it only if you separately choose and
authorize it for cross-engagement summaries. Use it with Blueprinting's
shared helper contract 1. No client data, external integrations, community plugins, approval
receipts or brand assets are bundled. Create a separate private Git repository per engagement;
configure its backup and access explicitly. Never use this reusable source repository for clients.

Clone this repository onto the machine running the engagement thread, then give Blueprinting
that clone's absolute path. Pin a commit for each engagement so its active bundle is reproducible:

```sh
git clone https://github.com/rahulnakmol/blueprinting-engagement-template.git
```

Each engagement vault is a separate private repository, not a fork of this public one. A GitHub
fork of a public repository is public. GPL-3.0 conditions apply when you convey this template or
a modified version; take legal advice before relying on how they apply to a client deliverable.

## Start with the next decision

Ask Blueprinting to Start with an explicit destination, engagement identity, journey, policy
and selected template IDs. Review the no-write preview before confirming it. Start creates
only selected definitions and navigation, not a document for every possible activity.
Create a working note when it serves an actual question. Unresolved policy is not permission.

| Template ID | Use when | Decision or action it supports |
| --- | --- | --- |
| opportunity | Positioning, pitch or pre-sales | Whether and how to pursue the opportunity |
| rfp | Responding to an issued solicitation | Bid/no-bid and evidenced obligation-by-obligation response |
| workshop | Preparing a session, questionnaire or evidence debrief | Which uncertainty to resolve with whom |
| functional-design | Reimagining processes and responsibilities | Which functional option meets the business outcome |
| decision | Presenting a decision, action, review or information item | A named authority's exact response |
| handover | Implementation kickoff or transfer | Whether the baseline and receiving owners are ready |
| debrief | Daily or agreed periodic reflection | What changed and what response is due |
| closeout | Won, lost, paused or completed engagement | Open commitments, outcome follow-up and permitted learning |

## Open in Obsidian

Open the **instantiated engagement directory**, not this source repository, as a vault.
Core Bases is sufficient. `resume <engagement-id>` reports the active bundle and its exact
navigation/view paths. Open that bundle's `navigation/Start-here.md`. A staged or historical
bundle may be visible in the file explorer but must not be used as the current template.

Only `notes/` appears in the editable working-note Base. Retained `records/` are immutable;
never change their properties with Bases. `Indexes/` contains helper-generated projections,
when requested. They are navigation, not evidence or approval. Without Bases, use the Markdown
index and ordinary note links. No Obsidian Sync or external account is needed for local use.

## Updates preserve working material

Use `template-preview`, inspect baseline/local/incoming text, resolve conflicts explicitly,
then stage and activate. Definitions, Bases and navigation are the entire upgrade allowlist.
Instantiated notes, policy, evidence and approvals are never upgrade targets. The active
manifest changes only after the new bundle is complete; incomplete staging stays inactive.
Update Obsidian's optional core Templates folder to the newly reported active `templates/`
path after activation, or use `template-create` to avoid a stale folder setting.

An asset edit is not acceptance of a business requirement. Retain material working-note changes
through explicit intake and review. Sharing, client communication and cross-client reuse need
separate permission. Follow the engagement's retention policy; do not infer deletion authority.

## Local checks and qualification

The host `ampcode` repository tests the public template/Start/Resume contracts. Actual Obsidian
editing, filtering, navigation and save/reopen are separate qualification gates. `examples/`
holds isolated synthetic practice material only; it is excluded from template selection.
