**Working material — not a client-approved baseline.**

This vault is the engagement's complete record and knowledge graph. Read [Knowledge graph](Knowledge-graph.md) first: it explains the node kinds, how links are recorded, the Graph view setup and the views that show gaps.

## Resume
Resume the explicitly named engagement in Blueprinting. Use the active bundle path it reports, not the newest-looking folder. Resolve pending operations, changed inputs and policy gaps before relying on conclusions.

## Create your first working note
1. In Obsidian **Settings → Core plugins**, enable **Templates**. In its settings, choose the active bundle's `templates/` folder reported by Resume. Update this setting after activating another bundle.
2. Create and name a Markdown note inside `notes/`. Open the command palette and run **Templates: Insert template**; select the template needed for your next question. The Base's **+ New** does not insert a selected template for you.
3. Edit the note's content and working properties: accountable role (`owner`), working status (`status`), requested response (`disposition`) and agreed date (`due`). Keep unknown owners/dates explicit; do not invent agreement.

**Agent alternative:** ask Blueprinting to run `template-create <template-id> <new-note-id>` at this engagement's explicit root. It uses only the active template and never replaces an existing note.

## Find and edit work
Open [Working notes](../views/Working-notes.base). **Open work** hides notes with `status: closed`; switch to **All working notes** to find them again. An empty view means no notes match, not that discovery is complete. Without Bases, navigate `notes/` or open [[Indexes/Current]] after asking Blueprinting to rebuild the index.

## Retain evidence
Saving a working note is not retaining reviewed evidence. Ask Blueprinting to intake material changes with source attribution, uncertainty and receiving ownership. Open [Retained index](../views/Retained-index.base) for derived revision navigation only. Never edit `records/` directly. Property edits cannot establish a client decision, publication permission or delivery.

## Before a client handoff
State whether the recipient must decide, act, review or take note. Name the requested response, accountable role, implications, approval status and agreed date. Keep unknowns visible. Use formal written briefs/workbooks and grounded editorial executive decks. Client-facing artifacts need their own evidence, permission, actual-render and exact-byte reviews.
