# 12/16 新しく作った　pruningの関数とrandomを実装
import copy
import time
import json
import datetime
import random
from new_method_geier_3 import point
from new_method_geier_3 import make_infoset_3
from new_method_geier_3 import rank
from new_method_geier_3 import get_default_util
from new_method_geier_3 import judge
from new_method_geier_3 import make_action
from new_CFR_node import Node

def train_cfr(iterations, players, file1, file2, NA, digit, nodeMap, strategy_interval, c, prune_threshold, LCFR_threshold, Discount_Interval):
    util = {'0' : 0, '1' : 0, '2' : 0}
    strategyMap = {}
    start = time.time()
    default_util = get_default_util(players)
    for t in range(iterations):
        for i in range(players):            
            # if t % strategy_interval == 0 :
            #     history = {'open': [],   'point':[0 for _ in range(players)], 'private': [list(range(1,NA+1)) for _ in range(players)], 'next_reward' : 0}
            #     rewards = list(range(1,NA+1))
            #     random.shuffle(rewards)
            #     update_strategy
            history = {'open': [],   'point':[0 for _ in range(players)], 'private': [list(range(1,NA+1)) for _ in range(players)], 'next_reward' : 0}
            rewards = list(range(1,NA+1))
            # random.shuffle(rewards)
            p_list = [1 for _ in range(players)]
            if t > prune_threshold:
                r = random.random()
                if r < 0.05:
                    util[str(i)] += cfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, False)
                else:
                    util[str(i)] += cfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, False)
            else:
                    util[str(i)] += cfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, False)
        # if t < LCFR_threshold and t % Discount_Interval == 0:
        #     d = ( t / Discount_Interval) / (t / Discount_Interval + 1 )
        #     for i in range(players):   
    elapsed_time = time.time() - start
    with open(file1, 'a') as f:
        print('elapsed_time: ' + str(elapsed_time),file=f)
    return util

## 12/16 pluribusのMCCFRを参考にして実装
def train_mccfr(iterations, players, file1, file2, NA, digit, nodeMap, strategy_interval, c, prune_threshold, LCFR_threshold, Discount_Interval):
    util = {'0' : 0, '1' : 0, '2' : 0}
    strategyMap = {}
    start = time.time()
    default_util = get_default_util(players)
    for t in range(iterations):
        for i in range(players):            
            # if t % strategy_interval == 0 :
            #     history = {'open': [],   'point':[0 for _ in range(players)], 'private': [list(range(1,NA+1)) for _ in range(players)], 'next_reward' : 0}
            #     rewards = list(range(1,NA+1))
            #     random.shuffle(rewards)
            #     update_strategy
            history = {'open': [],   'point':[0 for _ in range(players)], 'private': [list(range(1,NA+1)) for _ in range(players)], 'next_reward' : 0}
            rewards = list(range(1,NA+1))
            # random.shuffle(rewards)
            p_list = [1 for _ in range(players)]
            if t > prune_threshold:
                r = random.random()
                if r < 0.05:
                    util[str(i)] += mccfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, False)
                else:
                    util[str(i)] += mccfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, False)
            else:
                    util[str(i)] += mccfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, False)
        # if t < LCFR_threshold and t % Discount_Interval == 0:
        #     d = ( t / Discount_Interval) / (t / Discount_Interval + 1 )
        #     for i in range(players):   
    elapsed_time = time.time() - start
    with open(file1, 'a') as f:
        print('elapsed_time: ' + str(elapsed_time),file=f)
    return util

        
# ## 結果を見やすく出力する関数　ハゲタカがランダムじゃなかった時
# def display_order(iterations, players,util, digit, file1, file2, NA, nodeMap):
#     with open(file1, 'a') as f:
#         for i in range(players):
#             print("Average game values for player " + str(i) + ' : ' + str(round(util[str(i)] / iterations, digit)) , file = f)
#         a = [[] for _ in range(players * NA)]
#         for n in nodeMap.values():
#             if len(n.infoSet) == 2:
#                 a[0].append(n.infoSet)
#             for i in range(1, players * NA):
#                 if len(n.infoSet) == 3 * i:
#                     a[i].append(n.infoSet)
#         for i in range(len(a)):
#             for j in a[i]:
#                 print(nodeMap[j].toString(),file=f)

