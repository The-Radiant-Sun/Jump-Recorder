# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CypherPlaygroundGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from Info import Info


class UiForm(object):
    def __init__(self, form):
        self.info = Info()
        """Establish self variables and ratios"""
        # Forming initial ratios
        self.width_ratio = 1
        self.height_ratio = 1
        # Establishing base widgets
        self.jumpers = QtWidgets.QComboBox(form)
        self.mainInfo = QtWidgets.QPlainTextEdit(form)
        self.secondInfo = QtWidgets.QPlainTextEdit(form)
        self.jumps = QtWidgets.QListWidget(form)
        self.choices = QtWidgets.QListWidget(form)
        self.jumpCP = QtWidgets.QLineEdit(form)
        self.choiceCP = QtWidgets.QLineEdit(form)
        self.chained = QtWidgets.QCheckBox(form)
        self.active = QtWidgets.QCheckBox(form)

    def ratio_alter(self, x, y, width, height):
        """Return coordinates and dimensions altered by the form size"""
        alter_x = self.width_ratio * x
        alter_y = self.height_ratio * y
        alter_width = self.width_ratio * width
        alter_height = self.height_ratio * height
        return QtCore.QRect(alter_x, alter_y, alter_width, alter_height)

    def setup_ui(self, form):
        """Establish GUI components, specialities and connections"""
        def setup_widget(self_name, geometry, name):
            """Call functions based on self_name, geometry and name"""
            self_name.setGeometry(geometry)
            self_name.setObjectName(name)
        # Creating the form
        form.setObjectName("Form")
        form.resize(1000, 750)
        # Altering the ratios
        self.width_ratio = form.width() / 565
        self.height_ratio = form.height() / 399
        # Creating the widgets
        setup_widget(self.jumpers, self.ratio_alter(20, 10, 75, 14), 'jumpers')
        setup_widget(self.jumps, self.ratio_alter(20, 34, 75, 340), 'jumps')
        setup_widget(self.choices, self.ratio_alter(100, 34, 75, 340), 'choices')
        setup_widget(self.jumpCP, self.ratio_alter(100, 10, 75, 14), 'jumpCP')
        setup_widget(self.choiceCP, self.ratio_alter(477, 10, 75, 14), 'choiceCP')
        setup_widget(self.chained, self.ratio_alter(180, 10, 75, 14), 'chained')
        setup_widget(self.active, self.ratio_alter(220, 10, 75, 14), 'active')
        setup_widget(self.mainInfo, self.ratio_alter(180, 34, 372, 240), 'mainInfo')
        setup_widget(self.secondInfo, self.ratio_alter(180, 284, 372, 90), 'secondInfo')
        # Adding text to lists
        self.jumpers.addItems(self.info.jumpers)
        self.jumps.addItems(self.info.jumps)
        # Adding text to checkboxes
        self.chained.setText("Chained")
        self.active.setText("Active")

        self.jumpers.currentIndexChanged.connect(self.clickedJumper)
        self.jumps.clicked.connect(self.clickedJump)

    def clickedJumper(self):
        self.jumps.clear()
        self.info.getJumper(self.jumpers.currentText())
        self.jumps.addItems(self.info.jumps)

    def clickedJump(self):
        item = self.jumps.currentItem()
        jump = self.info.getJump(item.text())
