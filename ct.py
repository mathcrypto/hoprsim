# run from CLI via exec(open("ct.py").read())

import numpy
from decimal import *
import networkx as nx
import matplotlib.pyplot as plt
import hoprsim

# rows in channel stake matrix are funders
# columns are counterparty
# diagonal has to be empty as node cannot fund channel to self
# value 1 in second value of first row means node A staked 1 HOPR in channel with B


stake = hoprsim.setupStake(15, 2, 8)
#print("stake matrix: ", numpy.matrix(stake))

ctChannelBalance, ctChannelParty, ctPriorityList = hoprsim.openCtChannels(stake)
#print("parties: ", ctChannelParty)
#print("balances: ", ctChannelBalance)
#print("priorities:", ctPriorityList)
# loop for each CT packet

pathLength = 3
totalP = sum(ctPriorityList)

# map random number onto the stake distribution of the current node (starting with CT node)
count = [0] * len(stake)
for i in range(1000):
    counterparty = hoprsim.selectChannel(ctChannelBalance, ctChannelParty)
    count[counterparty] += 1

#print("distribution: ", count)

counterparty = hoprsim.selectChannel(ctChannelBalance, ctChannelParty)
#print("first counterparty: ", counterparty)

# loop over up to 3 intermediate hops
# map random number onto the normalized stake distribution p(n)
rand = numpy.random.rand()

availableChannels = [i for i, element in enumerate(stake[counterparty]) if element!=0]
#print("available channels: ", availableChannels)

# sum up total P of all available channels
totalPOfCounterparty = sum([ctPriorityList[i] for i in availableChannels])
#print("total P of counterparty: ", totalPOfCounterparty)

weights = [ctPriorityList[i] for i in availableChannels]
#print("weights: ", weights)

counterparty = hoprsim.selectChannel(weights, availableChannels)
print("next counterparty: ", counterparty)

# if outgoing stake < incoming stake, abort

# consider downtime distribution per node, try forwarding packet to next node, update tickets

# choose timeout until next packet is sent based on rewards that are to be distributed over time

# plot output of tickets after 10 iterations

hoprsim.drawGraph(stake)































