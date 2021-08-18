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

# loop over up to 3 intermediate hops
pathLength = 3

# map random number onto the normalized stake distribution p(n)
rand = numpy.random.rand()

availableChannels = [i for i, element in enumerate(stake[counterparty]) if element!=0]
#print("available channels: ", availableChannels)


weights = [ctPriorityList[i] for i in availableChannels]
#print("weights: ", weights)
