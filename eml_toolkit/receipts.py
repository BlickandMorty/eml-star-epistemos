"""Canonical, hash-chained receipts for replayable numerical evidence."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def stable_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class Receipt:
    sequence: int
    kind: str
    payload: dict[str, Any]
    previous_digest: str
    digest: str


class ReceiptChain:
    """Append-only receipt chain with deterministic serialization."""

    def __init__(self, receipts: Iterable[Receipt] = ()) -> None:
        self._receipts = list(receipts)

    @property
    def receipts(self) -> tuple[Receipt, ...]:
        return tuple(self._receipts)

    @property
    def root(self) -> str:
        return self._receipts[-1].digest if self._receipts else "0" * 64

    def append(self, kind: str, payload: dict[str, Any]) -> Receipt:
        sequence = len(self._receipts)
        previous = self.root
        material = {
            "version": 1,
            "sequence": sequence,
            "kind": kind,
            "payload": payload,
            "previous_digest": previous,
        }
        receipt = Receipt(sequence, kind, payload, previous, stable_digest(material))
        self._receipts.append(receipt)
        return receipt


def verify_receipts(receipts: Iterable[Receipt]) -> bool:
    previous = "0" * 64
    for sequence, receipt in enumerate(receipts):
        if receipt.sequence != sequence or receipt.previous_digest != previous:
            return False
        material = {
            "version": 1,
            "sequence": sequence,
            "kind": receipt.kind,
            "payload": receipt.payload,
            "previous_digest": previous,
        }
        if stable_digest(material) != receipt.digest:
            return False
        previous = receipt.digest
    return True
