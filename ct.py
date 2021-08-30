import numpy
from decimal import *
import networkx as nx
import matplotlib.pyplot as plt
import hoprsim



stake = [
   [0, 2, 0, 0, 0, 0, 8, 0, 12, 0,1], 
   [0, 0, 1, 0, 0, 0, 0, 7, 0, 0,2], 
   [0, 11, 0, 1, 0, 0, 8, 0, 0, 0,0], 
   [0, 2, 0, 0, 0, 0, 8, 0, 0, 0,0],
   [0, 0, 2, 0, 0, 0, 0, 13, 0, 0,0],
   [0, 0, 0, 14, 9, 0, 0, 5, 0, 0,4], 
   [0, 0, 0, 23, 6, 0, 0, 0, 9, 0,0],
   [0, 2, 0, 11, 0, 0, 3, 0, 0, 20,13], 
   [0, 0, 0, 0, 10, 0, 5, 0, 0, 0,3], 
   [0, 3, 5, 0, 0, 7, 0, 1, 9, 0,0] ,
   [0, 3, 21, 3, 11, 7, 7, 1, 9, 8,0] 
]



'''
stake = [
   [0, 20, 0, 2], 
   [0, 0, 5, 1], 
   [0, 0, 0, 0],
   [0, 5, 4, 0]
]
'''
#stake = hoprsim.setupStake(20, 3, 20, 10, 100000, 0.1)
importance = hoprsim.calcImportance(stake)
# print("importance ", importance)
sortedPrioList = [i[0] for i in sorted(enumerate(importance), key=lambda x:x[1], reverse=True)]
print("sortedPrioList", sortedPrioList)

   
   

ctChannel = [0] * len(stake)
balancePerCtChannel = 5
hops = 3
n = len(stake)

#ctChannelBalances, ctNodeBalance = hoprsim.openInitialCtChannels(ctNodeBalance, balancePerCtChannel, importance)
#print("channel balances", ctChannelBalances)
numTests = 10
totalPayout = [0] * len(stake)
totalCtNodes = [0] * numTests
ctNodeBalance = 50
payoutPerHop = 1


for w in range(numTests):
   remainingctNodeBalance = ctNodeBalance
   ctChannelBalances, remainingctNodeBalance = hoprsim.openInitialCtChannels(ctNodeBalance, balancePerCtChannel, importance)
   importanceTmp = list(importance)
   # print("CT channel balances", ctChannelBalances)

   # remove all importance entries for nodes to which CT node has no open channels
   for i in range(len(stake)):
      if ctChannelBalances[i] == 0 :
         importanceTmp[i] = 0

   pathIndices = [0] * hops
   nodePayout = [0] * n
   for j in range (hops):
      pathIndices[j] = hoprsim.randomPickWeightedByImportance(importanceTmp)
      print("importance", importance)
      print("path", pathIndices[j])
      # reset importance
      importanceTmp = list(importance)
      #print("importance", importanceTmp)
      

      # give equal payout 1 HOPR reward to nodes selected in the path
            
      nodePayout[pathIndices[j]] += payoutPerHop
      totalPayout[pathIndices[j]] += payoutPerHop
      dele = int(pathIndices[j])
      importanceTmp[dele] = 0
   
      # remove importance entries for nodes to which current hop has no open channels
      for i in range(len(stake)):
         if stake[dele][i] == 0 :
            importanceTmp[i] = 0
   # create node payout per node 
   totalCtNodes[w] = pathIndices
   #print("nodes Payout", nodePayout) 
print("path indices:", pathIndices)
   # find which nodes node j has open channels with. First time this test goes through, the node chosen should be the one with more nodes connected to it and more importance
listImp = []
path = sorted(pathIndices)
print("path", path)
for i in range(len(stake)):
   s = []
   v = []
   if i in path : 
      for j in range(len(stake)): 
         row = stake[i][:]
         col = stake[:][j]
  
         if (row[j] != 0):
            s.append(j)
            g= set(s) 
            for k in range(len(stake)):
                if (col[k] != 0):
         
        
                   v.append(k)
                   q= set(v) 
       
       
      #arr= numpy.array(row[j])
      #is_all_zero = numpy.all((arr == 0))

      #if is_all_zero:
        # g = []
      #print("list s",i, g)  
      print("list s",i, q) 
        

      #for e in range(len(g)):
      sumImportance = 0
      for p in q:
         sumImportance += importance[p]

      print("sum Importance", sumImportance)
      # Now we add those sum of importances of other nodes to each of the path nodes to a list and then we compare them
      # the node from the path that has the largest importance of other nodes with whom it has open channels with is the most strategic one 
      listImp.append(sumImportance)

print("list", listImp)

# find the maximum importance value in this list
indices = [i for i, x in enumerate(listImp) if x == max(listImp)]


for i in indices:
   for j in indices:
      if (importance[path[i]] > importance[path[j]]):
         maxIndex = i 
print("Best node", path[maxIndex])



      
      

# Strategy: consider node's importance as a parameter, the open channels it has with other nodes and their importance
#for i in range (len(importance)):
  #if importance[i] !=  0 :
       





# node with highest payout or a pretty high payout and smaller stake is a positive outlier
l = []
r =  []

for i in range (len(totalPayout)):
   #  find the best positive outlier
   if totalPayout[i] == max(totalPayout):
      bestNode = i
   
   for j in range (len(totalPayout)):
       if (totalPayout[j] > totalPayout[i] and importance[j]< importance[i]):
         l.append(j) 
   m= set(l) 
print("positive outliers", m)          
print("Node with highest payout", bestNode)



# now that we know who is the best node (meaning the one with largest payout) we can find out why did it receive more payout than others?
# Is is because it has the largest importance? --> Not necessarly. We have seen in some test cases that outlier nodes with less importance can receive largest Payout
# Then it must be because it has more open channels with important nodes than others
 




#print("stake:")
#hoprsim.printArray2d(stake)
stakeCopy = stake[:]
#print("stakeCopy", stakeCopy)

print("payout", totalPayout)

totalStake = numpy.sum(stake, axis=1)
#print("total stake:")
#hoprsim.printArray1d(totalStake)

print("importance", importance)
# exp node 2 has been chosen 20 times for example  
#table = [['Node's importance', 'total Payout']]
#print("table", table)
#accuracyAverage = [0.51,0.52,0.64,0.57,0.7,0.63,0.59,0.66,0.64]






hoprsim.drawGraph(stake)
plt.figure(2)

minMarkerSize = 2
maxMarkerSize = 20
normalizedImportance = [0] * len(importance)
minImportance = min(importance)
maxImportance = max(importance)
for x in range(len(importance)):
    normalizedImportance[x] = float((importance[x] - minImportance) / (maxImportance - minImportance) * (maxMarkerSize - minMarkerSize) + minMarkerSize)
print("normalizedImportance", normalizedImportance)


for x, y, size, text in zip(totalStake, totalPayout, normalizedImportance, range(len(stake))):
    plt.plot(x, y, ms=size, marker='o', color='r', linestyle='None')
    plt.text(x, y, text)
plt.title('Stake vs payout')
plt.xlabel('Stake')
plt.ylabel('Payout')
#plt.yscale('log')
#plt.xscale('log')
plt.show()

