# 五子棋AI，用于计算五子棋并下棋
# 功能尚未完全实现，这个为随机落子
# 作者：YubaC

import json
import random
import os

# 读取game.json的数据
with open(r'data\game.json', 'r') as f:
    game = json.load(f)
    f.close()

# 随机落子
def random_move(game):
    # 随机落子
    while True:
        i = random.randint(0, 14)
        j = random.randint(0, 14)
        if game['board'][i][j] == 0:
            return [i, j]

palce = random_move(game)
os.system("python gobangProcess.py drop," + str(palce[0]) + "," + str(palce[1]) + " Begonia")