---
kind: process
status: active
owner: unassigned
aliases: ["Allocate stock (as-is)"]
state: as-is
trigger: Customer order confirmed
outcome: Planner reserves on-hand stock to the order
supersedes: []
parent: []
replaces: []
capabilities: ["[[CAP-001-stock-allocation]]"]
goals: ["[[GOL-001-reliable-promises]]"]
roles: ["[[ROL-001-planner]]"]
organizations: ["[[ORG-001-plant-north]]"]
systems: ["[[SYS-001-erp-inventory]]"]
data: ["[[DAT-001-stock-batch]]"]
findings: ["[[FND-001-120-on-hand]]"]
sources: ["[[SRC-001-planner-statement]]"]
---
# Allocate stock (as-is) · synthetic

The planner reserves stock using on-hand quantity. Release status is not checked. Exception: blocked stock is discovered at picking, which forces reallocation.
