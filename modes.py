
"""Author Peiwen Chen 
   Date July 14th, 2014 """
   
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

#parameter is used in model name and input/output parameters
class Item:
	def __init__(self, name = "", itemtype = "", description = ""):
		self.name = name   
		self.itemtype = itemtype    
		self.description = description 
	
#model description has Model Item, inputs/outputs port items, and file items, each has name, type, and description
class ModelDescription:
	def __init__(self, model=None, inputports = [], outputports = [], files = []):
		self.model = model
		self.inputPorts = inputports  ### list of Items
		self.outputPorts = outputports  ### list of Items
		self.files = files   ### list of Items

	def loadModelDescriptionFromXML(self, xmldir):
		document = ElementTree.parse(xmldir)
			
		model_name = document.find('Model').attrib['name']
		model_type = document.find('Model').attrib['type']
		model_description = document.find('Model').attrib['description']
		modelItem = Item(model_name, model_type, model_description)
		self.model = modelItem
		
		self.inputPorts = [] 
		for inputitem in document.findall('Inputs/Port'): 
			### create a new Item 
			newitem = Item(inputitem.find('PortName').text, inputitem.find('Type').text, inputitem.find('Description').text)
			self.inputPorts.append(newitem) 
		
		self.outputPorts = []
		for outputitem in document.findall('Outputs/Port'):
			newitem = Item(outputitem.find('PortName').text, outputitem.find('Type').text, outputitem.find('Description').text)
			self.outputPorts.append(newitem)
			 
		self.files = []
		for fileitem in document.findall('Files/File'):
			newitem = Item(fileitem.attrib['name'], fileitem.attrib['type'], fileitem.attrib['location'])
			self.files.append(newitem)
	
	def saveModelDescriptionToXML(self, xmldir):
		modelDescription = Element('ModelDescription')
		modelItem = SubElement(modelDescription, 'Model', name=str(self.model.name), itemtype=str(self.model.itemtype), description=str(self.model.description))
		
		### Inputs Ports
		inputs = SubElement(modelDescription, 'Inputs')
		for port in self.inputPorts: ### for each port in the inputs Port List
			inputport = SubElement(inputs, 'Port')  
			inputportname = SubElement(inputport, 'PortName')
			inputportname.text = str(port.name) ###add PortName value
			inputporttype = SubElement(inputport, 'Type')
			inputporttype.text = str(port.type) ###add Type value
			inputportdes = SubElement(inputport, 'Description')
			inputportdes.text = str(port.description) ###add des value
		
		### Outputs Ports
		outputs = SubElement(modelDescription, 'Outputs')
		for port in self.outputPorts: ### for each port in the inputs Port List
			outputport = SubElement(outputs, 'Port')  
			outputportname = SubElement(outputport, 'PortName')
			outputportname.text = str(port.name) ###add PortName value
			outputporttype = SubElement(outputport, 'Type')
			outputporttype.text = str(port.type) ###add Type value
			outputportdes = SubElement(outputport, 'Description')
			outputportdes.text = str(port.description) ###add des value
			
		### Outputs Ports		
		files = SubElement(modelDescription, 'Files')
		for fileItem in self.files: ### for each port in the inputs Port List
			file = SubElement(files, 'File', name=fileItem.name, type=fileItem.type, location=fileItem.description)
				
		###write into xml file
		output_file = open(xmldir, 'w')
		output_file.write('<?xml version = "1.0"?>')
		output_file.write(ElementTree.tostring(modelDescription))
		output_file.close()

