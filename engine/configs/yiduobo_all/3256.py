def _pts(S):
    out = {}
    for name, c in (('1', 'blue'), ('2', 'pink'), ('3', 'green')):
        x, y = S.get('x' + name), S.get('y' + name)
        if x is not None and y is not None:
            out[(x, y)] = c
    return out


def _cell(S, i, j, v):
    c = _pts(S).get((i, j))
    if c:
        return c
    if '_inner' in S and 'vis_x' in S['_inner'] and i in S['_inner']['vis_x'] and False:
        return None
    return None


def _dim(S, i, j, v):
    I = S.get('_inner', {})
    vx, vy = I.get('vis_x'), I.get('vis_y')
    if vx is not None and vy is not None:
        return i in vx or j in vy
    return False


def _txt(S):
    I = S.get('_inner', {})
    if 'x' in I and 'y' in I and I['x'] is not None and 'i' in I and 'j' in I:
        return f"扫描 `({I['i']},{I['j']})`：当前最大 `({I['x']},{I['y']})` = =={S['board'][I['x']][I['y']]}=="
    if 'x1' in S:
        return '已放置的车：蓝 = 最大格，粉 = 其次，绿 = 第三'
    return ''


def _cmp(S):
    I = S
    i, j, x, y = S['i'], S['j'], S['x'], S['y']
    if i in S['vis_x'] or j in S['vis_y']:
        return f'`({i},{j})` 的行或列已被占 → 跳过'
    if x is None:
        return f'还没有候选，`({i},{j})` = {S["board"][i][j]} 成为第一个候选'
    return f'`({i},{j})` = {S["board"][i][j]} 对比当前最大 `({x},{y})` = {S["board"][x][y]}：' + ('更大 → ==更新==' if S['board'][x][y] < S['board'][i][j] else '不更大 → 保留')


CONFIG = dict(
    num=3256, title='放三个车的价值之和最大 I', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='贪心 + 分类讨论 · 最大格的行列',
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
    call='Solution().maximumValueSum([[1,2,3],[4,5,6],[7,8,9]])',
    expect=15,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='grid', var='board', h=420, cell=130, color=_cell, dim=_dim),
    ],
    watch=[('x1,y1', "(S.get('x1'), S.get('y1'))", 'blue'), ('x2,y2', "(S.get('x2'), S.get('y2'))", 'pink'),
           ('x3,y3', "(S.get('x3'), S.get('y3'))", 'green'), ('res', 'res', 'yellow')],
    captions={
        'if i not in vis_x and j not in vis_y': lambda S, B, r: _cmp(S),
        'x, y = i, j': '扫到 `({i},{j})` = {board[i][j]}，行列未被占且更大 → 成为新的最大格 `({x},{y})`',
        'x = i': '扫到第 `{i}` 行，未被占且更大 → 候选行 `x = {x}`',
        'y = j': '扫到第 `{j}` 列，未被占且更大 → 候选列 `y = {y}`',
        'return x, y': '剩余棋盘最大格 `({x},{y})` = {board[x][y]}',
        'return x': '这一列上可选的最大行：`x = {x}`',
        'return y': '这一行上可选的最大列：`y = {y}`',
        'x2, y2 = max_in_board': '屏蔽 x1 行、y1 列后，再找剩余最大格 `(x2,y2)`',
        'x3, y3 = max_in_board': '再屏蔽 x2 行、y2 列，找第三个 `(x3,y3)`',
        'x2_2 = max_in_col': '备选：y2 列上除去 x1、x2 行的最大格，给“最大格行列各一车”的方案用',
        'y2_2 = max_in_row': '备选：x2 行上除去 y1、y2 列的最大格',
        'res = board[x1][y1] + board[x2][y2] + board[x3][y3]': '方案一：直接取三个依次最大格 = =={res}==',
        'res = max(res, board[x1][y1] + board[x2][y2_2]': '方案二：车放 (x1,y1)，另外两个车互换行列取次优，`res` = =={res}==',
        'x1_2 = max_in_col': 'x1 行、y1 列各占一个车时，列方向要看 y1 列的前 3 大：次大行 `x1_2`',
        'y1_2 = max_in_row': 'x1 行上的前 3 大列：次大列 `y1_2`',
        'x1_3 = max_in_col': '列 y1 的第三大行 `x1_3`',
        'y1_3 = max_in_row': '行 x1 的第三大列 `y1_3`',
        'y_x12_ma =': 'x1_2 行上除去 y1、y1_2 列后的最大列，给组合 2 的第三个车',
        'x_y12_ma =': 'y1_2 列上除去 x1、x1_2 行后的最大行，给组合 3 的第三个车',
        'xx, yy = max_in_board': '组合 1：占 (x1,y1_2)、(x1_2,y1) 后，第三个车是剩余棋盘最大格 `({xx},{yy})`',
        'board[x1][y1_2] + board[x1_2][y1] + board[xx][yy]': '组合 1 的和与 res 取最大：`res` = =={res}==',
        'board[x1][y1_2] + board[x1_3][y1]': '组合 2：第三个车必在 x1_2 行，`res` = =={res}==',
        'board[x1][y1_3] + board[x1_2][y1]': '组合 3（与 2 对称）：第三个车在 y1_2 列，`res` = =={res}==',
        'board[x1][y1_3] + board[x1_3][y1]': '组合 4：第三个车只能是 (x1_2,y1_2)，`res` = =={res}==',
        'return res': '四种组合里最大的是 `{res}`',
        'x1, y1 = max_in_board': '先找整盘最大格 `(x1,y1)`：它要么被选，要么它的行和列各占一个车',
    },
    max_steps=150,
    skip=['vis_x = set', 'vis_y = set', 'm = len', 'n = len', 'for i in range', 'for j in range', 'if i not in vis_x and j not in vis_y', 'if j not in vis_y and', 'if i not in vis_x and (x', 'x, y = None, None', 'x = None', 'y = None'],
    cards=dict(
        one_liner='最大格要么被选，要么它的行、列各放一个车',
        complexity='时间 `O(mn)`，空间 `O(m+n)`（几次整盘遍历）',
        problem=['在棋盘上放三个互不攻击的车（不同行不同列），格子值之和最大',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `15`（对角线 1+5+9）'],
        quote='要么会将一个车放置在最优的单元格(x1, y1)上，要么会有两个车分别占据x1这一行以及y1这一列，否则的话必然可以将某个车移动到(x1, y1)上得到更优的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想一个车、两个车：两个车的最优是“最大格 + 剩余最大”或“最大格所在行、列的次大”',
              '三个车同理：要么选 `(x1,y1)`，要么行和列各占一个',
              '行上只需看前 3 大列，列上同理；再枚举 4 种组合并补第三个车'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`，II 题的 500 规模也够',
                 '易错：被屏蔽的行列要重新找剩余棋盘最大值（`max_in_board`）',
                 '易错：`None` 初值要先判，才能和 `board[x][y]` 比较',
                 '本视频只演示 3×3 小棋盘，分支讨论在最后几行取 max'],
    ),
)
