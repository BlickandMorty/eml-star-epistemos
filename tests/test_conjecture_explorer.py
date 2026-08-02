import mpmath as mp

from eml_toolkit.conjecture_explorer import ConjectureExplorer, score_expression
from eml_toolkit.ir import Expr


def test_candidate_retains_expression_and_error_vector():
    expression = Expr.eml(Expr.var(), Expr.one())
    points = [mp.mpc("0.2"), mp.mpc("0.5", "0.1"), mp.mpc("-0.4", "0.2")]
    candidate = score_expression(expression, mp.exp, points)
    assert candidate.expression == expression
    assert candidate.digest == expression.digest
    assert len(candidate.errors) == len(points)
    assert mp.mpf(candidate.max_error) < mp.mpf("1e-55")


def test_explorer_requires_multiple_points():
    explorer = ConjectureExplorer(num_rollouts=1)
    try:
        explorer.explore(mp.exp, [mp.mpc(1)])
    except ValueError as error:
        assert "two" in str(error)
    else:
        raise AssertionError("one-point identity search was accepted")
