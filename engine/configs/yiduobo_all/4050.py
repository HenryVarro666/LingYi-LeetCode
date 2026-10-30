def _fv(S):
    f = S.get('f')
    return None if f is None else [('—' if x is None else x) for x in f]


def _txt(S):
    if 'f' not in S:
        return '先预处理三角形数 `candidate[k] = (1+k)×k/2`，它们是物品的体积'
    if 'cost' in S and 'v' in S:
        return f"物品：连胜 `{S['cost']}` 天得 `{S['v']}` 分，代价 `{S['cost']} + 1` 天"
    return '`f[x]`：恰好凑出 x 分的最少天数，`—` 表示还凑不出'


def _col(S, k, val):
    if 'x' not in S or 'v' not in S or S.get('_line') not in (15, 16, 17):
        return None
    if k == S['x']:
        return 'green'
    if k == S['x'] - S['v']:
        return 'blue'
    return None


def _cap_if(S, B, ret):
    x, v, cost, f = S.x, S.v, S.cost, S.f
    p = f[x - v]
    if p is None:
        return f'`f[{x - v}]` 还凑不出 → 不能从它转移'
    cur = B.f[x]
    nv = p + cost + 1
    if cur is None:
        return f'`f[{x}]` 还没有值，`f[{x - v}] + {cost} + 1 = {nv}` → ==更新=='
    if cur > nv:
        return f'`f[{x}] = {cur} > {p} + {cost} + 1 = {nv}` → ==更新为 {nv}=='
    return f'`f[{x}] = {cur} ≤ {nv}` → 不更新'


CONFIG = dict(
    num=4050, title='得到恰好 N 分的最少天数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='完全背包（预处理三角形数）',
    code='''
class Solution(object):
    def minDays(self, n):
        
        candidate = [0]
        while candidate[-1] <= n:
            candidate.append(candidate[-1] + len(candidate))
        
        f = [None] * (n + 1)
        f[0] = -1
        for cost in range(len(candidate) - 1, 0, -1):
            v = candidate[cost]
            for x in range(v, n + 1):
                if f[x - v] is not None and (f[x] is None or f[x] > f[x - v] + cost + 1):
                    f[x] = f[x - v] + cost + 1
        
        return f[n]
''',
    call='Solution().minDays(12)',
    expect=7,
    views=[
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='array', var='candidate', label='candidate[k]：连胜 k 天的得分', cell=80, h=170,
             color=lambda S, k, v: 'orange' if S.get('cost') == k and 'f' in S else None),
        dict(type='array', var=_fv, label='f[x]：恰好得 x 分的最少天数', color=_col,
             pointers={'x': 'green', 'x - v': 'blue'}, pointer_labels={'x - v': 'x-v'}, cell=66, h=230),
    ],
    watch=[('cost', 'cost', 'orange'), ('v', 'v', 'orange'), ('x', 'x', 'green'), ('x-v', 'x - v', 'blue')],
    skip=['for x in range', 'v = candidate[cost]'],
    max_steps=80,
    captions={
        'candidate = [0]': '`candidate[k] = 1+2+…+k`，从 `0` 开始',
        'while candidate[-1] <= n': lambda S, B, ret: (f'最后一个 `{S.candidate[-1]}` ≤ `{S.n}`，还要继续生成' if S.candidate[-1] <= S.n else f'最后一个 `{S.candidate[-1]}` 已经超过 `n = {S.n}`，不用再生成'),
        'candidate.append': '新三角形数 = 上一个 + 当前长度 → `{candidate}`',
        'f = [None]': '`f` 全设为 `None`：表示还凑不出',
        'f[0] = -1': '`f[0] = -1`：第一次选物品不需要前面的跳过日，提前减 1 抵消多算的一天',
        'for cost in range': lambda S, B, ret: (f'物品 `cost = {S.cost}`：连胜 {S.cost} 天，体积 `{S.candidate[S.cost]}`，代价 `{S.cost} + 1` 天' if S.get('cost') != B.get('cost') or 'cost' not in B else '所有物品都处理完了'),
        'if f[x - v] is not None': _cap_if,
        'f[x] = f[x - v]': '`f[{x}] = f[{x - v}] + {cost} + 1` = =={f[x]}==',
        'return f[n]': '`f[{n}]` = =={ret}==（连胜 3 天、跳 1 天、再连胜 3 天）',
    },
    cards=dict(
        one_liner='用最少的三角形数拼出 n，每件代价多算一天跳过',
        complexity='时间 `O(n√n)`，空间 `O(n)`',
        problem=['连胜第 k 天得 k 分，跳过一天连胜清零',
                 '求恰好得到 `n` 分的最少天数（含跳过的天数）',
                 '本视频：`n = 12` → `7`（`1+2+3`，跳过，`1+2+3`）'],
        quote='题目实际上就是要用最少的(1 + k) * k // 2来拼凑出n，这是一个标准的背包问题……将k + 1作为使用这个物品的代价。',
        quote_src='—— yiduobo 题解',
        idea=['先预处理不超过 `n` 的所有 `(1+k)×k//2`，作为物品体积',
              '用 `k + 1` 作代价：物品之间至少要隔 1 天跳过',
              '第一次选不需要间隔，所以 `f[0]` 初值设为 `-1` 来抵消'],
        summary=['时间 `O(n√n)`，空间 `O(n)`',
                 '易错点：`None` 表示不可达，转移前要先判断 `f[x - v] is not None`',
                 '内层 `x` 从小到大，同一件物品可以重复选',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行'],
    ),
)
