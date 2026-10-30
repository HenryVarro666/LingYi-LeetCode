def _case(S):
    n, lim = S['n'], S['limit']
    if n <= lim:
        return f'`n={n} ≤ limit={lim}`：每人都不会超限'
    if n <= 2 * lim:
        return f'`limit={lim} < n={n} ≤ 2·limit`：第一个人拿的数目要受限'
    if n <= 3 * lim:
        return f'`2·limit < n={n} ≤ 3·limit`：只剩下很窄的区间'
    return f'`n={n} > 3·limit`：无解'


CONFIG = dict(
    num=2928, title='给小朋友们分糖果 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='按 limit 分档 · 等差数列求和', tags=[],
    code='''
class Solution(object):
    def distributeCandies(self, n, limit):

        if n <= limit:
            return (1 + n + 1) * (n + 1) // 2
        elif limit < n <= limit * 2:
            left = (n + 2) * (limit * 2 - n + 1) // 2
            right = (limit * 3 - n + 1) * (n - limit) // 2
            return left + right
        elif limit * 2 < n <= limit * 3:
            return (limit * 3 - n + 2) * (limit * 3 - n + 1) // 2
        else:
            return 0
''',
    call='Solution().distributeCandies(5, 3)',
    expect=12,
    views=[
        dict(type='text', size=38, h=110, fn=_case),
        dict(type='text', size=38, h=110, fn=lambda S: (
            f"`left = {S['left']}`（第一人拿 0 到 n−limit−1 颗）" if 'left' in S else '')),
        dict(type='text', size=38, h=110, fn=lambda S: (
            f"`right = {S['right']}`（第一人拿 n−limit 到 limit 颗）" if 'right' in S else '')),
    ],
    watch=['n', 'limit', 'left', 'right'],
    captions={
        'if n <= limit': '`{n} <= {limit}`？ 是：每人都够，等差数列 `(n+2)(n+1)/2`；否：继续分档',
        'elif limit < n <= limit * 2': '`{limit} < {n} <= {limit*2}`？ 第一个人拿的数量 `k` 分两段，剩余糖果落在不同档',
        'left = ': '`k` 在 `0 ~ n−limit−1`：剩余 `n−k` 在 `limit+1 ~ 2·limit`，等差数列和 = `{left}`',
        'right = ': '`k` 在 `n−limit ~ limit`：剩余不超过 `limit`，等差数列和 = `{right}`',
        'return left + right': '两段相加：`{left} + {right}` = =={ret}==',
        'elif limit * 2 < n': '`{limit*2} < {n} <= {limit*3}`？ 第一个人至少拿 `n−2·limit` 颗',
        'return (limit * 3': '只剩一个等差数列：`1 + 2 + … + (3·limit−n+1)` = =={ret}==',
        'return 0': '`n > 3·limit`：必有人超限 → `0`',
    },
    cards=dict(
        one_liner='三个小朋友，从 1 个推到 3 个，按 limit 的倍数给 n 分档',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 颗糖分给 3 个小朋友，每人不超过 `limit` 颗，求方案数',
                 '本视频：`n=5, limit=3` → `12`'],
        quote='将n按照limit的倍数进行分档。n > limit * 3的情况，显然是无解。',
        quote_src='—— yiduobo 题解原文',
        idea=['先固定第一个小朋友拿 `k` 颗，剩下 `n−k` 分给两个人',
              '两个人的方案数随 `n−k` 与 `limit` 的大小分两种，对 `k` 求和就是等差数列',
              '`n` 落在 `(limit, 2·limit]` 时 `k` 要拆成两段，所以有 `left` 和 `right`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文已是 `//` 整除，无需修改',
                 '易错：分档边界 `limit < n <= 2·limit` 要写全',
                 '对比灵神：灵神用隔板法 + 容斥一行公式；这里是分档 + 等差数列'],
    ),
)
