CONFIG = dict(
    num=2357, title='使数组中所有元素都等于零', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='集合去重 · 数不同的正数',
    tags=[],
    code='''
class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        return len(set(nums) - {0})
''',
    call='Solution().minimumOperations([1,5,0,3,5])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', cell=96, h=200,
             color=lambda S, i, v: 'green' if v != 0 else 'pink'),
        dict(type='text', h=120, size=34,
             fn=lambda S: '不同的正数：`{1, 3, 5}`，共 ==3== 个 → 至少 3 次操作' if 'nums' in S else ''),
    ],
    watch=[('不同的正数', 'sorted(set(nums) - {0})', 'green')],
    captions={
        'return len': '`set(nums)` = `{sorted(set(nums))}`，去掉 `0` 后剩 `{sorted(set(nums) - {0})}`，个数 =={len(set(nums) - {0})}==，每个不同的正数恰好需要一次操作',
    },
    cards=dict(
        after=[dict(heading='为什么答案是不同正数的个数', lines=['每次操作取 `x` = 当前最小的正数，值最小的那一批数同时变 0','其余的数保持原来的大小关系，相等的数仍然相等','所以每一种不同的正数恰好消耗一次操作','`0` 本来就是 0，不需要操作，所以用 `- {0}` 去掉','示例 `[1,5,0,3,5]`：不同正数 1、3、5，操作 3 次，对应 x = 1, 2, 2'])],
        one_liner='答案就是数组里不同的正数的个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每步选 `x ≤ 最小非零元素`，所有正数都减去 `x`',
                 '求让整个数组变成 0 的最少操作数',
                 '示例：`[1,5,0,3,5]` → `3`'],
        quote='return len(set(nums) - {0})',
        quote_src='—— 灵茶山艾府题解（一行代码）',
        idea=['每次取 `x` = 最小非零元素，最小值那些数一次变成 0',
              '其余的数变小但仍然保持"相等的还是相等"',
              '所以每种不同的正数各需要一次操作：集合去重再减去 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：数组里的 `0` 不算操作，要从集合里去掉',
                 '`set(nums) - {0}` 是集合差集，一行搞定'],
    ),
)
