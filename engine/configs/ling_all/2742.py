COST, TIME = [1, 2, 3, 2], [1, 2, 3, 2]


def _col(S, i, v):
    if S.get('_line') == 7 and 'j' in S and 't' in S:
        if i == S['j']:
            return 'yellow'
        if i == max(S['j'] - S['t'] - 1, 0):
            return 'blue'
    return None


def _txt(S):
    if 'c' in S and 't' in S:
        return f'当前物品：体积 `time+1 = {S["t"] + 1}`，价值 `cost = {S["c"]}`；`f[j]` = 体积和 ==至少== j 的最小花费'
    return '`f[j]` = 付费墙的 `time+1` 之和至少为 `j` 时的最小花费，要凑到 `n`'


CONFIG = dict(
    num=2742, title='给墙壁刷油漆', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='转成 0-1 背包 · 至少装满',
    tags=['难度分 2425'],
    code='''
class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        f = [0] + [inf] * n
        for c, t in zip(cost, time):
            for j in range(n, 0, -1):
                f[j] = min(f[j], f[max(j - t - 1, 0)] + c)
        return f[n]
''',
    call=f'Solution().paintWalls({COST}, {TIME})',
    expect=3,
    skip=['for j in range'],
    views=[
        dict(type='array', var='cost', label='cost（价值）', h=130, cell=70),
        dict(type='array', var='time', label='time', h=130, cell=70),
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='array', var='f', label='f[j]（黄 = 正在更新，蓝 = 来源）', h=200, cell=100, color=_col),
    ],
    watch=[('c', 'c', 'pink'), ('t', 't', 'blue'), ('j', 'j', 'yellow'), ('n', 'n', 'cyan')],
    captions={
        'n = len(cost)': '`n = {n}` 面墙：付费刷 `a` 面，免费最多刷 `Σtime` 面，要求 `a + 免费 = n`',
        'f = [0] + [inf]': '`f[j]`：体积和至少 j 的最小花费。`f[0] = 0`，其余先设为无穷大',
        'for c, t in zip': lambda S, B, r: (f'考虑物品：`cost = {S.c}`，`time = {S.t}`，体积 `time + 1 = {S.t + 1}`（付费刷它 + 免费刷 `{S.t}` 面）' if S.get('c') is not None and (S.get('c'), S.get('t')) != (B.get('c'), B.get('t')) or B.get('c') is None
                                            else '所有墙都考虑过了'),
        'f[j] = min': lambda S, B, r: f'不选 `{B.f[S.j]}`，选 `f[{max(S.j - S.t - 1, 0)}] + {S.c} = {S.f[max(S.j - S.t - 1, 0)] + S.c}`，取小 → `f[{S.j}]` = =={S.f[S.j]}==' + ('；体积已超出，下标截到 0' if S.j - S.t - 1 < 0 else ''),
        'return f[n]': '体积和至少为 `n` 的最小花费：=={ret}==',
    },
    cards=dict(
        one_liner='付费刷 1 面 = 体积 time+1，至少凑够 n',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['付费油漆匠刷第 `i` 面花 `cost[i]` 钱、`time[i]` 时间',
                 '免费油漆匠 1 单位时间刷 1 面，但付费匠工作时才干活',
                 '示例：`cost=time=[1,2,3,2]` → `3`（付费刷 0、1 号）'],
        quote='根据题意，付费刷墙个数 + 免费刷墙个数 = n。同时，付费刷墙时间之和必须 ≥ 免费刷墙个数。……得到：「付费刷墙时间+1」之和 ≥ n。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['设付费墙 `a` 面：免费墙 `n−a` 面 ≤ 付费总时间',
              '移项：`Σ(time[i]+1) ≥ n`，把 `time+1` 当体积、`cost` 当价值',
              '问题变成「体积和至少 n 的最小价值」：0-1 背包的至少装满'],
        summary=['时间 `O(n^2)`，空间 `O(n)`；`j` 倒序，每面墙只选一次',
                 '易错：体积不足时下标要 `max(j-t-1, 0)`，表示「已经凑够」',
                 '方法一用 `dfs(i, j)` 记付费时间 − 免费时间的差，同样 `O(n^2)`',
                 '另有手写 min/max 的快写法，思路一样'],
    ),
)
