# -*- coding: utf-8 -*-
from def_parser import *
from lef_parser import *

from collections import defaultdict

# We had to modify the lef parser to ignore the second parameter for the offset
# since our files provide only 1 value
path = "osu035.lef"
lef_parser = LefParser(path)
lef_parser.parse()


read_path = "bcd_routed.def"
def_parser = DefParser(read_path)
def_parser.parse()

netsDict = defaultdict(list)
pinsTable = []

# l2d is the conversion factor between the scale in LEF and DEF
# we need a function to generalize this for any two lef and def files
l2d = 10


# A function that takes an instance and a pin and returns a list of all
# rectangles of that pin 
def getPinLocation(instanceName, pinName, listOfPinRects):
    #myInstance = def_parser.components.get_comp(instanceName)
    origin = def_parser.components.comp_dict[instanceName].placed
    orientation = def_parser.components.comp_dict[instanceName].orient
    cellType = def_parser.components.comp_dict[instanceName].macro
    cellWidth= lef_parser.macro_dict[cellType].info['SIZE'][0] * l2d
    cellHeight = lef_parser.macro_dict[cellType].info['SIZE'][1] * l2d
    
    pinObject = lef_parser.macro_dict[cellType].pin_dict[pinName]
    port_info = pinObject.info['PORT'].info['LAYER'][0]
    
    if(orientation == 'N'):
        for shape in port_info.shapes:
            llx = shape.points[0][0]*l2d + origin[0]
            lly = shape.points[0][1]*l2d + origin[1]
            urx = shape.points[1][0]*l2d + origin[0]
            ury = shape.points[1][1]*l2d + origin[1]
            ll = (llx, lly)
            ur = (urx, ury)
            listOfPinRects.append((ll, ur))
            
    if(orientation == 'S'):
        # consider origin to be top right corner
        rotatedOrigin = (origin[0]+cellWidth, origin[1] + cellHeight)
        for shape in port_info.shapes:
            llx = rotatedOrigin[0] - shape.points[1][0]*l2d
            lly = rotatedOrigin[1] - shape.points[1][1]*l2d
            urx = rotatedOrigin[0] - shape.points[0][0]*l2d 
            ury = rotatedOrigin[1] - shape.points[0][1]*l2d
            ll = (llx, lly)
            ur = (urx, ury)
            listOfPinRects.append((ll, ur))
    
    if(orientation == 'W'):
        # consider origin to be bottom right corner
        rotatedOrigin = (origin[0]+cellHeight, origin[1])
        for shape in port_info.shapes:
            lrx = rotatedOrigin[0] - shape.points[0][1]*l2d
            lry = rotatedOrigin[1] + shape.points[0][0]*l2d
            ulx = rotatedOrigin[0] - shape.points[1][1]*l2d 
            uly = rotatedOrigin[1] + shape.points[1][0]*l2d
            
            ll = (ulx, lry)
            ur = (lrx, uly)
            listOfPinRects.append((ll, ur))
            
    if(orientation == 'E'):
        # consider origin to be top left corner
        rotatedOrigin = (origin[0], origin[1]+cellWidth)
        for shape in port_info.shapes:
            ulx = rotatedOrigin[0] + shape.points[0][1]*l2d
            uly = rotatedOrigin[1] - shape.points[0][0]*l2d
            lrx = rotatedOrigin[0] + shape.points[1][1]*l2d 
            lry = rotatedOrigin[1] - shape.points[1][0]*l2d
            
            ll = (ulx, lry)
            ur = (lrx, uly)
            listOfPinRects.append((ll, ur))
            
    if(orientation == 'FN'):
        # consider origin to be bottom right corner
        rotatedOrigin = (origin[0]+cellWidth, origin[1])
        for shape in port_info.shapes:
            lrx = rotatedOrigin[0] - shape.points[0][0]*l2d 
            lry = rotatedOrigin[1] + shape.points[0][1]*l2d
            ulx = rotatedOrigin[0] - shape.points[1][0]*l2d
            uly = rotatedOrigin[1] + shape.points[1][1]*l2d  
            
            ll = (ulx, lry)
            ur = (lrx, uly)
            listOfPinRects.append((ll, ur))
            
    if(orientation == 'FS'):
        # consider origin to be upper left corner
        rotatedOrigin = (origin[0], origin[1]+cellHeight)
        for shape in port_info.shapes:
            lrx = rotatedOrigin[0] + shape.points[1][0]*l2d 
            lry = rotatedOrigin[1] - shape.points[1][1]*l2d
            ulx = rotatedOrigin[0] + shape.points[0][0]*l2d
            uly = rotatedOrigin[1] - shape.points[0][1]*l2d  
            
            ll = (ulx, lry)
            ur = (lrx, uly)
            listOfPinRects.append((ll, ur))
            
    if(orientation == 'FW'):
        # consider origin to be bottom left corner
        rotatedOrigin = (origin[0], origin[1])
        for shape in port_info.shapes:
            llx = rotatedOrigin[0] + shape.points[0][1]*l2d 
            lly = rotatedOrigin[1] + shape.points[0][0]*l2d
            urx = rotatedOrigin[0] + shape.points[1][1]*l2d
            ury = rotatedOrigin[1] + shape.points[1][0]*l2d  
            
            ll = (llx, lly)
            ur = (urx, ury)
            listOfPinRects.append((ll, ur))
            
    if(orientation == 'FE'):
        # consider origin to be top right corner
        rotatedOrigin = (origin[0] + cellHeight, origin[1] + cellWidth)
        for shape in port_info.shapes:
            llx = rotatedOrigin[0] - shape.points[1][1]*l2d 
            lly = rotatedOrigin[1] - shape.points[1][0]*l2d
            urx = rotatedOrigin[0] - shape.points[0][1]*l2d
            ury = rotatedOrigin[1] - shape.points[0][0]*l2d  
            
            ll = (llx, lly)
            ur = (urx, ury)
            listOfPinRects.append((ll, ur))
    
