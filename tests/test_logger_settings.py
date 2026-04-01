import logging

from src.infrastructure.settings import logger as logger_module


def test_resolve_log_level_default_y_fallback(monkeypatch):
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    assert logger_module._resolve_log_level() == logging.INFO

    monkeypatch.setenv("LOG_LEVEL", "nivel_invalido")
    assert logger_module._resolve_log_level() == logging.INFO


def test_configure_logging_con_handlers_existentes(monkeypatch):
    root_logger = logging.getLogger()
    original_handlers = list(root_logger.handlers)
    original_level = root_logger.level
    try:
        root_logger.handlers[:] = [logging.NullHandler()]
        logger_module.configure_logging()
        assert len(root_logger.handlers) == 1
    finally:
        root_logger.handlers[:] = original_handlers
        root_logger.setLevel(original_level)


def test_configure_logging_sin_handlers_invoca_basicconfig(monkeypatch):
    root_logger = logging.getLogger()
    original_handlers = list(root_logger.handlers)
    original_level = root_logger.level
    called = {}

    def fake_basic_config(**kwargs):
        called.update(kwargs)
        root_logger.handlers[:] = [logging.NullHandler()]

    try:
        root_logger.handlers[:] = []
        monkeypatch.setattr(logger_module.logging, "basicConfig", fake_basic_config)
        logger_module.configure_logging()
        assert called["format"] == logger_module._DEFAULT_LOG_FORMAT
        assert called["level"] == logging.INFO
    finally:
        root_logger.handlers[:] = original_handlers
        root_logger.setLevel(original_level)
