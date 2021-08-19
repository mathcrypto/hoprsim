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

importance = hoprsim.calcImportance(stake)
print("importance ", importance);

firstCtChannel = hoprsim.openCtChannels(importance)
print("firstCtChannel", firstCtChannel)

ctNodeBalance = 1000
balancePerCtChannel = 5
ctChannelBalances, ctNodeBalance = hoprsim.openInitialCtChannels(ctNodeBalance, balancePerCtChannel, importance)
print("channel balances", ctChannelBalances)
print("remaining ct node balance: ", ctNodeBalance)
