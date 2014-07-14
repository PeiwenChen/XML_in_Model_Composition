
""" Author: Peiwen Chen 
    Date: July 10th, 2014"""



from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

class Port:
    def __init__(self, pname = [], ptype = [], description = []):
	self.PortName = pname   
	self.Type = ptype    
	self.Description = description 
	


class TagSignature:
    def __init__(self, tagtype=None, nametag = [], inputports = [], outputports = []):
        " self.* are the values stored in xml "
	self.tagtype = tagtype
	self.nametag = nametag  
	self.inputPorts = inputports 
	self.outputPorts = outputports 

    def loadTagSignatureFromXML(self, xmldir):
	document = ElementTree.parse(xmldir)

	self.tagtype = document.find('TagType').text
	self.nametag = document.find('NameTag').text.split(',')

	ilist = []
	for port in document.findall('Inputs/Port'): 
	    ### create a new Port 
            newport = Port(port.find('PortName').text.split(','), port.find('Type').text.split(','), port.find('Description').text.split(','))
	    ilist.append(newport)
	self.inputPorts = ilist 
	
	olist = []
	for port in document.findall('Outputs/Port'):
	     port2add = Port(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
	     olist.append(port2add)
	self.outputPorts = olist

    def saveTagSignatureToXML(self, xmldir):
	tagsignature = Element('TagSignature')
	tagtype = SubElement(tagsignature, 'TagType')  
	tagtype.text = str(self.tagtype)  
	nametag = SubElement(tagsignature, 'NameTag')
	nametag.text = str(self.nametag)   
	
	### Inputs Ports
	inputs = SubElement(tagsignature, 'Inputs')
	for port in self.inputPorts: ### for each port in the inputs Port List
	    inputport = SubElement(inputs, 'Port')  
	    inputportname = SubElement(inputport, 'PortName')
	    inputportname.text = str(port.PortName) ###add PortName value
	    inputporttype = SubElement(inputport, 'Type')
	    inputporttype.text = str(port.Type) ###add Type value
	    inputportdes = SubElement(inputport, 'Description')
	    inputportdes.text = str(port.Description) ###add des value
	
	### Outputs Ports
	outputs = SubElement(tagsignature, 'Outputs')
	for port in self.outputPorts: ### for each port in the inputs Port List
	    outputport = SubElement(outputs, 'Port')  
	    outputportname = SubElement(outputport, 'PortName')
	    outputportname.text = str(port.PortName) ###add PortName value
	    outputporttype = SubElement(outputport, 'Type')
	    outputporttype.text = str(port.Type) ###add Type value
	    outputportdes = SubElement(outputport, 'Description')
	    outputportdes.text = str(port.Description) ###add des value
	
	###write into xml file
	output_file = open(xmldir, 'w')
	output_file.write('<?xml version = "1.0"?>')
	output_file.write(ElementTree.tostring(tagsignature))
	output_file.close()

