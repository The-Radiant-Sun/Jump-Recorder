import os


class Info:
    def __init__(self):
        self.jumperPath = 'Info/Jumpers'

        self.jumpers = os.listdir(self.jumperPath)

        self.jumpPath = self.jumpers[0]

        self.jumps = os.listdir(self.jumperPath + '/' + self.jumpPath)
        self.remove(self.jumps, 4)

        self.file = self.jumpPath

    @staticmethod
    def remove(group, digits):
        for unit in group:
            group[group.index(unit)] = unit[:-digits]

    def getJumper(self, jumper):
        self.jumpPath = jumper
        self.jumps = os.listdir(self.jumperPath + '/' + self.jumpPath)
        self.remove(self.jumps, 4)

    def getJump(self, jump):
        self.file = self.jumpPath + jump + ".txt"