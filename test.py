import tagsignature
import tagsignaturelist
import modes
import modeslist

def testcase1():
    print "----------- testing class TagSignature----------------\n"
    tagsi = tagsignature.TagSignature()
    tagsi.loadTagSignatureFromXML('tagsignature.in.xml')
    tagsi.saveTagSignatureToXML('tagsignature.out.xml')
    print "---------test done  ! -----------------------------------\n"

def testcase2():
    print "------------- testing class TagSignatureList! ---------\n"
    tagsilist = tagsignaturelist.TagSignatureList()
    tagsilist.loadTagSignatureListFromXML('tagsignaturelist.in.xml')
    tagsilist.saveTagSignatureListToXML('tagsignaturelist.out.xml')
    print "------------- test done ! ---------------------------------\n"

def testcase3():
    print "---------------- testing for readline_tag-------------\n"""
    tagsilist = tagsignaturelist.TagSignatureList()
    tagsilist.readTagSignatureListFromFile('TagSignature_file.txt')
    print "----------------test done !------------------------------------\n"

def testcase4():
    print "-------------testing class ModelDescriptionList! ---------\n"
    modeslist = ModelDescriptionList()
    modeslist.loadModelDescriptionListFromXML('modelDescriptionList.in.xml')
    modeslist.saveModelDescriptionListToXML('modelDescriptionList.out.xml')
    print "-------------test done !-----------------------------------------\n"

def testcase5():
    print "------------test ModelDescriptionList read file.txt--------------\n"
    modeslist = ModelDescriptionList()
    modeslist.readModelDescriptionListFromFile('ModelDescription_file.txt')
    print "-------------test done !-------------------------------------------\n"



""" which testcase do you want to run ?"""

