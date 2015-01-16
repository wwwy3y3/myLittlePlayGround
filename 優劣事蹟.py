# coding= utf8
import zipfile
from collections import Counter
from lxml import etree
import re
import os, os.path

blacklist= [u'偵查佐', u'大隊部', u'員會同', u'人次。', u'優點：', u'，警員', u'、警員']
goodlist= Counter()
badlist= Counter()

def get_xml_tree(xml_string):
   return etree.fromstring(xml_string)

def get_word_xml(docx_filename):
   with open(docx_filename) as f:
      zip = zipfile.ZipFile(f)
      xml_content = zip.read('word/document.xml')
   return xml_content

for root, _, files in os.walk('./files/12'):
	for f in files:
		fullpath = os.path.join(root, f)
		tree= get_xml_tree(get_word_xml(fullpath))
		regexp= re.compile(r'\w')
		c= goodlist
		for word in tree.xpath("//text()"):
			if word.find(u'缺點') >= 0:
				c= badlist
			if len(word) == 3 and regexp.search(word) is None and not word in blacklist:
				c[word] += 1

print "good"
for item,val in goodlist.most_common():
	print item.encode('utf8'), val

print "bad"
for item,val in badlist.most_common():
	print item.encode('utf8'), val
