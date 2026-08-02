import mpmath as mp
import pytest

from eml_toolkit.optimizer import Conj, Const, EGraphOptimizer, EML, EMLStar, Exp, Ln, Sub, Var


@pytest.mark.parametrize(
    "expression,value",
    [
        (EML(Var(), Const(1)), mp.mpc("0.4", "0.2")),
        (EML(Const(1), Exp(Var())), mp.mpc("0.4")),
        (EML(Ln(Const(2)), Exp(Var())), mp.mpc("0.4")),
        (EMLStar(Const(0), EML(Var(), Const(1))), mp.mpc("0.4", "0.2")),
        (EML(EML(Const(1), Const(2)), Const(1)), mp.mpc("0.4")),
        (EML(Const(0), Const(2)), mp.mpc("0.4")),
    ],
)
def test_each_rewrite_preserves_value_on_admitted_example(expression, value):
    optimized = EGraphOptimizer().optimize(expression)
    assert abs(expression.eval(value) - optimized.eval(value)) < mp.mpf("1e-50")


def test_previously_wrong_rule_has_exp_one_not_one():
    optimized = EGraphOptimizer().optimize(EML(Const(1), Exp(Var())))
    assert optimized == Sub(Exp(Const(1)), Var())


def test_specific_rule_is_reachable_before_generic_rule():
    optimized = EGraphOptimizer().optimize(EML(EML(Const(1), Const(2)), Const(1)))
    assert optimized == Exp(Sub(Exp(Const(1)), Ln(Const(2))))


def test_helper_nodes_report_real_structure():
    expression = Sub(Exp(Var()), Conj(Ln(Const(2))))
    assert expression.depth() == 4
    assert expression.node_count() == 6
