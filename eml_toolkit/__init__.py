"""EML-star Epistemos edition: operators, witnessed IR, and evidence."""

from .branch import BranchWitness, witness_conjugation
from .core import *  # noqa: F403
from .ir import Expr, Evaluation
from .theorems import THEOREMS, TheoremRecord, TheoremStatus

__all__ = [
    "BranchWitness", "witness_conjugation", "Expr", "Evaluation",
    "THEOREMS", "TheoremRecord", "TheoremStatus",
]
