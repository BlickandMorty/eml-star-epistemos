# EML upstream comparison and consolidation record

Audit date: 2026-08-17.

## Flagship history

This repository preserves the full `antparis/eml_star` history and makes the
two-commit Epistemos research edition the default `main` line. At the time of
consolidation, the enhancement branch in the GitHub fork and this repository
resolved to the same commit:

```text
9814f796179b22cf6c63001bb177b2cf8ed81ab0
```

The duplicate fork page could therefore be retired without deleting the
enhancement, its ancestry, or the original author's history.

## Comparison projects

The research audit studied these independently authored implementations:

| Project | License at audit | What it helps compare |
| --- | --- | --- |
| `nasqret/eml-formalization` | Apache-2.0 | Lean/Mathlib formalization strategy |
| `cool-japan/oxieml` | Apache-2.0 | Rust symbolic-regression implementation |
| `antparis/oxieml-star` | Apache-2.0 | EML-star integration approach |
| `janegbert/pyeml` | MIT | Compact Python API |
| `yaniv-golan/eml-skill` | MIT | Agent-workflow presentation |
| `minchoCoin/all_functions_from_eml` | upstream terms | Independent implementation comparison |

Unmodified personal forks of those projects are not portfolio contributions.
They are unnecessary once upstream links, licenses, and local preservation
mirrors exist. No external code is relicensed here merely because it was
studied.

## Claim boundary

Preserving a Git graph establishes provenance, not mathematical truth. Use
`THEOREM_LEDGER.md` for formal, analytic, conditional, numerical, and open
statuses. The original EML-star operator and paper remain Anthony Monnerot's
work; the witnessed IR, receipts, corrected software rules, testing, packaging,
and evidence taxonomy are the Epistemos delta.
