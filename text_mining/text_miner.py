""" 
@author Robbie Siegel

This program analyzes text data.
"""
import pickle
import string
import matplotlib.pyplot as plt
from pattern.en.wordlist import PROFANITY

def create_dictionary(textfile):
    """Creates a dictionary that includes each word in the file 
       mapped to the number of times it appears

    textfile: text file including string to analyze
    returns: the dictionary of all words in the text
    """
    dict = {} 
    txt = file(textfile) #opens up text file to analyze as a string
    for line in txt: #runs through each line of text to find individual words
        update_dictionary(line, dict)
    return dict


def update_dictionary(line, dict):
    """Adds the words in the line to the dictionary of 
    all words in the text. If the word is already in the
    dictionary, the key will be increased by one.
.
    line: string of text
    dict: dictionary of words processed so far
    """

    line = line.replace('-', ' ') #replaces hyphens with spaces
    for word in line.split(): #removes punctuation and converts to lowercase
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        dict[word] = dict.get(word, 0) + 1 #updates dictionary


def analyze_profanity(dict):
    """Finds the number of words considered profanity in a dictionary
    and the ratio of profanity to total words.

    dict: a dictionary of all the words in the text to analyze
    mapped to their number of uses
    return: A nested list including the list of all curse words
    and the ratio of curse words to total words in the text.
    """    
    curse_words, curse_count, total_words = [], 0, 0 #initializes variables
    for word in dict: #runs through every word in dictionary
        total_words += dict.get(word) #tracks total number of words
        if word in PROFANITY: #finds if word is included in pattern's list of profanity
            curse_words.append(word) #adds curse to list of profanity
            curse_count+=dict.get(word) #adds the uses of this profanity to the curse count
    return[curse_words, float(curse_count)/total_words]

def plot_profanity(dict, label):
    """Finds the number of words considered profanity in a dictionary
    and the ratio of profanity to total words.

    dict: a dictionary of all the words in the text to analyze
    mapped to their number of uses
    return: A nested list including the list of all curse words
    and the ratio of curse words to total words in the text.
    """
    profanity = analyze_profanity(dict)
    curses = len(profanity[0]) #finds the number of different curse words used
    ratio = profanity[1] #ratio of words considered profanity to total words

    plt.plot([curses], [ratio]) #plots curses vs. ratio
    plt.axis([0, 25, 0, .0025])
    plt.annotate(label, (curses, ratio))


#creates dictionaries for every text file to analyze
d_moby = create_dictionary('moby_dick.txt')
d_wizard = create_dictionary('wizard_of_oz.txt')
d_beowulf = create_dictionary('beowulf.txt')
d_huckleberry = create_dictionary('huckleberry_finn.txt')
d_scarlet = create_dictionary('scarlet_letter.txt')
d_divine = create_dictionary('divine_comedy.txt')

#prints a list of each profane word used in each of six books
print analyze_profanity(d_moby)[0]
print analyze_profanity(d_wizard)[0]
print analyze_profanity(d_beowulf)[0]
print analyze_profanity(d_scarlet)[0]
print analyze_profanity(d_huckleberry)[0]
print analyze_profanity(d_divine)[0]


#Calls the plot_profanity function for each dictionary we want to analyze and then plots them together
plot_profanity(d_moby, 'Moby Dick')
plot_profanity(d_wizard, 'The Wizard of Oz')
plot_profanity(d_beowulf,'Beowulf')
plot_profanity(d_scarlet, 'The Scarlet Letter')
plot_profanity(d_huckleberry, 'Huckleberry Finn')
plot_profanity(d_divine, 'The Divine Comedy')


plt.title('Profanity in Different Novels')
plt.ylabel('Ratio of Curse Words to Total Words')
plt.xlabel('Number of Different Profanities Used')
plt.show()