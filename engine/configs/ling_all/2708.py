def _cand(S, B):
    if 'x' not in S or 'mn' not in B or S.get('_line') != 5:
        return '`mn`/`mx`：所选元素的最小 / 最大乘积'
    x, mn, mx = S['x'], B['mn'], B['mx']
    return (f'x = `{x}`；候选：不选 `mn`=`{mn}`、单独 `{x}`、`{mn}×{x}`=`{mn*x}`、`{mx}×{x}`=`{mx*x}`'
            f'  →  mn = =={min(mn, x, mn*x, mx*x)}==，mx = =={max(mx, x, mn*x, mx*x)}==')


CONFIG = dict(
    num=2708, title='一个小组的最大实力值', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 维护最小/最大乘积',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution:
    def maxStrength(self, nums: List[int]) -> int:
        mn = mx = nums[0]
        for x in nums[1:]:
            mn, mx = min(mn, x, mn * x, mx * x), \\
                     max(mx, x, mn * x, mx * x)
        return mx
''',
    skip=['max(mx, x'],
    call='Solution().maxStrength([3,-1,-5,2,5,-9])',
    expect=1350,
    views=[
        dict(type='array', var='nums', label='nums', h=190, cell=96,
             color=lambda S, i, v: 'blue' if 'x' in S and S['nums'].index(S['x']) == i else None,
             dim=lambda S, i, v: 'x' in S and i > S['nums'].index(S['x'])),
        dict(type='text', fn=_cand, size=26, h=110),
    ],
    watch=[('mn', 'mn', 'cyan'), ('mx', 'mx', 'green'), ('x', 'x', 'blue')],
    captions={
        'mn = mx = nums[0]': '第一个数必选：`mn = mx = {mn}`',
        'for x in nums[1:]': '依次看下一个数 `x`',
        'mn, mx = min': ('同时更新（用旧值算）：`mn = min({B.mn}, {x}, {B.mn*x}, {B.mx*x}) = {min(B.mn, x, B.mn*x, B.mx*x)}`，'
                          '`mx = max({B.mx}, {x}, {B.mn*x}, {B.mx*x}) = =={max(B.mx, x, B.mn*x, B.mx*x)}==`。'
                          '负负得正，==最小值也要带着=='),
        'return mx': '答案就是最大乘积 `mx = {mx}`',
    },
    cards=dict(
        one_liner='负负得正：同时维护最小乘积和最大乘积',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选一个非空子序列，使元素乘积最大',
                 '示例：`[3,-1,-5,2,5,-9]` → `1350`',
                 '`1 <= n <= 13`，`-9 <= nums[i] <= 9`'],
        quote='无论 x = nums[i] 是正是负还是零，mn 是以下四种情况的最小值：不选、x 单独一个数、mn·x、mx·x。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选或不选 `x`：不选则 `mn`、`mx` 不变',
              '选 `x`：正数乘最大、负数乘最小，所以两个值都要维护',
              '四个候选直接取 min / max，==不用判断正负==，两式同时计算'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`mn, mx` 要同时赋值，不能先改 `mn` 再用它算 `mx`',
                 '初始值 `mn = mx = nums[0]`，保证非空',
                 '思考题：改成子数组就是 152 题'],
    ),
)
