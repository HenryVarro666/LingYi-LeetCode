def _col(S, i, v):
    n = S.get('nums')
    if not n:
        return None
    m = len(n) // 2
    if i == m:
        return 'yellow'
    return 'red' if v == n[m] else None


def _txt(S):
    n = S.get('nums')
    if not n:
        return ''
    m = len(n) // 2
    return f"中间下标 `m = {m}`，`nums[{m}] = {n[m]}`，它在数组里出现 =={n.count(n[m])}== 次"


CONFIG = dict(
    num=3978, title='唯一中间元素', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='数中间元素出现次数', tags=[],
    code='''
class Solution:
    def isMiddleElementUnique(self, nums: list[int]) -> bool:
        return nums.count(nums[len(nums) // 2]) == 1
''',
    call='''Solution().isMiddleElementUnique([4, 2, 7, 2, 9, 6, 1])
Solution().isMiddleElementUnique([4, 2, 7, 5, 9, 6, 1])''',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='nums', label='nums（黄 = 中间元素，红 = 与它相同的值）', cell=90, color=_col, h=220),
        dict(type='text', fn=lambda S: '两个示例依次运行：第一个中间值 `2` 出现两次 → False；第二个只出现一次 → True', size=24),
    ],
    watch=[('len(nums) // 2', 'len(nums) // 2', 'yellow'), ('nums[m]', 'nums[len(nums) // 2]', 'blue'), ('次数', 'nums.count(nums[len(nums) // 2])', 'green')],
    captions={
        'return': lambda S, B, ret: (f"`nums.count({S.nums[len(S.nums)//2]}) = {S.nums.count(S.nums[len(S.nums)//2])}`，"
                                     + ('恰好是 1 → ==True==，中间元素是唯一的' if ret else '不是 1（中间元素自己算一次，还有别的位置也等于它）→ ==False==')),
    },
    cards=dict(
        one_liner='数一数中间元素出现几次，必须恰好是 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长度为奇数 `n` 的数组 `nums`，看==下标中间==的元素是否在数组里==恰好出现一次==',
                 '示例：`[1,2,3]` → `true`；`[1,2,2]` → `false`',
                 '本视频：`[4,2,7,2,9,6,1]` → `false`，`[4,2,7,5,9,6,1]` → `true`'],
        quote='统计 nums 中的 nums[m] 的出现次数，必须恰好为 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m = n // 2` 就是正中间的下标，`nums[m]` 自己一定算 1 次',
              '`nums.count(nums[m])` 数出现次数，等于 1 说明别处没有相同的值',
              '另一种写法：分别检查 `[0,m-1]` 和 `[m+1,n-1]` 都不含 `nums[m]`，可以中途跳出'],
        after=[dict(heading='另一种写法：提前退出', lines=[
            '`[0, m-1]` 和 `[m+1, n-1]` 两段都不能含有 `nums[m]`',
            '遍历时一旦发现相等，立刻返回 `False`，不必看完整个数组',
            '最坏仍是 `O(n)`，但平均更快'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`n` 是奇数，所以 `len(nums) // 2` 恰好是正中间',
                 '次数里已经包含中间元素自己，所以比较的是 `== 1` 而不是 `== 0`',
                 '灵神还给了「左右两段都不含 nums[m]」的写法，能提前退出'],
    ),
)
