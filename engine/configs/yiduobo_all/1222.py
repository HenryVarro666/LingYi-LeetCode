QUEENS = [[0, 2], [2, 0], [1, 1], [4, 4], [2, 3], [3, 3]]
KING = [2, 2]


EXP = [[2, 3], [3, 3], [2, 0], [1, 1], [0, 2]]


def _board(S):
    b = [['' for _ in range(8)] for _ in range(8)]
    for qx, qy in QUEENS:
        b[qx][qy] = '后'
    b[KING[0]][KING[1]] = '王'
    return b


def _color(S, i, j, v):
    if v == '王':
        return 'yellow'
    if 'res' in S and [i, j] in S['res']:
        return 'green'
    if v == '后':
        return 'pink'
    return None


def _step(S, B, r):
    x, y = S.nowx, S.nowy
    if x < 0 or x == 8 or y < 0 or y == 8:
        return f'`({x},{y})` 越界 → 这个方向走到头了，没有皇后能攻击国王'
    return f'`({x},{y})` 在棋盘内，继续判断'


CONFIG = dict(
    num=1222, title='可以攻击国王的皇后', difficulty='Medium', category='模拟',
    author='yiduobo', technique='从国王出发走八个方向',
    tags=[],
    code='''
class Solution(object):
    def queensAttacktheKing(self, queens, king):

        queen_set = set()
        for x, y in queens:
            queen_set.add((x, y))
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        res = []
        for index in range(8):
            nowx, nowy = king
            while True:
                nowx += dx[index]
                nowy += dy[index]
                if nowx < 0 or nowx == 8 or nowy < 0 or nowy == 8:
                    break
                if (nowx, nowy) in queen_set:
                    res.append([nowx, nowy])
                    break
        
        return res
''',
    call=f'Solution().queensAttacktheKing({QUEENS}, {KING})',
    expect=EXP,
    views=[
        dict(type='grid', var=_board, label='棋盘（黄 = 国王，粉 = 皇后，绿 = 能攻击国王，蓝框 = 当前走到的格子）',
             cell=58, h=500, color=_color, cursors=[('nowx', 'nowy', 'blue')]),
        dict(type='text', fn=lambda S: (f"方向 index = =={S['index']}==：`({S['dx'][S['index']]}, {S['dy'][S['index']]})`" if 'index' in S and 'dx' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('nowx', 'nowx'), ('nowy', 'nowy'), ('res', 'res', 'green')],
    skip=['queen_set = set()', 'for x, y in queens', 'queen_set.add', 'res = []', 'while True', 'nowx += dx'],
    max_steps=90,
    captions={
        'dx = [': '`dx`、`dy` 按位置配对，组成八个方向',
        'dy = [': '`dx`、`dy` 按位置配对，组成八个方向',
        'for index in range(8)': '第 `{index}` 个方向：`({dx[index]}, {dy[index]})`',
        'nowy += dy': '朝当前方向走一步：`({nowx}, {nowy})`',
        'nowx, nowy = king': '每个方向都从国王的位置重新出发：`({nowx}, {nowy})`',
        'if nowx < 0': _step,
        'if (nowx, nowy) in queen_set': lambda S, B, r: (f'`({S.nowx},{S.nowy})` 有皇后 → ==这个方向最近的皇后==，它能攻击国王'
                                                         if (S.nowx, S.nowy) in S.queen_set else f'`({S.nowx},{S.nowy})` 是空格，继续走'),
        'res.append': '最近的皇后加入答案：`res = {res}`',
        'return res': '八个方向都走完，答案 `{res}`',
    },
    cards=dict(
        one_liner='别从皇后出发，从国王出发：每个方向只看最近的那个皇后',
        complexity='时间 `O(m)`，空间 `O(m)`',
        problem=['`8×8` 棋盘，若干黑皇后，一个白国王',
                 '返回能==直接攻击==国王的黑皇后（被挡住的不算）',
                 '示例：皇后 `[[0,1],[1,0],[4,0],[0,4],[3,3],[2,4]]`，国王 `[0,0]`',
                 '→ `[[0,1],[1,0],[3,3]]`',
                 '本视频：国王 `[2,2]`，皇后 `[[0,2],[2,0],[1,1],[4,4],[2,3],[3,3]]`'],
        quote='同一方向上只有最近的皇后能攻击到国王，因此我们不应该从皇后出发，而应该从国王出发，分别向八个方向前进。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把皇后坐标放进集合，方便判断某格有没有皇后',
              '遍历八个方向，一步步走：遇到皇后就记入答案并停止',
              '走到棋盘边界还没遇到，说明这个方向安全'],
        summary=['时间 `O(m)`：建集合 + 八个方向各至多 8 步；空间 `O(m)`',
                 '遇到皇后后必须 `break`，后面的皇后被挡住了',
                 '边界判断：`nowx == 8` 与 `< 0` 一样要处理',
                 '原文为 Python 2 写法，代码在 Python 3 中可直接运行，未做修改'],
    ),
)
