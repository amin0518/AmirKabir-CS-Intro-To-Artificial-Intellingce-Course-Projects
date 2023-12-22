from math import ceil


class Constraint:
    def __init__(self, name, possibleValueSets=None):
        self.name = name
        self.cellsNumber = name[3] - name[2] + 1
        self.guide = name[4]
        self.possibleValueSets = possibleValueSets

    def isConsistent(self, num, game, usePreprocessing=True):
        t = self.name[0]
        a = self.name[1]
        b = self.name[2]
        c = self.name[3]
        hasVal = []
        if t == 'h':
            for d in range(b, c + 1):
                if not game.board[a][d].isEmpty():
                    hasVal.append(game.board[a][d].getValue())
        else:
            for d in range(b, c + 1):
                if not game.board[d][a].isEmpty():
                    hasVal.append(game.board[d][a].getValue())

        # is consistent
        if usePreprocessing:
            hasVal = set(hasVal)
            if num in hasVal:
                return False
            for possibleValueSet in self.possibleValueSets:
                if num in possibleValueSet and hasVal.issubset(possibleValueSet):
                    return True
            return False

        else:
            if num in hasVal:
                return False
            else:
                if len(hasVal) < self.cellsNumber - 1:
                    remain_cells = self.cellsNumber - len(hasVal) - 1
                    if self.guide - (sum(hasVal) + num) >= remain_cells * (remain_cells + 1) / 2:
                        return True
                    return False
                    # return True
                else:
                    if sum(hasVal) + num == self.guide:
                        return True
                    else:
                        return False

    def remainingAndTakenValueSets(self,game):

        t = self.name[0]
        a = self.name[1]
        b = self.name[2]
        c = self.name[3]
        hasVal = []
        if t == 'h':
            for d in range(b, c + 1):
                if not game.board[a][d].isEmpty():
                    hasVal.append(game.board[a][d].getValue())
        else:
            for d in range(b, c + 1):
                if not game.board[d][a].isEmpty():
                    hasVal.append(game.board[d][a].getValue())
        if not hasVal:
            return self.possibleValueSets,hasVal
        # else
        hasVal = set(hasVal)
        ActualValueSets = []
        for possibleValueSet in self.possibleValueSets:
            if hasVal.issubset(possibleValueSet):
                ActualValueSets.append(possibleValueSet)

        return ActualValueSets,hasVal

