#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Abenezer Lulseged Wube <itsm3abena@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import pytest
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit, QSpacerItem, QHBoxLayout, QVBoxLayout, QFrame

from desktop.ui.ui_hdwallet import Ui_MainWindow
from desktop.ui.ui_donations import Ui_Form


@pytest.fixture
def qt_app(request):
    """
    Pytest fixture to create a QApplication instance for testing names of Qt widgets.

    :param request: The pytest request object to manage application lifecycle.

    :return: The application instance.
    """

    app = QApplication([])
    request.addfinalizer(lambda: app.exit())
    return app


def get_widgets(ui):
    """
    Retrieves all relevant widgets from the given UI instance.

    :param ui: The UI instance from which to retrieve widgets.

    :return: A list of QWidget objects contained within the UI.
    """

    widgets = [obj for obj in ui.__dict__.values() if isinstance(obj, (QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame))]
    return widgets


def has_default_designer_name(widget):
    """
    Checks if a widget has a default name typically assigned by Qt Designer.

    :param widget: The widget to check.

    :return: True if the widget's name is a default name, False otherwise.
    """

    default_names = [
        'widget', 'pushButton', 'label', 'lineEdit', 'horizontalLayout', 'verticalLayout', 'frame', 'spacer'
    ]
    for default_name in default_names:
        if widget.objectName().startswith(default_name):
            return True
    return False


def test_default_widget_object_names(qt_app):
    """
    Tests that all widgets in the UI do not use default names set by Qt Designer.

    :param qt_app: The QApplication instance created by the qt_app fixture.

    :raises AssertionError: If a widget's object name is a default name.
    """

    def test_ui(ui_class):
        main_window = QWidget()
        ui_instance = ui_class()
        ui_instance.setupUi(main_window)

        widgets = get_widgets(ui_instance)

        for widget in widgets:
            assert not has_default_designer_name(widget)
            print(f"Object name for {type(widget).__name__}: {widget.objectName()}")

    test_ui(Ui_MainWindow)
    test_ui(Ui_Form)

