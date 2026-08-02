# Related EML projects and fork plan

Only repositories with a clear permissive license are candidates for derived
work. A fork preserves authorship and history; it is not a claim that the base
project was written by this account.

| Repository | License | Useful specialization |
|---|---|---|
| `antparis/eml_star` | README declares MIT | Anti-holomorphic theory; base of this repository |
| `antparis/oxieml-star` | Apache-2.0 | Applied symbolic-regression experiments |
| `cool-japan/oxieml` | Apache-2.0 | Rust search engine and performance work |
| `nasqret/eml-formalization` | Apache-2.0 code / CC BY-SA docs | Lean proof architecture and partial semantics |
| `janegbert/pyeml` | MIT | Small Python API and usability baseline |
| `yaniv-golan/eml-skill` | MIT | Agent-facing EML workflow packaging |

Repositories without a detected license were reviewed only as public prior art;
their code is not copied into this edition.

Recommended portfolio roles:

1. `eml-star-epistemos`: the flagship correctness and evidence project.
2. A focused `oxieml` fork: benchmarks, typed IR interchange, and Rust/Python
   reproducibility—not a cosmetic fork.
3. An `eml-formalization` fork only when it contains a small, upstreamable Lean
   proof contribution.
4. `pyeml` or `eml-skill` forks only if they receive a distinct integration;
   empty forks do not help an employer evaluate engineering ability.
