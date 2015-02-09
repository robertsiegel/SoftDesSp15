# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Robbie Siegel

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
	""" Shuffles the characters in the input string
		NOTE: this is a helper function, you do not have to modify this in any way """
	return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
	""" Returns the complementary nucleotide

		nucleotide: a nucleotide (A, C, G, or T) represented as a string
		returns: the complementary nucleotide
	>>> get_complement('A')
	'T'
	>>> get_complement('C')
	'G'
	"""
	if nucleotide == 'A':
		return 'T'
	elif nucleotide == 'T':
		return 'A'
	elif nucleotide == 'G':
		return 'C'
	elif nucleotide == 'C':
		return 'G'

def get_reverse_complement(dna):
	""" Computes the reverse complementary sequence of DNA for the specfied DNA
		sequence
	
		dna: a DNA sequence represented as a string
		returns: the reverse complementary DNA sequence represented as a string
	>>> get_reverse_complement("ATGCCCGCTTT")
	'AAAGCGGGCAT'
	>>> get_reverse_complement("CCGCGTTCA")
	'TGAACGCGG'
	"""
	backwards_dna = dna[::-1]
	reversed_dna = ""
	for nuc in backwards_dna:
		reversed_dna += get_complement(nuc)
	return reversed_dna

def rest_of_ORF(dna):
	""" Takes a DNA sequence that is assumed to begin with a start codon and returns
		the sequence up to but not including the first in frame stop codon.  If there
		is no in frame stop codon, returns the whole string.
		
		dna: a DNA sequence
		returns: the open reading frame represented as a string
	>>> rest_of_ORF("ATGTGAA")
	'ATG'
	>>> rest_of_ORF("ATGAGATAGG")
	'ATGAGA'
	"""
	rest_of_ORF = ""
	for i in range(0, len(dna), 3):
		if dna[i:i+3] in ["TAG", "TAA", "TGA"]:
			break
		else:
			rest_of_ORF += dna[i:i+3]
	return rest_of_ORF

def find_all_ORFs_oneframe(dna):
	""" Finds all non-nested open reading frames in the given DNA sequence and returns
		them as a list.  This function should only find ORFs that are in the default
		frame of the sequence (i.e. they start on indices that are multiples of 3).
		By non-nested we mean that if an ORF occurs entirely within
		another ORF, it should not be included in the returned list of ORFs.
		
		dna: a DNA sequence
		returns: a list of non-nested ORFs
	>>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
	['ATGCATGAATGTAGA', 'ATGTGCCC']
	"""

	i = 0
	ORFs = []
	while i < len(dna)-2:
		if dna[i:i+3] == "ATG":
			ORFs.append(rest_of_ORF(dna[i:]))
			i += len(ORFs[-1])
		else:
			i += 3
	return ORFs


def find_all_ORFs(dna):
	""" Finds all non-nested open reading frames in the given DNA sequence in all 3
		possible frames and returns them as a list.  By non-nested we mean that if an
		ORF occurs entirely within another ORF and they are both in the same frame,
		it should not be included in the returned list of ORFs.
		
		dna: a DNA sequence
		returns: a list of non-nested ORFs

	>>> find_all_ORFs("ATGCATGAATGTAG")
	['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
	"""
	
	all_ORFs = []

	for i in range(0, 3):
		 all_ORFs.extend(find_all_ORFs_oneframe(dna[i:]))
	return all_ORFs


def find_all_ORFs_both_strands(dna):
	""" Finds all non-nested open reading frames in the given DNA sequence on both
		strands.
		
		dna: a DNA sequence
		returns: a list of non-nested ORFs
	>>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
	['ATGCGAATG', 'ATGCTACATTCGCAT']
	"""
	return find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))


def longest_ORF(dna):
	""" Finds the longest ORF on both strands of the specified DNA and returns it
		as a string
	>>> longest_ORF("ATGCGAATGTAGCATCAAA")
	'ATGCTACATTCGCAT'
	"""
	if len(find_all_ORFs_both_strands(dna))>0:
		return max(find_all_ORFs_both_strands(dna), key=len)
	else:
		return ""


def longest_ORF_noncoding(dna, num_trials):
	""" Computes the maximum length of the longest ORF over num_trials shuffles
		of the specfied DNA sequence
		
		dna: a DNA sequence
		num_trials: the number of random shuffles
		returns: the maximum length longest ORF
	"""

	dna_list = []
	maximum = 0
	for i in range (0, num_trials):
		shuffled_dna = shuffle_string(dna)        
		if len(longest_ORF(shuffled_dna)) > maximum:
				maximum = len(longest_ORF(shuffled_dna))
	return maximum


def coding_strand_to_AA(dna):
	""" Computes the Protein encoded by a sequence of DNA.  This function
		does not check for start and stop codons (it assumes that the input
		DNA sequence represents an protein coding region).
		
		dna: a DNA sequence represented as a string
		returns: a string containing the sequence of amino acids encoded by the
				 the input DNA fragment

		>>> coding_strand_to_AA("ATGCGA")
		'MR'
		>>> coding_strand_to_AA("ATGCCCGCTTT")
		'MPA'
	"""

	acids = []
	for i in range(0, len(dna)-2, 3):
		acids.append(aa_table[dna[i:i+3]])
	return ''.join(acids)


def gene_finder(dna):
	""" Returns the amino acid sequences coded by all genes that have an ORF
		larger than the specified threshold.
		
		dna: a DNA sequence
		threshold: the minimum length of the ORF for it to be considered a valid
				   gene.
		returns: a list of all amino acid sequences whose ORFs meet the minimum
				 length specified.
	"""
	acids = []
	threshold = longest_ORF_noncoding(dna, 1500)
	for i in find_all_ORFs_both_strands(dna):
		if len(i) >= threshold:
			acids.append(coding_strand_to_AA(i))
	return acids


if __name__ == "__main__":
	import doctest
	doctest.testmod()
	print(gene_finder(load_seq('./data/X73525.fa')))
