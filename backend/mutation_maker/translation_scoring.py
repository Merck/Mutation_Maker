#    Copyright (c) 2020 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Kenilworth, NJ, USA.
#
#    This file is part of the Mutation Maker, An Open Source Oligo Design Software For Mutagenesis and De Novo Gene Synthesis Experiments.
#
#    Mutation Maker is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Bio.SeqUtils import GC
from mutation_maker.degenerate_codon import DegenerateTriplet
from functools import reduce
from typing import List, Dict


class TranslationScoring:
    """ Function object for calculating a score for a reverse-translated sequence."""
    threshold: float  # threshold for the codon frequency
    gc_power: int   # exponent value when calculating difference between desired and actual GC content
    gc_range: List[int]  # desired GC content range

    def __init__(self, threshold: float, gc_range: List[int], codonUsage, usage_table):
        self.threshold = threshold
        self.gc_power = 2
        self.gc_range = gc_range
        self.codonUsage = codonUsage
        self.usage_table = usage_table


    def get_codons(self, AA: str, threshold: float) -> Dict[str, float]:
        """ Method to get dictionary of possible codons with corresponding
        frequencies for a given amino acid """
        codons = self.codonUsage.get_all_possible_triplets_for_amino(AA, threshold) # list of codons for a given amino acid
        codons_with_frequency = {str(d) : self.usage_table[str(d)] for d in codons} # combinig a list of codons with corresponding frequencies from the table
        return codons_with_frequency


    def __call__(self, dna_sequence: str) -> tuple:
        # -- calculation of CAI --
        w_list = [] # list of individual Relative Adaptivness
        length = len(dna_sequence)-1
        dna_with_stop = dna_sequence + 'x' # add stop character to the end of dna sequence to be able to iterate by codons
        get_aa = DegenerateTriplet() # this instance is needed to later get the list of amino acids generated by a given codon
        n_codons = len(dna_sequence)/3 # number of codons on a sequence
        for i in range(0,len(dna_sequence)-1,3):
            codon = dna_sequence[i:i+3] # specifying given codon
            aa = get_aa.degenerate_codon_to_aminos(str(codon), self.codonUsage.table.forward_table)[0] # getting a corresponding amino acid for this codon
            all_codons = self.get_codons(aa, self.threshold) # getting a list of all codons for a given dna sequence
            c_max = all_codons[max(all_codons, key=all_codons.get)] # identifying maximal codon usage for a given amino acid
            c_current = all_codons[str(codon)] # identifying usage value for a given codon
            w = c_current/c_max # calculating Relative Adaptivness for a given codon
            w_list.append(w)
        CAI_score = (reduce(lambda x, y: x*y, w_list))**(1/n_codons) # calculating CAI (codon adaptation index) which is the exponent of the product of all
        #-- calculation of GC content ratio
        gc_desired = (self.gc_range[0] + self.gc_range[1])//2 # identifying middle of the desired gc content region
        gc_sequence = GC(dna_sequence)
        GC_score = abs(float((gc_desired - gc_sequence))/100) # calculating the score
        return (CAI_score, GC_score) # final score function
