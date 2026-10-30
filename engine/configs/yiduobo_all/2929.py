def _case(S):
    n, L = S['n'], S['limit']
    return 0 if n <= L else 1 if n <= 2 * L else 2 if n <= 3 * L else 3


CONFIG = dict(
    num=2929, title='给小朋友们分糖果 II', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按 limit 的倍数分档 · 等差数列求和',
    tags=[],
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
    call='Solution().distributeCandies(8, 5)',
    expect=27,
    views=[
        dict(type='text', fn=lambda S: f"`n = {S['n']}`，`limit = {S['limit']}`：档位边界 `{S['limit']}`、`{2 * S['limit']}`、`{3 * S['limit']}`", size=26, h=70),
        dict(type='array', var=lambda S: [f"n ≤ {S['limit']}", f"≤ {2 * S['limit']}", f"≤ {3 * S['limit']}", f"> {3 * S['limit']}"],
             label='n 落在哪一档（黄 = 当前档）', cell=200, h=190, index=False,
             color=lambda S, i, v: 'yellow' if i == _case(S) else None),
    ],
    watch=['n', 'limit', 'left', 'right'],
    captions={
        'if n <= limit': '`n = {n}` 不大于 `limit = {limit}`？否则继续看下一档' ,
        'elif limit < n <= limit * 2': '`{limit} < {n} <= {limit*2}` 成立吗？成立说明剩下糖会碰到「单人上限」，要分两段数',
        'left = ': '前一段：第一个人拿 `0 ~ n−limit−1` 颗，剩下两人受上限约束，等差数列求和 = =={left}==',
        'right = ': '后一段：第一个人拿 `n−limit ~ limit` 颗，剩下的不超限，方案数 `n−k+1`，求和 = =={right}==',
        'return left + right': '两段相加：`{left} + {right}` = =={ret}==',
        'return (1 + n': '`n ≤ limit` 时没有任何限制：`(n+2)(n+1)/2` 种',
        'return (limit * 3': '`2·limit < n ≤ 3·limit`：等差数列 `1 … 3·limit−n+1` 求和 = =={ret}==',
        'return 0': '`n > 3·limit`，必有人超限 → 0 种',
    },
    max_steps=60,
    cards=dict(
        one_liner='按 n 与 limit 的倍数关系分档，每档用等差数列求和',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `n` 颗糖分给 3 个小朋友，每人不超过 `limit` 颗（可以为 0）',
                 '求总方案数',
                 '示例：`n = 5, limit = 2` → `3`；本视频取 `n = 8, limit = 5` → `27`'],
        quote='由于题目只限定了3个小朋友，那么完全可以从1到3逐个推导。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看 1 个人、2 个人，再推到 3 个人',
              '3 个人时枚举第一个人拿 `k` 颗，剩下 `n−k` 颗交给两人的结论',
              '`n−k` 落在 `≤ limit` 还是 `(limit, 2limit]`，方案数公式不同 → 分档、等差数列求和'],
        summary=['时间、空间 `O(1)`',
                 '原文为 Python 2 写法，题解里的除法已是 `//`，无需改动',
                 '易错点：分档边界（`<` 还是 `<=`）和等差数列的首项、末项',
                 '对比灵神：灵神用隔板法 + 容斥，一行公式；yiduobo 分档讨论'],
    ),
)
