COST, TIME = [1, 2, 3, 2], [1, 2, 3, 2]


def _col(S, i, v):
    ln = S.get('_line')
    if ln in (14, 15) and 'index' in S and 't' in S:
        if i == S['index']:
            return 'yellow'
        if i == S['index'] - S['t'] - 1:
            return 'blue'
    if ln in (10, 11) and i == S.get('n'):
        return 'yellow'
    if ln in (17, 18) and i == S.get('index'):
        return 'yellow'
    return None


def _txt(S):
    if 'c' in S and 't' in S:
        return f'这位付费匠：花 `{S["c"]}` 钱，刷 1 面 + 白嫖 `{S["t"]}` 面 = ==刷掉 {S["t"] + 1} 面=='
    return '`f[j]` = 刷掉 `j` 面墙的最小花销（None = 凑不出）'


CONFIG = dict(
    num=2742, title='给墙壁刷油漆', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包 · 一次刷掉 time+1 面',
    tags=['难度分 2425'],
    code='''
class Solution(object):
    def paintWalls(self, cost, time):

        n = len(cost)
        f = [None] * (n + 1)
        f[0] = 0
        res = None
        for c, t in zip(cost, time):
            if t + 1 >= n:
                if f[n] is None or f[n] > c:
                    f[n] = c
            else:
                for index in range(n, t, -1):
                    if f[index - (t + 1)] is not None and (f[index] is None or f[index] > f[index - (t + 1)] + c):
                        f[index] = f[index - (t + 1)] + c
                for index in range(t, 0, -1):
                    if f[index] is None or f[index] > c:
                        f[index] = c

        return f[-1]
''',
    call=f'Solution().paintWalls({COST}, {TIME})',
    expect=3,
    skip=['for index in range', 'res = None'],
    views=[
        dict(type='array', var='cost', label='cost', h=130, cell=70),
        dict(type='array', var='time', label='time', h=130, cell=70),
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='array', var='f', label='f[j]：刷掉 j 面的最小花销（黄 = 写入，蓝 = 来源）', h=200, cell=100, color=_col),
    ],
    watch=[('c', 'c', 'pink'), ('t', 't', 'blue'), ('index', 'index', 'yellow'), ('n', 'n', 'cyan')],
    captions={
        'n = len(cost)': '`n = {n}` 面墙，目标是 `f[n]`：刷掉全部墙',
        'f = [None]': '`f[j]`：刷掉 `j` 面墙的最小花销；None 表示还凑不出',
        'f[0] = 0': '一面都不刷，花 0 元',
        'for c, t in zip': lambda S, B, r: (f'考虑付费方案：`cost = {S.c}`，`time = {S.t}`，等价于花 `{S.c}` 刷 `{S.t + 1}` 面' if S.get('c') is not None and (S.get('c'), S.get('t')) != (B.get('c'), B.get('t')) or B.get('c') is None
                                            else '所有方案都考虑完'),
        'if t + 1 >= n': lambda S, B, r: (f'`t + 1 = {S.t + 1} >= n = {S.n}`：这一个人就能刷完全部，直接尝试 `f[n] = c`' if S.t + 1 >= S.n
                                           else f'`t + 1 = {S.t + 1} < n = {S.n}`：不能一次刷完，走普通背包转移'),
        'if f[n] is None or f[n] > c': lambda S, B, r: (f'`f[n]` 是 `{S.f[S.n]}`，没有或比 `{S.c}` 大 → 更新为 `{S.c}`' if S.f[S.n] is None or S.f[S.n] > S.c
                                                         else f'`f[n]` 已是 `{S.f[S.n]}`，不比 `{S.c}` 大 → 不更新'),
        'f[n] = c': '`f[{n}] = {c}`',
        'if f[index - (t + 1)] is not None': lambda S, B, r: (lambda src: (f'`index = {S.index}`：来源 `f[{S.index - S.t - 1}]` 凑不出，跳过' if src is None
                                                              else f'`index = {S.index}`：来源 `f[{S.index - S.t - 1}] + {S.c} = {src + S.c}`，' + ('比现有更小 → 更新' if S.f[S.index] is None or S.f[S.index] > src + S.c else '不比现有更小 → 不变')))(S.f[S.index - S.t - 1]),
        'f[index] = f[index - (t + 1)] + c': '`f[{index}] = {f[index]}`（`f[{index - t - 1}] + {c}`）；`index` 倒序，保证每个方案只用一次',
        'if f[index] is None or f[index] > c': lambda S, B, r: (f'`index = {S.index} <= t`：这个人一个就够刷 `{S.index}` 面，花 `{S.c}`；' + ('比现有更小 → 更新' if S.f[S.index] is None or S.f[S.index] > S.c else f'现有 `{S.f[S.index]}` 更小 → 不变')),
        'f[index] = c': '`f[{index}] = {c}`',
        'return f[-1]': '刷完 `n` 面墙的最小花销 =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='雇一位匠人，等价于花 cost 刷掉 time+1 面墙',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['付费匠刷第 `i` 面花 `cost[i]`、用 `time[i]` 时间',
                 '免费匠每面 1 时间，只能在付费匠工作时干活',
                 '示例：`cost=time=[1,2,3,2]` → `3`'],
        quote='雇佣一位花费为cost[i]的粉刷匠可以工作time[i]的时间，也就是可以白嫖刷掉time[i]堵墙。换言之，雇佣这位粉刷匠相当于使用cost[i]来刷掉time[i] + 1堵墙。',
        quote_src='—— yiduobo 题解原文',
        idea=['雇一位付费匠：自己刷 1 面 + 免费匠陪刷 `time` 面',
              '转成背包：体积 `time+1`，价值 `cost`，目标是刷掉 `n` 面',
              '与常规背包不同：体积可超过 `n`，要单独处理'],
        summary=['时间 `O(n^2)`，空间 `O(n)`（倒序省掉 i 维）',
                 '易错：`time+1 ≥ j` 时一个人就够，只能取 `cost` 本身',
                 '大的 `index` 倒序转移，小的 `index ≤ t` 直接取 `c`',
                 '原文可直接在 Python 3 运行，未做修改',
                 '对比灵神：他用 `max(j-t-1, 0)` 一行合并这两种情况'],
    ),
)
