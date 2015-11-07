import json
import codecs
import math
from difflib import SequenceMatcher
import xml.etree.ElementTree as etree

# taken from http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
def similar(a, b):
	return SequenceMatcher(a, b).ratio()

def is_ascii(s):
	try:
		return all(ord(c) < 128 for c in s)
	except Exception as ex:
		return False

def standardDeviation(arr):
	if not len(arr) > 1:
		return 0
	def mean(arr):
		return sum(arr)/len(arr)
	dev = []
	arr_mean = mean(arr)
	for n in arr:
		dev.append((n - arr_mean)**2)
	return math.sqrt(mean(dev))

def occurance(arr):
	results = []
	for n in arr:
		data = {}
		data["point"] = n
		data["count"] = 0
		for i in range(0, len(arr)):
			if n == arr[i]:
				data["count"] += 1
		results.append(data)
	return results

def main():
	count = 0
	deviation = None
	plots = []
	books_of_bible = {}

	key_word = raw_input("Enter a keyword to search for:  ")
	print 'Search an entire book, chapter, or the entire Bible'
	print '1) Search a book'
	print '2) Search a chapter'
	print '3) Search the entire Bible'

	selection = int(raw_input("Select an option: "))
	tree = etree.parse('kjb.xml')
	bible = tree.getroot()
	plot_tag = None

	if selection == 1 or selection == 2:
		book_name = raw_input("Enter the book name: ")
		for i, book_node in enumerate(bible):
			if book_node.attrib.has_key("num") and (book_node.attrib["num"].lower() == book_name.lower()[:3]):
				# Book search
				if selection == 1:
					plot_tag = "Chapter"
					for chapter in book_node:
						for verse in chapter:
							if is_ascii(verse.text):
								if key_word.lower() in verse.text.lower():								
									count += 1
									plots.append(int(chapter.attrib["num"]))
				# Chapter search
				elif selection == 2:
					plot_tag = "Verse"
					chapter_num = int(raw_input("Enter chapter number: "))
					for chapter in book_node:
						if int(chapter.attrib["num"]) == chapter_num:
							for verse in chapter:
								if is_ascii(verse.text):
									if key_word.lower() in verse.text.lower():								
										count += 1
										plots.append(int(verse.attrib["num"]))
	# Bible search
	elif selection == 3:
		plot_tag = "Book"
		big_plots = {}
		for i, book_node in enumerate(bible):
			for chapter in book_node:
				for verse in chapter:
					if is_ascii(verse.text):
						if key_word.lower() in verse.text.lower():	
							if book_node.attrib.has_key("num"):						
								if big_plots.has_key(book_node.attrib["num"]):
									big_plots[book_node.attrib["num"]] += 1
								else:
									big_plots[book_node.attrib["num"]] = 1
							# if not books_of_bible.has_key(book_node.attrib["num"]):
							# 		books_of_bible[book_node.attrib["num"]] = i + 1

	print '--- Word Count ---' + str(count)
	print '--- Deviation ---'
	if selection == 1 or selection == 2:
		print "Deviation: " + str(standardDeviation([ item["point"] for item in occurance(plots)]))
		for item in occurance(plots):
			print plot_tag + ": " + str(item["point"]) + " Count: " + str(item["count"])
	elif selection == 3:
		for k,v in big_plots.iteritems():
			print plot_tag + ": " + k + " " + str(v)

if __name__ == '__main__':
	main()
