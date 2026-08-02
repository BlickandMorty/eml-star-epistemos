import mpmath as mp

from eml_toolkit.ir import Expr
from eml_toolkit.receipts import verify_receipts


def test_ir_has_stable_identity_and_structural_metrics():
    z = Expr.var("z")
    term = Expr.eml_star(Expr.const(0), Expr.eml(z, Expr.one()))
    rebuilt = Expr.eml_star(Expr.const(0), Expr.eml(Expr.var("z"), Expr.one()))
    assert term == rebuilt
    assert term.digest == rebuilt.digest
    assert term.size == 5
    assert term.depth == 2
    assert "eml_star" in term.to_source()


def test_evaluation_produces_replayable_receipts():
    term = Expr.eml(Expr.var("z"), Expr.one())
    result = term.evaluate({"z": mp.mpc("0.7", "0.2")})
    assert abs(result.value - mp.exp(mp.mpc("0.7", "0.2"))) < mp.mpf("1e-55")
    assert result.expression_digest == term.digest
    assert result.receipt_root == result.receipts[-1].digest
    assert verify_receipts(result.receipts)


def test_missing_variable_fails_loudly():
    try:
        Expr.var("x").evaluate({"z": 1})
    except KeyError as error:
        assert "x" in str(error)
    else:
        raise AssertionError("missing input was accepted")
