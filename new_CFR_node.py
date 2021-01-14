

# -*- coding: utf-8 -*-
class Node():
    def __init__(self, card_list,NA, digit):
        self.infoSet = ''
        self.util = 0
        self.count = 0
        self.NA = NA
        self.card_list = card_list
        self.regretSum =  [0 for _ in range(self.NA)]
        self.strategySum =  [0 for _ in range(self.NA)]
        self.digit = digit
        self.averageStrategy = [0 for _ in range(self.NA)]
        self.pruned_count = [0 for _ in range(self.NA)]
        self.update_count = 0
        
    ## regret matchingによって、strategyを求める関数  
    def getStrategy(self):
        normalizingSum = 0
        strategy =  [0 for _ in range(self.NA)]
        for a in self.card_list:
            strategy[a-1] = self.regretSum[a-1] if self.regretSum[a-1] > 0 else 0
            normalizingSum += strategy[a-1]
        
        for a in self.card_list:
            if normalizingSum > 0:
                strategy[a-1] /= normalizingSum
            else:
                strategy[a-1]  = 1.0 / len(self.card_list)
        
        return strategy 

    ## strategySumの要素の和を1にして、最終的な平均戦略を求める関数 
    ## 11/30 残りカードが1枚しかないなら、そこの要素だけ1のリストを返せば良い。例：残りの手札が2だけ → strategyは[0,1,0]
    def getAverageStrategy(self):
        if len(self.card_list) == 1:
            self.averageStrategy[self.card_list[0] - 1] = 1
            return self.averageStrategy
        normalizingSum = 0
        for a in range(self.NA):
            normalizingSum += self.strategySum[a]
            
        for a in self.card_list:
            if normalizingSum > 0:
                self.averageStrategy[a-1] = self.strategySum[a-1] / normalizingSum
            else:
                self.averageStrategy[a-1] = 1.0 / len(self.card_list)
        
        return self.averageStrategy
    
    ## 出力するための関数
    def toString(self):
        self.getAverageStrategy()
        avgStrategy = [round(self.averageStrategy[n], self.digit) for n in range(len(self.averageStrategy))]
        self.strategySum = [round(self.strategySum[n], self.digit) for n in range(len(self.strategySum))]
        self.regretSum = [round(self.regretSum[n], self.digit) for n in range(len(self.regretSum))]
        if self.count > 0:
            self.util = round(self.util / self.count, self.digit)
        return str(self.infoSet) + ' avgstrategy: ' + str(avgStrategy) + ' : ' +  str(self.util)  + ' regretSum: ' + str(self.regretSum)  + ' StrategySum: ' + str(self.strategySum)+ ' count: ' + str(self.count) + ' pruned_count: ' + str(self.pruned_count)

    ##hashとして保存するための関数
    def toHash(self):
        self.getAverageStrategy()
        node_hash = {}
        node_hash['infoSet'] = self.infoSet
        node_hash['avgStrategy'] = self.averageStrategy
        # node_hash['util'] = self.util
        # node_hash['regretSum'] = self.regretSum
        # node_hash['strategySum'] = self.strategySum
        # node_hash['pruned_count'] = self.pruned_count
        return node_hash
