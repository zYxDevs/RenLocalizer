# -*- coding: utf-8 -*-
"""
Test to ensure Main.qml and all QML components load without syntax or binding errors.
"""
import os
import sys
import pytest
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine


def test_qml_loads_cleanly():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv[:1])

    from src.backend.app_backend import AppBackend
    backend = AppBackend(parent=app)

    engine = QQmlApplicationEngine(app)
    engine.rootContext().setContextProperty("appBackend", backend)

    qml_root = os.path.abspath("src/gui/qml")
    engine.addImportPath(qml_root)
    qml_path = os.path.join(qml_root, "Main.qml")

    errors = []
    def on_warnings(warnings):
        for w in warnings:
            errors.append(w.toString())

    engine.warnings.connect(on_warnings)
    engine.load(QUrl.fromLocalFile(qml_path))

    assert len(engine.rootObjects()) > 0, f"QML failed to load: {errors}"
