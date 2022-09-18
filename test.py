import sys
import os
import random
import itertools
import copy

def trim(seqs ,direction=0):
    return ([0, 0, 0, 0] + [i for i in seqs if i])[-4:] if direction else ([i for i in seqs if i] + [0, 0, 0,0])[:4]

def sum_seqs(seqs ,direction=0):
    if seqs[0] and seqs[0] == seqs[1] == seqs[2] == seqs[3]:
        return trim([seqs[0] * 2, 0, seqs[2] * 2, 0], direction=direction)

    # fixme 处理一个序列中有除0外，三个相同的情况。
    # 前三个相同
    if seqs[0] and seqs[0] == seqs[1] == seqs[2] and direction == 0:
        return trim([seqs[0] * 2, seqs[1], 0, seqs[3]], direction=direction)
    if seqs[0] and seqs[0] == seqs[1] == seqs[2] and direction == 1:
        return trim([0, seqs[1], seqs[2] * 2, seqs[3]], direction=direction)
    # 后三个相同
    if seqs[1] and seqs[1] == seqs[2] == seqs[3] and direction == 0:
        return trim([seqs[0], seqs[1] * 2, seqs[2], 0], direction=direction)
    if seqs[1] and seqs[2] == seqs[3] == seqs[2] and direction == 1:
        return trim([seqs[0], 0, seqs[2], seqs[3] * 2], direction=direction)

    # 其它情况
    if seqs[1] and seqs[1] == seqs[2]:
        return trim([seqs[0], seqs[1] * 2, 0, seqs[3]], direction=direction)
    if seqs[0] and seqs[0] == seqs[1]:
        seqs[0], seqs[1] = seqs[0] * 2, 0
    if seqs[2] and seqs[2] == seqs[3]:
        seqs[2], seqs[3] = seqs[2] * 2, 0
    return trim(seqs, direction=direction)

def up(grad):
    for col in [0, 1, 2, 3]:
        for idx, n in enumerate(sum_seqs(trim([row[col] for row in grad]))):
            grad[idx][col] = n
    return grad

def down(grad):
    for col in [0, 1, 2, 3]:
        for idx, n in enumerate(sum_seqs(trim([row[col] for row in grad], direction=1), direction=1)):
            grad[idx][col] = n
    return grad

def left(grad):
    return [sum_seqs(trim(row)) for row in grad]

def right(grad):
    return [sum_seqs(trim(row,direction=1),direction=1) for row in grad]

