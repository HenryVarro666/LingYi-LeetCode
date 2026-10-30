CONFIG = dict(
    num=1144, title='递减元素使数组呈锯齿状', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='分奇偶两遍扫描',
    tags=['灵神题单', '贪心与思维', '难度分 1559'],
    code='''
class Solution(object):
    def movesToMakeZigzag(self, nums):

        n = len(nums)
        p1 = 0
        for index in range(0, n, 2):
            left = right = 0
            if index > 0 and nums[index] >= nums[index - 1]:
                left = nums[index] - nums[index - 1] + 1
            if index < n - 1 and nums[index] >= nums[index + 1]:
                right = nums[index] - nums[index + 1] + 1
            p1 += max(left, right)

        p2 = 0
        for index in range(1, n, 2):
            left = right = 0
            if index > 0 and nums[index] >= nums[index - 1]:
                left = nums[index] - nums[index - 1] + 1
            if index < n - 1 and nums[index] >= nums[index + 1]:
                right = nums[index] - nums[index + 1] + 1
            p2 += max(left, right)

        return min(p1, p2)
''',
    call='Solution().movesToMakeZigzag([9,6,1,6,2])',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"下标 `{S['index']}`（{'p2' if 'p2' in S else 'p1'} 这一轮）：向左要减 `{S['left']}`，向右要减 `{S['right']}` → 取大的" if 'index' in S and 'left' in S else '')),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=220,
             color=lambda S, i, v: ('yellow' if i == S.get('index') else None) if 'index' in S else None,
             dim=lambda S, i, v: 'index' in S and i % 2 != S['index'] % 2),
    ],
    watch=['index', 'left', 'right', ('p1', 'p1', 'green'), ('p2', 'p2', 'cyan')],
    captions={
        'p1 = 0': '`p1`：偶数下标当“低谷”（要减的）时的总操作数',
        'p2 = 0': '`p2`：奇数下标当“低谷”时的总操作数',
        'left = right = 0': '先假设左右都不用减',
        'if index > 0': lambda S, B, r: ('没有左邻居，左边不用减' if S.index == 0 else (f'`nums[{S.index}] = {S.nums[S.index]}` ≥ 左邻 `{S.nums[S.index-1]}`，成立：必须减到比左邻小' if S.nums[S.index] >= S.nums[S.index-1] else f'`nums[{S.index}] = {S.nums[S.index]}` < 左邻 `{S.nums[S.index-1]}`：已经比左邻小，左边不用减')),
        'if index < n - 1': lambda S, B, r: ('没有右邻居，右边不用减' if S.index == S.n - 1 else (f'`nums[{S.index}] = {S.nums[S.index]}` ≥ 右邻 `{S.nums[S.index+1]}`，成立：必须减到比右邻小' if S.nums[S.index] >= S.nums[S.index+1] else f'`nums[{S.index}] = {S.nums[S.index]}` < 右邻 `{S.nums[S.index+1]}`：已经比右邻小，右边不用减')),
        'left = nums[index]': '需减 `{nums[index]} − {nums[index-1]} + 1` = `{left}`（减到刚好比左邻小 1）',
        'right = nums[index]': '需减 `{nums[index]} − {nums[index+1]} + 1` = `{right}`（减到刚好比右邻小 1）',
        'p1 += max': '左右都要满足，取较大的：`max({left}, {right})` → `p1 = {p1}`',
        'p2 += max': '左右都要满足，取较大的：`max({left}, {right})` → `p2 = {p2}`',
        'return min': '两种形态取少的：`min({p1}, {p2}) = {ret}`',
    },
    cards=dict(
        one_liner='两种形态只差奇偶：各扫一遍，只减“低谷”位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可把一个元素减 1，使数组呈锯齿状',
                 '要么偶数下标比邻居大，要么奇数下标比邻居大',
                 '示例：`[9,6,1,6,2]` → `4`'],
        quote='只能使用递减操作，因此对于这种情况，偶数下标的A[0]、A[2]、A[4]、...等我们都不应该对其进行操作，而对于奇数下标的A[1]、A[3]、A[5]、...这些，我们就可以通过判断其与两侧偶数下标的数的大小来进行操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定一种形态：峰不动，谷 `A[index]` 要小于两侧',
              '左边 `≥` 就要减 `A[index] − A[index−1] + 1`，右边同理',
              '左右都要满足 → 取 `max`；奇偶互换再算一遍，取小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`p1` 扫偶数下标，`p2` 扫奇数下标，最后 `min`',
                 '易错点：要 `+1`（严格小于）；边界没有邻居就不算',
                 '原文为 Python 2 写法，无需改动代码',
                 '对比灵神：灵神用一个 `s[i % 2]` 一趟搞定，这里分两个循环'],
    ),
)
