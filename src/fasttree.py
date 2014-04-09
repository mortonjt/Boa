"""
Runs fasttree and generates a phylogenetic tree
"""


import Bio
from Bio import SeqIO, SeqFeature
from Bio.SeqRecord import SeqRecord

from Bio.Blast import NCBIXML
from Bio.Blast import NCBIStandalone

from collections import defaultdict

import sys
import os
import site
import argparse
import string
import numpy
import re
import subprocess
from accessionMap import GGAccession
from clustalw import ClustalW


class FastTree(object):
    def __init__(self,algnFile,treeFile):
        self.algnFile = algnFile
        self.treeFile = treeFile
    def run(self):
        cmd = "fasttree -nt %s"%self.algnFile
        proc = subprocess.Popen(cmd,stdout=open(self.treeFile,'w+'),shell=True)
        proc.wait()
    
class UnAlignedFastTree(FastTree):
    def __init__(self,rawSeqs,ggFile):
        self.rawSeqs=rawSeqs
        self.ggFile = ggFile
        basename,_ = os.path.splitext(rawSeqs)
        algnFile = "%s.align"%basename
        treeFile = "%s.tree"%basename
        self.accSeqs = "%s.acc"%basename
        super(UnAlignedFastTree,self).__init__(algnFile,treeFile)
    """ Run fasta tree """
    def run(self):
        super(UnAlignedFastTree,self).run()
    """ Run multiple alignment """
    def align(self):
        ggMap = GGAccession(self.ggFile)
        ggMap.swapGG(self.rawSeqs,self.accSeqs)        
        assert os.path.exists(self.accSeqs)
        assert os.stat(self.accSeqs).st_size!=0 #assert not empty
        cw = ClustalW(self.accSeqs,self.algnFile)
        cw.run()
        print self.accSeqs
        cw.outputFASTA()
        cw.cleanUp()
    def cleanUp(self):
        os.remove(self.accSeqs)
        os.remove(self.algnFile)

        
