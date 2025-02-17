import logging

import qdarktheme
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QActionGroup,
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSplitter,
)

from app.about_dialog import AboutDialog
from app.icons import get_icon
from app.settings import Settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Sanity")
        self.resize(600, 400)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.setWindowIcon(get_icon("logo_32x32.png"))

        self.settings = Settings()
        self.settings.load()

        preferences_menu = QMenu("&Preferences", self)
        theme_action_group = QActionGroup(self)
        theme_action_group.setExclusive(True)

        light_theme_action = theme_action_group.addAction("light")
        dark_theme_action = theme_action_group.addAction("dark")
        assert light_theme_action is not None
        assert dark_theme_action is not None
        light_theme_action.setCheckable(True)
        dark_theme_action.setCheckable(True)
        preferences_menu.addAction(light_theme_action)
        preferences_menu.addAction(dark_theme_action)
        dark_theme_action.triggered.connect(lambda: self._change_theme("dark"))
        light_theme_action.triggered.connect(lambda: self._change_theme("light"))

        if self.settings.theme == "dark":
            dark_theme_action.setChecked(True)
            self._change_theme("dark")
        else:  # Default to light theme
            light_theme_action.setChecked(True)
            self._change_theme("light")

        file_menu = QMenu("&File", self)
        file_menu.addMenu(preferences_menu)
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.close)

        help_menu = QMenu("&Help", self)
        help_menu.addAction("&About", self._show_about)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(help_menu)
        self.setMenuBar(menu_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setSizes([200, 400])

        self.setCentralWidget(splitter)

    def _show_about(self):
        """Show the about dialog."""
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def _change_theme(self, theme: str):
        """Change the application theme."""
        stylesheet = qdarktheme.load_stylesheet(theme)
        application = QApplication.instance()
        assert isinstance(application, QApplication)
        application.setStyleSheet(stylesheet)
        self.settings.set_theme(theme)