#创建游戏类
class Game:
    grad= []
    contorls = ["w","a","s","d"]

    #游戏随机出现2/4
    def rnd_field(self):
        #伪随机概率问题
        number = random.choice([4,2,4,2,4,2,4,2,4,2,4,2,])
        x, y = random.choice([(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if self.grad[x][y] == 0])
        self.grad[x][y]=number

    #输出
    def print_screen(self):
        os.system('cls')
        print('-'*21)
        for row in self.grad:
            print('|{}|'.format("|".join([str(col or ' ').center(4) for col in row])))
            print('-' * 21)

    #判断输入
    def logic(self,contorl):
        # if contorl == 'w':
        #     up(self.grad)
        # if contorl == 'a':
        #     left(self.grad)
        # if contorl == 's':
        #     down(self.grad)
        # if contorl == 'd':
        #     right(self.grad)
        grid = { 'w': up ,'a': left ,'s':down ,'d':right }[contorl]([[c for c in r] for  r in self.grad])
        if grid !=self.grad:
            del self.grad[:]
            self.grad.extend(grid)
            if [n for n in itertools.chain(*grid) if n >= 2048]:
                return 1,"You win"
            self.rnd_field()
        else:
            if not [1 for g in [f(grid) for f in [up,down,left,right]] if g != self.grad]:
                return -1,"You Lost"

        return 0,''

    #游戏事件循环
    def mian_loop(self):
        #游戏的初始化动作
        #清空棋盘
        del self.grad[:]
        #初始化棋盘
        self.grad.extend([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.rnd_field()
        while True :
            self.print_screen()
            contorl = input('input w/a/s/d:')
            if contorl in self.contorls:
                status,info= self.logic(contorl)
                if status:
                    print(info)
                    if input('Start another game?[Y/N]').lower() == 'Y':
                        break
                    else:
                        sys.exit(0)

        self.mian_loop()

#方案二
class Game2(object):

    def __init__(self):
        self.grid = []
        self.controls = ['w', 'a', 's', 'd']

    def init_grid(self):
        """初始化棋盘内容:随机给棋盘空白处填一个数字"""
        # 正态分布容错
        number = random.choice([2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, ])
        x, y = random.choice([(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if self.grid[x][y] == 0])
        self.grid[x][y] = number

    def print_scr(self):
        """
        打印棋盘
        :return:
        """
        os.system('cls')
        print('-' * 21)
        for row in self.grid:
            print('|{}|'.format("|".join([str(col or " ").center(4) for col in row])))
            print('-' * 21)

    def logic(self, control):
        """
        执行操作
        :return:
        """

        def __trim(seqs, direction=0):
            """
            用于操作单个序列的移动
            具体操作：
            例：[0,2,2,0]
            1、去零：[2,2]
            2、按方向补四零（左 = 上，右 = 下）
            3、切片，只留下长度为4的序列

            :param seqs: 序列
            :param direction: 哪个方向（0代表：左或上）
            :return:操作完毕的序列
            """
            return ([0, 0, 0, 0] + [i for i in seqs if i])[-4:] if direction else ([i for i in seqs if i] + [0, 0, 0,
                                                                                                             0])[:4]

        def __sum(seqs, direction=0):
            """
            定义相同数字相加的函数。
            主要思想是判断坐标对应的数值是否相等。
            :return:待移动的seqs
            """
            # 四个都相同
            if seqs[0] and seqs[0] == seqs[1] == seqs[2] == seqs[3]:
                return __trim([seqs[0] * 2, 0, seqs[2] * 2, 0], direction=direction)

            # fixme 处理一个序列中有除0外，三个相同的情况。
            # 前三个相同
            if seqs[0] and seqs[0] == seqs[1] == seqs[2] and direction == 0:
                return __trim([seqs[0] * 2, seqs[1], 0, seqs[3]], direction=direction)
            if seqs[0] and seqs[0] == seqs[1] == seqs[2] and direction == 1:
                return __trim([0, seqs[1], seqs[2] * 2, seqs[3]], direction=direction)
            # 后三个相同
            if seqs[1] and seqs[1] == seqs[2] == seqs[3] and direction == 0:
                return __trim([seqs[0], seqs[1] * 2, seqs[2], 0], direction=direction)
            if seqs[1] and seqs[2] == seqs[3] == seqs[2] and direction == 1:
                return __trim([seqs[0], 0, seqs[2], seqs[3] * 2], direction=direction)

            # 其它情况
            if seqs[1] and seqs[1] == seqs[2]:
                return __trim([seqs[0], seqs[1] * 2, 0, seqs[3]], direction=direction)
            if seqs[0] and seqs[0] == seqs[1]:
                seqs[0], seqs[1] = seqs[0] * 2, 0
            if seqs[2] and seqs[2] == seqs[3]:
                seqs[2], seqs[3] = seqs[2] * 2, 0
            return __trim(seqs, direction=direction)

        def __up(old_grid):
            for col in [0, 1, 2, 3]:
                for idx, n in enumerate(__sum(__trim([row[col] for row in old_grid]))):
                    old_grid[idx][col] = n
            return old_grid

        def __left(old_grid):
            return [__sum(__trim(row)) for row in old_grid]

        def __down(old_grid):
            for col in [0, 1, 2, 3]:
                for idx, n in enumerate(__sum(__trim([row[col] for row in old_grid], direction=1), direction=1)):
                    old_grid[idx][col] = n
            return old_grid

        def __right(old_grid):
            return [__sum(__trim(row, direction=1), direction=1) for row in old_grid]

        _grid = {'w': __up, 'a': __left, 's': __down, 'd': __right}[control](copy.deepcopy(self.grid))
        if _grid != self.grid:  # 看看玩家是不是赢了
            del self.grid[:]
            self.grid.extend(_grid)
            if [n for n in itertools.chain(*_grid) if n >= 2048]:
                return 1, "you win!"
            self.init_grid()
        else:  # 上下左右各移动移步没有变化
            if not [1 for g in [func(_grid) for func in [__up, __left, __down, __right]] if g != self.grid]:
                return -1, "you lost!"
        return 0, ''  # 继续战斗吧

    def main(self):
        """
        游戏引擎
        :return:
        """
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.init_grid()
        self.init_grid()
        while True:
            self.print_scr()
            control = input("w(上) a（左） s（下） d（右）q（退出）r（重开）:")
            if control == "q":
                sys.exit(0)
            if control == "r":
                break
            if control in self.controls:
                status, info = self.logic(control)
                if status:
                    print(info)
                    if input("需要再来一次吗？y/n]").lower() == 'y':
                        break
                    else:
                        sys.exit(0)
        self.main()

if __name__ =="__main__":
    Game().mian_loop()
    #Game2().main()