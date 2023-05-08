import logging
import pytest
from unittest.mock import patch
from gcp_logger import GCPLogStrategy


@pytest.fixture(scope='module')
def gcp_strategy():
    return GCPLogStrategy()


def test_info(gcp_strategy, caplog):
    with caplog.at_level(logging.INFO, logger='TestGCPLogStrategy'):
        with patch.object(gcp_strategy, 'logger', logging.getLogger('TestGCPLogStrategy')):
            gcp_strategy.info('Test info message')
    assert 'Test info message' in caplog.text


def test_debug(gcp_strategy, caplog):
    with caplog.at_level(logging.DEBUG, logger='TestGCPLogStrategy'):
        with patch.object(gcp_strategy, 'logger', logging.getLogger('TestGCPLogStrategy')):
            gcp_strategy.debug('Test debug message')
    assert 'Test debug message' in caplog.text


def test_warning(gcp_strategy, caplog):
    with caplog.at_level(logging.WARNING, logger='TestGCPLogStrategy'):
        with patch.object(gcp_strategy, 'logger', logging.getLogger('TestGCPLogStrategy')):
            gcp_strategy.warning('Test warning message')
    assert 'Test warning message' in caplog.text


def test_error(gcp_strategy, caplog):
    with caplog.at_level(logging.ERROR, logger='TestGCPLogStrategy'):
        with patch.object(gcp_strategy, 'logger', logging.getLogger('TestGCPLogStrategy')):
            gcp_strategy.error('Test error message')
    assert 'Test error message' in caplog.text


def test_critical(gcp_strategy, caplog):
    with caplog.at_level(logging.CRITICAL, logger='TestGCPLogStrategy'):
        with patch.object(gcp_strategy, 'logger', logging.getLogger('TestGCPLogStrategy')):
            gcp_strategy.critical('Test critical message')
    assert 'Test critical message' in caplog.text