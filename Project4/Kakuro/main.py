from Game import Game
import time


def possible(value, cell, game):
    # cond is class here
    condList = [game.constraints[cond] for cond in game.constraints if cond in cell.constraints]
    # condList = cell.FindConditionClasses(game.conditions)
    canAdd = True
    for cond in condList:
        canAdd = canAdd and cond.isConsistent(value, game)
    return canAdd


def setValue(value, cell):
    cell.value = value


def removeValue(cell):
    cell.value = None


def SolveBoard(game,forwardChecking,MRV):
    # solves the board without Forward-checking
    if MRV and forwardChecking:
        sortByPriority = lambda whiteCell: len(whiteCell.currentPossibleValues(game))
        game.Whites.sort(key=sortByPriority)
    elif MRV:
        sortByPriority = lambda whiteCell: len(whiteCell.initialPossibleValues(game.constraints))
        game.Whites.sort(key=sortByPriority)

    for white in game.Whites:
        cell = white
        if cell.isEmpty():
            if forwardChecking:
                cellPossibilities = cell.currentPossibleValues(game)
                for candidateValue in cellPossibilities:
                    setValue(candidateValue, cell)
                    SolveBoard(game, forwardChecking, MRV)
                    removeValue(cell)
                return
            else:
                cellPossibilities = cell.initialPossibleValues(game.constraints)
                for candidateValue in cellPossibilities:
                    if possible(candidateValue, cell, game):
                        setValue(candidateValue, cell)
                        SolveBoard(game, forwardChecking, MRV)
                        removeValue(cell)
                return

    game.printBoard(compact=False)


if __name__ == '__main__':
    print("This is Kakuro Solver.\nChoose a Game Board and input the parameters of the solver.")
    boardName = input("Choose the Board (among Expert1 and Easy1):  ")
    print("Now choose solver parameters:")
    doForwardChecking = bool(int(input("if you want forwardChecking type 1 otherwise 0:  ")))
    doMRV = bool(int(input("if you want Most Restrained Variable ordering type 1 otherwise 0:  ")))
    print('\n\nSolver params: doForwardChecking: ',doForwardChecking,'  doMRV: ',doMRV)
    start = time.perf_counter()
    mygame = Game(name=boardName)
    # mygame.printBoard(compact=False)
    SolveBoard(game=mygame,forwardChecking=doForwardChecking,MRV=doMRV)
    end = time.perf_counter()
    print('\nTotal Time to create the game board and Solve it: ', round(end - start, 6))

