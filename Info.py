import os

FileOrder = ['Name', 'Type', 'CP Change', 'Active', 'Chained', 'Description', 'Notes']


class Info:
    def __init__(self):
        self.path = 'Info/Jumpers'

        self.jumpers = os.listdir(self.path)

        self.jumperPath = self.pathConnect(self.path, self.jumpers[0])

        self.jumps = self.remove(os.listdir(self.jumperPath), 4)

        self.jump = self.jumperPath

        self.file = None

        self.jumpOptions = None
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

    def getJumper(self, jumper):
        self.jumperPath = self.pathConnect(self.path, jumper)
        self.jumps = os.listdir(self.jumperPath)
        self.remove(self.jumps, 4)

    def getJump(self, jump):
        self.jump = self.pathConnect(self.jumperPath, jump + ".csv")
        self.getJumpOptions()

    def getJumpOptions(self):
        try:
            self.file = open(self.jump, mode='r')
            self.jumpOptions = self.file.readlines()
            for i, option in enumerate(self.jumpOptions):
                if option != self.jumpOptions[-1]:
                    self.jumpOptions[i] = option[:-1].split(',,')
                else:
                    self.jumpOptions[i] = option.split(',,')
            self.writeJumpOptions()
        except Exception:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def changeJumpOptions(self, choice, section, new):
        try:
            self.jumpOptions[choice + 1][FileOrder.index(section)] = str(new)
            self.writeJumpOptions()
        except TypeError:
            """Do nothing"""

    def writeJumpOptions(self):
        self.file = open(self.jump, mode='w+')
        try:
            for x, row in enumerate(self.jumpOptions):
                for y, column in enumerate(row):
                    self.file.write(column + (('\n' if x + 1 != len(self.jumpOptions) else '') if y + 1 == len(row) else ',,'))
                    self.file.flush()
        except Exception:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def getChoice(self, choice):
        try:
            self.getJumpOptions()
            choice = self.jumpOptions[choice + 1]
            self.choiceType = int(choice[FileOrder.index('Type')])
            self.choiceCP = choice[FileOrder.index('CP Change')]
            self.choiceActive = bool(choice[FileOrder.index('Active')] == 'True')
            self.choiceChained = bool(choice[FileOrder.index('Chained')] == 'True')
            self.choiceDescription = choice[FileOrder.index('Description')]
            self.choiceNotes = choice[FileOrder.index('Notes')]
        except Exception:
            print(1)
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def getTotalCP(self):
        self.jumpCP = str(sum([int(choice[FileOrder.index('CP Change')]) for choice in self.jumpOptions[1:]]))

    def renameJump(self, newName):
        try:
            self.file.close()
            os.rename(self.jump, self.pathConnect(self.jumperPath, newName + ".csv"))
            self.jump = self.pathConnect(self.jumperPath, newName + ".csv")
            self.getJumpOptions()
        except TypeError:
            """Do nothing"""

    def renameChoice(self, choice, newName):
        self.changeJumpOptions(choice, 'Name', newName)

    def changeType(self, choice, newType):
        self.changeJumpOptions(choice, 'Type', newType)
        self.choiceType = int(newType)

    def changeCP(self, choice, newCP):
        self.changeJumpOptions(choice, 'CP Change', newCP)
        self.choiceCP = newCP
        self.getTotalCP()

    def changeActive(self, choice, newActive):
        self.changeJumpOptions(choice, 'Active', newActive)
        self.choiceActive = bool(newActive)

    def changeChained(self, choice, newChained):
        self.changeJumpOptions(choice, 'Chained', newChained)
        self.choiceChained = bool(newChained)

    def changeDescription(self, choice, newDescription):
        self.changeJumpOptions(choice, 'Description', newDescription)
        self.choiceDescription = newDescription

    def changeNotes(self, choice, newNotes):
        self.changeJumpOptions(choice, 'Notes', newNotes)
        self.choiceNotes = newNotes
