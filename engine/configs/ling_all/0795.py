CONFIG = dict(
    num=795, title='区间子数组个数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举右端点 · 三指针', tags=['三指针', '难度分 1817'],
    code='''
class Solution:
    def numSubarrayBoundedMax(self, nums: List[int], left: int, right: int) -> int:
        ans, i0, i1 = 0, -1, -1
        for i, x in enumerate(nums):
            if x > right: i0 = i
            if x >= left: i1 = i
            ans += i1 - i0
        return ans
''',
    call='Solution().numSubarrayBoundedMax([2,9,2,5,6], 2, 8)',
    expect=7,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"以 `i={S['i']}` 结尾：左端点可选 `[{S['i0'] + 1}, {S['i1']}]`，共 =={S['i1'] - S['i0']}== 个" if 'i' in S and S['_line'] >= 7 else f"范围 `[{S['left']}, {S['right']}]`：先更新 i0、i1，再数左端点")),
        dict(type='array', var='nums', h=300, pointers={'i': 'green', 'i0': 'pink', 'i1': 'blue'},
             window=('i0 + 1', 'i1'),
             color=lambda S, idx, v: ('pink' if v > S['right'] else 'blue' if v >= S['left'] else None) if 'right' in S else None,
             dim=lambda S, idx, v: 'i' in S and idx > S['i']),
    ],
    watch=[('i', 'i', 'green'), ('i0', 'i0', 'pink'), ('i1', 'i1', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans, i0, i1 = 0': '`i0`：最近一个==不能包含==的下标，`i1`：最近一个==可以做最大值==的下标，都先设为 -1',
        'for i, x in enumerate': '枚举子数组右端点 `i = {i}`，`x = {x}`',
        'if x > right': lambda S, B, r: (f'`{S.x} > {S.right}`：太大，任何包含它的子数组都不合法 → `i0 = {S.i}`' if S.x > S.right else f'`{S.x} <= {S.right}`：没超上界，`i0` 不变，仍是 {S.i0}'),
        'if x >= left': lambda S, B, r: (f'`{S.x} >= {S.left}`：它能当最大值 → `i1 = {S.i}`（即使 > right 也更新，保证 i1 >= i0）' if S.x >= S.left else f'`{S.x} < {S.left}`：太小，自己不能当最大值，`i1` 不变，仍是 {S.i1}'),
        'ans += i1 - i0': '左端点 `i0+1 … i1` 都合法：`i1 - i0 = {i1} - ({i0}) = {i1 - i0}` 个 → `ans` = =={ans}==',
        'return ans': '共 `{ans}` 个子数组',
    },
    cards=dict(
        one_liner='枚举右端点，数左端点：区间 [i0+1, i1] 里的都合法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `nums` 和范围 `[left, right]`，数最大值落在范围内的非空连续子数组',
                 '示例：`[2,9,2,5,6]`，`left=2, right=8` → `7`'],
        quote='上一个不能包含的下标为 i0，等价于上一个可以包含的下标为 i0+1，这是子数组左端点的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x > right`：右端点跨不过它，`i0` 更新为 i',
              '`x >= left`：最近的能当最大值的位置 `i1`',
              '左端点取 `i0+1 … i1`，右端点是 i，共 `i1 - i0` 个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`x >= left` 就更新 i1（包括 > right），这样 `i1 >= i0`，不会算出负数',
                 '`i1 - i0` 等价于左端点区间 `[i0+1, i1]` 的长度',
                 '相似题：2444 统计定界子数组的数目'],
    ),
)
