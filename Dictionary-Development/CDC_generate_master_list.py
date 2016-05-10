# -*- coding: utf-8 -*-
"""
Created on Tue May 03 23:28:01 2016

@author: ffan
"""

#from __future__ import division
import pandas as pd
import numpy as np

## import data
combo1=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo1_1.csv')
combo2=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo2_1.csv')
combo3=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo3_1.csv')
combo4=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo4_1.csv')
combo5=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo5_1.csv')
combo6=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo6_1.csv')
combo7=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo7_1.csv')
combo8=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo8_1.csv')

combo_all=[combo1,combo2,combo3,combo4,combo5,combo6,combo7,combo8]
combo_all=pd.concat(combo_all,keys=['1','2','3','4','5','6','7','8'])

joint_data = combo_all.drop_duplicates()
joint_data = joint_data.drop(joint_data.index[[0]])

## find unique agents
TerisAgentIdx=pd.notnull(joint_data['agentname'])
TerisNotesIdx=pd.notnull(joint_data['notes'])

ShepAgentIdx=pd.notnull(joint_data['ShepAgentName'])
ShepSumIdx=pd.notnull(joint_data['ShepDescrip'])

ReproNoIdx=pd.notnull(joint_data['DrugNo'])
ReproSumIdx=pd.notnull(joint_data['DrugSummary'])

ReproNo=set(joint_data['DrugNo'][ReproNoIdx])
TerisAgent=set(joint_data['agentname'][TerisAgentIdx])
ShepAgent=set(joint_data['ShepAgentName'][ShepAgentIdx])

print len(TerisAgent)
print len(ShepAgent)
print len(ReproNo)

#==============================================================================
# Generate Teris master list
#==============================================================================
Teris_agent_list=pd.DataFrame()
for item in list(TerisAgent):
    
    subgroup1=joint_data[joint_data['agentname'] == item]
    
    if len(subgroup1)>1:
         subgroup1 = subgroup1.sort(['DrugNo', 'ShepAgentName'], ascending=[1, 1])
         u1, indices1 = np.unique(subgroup1['DrugNo'], return_index=True)
         u2, indices2 = np.unique(subgroup1['ShepAgentName'], return_index=True)
         idx1=[i for i in indices1 if pd.notnull(subgroup1['DrugNo'].iloc[i])]
         idx2=[i for i in indices2 if pd.notnull(subgroup1['ShepAgentName'].iloc[i])]
         idx3=list(set(idx1) | set(idx2))
         subgroup1=subgroup1.iloc[idx3]
    Teris_agent_list=Teris_agent_list.append(subgroup1)
        
#==============================================================================
# Generate Shepherd master list      
#==============================================================================
Shep_agent_list=pd.DataFrame()

for item in list(ShepAgent):
    
    subgroup1=joint_data[joint_data['ShepAgentName'] == item]
    
    if len(subgroup1)>1:
         subgroup1 = subgroup1.sort(['agentname','DrugNo'], ascending=[1, 1])
         u1, indices1 = np.unique(subgroup1['agentname'], return_index=True)
         u2, indices2 = np.unique(subgroup1['DrugNo'], return_index=True)
         idx1=[i for i in indices1 if pd.notnull(subgroup1['agentname'].iloc[i])]
         idx2=[i for i in indices2 if pd.notnull(subgroup1['DrugNo'].iloc[i])]
         idx3=list(set(idx1) | set(idx2))
         subgroup1=subgroup1.iloc[idx3]
    Shep_agent_list=Shep_agent_list.append(subgroup1)

#len(set(Shep_agent_list['ShepAgentName']))
#==============================================================================
# Generate Reprotox agent master list
#==============================================================================
Repro_agent_list=pd.DataFrame()

for item in list(ReproNo):

#    item=1002.0
    subgroup1=joint_data[joint_data['DrugNo'] == item]
    
    if len(subgroup1)>1:
         subgroup1 = subgroup1.sort(['agentname','ShepAgentName'], ascending=[1, 1])
         u1, indices1 = np.unique(subgroup1['agentname'], return_index=True)
         u2, indices2 = np.unique(subgroup1['ShepAgentName'], return_index=True)
         idx1=[i for i in indices1 if pd.notnull(subgroup1['agentname'].iloc[i])]
         idx2=[i for i in indices2 if pd.notnull(subgroup1['ShepAgentName'].iloc[i])]
         idx3=list(set(idx1) | set(idx2))
         subgroup1=subgroup1.iloc[idx3]
    Repro_agent_list=Repro_agent_list.append(subgroup1)  

#==============================================================================
# Generate master list for all    
#==============================================================================
result=Teris_agent_list.append([Shep_agent_list,Repro_agent_list])
master_list = result.drop_duplicates()
master_list= master_list.sort(['agentname', 'DrugNo', 'ShepAgentName'], ascending=[1,1, 1])

np.savetxt(r'C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\master_list_v1.txt', master_list.values, fmt="%s")
master_list.to_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\master_list_v1.csv',index=False,na_rep=" ")

#print len(set(master_list['agentname'][pd.notnull(master_list['agentname'])]))
#print len(set(master_list['DrugNo'][pd.notnull(master_list['DrugNo'])]))
#print len(set(master_list['ShepAgentName'][pd.notnull(master_list['ShepAgentName'])]))