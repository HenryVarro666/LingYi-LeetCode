def _chain(S):
    if 'nums1' in S and 'v' in S and S.get('_inner', {}).get('nums') is not None:
        pass
    return S.get('nums') or []


def _fgh(S):
    f, g, h = S.get('f'), S.get('g'), S.get('h')
    if f is None or g is None or h is None or not isinstance(f, list):
        return [[]]
    return [['-' if x is None else x for x in row] for row in (f, g, h)]


def _cur(S):
    nums, v = S.get('nums'), S.get('v')
    if nums is None or v is None or 'f' not in S:
        return None
    return None


CONFIG = dict(
    num=3743, title='循环划分的最大得分', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='断环 + 配对最值（买卖 k 次股票）',
    tags=['难度分 3125'],
    code='''
class Solution(object):
    def maximumScore(self, nums, k):
        
        p = 0
        n = len(nums)
        for index in range(1, n):
            if nums[index] < nums[p]:
                p = index
        
        def calc(nums):
            f = [None] * (k + 1)
            g = [None] * (k + 1)
            h = [None] * (k + 1)
            f[0] = 0
            for v in nums:
                for t in range(k, -1, -1):
                    if f[t] is not None:
                        if g[t] is None or g[t] < f[t] - v:
                            g[t] = f[t] - v
                        if h[t] is None or h[t] < f[t] + v:
                            h[t] = f[t] + v

                    if t > 0 and g[t - 1] is not None and (f[t] is None or f[t] < g[t - 1] + v):
                        f[t] = g[t - 1] + v
                    if t > 0 and h[t - 1] is not None and (f[t] is None or f[t] < h[t - 1] - v):
                        f[t] = h[t - 1] - v
            
            return max(f)

        nums1 = nums[p:] + nums[:p]
        nums2 = nums[p + 1:] + nums[:p + 1]
        return max(calc(nums1), calc(nums2))
''',
    call='Solution().maximumScore([2, 5, 1], 1)',
    expect=4,
    skip=['f = [None]', 'g = [None]', 'h = [None]', 'f[0] = 0', 'for t in range', 'for v in nums'],
    max_steps=50,
    views=[
        dict(type='array', var=lambda S: S['nums'] if 'f' in S and 'nums' in S else (S['nums'] if 'nums' in S else []),
             label='nums（calc 里是断环后的链，蓝 = 当前元素 v）', h=170, cell=90,
             color=lambda S, i, v: 'blue' if ('f' in S and 'v' in S and S.get('v') == v and i == S['nums'].index(v)) else None),
        dict(type='table', var=_fgh, label='f 空闲 / g 已选最小 / h 已选最大；列 = 划分次数 t（- 为空）',
             h=260, cell=110, rows=['f', 'g', 'h'], cols=lambda S: [f't={t}' for t in range(len(S['f']))] if 'f' in S and isinstance(S['f'], list) else []),
    ],
    watch=[('p', 'p', 'orange'), ('v', 'v', 'blue'), ('t', 't', 'pink'), ('k', 'k', 'purple')],
    captions={
        'if nums[index] < nums[p]': '找最小值的下标：`nums[{index}] = {nums[index]}` 对 `nums[p] = {nums[p]}`',
        'p = index': '更新最小值下标 `p = {p}`',
        'nums1 = ': '在最小值 `nums[p]` 左边断开：它成为链的第一个元素，环变成直链',
        'nums2 = ': '在最小值右边断开：它成为链的最后一个元素',
        'if f[t] is not None': '`f[{t}]` 非空才能开启新的一段；空则这个状态不可达',
        'g[t] = f[t] - v': '选 `{v}` 当这一段的最小值（先扣掉）：`g[{t}] = {g[t]}`',
        'h[t] = f[t] + v': '选 `{v}` 当这一段的最大值（先加上）：`h[{t}] = {h[t]}`',
        'f[t] = g[t - 1] + v': '`{v}` 做最大值，补上前面扣掉的最小值，完成第 {t} 次划分：`f[{t}] = {f[t]}`',
        'f[t] = h[t - 1] - v': '`{v}` 做最小值，扣掉它，完成第 {t} 次划分：`f[{t}] = {f[t]}`',
        'return max(f)': '取各划分次数里的最大值：`{ret}`',
        'return max(calc': '两条链各跑一遍 `calc`，取较大值（先算 nums1，再算 nums2）',
        'if t > 0 and g[t - 1]': '用 `g[{t}-1]`（已选最小）+ `{v}` 当最大值，能不能让 `f[{t}]` 更优',
        'if t > 0 and h[t - 1]': '用 `h[{t}-1]`（已选最大）− `{v}` 当最小值，能不能让 `f[{t}]` 更优',
    },
    cards=dict(
        one_liner='断开最小值，化成可做多做空的 k 次股票问题',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['循环数组 `nums`，最多划分 `k` 个子数组（可环绕）',
                 '子数组得分 = 最大值 − 最小值，求总得分最大',
                 '本视频：`[2,5,1]`，`k=1` → `4`'],
        quote='对于nums中的最小值，不妨设其下标为index，那么与其有关的划分要么让nums[index]作为划分的左边界，要么让nums[index]作为划分的右边界，也就是说让nums在index这个位置断开必然可以达成最优解。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素 DP 要枚举断点，`O(n^2 k)` 太慢 → 改从最值入手',
              '多余元素可以并入相邻子数组，所以只需要挑出 `k` 对最大值 / 最小值',
              '这就是可做多可做空、最多交易 k 次的股票题：`f` 空闲，`g` 选了最小，`h` 选了最大'],
        summary=['时间 `O(nk)`，空间 `O(k)`（`t` 倒序省掉 index 一维）',
                 '作者以最小值断环，要试断在它左边和右边两种',
                 '`f/g/h` 用 `None` 表示不可达，比较前先判空',
                 '答案是 `max(f)`：划分次数不超过 `k` 即可',
                 '对比灵神：灵神以最大值断环，且直接套 3573 的模板'],
    ),
)
