CONFIG = dict(
    num=3178, title='找出 K 秒后拿着球的孩子', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='divmod · 往返周期', tags=[],
    code='''
class Solution:
    def numberOfChild(self, n: int, k: int) -> int:
        k, t = divmod(k, n - 1)
        return n - t - 1 if k % 2 else t
''',
    call='Solution().numberOfChild(5, 6)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"`k` 秒 = ==`{S['k']}`== 趟单程 + 余 ==`{S['t']}`== 步" if 't' in S else f"`n = {S['n']}`，球在 `0` 到 `{S['n']-1}` 之间来回传"), size=30),
        dict(type='array', var=lambda S: list(range(S['n'])), pointers={'t': 'blue'}, label='孩子编号（蓝 = 从左端数 t 步）', h=260),
        dict(type='text', fn=lambda S: (f"趟数 `{S['k']}` 是{'奇数 → 球正向左走：从右端数 t 步' if S['k'] % 2 else '偶数 → 球正向右走：从左端数 t 步'}" if 't' in S else ''), size=28),
    ],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'yellow'), ('t', 't', 'pink')],
    captions={
        'divmod': '单程要 `n-1 = {n-1}` 秒。`k` 秒走了 ==`{k}`== 个单程，余下 ==`{t}`== 秒（此时 k 已变成趟数）',
        'return': '趟数 `{k}` 是{"奇数：方向向左，球在 `n - t - 1 = " + str(n - t - 1) + "`" if k % 2 else "偶数：方向向右，球在 `t = " + str(t) + "`"} → ==`{ret}`==',
    },
    cards=dict(
        after=[dict(heading='手推一遍 n = 5, k = 6', lines=[
            '球的位置：`0 → 1 → 2 → 3 → 4`（4 秒，到右端）',
            '再 `4 → 3 → 2`（又走 2 秒，共 6 秒）',
            '`divmod(6, 4) = (1, 2)`：1 个单程，余 2 步',
            '趟数奇数 → 从右端 4 往回数 2 步 → `4 - 2 = 2`']),],
        one_liner='传球是往返运动：先数走了几个单程，再看余数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 个孩子站成一排，0 号拿球向右传，每秒传一位，到端点就反向',
                 '求 `k` 秒后拿球的孩子编号',
                 '示例：`n = 5, k = 6` → `2`'],
        quote='和 2582. 递枕头是一样的，那题下标从 1 开始，本题下标从 0 开始。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从一端走到另一端要 `n-1` 秒，所以用 `divmod(k, n-1)` 拆成（趟数，余数）',
              '趟数为偶数：方向向右，位置就是余数 `t`',
              '趟数为奇数：方向向左，从右端 `n-1` 往回数 `t` 步，即 `n-t-1`'],
        summary=['时间、空间都是 `O(1)`，不用模拟',
                 '除数是 ==n-1==（单程秒数），不是 n',
                 '==k 被 divmod 覆盖成了趟数==，后面的 `k % 2` 看的是趟数奇偶',
                 '同类：2582 递枕头（下标从 1 开始）'],
    ),
)
