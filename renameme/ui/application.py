import logging
import os.path
from dataclasses import dataclass, replace

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar, QProgressBar

from guibedos6 import css, error_reported

from renameme import api

from .central_widget import CentralWidget


_WINDOW_TITLE = "Rename me"
_ICON_FILENAME = "icon.png"

_logger = logging.getLogger(__name__)
_RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


@dataclass
class ApplicationOptions:
    """Options for the application"""
    show_css_editor: bool = False


class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        QMainWindow.__init__(self, parent)
        self._app = app

    def closeEvent(self, event):
        if self._app.confirm_exit():
            event.accept()
        else:
            event.ignore()


class Application(QObject):
    beforeExec = Signal()

    def __init__(self, options: ApplicationOptions, parent=None):
        QObject.__init__(self, parent)

        self._options = options

        self._q_application = QApplication()

        self._progress_bar = QProgressBar()
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setVisible(False)
        status_bar = QStatusBar()
        status_bar.addPermanentWidget(self._progress_bar)

        self._main_window = MainWindow(app=self)
        self._main_window.resize(1200, 800)
        self._main_window.setWindowTitle(_WINDOW_TITLE)
        self._main_window.setStatusBar(status_bar)

        self._central_widget = CentralWidget(app=self)
        self._main_window.setCentralWidget(self._central_widget)

        self.beforeExec.connect(self._initialize)

    def exec(self):
        self._main_window.show()
        # Initialization must happen in Qt's main loop to ensure proper error reporting to the user
        self.beforeExec.emit()
        return self._q_application.exec()

    def set_status_message(self, message, progress=None):
        if progress is not None:
            self._progress_bar.setVisible(True)
            self._progress_bar.setValue(progress)
        else:
            self._progress_bar.setVisible(False)

        self._main_window.statusBar().showMessage(message)
        QApplication.processEvents()

    #
    # Initialization / Exit
    @error_reported("Initialization", exit_on_error=True)
    def _initialize(self):
        self._load_settings()
        self._init_css()
        self._main_window.setWindowIcon(QIcon(os.path.join(_RESOURCES, _ICON_FILENAME)))

    def _load_settings(self):
        settings = api.settings.load()
        self._options = replace(self._options, **settings)

    def _init_css(self):
        if self._options.show_css_editor:
            _logger.info("Loading CSS Editor")
            from guibedos6.css.editor import CSSEditor
            self.css_editor = CSSEditor('Xilam')
        else:
            _logger.info("Loading CSS theme")
            css_theme_library = css.ThemeLibrary(_RESOURCES)
            css_theme_library.apply('theme-dark')

    @error_reported("Save preferences on exit")
    def confirm_exit(self):
        """Returns True if it is Ok to exit
        (usually called on main window's close Event)"""
        return True
