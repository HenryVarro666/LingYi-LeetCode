def _zone(S, i, v):
    lim = S['limit']
    if i <= lim:
        return 'green'
    if i <= 2 * lim:
        return 'yellow'
    if i <= 3 * lim:
        return 'orange'
    return None


def _top(S):
    n, lim = S['n'], S['limit']
    if n <= lim:
        z = '第 1 档：`n ≤ limit`，任何一个小朋友都不会超限'
    elif n <= 2 * lim:
        z = '第 2 档：`limit < n ≤ 2×limit`，第一个人分 k 颗，剩下 n−k 可能落在两种情况'
    elif n <= 3 * lim:
        z = '第 3 档：`2×limit < n ≤ 3×limit`，第一个人至少要分 `n − 2×limit` 颗'
    else:
        z = '`n > 3×limit`：三个人加起来也装不下，无解'
    return z


def _form(S):
    n, lim = S['n'], S['limit']
    if 'left' in S and 'right' in S:
        return f'左半 `({n}+2)×({2*lim}−{n}+1)/2` = {S["left"]}，右半 `({3*lim}−{n}+1)×({n}−{lim})/2` = {S["right"]}，相加 = =={S["left"] + S["right"]}=='
    return f'`n = {n}`，`limit = {lim}`，`3×limit = {3 * lim}`'


CONFIG = dict(
    num=2927, title='给小朋友们分糖果 III', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='按 limit 分档 + 等差数列求和',
    tags=['灵神题单·数学算法'],
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
    call='Solution().distributeCandies(3, 2)',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='array', var=lambda S: list(range(0, 3 * S['limit'] + 2)), pointers={'n': 'blue'},
             color=_zone, label='n 的取值（绿：≤limit　黄：≤2limit　橙：≤3limit）', h=220),
        dict(type='text', fn=_form, size=26, h=120),
    ],
    watch=['n', 'limit', 'left', 'right'],
    captions={
        'if n <= limit': '`n ≤ limit`（{n} ≤ {limit}）？{"成立" if n <= limit else "不成立"}：先看是不是最小的一档',
        'return (1 + n + 1)': '`k` 从 0 到 n，剩下的方案数 n+1, n, …, 1 → 等差数列求和 =={ret}==',
        'elif limit < n <= limit * 2': '`limit < n ≤ 2×limit`（{limit} < {n} ≤ {limit*2}）→ {"成立，分两段求和" if limit < n <= limit*2 else "不成立，继续看下一档"}',
        'left = ': '`k` 在 `n−limit` 到 `limit` 之间：剩下 `n−k ≤ limit`，每个 `k` 有 `n−k+1` 种 → 左半 =={left}==',
        'right = ': '`k` 在 `0` 到 `n−limit−1` 之间：剩下 `n−k > limit`，每个 `k` 有 `2×limit−(n−k)+1` 种 → 右半 =={right}==',
        'return left + right': '两段之和 `{left} + {right}` = =={ret}==',
        'elif limit * 2 < n': '`2×limit < n ≤ 3×limit` ？',
        'return (limit * 3': '第一个人只能拿 `n−2×limit` 到 `limit` 颗，等差数列从 1 到 `3×limit−n+1` → =={ret}==',
        'return 0': '`n > 3×limit`，每人最多 `limit` 颗，装不下 → 0',
    },
    cards=dict(
        one_liner='把 n 按 limit 的倍数分档，每档是一个等差数列求和',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 颗糖分给 3 个小朋友，每人不超过 `limit` 颗，求方案数',
                 '示例：`n = 5, limit = 2` → `3`',
                 '本视频：`n = 3, limit = 2` → `7`（总共 10 种，去掉 3 种有人拿 3 颗的）'],
        quote='由于题目只限定了3个小朋友，那么完全可以从1到3逐个推导。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想 1 个人：`0 ≤ n ≤ limit` 有 1 种；再想 2 个人：`n ≤ limit` 有 `n+1` 种，`limit < n ≤ 2limit` 有 `2limit−n+1` 种',
              '3 个人：枚举第一个人拿 `k` 颗，剩下 `n−k` 交给 2 人的结论',
              '`k` 变化时方案数成等差数列 → 用求和公式，分 4 档写出答案'],
        summary=['时间、空间都是 `O(1)`',
                 '分档边界要写对：`limit < n ≤ 2limit` 要拆成左、右两段求和',
                 '原文已经是 `//` 整除写法，代码无需修改',
                 '对比灵神：灵神用容斥一行搞定；yiduobo 逐档手推，更直观但分支多'],
    ),
)
