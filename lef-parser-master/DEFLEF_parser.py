# -*- coding: utf-8 -*-
import def_parser
import lef_parser
from collections import defaultdict

path = "./libraries/Nangate/NangateOpenCellLibrary.lef"
lef_parser = LefParser(path)
lef_parser.parse()


read_path = "./libraries/DEF/c1908.def"
def_parser = DefParser(read_path)
def_parser.parse()

netsDict = defaultdict(list)

for pin in def_parser.pins:
    print(pin)
    
def get_resistance(segment):
    layer_name = segment.layer
    rPerSquare = lef_parser.layer_dict[layer_name].resistance[1]
    width = lef_parser.layer_dict[layer_name].width
    length = abs(segment.points[0][0] - segment.points[1][0]) + abs(segment.points[0][1] - segment.points[1][1]) 
    resistance = length * rPerSquare / width
    return resistance
    
def get_capacitance(segment):
    layer_name = segment.layer
    cPerSquare = lef_parser.layer_dict[layer_name].capacitance[1]
    width = lef_parser.layer_dict[layer_name].width
    length = abs(segment.points[0][0] - segment.points[1][0]) + abs(segment.points[0][1] - segment.points[1][1])
    if(lef_parser.layer_dict[layer_name].edge_cap != None):
        edgeCapacitance = lef_parser.layer_dict[layer_name].edge_cap
    else:
        edgeCapacitance = 0
    capacitance = length * cPerSquare * width + edgeCapacitance * length
    return capacitance
    
for net in def_parser.nets:
    conList = []
    # generate the conn data structure for conn section
    for con in net.comp_pin:
        #check if pin is *P
        current_pin = []
        if(con[0] == "PIN"):
            current_pin.append("*P")
            current_pin.append(con[1])
            x = def_parser.pins.get_pin(con[1])
            if(x.direction == "INPUT"):
                current_pin.append("I")
            else:
                current_pin.append("O")
            
        else:
            current_pin.append("*I")
            current_pin.append(con[0]+":"+con[1]) 
            cell_type = def_parser.components.comp_dict[con[0]].macro
            direction = lef_parser.macro_dict[cell_type].pin_dict[con[1]].info["DIRECTION"]
            if(direction == "INPUT"):
                current_pin.append("I")
            else:
                current_pin.append("O")
                
        conList.append(current_pin)
        
    # generate the Resistance and Capacitances data structure
#    counter = 1
#    for segment in net.routed:
#        startingNodeKey = str(segment.layer)+str(segment.points[0][0])+str(segment.points[0][1])
#        endingNodeKey = str(segment.layer)+str(segment.points[1][0])+str(segment.points[1][1])
#        if(pinsDict[startingNodeKey] != None):
#            startingNode = pinsDict[startingNodeKey]
#        else:
#            startingNode = str(net.name) + ":" +  str(counter)
#            counter += 1
#            pinsDict[startingNodeKey] = startingNode
#            
#        if(pinsDict[endingNodeKey] != None):
#            endingNode = pinsDict[endingNodeKey]
#        else:    
#            endingNode = str(net.name) + ":" +  str(counter)
#            counter += 1
#            pinsDict[endingNodeKey] = endingNode
#        
#        resistance = get_resistance(segment)
#        capacitance = get_capacitance(segment)
#        
        
    counter = 1
    for segment in net.routed:
        #startingNodeKey = str(segment.layer)+str(segment.points[0][0])+str(segment.points[0][1])
        #endingNodeKey = str(segment.layer)+str(segment.points[1][0])+str(segment.points[1][1])
        startingNode = []
        endingNode = []
        for i int pinstable:
            if(segment.layer==i[0]):
                if(i[1]<=segment.points[0][0]<=i[3] && i[2]<=segment.points[0][1]<=i[4]):
                    startingNode = i
            
            if(segment.layer==i[0]):
                if(i[1]<=segment.points[1][0]<=i[3] && i[2]<=segment.points[1][1]<=i[4]):
                    endingNode = i  
                
        if(len(startingNode == 0)):    
            startingNode.append(str(segment.layer))
            startingNode.append(segment.points[0][0])
            startingNode.append(segment.points[0][1])
            startingNode.append(segment.points[0][0])
            startingNode.append(segment.points[0][1])
            startingNode.append(str(net.name) + ":" +  str(counter))
            counter += 1
            pinstable.append(startingNode)
            
        if(len(endingNode == 0):
            endingNode.append(str(segment.layer))
            endingNode.append(segment.points[1][0])
            endingNode.append(segment.points[1][1])
            endingNode.append(segment.points[1][0])
            endingNode.append(segment.points[1][1])
            endingNode.append(str(net.name) + ":" +  str(counter))
            counter += 1
            pinstable.append(endingNode)
        
        resistance = get_resistance(segment)
        capacitance = get_capacitance(segment)
        
        
        
        
    """
    newDictionary = {}
    newDictionary['conn'] = conList
    newDictionary['segments'] = segmentsList
    newDictionary['maxC'] = 95
    """    
    
    
    
    
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


#def getMaxCap(netsDict):
    

#conList = [['inp1', '*P', 'I'],['u1:a', '*I', 'I']]

#netsDict['_151_'].append(maxC)

'''
print(netsDict)
print(netsDict['_151_'])
print(netsDict['_151_']['conn'])
print(netsDict['_151_']['segments'])
print(netsDict['_151_']['maxC'])
'''




