CONFIG = dict(
    num=3584, title='子序列首尾元素的最大乘积', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 最小/最大值',
    tags=['灵神题单', '难度分 1763'],
    code='''
class Solution:
    def maximumProduct(self, nums: List[int], m: int) -> int:
        ans = mx = -inf
        mn = inf
        for i in range(m - 1, len(nums)):
            # 维护左边 [0,i-m+1] 中的最小值和最大值
            y = nums[i - m + 1]
            mn = min(mn, y)
            mx = max(mx, y)
            # 枚举右
            x = nums[i]
            ans = max(ans, x * mn, x * mx)
        return ans
''',
    call='Solution().maximumProduct([2,-1,2,-6,5,2,-5,7], 2)',
    expect=35,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 右端 x，黄 = 刚并入的 y，其余 [0, i−m+1] 是左边候选）', h=230, cell=96,
             pointers={'i': 'blue'},
             dim=lambda S, i, v: 'i' in S and i > S['i'] - S['m'] + 1 and i != S['i'],
             color=lambda S, i, v: ('blue' if S.get('i') == i else 'yellow' if 'i' in S and i == S['i'] - S['m'] + 1 else None)),
        dict(type='text', size=28, h=130,
             fn=lambda S: (f"左边：最小 `mn = {S['mn']}`，最大 `mx = {S['mx']}`；`x = {S['nums'][S['i']]}`：`x·mn` = {S['nums'][S['i']] * S['mn']}，`x·mx` = {S['nums'][S['i']] * S['mx']}"
                           if 'i' in S and S['mn'] != float('inf') and S['mx'] != -float('inf') else '乘积最大：正数配最大值，负数配最小值（负负得正）')),
    ],
    watch=[('i', 'i', 'blue'), ('mn', 'mn', 'cyan'), ('mx', 'mx', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = mx = -inf': '`ans`、`mx` 初始化成 `-inf`：==答案可能是负数==，不能从 0 开始',
        'mn = inf': '`mn` 初始化成 `+inf`，左边一个数都没有',
        'for i in range': lambda S, B, r: (f'枚举右端 `i = {S.i}`：首尾至少相隔 `m − 1 = {S.m - 1}`，所以 i 从 `m − 1` 开始' if 'i' in S and ('i' not in B or S.i != B.i) else '遍历结束'),
        'y = nums[i - m + 1]': '`i − m + 1 = {i - m + 1}`：这个位置刚好能当起点，取 `y = {y}` 并入左边',
        'mn = min': '左边最小值 `mn = min({B.mn}, {y}) = {mn}`（负负得正要靠它）',
        'mx = max': '左边最大值 `mx = max({B.mx}, {y}) = {mx}`',
        'x = nums[i]': '右端 `x = nums[{i}] = {x}`',
        'ans = max(ans, x * mn': '`x·mn = {x * mn}`、`x·mx = {x * mx}`：==x 为正配最大，为负配最小==，`ans = max({B.ans}, …) = {ans}`',
        'return ans': '最大乘积 `{ans}`',
    },
    cards=dict(
        one_liner='首尾下标至少差 m − 1：枚举右端，左边维护最大最小值',
        complexity='时间 `O(n − m)`，空间 `O(1)`',
        problem=['在长为 `m` 的子序列里，求首尾元素乘积的最大值',
                 '长为 m 的子序列，首尾下标相差至少 `m − 1`',
                 '本视频：`nums=[2,-1,2,-6,5,2,-5,7]`，`m=2` → `35`（5 × 7）'],
        quote='题目意思是首尾元素下标相差至少是 m-1，这样子序列长度才能是 m。……维护 [0,i-m+1] 中的最小值和最大值。维护最小值是因为负负得正，答案可以来自两个负数相乘。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心首尾两个数：问题变成“下标相差 ≥ m−1 的两数之积的最大值”',
              '枚举右边的 `nums[i]`，左边的候选范围是 `[0, i−m+1]`',
              '乘积最大：只有左边的最大值或最小值可能最优'],
        summary=['时间 `O(n − m)`，空间 `O(1)`',
                 '易错：`ans` 要初始化成 `-inf`，答案可能为负',
                 '`m = 1` 不用特判：自己乘自己，最大或最小值会被枚举到',
                 '同类题：枚举右，维护左（1014、2905）'],
    ),
)
