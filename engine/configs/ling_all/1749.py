NUMS = [2, -5, 1, -4, 3, -2]


def _k(S):
    """当前枚举到的下标（NUMS 元素互不相同，用 index 反查）"""
    if 'x' not in S:
        return None
    return S['nums'].index(S['x'])


def _series(S, sign):
    """辅助观察：把 f_max / f_min 在每个下标的值算出来（代码里只有两个变量，没有这个数组）"""
    nums = S['nums']
    k = _k(S)
    out = [None] * len(nums)
    if k is None:
        return out
    f = 0
    line = S['_line']
    for i, x in enumerate(nums[:k + 1]):
        f = (max(f, 0) if sign > 0 else min(f, 0)) + x
        if i < k or line >= (5 if sign > 0 else 6):
            out[i] = f
    return out


def _fmax(S):
    return _series(S, 1)


def _fmin(S):
    return _series(S, -1)


def _p(v):
    return f'({v})' if v < 0 else str(v)


def _text(S, B):
    k = _k(S)
    if k is None:
        return '`f_max` / `f_min`：以当前数==结尾==的最大 / 最小子数组和'
    x, ln = S['x'], S['_line']
    if ln == 5:
        p = B['f_max']
        return f'`f_max = max({p}, 0) + {_p(x)} = {S["f_max"]}`：前面是负的就==丢掉==，重新从 `{x}` 开始' if p < 0 else f'`f_max = max({p}, 0) + {_p(x)} = {S["f_max"]}`：前面不亏，接着往后拼'
    if ln == 6:
        p = B['f_min']
        return f'`f_min = min({p}, 0) + {_p(x)} = {S["f_min"]}`：前面是正的就==丢掉==，重新开始' if p > 0 else f'`f_min = min({p}, 0) + {_p(x)} = {S["f_min"]}`：前面已经是负的，接着往后拼'
    if ln == 7:
        return f'`ans = max({B["ans"]}, {S["f_max"]}, {-S["f_min"]})` = =={S["ans"]}=='
    return f'枚举子数组的最后一个数 `x = {x}`（下标 {k}）'


CONFIG = dict(
    num=1749, title='任意子数组和的绝对值的最大值', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最大 / 最小子数组和 · 滚动 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1542'],
    code='''
class Solution:
    def maxAbsoluteSum(self, nums: List[int]) -> int:
        ans = f_max = f_min = 0
        for x in nums:
            f_max = max(f_max, 0) + x
            f_min = min(f_min, 0) + x
            ans = max(ans, f_max, -f_min)
        return ans
''',
    call=f'Solution().maxAbsoluteSum({NUMS})',
    expect=8,
    views=[
        dict(type='text', fn=_text, h=70, size=26),
        dict(type='array', var='nums', label='nums（蓝 = 当前枚举的 x，子数组的最后一个数）', cell=96,
             pointers={'nums.index(x)': 'blue'}, pointer_labels={'nums.index(x)': 'x'},
             color=lambda S, i, v: 'blue' if i == _k(S) else None, h=190),
        dict(type='array', var=_fmax, label='f_max：以 nums[i] 结尾的最大子数组和（辅助观察，代码里只有一个变量）', cell=96,
             color=lambda S, i, v: 'green' if v is not None and v > 0 and i == _k(S) else None, h=150),
        dict(type='array', var=_fmin, label='f_min：以 nums[i] 结尾的最小子数组和', cell=96,
             color=lambda S, i, v: 'pink' if v is not None and v < 0 and i == _k(S) else None, h=150),
    ],
    watch=[('x', 'x', 'blue'), ('f_max', 'f_max', 'green'), ('f_min', 'f_min', 'pink'), ('ans', 'ans', 'yellow')],
    captions={
        'ans = f_max = f_min = 0': '三个变量都从 `0` 开始：子数组==可以为空==，所以答案至少是 0',
        'for x in nums': lambda S, B, r: ('`nums` 枚举完了，退出循环' if B.get('x') == S.x and 'x' in B
                                          else f'枚举子数组的==最后一个数== `x = {S.x}`'),
        'f_max = max': lambda S, B, r: (f'`f_max = max({B.f_max}, 0) + {_p(S.x)} = {S.f_max}`：前面的和 `{B.f_max}` < 0，拼上去只会更小 → ==丢掉，重新开始==' if B.f_max < 0
                                         else f'`f_max = max({B.f_max}, 0) + {_p(S.x)} = {S.f_max}`：前面的和 `{B.f_max}` ≥ 0，==接着往后拼=='),
        'f_min = min': lambda S, B, r: (f'`f_min = min({B.f_min}, 0) + {_p(S.x)} = {S.f_min}`：前面的和 `{B.f_min}` > 0，拼上去只会更大 → ==丢掉，重新开始==' if B.f_min > 0
                                         else f'`f_min = min({B.f_min}, 0) + {_p(S.x)} = {S.f_min}`：前面的和 `{B.f_min}` ≤ 0，==接着往后拼=='),
        'ans = max(ans': lambda S, B, r: (f'`ans = max({B.ans}, f_max={S.f_max}, -f_min={-S.f_min}) = {S.ans}`：'
                                          + ('最小子数组和取相反数更大 → ==答案来自负的那边==' if -S.f_min > S.f_max and -S.f_min > B.ans
                                             else '最大子数组和更大，==答案更新==' if S.f_max > B.ans
                                             else '都没有超过旧答案，保持不变')),
        'return ans': '所有位置都枚举完，最大的绝对值是 `{ans}`',
    },
    cards=dict(
        one_liner='|和| 最大 = 最大子数组和 与 最小子数组和的相反数，取大者',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，求==和的绝对值==最大的子数组（可以为空）',
                 '返回这个最大的 `abs(子数组和)`',
                 '示例：`[2,-5,1,-4,3,-2]` → `8`（子数组 `[-5,1,-4]`）'],
        quote='如果 x < 0，那么 x 越小，-x 就越大，问题转化成最小子数组和。我们可以把最大子数组和与最小子数组和（的相反数）都算出来，二者取最大值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x ≥ 0` 时越大越好 → 53 题最大子数组和；`x < 0` 时越小越好 → 最小子数组和',
              '`f[i] = max(f[i-1], 0) + nums[i]`：前面为负就丢掉，否则拼上去',
              '最小子数组和同理，两个 DP 一起滚动，每步用 `f_max` 和 `-f_min` 更新答案'],
        result='最大子数组和 `3`，最小子数组和 `-8`（`[-5,1,-4]`）→ 答案 `8` ✓',
        after=[dict(heading='方法二：前缀和', lines=[
            '设前缀和 `s[0]=0`，子数组和 = `s[j] − s[i]`，绝对值 = `|s[j] − s[i]|`',
            '一堆数里相差最大的是==最大值和最小值== → 答案 `max(s) − min(s)`',
            '最大值在最小值右边是最大子数组和，在左边是最小子数组和的绝对值',
            '代码：`s = list(accumulate(nums, initial=0))`，`return max(s) - min(s)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：子数组可以为空，所以 `ans`、`f_max`、`f_min` 都从 `0` 开始',
                 '易错：`f_min` 是负数，更新答案要用 `-f_min`',
                 '方法二（前缀和）：`max(s) - min(s)`，注意 `s[0] = 0` 也要算进去',
                 '同类：53. 最大子数组和（只算 `f_max`）'],
    ),
)
