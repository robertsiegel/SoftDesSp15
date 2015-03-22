""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg 

	Author: Robbie Siegel
"""

import string
from collections import OrderedDict
from operator import itemgetter

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a dictionary.
	"""
	f = open(file_name,'r')
	lines = f.readlines()
	dict = {}
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
		curr_line += 1
	lines = lines[curr_line+1:]
	for line in lines:
		line = line.replace('-', ' ') #replaces hyphens with spaces
		for word in line.split(): #removes punctuation and converts to lowercase
			word = word.strip(string.punctuation + string.whitespace)
			word = word.lower()
			dict[word] = dict.get(word, 0) + 1 #updates dictionary
	return dict 

def get_top_n_words(word_dict, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_dict: a dictionary of words (assumed to all be in lower case with no
					punctuation) mapped to its number of uses
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequently occurring
	"""
	ordered_dict = OrderedDict(sorted(word_dict.items(), key=itemgetter(1), reverse=True))
	return ordered_dict.keys()[:n]


if __name__ == "__main__":
	list = get_word_list('pg32325.txt')
	print get_top_n_words(list, 100)