# -*- coding: utf-8 -*-
## 12/16 新しく作った　3人プレイのハゲタカのえじきに必要な関数をまとめている

from scipy.stats import rankdata
import random
 
## 12/29 はげたかかーどをランダムにする時にinfosetも変えなければいけない 今までのrewardsと今まで出したカードだしておけばいい？ tエストケース合格
def make_infoset_3(card_list, rewards):
    n = len(card_list)
    a = ''
    if n % 3 == 0:
        a = str(card_list) 
    elif n == 1:
        a =  '[*]'
    elif n == 2:
        a =  '[*, *]'
    elif n % 3 == 1:
        a = str(card_list[0: n - 1])
        a = a[0: len(a) - 1]
        a += ', *]'
    else:
        a = str(card_list[0: n - 2])
        a = a[0: len(a) - 1]
        a += ', *, *]'
    
    b = str(rewards[0 : (n // 3) + 1])
    return a + ' ' + b
    
def make_action(strategy):
        r = random.random()
        sum = 0
        for i in range(len(strategy)):
            if sum < r < sum + strategy[i]:
                return i + 1
            sum += strategy[i]

def point(history, players, NA, rewards):
    n = len(history['open'])
    card = history['open'][n - players : n]
    sorted_card = sorted(card, reverse = True)
    max = sorted_card[0]
    i = 1
    non_max = False
    while True:
        if sorted_card[i] == max:
            i += 2
            if i >= players - 1:
                max = sorted_card[i -1]
                break
            max = sorted_card[i +1]
        else:
            break
    if max == sorted_card[players-2]:
        non_max = True
    if non_max:
        history['next_reward'] +=  rewards[int(n / players) -1]   
    else:
        get_index = card.index(max)
        history['point'][get_index] += rewards[int(n / players) -1]   +  history['next_reward']
        history['next_reward'] = 0
        
    return history
    
## 14:5 ~ 14:25  default_utilを求めるための関数 これも別にテスト
## 14:30 ~ 15:55 ご飯食べたり買い物したり　
## 15:55 ~ 16:02 着手 テストケースOK
def get_default_util(players):
    default_util = [0 for _ in range(players)]
    if players % 2 == 0:
        half = int(players / 2)
        for i in range(half):
            default_util[i] = (half) - i
        for i in range(half, players):
            default_util[i] = (half) - i - 1
    else:
        half = int((players - 1) / 2)
        for i in range(half):
            default_util[i] = (half) - i
        for i in range(half + 1, players):
            default_util[i] = (half) - i 
    return default_util

## 11/27 13:40 順位付けする関数を別に作る　これでテストケースを作る 13:45 OK
def rank(point_list):
    players = len(point_list)
            # 順位を返してくれる便利なメソッドだが、なぜか昇順しかできないので少し手を加える必要がある。
    rank_list = list(rankdata(point_list, method='max'))
    for i in range(players):
        rank_list[i] = players + 1 - rank_list[i]
    return rank_list


def judge(history, player,players,default_util):
    ## 各インデックスの順位を取得
        rank_list = rank(history['point'])
        players = len(rank_list)
        rank_util_list = [0 for _ in range(players)]
        ## 何位の物が何個あるかを数える
        for i in rank_list:
            rank_util_list[i-1] += 1
            
        ## 何位が何点かを計算する
        for i in range(len(rank_util_list)):
            # 複数あるなら、被ってる範囲の点数を被ってるやつで等分する
            if rank_util_list[i] > 1:
                util = 0
                for j in range(i, i + rank_util_list[i]):
                    util += default_util[j]
                rank_util_list[i] = (util / rank_util_list[i])
            ## 1個しかないrankのものは、そのままdefault_utilを返せば良い
            if rank_util_list[i] == 1:
                rank_util_list[i] = default_util[i]
        
        # playerは何位か
        player_rank = rank_list[player]
        return rank_util_list[player_rank - 1]

def make_infoset_3_old(card_list):
    n = len(card_list)
    if n % 3 == 0:
        return str(card_list)
    elif n % 3 == 1:
        a = card_list[0:n-1]
        i = 0
        while i < len(a):
            a[i] = card_list[i + 1]
            a[i + 1] = card_list[i]
            a[i + 2] = card_list[i + 2]
            i += 3
        return str(a)
    else:
        a = card_list[0:n-2]
        i = 0
        while i < len(a):
            a[i] = card_list[i + 2]
            a[i + 1] = card_list[i]
            a[i + 2] = card_list[i + 1]
            i += 3
        return str(a)

## 11/28 11:38 ~ 各プレイヤーでinfosetを変える　[1,2,3,4] → [1,2,3,*]みたいにする  11:45 テストケースとおった
def make_infoset_3_diff(card_list):
    n = len(card_list)
    if n % 3 == 0:
        return str(card_list) 
    elif n == 1:
        return '[*]'
    elif n == 2:
        return '[*, *]'
    elif n % 3 == 1:
        a = str(card_list[0: n - 1])
        a = a[0: len(a) - 1]
        a += ', *]'
        return str(a)
    else:
        a = str(card_list[0: n - 2])
        a = a[0: len(a) - 1]
        a += ', *, *]'
        return str(a)