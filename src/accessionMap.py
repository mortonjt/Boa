import Bio
from Bio import SeqIO, SeqFeature
from Bio.SeqRecord import SeqRecord

"""
Convert accession ids to green gene ids
"""
class AccessionGG(object):
    def __init__(self,input_file):
        self.input = input_file
        self.ggtable = dict()
        self.buildTable()
    def buildTable(self):
        with open(self.input,'r') as handle:
            for ln in handle:
                if ln[0]=='#': continue
                ln = ln.rstrip()
                toks = ln.split('\t')
                gg,db,acc = toks #green genes, database type, accession
                #print gg,db,acc
                self.ggtable[(db,acc)] = gg
    def lookupGenbank(self,acc):
        try:
            return self.ggtable[("Genbank",acc)]
        except:
            print "Accession ID %s not found in table"%acc
            return None
            #raise

"""
Convert accession ids to green gene ids
"""
class GGAccession(object):
    def __init__(self,input_file):
        self.input = input_file
        self.ggtable = dict()
        self.buildTable()
    def buildTable(self):
        with open(self.input,'r') as handle:
            for ln in handle:
                if ln[0]=='#': continue
                toks = ln.split('\t')
                assert len(toks)==3,toks
                gg,db,acc = toks #green genes, database type, accession
                self.ggtable[(db,gg)] = acc
    def lookupGenbank(self,gg):
        try:
            return self.ggtable[("Genbank",gg)]
        except:
            print "Accession ID %s not found in table"%acc
            return None
            #raise
    """Changes all gg ids in fasta file to accession ids"""
    def swapGG(self,fastain,fastaout):
        outHandle = open(fastaout,'w') 
        for record in SeqIO.parse( open(fastain),'fasta'):
            gg = record.id
            acc = self.lookupGenbank(gg)
            record.id = acc
            outHandle.write(record.format('fasta'))
            
        outHandle.close()
        
if __name__=="__main__":
    import unittest
    class TestGGtoAccession(unittest.TestCase):
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
            def testGG(self):
                ggMap = GGAccession(self.ggtable)
                ggMap.swapGG(self.infile,self.accSeqs)
                handle = open(self.accSeqs,'r')
                lines = handle.readlines()
                line1 = lines[0].rstrip()
                toks = line1.split(' ')
                self.assertFalse("1111886" in toks[0])
        
    unittest.main()
                
    
                
