CONFIG = dict(
    num=3396, title='使数组元素互不相同所需的最少操作次数', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='倒着遍历 · 最长无重复后缀',
    tags=[],
    code='''
class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        seen = set()
        for i in range(len(nums) - 1, -1, -1):
            x = nums[i]
            if x in seen:
                return i // 3 + 1
            seen.add(x)
        return 0
''',
    call='Solution().minimumOperations([1, 2, 3, 4, 2, 3, 3, 5, 7])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=260,
             color=lambda S, k, v: 'green' if 'i' in S and k > S['i'] else None, label='nums（绿色 = 已倒着遍历、没有重复的后缀）'),
        dict(type='set', var='seen', fmt=lambda x: str(x), h=160),
        dict(type='text', fn=lambda S: (f'前 `{S["i"]+1}` 个数都要移除，每次 3 个：`{S["i"]} // 3 + 1 = {S["i"]//3+1}` 次') if S.get('x') in S.get('seen', ()) and 'i' in S and S.get('_line') == 7 else '', size=28, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'orange'), ('seen', 'sorted(seen)', 'cyan')],
    captions={
        'seen = set()': '`seen` 记录倒着遍历时见过的数',
        'for i in range': '倒着遍历，现在 `i = {i}`',
        'x = nums[i]': '`x = nums[{i}] = {x}`',
        'if x in seen': '`{x}` 之前遍历过吗？{"遍历过：重复了" if x in seen else "没有，后缀目前仍无重复"}',
        'return i // 3': '下标 `[0, {i}]` 共 `{i+1}` 个数都要移除，`{i} // 3 + 1` = =={ret}== 次（等于上取整 `ceil({i+1}/3)`）',
        'seen.add(x)': '`{x}` 加入 `seen`，后缀继续变长',
        'return 0': '整个数组没有重复元素，不需要操作',
    },
    cards=dict(
        one_liner='剩下的一定是后缀，找最长的无重复后缀',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次操作移除数组开头 3 个元素（不足 3 个就全移除）',
                 '求使元素互不相同的最少操作次数',
                 '示例：`[1,2,3,4,2,3,3,5,7]` → `2`'],
        quote='每次操作，移除的都是 nums 的开头的元素，或者说移除的是 nums 的前缀。所以移除后，剩余的元素一定是 nums 的后缀。',
        quote_src='—— 灵茶山艾府题解',
        idea=['本质：找 `nums` 最长的、没有重复元素的后缀',
              '倒着遍历，`nums[i]` 之前出现过，说明 `[0, i]` 都要移除',
              '共 `i + 1` 个数，需要 `ceil((i+1)/3) = i // 3 + 1` 次'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：必须倒着遍历，先遇到的重复才决定最长后缀',
                 '上取整转下取整：`ceil((i+1)/3) = i // 3 + 1`',
                 '同类题：3779（题面一致，仅数据范围更大）'],
    ),
)
