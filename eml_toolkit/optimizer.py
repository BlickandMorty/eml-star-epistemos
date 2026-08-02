"""A small, auditable rewrite optimizer for EML/EML-star expressions.

This replaces three invalid or unreachable upstream rewrites.  Rewrites are
structural and expose their branch assumptions; numerical equality tests cover
representative values but are not substitutes for analytic proofs.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

mp.mp.dps = 60


class Expr:
    def eval(self, z=None):
        raise NotImplementedError

    def depth(self) -> int:
        return 1

    def node_count(self) -> int:
        return 1


@dataclass(frozen=True)
class Const(Expr):
    value: complex

    def eval(self, z=None):
        return mp.mpc(self.value)

    def __repr__(self):
        return str(self.value)


@dataclass(frozen=True)
class Var(Expr):
    name: str = "z"

    def eval(self, z=None):
        return z

    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class EML(Expr):
    left: Expr
    right: Expr

    def eval(self, z=None):
        return mp.exp(self.left.eval(z)) - mp.log(self.right.eval(z))

    def depth(self):
        return 1 + max(self.left.depth(), self.right.depth())

    def node_count(self):
        return 1 + self.left.node_count() + self.right.node_count()

    def __repr__(self):
        return f"eml({self.left}, {self.right})"


@dataclass(frozen=True)
class EMLStar(Expr):
    left: Expr
    right: Expr

    def eval(self, z=None):
        return mp.exp(self.left.eval(z)) - mp.log(mp.conj(self.right.eval(z)))

    def depth(self):
        return 1 + max(self.left.depth(), self.right.depth())

    def node_count(self):
        return 1 + self.left.node_count() + self.right.node_count()

    def __repr__(self):
        return f"eml_star({self.left}, {self.right})"


@dataclass(frozen=True)
class Exp(Expr):
    arg: Expr

    def eval(self, z=None):
        return mp.exp(self.arg.eval(z))

    def depth(self):
        return 1 + self.arg.depth()

    def node_count(self):
        return 1 + self.arg.node_count()

    def __repr__(self):
        return f"exp({self.arg})"


@dataclass(frozen=True)
class Ln(Expr):
    arg: Expr

    def eval(self, z=None):
        return mp.log(self.arg.eval(z))

    def depth(self):
        return 1 + self.arg.depth()

    def node_count(self):
        return 1 + self.arg.node_count()

    def __repr__(self):
        return f"ln({self.arg})"


@dataclass(frozen=True)
class Sub(Expr):
    left: Expr
    right: Expr

    def eval(self, z=None):
        return self.left.eval(z) - self.right.eval(z)

    def depth(self):
        return 1 + max(self.left.depth(), self.right.depth())

    def node_count(self):
        return 1 + self.left.node_count() + self.right.node_count()

    def __repr__(self):
        return f"({self.left} - {self.right})"


@dataclass(frozen=True)
class Conj(Expr):
    arg: Expr

    def eval(self, z=None):
        return mp.conj(self.arg.eval(z))

    def depth(self):
        return 1 + self.arg.depth()

    def node_count(self):
        return 1 + self.arg.node_count()

    def __repr__(self):
        return f"conj({self.arg})"


def _is_const(expr: Expr, value: int) -> bool:
    return isinstance(expr, Const) and expr.value == value


class EGraphOptimizer:
    """Fixed-point simplifier with six branch-aware rewrite rules."""

    RULES = (
        "eml(eml(1,x),1) -> exp(exp(1)-ln(x))",
        "eml(ln(x),exp(y)) -> x-y",
        "eml(1,exp(x)) -> exp(1)-x",
        "eml_star(0,exp(z)) -> 1-conj(z) [principal strip]",
        "eml(0,x) -> 1-ln(x)",
        "eml(x,1) -> exp(x)",
    )

    def __init__(self, max_passes: int = 10):
        self.max_passes = max_passes
        self.rules_applied = 0

    def optimize(self, expr: Expr) -> Expr:
        self.rules_applied = 0
        for _ in range(self.max_passes):
            new_expr = self._apply_rules(expr)
            if new_expr == expr:
                return new_expr
            expr = new_expr
        return expr

    def _apply_rules(self, expr: Expr) -> Expr:
        if isinstance(expr, (Const, Var)):
            return expr
        if isinstance(expr, (Exp, Ln, Conj)):
            return type(expr)(self._apply_rules(expr.arg))
        if isinstance(expr, Sub):
            return Sub(self._apply_rules(expr.left), self._apply_rules(expr.right))

        if isinstance(expr, EML):
            left = self._apply_rules(expr.left)
            right = self._apply_rules(expr.right)

            # Specific patterns must precede the generic right-one rule.
            if isinstance(left, EML) and _is_const(left.left, 1) and _is_const(right, 1):
                self.rules_applied += 1
                return Exp(Sub(Exp(Const(1)), Ln(left.right)))
            if isinstance(left, Ln) and isinstance(right, Exp):
                self.rules_applied += 1
                return Sub(left.arg, right.arg)
            if _is_const(left, 1) and isinstance(right, Exp):
                self.rules_applied += 1
                return Sub(Exp(Const(1)), right.arg)
            if _is_const(left, 0):
                self.rules_applied += 1
                return Sub(Const(1), Ln(right))
            if _is_const(right, 1):
                self.rules_applied += 1
                return Exp(left)
            return EML(left, right)

        if isinstance(expr, EMLStar):
            left = self._apply_rules(expr.left)
            right = self._apply_rules(expr.right)
            if _is_const(left, 0) and isinstance(right, Exp):
                self.rules_applied += 1
                return Sub(Const(1), Conj(right.arg))
            return EMLStar(left, right)

        raise TypeError(f"unknown expression node: {type(expr)!r}")


# Compatibility aliases for callers of the original module.
_ExpNode = Exp
_LnNode = Ln
_SubNode = Sub
_ConjNode = Conj


if __name__ == "__main__":
    z = Var()
    original = EMLStar(Const(0), EML(z, Const(1)))
    optimizer = EGraphOptimizer()
    simplified = optimizer.optimize(original)
    print(f"Original:   {original}")
    print(f"Simplified: {simplified}")
    print(f"Rules:      {optimizer.rules_applied}")
