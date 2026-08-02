"""Immutable EML/EML-star expression IR with canonical provenance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import mpmath as mp

from .core import eml, eml_star
from .receipts import Receipt, ReceiptChain, canonical_json, stable_digest


def _number(value: complex) -> tuple[str, str]:
    z = mp.mpc(value)
    return mp.nstr(mp.re(z), 80), mp.nstr(mp.im(z), 80)


@dataclass(frozen=True, slots=True)
class Evaluation:
    expression_digest: str
    value: complex
    receipts: tuple[Receipt, ...]
    receipt_root: str


@dataclass(frozen=True, slots=True)
class Expr:
    """A small typed-by-construction term algebra.

    Valid operations are ``one``, ``const``, ``var``, ``eml``, and
    ``eml_star``.  The canonical digest is independent of Python object IDs.
    """

    op: str
    args: tuple["Expr", ...] = ()
    literal: str | tuple[str, str] | None = None

    def __post_init__(self) -> None:
        arity = {"one": 0, "const": 0, "var": 0, "eml": 2, "eml_star": 2}
        if self.op not in arity or len(self.args) != arity[self.op]:
            raise ValueError(f"invalid {self.op!r} expression arity")
        if self.op in {"const", "var"} and self.literal is None:
            raise ValueError(f"{self.op} requires a literal")
        if self.op not in {"const", "var"} and self.literal is not None:
            raise ValueError(f"{self.op} cannot carry a literal")

    @classmethod
    def one(cls) -> "Expr":
        return cls("one")

    @classmethod
    def const(cls, value: complex) -> "Expr":
        return cls("const", literal=_number(value))

    @classmethod
    def var(cls, name: str = "z") -> "Expr":
        if not name:
            raise ValueError("variable name cannot be empty")
        return cls("var", literal=name)

    @classmethod
    def eml(cls, left: "Expr", right: "Expr") -> "Expr":
        return cls("eml", (left, right))

    @classmethod
    def eml_star(cls, left: "Expr", right: "Expr") -> "Expr":
        return cls("eml_star", (left, right))

    @property
    def size(self) -> int:
        return 1 + sum(arg.size for arg in self.args)

    @property
    def depth(self) -> int:
        return 0 if not self.args else 1 + max(arg.depth for arg in self.args)

    def canonical(self) -> dict:
        result: dict = {"op": self.op}
        if self.literal is not None:
            result["literal"] = self.literal
        if self.args:
            result["args"] = [arg.canonical() for arg in self.args]
        return result

    @property
    def canonical_json(self) -> str:
        return canonical_json(self.canonical())

    @property
    def digest(self) -> str:
        return stable_digest(self.canonical())

    def to_source(self) -> str:
        if self.op == "one":
            return "1"
        if self.op == "var":
            return str(self.literal)
        if self.op == "const":
            real, imag = self.literal  # type: ignore[misc]
            return real if imag == "0.0" else f"({real}+{imag}i)"
        name = "eml" if self.op == "eml" else "eml_star"
        return f"{name}({self.args[0].to_source()}, {self.args[1].to_source()})"

    def evaluate(self, environment: Mapping[str, complex]) -> Evaluation:
        chain = ReceiptChain()

        def visit(expr: "Expr"):
            if expr.op == "one":
                value = mp.mpc(1)
            elif expr.op == "const":
                real, imag = expr.literal  # type: ignore[misc]
                value = mp.mpc(real, imag)
            elif expr.op == "var":
                name = str(expr.literal)
                if name not in environment:
                    raise KeyError(f"missing value for variable {name!r}")
                value = mp.mpc(environment[name])
            else:
                left = visit(expr.args[0])
                right = visit(expr.args[1])
                value = eml(left, right) if expr.op == "eml" else eml_star(left, right)
            chain.append(
                "evaluate",
                {
                    "expression": expr.digest,
                    "op": expr.op,
                    "value": _number(value),
                },
            )
            return value

        value = visit(self)
        chain.append(
            "evaluation-complete",
            {"expression": self.digest, "value": _number(value), "dps": mp.mp.dps},
        )
        return Evaluation(self.digest, value, chain.receipts, chain.root)
