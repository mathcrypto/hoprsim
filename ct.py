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
numTests = 10
totalPayout = [0] * numTests
totalCtNodes = [0] * numTests
ctNodeBalance = 1000

for w in range(numTests):
   remainingctNodeBalance = ctNodeBalance
   ctChannelBalances, ctNodeBalance = hoprsim.openInitialCtChannels(ctNodeBalance, balancePerCtChannel, importance)
   print("channel balances", ctChannelBalances)
   print("remaining ct node balance: ", remainingctNodeBalance)
  
   for i in range(len(stake)):
      if ctChannelBalances[i] == 0 :
         importance[i] = 0
   pathIndices = [0] * hops     
   nodePayout = [0] * n
   for j in range (hops):
      pathIndices[j] = hoprsim.randomPickWeightedByImportance(importance) 
      importance = hoprsim.calcImportance(stake)
      # give equal payout 1 HOPR reward to nodes selected in the path
            
      nodePayout[pathIndices[j]] += 1
      dele = int(pathIndices[j])
      importance[dele] = 0
   
      for i in range(len(stake)):
         if stake[dele][i] == 0 :
            importance[i] = 0
   # create node payout per node 
   #totalPayout[w] = nodePayout
   totalCtNodes[w] = pathIndices
   print("nodes Payout", nodePayout) 
   print("ctNode", pathIndices)
totalPayout = sum(nodePayout[w] for w in range (numTests))
print("payout", totalPayout)  
# exp node 2 has been chosen 20 times for example  
#table = [['total CT Nodes', 'total Payout'], [totalpathIndices, totalPayout]]
#print("table", table)
#accuracyAverage = [0.51,0.52,0.64,0.57,0.7,0.63,0.59,0.66,0.64]




