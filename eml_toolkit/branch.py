"""Explicit principal-branch witnesses for the EML-star conjugation formula."""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

from .core import conjugate_formula
from .receipts import Receipt, ReceiptChain, verify_receipts


def _number(value: complex) -> tuple[str, str]:
    z = mp.mpc(value)
    return mp.nstr(mp.re(z), 80), mp.nstr(mp.im(z), 80)


@dataclass(frozen=True, slots=True)
class BranchWitness:
    theorem_id: str
    input_value: tuple[str, str]
    principal_value: tuple[str, str]
    branch_index: int
    corrected_value: tuple[str, str]
    residual: str
    precision_dps: int
    receipts: tuple[Receipt, ...]
    receipt_root: str

    @property
    def verified(self) -> bool:
        tolerance = mp.power(10, -(max(10, self.precision_dps - 10)))
        return mp.mpf(self.residual) <= tolerance and verify_receipts(self.receipts)


def witness_conjugation(z: complex) -> BranchWitness:
    """Recover ``conj(z)`` and record the observed integer branch correction.

    This is an executable numerical witness, not a machine-checked proof of the
    analytic branch law.  Exact branch-cut endpoints require symbolic handling.
    """
    value = mp.mpc(z)
    principal = conjugate_formula(value)
    target = mp.conj(value)
    period = 2 * mp.pi
    branch_index = int(mp.nint(mp.im(target - principal) / period))
    corrected = principal + branch_index * period * mp.j
    residual = abs(corrected - target)

    chain = ReceiptChain()
    chain.append("input", {"z": _number(value), "dps": mp.mp.dps})
    chain.append("principal-evaluation", {"value": _number(principal)})
    chain.append(
        "branch-correction",
        {"index": branch_index, "period": mp.nstr(period, 80)},
    )
    chain.append(
        "claim-check",
        {"corrected": _number(corrected), "target": _number(target), "residual": mp.nstr(residual, 80)},
    )
    return BranchWitness(
        theorem_id="epistemos.branch-corrected-conjugation.v1",
        input_value=_number(value),
        principal_value=_number(principal),
        branch_index=branch_index,
        corrected_value=_number(corrected),
        residual=mp.nstr(residual, 80),
        precision_dps=mp.mp.dps,
        receipts=chain.receipts,
        receipt_root=chain.root,
    )
