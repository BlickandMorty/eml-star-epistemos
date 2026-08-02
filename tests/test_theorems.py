from pathlib import Path

from eml_toolkit.theorems import THEOREMS, TheoremStatus, theorem


def test_registry_ids_are_unique_and_falsifiable():
    identifiers = [record.identifier for record in THEOREMS]
    assert len(identifiers) == len(set(identifiers))
    assert all(record.falsifier.strip() for record in THEOREMS)


def test_density_claim_remains_open():
    assert theorem("emlstar.density-conditional").status is TheoremStatus.OPEN


def test_structural_lean_file_contains_no_placeholder_proofs():
    source = (Path(__file__).parents[1] / "formal" / "EpistemosEMLStar.lean").read_text(encoding="utf-8")
    lowered = source.lower()
    assert "sorry" not in lowered
    assert "admit" not in lowered
