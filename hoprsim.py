# import hoprsim



import networkx as nx
import matplotlib.pyplot as plt
import numpy
from decimal import *


# setting up a stake matrix for a user-defined number of nodes
# random number of channels per node between min and max params

def setupStake(
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
     
        myFunds = numpy.random.rand() * (maxFundsPerNode - minFundsPerNode) + minFundsPerNode

        # get random number of channels per node
        myChannels = int(numpy.random.rand() * (maxChannelsPerNode - minChannelsPerNode + 1) + minChannelsPerNode)
       

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



# opens a random payment channel
# takes the stake matrix as parameter and returns list of balances, counter party ids (same as state matrix) and p(n)
def openCtChannels(stake):
    # initialize CT values
    # number of channels that a CT node can maintain
    maxCtChannels = 100
    # number of tokens that CT node can stake in their channels
    tokensToStake = Decimal("5")
    # each winning ticket costs this many tokens
    tokensPerTicket = Decimal("0.1")
    # probability that a certain ticket is a win (1 = 100%)
    winningProbability = 0.1

    # get total stake per node
    stakePerNode = [Decimal(sum(e)) for e in stake]

    totalStake = sum(stakePerNode)
    # stakePerNode = numpy.divide(stakePerNode, totalStake)
    #print("Total stake per node s(n) = ", stakePerNode)
    #print("Total stake in network: ", totalStake)
    otherTotalStake = [totalStake - i for i in stakePerNode]
    #print("other: ", otherTotalStake)

    # get weighted downstream stake which weights the sum of all downstream stakes of a node with the fraction of the node staked towards that downstream node
    # (nan = 0, inf = biggest possible number)
    # weightedDownstreamStake = sumOverAllC( sqrt(stake(n,c) / s(n)) * s(c) / other(n) )

    n = len(stake)
    weightedDownstreamStake = [0] * n
    for x in range(n):
        for y in range(n):
            weightedDownstreamStake[y] += 0 if stakePerNode[y]==0 else numpy.sqrt(stake[y][x]/stakePerNode[y] * stakePerNode[x]/otherTotalStake[y])

    #print("Weighted downstream stake per node p(n) = ", weightedDownstreamStake)

    # the priority list is p(n) in CT draft specification
    ctPriorityList = numpy.array(weightedDownstreamStake) * numpy.array(stakePerNode)
    #print("Priority list for cover traffic allocation a(n) = ", ctPriorityList)

    # find top maxCtChannels to which CT node should open channel directly
    sortedPrioList = [i[0] for i in sorted(enumerate(ctPriorityList), key=lambda x:x[1], reverse=True)]

    topStakeIndices = sortedPrioList[-maxCtChannels:]
    topStakeAmounts = [ctPriorityList[i[1]] for i in enumerate(topStakeIndices)]

    #print(sortedPrioList)
    # calculate total stake in top maxCtChannels
    totalTopStake = sum(topStakeAmounts)

    # allocate tokensToStake to the top most staked maxCtChannels nodes
    # round to tokensPerTicket and deal with rounding errors by using the Kahan Summation
    # ordering of entries should be randomized to prevent users from positioning themselves at the right spot with small stake and benefit from receiving a channel

    tokensLeft = tokensToStake # tokens that are left to be distributed
    stakeLeft = totalTopStake # stake that is left to be processed
    ctChannelBalance = [0] * maxCtChannels 
    ctChannelParty = [0] * maxCtChannels # counterparty of payment channel that CT node opens
    for i in enumerate(topStakeAmounts):
        #print("allocation: ", i)
        #print("tokens left: ", tokensLeft, ", stake left: ", stakeLeft)
        # calculate token allocation for node (non-rounded)
        nonRoundedAllocation = i[1] / stakeLeft * tokensLeft

        #print("non-rounded allocation: ", nonRoundedAllocation)
        # calculate rounded payout
        roundedAllocation = int(nonRoundedAllocation/tokensPerTicket) * tokensPerTicket
        ctChannelBalance[i[0]] = 5  # every channel is funded with same amount
        ctChannelParty[i[0]] = topStakeIndices[i[0]]
     
    
    return ctChannelBalance, ctChannelParty, ctPriorityList
