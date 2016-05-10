# -*- coding: utf-8 -*-
"""
Created on Mon May 02 15:57:58 2016

@author: ffan
"""
#from __future__ import division
import pandas as pd


## import data
joint_data=pd.read_csv('C:\\Users\\ffan\\Downloads\\Projects\\CDC\\full_data\\Combo5_1.csv')

#joint_data.shape
#joint_data.columns.values.tolist()

## checking matches
TerisAgentIdx=pd.notnull(joint_data['agentname'])
TerisNotesIdx=pd.notnull(joint_data['notes'])

ShepAgentIdx=pd.notnull(joint_data['ShepAgentName'])
ShepSumIdx=pd.notnull(joint_data['ShepDescrip'])

ReproNoIdx=pd.notnull(joint_data['DrugNo'])
ReproSumIdx=pd.notnull(joint_data['DrugSummary'])

TerisAgent=set(joint_data['agentname'][TerisAgentIdx])
ShepAgent=set(joint_data['ShepAgentName'][ShepAgentIdx])
ReproNo=set(joint_data['DrugNo'][ReproNoIdx])

# match 3

idx_temp_TSR = [all(idx) for idx in zip(TerisNotesIdx,ShepSumIdx, ReproSumIdx)]
match3_temp_T=set(joint_data['agentname'][idx_temp_TSR])
match3_temp_S=set(joint_data['ShepAgentName'][idx_temp_TSR])
match3_temp_R=set(joint_data['DrugNo'][idx_temp_TSR])

# Teris and shephard 
idx_temp_TS = [all(idx) for idx in zip(TerisNotesIdx,ShepSumIdx, [not i for i in ReproSumIdx])]
match2_TS_S_temp=set(joint_data['ShepAgentName'][idx_temp_TS])
match2_TS_T_temp=set(joint_data['agentname'][idx_temp_TS])

# Teris and Reprotox 
idx_temp_TR = [all(idx) for idx in zip(TerisNotesIdx,ReproSumIdx ,[not i for i in ShepSumIdx])]
match2_TR_T_temp=set(joint_data['agentname'][idx_temp_TR])
match2_TR_R_temp=set(joint_data['DrugNo'][idx_temp_TR])

# Shepherd and Reprotox
idx_temp_SR = [all(idx) for idx in zip(ReproSumIdx,ShepSumIdx ,[not i for i in TerisNotesIdx])]
match2_SR_S_temp=set(joint_data['ShepAgentName'][idx_temp_SR])
match2_SR_R_temp=set(joint_data['DrugNo'][idx_temp_SR])


# 3 summaries
match3_T= match3_temp_T | (match2_TS_T_temp & match2_TR_T_temp)
match3_R= match3_temp_R | (match2_SR_R_temp & match2_TR_R_temp)
match3_S= match3_temp_S | (match2_TS_S_temp & match2_SR_S_temp)

# 2 summaries
match2_TS_T=match2_TS_T_temp-match3_T
match2_TS_S=match2_TS_S_temp-match3_S

match2_TR_T=match2_TR_T_temp-match3_T
match2_TR_R=match2_TR_R_temp-match3_R

match2_SR_S=match2_SR_S_temp-match3_S
match2_SR_R=match2_SR_R_temp-match3_R

# only 1 summary
match1_T=TerisAgent-match3_T-match2_TS_T-match2_TR_T
match1_R=ReproNo-match3_R-match2_TR_R-match2_SR_R
match1_S=ShepAgent-match3_S-match2_TS_S-match2_SR_S

# print results
print len(match3_T),len(match3_S),len(match3_R)
print len(match2_TS_T),len(match2_TS_S)
print len(match2_TR_T),len(match2_TR_R)
print len(match2_SR_S),len(match2_SR_R)
print len(match1_T),len(match1_S),len(match1_R)

