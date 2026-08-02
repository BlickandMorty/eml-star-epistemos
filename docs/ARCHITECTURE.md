# Architecture

```text
Expr (immutable syntax)
  -> canonical JSON + SHA-256 identity
  -> high-precision evaluation
  -> append-only receipt chain
  -> branch witness / theorem record
  -> independent replay and falsifier
```

`core.py` is the reference numerical semantics. `ir.py` preserves expression
structure and generates evaluation receipts. `branch.py` records principal-log
corrections. `theorems.py` prevents evidence-level drift. The conjecture explorer
operates on IR terms, so a hit can be serialized, replayed on multiple points,
and promoted only after stronger analysis.

The design comes from Epistemos' earlier primitive-IR, explicit runtime-witness,
and deterministic-receipt work: runtime observations are carried as evidence,
not smuggled into a hidden proof body.
