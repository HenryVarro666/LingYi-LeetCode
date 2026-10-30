BOARD = [[5, 1, 2], [9, 8, 1], [4, 7, 3]]
_PTS = [
    (('x1', 'y1'), 'yellow'),
    (('x2', 'y2'), 'blue'),
    (('x3', 'y3'), 'green'),
    (('x2_2', 'y2'), 'cyan'),
    (('x2', 'y2_2'), 'cyan'),
    (('x1_2', 'y1'), 'pink'),
    (('x1', 'y1_2'), 'pink'),
    (('x1_3', 'y1'), 'purple'),
    (('x1', 'y1_3'), 'purple'),
    (('x1_2', 'y1_2'), 'orange'),
]


def _cell(S, r, c, v):
    out = None
    for (a, b), col in _PTS:
        if S.get(a) == r and S.get(b) == c and r is not None and c is not None:
            out = out or col
    for (xn, yn) in (('xx', 'yy'),):
        if S.get(xn) == r and S.get(yn) == c and r is not None:
            out = out or 'green'
    return out


def _txt(S):
    b = S['board']
    parts = []
    for name, (a, c) in (('最大格', ('x1', 'y1')), ('次优', ('x2', 'y2')), ('第三', ('x3', 'y3')),
                         ('剩余最大', ('xx', 'yy'))):
        if S.get(a) is not None and S.get(c) is not None:
            parts.append(f'{name} `({S[a]},{S[c]})`={b[S[a]][S[c]]}')
    if 'x1_2' in S and S['x1_2'] is not None:
        parts.append(f"列次大行 `{S['x1_2']}`")
    if 'y1_2' in S and S['y1_2'] is not None:
        parts.append(f"行次大列 `{S['y1_2']}`")
    if 'x1' not in S:
        return '先找最大格 `(x1, y1)`，再屏蔽行和列，找 `(x2, y2)`、`(x3, y3)`'
    return '；'.join(parts) + (f"；当前 `res` = {S['res']}" if 'res' in S else '')


