CONFIG = dict(
    num=348, title='设计井字棋', difficulty='Medium', category='设计',
    author='yiduobo', technique='行列对角计数',
    code='''
class TicTacToe(object):

    def __init__(self, n):
        self.n = n
        self.row = [0] * n
        self.col = [0] * n
        self.left = self.right = 0

    def move(self, row, col, player):
        if player == 1:
            delta = 1
        else:
            delta = -1
        
        self.row[row] += delta
        self.col[col] += delta
        if row == col:
            self.left += delta
        if row == self.n - 1 - col:
            self.right += delta

        if abs(self.row[row]) == self.n or abs(self.col[col]) == self.n or abs(self.left) == self.n or abs(self.right) == self.n:
            return player
        
        return 0
''',
    call='''t = TicTacToe(3)
out = []
out.append(t.move(0, 0, 1))
out.append(t.move(1, 1, 2))
out.append(t.move(0, 1, 1))
out.append(t.move(2, 2, 2))
out.append(t.move(0, 2, 1))
out''',
    expect=[0, 0, 0, 0, 1],
    views=[
        dict(type='array', var='self.row', label='self.row（每行：玩家 1 加 1，玩家 2 减 1）', h=210),
        dict(type='array', var='self.col', label='self.col（每列的计数）', h=210),
        dict(type='text', fn=lambda S: (f"主对角线 `left = {S['self.left']}`　副对角线 `right = {S['self.right']}`" if 'self.left' in S else ''), h=90),
    ],
    watch=['row', 'col', ('player', 'player', 'pink'), 'delta', ('self.left', 'self.left', 'cyan'), ('self.right', 'self.right', 'orange')],
    captions={
        'self.row = [0] * n': '`row[i]` 记录第 i 行的“净棋子数”，初始全 0',
        'self.col = [0] * n': '`col[j]` 记录第 j 列的净棋子数',
        'self.left = self.right': '两条对角线各用一个计数：`left` 主对角、`right` 副对角',
        'delta = 1': '玩家 1 放棋 → 计数 ==+1==',
        'delta = -1': '玩家 2 放棋 → 计数 ==-1==，两人的棋互相抵消，不会误判',
        'self.row[row] += delta': '第 `{row}` 行计数 += `{delta}` → =={self.row[row]}==',
        'self.col[col] += delta': '第 `{col}` 列计数 += `{delta}` → =={self.col[col]}==',
        'if row == col': lambda S, B, r: (f'`{S.row} == {S.col}`：在主对角线上，`left` 也要更新' if S.row == S.col else f'`{S.row} != {S.col}`：不在主对角线，跳过'),
        'self.left += delta': '`left` += `{delta}` → =={self.left}==',
        'if row == self.n - 1 - col': lambda S, B, r: (f'`{S.row} == {S.self.n - 1 - S.col}`：在副对角线上，`right` 也要更新' if S.row == S.self.n - 1 - S.col else f'`{S.row} != {S.self.n - 1 - S.col}`：不在副对角线，跳过'),
        'self.right += delta': '`right` += `{delta}` → =={self.right}==',
        'if abs(self.row[row])': lambda S, B, r: ('有一条线的计数绝对值达到 `n`：整行/列/对角线都是同一玩家的棋 → ==获胜==' if r is None and (abs(S.self.row[S.row]) == S.self.n or abs(S.self.col[S.col]) == S.self.n or abs(S.self.left) == S.self.n or abs(S.self.right) == S.self.n)
                                  else f'行 {abs(S.self.row[S.row])}、列 {abs(S.self.col[S.col])}、主对角 {abs(S.self.left)}、副对角 {abs(S.self.right)}：都没到 `{S.self.n}`，没人赢'),
        'return player': '返回获胜玩家 `{player}`',
        'return 0': '没人获胜，返回 `0`',
    },
    cards=dict(
        one_liner='不存棋盘，只记每行每列每对角线的净棋子数',
        complexity='每次 `move` 时间 `O(1)`，空间 `O(n)`',
        problem=['`n × n` 棋盘，两名玩家轮流落子，某一行、列或对角线被同一玩家占满即获胜',
                 '`move(row, col, player)` 返回获胜者，没人赢返回 `0`',
                 '示例：`n=3`，玩家 1 下满第 0 行的三格 → 第三次落子返回 `1`'],
        quote='利用哈希表储存所有行、列以及两条对角线上已经有多少枚相同的棋子。当相同的棋子到达n枚时，当前玩家就胜利了。',
        quote_src='—— yiduobo 题解原文',
        idea=['参考皇后问题：用计数代替整个棋盘',
              '玩家 1 加 1，玩家 2 减 1：某条线计数的绝对值 `== n` 就说明全是同一人',
              '落在 `row == col` 的格子属于主对角线，`row == n-1-col` 属于副对角线'],
        summary=['每次 `move` 只更新至多 4 个计数，`O(1)`',
                 '易错：副对角线的条件是 `row == n - 1 - col`',
                 '用 ±1 区分玩家，所以判断的是 `abs(...) == n`，不是 `== n`',
                 '同一格被重复下棋不在本题考虑范围内'],
    ),
)
