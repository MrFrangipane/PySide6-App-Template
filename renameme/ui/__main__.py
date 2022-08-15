import logging

from renameme.ui.application import Application, ApplicationOptions


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    options = ApplicationOptions()

    application = Application(options)
    application.exec()
