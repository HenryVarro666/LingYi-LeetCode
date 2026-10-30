def _pairs(S):
    """贪心已经组成的装运：[(l, r), ...]，截至当前 i"""
    w, i = S['weight'], S['i']
    out, j = [], 1
    while j < i:
        if w[j - 1] > w[j]:
            out.append((j - 1, j))
            j += 2
        else:
            j += 1
    return out


def _col(S, i, v):
    if 'i' not in S:
        return None
    for l, r in _pairs(S):
        if l <= i <= r:
            return 'green'
    return None


CONFIG = dict(
    num=3638, title='平衡装运的最大数量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='划分型贪心 · 相邻逆序对',
    tags=['贪心算法', '思维题', '难度分 1463'],
    code='''
class Solution:
    def maxBalancedShipments(self, weight: List[int]) -> int:
        n = len(weight)
        ans = 0
        i = 1
        while i < n:
            if weight[i - 1] > weight[i]:
                ans += 1
                i += 2  # 下个子数组至少要有两个数
            else:
                i += 1
        return ans
''',
    call='Solution().maxBalancedShipments([2,5,1,4,3,7,6])',
    expect=3,
    views=[
        dict(type='array', var='weight', h=260, label='weight', pointers={'i': 'blue'},
             window=('i - 1', 'min(i, n - 1)'),
             color=_col),
        dict(type='text', h=110, fn=lambda S: (f"已组成装运：{' '.join('`[' + str(S['weight'][l]) + ', ' + str(S['weight'][r]) + ']`' for l, r in _pairs(S)) or '（还没有）'}  共 ==" + str(S.get('ans', 0)) + '==' if 'i' in S else '子数组至少两个数；两个相邻数左大右小就够了')),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'i = 1': '从 `i = 1` 开始，每次看相邻的一对 `weight[i-1]`、`weight[i]`',
        'while i < n': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`，继续' if S.i < S.n else f'`i = {S.i} ≥ n = {S.n}`：没有数可配对了 → 结束'),
        'if weight[i - 1]': lambda S, B, r: (f'`weight[{S.i-1}] = {S.weight[S.i-1]} > weight[{S.i}] = {S.weight[S.i]}` → 左大右小，这两个数就==能单独成一个装运=='
                                               if S.weight[S.i-1] > S.weight[S.i] else
                                               f'`{S.weight[S.i-1]} ≤ {S.weight[S.i]}` → 最后一个数不小于前一个，这一对成不了；右移一位'),
        'ans += 1': '立刻切下这两个数，`ans` → {ans}：装运越短，能切出的越多',
        'i += 2': '这两个数已经用掉了，下一个装运从 `{i-1}` 起，至少要再有两个数：`i` → {i}',
        'i += 1': '`i` → {i}，把 `weight[{i-1}]` 当作下一对的左端',
        'return ans': '一共切出 `{ans}` 个平衡装运',
    },
    cards=dict(
        one_liner='装运越短越好：只要相邻两数左大右小，立刻切下来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['装运 = 连续子数组；它==最后一个数严格小于最大值==时叫平衡装运',
                 '选若干个不重叠的平衡装运（可以有包裹不装运），求最多几个',
                 '示例：`[2,5,1,4,3]` → `2`；本视频：`[2,5,1,4,3,7,6]` → `3`'],
        quote='贪心地，子数组的元素个数越少，我们能得到的子数组的个数就越多。所以子数组只需包含这两个数，包含更多元素是没有意义的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['单个数的装运最大值就是最后一个数，不平衡 → 每个装运==至少两个数==',
              '只要 `weight[i-1] > weight[i]`，这两个数就是长为 2 的平衡装运',
              '第一个装运越靠左，留给右边的机会越多 → 从左到右，发现就切，`i += 2` 跳过'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`i += 2`：用过的两个数不能再用，下一个装运至少要两个数',
                 '没有配上的数可以不装运，题目允许，别强行划分整个数组',
                 '归类：划分型贪心，类似「尽量多的不重叠区间」'],
    ),
)
