# Live EML fork inventory

Inventory date: 2026-08-02. Every entry below is a public GitHub repository
under `BlickandMorty`. Forks preserve GitHub's parent relationship and original
history.

| Live repository | GitHub parent | Default branch | Portfolio purpose |
|---|---|---|---|
| [`eml_star`](https://github.com/BlickandMorty/eml_star) | `antparis/eml_star` | `main` | Clean upstream fork plus `epistemos-witnessed-eml` enhancement branch |
| [`oxieml-star`](https://github.com/BlickandMorty/oxieml-star) | `antparis/oxieml-star` in the `cool-japan/oxieml` fork network | `master` | Symbolic-regression and performance integration |
| [`eml-formalization`](https://github.com/BlickandMorty/eml-formalization) | `nasqret/eml-formalization` | `main` | Lean/Mathlib proof work |
| [`pyeml`](https://github.com/BlickandMorty/pyeml) | `janegbert/pyeml` | `main` | Small Python API comparison |
| [`eml-skill`](https://github.com/BlickandMorty/eml-skill) | `yaniv-golan/eml-skill` | `main` | Agent workflow integration |
| [`all_functions_from_eml`](https://github.com/BlickandMorty/all_functions_from_eml) | `minchoCoin/all_functions_from_eml` | `main` | Independent implementation comparison |

GitHub permits only one personal fork per fork network. Because
`antparis/oxieml-star` is already a fork in the `cool-japan/oxieml` network,
requesting both correctly resolves to the single `oxieml-star` repository.
That is a GitHub invariant, not a missing clone.

## Dedicated repository

[`eml-star-epistemos`](https://github.com/BlickandMorty/eml-star-epistemos) is
the non-fork flagship. It preserves the full upstream history while making the
Epistemos additions the default `main` branch. This separation keeps provenance
obvious: readers can compare the clean GitHub fork, the enhancement branch, and
the dedicated edition.

An entry's presence here means its Git object graph and default branch are live.
It does not imply that every upstream research claim is independently proved by
the Epistemos edition; use the theorem ledger for those distinctions.
