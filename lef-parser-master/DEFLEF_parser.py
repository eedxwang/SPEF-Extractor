# -*- coding: utf-8 -*-
import def_parser
import lef_parser

path = "./libraries/Nangate/NangateOpenCellLibrary.lef"
lef_parser = LefParser(path)
lef_parser.parse()


read_path = "./libraries/DEF/c1908.def"
def_parser = DefParser(read_path)
def_parser.parse()

netsDict = {}

for pin in def_parser.pins:
    print(pin)
    

conList = []
for net in def_parser.nets:
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
