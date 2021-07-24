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

        self.choiceType = QtWidgets.QComboBox(form)

        self.chained = QtWidgets.QCheckBox(form)
        self.active = QtWidgets.QCheckBox(form)

        self.changeType = QtWidgets.QComboBox(form)
        self.changeButton = QtWidgets.QPushButton(form)

        self.jumpName = QtWidgets.QLineEdit(form)
        self.choiceName = QtWidgets.QLineEdit(form)

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
        form.showFullScreen()
        # Altering the ratios
        self.width_ratio = form.width() / 565
        self.height_ratio = form.height() / 399
        # Creating the widgets
        setup_widget(self.jumpers, self.ratio_alter(10, 10, 75, 14), 'jumpers')

        setup_widget(self.jumps, self.ratio_alter(10, 29, 75, 360.5), 'jumps')
        setup_widget(self.jumpName, self.ratio_alter(170, 29, 125, 14), 'jumpName')
        setup_widget(self.jumpCP, self.ratio_alter(170, 10, 75, 14), 'jumpCP')
        self.jumpCP.setReadOnly(True)

        setup_widget(self.changeType, self.ratio_alter(90, 10, 75, 14), 'changeType')
        setup_widget(self.changeButton, self.ratio_alter(90, 29, 75, 14), 'changeButton')

        setup_widget(self.choices, self.ratio_alter(90, 48, 75, 341.5), 'choices')
        setup_widget(self.choiceName, self.ratio_alter(300, 29, 252, 14), 'choiceName')
        setup_widget(self.choiceCP, self.ratio_alter(477, 10, 75, 14), 'choiceCP')
        setup_widget(self.choiceType, self.ratio_alter(250, 10, 150, 14), 'choiceType')

        setup_widget(self.active, self.ratio_alter(405, 10, 30, 14), 'active')
        setup_widget(self.chained, self.ratio_alter(435, 10, 35, 14), 'chained')

        setup_widget(self.mainInfo, self.ratio_alter(170, 48, 382, 221), 'mainInfo')
        setup_widget(self.secondInfo, self.ratio_alter(170, 274, 382, 115), 'secondInfo')

        self.getJumpers()
        self.getJumps()

        self.changeType.addItems(['Add Jump', 'Add Choice', 'Backup Jump', 'Add Jumper', 'Backup Jumper', 'Rearrange Jumps', 'Delete Choice', 'Delete Jump', 'Delete Jumper', 'Close Application'])
        self.choiceType.addItems(['Origin', 'Perk', 'Item', 'Companion', 'Drawback', 'Scenario', 'Other'])
        # Adding text to others
        self.active.setText("Active")
        self.chained.setText("Chained")
        self.changeButton.setText(self.changeType.currentText())
        # Connecting to the different widgets
        self.jumpers.currentIndexChanged.connect(self.clickedJumper)
        self.jumps.clicked.connect(self.clickedJump)
        self.choices.clicked.connect(self.clickedChoice)

        self.changeType.currentIndexChanged.connect(self.clickedChangeType)
        self.changeButton.clicked.connect(self.clickedChangeButton)

        self.jumpName.textChanged.connect(self.jumpNameChanged)

        self.choiceName.textChanged.connect(self.choiceNameChanged)
        self.choiceType.currentIndexChanged.connect(self.choiceTypeChanged)
        self.choiceCP.textChanged.connect(self.choiceCPChanged)

        self.mainInfo.textChanged.connect(self.mainInfoChanged)
        self.secondInfo.textChanged.connect(self.secondInfoChanged)

        self.active.stateChanged.connect(self.activeChanged)
        self.chained.stateChanged.connect(self.chainedChanged)

    def getJumpers(self):
        self.jumpers.clear()
        self.jumpers.addItems(self.info.jumpers)

    def getJumps(self):
        self.jumps.clear()
        self.jumps.addItems(self.info.jumps)

        for i in range(len(self.jumps)):
            self.jumps.setCurrentRow(i)
            self.jumps.currentItem().setText(self.jumps.currentItem().text()[10:])

    def getChoices(self):
        self.choices.clear()
        self.choices.addItems(name[0] for name in self.info.jumpChoices[1:])

    def clickedJumper(self):
        self.jumps.clear()
        self.info.getJumper(self.jumpers.currentText())
        self.makeLists()

    def clickedJump(self):
        self.info.getJump(self.jumps.currentRow() + 1, self.jumps.currentItem().text())

        self.jumpName.setText(self.jumps.currentItem().text())

        self.getChoices()

    def clickedChoice(self):
        item = self.choices.currentItem().text()
        self.info.getChoice(self.choices.currentRow())

        self.choiceName.setText(item)
        self.choiceCP.setText(self.info.choiceCP)
        self.choiceType.setCurrentIndex(self.info.choiceType)

        self.mainInfo.setPlainText(self.info.choiceDescription)
        self.secondInfo.setPlainText(self.info.choiceNotes)

        self.active.setChecked(self.info.choiceActive)
        self.chained.setChecked(self.info.choiceChained)

    def clickedChangeButton(self):
        text = self.changeType.currentText()
        if text == 'Add Jump':
            self.info.addJump()
            self.getJumps()
        elif text == 'Add Choice':
            self.info.addChoice()
            self.getChoices()
            self.choices.setCurrentRow(len(self.choices) - 1)
            self.clickedChoice()
        elif text == 'Backup Jump':
            self.info.backupJump()
        elif text == 'Add Jumper':
            self.info.addJumper()
        elif text == 'Backup Jumper':
            self.info.backupJumper()
        elif text == 'Delete Jumper' and self.confirm(text):
            self.info.deleteJumper()
        elif text == 'Delete Jump' and self.confirm(text):
            currentRow = self.jumps.currentRow()
            self.info.deleteJump()
            self.getJumps()
            self.jumps.setCurrentRow(currentRow - (1 if currentRow != 0 else 0))
            self.getChoices()
        elif text == 'Delete Choice' and self.confirm(text):
            self.info.deleteChoice(self.choices.currentRow())
            self.getChoices()
        elif text == 'Close Application' and self.confirm(text):
            quit()

    @staticmethod
    def confirm(text):
        check = QtWidgets.QMessageBox
        return check.Yes == check.question(QtWidgets.QWidget(), 'Confirmation Question', 'Are you sure you want to {}?'.format(text.lower()), check.Yes | check.No, check.No)

    def jumpNameChanged(self):
        self.info.renameJump(self.jumpName.text())
        self.jumps.currentItem().setText(self.jumpName.text())

    def choiceNameChanged(self):
        self.info.renameChoice(self.choices.currentRow(), self.choiceName.text())
        self.choices.currentItem().setText(self.choiceName.text())

    def clickedChangeType(self):
        self.changeButton.setText(self.changeType.currentText())

    def mainInfoChanged(self):
        self.info.changeDescription(self.choices.currentRow(), self.mainInfo.toPlainText())

    def secondInfoChanged(self):
        self.info.changeNotes(self.choices.currentRow(), self.secondInfo.toPlainText())

    def choiceCPChanged(self):
        try:
            int(self.choiceCP.text())
            self.info.changeCP(self.choices.currentRow(), self.choiceCP.text())
            self.jumpCP.setText(self.info.jumpCP)
        except Exception:
            self.choiceCP.setText(self.info.choiceCP)

    def choiceTypeChanged(self):
        self.info.changeType(self.choices.currentRow(), self.choiceType.currentIndex())

    def activeChanged(self):
        self.info.changeActive(self.choices.currentRow(), self.active.isChecked())
        self.jumpCP.setText(self.info.jumpCP)

    def chainedChanged(self):
        self.info.changeChained(self.choices.currentRow(), self.chained.isChecked())
