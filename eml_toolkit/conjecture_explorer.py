"""Reproducible multi-point conjecture search over expression trees.

Unlike the upstream prototype, candidates retain their syntax, stable digest,
and complete test vector.  Agreement at one point is never reported as an
identity.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Callable, Iterable

import mpmath as mp

from .ir import Expr


@dataclass(frozen=True, slots=True)
class Candidate:
    expression: Expr
    errors: tuple[str, ...]
    max_error: str

    @property
    def digest(self) -> str:
        return self.expression.digest


def score_expression(
    expression: Expr,
    target_fn: Callable[[complex], complex],
    points: Iterable[complex],
) -> Candidate:
    errors = []
    for point in points:
        got = expression.evaluate({"z": point}).value
        errors.append(abs(got - target_fn(point)))
    maximum = max(errors, default=mp.inf)
    return Candidate(
        expression,
        tuple(mp.nstr(error, 80) for error in errors),
        mp.nstr(maximum, 80),
    )


def _random_expr(depth: int, rng: random.Random) -> Expr:
    leaves = (Expr.var(), Expr.one(), Expr.const(0), Expr.const(-1), Expr.const(2))
    if depth <= 0 or rng.random() < 0.3:
        return rng.choice(leaves)
    constructor = Expr.eml if rng.random() < 0.5 else Expr.eml_star
    return constructor(_random_expr(depth - 1, rng), _random_expr(depth - 1, rng))


class ConjectureExplorer:
    def __init__(self, max_depth=4, num_rollouts=200, num_workers=1, dps=60, seed=2026):
        if num_workers != 1:
            raise ValueError("deterministic edition currently requires num_workers=1")
        self.max_depth = max_depth
        self.num_rollouts = num_rollouts
        self.num_workers = num_workers
        self.dps = dps
        self.seed = seed
        self.results: list[Candidate] = []

    def explore(self, target_fn, test_points=None, tolerance=None):
        mp.mp.dps = self.dps
        points = tuple(test_points or (
            mp.mpc("0.57721", "0.3"),
            mp.mpc("1.2", "-0.8"),
            mp.mpc("-0.4", "1.1"),
        ))
        if len(points) < 2:
            raise ValueError("at least two test points are required")
        limit = mp.mpf(tolerance or mp.power(10, -(self.dps - 10)))
        rng = random.Random(self.seed)
        seen: set[str] = set()
        matches = []
        for _ in range(self.num_rollouts):
            expression = _random_expr(self.max_depth, rng)
            if expression.digest in seen:
                continue
            seen.add(expression.digest)
            try:
                candidate = score_expression(expression, target_fn, points)
            except (ValueError, ZeroDivisionError, OverflowError):
                continue
            if mp.mpf(candidate.max_error) <= limit:
                matches.append(candidate)
        self.results = sorted(matches, key=lambda item: (mp.mpf(item.max_error), item.digest))
        return self.results[:10]

    def report(self):
        if not self.results:
            return "No multi-point matches found."
        return "\n".join(
            f"{index:>2}. {item.expression.to_source()} max_error={item.max_error} digest={item.digest[:12]}"
            for index, item in enumerate(self.results[:10], 1)
        )
