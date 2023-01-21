# 用于计算和重新绘制五子棋棋盘
# 1. 首先读取数据文件，获取棋盘数据
#   数据保存在game.json中
# 2. 计算新棋盘的变化：判断是否有五个棋子连在一起，如果有，则将这五个棋子的颜色改为win
# 3. 重新绘制棋盘，方法是：
#   1.首先读取README.md文件，寻找两个注释标记，然后将中间的内容删除
#   2.然后将新的棋盘数据插入到README.md文件中
#   开始的注释标记为：<!-- The-game-board-starts-here -->
#   结束的注释标记为：<!-- The-game-board-ends-here -->
#   两个标记中间的行即为棋盘
#   棋盘为一个Markdown表格，每一行为一个棋盘行
#   每一行中的每一个字符为一个棋盘格
#   棋盘格中的images/棋子颜色.svg，如果没有棋子，则为images/empty.svg
# game.json的示例：
# {
#    "start":"2021-01-20 20:00:00",
#    "history":[["YubaC",15,2], ["YubaD",3,13], ["YubaD",3,13], ["YubaD",3,13], ["YubaD",3,13], ["YubaD",3,13], ["YubaC",15,2]],
#     "step":"black",
#     "//board":"0:empty, 1:white, 2:black",
#     "board":[
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#     ]
# }
# Author: YubaC 2023-1-20

import json,sys
# import os
import time
URL = "https://github.com/YubaC/Gobang/issues/new?title=drop,{0},{1}&body=Just+push+%27Submit+new+issue%27+without+editing+the+title.+The+README+will+be+updated+after+approximately+30+seconds."
HISTORY_FRAME = """
Start: {0}
End: {1}
Win: {4}

Players & Moved Steps: 
{2}
History: 
{3}
"""
to = sys.argv[1].split(",")
new_piece = (int(to[1]), int(to[2]))
playerName = sys.argv[2]

# 1. 读取数据文件，获取棋盘数据
with open(r'data\game.json', 'r') as f:
    data = json.load(f)
    f.close()

data['history'].append([playerName, new_piece[0], new_piece[1]])

# 读取README.md文件
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read().splitlines()
    f.close()

# 读取棋盘数据
board = data['board']

# 插入新棋子
board[new_piece[0]][new_piece[1]] = 1 if data["step"] == "white" else 2

# 2. 计算新棋盘的变化：判断是否有五个棋子连在一起，如果有，则将这五个棋子的颜色改为win
# 遍历棋盘
win = -1
for i in range(15):
    for j in range(15):
        # 如果当前棋子为空，则跳过
        if board[i][j] == 0:
            continue
        # 如果当前棋子已经是win，则跳过
        if board[i][j] == 3:
            continue
        # 检查当前棋子的右边是否有四个棋子连在一起
        if j <= 10 and board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4]:
            win = board[i][j]
            board[i][j] = 3
            board[i][j+1] = 3
            board[i][j+2] = 3
            board[i][j+3] = 3
            board[i][j+4] = 3
            continue
        # 检查当前棋子的下边是否有四个棋子连在一起
        if i <= 10 and board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j]:
            win = board[i][j]
            board[i][j] = 3
            board[i+1][j] = 3
            board[i+2][j] = 3
            board[i+3][j] = 3
            board[i+4][j] = 3
            continue
        # 检查当前棋子的右下方是否有四个棋子连在一起
        if i <= 10 and j <= 10 and board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4]:
            win = board[i][j]
            board[i][j] = 3
            board[i+1][j+1] = 3
            board[i+2][j+2] = 3
            board[i+3][j+3] = 3
            board[i+4][j+4] = 3
            continue
        # 检查当前棋子的左下方是否有四个棋子连在一起
        if i <= 10 and j >= 4 and board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4]:
            win = board[i][j]
            board[i][j] = 3
            board[i+1][j-1] = 3
            board[i+2][j-2] = 3
            board[i+3][j-3] = 3
            board[i+4][j-4] = 3
            continue

# for i in board:
#     for j in i:
#         print(j, end='')
#     print('')

# 3. 重新绘制棋盘
# 3.1. 绘制棋盘的上边框

# 3.2. 绘制棋盘的左边框和棋子

