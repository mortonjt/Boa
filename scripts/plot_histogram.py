"""
Plot histogram of all context genes
"""


import os
import sys
import site
import re
import numpy as np
import numpy.random
import matplotlib.pyplot as plt

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path="%s/src"%base_path
for directory_name in os.listdir(base_path):
    site.addsitedir(os.path.join(base_path, directory_name))
    
import clique_filter
import hmmer            
from collections import Counter
import itertools
import cPickle
import gff

def bargraph(clusters,numFuncs):
	operon_cnts = Counter(['toxin','modifier','immunity','transport','regulator'])
	funcs = set()
	for cluster in clusters:
		cnts = Counter()
		for node in cluster:
			toks = node.split('|')
			acc,clrname,full_evalue,hmm_st,hmm_end,env_st,env_end,description=toks
			function = clrname.split('.')[0]
			funcs.add(function)
			cnts[function]+=1

		if numFuncs==len(funcs): operon_cnts = operon_cnts+cnts
	return operon_cnts

if __name__=="__main__":
	faidx = "/home/mortonjt/Projects/Bacfinder/workspace/quorum/data/all_trans.fai"
    gffFile = "/home/mortonjt/Projects/Bacfinder/workspace/quorum/data/all.gff"
    folder = "/home/mortonjt/Projects/Bacfinder/workspace/quorum/intermediate"
	if os.path.exists("all_hits.pickle"):
		all_hits, clusters = cPickle.load(open("all_hits.pickle",'rb'))

	else:

		toxin_hits     = hmmer.parse("%s/toxin.out"%folder)
		modifier_hits  = hmmer.parse("%s/modifier.out"%folder)
		immunity_hits  = hmmer.parse("%s/immunity.out"%folder)
		regulator_hits = hmmer.parse("%s/regulator.out"%folder)
		transport_hits = hmmer.parse("%s/transport.out"%folder)

		gff = gff.GFF(gff_file=gffFile,fasta_index=faidx)
		toxin_hits     = gff.call_orfs(toxin_hits    )
		modifier_hits  = gff.call_orfs(modifier_hits )
		immunity_hits  = gff.call_orfs(immunity_hits )
		regulator_hits = gff.call_orfs(regulator_hits)
		transport_hits = gff.call_orfs(transport_hits)
    	all_hits = toxin_hits+modifier_hits+immunity_hits+regulator_hits+transport_hits
    	all_hits=sorted(all_hits,key=lambda x: x[6])   
        all_hits=sorted(all_hits,key=lambda x: x[5])
        
        #Sort by genome name
        all_hits=sorted(all_hits,key=lambda x: x[0])  
    	all_hits = interval_filter.overlaps(all_hits,faidx)
    	all_hits = interval_filter.unique(all_hits)
    	cf = clique_filter.CliqueFilter(radius=50000)
    	cf.createGraph(all_hits,backtrans=False)
    	clusters = cf.filter(keyfunctions=["toxin","transport"])
    	

    	cPickle.dump((all_hits,clusters),open("all_hits.pickle",'wb'))

	func5 = bargraph(clusters,5)
	func4 = bargraph(clusters,5)
	func3 = bargraph(clusters,5)
	func2 = bargraph(clusters,5)
	toxinsCnts = [func5['toxin'],func4['toxin'],func3['toxin'],func2['toxin']]
	N = 4
	width = 0.1
	rect1 = ax.bar(ind,toxinCnts,width,color='r')
	ax.set_ylabel("Number of genes")
	ax.set_title("Number of gene function counts")
	ax.set_xlabel("Number of types of genes in operon")
	ax.set_xticks(ind)
	ax.set_xticklabels(('5','4','3','2'))

	plt.show()
