# import hoprsim
#stake = [
#    [0, 400, 400, 400],
#    [400, 0, 400, 400],
#    [400, 400, 0, 400],
#    [400, 400, 400, 0]
#]
#hoprsim.drawGraph(stake)

import networkx as nx
import matplotlib.pyplot as plt
import numpy
from decimal import *

#setting up a global stake value given to each node
stakePerNode = 400
# setting up a stake matrix for a user-defined number of nodes
# random number of channels per node between min and max params

def setupStake(
        numNodes=10,
        minChannelsPerNode=2,
        maxChannelsPerNode=7,
        tokensPerTicket=0.1
    ):

    stake = [[0 for i in range(numNodes)] for j in range(numNodes)]
    for x in range(numNodes):
        # get equal stake per node 
        myFunds = stakePerNode 

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



# selects a random payment channel
# weights: list of likelihoods that each entry is selected. This list does not need to be normalized to 1
# weightIndexToNodeLUT: look up table translating the position in the weights list to a node number (e.g. in stake matrix)
# returns: node number that has been selected
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




# takes the stake matrix as parameter and returns list of balances, counter party ids (same as state matrix) and p(n)
# as defined in CT draft proposal
def openCtChannels(stake):
    # initialize CT values
    # maximal number of channels that a CT node can maintain
    maxCtChannels = 4
    # number of tokens that CT node can stake in their channels
    tokensToStake = Decimal("1000")
    # each winning ticket costs this many tokens
    tokensPerTicket = Decimal("0.1")
    # probability that a certain ticket is a win (1 = 100%)
    winningProbability = 1

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
    ctChannelBalance = [0] * maxCtChannels # amounts in payment channels that CT node opens
    ctChannelParty = [0] * maxCtChannels # counterparty of payment channel that CT node opens
    for i in enumerate(topStakeAmounts):
        #print("allocation: ", i)
        #print("tokens left: ", tokensLeft, ", stake left: ", stakeLeft)
        # calculate token allocation for node (non-rounded)
        nonRoundedAllocation = i[1] / stakeLeft * tokensLeft

        #print("non-rounded allocation: ", nonRoundedAllocation)
        # calculate rounded payout
        roundedAllocation = int(nonRoundedAllocation/tokensPerTicket) * tokensPerTicket
        ctChannelBalance[i[0]] = roundedAllocation
        ctChannelParty[i[0]] = topStakeIndices[i[0]]
        tokensLeft -= roundedAllocation
        stakeLeft -= i[1]
        tickets = 10*setupStake()
        packets = tickets
        #print("rounded allocation: ", roundedAllocation)

    #print("--> channels opened to nodes: ", ctChannelParty)
    #print("--> channel allocations: ", ctChannelBalance)
    #print("CT priority list: ", ctPriorityList)
    # TODO for performance improvements in a real network with many small nodes, remove empty channels that did not receive any stake after rounding down
    return ctChannelBalance, ctChannelParty, ctPriorityList, packets

def numPackets (stake):


     #For x in range(numNodes):
     #we recover the number of stake given to each party
    #stake = setupStake()
    #each token is represented by 1 HOPR and there are 0.1 tokens in each ticket which means 1 token needs 10 tickets
    tickets = 10*stakePerNode
    packets = tickets
    return packets

def drawGraph(stake):
    """
    draws a network graph based on a square stake matrix with 0-diagonale
    the stake matrix has channel opener in rows and counterparty in columns
    each entry in the stake matrix represents the value staked in channel (0 for no channel)
    
    Parameters
    ----------
    stake: stake matrix
    """
    # parameters for drawing
    minLineWeight = 1
    maxLineWeight = 4
    blue1 = '#0000b4'
    blue2 = '#b4f0ff'
    blue3 = '#000050'
    blue4 = '#3c64a5'
    yellow = '#ffffa0'
    edgeColorA = blue1
    edgeColorB = blue4
    nodeColor = yellow
    nodeSize = 500
    labelFont = 'Source Code Pro'
    connectionstyle = 'arc3, rad=0.0'
    arrowstyle = '->'
    # /parameters

    G=nx.OrderedDiGraph()
    stake1d = numpy.concatenate(stake)
    maxS = max(stake1d)
    minS = min(stake1d[numpy.nonzero(stake1d)])
    bottomEdges = []
    topEdges = []
    bottomWeights = []
    topWeights = []
    bottomColors = []
    topColors = []
    print("maxS: ", maxS)
    print("minS: ", minS)

    for x in range(len(stake)):
        for y in range(x):
            weightA = 0
            weightB = 0
            if(stake[x][y] > 0):
                weightA = (stake[x][y] - minS) / (maxS - minS) * (maxLineWeight - minLineWeight) + minLineWeight
                G.add_edge(x, y, weight=weightA, color=edgeColorA)
            if(stake[y][x] > 0):
                weightB = (stake[y][x] - minS) / (maxS - minS) * (maxLineWeight - minLineWeight) + minLineWeight
                G.add_edge(y, x, weight=weightB, color=edgeColorB)

        # plot in the right order to have the fatter edge on the bottom 
            if(weightA > 0 and weightB > 0):
                if(weightA > weightB):
                    bottomEdges.append((x,y))
                    topEdges.append((y,x))
                    bottomWeights.append(weightA)
                    topWeights.append(weightB)
                    bottomColors.append(edgeColorA)
                    topColors.append(edgeColorB)
                else:
                    bottomEdges.append((y,x))
                    topEdges.append((x,y))
                    bottomWeights.append(weightB)
                    topWeights.append(weightA)
                    bottomColors.append(edgeColorB)
                    topColors.append(edgeColorA)
            elif(weightA > 0):
                topEdges.append((x,y))
                topWeights.append(weightA)
                topColors.append(edgeColorA)
            elif(weightB > 0):
                topEdges.append((y,x))
                topWeights.append(weightB)
                topColors.append(edgeColorB)

    weights = list(nx.get_edge_attributes(G,'weight').values())
    colors = list(nx.get_edge_attributes(G,'color').values())
    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=nodeSize, node_color=nodeColor)
    nx.draw_networkx_labels(G, pos, font_family=labelFont)
    nx.draw_networkx_edges(
        G,
        pos=pos,
        width=bottomWeights,
        edge_color=bottomColors,
        edgelist=bottomEdges,
        arrows=True,
        connectionstyle=connectionstyle,
        arrowstyle=arrowstyle
    )
    nx.draw_networkx_edges(
        G,
        pos=pos,
        width=topWeights,
        edge_color=topColors,
        edgelist=topEdges,
        arrows=True,
        connectionstyle=connectionstyle,
        arrowstyle=arrowstyle
    )

    plt.show()
