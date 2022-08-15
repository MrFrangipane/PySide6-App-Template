import logging

from renameme.ui.application import Application, ApplicationOptions


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    options = ApplicationOptions()
    options.show_css_editor = False

    application = Application(options)
    application.exec()
