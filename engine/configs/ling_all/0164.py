def _bk(S):
    b = S.get('buckets')
    if b is None:
        return '桶还没建'
    return '桶 [最小, 最大]：' + '  '.join(('空' if mn == float('inf') else f'[{mn},{mx}]') for mn, mx in b)


CONFIG = dict(
    num=164, title='最大间距', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='分桶 · 答案至少为 d', tags=[],
    code='''
class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        m = min(nums)
        M = max(nums)
        if M - m <= 1:
            return M - m

        n = len(nums)
        ans = d = (M - m + n - 2) // (n - 1)  # 答案至少是 d
        buckets = [[inf, -inf] for _ in range((M - m) // d + 1)]
        for x in nums:
            b = buckets[(x - m) // d]
            b[0] = min(b[0], x)  # 维护桶内元素的最小值和最大值
            b[1] = max(b[1], x)

        pre_max = inf
        for mn, mx in buckets:
            if mn != inf:  # 非空桶
                # 桶内最小值，减去上一个非空桶的最大值
                ans = max(ans, mn - pre_max)
                pre_max = mx
        return ans
''',
    call='Solution().maximumGap([3,6,9,1,15,12])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', h=190, color=lambda S, i, v: 'blue' if v == S.get('x') else None),
        dict(type='text', size=30, h=80, fn=lambda S: f"最小 m = {S['m']}，最大 M = {S['M']}，n = {S['n']}，桶宽 d = ==ceil(({S['M']}−{S['m']})/({S['n']}−1))== = =={S['d']}==" if 'd' in S else (f"最小 m = {S['m']}，最大 M = {S['M']}" if 'M' in S else '')),
        dict(type='text', size=30, h=90, fn=_bk),
        dict(type='text', size=30, h=80, fn=lambda S: f"x = {S['x']} → 桶下标 `({S['x']}−{S['m']})//{S['d']}` = =={(S['x']-S['m'])//S['d']}==" if 'x' in S and 'd' in S and S.get('_line') in (10, 11, 12, 13) else ''),
        dict(type='text', size=30, h=80, fn=lambda S: f"上一个非空桶最大值 pre_max = {S['pre_max']}" if 'pre_max' in S and S['pre_max'] != float('inf') else ''),
    ],
    watch=[('m', 'm'), ('M', 'M'), ('d', 'd', 'orange'), ('ans', 'ans', 'green'), ('pre_max', 'pre_max', 'pink')],
    captions={
        'm = min': '`m = {m}`：最小值',
        'M = max': '`M = {M}`：最大值',
        'if M - m <= 1': '`M - m = {M-m}`：<= 1 则直接返回差值，否则继续',
        'ans = d =': '把木棍 `M-m = {M-m}` 切成 `n-1 = {n-1}` 段，平均至少 ==`d = {d}`==，所以答案至少是 `d`',
        'buckets = [': '桶宽 `d = {d}`，共 `(M-m)//d + 1 = {len(buckets)}` 个桶，每个桶记 `[最小, 最大]`',
        'for x in nums': '依次放入 `x = {x}`',
        'b = buckets': '`x` 落到第 `(x-m)//d = {(x-m)//d}` 个桶',
        'b[0] = min': '维护桶内最小值：`{b[0]}`',
        'b[1] = max': '维护桶内最大值：`{b[1]}`（同桶两数之差 < d，不可能是答案）',
        'for mn, mx in buckets': '看桶 `[{mn}, {mx}]`',
        'if mn != inf': '`mn = {mn}`：{"非空桶" if mn != inf else "空桶，跳过"}',
        'ans = max(ans, mn - pre_max)': lambda S, B, r: (f'第一个非空桶：`pre_max = inf`，差是 −inf，不会更新答案，`ans = {S.ans}`' if S.pre_max == inf else f'相邻非空桶：`mn − pre_max = {S.mn} − {S.pre_max} = {S.mn - S.pre_max}`，`ans = {S.ans}`'),
        'pre_max = mx': '记下这个桶的最大值 `pre_max = {pre_max}`，留给下一个非空桶',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='最长小木棍至少是平均长度，分桶后只比相邻桶',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无序数组 `nums`，求排序后相邻元素的最大差，要求线性时间',
                 '示例：`[3,6,9,1]` → `3`',
                 '本视频：`[3,6,9,1,15,12]` → `3`'],
        quote='如果把两两之差小于 d 的数，分到同一组（桶）中，那么答案一定不会是同一个桶内的两数之差，而是不同的桶的两数之差！',
        quote_src='—— 灵茶山艾府题解',
        idea=['想象木棍 `[m, M]` 切 `n-2` 刀，==最长段 ≥ 平均长度==，上取整得 `d`',
              '相差 `< d` 的数放同一桶：桶内差不可能是答案',
              '每桶只记最小/最大值，答案 = 相邻非空桶 ==后桶最小 − 前桶最大== 的最大值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`M - m <= 1` 要先单独返回（含全部相等返回 0）',
                 '上取整写成 `(M-m+n-2)//(n-1)`；桶数 `(M-m)//d+1` 最多 n 个',
                 '`ans` 初始为 `d`，因为答案至少是 d'],
    ),
)
