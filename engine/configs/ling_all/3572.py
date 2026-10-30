def _lp(names, txt, end):
    def f(S, B, r):
        if all(n in B and B[n] == S[n] for n in names):
            return end
        return txt(S)
    return f


def _cur(S, i):
    a, b = S.get('a'), S.get('b')
    return a is not None and S['x'][i] == a and S['y'][i] == b


CONFIG = dict(
    num=3572, title='选择不同 X 值三元组使 Y 值之和最大', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='按 x 分组取最大 y · 前三大求和',
    tags=[],
    code='''
class Solution:
    def maxSumDistinctTriplet(self, x: List[int], y: List[int]) -> int:
        mx = defaultdict(int)
        for a, b in zip(x, y):
            mx[a] = max(mx[a], b)
        if len(mx) < 3:
            return -1
        return sum(nlargest(3, mx.values()))  # 底层用的堆
''',
    call='Solution().maxSumDistinctTriplet([1,2,1,3,2], [5,3,4,6,2])',
    expect=14,
    views=[
        dict(type='array', var='x', label='x（蓝 = 当前这一对）', h=190, cell=80,
             color=lambda S, i, v: 'blue' if _cur(S, i) else None),
        dict(type='array', var='y', label='y', h=170, cell=80,
             color=lambda S, i, v: 'blue' if _cur(S, i) else None),
        dict(type='map', var='mx', label='mx（每个 x 值对应的最大 y）', fmt=lambda k, v: f'x={k}: {v}', h=170, font=30),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"分组数 `len(mx) = {len(S['mx'])}`" if 'mx' in S and S.get('_line', 0) >= 7 else '每组 x 值只能选一个 y，当然选最大的')),
    ],
    watch=['a', 'b', ('ans', 'ans', 'green')],
    captions={
        'mx = defaultdict': '`mx[v]`：x 值为 `v` 的所有 y 中的最大值，默认 `0`',
        'for a, b in zip': _lp(['a', 'b'], lambda S: f'取下标对应的一对：`x = {S.a}`，`y = {S.b}`', '所有下标都处理完，`mx` 建好了'),
        'mx[a] = max': '`mx[{a}] = max({B.mx.get(a, 0)}, {b})` = =={mx[a]}==：同一个 x 值只留最大的 y',
        'if len(mx) < 3': lambda S, B, r: (f'只有 `{len(S.mx)}` 种 x 值，选不出三个互不相同的 → 返回 `-1`' if len(S.mx) < 3 else f'有 `{len(S.mx)}` 种 x 值，至少 3 种，可以选'),
        'return sum': lambda S, B, r: f'每组最大值 `{sorted(S.mx.values(), reverse=True)}`，取前 3 大 `{sorted(S.mx.values(), reverse=True)[:3]}`，和 =={r}==',
    },
    cards=dict(
        one_liner='相同 x 的 y 至多选一个：每组取最大，再取前三大',
        complexity='时间 `O(n log n)` 或 `O(n)`，空间 `O(n)`',
        problem=['选三个下标，对应的 `x` 两两不同，使 `y[i]+y[j]+y[k]` 最大',
                 '选不出就返回 `-1`',
                 '示例：`x=[1,2,1,3,2]`，`y=[5,3,4,6,2]` → `14`'],
        quote='把相同 x[i] 对应的 y[i] 放到同一组，每组至多选一个数。贪心地，每组选最大的。所有最大值取前 3 大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 相同的下标分在同一组，每组至多选一个',
              '每组选 `y` 最大的：`mx[a] = max(mx[a], b)`',
              '不足 3 组就 `-1`，否则 `nlargest(3, mx.values())` 求和'],
        summary=['时间 `O(n log n)`，用快速选择或堆维护前三大可到 `O(n)`；空间 `O(n)`',
                 '易错点：先判 `len(mx) < 3`，再求前三大',
                 '`nlargest` 底层用的是堆',
                 '同类思路：分组后每组取最值，再对各组最值做贪心'],
    ),
)
