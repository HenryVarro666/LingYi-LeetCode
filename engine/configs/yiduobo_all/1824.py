OB = [0, 1, 2, 3, 0]
N0 = len(OB)


def _rows(S):
    f, g = S.get('f'), S.get('g')
    if f is None:
        return None
    n = S['n']
    sh = lambda a: ['X' if v == n + 1 else v for v in a]
    return [sh(f), sh([x if x is not None else 0 for x in g])]


def _cell(S, r, c, v):
    idx = S.get('index')
    ob = S.get('obstacles')
    if idx is not None and S.get('_line', 0) >= 10 and c == S.get('pos') and r == 1:
        return 'yellow'
    if idx is not None and r == 0 and S.get('_line', 0) >= 10 and c == S.get('prev_pos'):
        return 'blue'
    return None


def _text(S):
    idx, ob = S.get('index'), S.get('obstacles')
    if idx is None:
        return '`f[p]` = 走到当前列、第 `p+1` 条跑道的最少侧跳次数；`X` = 有障碍（`n+1`）'
    return f'当前列 `index = {idx}`，障碍在跑道 `{ob[idx]}`（0 = 无）；上排 = 上一列 `f`，下排 = 本列 `g`'


CONFIG = dict(
    num=1824, title='最少侧跳次数', difficulty='Medium', category='网格图',
    author='yiduobo', technique='按列 DP（滚动两行）',
    tags=['灵神核心路线', '灵神题单·网格图', '灵神题单·动态规划', '难度分 1778'],
    code='''
class Solution(object):
    def minSideJumps(self, obstacles):

        n = len(obstacles)
        f = [1, 0, 1]
        if obstacles[0] != 0:
            f[obstacles[0] - 1] = n + 1
        
        g = [None] * 3
        for index in range(1, n):
            for pos in range(3):
                g[pos] = n + 1
                if obstacles[index] - 1 == pos:
                    continue
                
                for prev_pos in range(3):
                    if obstacles[index] - 1 == prev_pos:
                        continue
                    if prev_pos == pos:
                        delta = 0
                    else:
                        delta = 1
                    g[pos] = min(g[pos], f[prev_pos] + delta)
            
            f = g[:]
        
        return min(f)
''',
    call='Solution().minSideJumps([0, 2, 0])',
    expect=1,
    max_steps=100,
    skip=['n = len', 'if obstacles[0]', 'f[obstacles[0]', 'g = [None]', 'for pos in range', 'for prev_pos in range', 'else:', 'continue', 'g[pos] = n + 1', 'delta = 0', 'delta = 1', 'if prev_pos == pos'],
    views=[
        dict(type='text', fn=_text, size=22, h=55),
        dict(type='table', var=_rows, label='f = 上一列，g = 本列：三条跑道的最少侧跳次数', h=220, cell=100,
             rows=lambda S: ['f', 'g'], cols=lambda S: ['跑1', '跑2', '跑3'], color=_cell),
        dict(type='array', var='obstacles', label='obstacles（每个点的障碍所在跑道）', h=150, cell=80,
             pointers={'index': 'blue'}),
    ],
    watch=[('index', 'index', 'blue'), ('pos', 'pos', 'pink'), ('prev_pos', 'prev_pos', 'purple'), ('delta', 'delta', 'green')],
    captions={
        'f = [1, 0, 1]': '起点在跑道 2：到跑道 2 需 `0` 次；跑道 1、3 要在点 0 侧跳一次 → `f = [1, 0, 1]`',
        'if obstacles[index] - 1 == pos': lambda S, B, r: (f'第 {S.index} 列跑道 {S.pos+1} 有障碍 → 到不了，`g[{S.pos}]` 保持 `n+1`' if S.obstacles[S.index]-1 == S.pos else f'第 {S.index} 列跑道 {S.pos+1} 没有障碍，继续枚举上一步位置'),
        'if obstacles[index] - 1 == prev_pos': lambda S, B, r: (f'本列跑道 {S.prev_pos+1} 有障碍，青蛙落不到这里，不能当中转' if S.obstacles[S.index]-1 == S.prev_pos else f'上一列 `f[{S.prev_pos}]` 向右到本列跑道 {S.prev_pos+1}（无障碍），再侧跳到跑道 {S.pos+1}'),
        'g[pos] = min': '`g[{pos}] = min({B.g[pos]}, f[{prev_pos}] + {delta})` = =={g[pos]}==（`prev_pos == pos` 不用侧跳，否则 +1）',
        'f = g[:]': '本列算完：把 `g` 复制成新的 `f`（只依赖上一列，所以去掉 `index` 维）',
        'return min': '最后一列三条跑道取最小：`min({f})` = =={ret}==',
    },
    cards=dict(
        one_liner='按列做 DP：先在本列侧跳到 pos，再向右，没障碍就转移',
        complexity='时间 `O(n)`（常数 27），空间 `O(1)`',
        problem=['3 跑道、`n+1` 个点，青蛙从点 0 的跑道 2 出发，要到点 `n`',
                 '`obstacles[i] = x` 表示点 `i` 的跑道 `x` 有障碍；同点可侧跳到别的无障碍跑道',
                 '求最少侧跳次数；示例 `[0,1,2,3,0]` → `2`；演示用 `[0,2,0]` → `1`'],
        quote='令 f[index][p] 表示跳到第 index 列，第 p 行所需的最少侧跳次数……枚举上一步的所有位置 prev_p。尝试从 f[index - 1][prev_p] 跳到 f[index][prev_p]，再跳到 f[index][p]。',
        quote_src='—— yiduobo 题解',
        idea=['`f[p]`：到本列跑道 `p` 的最少侧跳次数，有障碍记为 `n + 1`',
              '枚举上一列的跑道 `prev_pos`：先向右到本列 `prev_pos`（要求没障碍），再侧跳到 `pos`',
              '`prev_pos == pos` 不用侧跳 `delta = 0`，否则 `delta = 1`'],
        summary=['每列只依赖上一列，滚动数组空间 `O(1)`，时间 `O(n)`',
                 '易错：初始 `f = [1, 0, 1]`，点 0 无障碍；障碍格必须置为 `n + 1`',
                 '作者说明可能还存在贪心做法，这里用的是 DP',
                 '同点侧跳可以到任何跑道，所以枚举 `prev_pos` 即覆盖侧跳'],
    ),
)
