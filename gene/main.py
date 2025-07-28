import time
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

import numpy as np
import pandas as pd
import os

from pathlib import Path


import scanpy as sc
import omicverse as ov
import matplotlib.pyplot as plt
ov.plot_set()


data_dir = Path("/workspace/pyfaster/examples/gene/data")
data_dir = Path("/app/examples/gene/data")

input_file = data_dir / "valid_gene_20115.csv"

with open(input_file, "r") as f:
    gene_df = pd.read_csv(f, index_col=0)


from statsmodels import robust #import package
gene_mad=gene_df.apply(robust.mad) #use function to calculate MAD
gene_df=gene_df.T
gene_df=gene_df.loc[gene_mad.sort_values(ascending=False).index[:2000]]


#import PyWGCNA
pyWGCNA_5xFAD = ov.bulk.pyWGCNA(name='5xFAD_2k', 
                              species='mus musculus', 
                              geneExp=gene_df, 
                              outputPath='',
                              save=True)
pyWGCNA_5xFAD.geneExpr.to_df().head(5)

pyWGCNA_5xFAD.preprocess()

pyWGCNA_5xFAD.calculate_soft_threshold()


pyWGCNA_5xFAD.calculating_adjacency_matrix()


pyWGCNA_5xFAD.calculating_TOM_similarity_matrix()


pyWGCNA_5xFAD.calculate_geneTree()
pyWGCNA_5xFAD.calculate_dynamicMods(kwargs_function={'cutreeHybrid': {'deepSplit': 2, 'pamRespectsDendro': False}})
pyWGCNA_5xFAD.calculate_gene_module(kwargs_function={'moduleEigengenes': {'softPower': 5}})

pyWGCNA_5xFAD.plot_matrix(save=True)

pyWGCNA_5xFAD.saveWGCNA()


