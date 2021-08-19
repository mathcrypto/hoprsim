import numpy
from decimal import *
import networkx as nx
import matplotlib.pyplot as plt
import hoprsim


# the value 15 in setupStake function is number of nodes since we are testing for a small network size. This value can change of course to higher or smaller values
# The second and third values represent the minimum and maximum channels number
#stake = hoprsim.setupStake(3, 5, 5)
stake = [
   [0, 2, 0, 0],
   [0, 0, 1, 0],
   [0, 0, 0, 1],
   [0, 0, 0, 0]
]
#stake = [[Decimal(i) for i in j] for j in stake]
#print("stake", stake)
#
#define a stake manually and test with it 
#print("stake matrix: ", numpy.matrix(stake))

ctChannelBalance, ctChannelParty, ctImportanceList = hoprsim.openCtChannels(stake)

pathLength = 3


# map random number onto the stake distribution of the current node (starting with CT node)
count = [0] * len(stake)
for i in range(1000):
   counterparty = hoprsim.selectChannel(ctChannelBalance, ctChannelParty)
   count[counterparty] += 1

print("stake distribution: ", count)

counterparty = hoprsim.selectChannel(ctChannelBalance, ctChannelParty)
#print("first counterparty: ", counterparty)

