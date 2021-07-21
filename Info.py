import os

FileOrder = ['Name', 'Type', 'CP Change', 'Active', 'Chained', 'Description', 'Notes']

class Info:
    def __init__(self):
        self.path = 'Info/Jumpers'

        self.jumpers = os.listdir(self.path)

        self.jumperPath = self.pathConnect(self.path, self.jumpers[0])

        self.jumps = self.remove(os.listdir(self.jumperPath), 4)

        self.jump = self.jumperPath

        self.file = ''

        self.jumpOptions = ''
        self.jumpCP = 1000

        self.choiceName = 'Unknown'
        self.choiceType = 'Unknown'
        self.choiceCP = 0
        self.active = False
        self.chained = False
        self.description = 'Unknown'

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

    def getJumpOptions(self):
        try:
            self.file = open(self.jump, mode='r')
            self.jumpOptions = [option.split(',,') for option in self.remove(self.file.readlines(), 2)]
            self.file = open(self.jump, mode='w+')
            print(self.jumpOptions)
            for row in self.jumpOptions:
                for column in row:
                    self.file.write(column + ('\n' if column == row[-1] else ',,'))
                    print(column + ('\n' if column == row[-1] else ',,'))
                    print(self.file.readlines())
        except BaseException:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()

    def renameJump(self, newName):
        try:
            self.file.close()
            print(self.jump)
            print(self.pathConnect(self.jumperPath, newName + ".csv"))
            os.rename(self.jump, self.pathConnect(self.jumperPath, newName + ".csv"))
            self.jump = self.pathConnect(self.jumperPath, newName + ".csv")
            self.getJumpOptions()
        except TypeError:
            """Do nothing"""
