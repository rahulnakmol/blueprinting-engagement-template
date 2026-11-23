# Synthetic practice only

`synthetic-vault/` is a small connected knowledge graph for a fictional multi-plant manufacturer. Open it as an Obsidian vault and start at `Start-here.md`; Bases views ship with Start bundles, not with this example. Check it with:

```sh
python3 scripts/check.py --vault examples/synthetic-vault --schema navigation/Knowledge-graph.md
```

It practises a planner reporting 120 on-hand units with release status unknown, followed by quality evidence that only 60 are released. These counts can coexist; the contested claim is the conclusion that 100 units can be allocated. Both attributed findings stay, a proposed requirement and an open question carry the gap, and the allocation decision stays unapproved. The one checker warning, a risk with no owner, is deliberate.

These are exercise notes, not observed client facts, accepted requirements or receipts. No example files are installed by the template manifest.
