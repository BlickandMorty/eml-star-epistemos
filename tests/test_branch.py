import mpmath as mp

from eml_toolkit.branch import witness_conjugation


def test_in_strip_witness_needs_no_correction():
    witness = witness_conjugation(mp.mpc("1.2", "0.8"))
    assert witness.branch_index == 0
    assert witness.verified


def test_out_of_strip_witness_records_integer_jump():
    witness = witness_conjugation(mp.mpc("1.2", "20"))
    assert witness.branch_index != 0
    assert witness.verified
    assert len(witness.receipt_root) == 64


def test_witness_is_deterministic_at_fixed_precision():
    left = witness_conjugation(mp.mpc("-0.4", "9.1"))
    right = witness_conjugation(mp.mpc("-0.4", "9.1"))
    assert left == right
