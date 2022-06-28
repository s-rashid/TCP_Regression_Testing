import sys

faults = ['AbstractVectorTest.testGet()', 'AbstractVectorTest.testTimesVector()', 'AbstractVectorTest.testZSum()', 'AbstractVectorTest.testDot()', 'AbstractVectorTest.testToString()', 'AbstractVectorTest.testCrossProduct()', 'AbstractVectorTest.testDot2()', 'AbstractVectorTest.testMinus()', 'TestLanczosSolver.testEigenvalueCheck()', 'TestLanczosSolver.testLanczosSolver()', 'VectorBinaryAggregateTest.testSeparate()', 'TestHebbianSolver.testHebbianSolver()', 'MatrixTest.testAggregateRows()', 'MatrixTest.testTimesVector()', 'MatrixTest.testAggregateCols()', 'MatrixTest.testTimesVector()', 'MatrixTest.testAggregateRows()', 'MatrixTest.testTimesSquaredTimesVector()', 'MatrixTest.testRowView()', 'VectorTest.testGetDistanceSquared()', 'VectorTest.testDenseVector()', 'VectorTest.testAggregation()']

methodMap = {}

def getMethodMap(fileName):
    #methodMap = {}
    with open(fileName) as fp:
        line = fp.readline()
        
        while line:
            data = line.strip().split(": ")
            key = data[0]
            value = data[1].strip('][').split(', ')
            methodMap.update({key : value})

            line = fp.readline()
    
    #return methodMap

def sortMethodMap():
    for key, value in methodMap.items():
        if value[0] == '':
            methodMap[key] = 0
        else:
            methodMap[key] = len(value)

    listofTuples = sorted(methodMap.items() ,  key=lambda x: x[1], reverse=True)
    
    f = open("mahout-total-result.txt", "w")
    for elem in listofTuples :
        line = str(elem[0]) + ': ' + str(elem[1]) + '\n'
        f.write(line)
    
    f.close()
    return listofTuples


def getTFValue(sortedList):
    countSum = 0
    for fault in faults:
        count = 0
        for elem in sortedList:
            if(elem[0] == fault):
                break
            count = count + 1
        countSum = countSum + count

    return countSum


def calculateAPFD(sortedList):
    f = open('mahout-total-apfd.txt', 'w')
    num_t = 2500
    num_f = 22

    TF = getTFValue(sortedList)

    APFD = 1 - (TF / (num_t * num_f)) + (1 / (2 * num_t))

    result = 'APFD = ' + str(APFD)
    f.write(result)
    f.close()


def getTotalResult(inFile):
    getMethodMap(inFile)
    sortedTestCases = sortMethodMap()
    calculateAPFD(sortedTestCases)


def main(argv):
    coverageFile = sys.argv[2]
    getTotalResult(coverageFile)


if __name__ == "__main__":
   main(sys.argv[1:])