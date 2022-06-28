import sys
import copy

faults = ['AbstractVectorTest.testGet()', 'AbstractVectorTest.testTimesVector()', 'AbstractVectorTest.testZSum()', 'AbstractVectorTest.testDot()', 'AbstractVectorTest.testToString()', 'AbstractVectorTest.testCrossProduct()', 'AbstractVectorTest.testDot2()', 'AbstractVectorTest.testMinus()', 'TestLanczosSolver.testEigenvalueCheck()', 'TestLanczosSolver.testLanczosSolver()', 'VectorBinaryAggregateTest.testSeparate()', 'TestHebbianSolver.testHebbianSolver()', 'MatrixTest.testAggregateRows()', 'MatrixTest.testTimesVector()', 'MatrixTest.testAggregateCols()', 'MatrixTest.testTimesVector()', 'MatrixTest.testAggregateRows()', 'MatrixTest.testTimesSquaredTimesVector()', 'MatrixTest.testRowView()', 'VectorTest.testGetDistanceSquared()', 'VectorTest.testDenseVector()', 'VectorTest.testAggregation()']

methodMap = {}

def sortMethodMap(mmap):
    for key, value in mmap.items():
        if not value or value[0] == '':
            mmap[key] = 0
        else:
            mmap[key] = len(value)

    listofTuples = sorted(mmap.items() ,  key=lambda x: x[1], reverse=True)
    
    return listofTuples


def coverageFileMapping(fileName):
    with open(fileName) as fp:
        line = fp.readline()
        
        while line:
            data = line.strip().split(": ")
            key = data[0]
            value = data[1].strip('][').split(', ')
            methodMap.update({key : value})

            line = fp.readline()
        

def removeAdditionalMethods(additionalMethods):
    if additionalMethods:    
        for key, value in methodMap.items():
            for methodName in additionalMethods:
                if methodName in value:
                    value.remove(methodName)       



def getTFValue(sortedList):
    countSum = 0
    for fault in faults:
        count = 0
        for elem in sortedList:
            if(elem == fault):
                break
            count = count + 1
        countSum = countSum + count

    return countSum


def calculateAPFD(sortedList):
    f = open('mahout-additional-apfd.txt', 'w')
    num_t = 2500
    num_f = 22

    TF = getTFValue(sortedList)

    APFD = 1 - (TF / (num_t * num_f)) + (1 / (2 * num_t))

    result = 'APFD = ' + str(APFD)
    f.write(result)
    f.close()


def getTCPAdditionallResult(inFile):
    coverageFileMapping(inFile)
    f = open('mahout-additional-result.txt', 'w')

    additionalMethods = []
    additional_sortedList = {}

    count = 1616
    while count > 0:
        removeAdditionalMethods(additionalMethods)
        mmap = copy.deepcopy(methodMap)
        sortedList = sortMethodMap(mmap)
        line = str(sortedList[0][0]) + ': ' + str(sortedList[0][1]) + '\n'
        f.write(line)
        additional_sortedList.update({sortedList[0][0] : sortedList[0][1]})
        additionalMethods = methodMap[sortedList[0][0]]
        del methodMap[sortedList[0][0]]

        count = count - 1

    calculateAPFD(additional_sortedList)


def main(argv):
    tcp_total_result = sys.argv[2]
    getTCPAdditionallResult(tcp_total_result)


if __name__ == "__main__":
   main(sys.argv[1:])