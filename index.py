import json
import codecs
from difflib import SequenceMatcher
import xml.etree.ElementTree as etree

# taken from http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
def similar(a, b):
	return SequenceMatcher(a, b).ratio()

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def main():

	stats = {}
	stats['count'] = 0
	stats['deviation'] = None
	plots = []

	# key_word = raw_input("Enter a keyword to search for:  ")
	# print 'Search an entire book, chapter, or the entire Bible'
	# print '1) Search a book'
	# print '2) Search a specific chapter'
	# print '4) Search the entire Bible'
	# selection = int(raw_input("Select an option: "))
	tree = etree.parse('kjb.xml')
	bible = tree.getroot()

	for i, book_node in enumerate(bible):
			for chapter_node in book_node:
				for verse in chapter_node:
					f.write(unicode(verse.text))

	# print 'Word count: ' + str(stats['count'])
if __name__ == '__main__':
	main()