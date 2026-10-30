def _text(S):
    if 'median' not in S:
        if 'nums' in S and S['nums'] != sorted(S['nums']):
            return '先排序，再取下标 `n // 2` 处的数'
        return '排序后，中位数就在下标 `n // 2`'
    m = S['median']
    d = [abs(x - m) for x in S['nums']]
    return f'到中位数 `{m}` 的距离：`{" + ".join(map(str, d))}` = =={sum(d)}=='


CONFIG = dict(
    num=462, title='最小操作次数使数组元素相等 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='中位数贪心',
    tags=[],
    code='''
class Solution:
    def minMoves2(self, nums: List[int]) -> int:
        nums.sort()
        median = nums[len(nums) // 2]
        return sum(abs(x - median) for x in nums)
''',
    call='Solution().minMoves2([7, 1, 9, 2, 4, 8, 3])',
    expect=18,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='bars', var='nums', pointers={'len(nums) // 2': 'pink'}, h=380, label='nums',
             color=lambda S, i, v: 'pink' if i == len(S['nums']) // 2 and 'median' in S else None),
        dict(type='array', var='[abs(x - median) for x in nums]', h=170, label='每个数到中位数的操作次数 |x − median|'),
    ],
    watch=['median', ('x', 'x', 'blue')],
    captions={
        'nums.sort()': '先排序：`nums = {nums}`，中位数就落在中间',
        'median =': '中位数取下标 `len(nums) // 2 = {len(nums) // 2}`，`median = {median}`（奇偶都能用这个下标）',
        'return sum': lambda S, B, r: (f'所有数都变成中位数 `{S.median}`：总操作数 = 各数到它的距离之和 = =={r}==' if r is not None
                                       else f'累加 `|{S.x} − {S.median}| = {abs(S.x - S.median)}`'),
    },
    cards=dict(
        one_liner='所有数都变成中位数，总操作数最少',
        complexity='时间 `O(n log n)`（快速选择可 `O(n)`），空间 `O(1)`',
        problem=['每次操作可以让数组中一个数加 1 或减 1',
                 '求让所有元素相等的最少操作次数',
                 '示例：`[1,10,2,9]` → `16`；本视频：`[7,1,9,2,4,8,3]` → `18`'],
        quote='定理：把所有数都变成 nums 的中位数是最优的。无论 n 是奇数还是偶数，中位数的下标都可以取 ⌊n/2⌋。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先排序，取下标 `n // 2` 的数作为目标 `median`',
              '答案就是每个数到 `median` 的距离之和',
              '另一种写法：用快速选择找中位数，`O(n)`'],
        after=[dict(heading='另一种写法', lines=['用快速选择找中位数，平均 `O(n)`（见原文 C++/Rust）', '定理的证明见原文链接'])],
        summary=['时间 `O(n log n)`，空间 `O(1)`（忽略排序栈）',
                 '奇偶都取 `nums[n // 2]`：偶数时中间两个数任取一个，答案相同',
                 '易错点：题目保证答案在 32 位内，Python 无需担心溢出',
                 '`nums.sort()` 会改变原数组'],
    ),
)
