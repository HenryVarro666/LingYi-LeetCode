CONFIG = dict(
    num=3708, title='最长斐波那契子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='一次遍历 · 分组循环',
    tags=['分组循环', '难度分 1381'],
    code='''
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 2
        start = 0
        for i in range(2, n):
            if nums[i] != nums[i - 1] + nums[i - 2]:
                ans = max(ans, i - start)  # [start,i-1] 是斐波那契子数组
                start = i - 1
        return max(ans, n - start)  # [start,n-1] 是斐波那契子数组
''',
    call='Solution().longestSubarray([1,1,2,3,5,1,6,7,13,20])',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"检查 `nums[{S['i']}] = {S['nums'][S['i']]}` 是否等于 `{S['nums'][S['i']-1]} + {S['nums'][S['i']-2]}` = =={S['nums'][S['i']-1]+S['nums'][S['i']-2]}==") if 'i' in S and isinstance(S['i'], int) and S['i'] >= 2 else '', size=30),
        dict(type='array', var='nums', pointers={'start': 'blue', 'i': 'pink'},
             window=(lambda S: S['start'], lambda S: S['i'] - 1 if S['i'] > S['start'] else S['start']), h=300, cell=90,
             dim=lambda S, k, v: 'start' in S and k < S['start']),
    ],
    watch=[('start', 'start', 'blue'), ('i', 'i', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 2': '长度 1、2 的子数组一定合法，所以答案起码是 ==2==',
        'start = 0': '`start` 记录当前斐波那契段的起点',
        'if nums[i] !=': lambda S, B, r: (f"`nums[{S.i}] = {S.nums[S.i]}`，前两项之和 `{S.nums[S.i-1] + S.nums[S.i-2]}` → 不相等，这一段到 `{S.i-1}` 为止"
                                          if S.nums[S.i] != S.nums[S.i-1] + S.nums[S.i-2]
                                          else f"`nums[{S.i}] = {S.nums[S.i-1]} + {S.nums[S.i-2]}` 成立 → 段继续延长，什么都不用做"),
        'ans = max(ans, i - start)': '段 `[{start}, {i-1}]` 长度 `{i - start}`，`ans = max({B.ans}, {i - start}) = {ans}`',
        'start = i - 1': '==下一段从 `i-1` 开始==：最后一个数可能是新段的第一个数，`start` → {start}',
        'return': '收尾：最后一段 `[{start}, {n-1}]` 没被循环结算，`max({ans}, {n - start}) = {ret}`',
    },
    cards=dict(
        one_liner='一次遍历：断了就从前一个数重新开段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['斐波那契数组：第 3 项起每项等于前两项之和',
                 '求 `nums` 里最长的斐波那契==连续==子数组，长度 1、2 总是合法',
                 '示例：`[1,1,2,3,5,1,6,7,13,20]` → `6`'],
        quote='斐波那契子数组的最后一个数，可能是下一个斐波那契子数组的第一个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从 `nums[0]` 找到 `[1,1,2,3,5]` 后，从下标 1 开始只会得到更短的段，不必再试',
              '所以断点处直接令 `start = i - 1`，==共用断点前的那个数==',
              '循环结束还要结算最后一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：断开后新段起点是 `i-1`，不是 `i`',
                 '易错：循环外要再结算最后一段，`ans` 初值为 2',
                 '方法一是枚举左端点、暴力向右延伸，复杂度 `O(n log U)`',
                 '变形：873 题改成子序列'],
    ),
)
