import os
import csv

FileOrder = ['Name', 'Type', 'CP Change', 'Active', 'Chained', 'Description']

class Info:
    def __init__(self):
        self.path = 'Info/Jumpers'

        self.jumpers = os.listdir(self.path)

        self.jumperPath = self.pathConnect(self.path, self.jumpers[0])

        self.jumps = os.listdir(self.jumperPath)
        self.remove(self.jumps, 4)

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
            self.jumpOptions = csv.reader(self.file)
            self.file = open(self.jump, mode='w+')
            print(self.jumpOptions)
        except BaseException:
            thisIsLiterallyImpossible = True  # Read name of variable
            quit()
