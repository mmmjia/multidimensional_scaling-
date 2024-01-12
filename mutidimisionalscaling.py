# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:16:20 2024

@author: user
"""

import pandas as pd
from sklearn.manifold import MDS
import numpy as np


year = ['2020','2021','2022','2023']; months = [str(i).zfill(2) for i in range(1,12+1)]
month0 = [i+'-'+j for i in year for j in months]
tt=18

ao=pd.read_excel(r"C:/Users/user/OneDrive - HKUST Connect/landscape/month-cleaned/"+month0[tt-1]+".xlsx")

#view Dataframe
seqclass=ao['class'].tolist()
seqdis=ao['Var'].tolist()
mutation_n=ao['mutation number'].tolist()
mutation_n=np.array(mutation_n)

data = ao['mutation|insertion info']
a0 = data.shape[0]
# data_mo2=dataa['MutList'][1:51]
aa = 'ACDEFGHIKLMNPQRSTVWY-'
aa2idx = {}
for i in range(len(aa)):
    aa2idx[aa[i]] = i

seqlabel=list(set(seqclass))


mutation = np.zeros((a0, 1274))
# print(data)
for j in range(0, len(data)):

    item = data[j]
    items = item.split('|')[0]
    items=items.split(';')
    for site in items:
        if not site == '':
            pos = int(site[1:-1])
            aap = site[-1]
            mutation[j][pos] = 1
            
mds = MDS(random_state=None,metric=True)
scaled_df = mds.fit_transform(mutation)

import matplotlib.pyplot as plt

#create scatterplot
plt.scatter(scaled_df[:,0], scaled_df[:,1])
#plt.scatter(df[:,0], df[:,1])
plt.show()


class Temp:
    def __init__(self, name, position,data,color):
        self.name=name
        self.position=position
        self.data=data
        self.color=color

# Create an empty dictionary to store class-wise data
class_data = {}
class_seq={}
# Iterate over the labels and data simultaneously
for label,element in zip(seqclass,data):
    if label not in class_seq:
        class_seq[label] = []  # Create an empty list for the class if it doesn't exist
    class_seq[label].append([element])  # Append a Temp instance to the respective class list

for label1, element1, element2, element3 in zip(seqclass, scaled_df[:,0], scaled_df[:,1], mutation_n):
    if label1 not in class_data:
        class_data[label1] = []  # Create an empty list for the class if it doesn't exist
    class_data[label1].append([element1,element2,element3])  # Append a Temp instance to the respective class list
    

colorall=['teal','yellow','blue','orange','grey','red','teal','cyan','grey','black','olive','tomato',
          'red','maroon','coral','orange',
     'pink','teal','orange','olive','maroon','teal','cyan','red','black','olive','tomato']

subseqs = []
for i in range(len(seqlabel)):
    na=seqlabel[i]
    subseqs.append(Temp(na, class_data[na],class_seq[na],colorall[i]))

k=0
for j in range(len(seqlabel)):
    pos = np.array(subseqs[k].position)
    pos1=pos[:,0]
    pos2=pos[:,1]
    plt.scatter((pos1),(pos2),label=subseqs[k].name,c=subseqs[k].color,alpha=0.5,s=30)
    print(subseqs[k].name,subseqs[k].color)
    k=k+1
        
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize="15")
plt.show()
    



