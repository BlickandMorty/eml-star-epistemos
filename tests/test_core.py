import mpmath as mp

from eml_toolkit import core


POINTS = [
    mp.mpc("0.7"),
    mp.mpc("1.3", "0.2"),
    mp.mpc("2.1", "-0.4"),
]


def assert_close(actual, expected, tolerance="1e-48"):
    assert abs(actual - expected) < mp.mpf(tolerance)


def test_public_derived_arithmetic_uses_real_package():
    for left, right in zip(POINTS, reversed(POINTS)):
        assert_close(core.eml_add(left, right), left + right)
        assert_close(core.eml_sub(left, right), left - right)
        assert_close(core.eml_mul(left, right), left * right)
    for point in POINTS:
        assert_close(core.eml_neg(point), -point)
        assert_close(core.eml_inv(point), 1 / point)


def test_conjugate_observables_in_principal_strip():
    for point in POINTS:
        assert_close(core.conjugate_formula(point), mp.conj(point))
        assert_close(core.real_part(point), mp.re(point))
        assert_close(core.imag_part(point), mp.im(point))
        assert_close(core.modulus_squared(point), abs(point) ** 2)


def test_fold_to_strip_is_half_open_and_periodic():
    for imaginary in (-20, -4, -mp.pi, 0, mp.pi, 4, 20):
        folded = core.fold_to_strip(mp.mpc(2, imaginary))
        assert -mp.pi <= mp.im(folded) < mp.pi
        turns = (imaginary - mp.im(folded)) / (2 * mp.pi)
        assert abs(turns - mp.nint(turns)) < mp.mpf("1e-48")
