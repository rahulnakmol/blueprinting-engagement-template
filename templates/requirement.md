---
kind: requirement
status: open
owner: unassigned
aliases: []
req_type:
priority: unknown
fit: unresolved
record:
product:
location:
supersedes: []
parent: []
goals: []
processes: []
roles: []
systems: []
data: []
findings: []
sources: []
questions: []
---
# Requirement

**Purpose:** State one testable business requirement, traced to the goals it serves and the evidence it rests on.

## Statement
Write the requirement as one business outcome or rule. Set `req_type` and `priority` (must, should, could, wont). Use `parent` for detail under a broader requirement.

## Rule and exceptions
State the business rule, its conditions and every exception. Name the receiving owner of each exception.

## Acceptance example
Give a concrete input and expected result that distinguishes a correct implementation from a plausibly wrong one.

## Traceability
List the `goals` served, the `processes` and `roles` affected, relevant `systems` and `data`, the supporting `findings` and `sources`, and open `questions`. A requirement with no evidence is a hypothesis. For an RFP obligation, cite the `finding` that quotes the clause and put the obligation ID in `location`.

## Fit
Name the `product` and version or edition assessed. Set `fit` to supported, configuration, extension, process-change, integration or unresolved, with dated evidence, limitations and alternatives. A marketing page or demo is not proof for a specific configuration.

## Agreement
This requirement is agreed only when a `decision` lists it and that decision's `record` holds the retained, baseline-checked decision. Set `record` here to the retained requirement record when Blueprinting retains it.
