import tagsignature
import tagsignaturelist


print "-----------I am doing test class TagSignature----------------\n"

tagsi = tagsignature.TagSignature()
tagsi.loadTagSignatureFromXML('tagsignature.in.xml')
tagsi.saveTagSignatureToXML('tagsignature.out.xml')


print "-------------I am doing test class TagSignatureList! ---------\n"
tagsilist = tagsignaturelist.TagSignatureList()
tagsilist.loadTagSignatureListFromXML('tagsignaturelist.in.xml')
tagsilist.saveTagSignatureListToXML('tagsignaturelist.out.xml')



""" I am doing test for readline_tag"""
tagsilist.readTagSignatureListFromFile('TagSignature_file.txt')