def drawBoard(board, useLink=False):
    gameBoard = [
        "|   | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |",
        "| - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |"]
    for i in range(15):
        if i < 9:
            line = "| %s |" % ("0"+str(i+1))
        else:
            line = "| %s |" % (i+1)
        for j in range(15):
            if board[i][j] == 0:
                if useLink:
                    line += " [![](images/empty.svg)]("+URL.format(i,j)+") |"
                else:
                    line += " ![](images/empty.svg) |"
            elif board[i][j] == 1:
                line += " ![](images/white.svg) |"
                # line += " ○ |"
            elif board[i][j] == 2:
                line += " ![](images/black.svg) |"
            elif board[i][j] == 3:
                line += " ![](images/win.svg) |"
        gameBoard.append(line)
    return gameBoard

# 3.3. 更新README.md文件
#   开始的注释标记为：<!-- The-game-board-starts-here -->
#   结束的注释标记为：<!-- The-game-board-ends-here -->
#   从开始的注释标记到结束的注释标记之间的内容，就是棋盘的内容

# 3.3. 判断胜负，并用新的棋盘替换掉旧的棋盘

# 历史棋盘开始的注释标记为：<!-- The-history-board-starts-here -->
# 历史棋盘结束的注释标记为：<!-- The-history-board-ends-here -->
# 从开始的注释标记到结束的注释标记之间的内容，就是历史棋盘的内容
# 如果win != -1，说明有一方获胜了，需要更新历史棋盘
step_history = data['history']
if win != -1:
    # 给gameBoard添加开始时间、结束时间、玩家操作、获胜方
    # gameBoard.insert(0, HISTORY_FRAME.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), player, win))
    HistoryGameBoard=drawBoard(board)
    # 统计玩家的操作步数表，并对此排序
    # 方法是：遍历step_history这个列表
    # step_history的格式为[[PlayerName, x, y], [PlayerName, x, y], ...]
    # PlayerName是玩家的名字，x是横坐标，y是纵坐标
    # 例如：[["YubaC",15,2], ["YubaD",3,13]]
    # YubaC在(15,2)处落子，YubaD在(3,13)处落子
    # 最后统计出一个字典，格式为：{"YubaC": 1, "YubaD": 1}
    # 表示YubaC总共落了1步子，YubaD总共落了1步子
    # 用这个字典来排序，就可以知道谁落的棋子多，谁落的棋子少
    # 例如：{"YubaC": 1, "YubaD": 2}，YubaC落的棋子少，YubaD落的棋子多

    # 用来统计玩家的操作步数表
    step_count = {}
    for step in step_history:
        if step[0] in step_count:
            step_count[step[0]] += 1
        else:
            step_count[step[0]] = 1
    # 对step_count这个字典进行排序

    # 方法是：先把step_count这个字典转换成列表
    # 列表的格式为：[("YubaC", 1), ("YubaD", 2)]
    # 然后用sorted函数对列表进行排序
    # sorted函数的参数key指定了排序的依据
    # key指定的函数，会对列表中的每一个元素进行处理
    # 例如：key指定的函数是lambda x: x[1]
    # 则列表中的每一个元素都会被处理成x[1]
    # 例如：[("YubaC", 1), ("YubaD", 2)]
    # 则会被处理成[1, 2]
    # 然后再对[1, 2]进行排序
    # 最后得到的结果是[1, 2]
    # 然后再把[1, 2]转换成[("YubaC", 1), ("YubaD", 2)]
    # 这样就完成了对step_count这个字典的排序
    step_count = sorted(step_count.items(), key=lambda x: x[1], reverse=True)
    # 将这个列表翻转以实现由大到小的排序
    # step_count.reverse()

    # 将这个列表转化为Markdown格式的表格
    # 标题为Player Name和Step Count
    # 内容为step_count这个列表
    step_count_table = "| Player Name | Step Count |\n| - | - |\n"
    for i in range(len(step_count)):
        step_count_table += "| {} | {} |\n".format("[@"+step_count[i][0]+"](https://github.com/"+step_count[i][0]+")", step_count[i][1])
    # 将这个表格添加到gameBoard中
    # gameBoard.insert(1, step_count)

    HistoryGameBoard.insert(0, """
<details>
<summary><b>Gobang board</b></summary>
""")
    HistoryGameBoard.append("</details>")
    
    history_steps = """
<details>
<summary><b>Step History</b></summary>

| Player Name | Step |\n| - | - |\n"""
    for i in range(len(step_history)):
        # 将Y坐标转为字母
        y = chr(step_history[i][2] + 65)
        history_steps += "| {} | {} |\n".format(step_history[i][0], y+str(step_history[i][1]+1))
    history_steps += "</details>\n"
    
    if win == 1:
        win = "![White](images/white.svg) wins"
    elif win == 2:
        win = "![Black](images/black.svg) wins"

    HistoryGameBoard.insert(0, HISTORY_FRAME.format(data['start'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), step_count_table, history_steps, win))
    # HistoryGameBoard.insert(1, "| - | - | - | - |")
    HistoryGameBoard.insert(0, "\n### Game" + str(data["number"]))
    
    #找到开始的注释标记的行号
    for i in range(len(readme)):
        if readme[i] == '<!-- The-history-board-starts-here -->':
            start = i
            break
    # 找到结束的注释标记的位置
    for i in range(start+1, len(readme)):
        if readme[i] == '<!-- The-history-board-ends-here -->':
            end = i
            break
    # 用新的棋盘替换掉旧的棋盘
    # 删除旧棋盘所在行，在开始的注释标记后面插入新的棋盘
    readme = '\n'.join(readme[:start+1]) + '\n' + '\n'.join(HistoryGameBoard) + '\n\n' +'\n'.join(readme[start+1:])
    readme = readme.splitlines()

    # 读取frame.json
    with open(r'data\frame.json', 'r', encoding='utf-8') as f:
        frame = json.loads(f.read())
        f.close()

    # 获取当前时间
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    frame['start'] = now

    number = data['number'] + 1
    
    data = frame
    frame['number'] = number
    board = data['board']
    step_history=[]

    # number-of-games下面插入游戏次数
    for i in range(len(readme)):
        if readme[i] == '<!-- Number-of-games -->':
            readme[i+1] = "### Game" + str(number)
            break


