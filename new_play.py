# -*- coding: utf-8 -*-
import random
import copy
import datetime
import math
import time
import os
import json
from new_method_geier_3 import point
from new_method_geier_3 import make_infoset_3
from new_method_geier_3 import rank
from new_method_geier_3 import get_default_util
from new_method_geier_3 import judge
from new_method_geier_3 import make_action
from new_CFR_node import Node
from new_geier_player_3 import cfr
from new_geier_player_3 import mccfr
from new_geier_player_3 import train_cfr
from new_geier_player_3 import train_mccfr
from new_geier_player_3 import display_order_random
from new_geier_player_3 import dump_hash

NA = 4
players = 3
PlayerMap = {}
dt_now = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second) 
digit = 5
play_iterations = 100000
default_util = get_default_util(players)

file1 = "./対戦記録/4枚 MCCFR iteration少ない.txt"
# file2 = "/Users/hayashikippei/new_CFR/3_Geier/hash記録/NA_3/iterations: 1000002021-01-12 9:38:51.json"
file2 = "/Users/hayashikippei/Desktop/Experiment/Geier/hash記録/NA_4iterations: 10000 MCCFR.json"
f = open(file1, 'w')
f.close()
with open(file1, 'a') as f:
    print(file2, file = f)
    print("4枚 MCCFR そのまま対戦 play iterations: " + str(play_iterations), file = f)
## ファイルの先頭に何かコメントをつけるなら。
class Player():
    def __init__(self):
        self.util = 0
        self.strategy = [0] * NA
        self.nodeMap = {}
        self.random_flg = False

# strategyに応じてactionを決める。
    def make_action(self, card_list, infoSet):
        if self.random_flg or (not infoSet in self.nodeMap):
            return random.choice(card_list)
        self.strategy =  self.nodeMap[infoSet]['avgStrategy']
        r = random.random()
        sum = 0
        for i in range(len(self.strategy)):
            if sum < r < sum + self.strategy[i]:
                return i + 1
            sum += self.strategy[i]

# strategyとは逆のactionを出す
    def make_reverse_action(self, card_list, infoSet):
        # if self.random_flg:
        #     return random.choice(card_list)
        self.strategy =  self.nodeMap[infoSet]['avgStrategy']
        strategy = self.strategy
        normalizingSum = 0
        for i in card_list:
            strategy[i-1] = 1 - strategy[i-1]
            normalizingSum += strategy[i-1]
        for i in range(len(strategy)):
            strategy[i] /= normalizingSum
        r = random.random()
        sum = 0
        for i in range(len(strategy)):
            if sum < r < sum + strategy[i]:
                return i + 1
            sum += strategy[i]

##　一人をランダムプレイヤーに変更して対戦させる関数
def play():
    ##まず、人数分Playerクラスを作る。
    for i in range(players):
        PlayerMap['player_' + str(i)] = Player()
    for i in range(players):
        with open(file1, 'a') as f:
            print(str(i)  + "がランダム" , file=f)   
        PlayerMap['player_' + str(i)].random_flg = True
        temp = list(range(players))
        temp.pop(i)
        ## 学習ずみプレイヤーを用意
        for j in temp:
            with open(file2, 'r')as f:
                PlayerMap['player_' + str(j)].nodeMap = json.load(f)
        start = time.time()
        for t in range(play_iterations):
            history = {'open': [],   'point':[0 for _ in range(players)], 'private': [list(range(1,NA+1)) for _ in range(players)], 'next_reward' : 0}
            rewards = list(range(1,NA+1))
            random.shuffle(rewards)
            ## 持っているカードが２枚以上ある内はstrategyに応じて手を決める
            for i in range(players * (NA - 1)):
                player = len(history['open']) % players
                infoSet = make_infoset_3(history['open'], rewards)

                ## 行動を決定し、openに追加　card_listから消去
                a = PlayerMap['player_' + str(player)].make_action(history['private'][player], infoSet)
                history['open'].append(a)
                history['private'][player].remove(a)
                if len(history['open']) % players == 0:
                    point(history,players,NA,rewards)

            ## 上の繰り返しを終えて、持っているカードがみんな1枚になったら、自動的にopenに残りのカードを足していって最後のpointを計算
            for i in range(players):
                history['open'].append(history['private'][i][0])
                history['private'][i].pop(0)
            point(history,players,NA,rewards)

            ## それぞれ勝敗のutilを記録
            for i in range(players):
                PlayerMap['player_' + str(i)].util += judge(history, i, players, default_util)
                
        elapsed_time = time.time() - start
        ## 実行時間を記録
        with open(file1, 'a') as f:
            print('elapsed_time_for play: ' + str(round(elapsed_time,digit)),file=f)
        
        ##ゲームが終わったら、最終的な平均utilを出力
        for i in range(players):
            with open(file1, 'a') as f:
                print("Average game values for player " + str(i) + ' : ' + str(round(PlayerMap['player_' + str(i)].util / play_iterations , digit)) , file = f)

