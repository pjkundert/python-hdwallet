import pytest
from unittest.mock import patch, MagicMock

from PySide6.QtCore import Qt

from desktop.main import MainApplication

@pytest.fixture
def app(qtbot):
    test_app = MainApplication()
    qtbot.addWidget(test_app.app)
    return test_app

def test_generate_entropy(app, qtbot):
    qtbot.mouseClick(app.ui.generateEntropyClientAndStrengthQPushButton, Qt.LeftButton)
            
def test_generate_mnemonic(app, qtbot):
    pass

def test_generate_seed(app, qtbot):
    pass

def test_generate_passphrase(app, qtbot):
    pass