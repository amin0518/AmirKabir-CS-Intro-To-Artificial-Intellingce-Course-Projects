class Cell:

    def __init__(self, white=False, value=None, constraints=None, possibleValues=None, priority=None, coordinate=None):
        # For white cells, value is the answer, for blacks it's the condition.
        # conditions is the name of condition classes biding on the cell
        # acceptable shows valid possible choices
        if constraints is None:
            constraints = []
        self.coordinate = coordinate
        self.white = white
        self.value = value
        self.constraints = constraints
        self.possibleValues = possibleValues  # values that are Possibles
        self.priority = priority
        # self.singleCondition = False

    def isWhite(self):
        return self.white

    def isBlack(self):
        return not self.white

    def isBlackCondition(self):
        return (not self.white) and (self.value is not None)

    def getValue(self):
        return self.value

    def isEmpty(self):
        return self.value is None

    def initialPossibleValues(self, GameConstraints):
        if self.possibleValues is not None:
            return self.possibleValues

        constraintClasses = [GameConstraints[cond] for cond in GameConstraints if cond in self.constraints]
        c1, c2 = constraintClasses
        p1 = c1.possibleValueSets
        p2 = c2.possibleValueSets
        possibleValues = []
        for item1 in p1:
            for item2 in p2:
                item = item1 & item2
                if len(item) > 0:
                    for i in item:
                        if i not in possibleValues:
                            possibleValues.append(i)

        self.possibleValues = possibleValues
        return possibleValues

    def currentPossibleValues(self, game):
        constraintClasses = [game.constraints[cond] for cond in game.constraints if cond in self.constraints]
        c1, c2 = constraintClasses
        p1,h1 = c1.remainingAndTakenValueSets(game)
        p2,h2 = c2.remainingAndTakenValueSets(game)
        if not h1 and not h2:
            self.initialPossibleValues(game.constraints)
            return self.possibleValues
        # else
        currentPossibleValues = []
        for item1 in p1:
            for item2 in p2:
                item = item1 & item2
                if len(item) > 0:
                    for i in item:
                        if i not in currentPossibleValues and i not in h1 and i not in h2:
                            currentPossibleValues.append(i)
        return currentPossibleValues

