NUMS = [3, -1, -4, 2, 4]


def _F(v):
    return '-∞' if v == float('-inf') else str(v)


def _P(v):
    return f'({v})' if v < 0 else str(v)


def _idx(S):
    x = S.get('x')
    if x is None or x not in NUMS:
        return None
    k = NUMS.index(x)
    # for 行刚取出 x、还没更新 DP 时，DP 只处理到 k-1
    return k if S.get('_line') != 7 else k - 1


def _sim(upto):
    mf, ms, ms_rng, a = 0, float('-inf'), None, 0
    nf, ns, ns_rng, b = 0, 0, None, 0
    for k in range(upto + 1):
        v = NUMS[k]
        if mf > 0:
            mf += v
        else:
            mf, a = v, k
        if mf > ms:
            ms, ms_rng = mf, (a, k)
        if nf < 0:
            nf += v
        else:
            nf, b = v, k
        if nf < ns:
            ns, ns_rng = nf, (b, k)
    return dict(cur_max=(a, upto), best_max=ms_rng, cur_min=(b, upto), best_min=ns_rng)


def _info(S):
    k = _idx(S)
    if k is None or k < 0:
        return None
    return _sim(k)


def _win(key, end):
    def f(S):
        d = _info(S)
        if not d or not d[key]:
            return None
        return d[key][end]
    return f


def _in(key, color):
    def f(S, i, v):
        d = _info(S)
        if d and d[key] and d[key][0] <= i <= d[key][1]:
            return color
        return None
    return f


def _outside(S, i, v):
    d = _info(S)
    if d and d['best_min']:
        a, b = d['best_min']
        return None if a <= i <= b else 'purple'
    return None


def _final(S):
    if S.get('_line') in (13, 14, 15):
        tot = sum(NUMS)
        return (f"情况一 `max_s = {S['max_s']}`；情况二 `sum − min_s = {tot} − ({S['min_s']}) = {tot - S['min_s']}`")
    return '`max_f/max_s`：最大子数组（非空）　`min_f/min_s`：最小子数组（可空）'


def _maxf(S, B, ret):
    if B.max_f > 0:
        return f'前面的和 `{B.max_f}` > 0，==接上==：`{B.max_f} + {_P(S.x)} = {S.max_f}`'
    return f'前面的和 `{B.max_f}` ≤ 0，不如==重新开始==：`max_f = {S.x}`'


def _minf(S, B, ret):
    if B.min_f < 0:
        return f'前面的和 `{B.min_f}` < 0，==接上==：`{B.min_f} + {_P(S.x)} = {S.min_f}`'
    return f'前面的和 `{B.min_f}` ≥ 0，==重新开始==：`min_f = {S.x}`'


