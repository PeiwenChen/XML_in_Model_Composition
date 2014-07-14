""" Author: Peiwen Chen 
    Date: July 10th, 2014"""



from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import tagsignature

class TagSignatureList:
    "list of TagSignature"
    def __init__(self, tslist = {}):
	self.tagSignatureList = tslist ### dict: {'1': signature1, '2':signature2}

    def loadTagSignatureListFromXML(self, xmldir):
	tslistdoc = ElementTree.parse(xmldir)
	for ts in tslistdoc.findall('TagSignature'):
            newts = tagsignature.TagSignature() ### create a new TagSignature
	    newts.tagtype = ts.find('TagType').text
	    newts.nametag = ts.find('NameTag').text.split(',')
	
	    inlist = []
	    for port in ts.findall('Inputs/Port'):  
                port2add = tagsignature.Port(port.find('PortName').text.split(','), port.find('Type').text.split(','), port.find('Description').text.split(','))
	        inlist.append(port2add)
            newts.inputPorts = inlist 
	
	    olist = []
	    for port in ts.findall('Outputs/Port'):
	         port2add = tagsignature.Port(port.find('PortName').text.split(','), port.find('Type').text.split(','), port.find('Description').text.split(','))
	         olist.append(port2add) 
            newts.outputPorts = olist	
	    
	    self.tagSignatureList[ts.attrib['tagid']] = newts  ###add new signature to the dictory, id is totid


    def saveTagSignatureListToXML(self, xmldir):	
	tslist = Element('TagSignatureList')
        for tid, ts in self.tagSignatureList.items():  ### for all valus in dict 
            tss = SubElement(tslist, 'TagSignature', tagid = str(tid)) ### create a new TagSignature Node

	    tagtype = SubElement(tss, 'TagType') 
	    if (ts.tagtype):
		tagtype.text = str(ts.tagtype)  
	    nametag = SubElement(tss, 'NameTag')
	    if (ts.nametag):
		nametag.text = str(ts.nametag)   
	
	    ### Inputs Ports
	    inputs = SubElement(tss, 'Inputs')
	    for port in ts.inputPorts: 
		inputport = SubElement(inputs, 'Port') ###create a new Port 
	        inputportname = SubElement(inputport, 'PortName')
		if (port.PortName):
		    inputportname.text = str(port.PortName)
	        inputporttype = SubElement(inputport, 'Type')
		if (port.Type):
		    inputporttype.text = str(port.Type)
	        inputportdes = SubElement(inputport, 'Description')
		if (port.Description):
		    inputportdes.text = str(port.Description) 
	
	    ### Outputs Ports
	    outputs = SubElement(tss, 'Outputs')
	    for port in ts.outputPorts: 
	        outputport = SubElement(outputs, 'Port')  
	        outputportname = SubElement(outputport, 'PortName')
		if (port.PortName):
		    outputportname.text = str(port.PortName) 
	        outputporttype = SubElement(outputport, 'Type')
		if (port.Type):
		    outputporttype.text = str(port.Type)
	        outputportdes = SubElement(outputport, 'Description')
		if (port.Description):
		    outputportdes.text = str(port.Description) 
	
	###write into xml file
	output_file = open(xmldir, 'w')
	output_file.write('<?xml version = "1.0"?>')
	output_file.write(ElementTree.tostring(tslist))
	output_file.close()

    """ read TagSignature-file.txt 
    NameTag | NameTag | Input PortName | Output PortName to a tagsignaturelist"""

    def readTagSignatureListFromFile(self, filedir):
        "parse all lines, store in list, and save to XML file"
        totid = 0
        with open(filedir) as f:
	    for line in f:
	        linetagsig = self.readTagSignatureFromLine(totid, line)
		if (linetagsig != None):
		    self.tagSignatureList[totid] = linetagsig ### add key-value pair into dict
		    totid += 1


        print "test if read is correct totid = " + str(totid)

	self.saveTagSignatureListToXML('readfile.xml')
    

    def readTagSignatureFromLine(self, totid, line):
        linelist = line.split('|')
        if (len(linelist) != 4):
	    return None
    ### this is a tag line 
	tagsig = tagsignature.TagSignature()
	tagsig.nametag.append(linelist[0])
	tagsig.nametag.append(linelist[1])

	inputportlist = linelist[2].split() ### find all Input Ports
	for inputport in inputportlist:
	    iport = tagsignature.Port()
	    inputportname = inputport.split('_')
	    for name in inputportname:
		iport.PortName.append(name)
	    tagsig.inputPorts.append(iport)

	outputportlist = linelist[3].split() ### find all Input Ports
	for outputport in outputportlist:
	    oport = tagsignature.Port()
	    outputportname = outputport.split('_')
	    for name in outputportname:
		oport.PortName.append(name)
	    tagsig.outputPorts.append(oport)
    
	return tagsig