if data['step'] == "black":
    data['step'] = "white"
else:
    data['step'] = "black"

# number-of-games下面插入游戏次数
for i in range(len(readme)):
    if readme[i] == '<!-- Next-piece -->':
        if data['step'] == "black":
            readme[i+1] = "![Black](images/black.svg)"
        else:
            readme[i+1] = "![White](images/white.svg)"
        break

# 3.3.1. 找到开始的注释标记的行号
for i in range(len(readme)):
    if readme[i] == '<!-- The-game-board-starts-here -->':
        start = i
        break
# 3.3.2. 找到结束的注释标记的位置
for i in range(start+1, len(readme)):
    if readme[i] == '<!-- The-game-board-ends-here -->':
        end = i
        break
# 删除旧棋盘所在行，在开始的注释标记后面插入新的棋盘
gameBoard = drawBoard(board, useLink=True)
readme = '\n'.join(readme[:start+1]) + '\n' + '\n'.join(gameBoard) + '\n' +'\n'.join(readme[end:])

# 更新Last-few-moves-starts-here
readme = readme.splitlines()
for i in range(len(readme)):
    if readme[i] == '<!-- Last-few-moves-starts-here -->':
        start = i
        break
for i in range(start+1, len(readme)):
    if readme[i] == '<!-- Last-few-moves-ends-here -->':
        end = i
        break
# 绘制最后几步棋
steps = []
# 获取step_history中最后几步棋
for i in range(len(step_history)):
    if i > 5:
        break
    steps.append(step_history[-i-1])
# 将最后几步棋转为表格
steps_table = "| Player Name | Step |\n| - | - |\n"
for i in range(len(steps)):
    # 将Y坐标转为字母
    y = chr(steps[i][2] + 65)
    steps_table += "| {} | {} |\n".format(steps[i][0], y+str(steps[i][1]+1))
steps = steps_table
readme = '\n'.join(readme[:start+1]) + '\n' + str(steps) + '\n' +'\n'.join(readme[end:])

# 4. 保存README.md文件
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)
    f.close()

# 保存games.json
with open(r'data\game.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data))
    f.close()

