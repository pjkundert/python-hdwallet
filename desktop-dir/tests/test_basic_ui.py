import pytest

from PySide6.QtCore import Qt

from desktop.main import MainApplication

@pytest.fixture
def app(qtbot):
    test_app = MainApplication()
    qtbot.addWidget(test_app.app)
    return test_app

def test_dump_generate_button(app, qtbot):
    qtbot.mouseClick(app.ui.generateQPushButton, Qt.LeftButton)
    assert app.ui.hdwalletQStackedWidget.currentWidget() == app.ui.generatePageQStackedWidget

    qtbot.mouseClick(app.ui.dumpQPushButton, Qt.LeftButton)
    assert app.ui.hdwalletQStackedWidget.currentWidget() == app.ui.dumpsPageQStackedWidget

def test_terminal_output(app, qtbot):
    app.app.println("test")
    assert app.ui.outputTerminalQPlainTextEdit.toPlainText() == 'test'

    app.app.println("test")
    assert app.ui.outputTerminalQPlainTextEdit.toPlainText() == 'test\ntest'

    qtbot.mouseClick(app.ui.clearTerminalQPushButton, Qt.LeftButton)
    assert app.ui.outputTerminalQPlainTextEdit.toPlainText() == ''