CONFIG = dict(
    num=918, title='环形子数组的最大和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='正难则反 · 最大/最小子数组和',
    tags=['面试经典150'],
    code='''
class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        max_f = 0     # 计算最大子数组和的 DP 数组（空间优化成一个变量）
        max_s = -inf  # 最大子数组和，不能为空
        min_f = 0     # 计算最小子数组和的 DP 数组（空间优化成一个变量）
        min_s = 0     # 最小子数组和，可以为空（元素和为 0）
        for x in nums:
            # 53. 最大子数组和（空间优化写法）
            max_f = max(max_f, 0) + x
            max_s = max(max_s, max_f)
            min_f = min(min_f, 0) + x
            min_s = min(min_s, min_f)
        if max_s < 0:
            return max_s
        return max(max_s, sum(nums) - min_s)
''',
    call=f'Solution().maxSubarraySumCircular({NUMS})',
    expect=9,
    views=[
        dict(type='text', fn=_final, size=26),
        dict(type='array', var='nums', label='最大：框 = 以 x 结尾的 max_f 子数组，绿 = 目前的 max_s', cell=96, h=215,
             pointers={'nums.index(x)': 'blue'}, pointer_labels={'nums.index(x)': 'x'},
             window=(_win('cur_max', 0), _win('cur_max', 1)), window_color='green', color=_in('best_max', 'green')),
        dict(type='array', var='nums', label='最小：框 = 以 x 结尾的 min_f 子数组，红 = 目前的 min_s', cell=96, h=215,
             pointers={'nums.index(x)': 'blue'}, pointer_labels={'nums.index(x)': 'x'},
             window=(_win('cur_min', 0), _win('cur_min', 1)), window_color='red', color=_in('best_min', 'red')),
        dict(type='array', var='nums', label='情况二：去掉目前的 min_s 段，剩下首尾相连的部分（紫）', cell=96, h=150, index=False,
             color=_outside),
    ],
    watch=[('max_f', 'max_f', 'green'), ('max_s', 'max_s', 'green'), ('min_f', 'min_f', 'red'), ('min_s', 'min_s', 'red')],
    captions={
        'max_f = 0': '`max_f`：以当前元素结尾的==最大==子数组和（53 题 DP 的空间优化）',
        'max_s = -inf': '`max_s = -∞`：最大子数组和，==不能为空==',
        'min_f = 0': '`min_f`：以当前元素结尾的==最小==子数组和',
        'min_s = 0': '`min_s = 0`：最小子数组和，==可以为空==（空数组和为 0）',
        'for x in nums': lambda S, B, ret: (f'遍历到 `x = {S.x}`' if S.get('x') != B.get('x') or 'x' not in B else '遍历结束'),
        'max_f = max(max_f, 0) + x': _maxf,
        'max_s = max(max_s, max_f)': lambda S, B, ret: f"`max_s = max({_F(B.max_s)}, {S.max_f})` = =={S.max_s}==",
        'min_f = min(min_f, 0) + x': _minf,
        'min_s = min(min_s, min_f)': lambda S, B, ret: f'`min_s = min({B.min_s}, {S.min_f})` = =={S.min_s}==',
        'if max_s < 0': lambda S, B, ret: ('`max_s < 0`：全是负数，`sum − min_s` 对应==空数组==，不合法' if S.max_s < 0
                                           else f'`max_s = {S.max_s} ≥ 0` → 比较两种情况'),
        'return max_s': '只能返回 `max_s = {ret}`',
        'return max(max_s': lambda S, B, ret: f'`max({S.max_s}, {sum(S.nums)} − ({S.min_s}))` = =={ret}==：跨越首尾的 `[2,4,3]` 更大',
    },
    cards=dict(
        one_liner='正难则反：跨越首尾的子数组 = 总和 − 中间的最小子数组',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==环形==整数数组 `nums`（末尾和开头相连），求非空子数组的最大和',
                 '每个元素最多用一次',
                 '示例：`[5,-3,5]` → `10`（`[5,5]` 跨越首尾）；本视频：`[3,-1,-4,2,4]` → `9`'],
        before=[dict(heading='一张图：两种情况', lines=[
            '情况一：子数组==不跨越==首尾 → 就是 53 题的最大子数组和 `max_s`',
            '情况二：子数组==跨越==首尾 → 剩下的中间部分是连续的一段',
            '中间那段越小，两头越大 → 情况二 = `sum(nums) − min_s`',
            '特例：全是负数时 `min_s = sum`，相当于选了空数组 → 直接返回 `max_s`'])],
        quote='【图解】正难则反，一张图秒懂！如何计算 53. 最大子数组和，请看我的题解，下面代码修改自我题解中的空间优化版本。',
        quote_src='—— 灵茶山艾府题解（标题与正文）',
        idea=['一次遍历同时算 `max_f / max_s` 和 `min_f / min_s`',
              '`max_f = max(max_f, 0) + x`：前面的和是正的才接上，否则从 x 重新开始',
              '答案 `max(max_s, sum − min_s)`；`max_s < 0` 时直接返回 `max_s`'],
        result='`max_s = 6`（`[2,4]`），`sum − min_s = 4 − (−5) = 9`（`[2,4,3]` 跨越首尾）→ `9` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`max_s` 初始 `-∞`（不能为空），`min_s` 初始 `0`（可以为空）',
                 '易错：全负数时 `sum − min_s = 0` 是空数组，必须特判返回 `max_s`',
                 '变形：选两个不重叠子数组（洛谷 P2642 / P1121 环形版）'],
    ),
)
