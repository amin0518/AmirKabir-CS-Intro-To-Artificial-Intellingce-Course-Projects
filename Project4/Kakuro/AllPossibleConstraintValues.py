
import pickle
from pprint import pprint

if __name__ == '__main__':
    maxCells = 10
    a = []
    for cells in range(1, maxCells):
        minGuide = int(cells * (cells + 1) / 2)
        maxGuide = sum(sorted(list(range(1, 10)), reverse=True)[:cells])
        a.append(maxGuide-minGuide+1)
        print("cells: ", cells," min: ",minGuide," max: ", maxGuide)
    print("total constraints: ",sum(a))

    allPossibleConstraintValues = dict()
    a = 0
    for cells in range(1, maxCells):
        minGuide = int(cells * (cells + 1) / 2)
        maxGuide = sum(sorted(list(range(1, 10)), reverse=True)[:cells])
        for guide in range(minGuide, maxGuide + 1):
            answers = []
            m = 10 ** cells - 1
            for x in range(1, m):
                if len(set(str(x))) == cells and '0' not in set(str(x)) and sum(map(int, list(str(x)))) == guide:
                    candidate = set(map(int, list(str(x))))
                    if candidate not in answers:
                        answers.append(candidate)
            allPossibleConstraintValues[(cells, guide)] = answers
            a += 1
            print("number ",a, f' ({cells},{guide}) '," is done!")

    with open('allPossibleConstraintValues.pkl', 'wb') as fp:
        pickle.dump(allPossibleConstraintValues, fp)
        print('dictionary saved successfully to file')

    with open('allPossibleConstraintValues.pkl', 'rb') as fp:
        mydict = pickle.load(fp)
        print("2,16 : ", mydict[(2, 16)])
        print("3,23 : ", mydict[(3, 23)])
        print("7,35 : ", mydict[(7, 35)])
        # print('allPossibleConditionValues dictionary:\n')
        # pprint(mydict)
