_M, _N = 2, 3


def _mat(S):
    now = S['_inner'].get('now')
    if now is None:
        return S['grid']
    return [[now >> (i * _N + j) & 1 for j in range(_N)] for i in range(_M)]


def _color(S, i, j, v):
    rx, ry = S['_inner'].get('rx'), S['_inner'].get('ry')
    if rx is None or S.get('_line', 0) < 19:
        return None
    if i == rx and j == ry:
        return 'yellow'
    if v == 1 and (i == rx or j == ry):
        return 'red'
    return None


CONFIG = dict(
    num=2174, title='通过翻转行或列来去除所有的1 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='状态压缩 DP（记忆化搜索）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def removeOnes(self, grid):

        m = len(grid)
        n = len(grid[0])
        f = [None] * (1 << (m * n))
        f[0] = 0

        def calc(now):
            if f[now] is None:
                f[now] = m * n
                one_set = set()
                for i in range(m):
                    for j in range(n):
                        state = 1 << (i * n + j)
                        if now & state == state:
                            one_set.add((i, j))

                for rx, ry in one_set:
                    remove = 1 << (rx * n + ry)
                    for i in range(m):
                        if (i, ry) in one_set:
                            remove |= 1 << (i * n + ry)

                    for j in range(n):
                        if (rx, j) in one_set:
                            remove |= 1<< (rx * n + j)

                    f[now] = min(f[now], calc(now ^ remove) + 1)

            return f[now]

        now = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    now |= 1 << (i * n + j)

        return calc(now)
''',
    call='Solution().removeOnes([[1, 1, 0], [0, 1, 1]])',
    expect=2,
    views=[
        dict(type='grid', var=_mat, label='当前状态 now 还原成矩阵（黄 = 选中的 1，红 = 同行同列被一起清掉的 1）', h=180, cell=90, color=_color),
        dict(type='map', var=lambda S: {format(k, '06b'): v for k, v in enumerate(S['f']) if v is not None} if 'f' in S else None,
             label='f[state]（state 的二进制，低位 = (0,0)）= 清空最少操作数', h=150, font=24),
        dict(type='calls', h=190, hide=('grid', 'm', 'n', 'f')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('remove', lambda S: S['_inner'].get('remove'), 'red'),
           ('(rx,ry)', lambda S: (S['_inner'].get('rx'), S['_inner'].get('ry')) if 'rx' in S['_inner'] else None, 'yellow')],
    skip=['m = len(grid)', 'n = len(grid[0])', 'for i in range(m)', 'for j in range(n)', 'state = 1 <<', 'for rx, ry in one_set', 'one_set = set()',
          'if (i, ry) in one_set', 'if (rx, j) in one_set', 'if now & state', 'if grid[i][j] == 1', 'now = 0', 'def calc', 'one_set.add', 'remove |= 1 << (i', 'remove |= 1<<', 'f[now] = m * n', 'remove = 1 << (rx'],
    max_steps=100,
    captions={
        'f = [None]': '`f[state]`：把 `state`（每个格子一位，第 `i*n+j` 位）清空所需的最少操作数，先全设为未知',
        'f[0] = 0': '`f[0] = 0`：已经没有 1 了，不需要操作',
        'now |= 1 <<': '把矩阵压成整数 `now = {now}`（二进制 `{bin(now)[2:].zfill(6)}`）',
        'return calc(now)': lambda S, B, ret: ('开始：`calc(now)` 求清空整个矩阵的最少次数' if ret is None else '答案 `calc(now)` = =={}=='.format(ret)),
        'if f[now] is None': lambda S, B, ret: ('`f[{}]` 还没算过 → 要枚举每个 1 作为这一轮的操作'.format(S['_inner']['now']) if S['f'][S['_inner']['now']] is None
                                               else '`f[{}]` 已有结果，直接用（记忆化）'.format(S['_inner']['now'])),
        'f[now] = m * n': '先把 `f[now]` 设成上界 `m*n`（最多每个格子操作一次）',
        'one_set.add': '`({i},{j})` 是 1，放进 `one_set`',
        'remove = 1 << (rx': '选 `({rx},{ry})` 为这一轮要操作的 1，先标记它自己',
        'remove |= 1 << (i': '同列的 `({i},{ry})` 也是 1 → 一起清掉',
        'remove |= 1<<': '同行的 `({rx},{j})` 也是 1 → 一起清掉',
        'f[now] = min': lambda S, B, ret: ('选 `({},{})`：它所在行、列的 1 一起清掉（`remove` = {}），剩下 `now ^ remove` = {}，递归去算 `calc({}) + 1`'
                                           .format(B['rx'], B['ry'], bin(B['remove'])[2:].zfill(6), B['now'] ^ B['remove'], B['now'] ^ B['remove'])),
        'return f[now]': '`f[{now}]` = =={ret}==（取各种操作里最小的）',
    },
    cards=dict(
        one_liner='把矩阵压成二进制数，对每个 1 试一次“清行清列”，取最少',
        complexity='时间 `O(2^(mn) · mn · (m+n))`，空间 `O(2^(mn))`',
        problem=['0/1 矩阵，每次选一个 1，把它所在行和列全部变成 0',
                 '求把所有 1 清掉的最少操作次数',
                 '本视频：`[[1,1,0],[0,1,1]]` → 2'],
        quote='对于矩阵中x行y列这个位置，可以认为是二进制数中的第x*n+y位，这样一来就可以将这个01矩阵变为一个长度为m*n的二进制数，从而使用状态压缩动态规划。',
        quote_src='—— yiduobo 题解',
        idea=['`f[state]` = 清空这个状态的最少操作数，`f[0] = 0`',
              '枚举 `state` 里的每个 1：同行同列的 1 合成 `remove`',
              '转移 `f[state] = min(f[state], f[state ^ remove] + 1)`，用记忆化递归实现'],
        result='最少操作 2 次',
        summary=['时间约 `O(2^(mn) · mn · (m+n))`，数据范围 mn ≤ 15 可接受',
                 '记忆化：`f[now] is None` 才计算，避免重复子状态',
                 '每次操作只会清掉 1，所以 `state ^ remove` 一定变小',
                 '位运算：格子 `(i,j)` 对应第 `i*n+j` 位',
                 '题面为 LeetCode 2174（VIP），上面是按 yiduobo 文章与题意整理'],
    ),
)
