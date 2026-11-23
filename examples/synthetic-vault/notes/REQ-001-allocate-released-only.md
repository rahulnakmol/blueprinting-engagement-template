---
kind: requirement
status: open
owner: unassigned
aliases: ["Allocate released stock only"]
req_type: business-rule
priority: unknown
fit: unresolved
record:
product: Fictional ERP inventory module
location:
supersedes: []
parent: []
goals: ["[[GOL-001-reliable-promises]]"]
processes: ["[[PRC-001-allocate-stock-as-is]]"]
roles: ["[[ROL-001-planner]]"]
systems: ["[[SYS-001-erp-inventory]]"]
data: ["[[DAT-001-stock-batch]]"]
findings: ["[[FND-001-120-on-hand]]", "[[FND-002-60-released]]"]
sources: []
questions: ["[[QST-001-allocation-rule]]"]
---
# Allocate released stock only · proposed, synthetic

**Proposed rule, not confirmed:** only quality-released stock may be allocated to customer orders.

Acceptance example: with 120 on hand and 60 released, an allocation request for 100 units is limited to 60 and the remaining 40 are flagged as unfulfilled.

Priority stays unknown and fit unresolved until the operations director confirms the rule and the ERP's release-status behaviour is checked.
