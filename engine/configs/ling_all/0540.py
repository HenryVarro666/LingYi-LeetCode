CONFIG = dict(
    num=540, title='有序数组中的单一元素', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分 · 只查偶数下标',
    tags=['灵神题单·二分算法'],
    code='''
class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        left, right = -1, len(nums) // 2
        while left + 1 < right:
            mid = (left + right) // 2
            if nums[mid * 2] != nums[mid * 2 + 1]:
                right = mid
            else:
                left = mid
        return nums[right * 2]
''',
    call='Solution().singleNonDuplicate([1,1,2,3,3,4,4,8,8])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（只检查偶数下标 2k）', h=330,
             pointers={'mid * 2': 'yellow'},
             color=lambda S, i, v: ('yellow' if 'mid' in S and i in (S['mid'] * 2, S['mid'] * 2 + 1) else 'green' if 'mid' not in S and False else None),
             dim=lambda S, i, v: 'left' in S and i % 2 == 0 and (i // 2 <= S['left']) and S['left'] >= 0),
        dict(type='text', h=70, fn=lambda S: (f"二分 `k`：开区间 ==({S['left']}, {S['right']})==，即下标 `{max(S['left'],0)*2}` ~ `{S['right']*2}`" if 'right' in S and 'left' in S else '')),
    ],
    watch=['left', 'right', 'mid'],
    captions={
        'left, right =': '二分 `k`（检查 `nums[2k]`）：开区间边界 `left = -1`，`right = n // 2 = {right}`。==`k = {right}` 即最后一个位置不用检查==',
        'while left + 1 < right': lambda S, B, r: f'`left + 1 = {S.left + 1} < right = {S.right}`，区间里还有没检查的 `k`' if S.left + 1 < S.right else f'`left + 1 = {S.left + 1} == right`：区间空了，`right` 就是第一个满足 `nums[2k] != nums[2k+1]` 的 `k`',
        'mid = (left': '取中间的 `k = {mid}`，检查下标 `{mid*2}` 和 `{mid*2+1}`',
        'if nums[mid * 2]': lambda S, B, r: (f'`nums[{S.mid*2}] = {S.nums[S.mid*2]}` != `nums[{S.mid*2+1}] = {S.nums[S.mid*2+1]}` → ==成立==：单一元素的下标 `<= {S.mid*2}`' if S.nums[S.mid*2] != S.nums[S.mid*2+1] else f'`nums[{S.mid*2}] = {S.nums[S.mid*2]}` == `nums[{S.mid*2+1}]` → 它俩成对，单一元素在它们右边（下标 `> {S.mid*2}`）'),
        'right = mid': '不等：答案在 `2k` 或更左，`right = {right}`',
        'left = mid': '相等：这一对在单一元素左边，`left = {left}`',
        'return nums[right': '`right = {right}`，答案在偶数下标 `{right*2}` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='单一元素一定在偶数下标，检查 nums[2k] 与 nums[2k+1] 是否相等',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['有序数组里每个数出现两次，只有一个数出现一次，找出它',
                 '要求 `O(log n)` 时间、`O(1)` 空间',
                 '示例：`[1,1,2,3,3,4,4,8,8]` → `2`'],
        quote='只出现一次的那个数，一定位于偶数下标上。这启发我们去检查偶数下标 2k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数组长度是奇数，成对的数相邻，所以单一元素左边全是整对，它落在偶数下标',
              '`nums[2k] == nums[2k+1]`：单一元素在右边；`!=`：在 `2k` 或左边',
              '随 `k` 变大，`!=` 越来越容易成立，有单调性 → 开区间二分 `k`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`right` 初始为 `n // 2`：`2k = n-1` 那个位置不用查，没找到就是它',
                 '库函数写法：`bisect_left(range(n//2), True, key=check)`',
                 '扩展：每个数出现 `m` 次，同样思路 `O(log(n/m))`，比 `nums[mid] != nums[mid^1]` 更快'],
    ),
)
