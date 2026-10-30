def _txt(S):
    if 'q' not in S or 'p' not in S:
        return '先把每个 limit 与 `n-1` 取小，再排序'
    lim, n = S['limit'], S['n']
    return f'`p = {S["p"]}` 对应 `{lim[S["p"]]}`；`q = {S["q"]}` 是它能配的最小下标；后缀和 `s` = =={S["s"]}=='


CONFIG = dict(
    num=3802, title='给纸张涂色的方式数量', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 双指针 + 后缀和',
    tags=[],
    code='''
class Solution(object):
    def numberOfWays(self, n, limit):

        for index, v in enumerate(limit):
            limit[index] = min(v, n - 1)

        limit.sort()
        q = len(limit)
        s = 0
        res = 0
        mod = 10 ** 9 + 7
        for p in range(len(limit)):
            while q > 0 and limit[p] + limit[q - 1] >= n:
                q -= 1
                s += limit[q]

            res = (res + (limit[p] - n + 1) * (len(limit) - q) % mod + s) % mod
            if limit[p] * 2 >= n:
                res = (res - (limit[p] - (n - limit[p]) + 1) + mod) % mod

        return res
''',
    call='Solution().numberOfWays(5, [3,6,2,4,1])',
    expect=34,
    views=[
        dict(type='text', h=70, size=28, fn=_txt),
        dict(type='array', var='limit', label='limit（取小并排序后）；框 = 下标 [q, m-1]，都能和 p 配对', pointers={'p': 'blue', 'q': 'pink'},
             window=('q', 'len(limit) - 1'), h=300, cell=100,
             dim=lambda S, i, v: 'q' in S and i < S['q']),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('s', 's', 'cyan'), ('res', 'res', 'green')],
    captions={
        'limit[index] = min': '`limit[{index}]` 与 `n-1 = {n-1}` 取小：每对颜色里另一种至少涂 1 张，所以最多 `n-1`',
        'limit.sort()': '排序后 `{limit}`：`p` 增大时，能配的最小下标 `q` 单调不增',
        'q = len': '`q` 从末尾开始，往左扩展（后缀 `[q, m-1]`）',
        9: '`s` = `limit[q] + … + limit[m-1]`（后缀和）',
        10: '`res` 累计方案数',
        'mod = ': '答案对 `10^9+7` 取模',
        'for p in range': '`p` 枚举涂前半段的颜色，下标 {p}',
        'while q > 0': lambda S, B, r: (
            f'`{S.limit[S.p]} + {S.limit[S.q - 1]} ≥ {S.n}`：`q-1` 也能配，后缀扩大' if S.q > 0 and S.limit[S.p] + S.limit[S.q - 1] >= S.n
            else ('`q` 已到最左，没有更多颜色了：停' if S.q == 0 else
                  f'`{S.limit[S.p]} + {S.limit[S.q - 1]} < {S.n}`：再往左的配不上 `p`：停')),
        'q -= 1': '`q` 左移到 {q}',
        's += limit[q]': '`limit[{q}] = {limit[q]}` 加进后缀和：`s` = {s}',
        'res = (res + (limit[p]': lambda S, B, r: (
            f'`p` 与后缀 `{len(S.limit) - S.q}` 种颜色配对：`({S.limit[S.p]}−{S.n}+1)×{len(S.limit) - S.q} + s({S.s})` → `res` = =={S.res}=='),
        'if limit[p] * 2 >= n': lambda S, B, r: (
            '`limit[p]×2 ≥ n`：后缀里包含 `p` 自己，要扣掉' if S.limit[S.p] * 2 >= S.n else '`limit[p]×2 < n`：`p` 不在后缀里，不用扣'),
        'res = (res - (limit[p]': '同一种颜色不能涂两段：减去 `{limit[p]} − ({n} − {limit[p]}) + 1` → `res` = =={res}==',
        'return res': '一共 `{res}` 种方案',
    },
    cards=dict(
        one_liner='排序后，p 越大，能配的最小 q 越靠左：用后缀和一次算完',
        complexity='时间 `O(m log m)`，空间 `O(1)`',
        problem=['`n` 张纸，每种颜色 `k` 最多涂 `limit[k]` 张',
                 '恰好用两种颜色，各涂连续的一段，求涂色方案数（模 `10^9+7`）',
                 '本视频：`n=5`，`limit=[3,6,2,4,1]` → `34`'],
        quote='如果在这里不考虑涂色的方案数，而是只考虑可以涂色的颜色对数量，问题就转化成了经典的两数之和，排序后使用两个指针从两侧向中间移动就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a` 涂前半段、`b` 涂后半段：`a` 的张数在 `n−limit[b]` 到 `limit[a]` 之间，共 `limit[a]−(n−limit[b])+1` 种',
              '`p` 能和 `q..m-1` 全部配对，提出 `limit[p]−n+1`，剩下后缀和 `s`',
              '`p` 变大时 `q` 只会左移，`s` 同步更新；`q ≤ p` 时要减去和自己配对'],
        summary=['时间 `O(m log m)`，空间 `O(1)`',
                 '`limit` 先与 `n-1` 取小，保证两种颜色都至少涂一张',
                 '当 `limit[p]×2 ≥ n`，`p` 会和自己配对，必须减掉',
                 '`p` 当前颜色涂前半段，两种颜色次序不同算两种方案，所以每个 `p` 都枚举',
                 '原文是 Python 2 风格，无需改动即可在 Python 3 运行'],
    ),
)