def ggRun(in16SRNA):#Running FastTree on gg 16SRNA data
    basename,_ = os.path.splitext(in16SRNA)
    ft = UnAlignedFastTree() #Swap all gg ids with accession ids
    ft.align() #Run multiple sequence alignment and spit out aligned fasta file
    ft.run() #Run fasttree on multiple alignment and spit out newick tree
    ft.cleanUp() #Clean up!
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description=\
        'Runs fasttree on unaligned 16SRNA sequences from greengenes')
    parser.add_argument(\
        '--16SRNA', type=str, nargs="+", required=False,
        help='FASTA files containing 16SRNA sequences')
    parser.add_argument(\
        '--gg-table', type=str, nargs="+", required=False,
        help='A table that converts gg ids to accession ids')
    parser.add_argument(\
        '--test', action='store_const', const=True, default=False,
        help='Run unittests')
    args = parser.parse_args()

    if not args.test:
        ggRun()
    else:
        del sys.argv[1:]
        import unittest
        class TestRun(unittest.TestCase):
            def setUp(self):
                self.infile="test.fa"
                self.ggtable = "../data/gg_13_5_accessions.txt"
                self.accSeqs= "acc.fa"
                entries = [">1111886",
                           "AACGAACGCTGGCGGCATGCCTAACACATGCAAGTCGAACGAGACCTTCGGGTCTAGTGGCGCACGGGTGCGTAACGCGTGGGAATCTGCCCTTGGGTACGGAATAACAGTTAGAAATGACTGCTAATACCGTATAATGACTTCGGTCCAAAGATTTATCGCCCAGGGATGAGCCCGCGTAGGATTAGCTTGTTGGTGAGGTAAAGGCTCACCAAGGCGACGATCCTTAGCTGGTCTGAGAGGATGATCAGCCACACTGGGACTGAGACATGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATATTGGACAATGGGCGAAAGCCTGATCCAGCAATGCCGCGTGAGTGATGAAGGCCTTAGGGTTGTAAAGCTCTTTTACCCGGGATGATAATGACAGTACCGGGAGAATAAGCCCCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGGGCTAGCGTTGTTCGGAATTACTGGGCGTAAAGCGCACGTAGGCGGCTTTGTAAGTTAGAGGTGAAAGCCCGGGGCTCAACTCCGGAATTGCCTTTAAGACTGCATCGCTAGAATTGTGGAGAGGTGAGTGGAATTCCGAGTGTAGAGGTGAAATTCGTAGATATTCGGAAGAACACCAGTGGCGAAGGCGACTCACTGGACACATATTGACGCTGAGGTGCGAAAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCGTAAACGATGATGACTAGCTGTCGGGGCGCTTAGCGTTTCGGTGGCGCAGCTAACGCGTTAAGTCATCCGCCTGGGGAGTACGGCCGCAAGGTTAAAACTCAAAGAAATTGACGGGGGCCTGCACAAGCGGTGGAGCATGTGGTTTAATTCGAAGCAACGCGCAGAACCTTACCAGCGTTTGACATGGTAGGACGGTTTCCAGAGATGGATTCCTACCCTTACGGGACCTACACACAGGTGCTGCATGGCTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCTCGTCTTTGGTTGCTACCATTTAGTTGAGCACTCTAAAAAAACTGCCGGTGATAAGCCGGAGGAAGGTGGGGATGACGTCAAGTCCTCATAGCCCTTACGCGCTGGGCTACACACGTGCTACAATGGCGGTGACAGAGGGCAGCAAACCCGCGAGGGTGAGCTAATCTCCAAAAGCCGTCTCAGTTCGGATTGTTCTCTGCAACTCGAGAGCATGAAGGCGGAATCGCTAGTAATCGCGGATCAGCACGCCGCGGTGAATACGTTCCCAGGCCTTGTACACACCGCCCGTCACATCACGAAAGTCGGTTGCACTAGAAGTCGGTGGGCTAACCCGCAAGGGAGGCAGCCGCCTAAAGTGTGATCGGTAATTGGGGTG",
                           ">1111885",
                           "AGAGTTTGATCCTGGCTCAGAATGAACGCTGGCGGCGTGCCTAACACATGCAAGTCGTACGAGAAATCCCGAGCTTGCTTGGGAAAGTAAAGTGGCGCACGGGTGAGTAACGCGTGGGTAACCCACCCCCGAATTCGGGATAACTCCGCGAAAGCGGTGCTAATACCGGATAAGACCCCTACCGCTTCGGCGGCAGAGGTAAAAGCTGACCTCTCCATGGAAGTTAGCGTTTGGGGACGGGCCCGCGTCCTATCAGCTTGTTGGTGGGGTAACAGCCCACCAAGGCAACGACGGGTAACTGGTCTGAGAGGATGATCAGTCACACTGGAACTGGAACACGGTCCAGACTCCTACGGGAGGCAGCAGTGAGGAATTTTGCGCAATGGGCGAAAGCCTGACGCAGCAACGCCGCGTGGGTGAAGAAGGCTTTCGGGTCGTAAAGCCCTGTCAGGTGGGAAGAAACCTTTCCGGTACTAATAATGCCGGAAATTGACGGTACCACCAAAGGAAGCACCGGCCAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCAAGCGTTGTTCGGAATTATGGGGCGTAAAGAGCGTGTGGGCGGTTAGGAAAGTCAGATGTGAAAGCCCTGGGCTCAACCCAGGAAGTGCATTTGAAACTGCCTAACTTGAGTACGGGAGAGGAAGGGGGAATTCCCGGTGTAGAGGTGAAATTCGTAGATATCGGGAGGAATACCGGTGGCGAAGGCGCCCTTCTGGACCGATACTGACGCTGAGACGCGAAAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCGTAAACGATGAGCACTAGGTGTAGCGGGTATTGACCCCTGCTGTGCCGTAGCTAACGCATTAAGTGCTCCGCCTGGGGATTACGGTCGCAAGACTAAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGACGCAACGCGAAGAACCTTACCTGGGCTTGACATCCCCGGACAGCCCTGGAAACAGGGTCTCCCACTTCGGTGGGCTGGGTGACAGGTGCTGCATGGCTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCCTGCCTTTAGTTGCCATCATTTAGCTGGGCACTCTAAAGGGACTGCCGGTGTTAAACCGGAGGAAGGTGGGGACGACGTCAAGTCCTCATGGCCTTTATGCCCAGGGCTACACACGTGCTACAATGGGCGGTACAAAGGGCAGCGACATCGTGAGGTGAAGCAAATCCCAAAAAACCGCTCTCAGTTCGGATCGGAGTCTGCAACTCGACTTCGTGAAGGTGGAATCACTAGTAATCGTGGATCAGCATGCCACGGTGAATACGTTCCCGGGCCTTGTACACACCGCCCGTCACACCACGAAAGTCTGCTGTACCAGAAGTCGCTGGGCTAACCCGCCCTAGGCGGGAGGTAGGCGCCTAAGGTACGGCCGGTAATTGGGGTGAAGTCGTAACAAGGTAACC",
                           ">1111883",
                           "GCTGGCGGCGTGCCTAACACATGTAAGTCGAACGGGACTGGGGGCAACTCCAGTTCAGTGGCAGACGGGTGCGTAACACGTGAGCAACTTGTCCGACGGCGGGGGATAGCCGGCCCAACGGCCGGGTAATACCGCGTACGCTCGTTTAGGGACATCCCTGAATGAGGAAAGCCGTAAGGCACCGACGGAGAGGCTCGCGGCCTATCAGCTAGTTGGCGGGGTAACGGCCCACCAAGGCGACGACGGGTAGCTGGTCTGAGAGGATGGCCAGCCACATTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATCTTGCGCAATGGCCGCAAGGCTGACGCAGCGACGCCGCGTGTGGGATGACGGCCTTCGGGTTGTAAACCACTGTCGGGAGGAACGAATACTCGGCTAGTCCGAGGGTGACGGTACCTCCAAAGGAAGCACCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCGAGCGTTGTCCGGAATCACTGGGCGTAAAGGGCGCGTAGGTGGCCCGTTAAGTGGCTGGTGAAATCCCGGGGCTCAACTCCGGGGCTGCCGGTCAGACTGGCGAGCTAGAGCACGGTAGGGGCAGATGGAATTCCCGGTGTAGCGGTGGAATGCGTAGATATCGGGAAGAATACCAGTGGCGAAGGCGTTCTGCTGGGCCGTTGCTGACACTGAGGCGCGACAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCGTAAACGATGGACACTAGACGTCGGGGGGAGCGACCCTCCCGGTGTCGTCGCTAACGCAGTAAGTGTCCCGCCTGGGGAGTACGGCCGCAAGGCTGAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGAAGCAACGCGAAGAACCTTACCTGGGCTTGACATGCTGGTGCAAGCCGGTGGAAACATCGGCCCCTCTTCGGAGCGCCAGCACAGGTGCTGCATGGCTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACTCTCGCTCCCAGTTGCCAGCGGTTCGGCCGGGGACTCTGGGGGGACTGCCGGCGTTAAGCCGGAGGAAGGTGGGGACGACGTCAAGTCATCATGGCCCTTACGTCCAGGGCGACACACGTGCTACAATGCCTGGTACAGCGCGTCGCGAACTCGCAAGAGGGAGCCAATCGCCAAAAGCCGGGCTAAGTTCGGATTGTCGTCTGCAACTCGACGGCATGAAGCCGGAATCGCTAGTAATCGCGGATCAGCCACGCCGCGGTGAATACGTTCCCGGGCCTTGTACACACCGCCCGTCACGCCATGGAAGCCGGAGGGACCCGAAACCGGTGGGCCAACCGCAAGGGGGCAGCCGTCTAAGGT",
                           ">1111882",
                           "AGAGTTTGATCATGGCTCAGGATGAACGCTAGCGGCAGGCCTAACACATGCAAGTCGAGGGGTAGAGGCTTTCGGGCCTTGAGACCGGCGCACGGGTGCGTAACGCGTATGCAATCTGCCTTGTACTAAGGGATAGCCCAGAGAAATTTGGATTAATACCTTATAGTATATAGATGTGGCATCACATTTCTATTAAAGATTTATCGGTACAAGATGAGCATGCGTCCCATTAGCTAGTTGGTATGGTAACGGCATACCAAGGCAATGATGGGTAGGGGTCCTGAGAGGGAGATCCCCCACACTGGTACTGAGACACGGACCAGACTCCTACGGGAGGCAGCAGTGAGGAATATTGGTCAATGGGCGCAAGCCTGAACCAGCCATGCCGCGTGCAGGATGACGGTCCTATGGATTGTAAACTGCTTTTGTACGGGAAGAAACACTCCTACGTGTAGGGGCTTGACGGTACCGTAAGAATAAGGATCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGATCCAAGCGTTATCCGGAATCATTGGGTTTAAAGGGTCCGTAGGCGGTTTTATAAGTCAGTGGTGAAATCCGGCAGCTCAACTGTCGAACTGCCATTGATACTGTAGAACTTGAATTACTGTGAAGTAACTAGAATATGTAGTGTAGCGGTGAAATGCTTAGATATTACATGGAATACCAATTGCGAAGGCAGGTTACTAACAGTATATTGACGCTGATGGACGAAAGCGTGGGGAGCGAACAGGATTAGATACCCTGGTAGTCCACGCCGTAAACGATGGATACTAGCTGTTTGGCAGCAATGCTGAGTGGCTAAGCGAAAGTGTTAAGTATCCCACCTGGGGAGTACGAACGCAAGTTTGAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGATGATACGCGAGGAACCTTACCAGGGCTTAAATGTAGAGTGACAGGACTGGAAACAGTTTTTTCTTCGGACACTTTACAAGGTGCTGCATGGTTGTCGTCAGCTCGTGCCGTGAGGTGTCAGGTTAAGTCCTATAACGAGCGCAACCCCTGTTGTTAGTTGCCAGCGAGTAATGTCGGGAACTCTAACAAGACTGCCGGTGCAAACCGTGAGGAAGGTGGGGATGACGTCAAATCATCACGGCCCTTACGTCCTGGGCTACACACGTGCTACAATGGCCGGTACAGAGAGCAGCCACCTCGCGAGGGGGAGCGAATCTATAAAGCCGGTCACAGTTCGGATTGGAGTCTGCAACCCGACTCCATGAAGCTGGAATCGCTAGTAATCGGATATCAGCCATGATCCGGTGAATACGTTCCCGGGCCTTGTACACACCGCCCGTCAAGCCATGGAAGCTGGGGGTACCTGAAGTCGGTGACCGCAAGGAGCTGCCTAGGGTAAAACTGGTAACTGGGGCTAAGTCGTACAAGGTAGCCGTA",
                           ">1111879",
                           "CCTAATGCATGCAAGTCGAACGCAGCAGGCGTGCCTGGCTGCGTGGCGAACGGCTGACGAACACGTGGGTGACCTGCCCCGGAGTGGGGGATACCCCGTCGAAAGACGGGACAATCACGCATACGCTCTTTGGAGGAAAGCCATCCGGCGCTCTGGGAGGGGCCTGCGGCCCATCAGGTAGTTGGTGTGGTAACGGCGCACCAAGCCAATGACGGGTACCCGGTCTGAGAGGACGACCGGCCAGACTGGAACTGCGACACGGCCCAGACTCCTACGGGAGGCAGCAGCAAGGAATTTTCCCCAATGGGCGCAAGCCTGAGGCAGCAACGCCGCGTGCGGGATGACGGACTTCGGGTTGTAAACCGCTTTTCGGGGGGACAACCCTGACGGTACCCCCGGAACAAGCCCCGGCTAACTCTGTGCCAGCAGCCGCGGTAAGACAGAGGGGGCAAGCGTTGTCCGGAGTCACTGGGCGTAAAGCGCGCGCAGGCGGCTGCCTAAGTGTCGTGTGAAAGCCCCCGGCTCAACCGGGGGAGGCCATGGCAAACTGGGTGGCTCGAGCGGCGGAGAGGTCCCTCGAATTGCCGGTGTAGCGGTGAAATGCGTAGAGATCGGCAGGAAGACCAAGGGGGAAGCCAGGGGGCTGGCCGCCGGCTGACGCTGAGGCGCGACAGCGTGGGGAGCAAACCGGATTAGATACCCGGGTAGTCCACGCCGTAAACGATGACCACTCGGCGTGTGGCGACTATTAACGTCGCGGCGCGCCCTAGCTCACGCGATAAGTGGTCCGCCTGGGAACTACGAGCGCAAGCTTAAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCAGCGGAGCGTGTGGTTTAATTCGACGCAACCCGCAGAACCTTACCCAGACTGGACATGACGGTGCAGACGGCGGAAACGTCGTCGCCTGCGAGGGTCCGTCACAGGTGCTGCATGGCTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCCTGCGGTTAGTTACCCGTGTCTAACCGGACTGCCCTTCGGGGAGGAAGGCGGGGATGACGTCAAGTCCGCATGGCCCTTACGTCTGGGGCGACACACACGCTACAATGGCGCCGACAATGCGTCGCTCCCGCGCAAGCGGATGCTAATCGCCAAACGGCGCCCCAGTGCAGATCGGGGGCTGCAACTCGCCCCCGTGAAGGCGGAGTTGCTAGTAACCGCGTATCAGCCATGGCGCGGTGAATACGTACCCGGGCCTTGTACACACCGCCCGTCACGTCATGGAGTTGTCAATGCCTGAAGTCCGCCAGCTAACC"
                           ]
                open(self.infile,'w').write('\n'.join(entries))
            def tearDown(self):
                os.remove(self.infile)
            def testAlign(self):
                ft = UnAlignedFastTree(self.infile,self.ggtable)
                ft.align()
                self.assertTrue( os.path.exists(ft.algnFile) )
                self.assertTrue( os.stat(ft.algnFile).st_size!=0 )
                ft.cleanUp()
                os.remove(ft.treeFile)
            def testRun(self):
                ft = UnAlignedFastTree(self.infile,self.ggtable)
                ft.align()
                ft.run()
                self.assertTrue( os.path.exists(ft.treeFile) )
                self.assertTrue( os.stat(ft.treeFile).st_size!=0 )
                ft.cleanUp() 
                os.remove(ft.treeFile)
        unittest.main()
        
        
        
        
        
        
        