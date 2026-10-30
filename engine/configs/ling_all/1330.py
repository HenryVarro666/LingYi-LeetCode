def _k(S):
    """当前 pairwise 的 (a, b) 在 nums 里的下标 k（示例里数字互不相同）"""
    if 'a' not in S or 'b' not in S:
        return None
    n = S['nums']
    for k in range(len(n) - 1):
        if n[k] == S['a'] and n[k + 1] == S['b']:
            return k
    return None


def _t(S):
    if 'a' not in S or 'mx' not in S:
        return ''
    m = S['mx']
    w = S['mn']
    if m == float('-inf') or w == float('inf'):
        return f"当前一对 `a={S['a']}, b={S['b']}`"
    return f"mx = 各对 min 的最大 = =={m}==　　mn = 各对 max 的最小 = =={w}==　　2×(mx−mn) = {2*(m-w)}"


CONFIG = dict(
    num=1330, title='翻转子数组得到最大的数组值', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='分类讨论 · 恒等式化简',
    tags=['灵神题单·数学算法', '灵神题单·贪心与思维', '难度分 2482'],
    code='''
class Solution:
    def maxValueAfterReverse(self, nums: List[int]) -> int:
        base = d = 0
        mx, mn = -inf, inf
        for a, b in pairwise(nums):
            base += abs(a - b)
            mx = max(mx, min(a, b))
            mn = min(mn, max(a, b))
            d = max(d, abs(nums[0] - b) - abs(a - b),  # i=0
                       abs(nums[-1] - a) - abs(a - b))  # j=n-1
        return base + max(d, 2 * (mx - mn))
''',
    call='Solution().maxValueAfterReverse([2,3,1,5,4])',
    expect=10,
    views=[
        dict(type='text', fn=_t, size=26, h=70),
        dict(type='array', var='nums', label='nums（框 = 当前相邻一对 a, b）',
             color=lambda S, i, v: ('yellow' if _k(S) is not None and i in (_k(S), _k(S) + 1) else None),
             h=320),
        dict(type='text', fn=lambda S: (f"边界翻转的收益：翻前缀 `|{S['nums'][0]}−{S['b']}|−|{S['a']}−{S['b']}|` = {abs(S['nums'][0]-S['b'])-abs(S['a']-S['b'])}；翻后缀 `|{S['nums'][-1]}−{S['a']}|−|{S['a']}−{S['b']}|` = {abs(S['nums'][-1]-S['a'])-abs(S['a']-S['b'])}" if 'a' in S and 'b' in S else ''), size=24, h=110),
    ],
    watch=[('base', 'base', 'blue'), ('d', 'd', 'orange'), ('mx', 'mx', 'cyan'), ('mn', 'mn', 'pink')],
    skip=['abs(nums[-1] - a) - abs(a - b))'],
    max_steps=60,
    captions={
        'base = d = 0': '`base` 是不翻转的数组值；`d` 是翻转带来的最大增量，初始 0（翻长为 1 的子数组什么也不变）',
        'mx, mn = -inf': '`mx` 记所有相邻对 `min(a,b)` 的最大值，`mn` 记 `max(a,b)` 的最小值',
        'for a, b in pairwise': lambda S, B, r: ('相邻对都看完了' if 'a' in B and B.a == S.a and B.b == S.b else f'看相邻一对 `a = {S.a}, b = {S.b}`'),
        'base += abs': '`base += |{a} − {b}|` → =={base}==',
        'mx = max': '`mx = max({B.mx}, min({a}, {b}))` = =={mx}==：这对的较小值能否刷新 mx',
        'mn = min': '`mn = min({B.mn}, max({a}, {b}))` = =={mn}==：这对的较大值能否刷新 mn',
        'd = max(d': '翻转端点在数组边界时：翻前缀得 `{abs(nums[0]-b)-abs(a-b)}`，翻后缀得 `{abs(nums[-1]-a)-abs(a-b)}`，`d` 取三者最大（看下方 d）',
        'return base': lambda S, B, r: f'中间翻转的增量 `2×(mx−mn) = 2×({S.mx}−{S.mn}) = {2*(S.mx-S.mn)}`，边界翻转 `d = {S.d}`，取大者加上 base：`{S.base} + {max(S.d, 2*(S.mx-S.mn))}` = =={r}=='
    },
    cards=dict(
        one_liner='24 种大小关系里，只有「两对分居左右」才会让数组值变大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组值 = 相邻差的绝对值之和；可以翻转一个子数组一次，求最大数组值',
                 '示例：`[2,3,1,5,4]` → 翻转 `[3,1,5]` 得 `[2,5,1,3,4]`，数组值 `10`'],
        quote='利用对称性，只需讨论其中 3 类……只有第 1 类的情况会影响 d 的最大值，为了最大化 d，在遍历 nums 的所有相邻元素 a,b 的同时，维护 min(a,b) 的最大值 mx，以及 max(a,b) 的最小值 mn。',
        quote_src='—— 灵茶山艾府题解',
        idea=['翻转 `nums[i..j]` 只改变两端：`d = |a−x| + |b−y| − |a−b| − |x−y|`',
              '用 `|a−b| = max − min` 分类，三类里只有 `max(a,b) ≤ min(x,y)` 时 `d = 2·min(x,y) − 2·max(a,b) > 0`',
              '所以要 `mx = max(min(a,b))`、`mn = min(max(a,b))`，`d = 2(mx−mn)`；翻到端点的情况单独枚举'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`mx ≤ mn` 时中间翻转无增量，靠 `d` 初值 0 兜住',
                 '翻前缀 / 后缀（i=0 或 j=n−1）要单独算，公式里没有 a 或 y',
                 '同类：1131 绝对值表达式的最大值、CF1898D'],
    ),
)
