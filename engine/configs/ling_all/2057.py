CONFIG = dict(
    num=2057, title='值相等的最小索引', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='一次遍历（Go 原文转写）', tags=[],
    code='''
class Solution:
    def smallestEqual(self, nums: List[int]) -> int:
        for i, num in enumerate(nums):
            if i % 10 == num:
                return i
        return -1
''',
    call='Solution().smallestEqual([4,3,5,7,4,5,6,9])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（蓝箭头 = 当前下标 i）', pointers={'i': 'blue'}, cell=96, h=260,
             color=lambda S, i, v: ('green' if 'i' in S and i == S['i'] and S['i'] % 10 == v else None)),
        dict(type='text', h=110, size=32,
             fn=lambda S: f"`i % 10 = {S['i'] % 10}`，`nums[i] = {S['num']}`" if 'i' in S and 'num' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('num', 'num')],
    captions={
        'for i, num': '取下标 `i = {i}`，值 `num = {num}`',
        'if i % 10 == num': '比较 `i % 10 = {i % 10}` 与 `num = {num}` → ' + '{"==相等==" if i % 10 == num else "不等，继续往后找"}',
        'return i': '第一个满足条件的下标就是最小的，直接返回 ==`{ret}`==',
        'return -1': '整个数组都没有满足的下标，返回 `-1`',
    },
    cards=dict(
        one_liner='从小到大扫下标，碰到的第一个就是最小的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最小的下标 `i`，使 `i mod 10 == nums[i]`，没有就返回 `-1`',
                 '示例：`[4,3,2,1]` → `2`',
                 '本视频：`[4,3,5,7,4,5,6,9]` → `4`'],
        quote='func smallestEqual(nums []int) int { for i, num := range nums { if i%10 == num { return i } } return -1 }',
        quote_src='—— 灵茶山艾府题解（Go）',
        idea=['下标按递增顺序遍历，==第一次命中就是最小下标==',
              '命中就立刻 `return`，不用扫完整个数组'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`range nums` → `enumerate(nums)`）',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：比较的是下标 `i % 10`，不是 `nums[i] % 10`',
                 '没找到才返回 `-1`，`return -1` 要放在循环外'],
    ),
)
