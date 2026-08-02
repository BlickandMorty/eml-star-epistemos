# Theorem and evidence ledger

The canonical machine-readable registry is `eml_toolkit/theorems.py`. This
human ledger exists so a reader can tell at a glance what is proved, tested,
conditional, or open.

| Identifier | Status | Core obligation |
|---|---|---|
| `eml.holomorphic-closure` | analytic | Functions and branches must be defined on the domain |
| `emlstar.conjugation-principal-strip` | analytic-conditional | Principal log; `Im(z) in [-pi,pi)` |
| `emlstar.density-conditional` | open | Requires branch-safe arithmetic witness trees on compact `K` |
| `epistemos.branch-corrected-conjugation.v1` | numerical-evidence | Finite precision; endpoints require symbolic treatment |
| `epistemos.receipt-replay.v1` | software-verified | Canonical JSON v1 and SHA-256 collision resistance |
| `epistemos.ir-structure.v1` | formal-structural | Concerns syntax/certificates only, not complex analysis |

## Epistemos branch-correction claim

Let `p(z)` be the value returned by the depth-two EML-star conjugation formula.
The executable witness searches for the integer `k` observed under principal-log
evaluation and records

```text
p(z) + 2*pi*i*k ~= conjugate(z).
```

The receipt includes the input, working precision, principal value, correction,
target, and residual. Its falsifier is concrete: produce a receipt-valid witness
whose residual exceeds the precision-derived tolerance. Passing this check is
still numerical evidence, not a Lean theorem.

## Open work worth contributing

1. A formal interval proof of branch safety for each intermediate node in the
   addition and multiplication witness trees.
2. A Mathlib formalization connecting the structural Lean certificate schema to
   principal `Complex.log` semantics.
3. Property-based counterexample search at branch-cut neighborhoods.
4. Proof-producing optimization: every rewrite should emit its assumptions and
   an equality certificate rather than only a smaller tree.
5. Cross-language canonical IR vectors shared by Python, Rust, and Lean.