## 結果を見やすく出力する関数　ハゲタカがランダム
def display_order_random(iterations, players,util, digit, file1, file2, NA, nodeMap):
    with open(file1, 'a') as f:
        for i in range(players):
            print("Average game values for player " + str(i) + ' : ' + str(round(util[str(i)] / iterations, digit)) , file = f)
        n_count = 0
        update_count_sum = 0
        for n in nodeMap.values():
            update_count_sum += n.update_count
            n_count += n.count
        print("Strategy update  " + str(update_count_sum), file = f)
        print("node count  " + str(n_count), file = f)
        a = [[] for _ in range(players * NA)]
        for n in nodeMap.values():
            if len(n.infoSet) == 6:
                a[0].append(n.infoSet)
            elif len(n.infoSet) == 7:
                a[1].append(n.infoSet)
            elif len(n.infoSet) == 10:
                a[2].append(n.infoSet)
            for i in range(1, NA -1):
                for j in range(NA):
                    if len(n.infoSet) == 16 + 12 * (i - 1) + 3 * j:
                        a[i * players + j].append(n.infoSet)
        for i in range(len(a)):
            for j in a[i]:
                print(nodeMap[j].toString(),file=f)

## 学習したnodeをjson形式で書き込む関数
def dump_hash(file3, nodeMap):
    has = {}
    for k in nodeMap.keys():
        has[k] = nodeMap[k].toHash()
    with open(file3, 'a') as f:
        print(json.dumps(has), file = f)


def cfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, pruning_flg):
    ## 今nターン目
    n = len(history['open'])
    player = n % players

    # ゲームが終わっておらず、全員カードを出し終わったのなら自分と相手の出したカードに応じて得点計算
    if n > 0 and n % players == 0:
        point(history,players,NA,rewards)

    # 11/30手札があと1枚しかないなら、strategyは、必ず残っている手札の所だけが1になるので計算する必要もない。
    # ゲームが実質終了(全員手札が残り1枚しかなくなった時)
    if n == players * (NA - 1):
        ## openに残りの手札をそれぞれ追加する。
        for j in range(players):
            history['open'].append(history['private'][j][0])
        ## 終わったらjudgeする
        return judge(history, i, players, default_util)
        
    # infoSetを作成
    infoSet = make_infoset_3(history['open'], rewards)

    # nodeMapにinfosetが既にあるならそれを引っ張ってくる。なければ新たにつくる。
    if infoSet in nodeMap:
        node = nodeMap[infoSet]
    else:
        node = Node(history['private'][player], NA, digit)
        node.infoSet = infoSet
        nodeMap[infoSet] = node

    # strategyにinformationsetとtの変数要素を組み込ませるために追加 11/5 問題ないはず
    strategyKey = infoSet + ' : ' + str(t)
    if strategyKey in strategyMap:
        strategy = copy.deepcopy(strategyMap[strategyKey])
        
    else:
        strategyMap[strategyKey] = node.getStrategy()
        strategy = copy.deepcopy(strategyMap[strategyKey])

    ## 再帰の部分
    util = [0 for _ in range(NA)]
    nodeUtil = 0
    explored = [True for _ in range(NA)]
    node.count+=1
    for a in history['private'][player]:
        if node.regretSum[a-1] > c or (not pruning_flg):
            explored[a-1] = True
            ## 何回枝切り(pruning)されたかを数える。
            node.pruned_count[a-1] += 1
            nexthistory = copy.deepcopy(history)
            nexthistory['open'].append(a) 
            nexthistory['private'][player].remove(a) 
            p_list[player] *= strategy[a-1]
            util[a-1] = cfr(nexthistory, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, pruning_flg)
            nodeUtil += strategy[a-1] * util[a-1]
        else: 
            explored[a-1] = False
    if player == i:
        node.util += nodeUtil
        temp = copy.deepcopy(p_list)
        temp.pop(player)
        b = 1
        for j in temp:
            b *= j
        for a in history['private'][player]:
            if player == 0:
                node.regretSum[a-1] += ((p_list[1] * p_list[2]) * (util[a-1] - nodeUtil)) * t
                node.strategySum[a-1] += (p_list[0] * strategy[a-1])
            elif player == 1:
                node.regretSum[a-1] += ((p_list[0] * p_list[2]) * (util[a-1] - nodeUtil)) * t
                node.strategySum[a-1] += (p_list[1] * strategy[a-1])
            else:
                node.regretSum[a-1] += ((p_list[0] * p_list[1]) * (util[a-1] - nodeUtil)) * t
                node.strategySum[a-1] += (p_list[2] * strategy[a-1])
                node.update_count += 1
    strategyMap[infoSet + ' : ' + str(t + 1)]  = node.getStrategy()

    return nodeUtil


def mccfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, pruning_flg):
    ## 今nターン目
    n = len(history['open'])
    player = n % players

    # ゲームが終わっておらず、全員カードを出し終わったのなら自分と相手の出したカードに応じて得点計算
    if n > 0 and n % players == 0:
        point(history,players,NA,rewards)

    # 11/30手札があと1枚しかないなら、strategyは、必ず残っている手札の所だけが1になるので計算する必要もない。
    # ゲームが実質終了(全員手札が残り1枚しかなくなった時)
    if n == players * (NA - 1):
        ## openに残りの手札をそれぞれ追加する。
        for j in range(players):
            history['open'].append(history['private'][j][0])
        ## 終わったらjudgeする
        return judge(history, i, players, default_util)
        
    # infoSetを作成
    infoSet = make_infoset_3(history['open'], rewards)

    # nodeMapにinfosetが既にあるならそれを引っ張ってくる。なければ新たにつくる。
    if infoSet in nodeMap:
        node = nodeMap[infoSet]
    else:
        node = Node(history['private'][player], NA, digit)
        node.infoSet = infoSet
        nodeMap[infoSet] = node

    # strategyにinformationsetとtの変数要素を組み込ませるために追加 11/5 問題ないはず
    strategyKey = infoSet + ' : ' + str(t)
    if strategyKey in strategyMap:
        strategy = copy.deepcopy(strategyMap[strategyKey])
        
    else:
        strategyMap[strategyKey] = node.getStrategy()
        strategy = copy.deepcopy(strategyMap[strategyKey])

    ## 再帰の部分
    util = [0 for _ in range(NA)]
    nodeUtil = 0
    explored = [True for _ in range(NA)]
    node.count += 1
    # print(str(node.count) + " " + str(infoSet))
    if player == i:
        for a in history['private'][player]:
            if node.regretSum[a-1] > c or (not pruning_flg):
                explored[a-1] = True
                nexthistory = copy.deepcopy(history)
                nexthistory['open'].append(a) 
                nexthistory['private'][player].remove(a) 
                p_list[player] *= strategy[a-1]
                util[a-1] = mccfr(nexthistory, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util, c, pruning_flg)
                nodeUtil += strategy[a-1] * util[a-1]
            else: 
                explored[a-1] = False
                ## 何回枝切り(pruning)されたかを数える。
                node.pruned_count[a-1] += 1
        
        node.util += nodeUtil
        temp = copy.deepcopy(p_list)
        temp.pop(player)
        b = 1
        for j in temp:
            b *= j
        for a in history['private'][player]:
            if explored[a-1]:
                node.regretSum[a-1] += (b * (util[a-1] - nodeUtil)) * t
                node.strategySum[a-1] += (p_list[player] * strategy[a-1])
                node.update_count += 1
        strategyMap[infoSet + ' : ' + str(t + 1)]  = node.getStrategy()

        return nodeUtil

    else:
        a = make_action(strategy)
        nexthistory = copy.deepcopy(history)
        nexthistory['open'].append(a) 
        nexthistory['private'][player].remove(a) 
        p_list[player] *= strategy[a-1]
        return mccfr(nexthistory, i, t,  p_list, nodeMap, strategyMap, players, digit, file1, file2, rewards, NA, default_util , c, pruning_flg)   


