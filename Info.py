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

        self.choiceType = 0
        self.choiceCP = 0
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
            self.jumpOptions = [self.remove(self.jumpOptions[:-1], 1), [self.jumpOptions[-1]]]
            self.jumpOptions = [option[0].split(',,') for option in self.jumpOptions]
            self.file = open(self.jump, mode='w+')
            for row in self.jumpOptions:
                for column in row:
                    self.file.write(column + (('\n' if row != self.jumpOptions[-1] else '') if column == row[-1] else ',,'))
                    self.file.flush()
        except Exception:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def getChoice(self, choice):
        try:
            a = 'b'
        except Exception:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def renameJump(self, newName):
        try:
            self.file.close()
            os.rename(self.jump, self.pathConnect(self.jumperPath, newName + ".csv"))
            self.jump = self.pathConnect(self.jumperPath, newName + ".csv")
            self.getJumpOptions()
        except TypeError:
            """Do nothing"""

    def renameChoice(self, choice, newName):
        try:
            # Add filling
            self.getJumpOptions()
        except TypeError:
            """Do nothing"""
