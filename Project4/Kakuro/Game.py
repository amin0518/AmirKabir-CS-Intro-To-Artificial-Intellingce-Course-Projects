import pickle

import boardLists
from Cell import Cell
from Constraint import Constraint
from pandas import DataFrame


class Game:
    # encapsulates game board with all its cells and conditions
    def makeBoardFromList(self, name=None):  # TODO: Add other boards
        self.board = []  # 2D board list

        if name == "Easy1":
            boardList = boardLists.Easy1
        elif name == "Expert1":
            boardList = boardLists.Expert1
        else:
            boardList = boardLists.Easy1

        for line in boardList:
            cellLine = []  # 1D read cell line list
            for item in line:
                if item == 'b':
                    cell = Cell()
                    cellLine.append(cell)
                elif item == 'w':
                    cell = Cell(white=True)
                    cellLine.append(cell)
                else:
                    a1, a2 = item
                    cell = Cell(white=False, value=(a1, a2))
                    cellLine.append(cell)
            self.board.append(cellLine)

    def addConstraints(self):
        # calculates conditions and adds them to their binding cells
        # also makes the whites list
        boardSize = len(self.board)
        with open('allPossibleConstraintValues.pkl', 'rb') as fp:
            allPossibleConstraintValues = pickle.load(fp)
            for i in range(boardSize):
                for j in range(boardSize):
                    if self.board[i][j].isBlackCondition():

                        a1, a2 = self.board[i][j].getValue()

                        if a2 != 0:  # horizontal condition
                            start = j + 1
                            end = 0
                            for k in range(start, boardSize):
                                if self.board[i][k].isBlack():
                                    end = k - 1
                                    break
                            if end == 0:
                                end = boardSize-1
                            condition = ('h', i, start, end, a2)  # row, start, end, sum
                            for k in range(start, end + 1):
                                self.board[i][k].constraints.append(condition)
                            cells = end - start + 1
                            self.constraints[condition] = Constraint(name=condition,
                                                                     possibleValueSets=allPossibleConstraintValues[
                                                                       (cells, a2)])

                        if a1 != 0:  # vertical condition
                            start = i + 1
                            end = 0
                            for k in range(start, boardSize):
                                if self.board[k][j].isBlack():
                                    end = k - 1
                                    break
                            if end == 0:
                                end = boardSize-1
                            condition = ('v', j, start, end, a1)  # column, start, end, sum
                            for k in range(start, end + 1):
                                self.board[k][j].constraints.append(condition)
                            cells = end - start + 1
                            self.constraints[condition] = Constraint(name=condition,
                                                                     possibleValueSets=allPossibleConstraintValues[
                                                                       (cells, a1)])

            for i in range(boardSize):
                for j in range(boardSize):
                    if self.board[i][j].isWhite():
                        cords = (i, j)
                        self.board[i][j].coordinate = cords
                        # self.board[i][j].FindInitialPossibleValues(self.conditions)
                        self.Whites.append(self.board[i][j])

    def __init__(self, name='Easy1'):
        self.constraints = dict()  # Game constraints is a dict while Cell constraints is a list
        self.board = None
        self.Whites = []
        self.makeBoardFromList(name)
        self.addConstraints()

    def printBoard(self, compact=True):

        def strOutTuple(t):
            # outs len 5 strings
            t1, t2 = t
            if t1 == 0:
                if t2 < 10:
                    t2 = f'{t2} '
                else:
                    t2 = str(t2)
                return '  \\' + t2
            elif t2 == 0:
                if t1 < 10:
                    t1 = f' {t1}'
                else:
                    t1 = str(t1)
                return t1 + '\\  '
            else:
                if t1 < 10:
                    t1 = f' {t1}'
                if t2 < 10:
                    t2 = f'{t2} '
                t1 = str(t1)
                t2 = str(t2)
                return t1 + '\\' + t2

        def strOutNum(num):
            if num < 10:
                return f'  {num}  '
            else:
                return f' {num}  '

        print('\n')
        boardSize = len(self.board)
        boardList = []
        if compact:
            for i in range(boardSize):
                row = []
                for j in range(boardSize):
                    cell = self.board[i][j]
                    if cell.isBlack():
                        row.append('  B  ')  # 2 spaces
                    if cell.isWhite():
                        if cell.isEmpty():
                            row.append('  W  ')
                        else:
                            row.append(strOutNum(cell.getValue()))
                boardList.append(row)
        else:
            for i in range(boardSize):
                row = []
                for j in range(boardSize):
                    cell = self.board[i][j]
                    if cell.isBlack():
                        if cell.isBlackCondition():
                            row.append(strOutTuple(cell.getValue()))
                        else:
                            row.append('  B  ')  # 2 spaces
                    if cell.isWhite():
                        if cell.isEmpty():
                            row.append('  W  ')
                        else:
                            row.append(strOutNum(cell.getValue()))
                boardList.append(row)

        print(DataFrame(boardList).to_string(index=False, header=False))
