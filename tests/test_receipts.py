from dataclasses import replace

from eml_toolkit.receipts import ReceiptChain, verify_receipts


def test_same_inputs_produce_same_chain():
    left = ReceiptChain()
    right = ReceiptChain()
    for chain in (left, right):
        chain.append("input", {"z": ["1", "2"]})
        chain.append("result", {"value": ["3", "4"]})
    assert left.receipts == right.receipts
    assert left.root == right.root


def test_tampering_breaks_replay():
    chain = ReceiptChain()
    chain.append("input", {"z": ["1", "2"]})
    receipts = list(chain.receipts)
    receipts[0] = replace(receipts[0], payload={"z": ["9", "9"]})
    assert not verify_receipts(receipts)
