"""Numerical reference semantics for EML and EML-star.

The derived arithmetic programs are identities only where every principal-log
branch used by the program is valid.  This module deliberately exposes the
small primitives as well as the derived programs so callers can attach branch
evidence instead of treating floating-point agreement as a proof.
"""

from __future__ import annotations

import mpmath as mp

mp.mp.dps = 60

ONE = mp.mpc(1)
ZERO = mp.mpc(0)


def eml(x: complex, y: complex):
    """Return ``exp(x) - log(y)`` using the principal complex logarithm."""
    return mp.exp(x) - mp.log(y)


def eml_star(x: complex, y: complex):
    """Return ``exp(x) - log(conj(y))`` on the principal branch."""
    return mp.exp(x) - mp.log(mp.conj(y))


def eml_exp(z: complex):
    return eml(z, ONE)


def eml_ln(z: complex):
    return eml(ONE, eml(eml(ONE, z), ONE))


def eml_zero():
    return eml(ONE, eml(eml(ONE, ONE), ONE))


def eml_neg(z: complex):
    return eml(eml(ONE, eml(eml(ONE, eml_zero()), ONE)), eml(z, ONE))


def eml_sub(a: complex, b: complex):
    return eml(eml_ln(a), eml_exp(b))


def eml_add(a: complex, b: complex):
    return eml_sub(a, eml_neg(b))


def eml_inv(z: complex):
    return eml_exp(eml_neg(eml_ln(z)))


def eml_mul(a: complex, b: complex):
    return eml_exp(eml_add(eml_ln(a), eml_ln(b)))


def conjugate_formula(z: complex):
    """The depth-two EML-star conjugation formula.

    It equals ``conj(z)`` on the theorem's principal strip and otherwise
    returns a representative differing by an integer multiple of ``2*pi*i``.
    """
    return ONE - eml_star(ZERO, eml(z, ONE))


def fold_to_strip(z: complex):
    """Fold the imaginary component into the half-open interval [-pi, pi)."""
    value = mp.mpc(z)
    period = 2 * mp.pi
    folded_im = mp.im(value) - period * mp.floor((mp.im(value) + mp.pi) / period)
    return mp.mpc(mp.re(value), folded_im)


def real_part(z: complex):
    return (z + conjugate_formula(z)) / 2


def imag_part(z: complex):
    return (z - conjugate_formula(z)) / (2 * mp.j)


def modulus_squared(z: complex):
    return z * conjugate_formula(z)


def modulus(z: complex):
    return mp.sqrt(modulus_squared(z))


def alt_conjugate(z: complex):
    """Unconditional conjugation when ``Re`` is admitted as a primitive."""
    return 2 * mp.re(z) - z


def alt_modulus_squared(z: complex):
    return mp.re(z) ** 2 + mp.im(z) ** 2


# Backwards-compatible names used by the original scripts.
E_neg = eml_neg
E_sub = eml_sub
E_add = eml_add
E_mul = eml_mul
E_conj = conjugate_formula

__all__ = [
    "ONE", "ZERO", "eml", "eml_star", "eml_exp", "eml_ln",
    "eml_zero", "eml_neg", "eml_sub", "eml_add", "eml_inv",
    "eml_mul", "conjugate_formula", "fold_to_strip", "real_part",
    "imag_part", "modulus_squared", "modulus", "alt_conjugate",
    "alt_modulus_squared", "E_neg", "E_sub", "E_add", "E_mul",
    "E_conj",
]
