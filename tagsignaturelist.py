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
	self.totid = 0

    def addTagSignature(self, tagsi):
    " add tagsignature into the list"
    self.tagSignatureList[self.totid] = tagsi 
    totid += 1

    def removeTagSignatureByValue(self, tagsi):
    " remove tagsignature by value from the list "
    tmplist = {} 
    tmplist = {key: value for key, value in self.modelDescriptionList.items()
        if value != tagsi} ## how to compare? need re-visit!
    self.tagSignatureList = templist

    def removeTagSignatureByID(self, k):
    "remove tagsignature by ID from the list"
    self.tagSignatureList.pop(k, None)

    def findTagSignatureByID(self, tagsi):
    " find the tagsignature id(the key for dict) in the list"
    for key, value in self.tagSignatureList.items():
	# only check tagtype and nametag "
	if(tagsi.tagtype == value.tagtype) &&(tagsi.nametag == value.nametag)):
	    return k
    return 0 # not found	
		
    def loadTagSignatureListFromXML(self, xmldir):
	tslistdoc = ElementTree.parse(xmldir)
	for ts in tslistdoc.findall('TagSignature'):
            newts = tagsignature.TagSignature() ### create a new TagSignature
	    newts.tagtype = ts.find('TagType').text
	    newts.nametag = ts.find('NameTag').text.split(',')
	
	    newts.inputPorts = []
	    for port in ts.findall('Inputs/Port'):  
                port2add = tagsignature.Port(port.find('PortName').text.split(','), port.find('Type').text.split(','), port.find('Description').text.split(','))
	        newts.inputPorts.append(port2add)
	
	    newts.outputPorts = []
	    for port in ts.findall('Outputs/Port'):
	         port2add = tagsignature.Port(port.find('PortName').text.split(','), port.find('Type').text.split(','), port.find('Description').text.split(','))
	         newts.outputPorts.append(port2add) 
	    
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
		nametag.text = str(','.join(ts.nametag))   
	    ### Inputs Ports
	    inputs = SubElement(tss, 'Inputs')
	    for port in ts.inputPorts: 
		inputport = SubElement(inputs, 'Port') ###create a new Port 
	        inputportname = SubElement(inputport, 'PortName')
		if (port.PortName):
		    inputportname.text = str(','.join(port.PortName))
	        inputporttype = SubElement(inputport, 'Type')
		if (port.Type):
		    inputporttype.text = str(','.join(port.Type))
	        inputportdes = SubElement(inputport, 'Description')
		if (port.Description):
		    inputportdes.text = str(','.join(port.Description))
	
	    ### Outputs Ports
	    outputs = SubElement(tss, 'Outputs')
	    for port in ts.outputPorts: 
	        outputport = SubElement(outputs, 'Port')  
	        outputportname = SubElement(outputport, 'PortName')
		if (port.PortName):
		    outputportname.text = str(','.join(port.PortName)) 
	        outputporttype = SubElement(outputport, 'Type')
		if (port.Type):
		    outputporttype.text = str(','.join(port.Type))
	        outputportdes = SubElement(outputport, 'Description')
		if (port.Description):
		    outputportdes.text = str(','.join(port.Description)) 
	
	###write into xml file
	output_file = open(xmldir, 'w')
	output_file.write('<?xml version = "1.0"?>')
	output_file.write(ElementTree.tostring(tslist))
	output_file.close()

    """ read TagSignature-file.txt 
    NameTag | NameTag | Input PortName | Output PortName to a tagsignaturelist"""
    def readTagSignatureFromLine(self, totid, line):
        linelist = line.split('|')
        tagsig = tagsignature.TagSignature()
	if (len(linelist) != 4):
	    return None
    ### this is a tag line 
	nametaglist = [] ### init before user
	nametaglist.append(linelist[0])
	nametaglist.append(linelist[1])
        tagsig.nametag = nametaglist
	

	tagsig.outputPorts = []  ### init before use
	for oport in linelist[2].split(): ### ports split with ' ' 
	    newport = tagsignature.Port()
	    newport.PortName = []  ### init before use
	    for name in oport.split('_'): ### portname split with '_' 
		newport.PortName.append(name)  ### port name 
            tagsig.outputPorts.append(newport)

        tagsig.inputPorts = []  ### init before use
	for iport in linelist[3].split(): ### ports split with ' ' 
	    newport = tagsignature.Port()
	    newport.PortName = []  ### init before use
	    for name in iport.split('_'): ### portname split with '_' 
		newport.PortName.append(name)  ### port name 
            tagsig.inputPorts.append(newport)

	return tagsig
    
    def readTagSignatureListFromFile(self, filedir):
        "parse all lines, store in list, and save to XML file"
        totid = 0
        with open(filedir) as f:
	    for line in f:
	        linetagsig = self.readTagSignatureFromLine(totid, line)
		if (linetagsig):
		    self.tagSignatureList[totid] = linetagsig ### add key-value pair into dict
		    totid += 1


        print "test if read is correct totid = " + str(totid)
	self.saveTagSignatureListToXML('readfile.xml')
    

