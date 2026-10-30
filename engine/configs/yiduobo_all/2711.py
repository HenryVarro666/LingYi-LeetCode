G = [[1, 2, 3], [3, 1, 5], [3, 2, 1]]


def _ok(S):
    return 'i' in S and 'j' in S and S.get('_line', 0) >= 10


def _cell(S, i, j, v):
    if not _ok(S):
        return None
    ci, cj, ln = S['i'], S['j'], S['_line']
    if (i, j) == (ci, cj):
        return 'blue'
    t = i - ci
    if t == j - cj and t != 0:
        if t < 0:      # 左上方向
            if ln in (14, 21, 25):
                done = ln != 14 or -t <= ci - S.get('x', ci)
                return 'cyan' if done else None
        else:          # 右下方向
            if ln in (21, 25):
                done = ln == 25 or t <= S.get('x', ci) - ci
                return 'orange' if done else None
    return None


def _cur(S, k):
    if S.get('_line') in (14, 21) and 'x' in S:
        return (S['x'], S['y'])[k]
    return None


def _up(S):
    return set() if S.get('_line', 0) <= 10 else S.get('up_set')


def _down(S):
    return set() if S.get('_line', 0) <= 14 else S.get('down_set')


def _cap(S, B, side):
    x, y = S.x, S.y
    v = S.grid[x][y]
    nm = 'up_set' if side == 'up' else 'down_set'
    cur = S[nm]
    old = B.get(nm) or set()
    where = '左上' if side == 'up' else '右下'
    tail = '：已经有了，==集合不变==' if v in old else ''
    return f'{where}走到 `({x},{y})`，值 `{v}` 加入 `{nm}` → {sorted(cur)}{tail}'


CONFIG = dict(
    num=2711, title='对角线上不同值的数量差', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举每个格子 · 两个集合去重',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1429'],
    code='''
class Solution(object):
    def differenceOfDistinctValues(self, grid):

        m = len(grid)
        n = len(grid[0])

        res = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                x, y = i - 1, j - 1
                up_set = set()
                while x >= 0 and y >= 0:
                    up_set.add(grid[x][y])
                    x -= 1
                    y -= 1

                x, y = i + 1, j + 1
                down_set = set()
                while x < m and y < n:
                    down_set.add(grid[x][y])
                    x += 1
                    y += 1

                res[i][j] = abs(len(up_set) - len(down_set))

        return res
''',
    call=f'Solution().differenceOfDistinctValues({G})',
    expect=[[1, 1, 0], [1, 0, 1], [0, 1, 1]],
    skip=[4, 5, 11, 12, 13, 15, 16, 18, 19, 20, 22, 23],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前格子，青 = 左上已走过，橙 = 右下已走过）', cell=80, h=260,
             color=_cell, cursors=[(lambda S: _cur(S, 0), lambda S: _cur(S, 1), 'pink')]),
        dict(type='grid', var='res', label='res（答案）', cell=80, h=260),
        dict(type='set', var=_up, label='up_set（左上对角线上出现过的值）', fmt=lambda x: str(x), h=100),
        dict(type='set', var=_down, label='down_set（右下对角线上出现过的值）', fmt=lambda x: str(x), h=100),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'pink'),
           ('|up|', 'len(up_set)', 'cyan'), ('|down|', 'len(down_set)', 'orange')],
    captions={
        7: '`m = {m}`，`n = {n}`；`res` 先全 0，每个格子单独算一遍',
        9: lambda S, B, r: ('全部格子算完' if 'i' in B and S.i == B.i else f'处理第 `{S.i}` 行'),
        10: lambda S, B, r: ('这一行算完了' if 'j' in B and S.j == B.j
                             else f'格子 `({S.i},{S.j})`：左上 {min(S.i, S.j)} 个数，右下 {min(S.m - 1 - S.i, S.n - 1 - S.j)} 个数'),
        14: lambda S, B, r: _cap(S, B, 'up'),
        21: lambda S, B, r: _cap(S, B, 'down'),
        25: lambda S, B, r: (f'`up_set` 有 {len(S.up_set)} 种，`down_set` 有 {len(S.down_set)} 种 → '
                             f'`|{len(S.up_set)} − {len(S.down_set)}|` = =={S.res[S.i][S.j]}=='),
        27: '每个格子都算好了 → 返回 `res`',
    },
    cards=dict(
        one_liner='数据规模小：枚举每个格子，向两个方向走一遍，用集合数不同值',
        complexity='时间 `O(mn·min(m,n))`，空间 `O(min(m,n))`',
        problem=['格子 `(r, c)` 的左上对角线、右下对角线上各有若干数',
                 '`answer[r][c] = |左上不同值个数 − 右下不同值个数|`',
                 '示例：`[[1,2,3],[3,1,5],[3,2,1]]` → `[[1,1,0],[1,0,1],[0,1,1]]`'],
        quote='题目的数据规模很小，因此可以直接枚举矩阵中的每个位置，然后从这个位置出发分别向左上和右下不断行走直到来到矩阵边界上。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个格子：从 `(i-1, j-1)` 往左上走，从 `(i+1, j+1)` 往右下走，直到出界',
              '走的时候把值放进 `up_set` / `down_set`，集合自动去重',
              '最后用两个集合大小之差的绝对值更新 `res[i][j]`'],
        summary=['时间 `O(mn·min(m,n))`：每个格子走一条对角线，本题 `m, n ≤ 50` 足够',
                 '易错：两个集合要==每个格子重新创建==，起点是 `(i±1, j±1)`，不含格子自己',
                 '原文是 Python 2 风格，但可直接在 Python 3 运行，代码未改',
                 '灵神把每条对角线当数组做前后缀分解，复杂度降到 `O(mn)`；yiduobo 是暴力枚举'],
    ),
)
