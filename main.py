     # -*- coding: utf-8 -*-
import sys
sys.path.insert(0, './lef_def_parser')

from def_parser import *
from lef_parser import *
import codecs
from collections import defaultdict
import datetime

#in order to print Date in the SPEF file
now = datetime.datetime.now()
    
def remap_names():  #name mapping method that reduces all net names in order to minimize the SPEF size
    name_counter = 0
    map_of_names = []
    for key in def_parser.nets.net_dict:
        new_name = []
        new_name.append(def_parser.nets.net_dict[key].name)
        def_parser.nets.net_dict[key].name = "*" + str(name_counter)
        new_name.append(def_parser.nets.net_dict[key].name)
        name_counter += 1
        map_of_names.append(new_name)
    return(map_of_names)


def printNameMap(map_of_names): #printing the keys of the name map into the SPEF file 
    f.write('*NAME_MAP\n')
    for entry in map_of_names:
        f.write(entry[1] + " " + entry[0] + "\n")
    f.write("\n")

# A method that takes an instance and a pin and returns a list of all
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

def getViaType(via): #method to extract the via type by its name fromt the lef file
    firstLayer = lef_parser.via_dict[via].layers[0]
    secondLayer = lef_parser.via_dict[via].layers[1]
    thirdLayer = lef_parser.via_dict[via].layers[2]
    
    if(firstLayer.name[0:3] != 'met'):
        via_type = firstLayer.name
    if(secondLayer.name[0:3] != 'met'):
        via_type = secondLayer.name
    
    if(thirdLayer.name[0:3] != 'met'):
        via_type = thirdLayer.name
    return via_type
                 
   
#method to get the resistance of a certain segment (wire of via) using its length (distance between 2 points) and info from the lef file
def get_resistance_modified(point1, point2, layer_name, via_type): #point is a list of (x, y)
    if(point1 == point2): #we have a via
        return lef_parser.layer_dict[via_type].resistance
    else: #we have a wire
        rPerSquare = lef_parser.layer_dict[layer_name].resistance[1]
        width = lef_parser.layer_dict[layer_name].width/1000 #width in microns
        wire_len = (abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]))/100 #length in microns
        resistance = wire_len * rPerSquare / width #R in ohms
        return resistance

#method to get the capacitance of a certain segment (wire of via) using its length (distance between 2 points) and info from the lef file
def get_capacitance_modified(point1, point2, layer_name, via_type): #point is a list of (x, y)
    if(point1 == point2): #we have a via
        if(lef_parser.layer_dict[via_type].edge_cap == None):
            return 2.5e-5 #capacitance in pF
        else:
            return lef_parser.layer_dict[via_type].edge_cap
    else: #we have a wire
        cPerSquare = lef_parser.layer_dict[layer_name].capacitance[1]
        width = lef_parser.layer_dict[layer_name].width/1000 #width in microns
        length = (abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]))/100 #length in microns
        if(lef_parser.layer_dict[layer_name].edge_cap != None):
            edgeCapacitance = lef_parser.layer_dict[layer_name].edge_cap
        else:
            edgeCapacitance = 0
        capacitance = length * cPerSquare * width + edgeCapacitance * length  #capactiance in pF
        return capacitance
    

#method to look for intersetions between segment nodes in order to decide on creating a new node or add to the existing capacitance
def checkPinsTable(point, layer, pinsTable): 
    flag= "new"
    for j in pinsTable:
        if(layer == j[3]):
                if(str(type(j[0][0])) != "<class 'int'>"):
                    for f in j[0]:    
                        if(str(type(f[0])) != "<class 'int'>"):
                            if ((f[0][0] - 5 <= float(point[0]) <= f[1][0] + 5) and (f[0][1]  - 5<= float(point[1]) <= f[1][1] + 5)):
                                flag= j
                                return flag
                            else: flag= "new"
                        else: 
                            if((f[0] - 5 <=point[0]<=f[0] + 5) and (f[1] - 5 <= point[1] <= f[1] +5)):
                                    flag= j
                                    return flag
                            else: flag= "new"
                else:
                    if(point[0]==j[0][0] and point[1]==j[0][1]):
                            flag= j
                            return flag
                    else: flag= "new"
        else: 
            flag= "new"
    return flag

#method to print all nets in the net dictionay
def printSPEFNets(netsDict):
    for key, value in netsDict.items():
        printNet(netsDict, key)


