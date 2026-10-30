N0 = 13


def _cell(S, r, c, v):
    if S.get('now') is None:
        return None
    if (r, c) == (S['now'], S['max_line']):
        return 'yellow'
    return 'green' if v is not None else None


def _cap_enter(S, B, ret):
    return f'`f[{S.now}][{S.max_line}]` 还没算过 → 先置 0，再枚举最后一行用多少张牌' if B.f[S.now][S.max_line] is None else f'`f[{S.now}][{S.max_line}]` ==已经算过== → 直接返回'


def _cap_one(S, B, ret):
    now, ml = S.now, S.max_line
    if (now - 2) % 3 == 0 and (now - 2) // 3 + 1 <= ml:
        return f'`{now} - 2` 能被 3 整除，且这一行需要 `{(now - 2) // 3 + 1}` 个落脚点 ≤ {ml} → =={now} 张牌全放当前行==，方案数 +1'
    return f'`{now}` 张牌不能恰好摆成一行（或落脚点不够）→ 保持 0'


def _cap_cnt(S, B, ret):
    return f'当前行用 `cnt = {S.cnt}` 张牌，需要 `{S.cnt // 3 + 1}` 个落脚点，当前最多 `{S.max_line}` 个 → ' + ('够，可以放' if S.cnt // 3 + 1 <= S.max_line else '不够，换下一种')


CONFIG = dict(
    num=2189, title='建造纸牌屋的方法数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='记忆化搜索 · 按行放牌',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def houseOfCards(self, n):

        f = [[None] * ((n - 2) // 3 + 2) for _ in range(n + 1)]

        def calc(now, max_line):
            if f[now][max_line] is None:
                f[now][max_line] = 0
                if (now - 2) % 3 == 0 and (now - 2) // 3 + 1 <= max_line:
                    f[now][max_line] = 1
                
                for cnt in range(2, now, 3):
                    if cnt // 3 + 1 <= max_line:
                        f[now][max_line] += calc(now - cnt, cnt // 3)
            
            return f[now][max_line]

        return calc(n, (n - 2) // 3 + 1)
''',
    call=f'Solution().houseOfCards({N0})',
    expect=2,
    max_steps=90,
    skip=['f = [[None]', 'def calc', 'for cnt in range', 'f[now][max_line] = 0'],
    views=[
        dict(type='table', var='f', label='f[牌数][落脚点]（· = 没算；绿 = 已记忆；黄 = 当前状态）', h=560, cell=40,
             rows=lambda S: [f'{k}张' for k in range(N0 + 1)], cols=lambda S: [f'{k}点' for k in range((N0 - 2) // 3 + 2)],
             color=_cell),
        dict(type='calls', h=150, hide=('f',)),
    ],
    watch=[('now', 'now', 'blue'), ('max_line', 'max_line', 'pink'), ('cnt', 'cnt', 'orange')],
    captions={
        'return calc(n': lambda S, B, r: (f'从 `{N0}` 张牌、最多 `{(N0 - 2) // 3 + 1}` 个落脚点开始搜' if r is None else f'答案 =={r}== 种'),
        'if f[now][max_line] is None': _cap_enter,
        'f[now][max_line] = 0': '先假设 0 种方案',
        'if (now - 2) % 3 == 0': _cap_one,
        'f[now][max_line] = 1': '一行 `k+1` 个落脚点要 `3k+2` 张牌 → 全放当前行是 ==1 种==',
        'for cnt in range': '枚举当前行用 `cnt` 张牌：`cnt = 3k + 2`，从 2 开始步长 3',
        'if cnt // 3 + 1 <= max_line': _cap_cnt,
        'f[now][max_line] += calc': '放 `cnt = {B.cnt}` 张在当前行 → 剩 `{B.now - B.cnt}` 张放上面，上一行只剩 `{B.cnt // 3}` 个落脚点 → 递归 `calc({B.now - B.cnt}, {B.cnt // 3})`',
        'return f[now][max_line]': '`f[{now}][{max_line}] = {ret}`，返回上一层',
    },
    cards=dict(
        one_liner='一行 3k+2 张牌撑起 k+1 个落脚点，再给上一行 k 个',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['用 `n` 张纸牌搭纸牌屋：每行由若干「三角形」（两张斜靠）和它们之间的横牌组成，上一行只能放在下一行的横牌上，每张牌都要用完',
                 '求不同纸牌屋的方案数（两个纸牌屋任一行的三角形数不同就算不同）',
                 f'本视频：`n = {N0}` → `2`'],
        quote='同一行中的纸牌数必然是3k + 2的形式，而这3k + 2张牌需要k + 1个落脚点，同时可以为下一行提供k个落脚点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：用 `i` 张牌、当前行最多 `j` 个落脚点的合法方案数',
              '当前行用 `cnt = 3k+2` 张牌，需要 `k+1 ≤ j`，然后剩下的牌放上面，落脚点只剩 `k`',
              '`i` 张牌恰好一行放完也是一种方案；用 `None` 区分「没算过」'],
        summary=['状态 `O(n^2)`，每个状态枚举 `O(n)` 种牌数，总计约 `O(n^3)`，n 小于等于 500 可过',
                 '`f` 初始化为 `None`，不能用 0，否则分不清「没算」和「0 种」',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '最后一行单独成一种（`f = 1`），其余情况靠 `for` 递归拆分'],
    ),
)
