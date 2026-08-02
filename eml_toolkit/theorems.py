"""Machine-readable theorem and claim-status registry."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TheoremStatus(str, Enum):
    FORMAL_STRUCTURAL = "formal-structural"
    ANALYTIC = "analytic"
    ANALYTIC_CONDITIONAL = "analytic-conditional"
    SOFTWARE_VERIFIED = "software-verified"
    NUMERICAL = "numerical-evidence"
    OPEN = "open"


@dataclass(frozen=True, slots=True)
class TheoremRecord:
    identifier: str
    statement: str
    status: TheoremStatus
    assumptions: tuple[str, ...]
    evidence: tuple[str, ...]
    falsifier: str


THEOREMS: tuple[TheoremRecord, ...] = (
    TheoremRecord(
        "eml.holomorphic-closure",
        "Every finite EML-only composition is holomorphic on its domain.",
        TheoremStatus.ANALYTIC,
        ("Each constituent is defined on the domain under discussion.",),
        ("Upstream paper, Theorem 2.1",),
        "Exhibit a finite EML-only term with a nonzero Wirtinger d/d(conj z).",
    ),
    TheoremRecord(
        "emlstar.conjugation-principal-strip",
        "1 - eml_star(0, eml(z, 1)) = conjugate(z) on the stated half-open strip.",
        TheoremStatus.ANALYTIC_CONDITIONAL,
        ("Im(z) is in [-pi, pi).", "Principal complex logarithm is used."),
        ("Upstream Theorems 3.1 and 3.2", "verify_theorem4.py"),
        "A point in the stated mathematical domain where exact evaluation differs.",
    ),
    TheoremRecord(
        "emlstar.density-conditional",
        "The EML/EML-star algebra is dense in C(K,C) under branch-safety assumptions.",
        TheoremStatus.OPEN,
        ("K is compact in the principal strip.", "All arithmetic witness trees are branch-safe."),
        ("Upstream Theorem 4.3", "branch_safety_final.py provides numerical evidence only"),
        "A failure of an assumption or counterexample to separation/closure on an admitted K.",
    ),
    TheoremRecord(
        "epistemos.branch-corrected-conjugation.v1",
        "The observed principal-branch representative is corrected by an explicit integer multiple of 2*pi*i.",
        TheoremStatus.NUMERICAL,
        ("Finite-precision mpmath evaluation.", "Exact branch endpoints are handled separately."),
        ("eml_toolkit.branch.witness_conjugation", "hash-chained replay receipts"),
        "A witness with a verified receipt chain whose corrected residual exceeds tolerance.",
    ),
    TheoremRecord(
        "epistemos.receipt-replay.v1",
        "Any mutation of canonical receipt material changes verification outcome.",
        TheoremStatus.SOFTWARE_VERIFIED,
        ("SHA-256 collision resistance.", "Canonical JSON v1 encoding."),
        ("eml_toolkit.receipts.verify_receipts", "tests/test_receipts.py"),
        "A mutated receipt accepted without a SHA-256 collision.",
    ),
    TheoremRecord(
        "epistemos.ir-structure.v1",
        "The EML-star IR has positive size and deterministic structural projections.",
        TheoremStatus.FORMAL_STRUCTURAL,
        (),
        ("formal/EpistemosEMLStar.lean",),
        "A Lean kernel build failure or a counterexample in the inductive grammar.",
    ),
)


def theorem(identifier: str) -> TheoremRecord:
    for record in THEOREMS:
        if record.identifier == identifier:
            return record
    raise KeyError(identifier)
