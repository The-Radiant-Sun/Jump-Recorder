from PyQt5 import QtCore, QtWidgets
from Info import Info


class UiForm(object):
    def __init__(self, form):
        self.info = Info()
        """Establish self variables and ratios"""
        # Forming initial ratios
        self.width_ratio = 1
        self.height_ratio = 1
        self.memory = {}
        # Establishing base widgets
        self.jumpers = QtWidgets.QComboBox(form)

        self.mainInfo = QtWidgets.QPlainTextEdit(form)
        self.secondInfo = QtWidgets.QPlainTextEdit(form)

        self.jumps = QtWidgets.QListWidget(form)
        self.choices = QtWidgets.QListWidget(form)

        self.jumpCP = QtWidgets.QLineEdit(form)
        self.choiceCP = QtWidgets.QLineEdit(form)

        self.displayType = QtWidgets.QComboBox(form)

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

        setup_widget(self.jumps, self.ratio_alter(10, 48, 75, 341.5), 'jumps')
        setup_widget(self.jumpName, self.ratio_alter(170, 29, 100, 14), 'jumpName')
        setup_widget(self.jumpCP, self.ratio_alter(170, 10, 75, 14), 'jumpCP')
        self.jumpCP.setReadOnly(True)

        setup_widget(self.displayType, self.ratio_alter(10, 29, 75, 14), 'displayType')

        setup_widget(self.changeType, self.ratio_alter(90, 10, 75, 14), 'changeType')
        setup_widget(self.changeButton, self.ratio_alter(90, 29, 75, 14), 'changeButton')

        setup_widget(self.choices, self.ratio_alter(90, 48, 75, 341.5), 'choices')
        setup_widget(self.choiceName, self.ratio_alter(275, 29, 277, 14), 'choiceName')
        setup_widget(self.choiceCP, self.ratio_alter(477, 10, 75, 14), 'choiceCP')
        setup_widget(self.choiceType, self.ratio_alter(250, 10, 150, 14), 'choiceType')

        setup_widget(self.active, self.ratio_alter(405, 10, 30, 14), 'active')
        setup_widget(self.chained, self.ratio_alter(435, 10, 35, 14), 'chained')

        setup_widget(self.mainInfo, self.ratio_alter(170, 48, 382, 251), 'mainInfo')
        setup_widget(self.secondInfo, self.ratio_alter(170, 304, 382, 85), 'secondInfo')

        self.getJumpers()
        self.getJumps()

        self.displayType.addItems(['Display All', 'Display Active', 'Display Chained'])

        self.changeType.addItems([
            'Add Jump', 'Add Choice', 'Rearrange Choices',
            'Backup Jump', 'Import Jump', 'Rearrange Jumps',
            'Add Jumper', 'Backup Jumper', 'Rename Jumper',
            'Delete Choice', 'Delete Jump', 'Delete Jumper',
            'Close Application'
        ])

        self.choiceType.addItems(['Origin', 'Perk', 'Item', 'Companion', 'Drawback', 'Scenario', 'Other'])
        # Adding text to others
        self.active.setText("Active")
        self.chained.setText("Chained")
        self.changeButton.setText(self.changeType.currentText())
        # Connecting to the different widgets
        self.jumpers.currentIndexChanged.connect(self.clickedJumper)
        self.jumps.clicked.connect(self.clickedJump)
        self.choices.clicked.connect(self.clickedChoice)

        self.displayType.currentIndexChanged.connect(self.clickedDisplayType)

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
        # Grabbing initial values
        self.clickedJump()
        self.choices.setCurrentRow(0)
        self.clickedChoice()


    def getJumpers(self):
        self.jumpers.clear()
        self.jumpers.addItems(self.info.jumpers)

    def getJumps(self):
        self.jumps.clear()
        self.jumps.addItems(self.info.jumps)

        for i in range(len(self.jumps)):
            self.jumps.setCurrentRow(i)
            self.jumps.currentItem().setText(self.jumps.currentItem().text().split('__')[1])

        self.jumps.setCurrentRow(0)
        self.clickedJump()

    def getChoices(self):
        self.choices.clear()
        if self.displayType.currentIndex() == 0:
            self.choices.addItems(name[0] for name in self.info.jumpChoices[1:])
        elif self.displayType.currentIndex() == 1:
            for i in range(len(self.info.jumpChoices[1:])):
                self.info.getChoice(i)
                if self.info.choiceActive:
                    self.choices.addItem(self.info.jumpChoices[1:][i][0])
                    self.memory[len(self.memory)] = i
        else:
            for i in range(len(self.info.jumpChoices[1:])):
                self.info.getChoice(i)
                if self.info.choiceChained:
                    self.choices.addItem(self.info.jumpChoices[1:][i][0])
                    self.memory[len(self.memory)] = i

    def clickedJumper(self):
        if len(self.jumpers) != 0:
            self.jumps.clear()
            self.info.getJumper(self.jumpers.currentText())
            self.getJumps()
            self.jumps.setCurrentRow(0)
            self.clickedJump()

    def clickedJump(self):
        self.info.getJump(self.jumps.currentRow() + 1, self.jumps.currentItem().text())
        self.jumpName.setText(self.jumps.currentItem().text())
        self.getChoices()
        self.choices.setCurrentRow(0)
        self.clickedChoice()
        self.jumpCP.setText(self.info.jumpCP)

    def clickedChoice(self):
        item = self.choices.currentItem().text()

        if self.displayType == 0:
            self.info.getChoice(self.choices.currentRow())
        else:
            self.info.getChoice(self.memory[self.choices.currentRow()])

        self.choiceName.setText(item)
        self.choiceCP.setText(self.info.choiceCP[:-1])
        self.choiceCPChanged()
        self.choiceType.setCurrentIndex(self.info.choiceType)

        self.mainInfo.setPlainText(self.info.choiceDescription.replace('%%', '\n'))
        self.secondInfo.setPlainText(self.info.choiceNotes.replace('%%', '\n'))

        self.active.setChecked(self.info.choiceActive)
        self.chained.setChecked(self.info.choiceChained)

    def clickedChangeButton(self):
        text = self.changeType.currentText()

        if text == 'Add Jump':
            self.info.addJump()
            self.getJumps()
            self.jumps.setCurrentRow(len(self.jumps) - 1)
            self.clickedJump()

        elif text == 'Add Choice':
            self.info.addChoice()
            self.getChoices()
            self.choices.setCurrentRow(len(self.choices) - 1)
            self.clickedChoice()
            self.active.setChecked(False)
            self.chained.setChecked(False if self.choiceType.currentText() != 'Perk' and self.choiceType.currentText() != 'Item' else True)
            self.choiceCP.setText('0')

        elif text == 'Rearrange Choices':
            newPos = QtWidgets.QInputDialog.getItem(QtWidgets.QWidget(), 'Rearrange Choices', 'Move current choice to:', ["{} - {}".format(i + 1, choice[0]) for i, choice in enumerate(self.info.jumpChoices[1:])], 0, False)
            if newPos[1]:
                self.info.moveChoice(int(newPos[0].split(' - ')[0]), self.choices.currentRow() + 1)
                self.clickedJump()
                self.choices.setCurrentRow(int(newPos[0].split(' - ')[0]) - 1)
                self.clickedChoice()

        elif text == 'Backup Jump':
            self.info.backupJump(False)

        elif text == 'Import Jump' and len(self.info.backups) != 0:
            newJump = QtWidgets.QInputDialog.getItem(QtWidgets.QWidget(), 'Import Jump', 'Import Jump:', [backup[:-4] for backup in self.info.backups], 0, False)
            if newJump[1]:
                newJump = self.info.importJump(newJump[0])
                if newJump:
                    self.getJumps()
                    self.jumps.setCurrentRow(len(self.jumps))

        elif text == 'Rearrange Jumps':
            newPos = QtWidgets.QInputDialog.getItem(QtWidgets.QWidget(), 'Rearrange Current Jump', 'Move current jump to:', ["{} - {}".format(str(int(jump.split('__')[0])), jump.split("__")[1]) for jump in self.info.jumps], 0, False)
            if newPos[1]:
                self.info.moveJump(self.jumps.currentRow() + 1, int(newPos[0].split(' - ')[0]))
                self.getJumps()
                self.jumps.setCurrentRow(int(newPos[0].split(' - ')[0]))
                self.clickedJump()

        elif text == 'Add Jumper':
            newJumper = self.info.addJumper(QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), 'Add Jumper', 'Name of new Jumper:'))
            if newJumper == False:
                QtWidgets.QMessageBox.warning(QtWidgets.QWidget(), 'Jumper Name Error', 'Change new Jumper Name', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            else:
                self.getJumpers()
                self.jumpers.setCurrentIndex(self.info.jumpers.index(newJumper))
                self.clickedJumper()

        elif text == 'Backup Jumper':
            self.info.backupJumper()

        elif text == 'Rename Jumper':
            newName = self.info.renameJumper(QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), 'Add Jumper', 'Name of new Jumper:'))
            if not newName[0]:
                QtWidgets.QMessageBox.warning(QtWidgets.QWidget(), 'Jumper Name Error', 'Change Jumper Name', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            else:
                self.getJumpers()
                self.jumpers.setCurrentIndex(self.info.jumpers.index(newName[1]))
                self.clickedJumper()

        elif text == 'Delete Jumper' and self.confirm(text) and len(self.jumpers) != 0:
            self.info.deleteJumper()
            self.getJumpers()
            self.jumpers.setCurrentIndex(0)

        elif text == 'Delete Jump' and len(self.jumps) > 1 and self.confirm(text):
            currentRow = self.jumps.currentRow()
            self.info.deleteJump()
            self.getJumps()
            self.jumps.setCurrentRow(currentRow if currentRow < len(self.jumps) else len(self.jumps) - 1)
            self.clickedJump()

        elif text == 'Delete Choice' and self.confirm(text):
            self.info.deleteChoice(self.choices.currentRow())
            self.getChoices()

        elif text == 'Close Application' and self.confirm(text):
            quit()

    def setEditable(self, tf):
        tf = not tf
        self.mainInfo.setReadOnly(tf)
        self.secondInfo.setReadOnly(tf)
        self.choiceType.setDisabled(tf)
        self.chained.setDisabled(tf)
        self.active.setDisabled(tf)
        self.choiceCP.setReadOnly(tf)
        self.jumpName.setReadOnly(tf)
        self.choiceName.setReadOnly(tf)
        self.changeType.setDisabled(tf)
        self.changeButton.setDisabled(tf)

    @staticmethod
    def confirm(text):
        check = QtWidgets.QMessageBox
        return check.Yes == check.question(QtWidgets.QWidget(), 'Confirmation Question', 'Are you sure you want to {}?'.format(text.lower()), check.Yes | check.No, check.No)

    def clickedDisplayType(self):
        index = self.displayType.currentIndex()
        self.memory = {}
        if index == 0:
            self.setEditable(True)
        else:
            self.setEditable(False)
        self.getChoices()

    def jumpNameChanged(self):
        index = self.choices.currentRow()
        self.info.renameJump(self.jumpName.text())
        self.jumps.currentItem().setText(self.jumpName.text())
        self.getChoices()
        self.choices.setCurrentRow(index)

    def choiceNameChanged(self):
        self.info.renameChoice(self.choices.currentRow(), self.choiceName.text())
        self.choices.currentItem().setText(self.choiceName.text())

    def clickedChangeType(self):
        self.changeButton.setText(self.changeType.currentText())

    def mainInfoChanged(self):
        try:
            self.info.changeDescription(self.choices.currentRow(), self.mainInfo.toPlainText().replace('\n', '%%'))
        except Exception:
            self.mainInfo.setPlainText(self.info.choiceDescription)

    def secondInfoChanged(self):
        self.info.changeNotes(self.choices.currentRow(), self.secondInfo.toPlainText().replace('\n', '%%'))

    def choiceCPChanged(self):
        try:
            int(self.choiceCP.text() + '0')
            self.info.changeCP(self.choices.currentRow(), self.choiceCP.text() + '0')
            self.jumpCP.setText(self.info.jumpCP)
        except Exception:
            self.choiceCP.setText(self.info.choiceCP[:-1])

    def choiceTypeChanged(self):
        self.info.changeType(self.choices.currentRow(), self.choiceType.currentIndex())

    def activeChanged(self):
        self.info.changeActive(self.choices.currentRow(), self.active.isChecked())
        self.jumpCP.setText(self.info.jumpCP)

    def chainedChanged(self):
        self.info.changeChained(self.choices.currentRow(), self.chained.isChecked())
