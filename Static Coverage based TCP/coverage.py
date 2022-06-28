import os
import subprocess
import sys
import datetime

# dict to hold final test case to static-code coverage 
methodMap = {}
staticMethodMap = {}

# filters the lines from callGraph file to contain only the ones only in mahout package
def filterCallGraph():
    filepath = 'callGraph.txt'
    with open(filepath) as fp:
        f = open("mahoutProjCallGraph.txt", "w")
        
        line = fp.readline()
        
        while line:
            if line.startswith('M:org.apache.mahout') and 'init' not in line:
                data = line.strip().split(" ")

                if 'org.apache.mahout' not in data[1]:
                    line = fp.readline()
                    continue

                f.write(line)

            line = fp.readline()

        f.close()

# maps source code methods
def generateStaticMethodMapping():
    filepath = 'mahoutProjCallGraph.txt'
    with open(filepath) as fp:
        line = fp.readline()
        
        while line:
            data = line.strip().split(" ")
            caller = data[0].split(":")
            callee = data[1].split(":")

            callerMethod = caller[2]
            callerClassPkg = caller[1].split('.')
            callerClass = callerClassPkg[len(callerClassPkg) - 1]

            calleeMethod = callee[1]
            calleeClassPkg = callee[0].split('.')
            calleeClass = calleeClassPkg[len(calleeClassPkg) - 1]

            if 'Test' not in callerClass and 'test' not in callerMethod:
                key = callerClass + "." + callerMethod
                if key not in staticMethodMap.keys():
                    staticMethodMap.update({key: set()})
                if 'Test' not in callerClass and 'test' not in callerMethod:
                    value = calleeClass + "." + calleeMethod
                    staticMethodMap[key].add(value)

            line = fp.readline()

    
# generates the initial mapping of test method to source code methods
def generateTestMethodMapping():
    filepath = 'callGraph.txt'
    with open(filepath) as fp:
        line = fp.readline()
        
        while line:
            if line.startswith('M:org.apache.mahout') and 'init' not in line:
                data = line.strip().split(" ")
                caller = data[0].split(":")

                if 'org.apache.mahout' not in data[1]:
                    line = fp.readline()
                    continue

                callee = data[1].split(":")

                callerMethod = caller[2]
                callerClassPkg = caller[1].split('.')
                callerClass = callerClassPkg[len(callerClassPkg) - 1]

                calleeMethod = callee[1]
                calleeClassPkg = callee[0].split('.')
                calleeClass = calleeClassPkg[len(calleeClassPkg) - 1]

                if 'Test' in callerClass and 'test' in callerMethod:
                    key = callerClass + "." + callerMethod
                    if key not in methodMap.keys():
                        methodMap.update({key: set()})
                    if 'Test' not in calleeClass and 'test' not in calleeMethod:
                        value = calleeClass + "." + calleeMethod
                        methodMap[key].add(value)

            line = fp.readline()

    # get deeper to get static method level coverage - get the methods invoked by the callee methods in the 'methodMap'
    count = 0
    while count < 10:
        for key in methodMap.keys():
            methodMap[key].update(getSubSet(methodMap[key]))
        count = count + 1

    # write the result to a file
    f = open("mahout-coverage.txt", "w")
    for key, value in methodMap.items():
        line = str(key) + ': ' + str(list(value)) + '\n'
        f.write(line)

    f.close()


def getSubSet(methodList):
    result = set()
    for elem in methodList:
        if elem in staticMethodMap.keys():
            result = result.union(staticMethodMap[elem])

    return result


def generateCallGraph(jarFile):
    f = open("callGraph.txt", "w")
    subprocess.call("java -jar ./data/mahout/javacg-0.1-SNAPSHOT-static.jar " + jarFile, shell=True, stdout=f)
    f.close()
    filterCallGraph()
    generateStaticMethodMapping()
    generateTestMethodMapping()


def main(argv):
    jarFile = sys.argv[2]
    generateCallGraph(jarFile)


if __name__ == "__main__":
   main(sys.argv[1:])
