# Provenance and attribution

This repository preserves the complete Git history of Anthony Monnerot's
[`antparis/eml_star`](https://github.com/antparis/eml_star). The Epistemos
edition begins from upstream commit
`f92b59fad37e979e229c9d949e32fcb47db7c7cc`.

The EML-star operator, its paper, original scripts, and original theorem claims
are Monnerot's work, extending Andrzej Odrzywołek's EML research. The upstream
README states an MIT license but did not contain a standalone license file at
the fork point; this repository adds the conventional MIT text while retaining
the upstream copyright.

The immutable IR, canonical receipts, branch witnesses, theorem-status
registry, deterministic conjecture search, corrected optimizer, packaging,
tests, and Lean structural certificate schema are Epistemos-edition additions.
They adapt ideas previously developed in BlickandMorty's Epistemos formal
primitives and deterministic-agent-kernel projects.

Nothing in this repository should be cited as a formal proof of the upstream
open branch-safety lemma. Claim levels are deliberately recorded in
[`docs/THEOREM_LEDGER.md`](docs/THEOREM_LEDGER.md).
