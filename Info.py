import os
import sys
import subprocess


FileOrder = ['Name', 'Type', 'CP Change', 'Active', 'Chained', 'Description', 'Notes']

FileTree = ['Info/Jumpers', 'Info/Backup/Jumpers', 'Info/Backup/Jumps']


class Info:
    def __init__(self):
        for tree in FileTree:
            if not os.path.exists(tree):
                os.makedirs(tree)

        self.path = 'Info/Jumpers'

        self.getBackups()

        self.getJumpers()

        if len(self.jumpers) == 0:
            os.makedirs('Info/Jumpers/Jumper 1')
            self.getJumpers()
            try:
                open(self.pathConnect(self.path, self.jumpers[0]), mode='x').write("Name,,Type,,CP Change,,Active,,Chained,,Description,,Notes\nStarting CP,,6,,1000,,True,,False,,,,")
            except PermissionError:
                subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

        self.jumperPath = self.pathConnect(self.path, self.jumpers[0])

        self.getJumps()

        if len(self.jumps) == 0:
            self.addJump()

        self.jump = self.jumperPath

        self.file = None

        self.jumpChoices = []
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

    def getJumpers(self):
        self.jumpers = os.listdir(self.path)

    def getJumps(self):
        self.jumps = self.remove(os.listdir(self.jumperPath), 4)

    def getJumper(self, jumper):
        self.jumperPath = self.pathConnect(self.path, jumper)
        self.getJumps()

    def getBackups(self):
        self.backups = os.listdir(FileTree[2])

    def addJumper(self, jumperName):
        if jumperName[1] == True:
            try:
                os.makedirs(self.pathConnect(self.path, jumperName[0]))
                self.jumperPath = self.pathConnect(self.path, jumperName[0])
                self.getJumpers()
                self.getJumps()
                self.addJump()
                return jumperName[0]
            except Exception:
                return False
        return False

    def backupJumper(self):
        backupPath = self.pathConnect("Info/Backup/Jumpers", self.jumperPath.split('/')[-1])
        if os.path.exists(backupPath):
            os.rmdir(backupPath)
        os.makedirs(backupPath)
        record = self.jump
        for jump in self.jumps:
            self.jump = self.pathConnect(self.jumperPath, '{}.csv'.format(jump))
            self.getJumpChoices()
            self.backupJump(True)
        self.jump = record

    def renameJumper(self, newName):
        if newName[1] and newName[0] != '':
            try:
                self.file.close()
                newPath = self.pathConnect(self.path, newName[0])
                os.rename(self.jumperPath, newPath)
                self.getJumpers()
                self.jumperPath = newPath
                self.getJumps()
                return [True, newName[0]]
            except Exception:
                return [False]
        return [False]

    def deleteJumper(self):
        os.rmdir(self.jumperPath)
        self.getJumpers()

    def addJump(self):
        try:
            self.jump = self.pathConnect(self.jumperPath, '{}__New Jump {}.csv'.format(self.getLength(str(len(self.jumps) + 1)), str(len(self.jumps) + 1)))
            self.file = open(self.jump, mode='x')
            self.file.write("Name,,Type,,CP Change,,Active,,Chained,,Description,,Notes\nStarting CP,,6,,10000,,True,,False,,,,")
            self.getJumps()
        except FileExistsError:
            "Do Nothing"

    def getJump(self, row, jump):
        self.jump = self.pathConnect(self.jumperPath, "{}__{}.csv".format(self.getLength(str(row)), jump))
        self.getJumpChoices()

    def renameJump(self, newName):
        try:
            self.file.close()
            newName = "{}__{}.csv".format(self.jump.split('/')[-1].split('__')[0], newName)
            os.rename(self.jump, self.pathConnect(self.jumperPath, newName))
            self.jump = self.pathConnect(self.jumperPath, newName)
            self.getJumpChoices()
        except TypeError as Error:
            print(Error)

    def backupJump(self, toJumper):
        if toJumper:
            backupPath = self.pathConnect("Info/Backup/Jumpers", self.jump.split('/')[-2] + '/' + self.jump.split('/')[-1])
        else:
            backupPath = self.pathConnect("Info/Backup/Jumps", self.jump.split('/')[-1].split('__')[-1])
            backupPath = backupPath.split('.')
            backupPath = "{} - {}.{}".format(backupPath[0], self.jumperPath.split('/')[-1], backupPath[1])
        try:
            self.file = open(backupPath, mode='x')
        except FileExistsError:
            "Continue"
        record = self.jump
        self.jump = backupPath
        self.writeJumpChoices()
        self.getBackups()
        self.jump = record

    def importJump(self, jump):
        try:
            self.jump = self.pathConnect(FileTree[2], jump + '.csv')
            self.getJumpChoices()
            self.jump = self.pathConnect(self.jumperPath, '{}__{}.csv'.format(self.getLength(str(len(self.jumps) + 1)), jump))
            self.file = open(self.jump, mode='x')
            self.writeJumpChoices()
            self.getJumps()
            return True
        except Exception:
            return False

    def moveJump(self, oldPos, newPos):
        try:
            self.file.close()
            os.rename(self.jump, self.pathConnect(self.jumperPath, '0__' + self.jump.split('__')[1]))
            for jump in self.jumps:
                jumpID = int(jump.split('__')[0])
                if jumpID == oldPos:
                    continue
                if oldPos > jumpID > newPos:
                    os.rename(self.pathConnect(self.jumperPath, jump + '.csv'), self.pathConnect(self.jumperPath, '{}__{}.csv'.format(self.getLength(str(jumpID + 1)), jump.split('__')[1])))
                if oldPos < jumpID < newPos:
                    os.rename(self.pathConnect(self.jumperPath, jump + '.csv'), self.pathConnect(self.jumperPath, '{}__{}.csv'.format(self.getLength(str(jumpID - 1)), jump.split('__')[1])))
                if jumpID == newPos:
                    os.rename(self.pathConnect(self.jumperPath, jump + '.csv'), self.pathConnect(self.jumperPath, '{}__{}.csv'.format(self.getLength(str(jumpID + (-1 if int(self.jump.split('/')[-1].split('__')[0]) == 1 else 1))), jump.split('__')[1])))
            os.rename(self.pathConnect(self.jumperPath, '0__' + self.jump.split('__')[1]), self.pathConnect(self.jumperPath, '{}__{}'.format(self.getLength(str(newPos)), self.jump.split('__')[1])))
            self.getJumps()
        except Exception as Error:
            print(Error)

    def deleteJump(self):
        try:
            self.file.close()
            os.remove(self.jump)
            self.getJumps()
            for jump in self.jumps:
                jumpID = int(jump.split('__')[0])
                if jumpID > int(self.jump.split('/')[-1].split('__')[0]):
                    os.rename(self.pathConnect(self.jumperPath, jump + '.csv'), self.pathConnect(self.jumperPath, '{}__{}.csv'.format(self.getLength(str(jumpID - 1)), jump.split('__')[1])))
        except Exception:
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
        except Exception as Error:
            print(Error)

    def changeJumpChoices(self, choice, section, new):
        self.jumpChoices[choice + 1][FileOrder.index(section)] = str(new)
        self.writeJumpChoices()

    def writeJumpChoices(self):
        self.file = open(self.jump, mode='w+')
        try:
            for x, row in enumerate(self.jumpChoices):
                for y, column in enumerate(row):
                    for char in column:
                        try:
                            self.file.write(char)
                        except Exception:
                            self.file.write('?')
                    self.file.write(('\n' if x + 1 != len(self.jumpChoices) else '') if y + 1 == len(row) else ',,')
                    self.file.flush()
        except Exception as Error:
            print(Error)

    def addChoice(self):
        newFileOrder = ['' for order in FileOrder]
        newFileOrder[FileOrder.index('Name')] = 'Choice {}'.format(str(len(self.jumpChoices)))
        newFileOrder[FileOrder.index('Type')] = self.jumpChoices[-1][FileOrder.index('Type')]
        newFileOrder[FileOrder.index('CP Change')] = '00'
        newFileOrder[FileOrder.index('Active')] = 'False'
        newFileOrder[FileOrder.index('Chained')] = 'False'

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
        except Exception as Error:
            print(Error)

    def moveChoice(self, newPos, oldPos):
        try:
            changed = []
            for i, choice in enumerate(self.jumpChoices):
                if i == newPos:
                    changed.append(self.jumpChoices[oldPos])
                if i != oldPos:
                    changed.append(choice)
            self.jumpChoices = changed
            self.writeJumpChoices()
        except Exception as Error:
            print(Error)

    def deleteChoice(self, choice):
        self.getJumpChoices()
        del self.jumpChoices[choice + 1]
        self.writeJumpChoices()

    def getTotalCP(self):
        self.jumpCP = str(sum([int((choice[FileOrder.index('CP Change')][:-1]) if bool(choice[FileOrder.index('Active')] == 'True') else 0) for choice in self.jumpChoices[1:]]))

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
