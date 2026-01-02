from src.logger import get_logger

def test_logger_creation():
    logger = get_logger("TEST", "test.log")
    assert logger is not None
