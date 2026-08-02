# Contributing

Contributions are welcome when they improve correctness, reproducibility, or
proof strength.

1. Install with `python -m pip install -e ".[test]"`.
2. Run `python -m pytest` before opening a pull request.
3. Give every mathematical claim an entry in `eml_toolkit/theorems.py` with
   assumptions, evidence, and a concrete falsifier.
4. Do not promote numerical agreement to analytic or formal status.
5. Optimizer rewrites must include equivalence tests and document branch/domain
   assumptions.
6. Preserve upstream attribution and update `NOTICE.md` when importing licensed
   material from another project.

The highest-value contributions are interval branch certificates, Mathlib
bridges for principal complex logarithms, property-based branch-cut tests, and
cross-language canonical IR fixtures.