#method to print a particular net into SPEF format 
def printNet(netsDict, wireName):
    var=('*D_NET'+" "+ wireName+" "+ str(netsDict[wireName]['maxC']))
    f.write(var+'\n')
    var=('*CONN')
    f.write(var+'\n')
    for eachConnection in netsDict[wireName]['conn']:
        var=(eachConnection[0]+" "+ eachConnection[1]+" "+ eachConnection[2])
        f.write(var+'\n')
    
    
    var=('*CAP')
    f.write(var+'\n')
    
    
    for key,value in bigCapacitanceTable[wireName].items():
        var=(str(capCounter[0]) +" "+ str(key) +" "+ str(value))
        f.write(var+'\n')
        capCounter[0] += 1
        
    var=('*RES')
    f.write(var+'\n')
    for eachSegment in netsDict[wireName]['segments']:
        var=(str(resCounter[0])+" "+ str(eachSegment[0])+" "+ str(eachSegment[1])+" "+ str(eachSegment[2]))
        f.write(var+'\n')
        resCounter[0] += 1
    var=('*END\n')
    f.write(var+'\n')
    
    
    
    
    
    
# main starts here:
    
    
# l2d is the conversion factor between the scale in LEF and DEF
# we need a function to generalize this for any two lef and def files
l2d = 100
    
listOfLocations = []
pinsTable = []
segmentsList = []
bigPinsTable={}
bigSegmentsTable = {}
bigCapacitanceTable = {}
netsDict = {}

#run from terminal section

if(len(sys.argv) < 3):
    sys.exit("Arguments should be passed: python <script_name>.py <path/lef_name>.lef <path/def_name>.def")
elif(sys.argv[1].find(".lef") == -1 or sys.argv[2].find(".def") == -1):
    sys.exit("Arguments should be passed: python <script_name>.py <path/lef_name>.lef <path/def_name>.def")
else:
    lef_file_name = sys.argv[1]
    def_file_name = sys.argv[2]
    

print("Input LEF file name")
#lefPath = input()

# We had to modify the lef parser to ignore the second parameter for the offset
# since our files provide only 1 value
lef_parser = LefParser(lef_file_name)
lef_parser.parse()

print("Input DEF file name")
#defPath = input()
def_parser = DefParser(def_file_name)
def_parser.parse()

#creation of the name map
map_of_names = remap_names()