#学習した戦略そのままで学習させる関数
def play_2():
    ##まず、人数分Playerクラスを作る。
    for i in range(players):
        PlayerMap['player_' + str(i)] = Player()
    ## 学習ずみプレイヤーを用意
    for i in range(players):
        with open(file2, 'r')as f:
            PlayerMap['player_' + str(i)].nodeMap = json.load(f)
    start = time.time()
    for t in range(play_iterations):
        history = {'open': [],   'point':[0 for _ in range(players)], 'private': [list(range(1,NA+1)) for _ in range(players)], 'next_reward' : 0}
        rewards = list(range(1,NA+1))
        random.shuffle(rewards)
        ## 持っているカードが２枚以上ある内はstrategyに応じて手を決める
        for i in range(players * (NA - 1)):
            player = len(history['open']) % players
            infoSet = make_infoset_3(history['open'], rewards)

            ## 行動を決定し、openに追加　card_listから消去
            a = PlayerMap['player_' + str(player)].make_action(history['private'][player], infoSet)
            history['open'].append(a)
            history['private'][player].remove(a)
            if len(history['open']) % players == 0:
                point(history,players,NA,rewards)

        ## 上の繰り返しを終えて、持っているカードがみんな1枚になったら、自動的にopenに残りのカードを足していって最後のpointを計算
        for i in range(players):
            history['open'].append(history['private'][i][0])
            history['private'][i].pop(0)
        point(history,players,NA,rewards)

        ## それぞれ勝敗のutilを記録
        for i in range(players):
            PlayerMap['player_' + str(i)].util += judge(history, i, players, default_util)
            
    elapsed_time = time.time() - start
    ## 実行時間を記録
    with open(file1, 'a') as f:
        print('elapsed_time_for play: ' + str(round(elapsed_time,digit)),file=f)
    
    ##ゲームが終わったら、最終的な平均utilを出力
    for i in range(players):
        with open(file1, 'a') as f:
            print("Average game values for player " + str(i) + ' : ' + str(round(PlayerMap['player_' + str(i)].util / play_iterations , digit)) , file = f)


if __name__ == '__main__':
    play()
    with open(file1, 'a') as f:
        print(file = f)
    play_2()



#二人をらんだむいして対戦
def play_3():
    ##まず、人数分Playerクラスを作る。
    for i in range(players):
        PlayerMap['player_' + str(i)] = Player()
    for i in range(players):
        with open(file1, 'a') as f:
            print(str(i)  + "以外がランダム" , file=f)   
        with open(file2, 'r')as f:
            PlayerMap['player_' + str(i)].nodeMap = json.load(f)
        temp = list(range(players))
        temp.pop(i)
        ## 学習ずみプレイヤーを用意
        for j in temp:
            PlayerMap['player_' + str(j)].random_flg = True
        start = time.time()
        for t in range(play_iterations):
            history = {'open': [],   'point':[0 for _ in range(players)], 'private': [list(range(1,NA+1)) for _ in range(players)], 'next_reward' : 0}
            rewards = list(range(1,NA+1))
            random.shuffle(rewards)
            ## 持っているカードが２枚以上ある内はstrategyに応じて手を決める
            for i in range(players * (NA - 1)):
                player = len(history['open']) % players
                infoSet = make_infoset_3(history['open'], rewards)

                ## 行動を決定し、openに追加　card_listから消去
                a = PlayerMap['player_' + str(player)].make_action(history['private'][player], infoSet)
                history['open'].append(a)
                history['private'][player].remove(a)
                if len(history['open']) % players == 0:
                    point(history,players,NA,rewards)

            ## 上の繰り返しを終えて、持っているカードがみんな1枚になったら、自動的にopenに残りのカードを足していって最後のpointを計算
            for i in range(players):
                history['open'].append(history['private'][i][0])
                history['private'][i].pop(0)
            point(history,players,NA,rewards)

            ## それぞれ勝敗のutilを記録
            for i in range(players):
                PlayerMap['player_' + str(i)].util += judge(history, i, players, default_util)
                
        elapsed_time = time.time() - start
        ## 実行時間を記録
        with open(file1, 'a') as f:
            print('elapsed_time_for play: ' + str(round(elapsed_time,digit)),file=f)
        
        ##ゲームが終わったら、最終的な平均utilを出力
        for i in range(players):
            with open(file1, 'a') as f:
                print("Average game values for player " + str(i) + ' : ' + str(round(PlayerMap['player_' + str(i)].util / play_iterations , digit)) , file = f)
