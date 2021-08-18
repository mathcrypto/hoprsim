# import hoprsim
import networkx as nx
import matplotlib.pyplot as plt
import numpy
from decimal import *


# setting up a stake matrix for a user-defined number of nodes
# random number of channels per node between min and max params

def setupStake(
        # Number of nodes in the network. This number can be changed to test with small and large network size
        numNodes=100,
        # the minimum number of channels a node can open
        minChannelsPerNode=2,
        # the maximum number of channels a node can open 
        maxChannelsPerNode=10,
        minFundsPerNode=10,
        maxFundsPerNode=100,
        tokensPerTicket=0.1
    ):

    stake = [[0 for i in range(numNodes)] for j in range(numNodes)]
    for x in range(numNodes):
        # each node is given a random funding amount
        myFunds = numpy.random.rand() * (maxFundsPerNode - minFundsPerNode) + minFundsPerNode

        # get random number of channels per node
        myChannels = int(numpy.random.rand() * (maxChannelsPerNode - minChannelsPerNode + 1) + minChannelsPerNode)
       
        # This value represents the amount each node stakes in their channel
        # It is computed as the number of funds a node has divided by number of channels they open
        stakePerChannel = myFunds / myChannels
        stakePerChannel = int(stakePerChannel / tokensPerTicket) * tokensPerTicket

        # fund channels by writing into stake matrix
        for c in range(myChannels):
            # TODO: this does not prevent a node from opening a channel to the same counterparty multiple times
            counterparty = int(numpy.random.rand() * (numNodes - 1))

            # cannot open channel to self - keep diagonal of matrix at 0
            if counterparty >= x:
                counterparty = counterparty + 1
            stake[x][counterparty] = stakePerChannel
            stake = [[Decimal(i) for i in j] for j in stake]
    return stake

def selectChannel(weights, weightIndexToNodeLUT):
    rand = numpy.random.rand()
    totalWeight = sum(weights)
    sumWeights = 0
    counterparty = -1
    for i in enumerate(weights):
        sumWeights += i[1]
        if sumWeights / totalWeight >= rand:
            counterparty = weightIndexToNodeLUT[i[0]]
            #print("selected counterparty: ", counterparty)
            break;
    if counterparty == -1:
        counterparty = weightIndexToNodeLUT[len(weights) - 1]
        #print("selected last counterparty", counterparty)
    return counterparty



# opens a random payment channel
# takes the stake matrix as parameter and returns list of balances and counter party ids
def openCtChannels(stake):
 
    # number of channels we want to open
    maxCtChannels = 7

    # stake value for each opened channel. we fix this value for testing purposes
    channelStake= 5

    # get total stake per node
    stakePerNode = [Decimal(sum(e)) for e in stake]

    totalStake = sum(stakePerNode)
   
    otherTotalStake = [totalStake - i for i in stakePerNode]
    n = len(stake)
    weight = [0] * n
    importance = [0] * n
    for x in range(n):
        for y in range(n):
            # weight of a node is 0 if its stake is equal to 0
            #weight(channel) = sqrt(balance(channel) / stake(channel.source) * stake(channel.destination))
            weight[y] += 0 if stakePerNode[y]==0 else numpy.sqrt(stake[y][x]/stakePerNode[y] * stakePerNode[x])

    print("Weighted downstream stake per node p(n) = ", weight)
    ctImportanceList = numpy.array(weight) * numpy.array(stakePerNode)
    #print("Priority list for cover traffic allocation a(n) = ", ctImportanceList)

    # find top maxCtChannels to which CT node should open channel directly
    sortedPrioList = [i[0] for i in sorted(enumerate(ctImportanceList), key=lambda x:x[1], reverse=True)]

    ##selectChannel(sortedPrioList,  )
    topStakeIndices = sortedPrioList[-maxCtChannels:]
    topStakeAmounts = [ctImportanceList[i[1]] for i in enumerate(topStakeIndices)]
    print("topStakeIndices:", topStakeIndices)
    #print(sortedPrioList)
    ctChannelBalance = [0] * maxCtChannels 
    ctChannelParty = [0] * maxCtChannels # counterparty of payment channel that CT node opens
    for i in enumerate(topStakeAmounts):
        ctChannelBalance[i[0]] = channelStake # every channel is funded with same amount

        # channel opening is randomized
        #ctChannelParty[i[0]] = int(numpy.random.rand() *(topStakeIndices[i[0]]))
        ctChannelParty[i[0]] = int(numpy.random.rand() * (sortedPrioList[i[0]]))
        print("--> sorted priority list: ", sortedPrioList[i[0]])

    # all the nodes with non zero stake amount to whom payment channels have been opened  
    print("--> channels opened to nodes: ", ctChannelParty)
    #print("--> channel allocations: ", ctChannelBalance)
    print("CT priority list: ", ctImportanceList)
    return ctChannelBalance, ctChannelParty, ctImportanceList
