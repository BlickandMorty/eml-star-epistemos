# EML-star Epistemos

[![CI](https://github.com/BlickandMorty/eml-star-epistemos/actions/workflows/ci.yml/badge.svg)](https://github.com/BlickandMorty/eml-star-epistemos/actions/workflows/ci.yml)
[![Python 3.10–3.13](https://img.shields.io/badge/Python-3.10--3.13-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An evidence-carrying research toolkit for
`eml(x,y) = exp(x) - log(y)` and Anthony Monnerot's anti-holomorphic companion
`eml_star(x,y) = exp(x) - log(conj(y))`.

This is an attributed, full-history derivative of
[`antparis/eml_star`](https://github.com/antparis/eml_star), not a claim of
authorship over its paper or original operator. The Epistemos edition turns the
prototype into an installable, replayable research artifact: expressions keep
their syntax, numerical claims carry branch witnesses, and every theorem is
labelled by evidence strength.

The dedicated repository was assembled in August 2026, but the underlying EML
and EML-star research, source history, and experiments predate that publication
step. It consolidates the substantive Epistemos branch into one flagship so the
mathematics remains public without padding the profile with unchanged reference
forks.

## What this edition contributes

- A corrected public arithmetic API. The upstream tests silently fell back to
  inline functions when imports failed, so green tests did not exercise the
  installed package; the fallback is removed.
- An immutable EML/EML-star IR with canonical JSON, stable SHA-256 identities,
  structural size/depth, and deterministic evaluation receipts.
- An explicit branch-correction witness recording the integer `2*pi*i` jump,
  residual, precision, and tamper-evident receipt root.
- A multi-point conjecture explorer that returns the actual expression tree,
  digest, and error vector rather than only a coincident value at one point.
- Six audited optimizer rules. The upstream rules
  `eml(1,exp(x)) -> 1-x` and `eml(eml(1,x),1) -> exp(1-x)` were incorrect;
  their corrected right sides contain `exp(1)` and `log(x)`.
- A machine-readable theorem ledger separating structural Lean results,
  analytic results, conditional arguments, numerical evidence, and open work.
- Cross-platform packaging, strict tests, and GitHub Actions.

## Quick start

```bash
python -m venv .venv
python -m pip install -e ".[test]"
python -m pytest
```

```python
from eml_toolkit import Expr, witness_conjugation

z = Expr.var("z")
term = Expr.eml_star(Expr.const(0), Expr.eml(z, Expr.one()))
run = term.evaluate({"z": 1.25 + 0.8j})
print(term.to_source(), term.digest, run.receipt_root)

witness = witness_conjugation(1 + 20j)
print(witness.branch_index, witness.residual, witness.verified)
```

## Evidence ladder

| Label | Meaning |
|---|---|
| `formal-structural` | Checked structural statement in the included Lean schema; not an analytic complex-log proof |
| `analytic` | Mathematical argument not currently kernel-checked here |
| `analytic-conditional` | Analytic result with explicit domain/branch assumptions |
| `software-verified` | Deterministic executable invariant covered by tests |
| `numerical-evidence` | High-precision experiments; never presented as proof |
| `open` | A named obligation or conjecture remains unresolved |

See [`docs/THEOREM_LEDGER.md`](docs/THEOREM_LEDGER.md) for the claims and
falsifiers, and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the data flow.

## Original result and honest boundary

Monnerot's depth-two formula

```text
conj(z) = 1 - eml_star(0, eml(z, 1))
```

uses the principal complex logarithm and is exact on the stated half-open strip
`Im(z) in [-pi, pi)`. Outside that strip, it returns a representative separated
from `conj(z)` by an integer multiple of `2*pi*i`. The Epistemos witness makes
that integer explicit and replayable. It does **not** prove the separate open
branch-safety premise in the upstream Stone-Weierstrass density argument.

## Research map

The local audit also studies compatible projects without copying unlicensed
code: `nasqret/eml-formalization` (Apache-2.0, Lean),
`cool-japan/oxieml` (Apache-2.0, Rust), `antparis/oxieml-star`
(Apache-2.0, Python), `janegbert/pyeml` (MIT), and `yaniv-golan/eml-skill`
(MIT). See [`docs/RELATED_PROJECTS.md`](docs/RELATED_PROJECTS.md) for what each
teaches and where its license permits a derived fork.

The upstream comparison and consolidation record is in
[`docs/FORK_INVENTORY.md`](docs/FORK_INVENTORY.md).

## Scope and non-claims

- Numerical evidence is not a formal proof.
- A stable digest proves reproducibility/tamper evidence, not mathematical truth.
- Exact branch-cut endpoints should use symbolic or interval reasoning.
- The original paper PDFs and historical scripts remain for reproducibility;
  the maintained package lives in `eml_toolkit/`.

## Attribution and license

Original EML-star work: Anthony Monnerot (2026), extending Andrzej
Odrzywołek's EML operator. Epistemos edition: BlickandMorty (2026). See
[`NOTICE.md`](NOTICE.md) for the exact fork point and contribution boundary.
The repository is distributed under the MIT terms in [`LICENSE`](LICENSE),
consistent with the upstream README's license declaration.
