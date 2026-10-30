CONFIG = dict(
    num=2009, title='使数组连续的最少操作数', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序去重 + 定长窗口右端点枚举',
    tags=['二、不定长滑动窗口', '难度分 2084'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        nums = sorted(set(nums))  # 去重排序

        ans = left = 0
        for i, x in enumerate(nums):
            while nums[left] < x - n + 1:  # nums[left] 不在窗口中
                left += 1
            ans = max(ans, i - left + 1)
        return n - ans
''',
    call='Solution().minOperations([1,3,3,4,8,9,10])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"窗口 = [`{S['x']-S['n']+1}`, `{S['x']}`]（长度 n = {S['n']}），窗口内保留 ==`{S['i']-S['left']+1}`== 个点" if 'x' in S and 'left' in S else '')),
        dict(type='array', var='nums', pointers={'left': 'blue', 'i': 'pink'}, window=('left', 'i'), h=300, label='nums（去重排序后）',
             dim=lambda S, i, v: 'left' in S and 'i' in S and not (S['left'] <= i <= S['i'])),
    ],
    watch=['n', ('left', 'left', 'blue'), ('i', 'i', 'pink'), 'x', ('ans', 'ans', 'green')],
    captions={
        'nums = sorted': '正难则反：改最少 = 保留最多。顺序无所谓，==去重排序==后变成数轴上的点：`{nums}`',
        'while nums[left]': '`nums[left] = {nums[left]}` 与窗口左边界 `x - n + 1 = {x - n + 1}` 比：{"在窗口外，左端点右移" if nums[left] < x - n + 1 else "在窗口内，窗口左端点不用动"}',
        'left += 1': '`{nums[left-1]}` 掉出窗口，`left` → {left}',
        'ans = max': '窗口内点数 `i - left + 1 = {i - left + 1}`，`ans = max({B.ans}, {i - left + 1}) = {ans}`',
        'return n': '保留最多 `{ans}` 个，其余都要改：`n - ans = {n} - {ans}` = =={n - ans}==，即为答案',
    },
    cards=dict(
        one_liner='正难则反：最多保留几个，其余全改',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['一次操作可把任意元素改成任意整数',
                 '连续 = ==元素互不相同，且最大 − 最小 = n − 1==',
                 '求使数组连续的最少操作次数。示例：`[1,3,3,4,8,9,10]` → `3`'],
        quote='把 a[i] 画在数轴上……相当于有一个长度为 n 的滑动窗口，窗口内的点保留不变，窗口外的点需要改变，填在窗口内的空位上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序去重后，问题变成：长度为 n 的窗口最多罩住几个点',
              '定理：只需枚举 ==a[i] 作为窗口右端点==，窗口右端无点时滑动不会多罩点',
              '`left` 只右移，满足 `a[left] ≥ a[i] − n + 1`，答案 `n − 最大点数`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(n)`（原地去重可到 `O(1)`）',
                 '易错：==必须先去重==，重复元素至多保留一个',
                 '窗口左边界是 `x - n + 1`，别漏掉 +1',
                 '同类题：1040 移动石子直到连续 II'],
    ),
)
