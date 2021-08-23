import numpy
from decimal import *
import networkx as nx
import matplotlib.pyplot as plt
import hoprsim



stake = [
   [0, 2, 0, 0, 0, 0, 8, 0, 12, 0], 
   [0, 0, 1, 0, 0, 0, 0, 7, 0, 0], 
   [0, 11, 0, 1, 0, 0, 8, 0, 0, 0], 
   [0, 2, 0, 0, 0, 0, 8, 0, 0, 0],
   [0, 0, 2, 0, 0, 0, 0, 13, 0, 0],
   [0, 0, 0, 14, 9, 0, 0, 5, 0, 0], 
   [0, 0, 0, 23, 6, 0, 0, 0, 9, 0],
   [0, 2, 0, 11, 0, 0, 3, 0, 0, 20],
   [0, 0, 0, 0, 10, 0, 5, 0, 0, 0], 
   [0, 3, 5, 0, 0, 7, 0, 1, 9, 0]  
]

'''
stake = [
   [0, 200, 0], 
   [0, 0, 10], 
   [0, 1, 0]
]
'''

importance = hoprsim.calcImportance(stake)
print("importance ", importance)
sortedPrioList = [i[0] for i in sorted(enumerate(importance), key=lambda x:x[1], reverse=True)]
print("sortedPrioList", sortedPrioList)



ctChannel = [0] * len(stake)
balancePerCtChannel = 500
ctNodeBalance = 1000
#balancePerCtChannel = 5
ctChannelBalances, ctNodeBalance = hoprsim.openInitialCtChannels(ctNodeBalance, balancePerCtChannel, importance)
print("channel balances", ctChannelBalances)
print("remaining ct node balance: ", ctNodeBalance)


#for w in range(4):
for i in range(len(stake)):
   if ctChannelBalances[i] == 0 :
      importance[i] = 0
         
   hops = 3
   ctNode = [0] * hops 
   #table = [0] * 3
for j in range (hops):
   ctNode[j] = hoprsim.randomPickWeightedByImportance(importance) 
   importance = hoprsim.calcImportance(stake)
   # give away 1 HOPR reward to nodes selected in the path
   nodePayout = ctChannelBalances
   #nodePayout[ctNode[j]] = ctChannelBalances[ctNode[j]]
   nodePayout[ctNode[j]] += 1
   #print("Node's balance after reward", nodePayout[ctNode[j]])
   #print("Node's balance ", ctChannelBalances[j])
   dele = int(ctNode[j])
   importance[dele] = 0
   #print("channel balances", ctChannelBalances)
   
      
   
   for i in range(len(stake)):
      if stake[dele][i] == 0 :
         importance[i] = 0
print("ctNode", ctNode)
print("channel balances", nodePayout)
   
#table = [['w', 'ctNodes', 'ctChannelBalances'], [w, ctNode, ctChannelBalances]]
#print("table", table)
 



