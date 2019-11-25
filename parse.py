# -*- coding: utf-8 -*-

netsDict = {}
pinsDict = {}
capCounter = {}
capCounter[0] = 0
resCounter = {}
resCounter[0] = 0
def getTotalCap(netsDict, wireName):
    maxC = 0
    segmentsList = netsDict[wireName]['segments']
   
    for eachList in segmentsList:
            maxC += eachList[2]
    
    return maxC
    
def printSPEFNets(netsDict):
    for key, value in netsDict.items():
        printNet(netsDict, key)
        
def printNet(netsDict, wireName):
    print('*D_NET', wireName, netsDict[wireName]['maxC'])
    print('*CONN')
    for eachConnection in netsDict[wireName]['conn']:
        print(eachConnection[0], eachConnection[1], eachConnection[2])
    
    print('*CAP')
    start = 1 #flag to print pin capacitance = 0
    for eachSegment in netsDict[wireName]['segments']:
        if(start):
            print(capCounter[0], eachSegment[0], '0')
            capCounter[0] += 1
            print(capCounter[0], eachSegment[1], eachSegment[2])   
            start = 0
        else:
            print(capCounter[0], eachSegment[1], eachSegment[2])
        capCounter[0] += 1
        
    print('*RES')
    for eachSegment in netsDict[wireName]['segments']:
        print(resCounter[0], eachSegment[0], eachSegment[1], eachSegment[3])
        resCounter[0] += 1
    print('*END\n')
    
#conList = [['inp1', '*P', 'I'],['u1:a', '*I', 'I']]
conList = []
conList.append(['*P', 'inp1', 'I'])
conList.append(['*I', 'u1:a', 'I'])
segmentsList = []
segmentsList.append(['inp1','inp1:1', 1.4,3.4])
segmentsList.append(['inp1:1','inp1:2', 1.4,3.5])
segmentsList.append(['inp1:2','u1:a', 1.5,3.6])
#maxC = getMaxCap(netsDict)

newDictionary = {}
newDictionary['conn'] = conList
newDictionary['segments'] = segmentsList
netsDict['_151_'] = newDictionary
netsDict['_151_']['maxC'] = getTotalCap(netsDict, '_151_')

#netsDict['_151_'].append(maxC)


print(netsDict)
print(netsDict['_151_'])
print(netsDict['_151_']['conn'])
print(netsDict['_151_']['segments'])
print(netsDict['_151_']['maxC'])


newDictionary = {}
newDictionary['M'] = 'M1'
newDictionary['x'] = 500
newDictionary['y'] = 700
newDictionary['name'] = 'inp:2'
newDictionary['type'] = '*I'
pinsDict['M1500700'] = newDictionary
print(pinsDict)

pinsDict['M1500700']['x'] = 700 #edit an item
print(pinsDict)

print(getMaxCap(netsDict, '_151_'))
#printNet(netsDict, '_151_')



conList = []
conList.append(['*P', 'inp2', 'I'])
conList.append(['*I', 'u1:b', 'I'])
segmentsList = []
segmentsList.append(['inp2','inp2:1', 2.0,4.0])
segmentsList.append(['inp2:1','inp2:2', 1.4,3.5])
segmentsList.append(['inp2:2','u1:b', 1.7,2.6])
#maxC = getMaxCap(netsDict)

newDictionary = {}
newDictionary['conn'] = conList
newDictionary['segments'] = segmentsList
netsDict['_149_'] = newDictionary
netsDict['_149_']['maxC'] = getTotalCap(netsDict, '_149_')


printSPEFNets(netsDict)