# test the getPinLocationFunction
listOfLocations = []
getPinLocation('NOR2X1_1', 'A', listOfLocations)

def get_resistance(points, points2, segment):
    layer_name = segment
    if(points != points2):
        rPerSquare = lef_parser.layer_dict[layer_name].resistance[1]
        width = lef_parser.layer_dict[layer_name].width
        length = abs(points[0] - points2[1]) + abs(points[0] - points2[1]) 
        resistance = length * rPerSquare / width
        return resistance
    #handelling a VIA, is there's only one coordinate for a segment then it's a via
#    else:
#        resistance = lef_parser.via_dict[layer_name].resistance[1]
    
    
def get_capacitance(points, points2, segment):
    layer_name = segment
    if(points != points2):
        cPerSquare = lef_parser.layer_dict[layer_name].capacitance[1]
        width = lef_parser.layer_dict[layer_name].width
        length = abs(points[0] - points2[1]) + abs(points[0] - points2[1]) 
        if(lef_parser.layer_dict[layer_name].edge_cap != None):
            edgeCapacitance = lef_parser.layer_dict[layer_name].edge_cap
        else:
            edgeCapacitance = 0
        capacitance = length * cPerSquare * width + edgeCapacitance * length
        return capacitance
    #handelling a VIA
#    else:
#        capacitance = lef_parser.via_dict[layer_name].capacitance[1]
    
    

def checkPinsTable(point, layer, pinsTable): 
    flag= "new"
    for j in pinsTable:
        if(layer == j[3]):
                if(str(type(j[0][0])) != "<class 'int'>"):
                    for f in j[0]:    
                        if(str(type(f[0])) != "<class 'int'>"):
                            if ((f[0][0] <= float(point[0]) <= f[1][0]) and (f[0][1] <= float(point[1]) <= f[1][1])):
                                flag= j
                            else: flag= "new"
                        else: 
                            if(point[0]==f[0] and point[1]==f[1]):
                                    flag= j
                            else: flag= "new"
                else:
                    if(point[0]==j[0][0] and point[1]==j[0][1]):
                            flag= j
                    else: flag= "new"
        else: 
            flag= "new"
    return flag

segmentsList = []
bigTable={}

