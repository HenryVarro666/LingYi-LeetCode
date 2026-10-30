CONFIG = dict(
    num=2592, title='最大化数组的伟大值', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='田忌赛马 · 排序 + 双指针',
    tags=['灵神题单', '难度分 1569'],
    code='''
class Solution:
    def maximizeGreatness(self, nums: List[int]) -> int:
        nums.sort()
        i = 0
        for x in nums:
            if x > nums[i]:
                i += 1
        return i
''',
    call='Solution().maximizeGreatness([1,3,5,2,1,3,1])',
    expect=4,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"已配对 ==`{S['i']}`== 个；当前最弱的未配对数 `nums[{S['i']}] = {S['nums'][S['i']]}`" + (f"，来挑战它的 `x = {S['x']}`" if 'x' in S else '')) if 'i' in S else '先排序：只在乎匹配关系，和下标无关'),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=300, label='nums（排序后）',
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None,
             dim=lambda S, i, v: False),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink')],
    captions={
        'nums.sort()': '从小到大排序：只在乎谁能压过谁，下标无关 → `{nums}`',
        'i = 0': '`i` 指向当前最弱、还没被压过的数，同时 `i` 就是已配对的个数',
        'for x in nums': '让每个 `x = {x}` 依次去挑战 `nums[i]`',
        'if x > nums[i]': lambda S, B, r: (f"`x = {S.x}` > `nums[{S.i}] = {S.nums[S.i]}` → ==成立==：x 刚好压过最弱的数，配对成功" if S.x > S.nums[S.i]
                                           else f"`x = {S.x}` ≤ `nums[{S.i}] = {S.nums[S.i]}` → 不成立：x 压不过它，跳过这个 x，留给更大的数"),
        'i += 1': '配对 +1，下一个最弱的数变成 `nums[{i}]`',
        'return i': '`i` 就是伟大值，返回 =={i}==',
    },
    cards=dict(
        one_liner='田忌赛马：用刚好大一点的数去压最小的数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['重排 `nums` 得到 `perm`，统计满足 `perm[i] > nums[i]` 的下标个数，求最大值',
                 '示例：`[1,3,5,2,1,3,1]` → `4`',
                 '因为只看「谁压过谁」，可以先排序再配对'],
        quote='`nums` 的最小值要与次小值匹配，这样后面的数字才能取匹配更大的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后：最小的数要参与匹配，否则更大的数更难匹配',
              '`i` 指着最弱的未配对数，`x` 遍历每个候选；`x > nums[i]` 就配对，`i` 右移',
              '示例排序后 `[1,1,1,2,3,3,5]`：三个 1 配 `2,3,3`，2 配 5，后面无法配对'],
        summary=['时间 `O(n log n)`，空间 `O(1)`，瓶颈在排序',
                 '`i` 既是指针也是答案：不用再单独计数',
                 '易错点：条件是严格大于 `>`，相等不算',
                 '另一种写法：不能配对的个数恰好是出现次数最大值，答案 `len(nums) - max(Counter(nums).values())`，`O(n)`'],
    ),
)
