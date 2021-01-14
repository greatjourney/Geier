# -*- coding: utf-8 -*-
import random
import copy
import datetime
import math
import time
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

## 12/1 モジュール化
digit = 5
players = 3
iterations = 100000
NA = 2
strategy_interval = 10000
c = -0.5 * iterations
prune_threshold = iterations * 0.2
LCFR_threshold = 100
Discount_Interval = 10
dt_now = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second) 

# logのアウトプット用ファイル作成
file1 = "./学習記録/NA_" + str(NA) + "/output" +  str(dt_now) +  " iterations: " + str(iterations) + " players: " + str(players)  + ".txt"
# file1 = "./学習記録/NA_" + str(NA) + "/count_CFR.txt"
file2 = "./log_Player_3/NA_" + str(NA) + "/debug"  + str(dt_now) +" iterations: " + str(iterations) + " players: " + str(players) + ".txt"
file3 = "./hash記録/NA_" + str(NA) + "/iterations: " + str(iterations) + str(dt_now) +  ".json"
f = open(file1, 'w')
f.close()
f = open(file3, 'w')
f.close()
## ファイルの先頭に何かコメントをつけるなら。
with open(file1, 'a') as f:
    print("実験　MCCFR　ハゲタカはrandomにする strategy_intervalとLCFR_threshold, Discount_Intervalを使わない", file=f)
    print("iterations: " + str(iterations) + " NA: " + str(NA) + " players: " + str(players) + " : " + str(dt_now)  ,file=f)
    print("strategy_interval: " + str(strategy_interval) + " c: " + str(c) + " prune_threshold: " + str(prune_threshold) + " LCFR_threshold: " + str(LCFR_threshold) + " Discount_Interval: " + str(Discount_Interval), file = f)

if __name__ == '__main__':
    ## logのアウトプット用ファイル作成
    nodeMap = {}
    util = train_mccfr(iterations, players, file1, file2, NA, digit, nodeMap, strategy_interval, c, prune_threshold, LCFR_threshold, Discount_Interval)
    display_order_random(iterations, players,util, digit, file1, file2, NA, nodeMap)
    dump_hash(file3, nodeMap)