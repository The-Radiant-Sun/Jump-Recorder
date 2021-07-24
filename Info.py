import os

FileOrder = ['Name', 'Type', 'CP Change', 'Active', 'Chained', 'Description', 'Notes']
EmptyFileOrder = ['', '', '', '', '', '', '', '']

FileTree = ['Info/Jumpers', 'Info/Backup/Jumpers', 'Info/Backup/Jumps']


class Info:
    def __init__(self):
        self.path = 'Info/Jumpers'

        for tree in FileTree:
            if not os.path.exists(tree):
                os.makedirs(tree)

        self.jumpers = os.listdir(self.path)

        self.jumperPath = self.pathConnect(self.path, self.jumpers[0])

        self.jumps = self.remove(os.listdir(self.jumperPath), 4)

        self.jump = self.jumperPath

        self.file = None

        self.jumpChoices = None
        self.jumpCP = None

        self.choiceType = 'Unknown'
        self.choiceCP = 'Unknown'
        self.choiceActive = False
        self.choiceChained = False
        self.choiceDescription = 'Unknown'
        self.choiceNotes = 'Unknown'

    @staticmethod
    def remove(group, digits):
        for unit in group:
            group[group.index(unit)] = unit[:-digits]
        return group

    @staticmethod
    def pathConnect(branch, subBranch):
        return branch + '/' + subBranch

    def getLength(self, length):
        if len(length) < 8:
            length = self.getLength('0' + length)
        return length

    def getJumper(self, jumper):
        self.jumperPath = self.pathConnect(self.path, jumper)
        self.jumps = os.listdir(self.jumperPath)
        self.remove(self.jumps, 4)

    def deleteJumper(self):
        os.rmdir(self.jumperPath)

    def addJump(self):
        try:
            self.jump = self.pathConnect(self.jumperPath, '{}__New Jump.csv'.format(self.getLength(str(len(self.jumps) + 1))))
            self.file = open(self.jump, mode='x')
            self.file.write("Name,,Type,,CP Change,,Active,,Chained,,Description,,Notes\nStarting CP,,6,,1000,,True,,False,,,,")
            self.jumps = self.remove(os.listdir(self.jumperPath), 4)
        except FileExistsError:
            "Do Nothing"

    def getJump(self, row, jump):
        self.jump = self.pathConnect(self.jumperPath, "{}__{}.csv".format(self.getLength(str(row)), jump))
        self.getJumpChoices()

    def deleteJump(self):
        try:
            self.file.close()
            os.remove(self.jump)
        except FileNotFoundError:
            "Do nothing"

    def getJumpChoices(self):
        try:
            self.file = open(self.jump, mode='r')
            self.jumpChoices = self.file.readlines()
            for i, option in enumerate(self.jumpChoices):
                if option != self.jumpChoices[-1]:
                    self.jumpChoices[i] = option[:-1].split(',,')
                else:
                    self.jumpChoices[i] = option.split(',,')
            self.writeJumpChoices()
        except Exception:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def changeJumpChoices(self, choice, section, new):
        try:
            self.jumpChoices[choice + 1][FileOrder.index(section)] = str(new)
            self.writeJumpChoices()
        except TypeError:
            """Do nothing"""

    def writeJumpChoices(self):
        self.file = open(self.jump, mode='w+')
        try:
            for x, row in enumerate(self.jumpChoices):
                for y, column in enumerate(row):
                    self.file.write(column + (('\n' if x + 1 != len(self.jumpChoices) else '') if y + 1 == len(row) else ',,'))
                    self.file.flush()
        except Exception:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def addChoice(self):
        newFileOrder = EmptyFileOrder
        newFileOrder[FileOrder.index('Name')] = 'Choice {}'.format(str(len(self.jumpChoices)))
        newFileOrder[FileOrder.index('Type')] = self.jumpChoices[-1][FileOrder.index('Type')]
        self.jumpChoices.append(newFileOrder)
        self.writeJumpChoices()

    def getChoice(self, choice):
        try:
            self.getJumpChoices()
            choice = self.jumpChoices[choice + 1]
            self.choiceType = int(choice[FileOrder.index('Type')])
            self.choiceCP = choice[FileOrder.index('CP Change')]
            self.choiceActive = bool(choice[FileOrder.index('Active')] == 'True')
            self.choiceChained = bool(choice[FileOrder.index('Chained')] == 'True')
            self.choiceDescription = choice[FileOrder.index('Description')]
            self.choiceNotes = choice[FileOrder.index('Notes')]
        except Exception:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def deleteChoice(self, choice):
        self.getJumpChoices()
        del self.jumpChoices[choice + 1]
        self.writeJumpChoices()

    def getTotalCP(self):
        self.jumpCP = str(sum([int((choice[FileOrder.index('CP Change')]) if choice[FileOrder.index('CP Change')] != '' and bool(choice[FileOrder.index('Active')] == 'True') else 0) for choice in self.jumpChoices[1:]]))

    def renameJump(self, newName):
        try:
            self.file.close()
            newName = "{}__{}.csv".format(self.jump.split('/')[-1].split('__')[0], newName)
            os.rename(self.jump, self.pathConnect(self.jumperPath, newName))
            self.jump = self.pathConnect(self.jumperPath, newName)
            self.getJumpChoices()
        except TypeError:
            """Do nothing"""

    def renameChoice(self, choice, newName):
        self.changeJumpChoices(choice, 'Name', newName)

    def changeType(self, choice, newType):
        self.changeJumpChoices(choice, 'Type', newType)
        self.choiceType = int(newType)

    def changeCP(self, choice, newCP):
        self.changeJumpChoices(choice, 'CP Change', newCP)
        self.choiceCP = newCP
        self.getTotalCP()

    def changeActive(self, choice, newActive):
        self.changeJumpChoices(choice, 'Active', newActive)
        self.choiceActive = bool(newActive)
        self.getTotalCP()

    def changeChained(self, choice, newChained):
        self.changeJumpChoices(choice, 'Chained', newChained)
        self.choiceChained = bool(newChained)

    def changeDescription(self, choice, newDescription):
        self.changeJumpChoices(choice, 'Description', newDescription)
        self.choiceDescription = newDescription

    def changeNotes(self, choice, newNotes):
        self.changeJumpChoices(choice, 'Notes', newNotes)
        self.choiceNotes = newNotes
