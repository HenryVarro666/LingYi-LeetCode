CONFIG = dict(
    num=2453, title='摧毁一系列目标', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='按余数分组 · 取最大组的最小值',
    tags=['灵神题单', '数学算法', '难度分 1762'],
    code='''
class Solution:
    def destroyTargets(self, nums: List[int], space: int) -> int:
        g = defaultdict(list)
        for x in nums:
            g[x % space].append(x)
        mx = ans = 0
        for a in g.values():
            m, low = len(a), min(a)
            if m > mx or m == mx and low < ans:
                mx, ans = m, low
        return ans
''',
    call='Solution().destroyTargets([6,2,5,3,4,1], 3)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（space = 3）', pointers={}, h=170),
        dict(type='map', var='g', label='g：余数 → 同余的数', fmt=lambda k, v: f'{k}: {v}', h=200, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"目前最大组：大小 ==%d==，最小值 ==%d==" % (S['mx'], S['ans'])) if 'mx' in S else '同余的数，可以被其中最小的数一次摧毁'),
    ],
    watch=['x', ('mx', 'mx', 'orange'), ('ans', 'ans', 'green'), 'm', 'low'],
    captions={
        'g = defaultdict': '`g` 按 `x % space` 分组：余数相同的数放进同一组',
        'g[x % space].append': '`{x}` 的余数是 `{x % space}` → 放进第 {x % space} 组：`{g[x % space]}`',
        'mx = ans = 0': '`mx` 记最大组的大小，`ans` 记那一组的最小值',
        'for a in g.values()': '逐个看每一组',
        'm, low = len(a), min(a)': '这一组有 `{m}` 个数，输入其中最小的 `{low}` 就能全部摧毁',
        'if m > mx': lambda S, B, r: (f'`{S.m} > {S.mx}`：这一组更大 → 更新' if S.m > S.mx else
            (f'大小相同（{S.m}），最小值 `{S.low} < {S.ans}` → 取更小的，更新' if S.m == S.mx and S.low < S.ans
             else f'`m = {S.m}`，不比目前的 `mx = {S.mx}` 更优（或相同但最小值不更小）→ 不更新')),
        'mx, ans = m, low': '更新：`mx = {mx}`，`ans = {ans}`',
        'return ans': '摧毁最多的那一组里最小的数：`{ans}`',
    },
    cards=dict(
        one_liner='模 space 相同的数，被其中最小的那个一起摧毁',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['输入 `nums[i]` 会摧毁所有 `nums[i] + c*space` 位置的目标（c ≥ 0）',
                 '求摧毁数目最多时，输入值 `nums[i]` 的==最小值==',
                 '示例：`nums=[3,7,8,1,1,5], space=2` → `1`；本视频：`[6,2,5,3,4,1], space=3` → `1`'],
        quote='根据题意，模 space 相同的数是可以被这些数中最小的那个数摧毁的。……因此按模 space 的结果分组，最大组的最小值就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个数 `x` 只能摧毁比它大且同余的数，所以输入组内最小的最划算',
              '问题变成：找元素最多的余数组，并列时取最小值更小的那组',
              '比较条件 `m > mx or m == mx and low < ans` 一次处理两种情况'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：并列时要比较最小值，不能只比大小',
                 '余数分组是同余题的常见套路'],
    ),
)
