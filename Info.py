import os


class Info:
    def __init__(self):
        self.jumpPath = 'Info/Jumps'
        self.jumperPath = 'Info/Jumpers'

        self.jumps = os.listdir(self.jumpPath)
        self.remove(self.jumps, 4)

        self.jumpers = os.listdir(self.jumperPath)
        self.remove(self.jumpers, 4)

        self.file = self.jumpPath

    @staticmethod
    def remove(group, digits):
        for unit in group:
            group[group.index(unit)] = unit[:-digits]


    def getJump(self, jump):
        self.file = self.jumpPath + jump