for net in def_parser.nets:
#traversing over all nets in the def file to extract segments infromation
    conList = []
    pinsTable=[]
    segmentsList = []
    # generate the conn data structure for conn section
    for con in net.comp_pin:
        #check if pin is (*P) an external input/output pin
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
            
            
        else: #it is an internal pin, check for input or output
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
    
    # the value will be incremented if more than 1 segment end at the same node
    currentNodeList = {}
    for segment in net.routed:
    #traversing all segments in a certain net to get all their information
        for it in range (len(segment.points)):
        ##traversing all points in a certain segment, classifyng them as starting and ending points and 
        #checking for their existence in the pinstable, using checkPinsTable method 
            last = 0
            if(it < (len(segment.points) - 1)):
                spoint = segment.points[it]
                epoint = segment.points[it+1]
            else: #last point in the line (either via or no via)
                spoint = segment.points[it]
                epoint = segment.points[it]
                last = 1
                #if we are at the last point and there is no via, then ignore the point
                #as it has already been considered with the previous point
                if((segment.end_via == ';' or segment.end_via == None)):
                    continue
                
            sflag=checkPinsTable(spoint, segment.layer, pinsTable)
            
            if( sflag != "new"):
                snode = sflag
            else:
                snode = []
                snode.append(spoint)
                snode.append(str(net.name) )
                snode.append(str(counter))
                snode.append(str(segment.layer))
                counter += 1
                pinsTable.append(snode)
                
            
            if ((last) and  (segment.end_via != ';' and segment.end_via != None)):
            #special handeling for vias to tget the via types through the via name
                myVia = segment.end_via
                if(myVia[-1] == ';'):
                    myVia = myVia[0:-1]
                
                firstLayer = lef_parser.via_dict[myVia].layers[0]
                secondLayer = lef_parser.via_dict[myVia].layers[1]
                thirdLayer = lef_parser.via_dict[myVia].layers[2]
                
                s = firstLayer.name[0:3];
                if(firstLayer.name[0:3] != 'met'):
                    first = secondLayer.name
                    second = thirdLayer.name
                if(secondLayer.name[0:3] != 'met'):
                    first = firstLayer.name
                    second = thirdLayer.name
                
                if(thirdLayer.name[0:3] != 'met'):
                    first = firstLayer.name
                    second = secondLayer.name
                    
                if(first == segment.layer):
                    choose = 2  # choose second layer in case of creating end node
                    eflag=checkPinsTable(epoint, second, pinsTable)
                else:
                    choose = 1  # choose first layer in case of creating end node
                    eflag=checkPinsTable(epoint, first, pinsTable)
                    
            else:
                eflag=checkPinsTable(epoint, segment.layer, pinsTable)
                
            if( eflag != "new"):
                enode = eflag
            else:
                enode = []
                enode.append(epoint)
                enode.append(str(net.name) )
                enode.append(str(counter))
                if(last):
                    # if it is a VIA and starting point was on second layer
                    if(choose == 1):
                        enode.append(first)
                    else:
                        enode.append(second)
                else:
                    enode.append(str(segment.layer))
                counter += 1
                pinsTable.append(enode)
              
            seg=[]
            
            #TODO: pass segment.endvia to function to be used if 2 points are equal
            
            if(segment.end_via != None) & (segment.end_via != ';') :
                via_type = getViaType(segment.end_via)
                resistance = get_resistance_modified(spoint, epoint, segment.layer, via_type)
                capacitance = get_capacitance_modified(spoint, epoint, segment.layer, via_type)
            else:
                resistance = get_resistance_modified(spoint, epoint, segment.layer, 'via1') # dummy via
                capacitance = get_capacitance_modified(spoint, epoint, segment.layer, 'via1') #dummy via
            
            # the name of the current node
            currentNodeName = str(enode[1]) + ':' + str(enode[2])
            # put the capacitance for the current node.
            exists = 0
            for key in currentNodeList:
                if(currentNodeName == key):
                    exists = 1
                    break
            if(exists == 1): #adding the capacitance to the previous capacitances in an existing node
                currentNodeList[currentNodeName] += capacitance
            else: #assigning the new node capacitance
                currentNodeList[currentNodeName] = capacitance
            
            if(snode[1] != 'PIN'):
                seg.append(snode[1]  + ':' + snode[2])
            else:
                seg.append(snode[2])
            if(enode[1] != 'PIN'): 
                seg.append(enode[1]  + ':' + enode[2])
            else:
                seg.append(enode[2])
            seg.append(resistance)
            seg.append(capacitance)
            segmentsList.append(seg)
    
    
    ##appending the pins, segments resistances and node capacitances into the big table dictionaries that will
    #be used for printing the final SPEF             
    bigPinsTable[net.name] = pinsTable
    bigSegmentsTable[net.name] = segmentsList
    bigCapacitanceTable[net.name] = currentNodeList
    
    
    sumC=0 
    lists= {}  
    for k in currentNodeList:
        sumC+=currentNodeList[k]
    lists["conn"]=conList
    lists['maxC']=sumC
    lists['segments']=segmentsList
    netsDict[net.name]= lists


#method for creating the header of the SPEF file 
def printSPEFHeader():
    f.write('*SPEF "IEEE 1481-1998"'+'\n')
    f.write('*DESIGN "'+ def_parser.design_name + '"'+'\n')
    f.write('*DATE "' + now.strftime("%a %b %d %H:%M:%S %Y") + '"\n')
    f.write('*VENDOR "ISPD 2013 Contest"\n')
    f.write('*PROGRAM "Benchmark Parasitic Generator"\n')
    f.write('*VERSION "0.0"\n')
    f.write('*DESIGN_FLOW "PIN_CAP NONE"'+'\n')
    f.write('*DIVIDER ' + def_parser.dividerchar[1] +'\n')
    f.write('*DELIMITER :' + '\n')
    f.write('*BUS_DELIMITER ' + def_parser.busbitchars[1:3] +'\n')
    f.write('*T_UNIT 1.00000 NS' +'\n')
    f.write('*C_UNIT 1.00000 PF'+'\n')
    f.write('*R_UNIT 1.00000 OHM'+'\n')
    f.write('*L_UNIT 1.00000 HENRY'+'\n')
    f.write('\n'+'\n')


print("RC Extraction is done")

 
#writing into SPEF file
capCounter = {}
capCounter[0] = 0
resCounter = {}
resCounter[0] = 0
f = open("RC_parasitics.spef","w+")
print("Start writing SPEF file")
printSPEFHeader()
printNameMap(map_of_names)
printSPEFNets(netsDict)  
f.close()
content = codecs.open('RC_parasitics.spef', encoding='utf-8').read()
newContent = content.replace('<', '[')
newContent = newContent.replace('>', ']')
newContent = newContent.replace('\n', '')

f =  open("RC_parasitics.spef","w+")
f.write(newContent)

print("Writing SPEF is done")

