from src.evaluation_summary import compute_accuracy

def test_compute_accuracy_range():
    acc = compute_accuracy(wer=10, cer=5)
    assert 70 <= acc <= 100

def test_compute_accuracy_high_error():
    acc = compute_accuracy(wer=90, cer=80)
    assert acc == 70
