# -*- coding: utf-8 -*-

netsDict = {}



#def getMaxCap(netsDict):
    
    
    
    


#conList = [['inp1', '*P', 'I'],['u1:a', '*I', 'I']]
conList = []
conList.append(['inp1', '*P', 'I'])
conList.append(['u1:a', '*I', 'I'])
segmentsList = []
segmentsList.append(['inp1','inp1:1', 1.4,3.4])
segmentsList.append(['inp1:1','inp1:2', 1.4,3.5])
segmentsList.append(['inp1:2','u1:a', 1.5,3.6])
#maxC = getMaxCap(netsDict)

newDictionary = {}
newDictionary['conn'] = conList
newDictionary['segments'] = segmentsList
newDictionary['maxC'] = 95

netsDict['_151_'] = newDictionary
#netsDict['_151_'].append(maxC)


print(netsDict)
print(netsDict['_151_'])
print(netsDict['_151_']['conn'])
print(netsDict['_151_']['segments'])
print(netsDict['_151_']['maxC'])