for net in def_parser.nets:
    conList = []
    pinsTable=[]
    # generate the conn data structure for conn section
    for con in net.comp_pin:
        #check if pin is *P
        current_pin = []
        locationsOfCurrentPin = []
        if(con[0] == "PIN"):
            current_pin.append("*P")
            current_pin.append(con[1])
            x = def_parser.pins.get_pin(con[1])
            if(x.direction == "INPUT"):
                current_pin.append("I")
            else:
                current_pin.append("O")
                
            # these are used for the pinsTable
            pinLocation = def_parser.pins.pin_dict[con[1]].placed
            metalLayer = def_parser.pins.pin_dict[con[1]].layer.name
            locationsOfCurrentPin.append(pinLocation)
            
            
        else:
            current_pin.append("*I")
            current_pin.append(con[0]+":"+con[1]) 
            cell_type = def_parser.components.comp_dict[con[0]].macro
            direction = lef_parser.macro_dict[cell_type].pin_dict[con[1]].info["DIRECTION"]
            if(direction == "INPUT"):
                current_pin.append("I")
            else:
                current_pin.append("O")
            
            #this is used for the pins table
            getPinLocation(con[0], con[1], locationsOfCurrentPin)
            metalLayerInfo = lef_parser.macro_dict[cell_type].pin_dict[con[1]].info
            metalLayer = metalLayerInfo['PORT'].info['LAYER'][0].name
       
        # we addpend list of pin locations - cellName - pinName - metalLayer
        pinsTable.append((locationsOfCurrentPin, con[0], con[1],metalLayer))
        conList.append(current_pin)

    counter = 1
    
    for segment in net.routed:
        node = []
        c2=0
        for i in segment.points:
            flag=checkPinsTable(i, segment.layer, pinsTable)
            if( flag != "new"):
                node = flag
                #TODO: ADD HANDLING NODES THAT ALREADY EXIST
            else:
                node = []
                if(len(segment.points)>1):
                    node.append(i)
                    node.append(str(net.name) )
                    node.append(":" +  str(counter))
                    node.append(str(segment.layer))
                    counter += 1
                    c2 += 1
                    if( c2>1 ):
                        seg=[]
                        prev = pinsTable[len(pinsTable)-1]
                        resistance = get_resistance(prev[0], i, segment.layer)
                        capacitance = get_capacitance(prev[0], i, segment.layer)
                        seg.append(prev[1]+prev[2])
                        seg.append(node[1] + node[2])
                        seg.append(resistance)
                        seg.append(capacitance)
                        segmentsList.append(seg)
                    pinsTable.append(node)
                    
                    
                    if((segment.end_via != ';' and segment.end_via != None) and i ==segment.points[len(segment.points)-1]):  #Handeling Vias at the end of segments 
                        node = []
                        seg=[]
                        node.append(i)
                        node.append(str(net.name))
                        node.append(":" +  str(counter))
                        if(segment.end_via[len(segment.end_via)-1]==';'):
                            segment.end_via = segment.end_via.replace(';','')
                        node.append(str(segment.end_via))
                        counter += 1
                        resistance = get_resistance(i, i, segment.end_via)
                        capacitance = get_capacitance(i, i, segment.end_via)
                        seg.append(node[1] +node[2])
                        seg.append(node[1] +node[2])
                        seg.append(resistance)
                        seg.append(capacitance)
                        segmentsList.append(seg)
                        pinsTable.append(node)
                       
                elif(len(segment.points) == 1):
                    seg=[]
                    node.append(i)
                    node.append(str(net.name))
                    node.append(":" +  str(counter))
                    node.append(str(segment.end_via))
                    counter += 1
                    resistance = get_resistance(i, i, segment.end_via)
                    capacitance = get_capacitance(i, i, segment.end_via)
                    seg.append(node[1] +node[2])
                    seg.append(node[1] +node[2])
                    seg.append(resistance)
                    seg.append(capacitance)
                    segmentsList.append(seg)
                    pinsTable.append(node)
                    
                    

                    
    bigTable[net.name] = pinsTable
      
        
 


    
        
        
        
    """
    newDictionary = {}
    newDictionary['conn'] = conList
    newDictionary['segments'] = segmentsList
    newDictionary['maxC'] = 95
    """    
    
    
    
    

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




