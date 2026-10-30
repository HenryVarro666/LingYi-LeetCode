def _mn(S):
    m = S.get('mn')
    return m if isinstance(m, int) else None


def _col(S, i, v):
    if 'x' not in S:
        return None
    m = _mn(S)
    if v == S['x']:
        return 'blue'
    if m is not None and v <= S['x'] and v >= m and v - m <= S['k']:
        return 'green'
    return None


def _dim(S, i, v):
    return 'x' in S and v > S['x']


def _txt(S):
    if 'mn' not in S:
        return '先排序：只关心每组的最小值和最大值，与顺序无关'
    m = _mn(S)
    if m is None:
        return '还没有任何一段：`mn = -inf`'
    return f"当前段 [{m}, {m + S['k']}] 内的数都能归到同一组，已分 ==`{S['ans']}`== 段"


def _chk(S, B, ret):
    x, mn, k = S.x, S.mn, S.k
    m = '-inf' if mn == -float('inf') else mn
    if x - mn > k:
        return f"`x - mn = {x} - ({m}) > {k}` → x 放不进当前段，==必须分割=="
    return f"`x - mn = {x} - {m} = {x - mn} <= {k}` → x 属于当前段"


CONFIG = dict(
    num=2294, title='划分数组使最大差为 K', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 划分型贪心',
    tags=['贪心算法', '划分型贪心', '难度分 1416'],
    code='''
class Solution:
    def partitionArray(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = 0
        mn = -inf
        for x in nums:
            if x - mn > k:  # 必须分割
                ans += 1
                mn = x  # mn 是下一段的最小值
        return ans
''',
    call='Solution().partitionArray([3,6,1,2,5,9], 2)',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（蓝 = x，绿 = 当前段内的数，灰 = 还没处理）', cell=90, color=_col, dim=_dim, h=300),
        dict(type='text', fn=lambda S: '子序列只看最大/最小值 ⇒ 排序后每组是一段连续子数组', size=24),
    ],
    watch=[('x', 'x', 'blue'), ('mn', 'mn', 'cyan'), ('k', 'k'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '先排序：组的最大值、最小值与顺序无关，排序后==同组的数是连续的一段==',
        'ans = 0': '`ans` 是已经开出的段数',
        'mn = -inf': '`mn` 是当前段的最小值；初始 `-inf`，保证第一个数一定开新段',
        'for x in nums': lambda S, B, r: ('从小到大取下一个数 `x = %s`' % S.x if 'x' not in B or S.x != B.x else '遍历结束，没有更多的数'),
        'if x - mn > k': _chk,
        'ans += 1': '开一个新段：`ans` → =={ans}==',
        'mn = x': '`x = {x}` 是新段的最小值：`mn` → =={mn}==，后面 `<= {mn + k}` 的数都归它',
        'return ans': '共分出 =={ans}== 段',
    },
    cards=dict(
        one_liner='排序后，每组是连续的一段，从最小值开始往右吞',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['把数组分成若干子序列，每个子序列最大值减最小值 `<= k`，求最少几个',
                 '示例：`[3,6,1,2,5], k=2` → `2`',
                 '本视频：`[3,6,1,2,5,9], k=2` → `3`'],
        quote='我们只关心子序列的最大值和最小值，这与子序列的元素顺序无关。为方便计算，先把 nums 从小到大排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，与最小值相差 `<= k` 的数是==连续的一段==',
              '问题变成：分割成若干段，每段首尾之差 `<= k`，最少几段',
              '记录当前段最小值 `mn`，`x - mn > k` 就开新段'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '`mn` 初始化为 `-inf` 而不是 `nums[0]`，空数组也正确',
                 '开新段时别忘了 `mn = x`',
                 '同类：划分型贪心，如 2405、2358、2522'],
    ),
)
