import numpy
from decimal import *
import networkx as nx
import matplotlib.pyplot as plt
import hoprsim


'''
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


importance = hoprsim.calcImportance(stake)
print("importance ", importance)
sortedPrioList = [i[0] for i in sorted(enumerate(importance), key=lambda x:x[1], reverse=True)]
print("sortedPrioList", sortedPrioList)



ctChannel = [0] * len(stake)
balancePerCtChannel = 500
hops = 3
n = len(stake)
#ctChannelBalances, ctNodeBalance = hoprsim.openInitialCtChannels(ctNodeBalance, balancePerCtChannel, importance)
#print("channel balances", ctChannelBalances)
 
for w in range(10):
   ctNodeBalance = 1000
   ctChannelBalances, ctNodeBalance = hoprsim.openInitialCtChannels(ctNodeBalance, balancePerCtChannel, importance)
   print("channel balances", ctChannelBalances)
   print("remaining ct node balance: ", ctNodeBalance)
  
   for i in range(len(stake)):
      if ctChannelBalances[i] == 0 :
         importance[i] = 0
   ctNode = [0] * hops     
   nodePayout = [0] * n
   for j in range (hops):
      ctNode[j] = hoprsim.randomPickWeightedByImportance(importance) 
      importance = hoprsim.calcImportance(stake)
      # give equal payout 1 HOPR reward to nodes selected in the path
            
      nodePayout[ctNode[j]] += 1
      dele = int(ctNode[j])
      importance[dele] = 0
   
      for i in range(len(stake)):
         if stake[dele][i] == 0 :
            importance[i] = 0

   print("nodes Payout", nodePayout) 
   print("ctNode", ctNode)
   
#table = [['w', 'ctNodes', 'ctChannelBalances'], [w, ctNode, ctChannelBalances]]
#print("table", table)
 