CONFIG = dict(
    num=3257, title='放三个车的价值之和最大 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='最大格 + 屏蔽行列的分类讨论',
    tags=['枚举中间', '前后缀分解', '难度分 2553'],
    code='''
class Solution(object):
    def maximumValueSum(self, board):

        m = len(board)
        n = len(board[0])

        def max_in_board(vis_x_list, vis_y_list):
            vis_x = set(vis_x_list)
            vis_y = set(vis_y_list)
            x, y = None, None
            for i in range(m):
                for j in range(n):
                    if i not in vis_x and j not in vis_y and (x is None or board[x][y] < board[i][j]):
                        x, y = i, j
            return x, y
        
        def max_in_col(y, vis_x_list):
            vis_x = set(vis_x_list)
            x = None
            for i in range(m):
                if i not in vis_x and (x is None or board[x][y] < board[i][y]):
                    x = i
            return x

        def max_in_row(x, vis_y_list):
            vis_y = set(vis_y_list)
            y = None
            for j in range(n):
                if j not in vis_y and (y is None or board[x][y] < board[x][j]):
                    y = j
            return y

        x1, y1 = max_in_board([], [])
        x2, y2 = max_in_board([x1], [y1])
        x3, y3 = max_in_board([x1, x2], [y1, y2])
        x2_2 = max_in_col(y2, [x1, x2])
        y2_2 = max_in_row(x2, [y1, y2])
        res = board[x1][y1] + board[x2][y2] + board[x3][y3]
        res = max(res, board[x1][y1] + board[x2][y2_2] + board[x2_2][y2])
        
        x1_2 = max_in_col(y1, [x1])
        y1_2 = max_in_row(x1, [y1])
        x1_3 = max_in_col(y1, [x1, x1_2])
        y1_3 = max_in_row(x1, [y1, y1_2])
        y_x12_ma = max_in_row(x1_2, [y1, y1_2])
        x_y12_ma = max_in_col(y1_2, [x1, x1_2])

        xx, yy = max_in_board([x1, x1_2], [y1, y1_2])
        res = max(res, board[x1][y1_2] + board[x1_2][y1] + board[xx][yy])
        res = max(res, board[x1][y1_2] + board[x1_3][y1] + board[x1_2][y_x12_ma])
        res = max(res, board[x1][y1_3] + board[x1_2][y1] + board[x_y12_ma][y1_2])
        res = max(res, board[x1][y1_3] + board[x1_3][y1] + board[x1_2][y1_2])

        return res
''',
    call=f'Solution().maximumValueSum({BOARD})',
    expect=18,
    views=[
        dict(type='grid', var='board', label='board（黄 最大格 / 蓝 次优 / 绿 第三 / 其他色 候选）', h=300, cell=76, color=_cell),
        dict(type='text', fn=_txt, size=22, h=80),
    ],
    watch=[('res', 'res', 'green')],
    skip=['vis_x = set', 'vis_y = set', 'x, y = None, None', 'for i in range(m)', 'for j in range(n)',
          'if i not in vis_x', 'x, y = i, j', 'return x, y', 'x = None', 'y = None', 'x = i', 'y = j', 'return x',
          'return y', 'm = len', 'n = len', 'def max_in', 'if j not in vis_y'],
    captions={
        'x1, y1 = max_in_board([], [])': '整盘扫一遍，找最大格 `(x1, y1)`（不屏蔽任何行列）',
        'x2, y2 = max_in_board([x1], [y1])': '屏蔽最大格所在的第 `{x1}` 行、第 `{y1}` 列，再扫一遍找 `(x2, y2)`',
        'x3, y3 = max_in_board([x1, x2], [y1, y2])': '再屏蔽 `x2` 行、`y2` 列，扫出第三个格 `(x3, y3)`；最大 `{board[x1][y1]}`、次优 `{board[x2][y2]}` 已定',
        'x2_2 = max_in_col': '`x2_2`：第 `{y2}` 列上，除去 `x1`、`x2` 两行后的最大格所在行',
        'y2_2 = max_in_row': '`y2_2`：第 `{x2}` 行上，除去 `y1`、`y2` 两列后的最大格所在列',
        'res = board[x1][y1] + board[x2][y2] + board[x3][y3]': '方案 A：==贪心三连==选 `{board[x1][y1]}` + `{board[x2][y2]}` + `{board[x3][y3]}` = =={res}==',
        'res = max(res, board[x1][y1] + board[x2][y2_2]': '方案 B：最大格保留，另两个车占 `x2` 行和 `y2` 列：`{board[x1][y1]} + {board[x2][y2_2]} + {board[x2_2][y2]}` → `res` = =={res}==',
        'x1_2 = max_in_col': '`x1_2`：最大格所在第 `{y1}` 列上，去掉第 `{x1}` 行后的最大 → 列上的次大',
        'y1_2 = max_in_row': '`y1_2`：最大格所在第 `{x1}` 行上，去掉第 `{y1}` 列后的最大 → 行上的次大',
        'x1_3 = max_in_col': '`x1_3`：这一列的第三大；==第 4 大以后不用看==（总能挪到没被占的列）',
        'y1_3 = max_in_row': '`y1_3`：这一行的第三大',
        'y_x12_ma = max_in_row': '`y_x12_ma`：`x1_2` 行上去掉 `y1`、`y1_2` 后的最大列',
        'x_y12_ma = max_in_col': '`x_y12_ma`：`y1_2` 列上去掉 `x1`、`x1_2` 后的最大行',
        'xx, yy = max_in_board([x1, x1_2]': '屏蔽 `x1`、`x1_2` 两行和 `y1`、`y1_2` 两列后重新扫，找剩下的最大格 `(xx, yy)`',
        'board[x1][y1_2] + board[x1_2][y1] + board[xx][yy]': '方案 C：两个车占最大格的行和列（次大 + 次大），第三个放剩余最大 → `res` = =={res}==',
        'board[x1][y1_2] + board[x1_3][y1]': '方案 D：行上次大、列上第三大，第三个车必在 `x1_2` 行 → `res` = =={res}==',
        'board[x1][y1_3] + board[x1_2][y1]': '方案 E：与 D 对称，第三个车必在 `y1_2` 列 → `res` = =={res}==',
        'board[x1][y1_3] + board[x1_3][y1]': '方案 F：行、列都取第三大，第三个车只能是 `(x1_2, y1_2)` → `res` = =={res}==',
        'return res': '所有情形取最大 → =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='最优解要么放在最大格上，要么有两个车占住它的行和列',
        complexity='时间 `O(mn)`（常数次扫盘），空间 `O(m+n)`',
        problem=['`m × n` 棋盘，`board[i][j]` 是格子的价值',
                 '放三个车，==不同行、不同列==，求价值之和最大',
                 '示例：`[[5,1,2],[9,8,1],[4,7,3]]` → `18`'],
        quote='可以明确的是要么会将一个车放置在最优的单元格(x1, y1)上，要么会有两个车分别占据x1这一行以及y1这一列，否则的话必然可以将某个车移动到(x1, y1)上得到更优的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想放 1 个、2 个车的情形，归纳出「最大格要么选，要么被行列次大夹住」',
              '最大格选中：屏蔽它的行列，等价于放 2 个车，贪心加一次「再扫一遍」',
              '行、列上各只留前 3 大（第 4 大总能挪到空列），再分四种组合算第三个车'],
        result='比较 6 种方案，最大是 18',
        summary=['时间 `O(mn)`：每次 `max_in_*` 扫一遍，总共常数次',
                 '原文已是 Python 3 可运行写法，没有改动',
                 '易错：屏蔽行列后，`(x2, y2)` 可能被屏蔽，必须重新扫 `max_in_board`',
                 '灵神用「枚举中间 + 前后缀」；这里靠分类讨论，代码更长但思路直观',
                 '本视频跳过了 `max_in_*` 内部的扫描循环，只看每次调用的结果'],
    ),
)
