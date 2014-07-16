

"""Author Peiwen Chen 
   Date July 14th, 2014 """
   
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import modes

class ModelDescriptionList:
	"list of ModelDescription"
	def __init__(self, mdlist = {}):
		self.modelDescriptionList = mdlist ### dict: {'1': signature1, '2':signature2}
		self.totid = 0 ## this is unique and monotonous increasing, we do not decrease it 
	
	def addModelDescription(self, modeldes):
	    " add modeldescription into the list"
	    self.modelDescriptionList[self.totid] = modeldes
	    totid += 1

	def removeModelDescriptionByValue(self, modeldes):
	    " remove modeldescription by value from the list "
	    tmplist = {} 
	    tmplist = {key: value for key, value in self.modelDescriptionList.items()
		    if value != modeldes} ## how to compare? need re-visit!
	    self.modelDescriptionList = templist

	def removeModelDescriptionByID(self, k):
	    "remove modeldescription by ID from the list"
	    self.modelDescriptionList.pop(k, None)

	def findModelDescriptionID(self, modeldes):
	    " find the modeldes id(the key for dict) in the list"
	    for key, value in self.modelDescriptionList.items():
		# only check model item "
		if(modeldes.model.name == value.name) &&(modeldes.model.itemtype == value.itemtype)):
		    return k
	    return 0 # not found	
		
	def loadModelDescriptionListFromXML(self, xmldir):	
		document = ElementTree.parse(xmldir)
		
		for ts in document.findall('ModelDescription'):		
			modelTemp = modes.ModelDescription()  ##to be saved
			
			model_name = ts.find('Model').attrib['name']
			model_type = ts.find('Model').attrib['type']
			model_description = ts.find('Model').attrib['description']
			modelItem = modes.Item(model_name, model_type, model_description)	
			modelTemp.model = modelItem

			modelTemp.inputPorts = []
			for item in ts.findall('Inputs/Port'): 
				newitem = modes.Item(item.find('PortName').text, item.find('Type').text, item.find('Description').text)
				modelTemp.inputPorts.append(newitem)
			
			modelTemp.outputPorts = []
			for item in ts.findall('Outputs/Port'):
				newitem = modes.Item(item.find('PortName').text, item.find('Type').text, item.find('Description').text)
				modelTemp.outputPorts.append(newitem)
			
			modelTemp.files = []
			for item in ts.findall('Files/File'):				
			    newitem = modes.Item(item.attrib['name'], item.attrib['type'], item.attrib['location'])
			    modelTemp.files.append(newitem)
						
			self.modelDescriptionList[ts.attrib['id']] = modelTemp 
		
	def printModelDescriptionList(self): 	
		for tid,ts in self.modelDescriptionList.items():  
			print('Model:', ts.model.name, ts.model.type, ts.model.description)
			for iport in ts.inputPorts:
				print('inputPort:', iport.name, iport.type, iport.description)
			for oport in ts.outputPorts:
				print('outputPorts:', oport.name, oport.type, oport.description)
			for file in ts.files:
				print('files:', file.name, file.type, file.description)
	
	def saveModelDescriptionListToXML(self, xmldir):
		tslist = Element('ModelDescriptionList')
		for tid,ts in self.modelDescriptionList.items():  ### for all valus in dict 
			modelDescription = SubElement(tslist, 'ModelDescription', id=str(tid)) 
			### create a new ModelDescription Node
			modelItem = SubElement(modelDescription, 'Model', name=str(ts.model.name), itemtype=str(ts.model.itemtype), description=str(ts.model.description))
		
			### Inputs Ports
			inputs = SubElement(modelDescription, 'Inputs')
			for port in ts.inputPorts: ### for each port in the inputs Port List
				inputport = SubElement(inputs, 'Port')  
				inputportname = SubElement(inputport, 'PortName')
				inputportname.text = str(port.name) ###add PortName value
				inputporttype = SubElement(inputport, 'Type')
				inputporttype.text = str(port.itemtype) ###add Type value
				inputportdes = SubElement(inputport, 'Description')
				inputportdes.text = str(port.description) ###add des value
			
			### Outputs Ports
			outputs = SubElement(modelDescription, 'Outputs')
			for port in ts.outputPorts: ### for each port in the outputs Port List
				outputport = SubElement(outputs, 'Port')
				outputportname = SubElement(outputport, 'PortName')
				outputportname.text = str(port.name) ###add PortName value
				outputporttype = SubElement(outputport, 'Type')
				outputporttype.text = str(port.itemtype) ###add Type value
				outputportdes = SubElement(outputport, 'Description')
				outputportdes.text = str(port.description) ###add des value
				
			files = SubElement(modelDescription, 'Files')
			for fileItem in ts.files: ### for each port in the inputs Port List
				file = SubElement(files, 'File', name=fileItem.name, itemtype=fileItem.itemtype, location=fileItem.description)
				
					
		###write into xml file
		output_file = open(xmldir, 'w')
		output_file.write('<?xml version = "1.0"?>')
		output_file.write(ElementTree.tostring(tslist))
		output_file.close()

	""" model name | model name | Output PortName | Input PortName """
	def readModelDescriptionFromLine(self, totid, line):
	    linelist = line.split('|')
	    linemodes = modes.ModelDescription()
	    if (len(linelist) != 4):
		return None
	    ### this is a model description line 
	    linemodes.model = modes.Item() 
	    modelname = linelist[0] + "," + linelist[1] ### seperate with ,
	    linemodes.model.name = modelname

	    linemodes.outputPorts = []  ### init before use
	    for oport in linelist[2].split(): ### ports split with ' ' 
		newitem = modes.Item()
		newitem.name = oport  ### init before use
		linemodes.outputPorts.append(newitem)

	    linemodes.inputPorts = []  ### init before use
	    for iport in linelist[3].split(): ### ports split with ' ' 
		newitem = modes.Item()
		newitem.name = iport
		linemodes.inputPorts.append(newitem)

	    return linemodes
    
	def readModelDescriptionListFromFile(self, filedir):
	    "parse all lines, store in list, and save to XML file"
	    totid = 0
	    with open(filedir) as f:
		for line in f:
		    linemodes = self.readModelDescriptionFromLine(totid, line)
		    if (linemodes):
			self.modelDescriptionList[totid] = linemodes ### add key-value pair into dict
			totid += 1
	    print "test if read is correct totid = " + str(totid)
	    self.saveModelDescriptionListToXML('readfile_modes.xml')


