from GUI import UiForm

from PyQt5 import QtWidgets
import sys


class RunApplication:
    def __init__(self):
        """Run UI"""
        app = QtWidgets.QApplication(sys.argv)
        form = QtWidgets.QWidget()
        ui = UiForm(form)
        ui.setup_ui(form)
        form.show()
        sys.exit(app.exec_())


RunApplication()
