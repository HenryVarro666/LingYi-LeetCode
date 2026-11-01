CONFIG = dict(
    num=2089, title='找出数组排序后的目标下标', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='不排序，数 less 和 equal', tags=[],
    code='''
class Solution:
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        less = equal = 0
        for x in nums:
            if x < target:
                less += 1
            elif x == target:
                equal += 1

        return list(range(less, less + equal))
''',
    call='Solution().targetIndices([1,2,5,2,3], 2)',
    expect=[1, 2],
    views=[
        dict(type='array', var='nums', label='nums（不用真的排序）', cell=96, h=240,
             color=lambda S, i, v: ('green' if v == S.get('target') else 'blue' if v < S.get('target', 0) else None) if 'less' in S else None),
        dict(type='array', var=lambda S: sorted(S['nums']), label='排序后（仅用于理解：蓝 = less 个，绿 = equal 个）', cell=96, h=240,
             color=lambda S, i, v: ('green' if v == S['target'] else 'blue' if v < S['target'] else None)),
        dict(type='text', h=90, size=32, fn=lambda S: f"`less = {S['less']}`，`equal = {S['equal']}`" if 'less' in S else ''),
    ],
    watch=[('x', 'x'), ('less', 'less', 'blue'), ('equal', 'equal', 'green'), 'target'],
    captions={
        'less = equal': '`less` 数比 target 小的个数，`equal` 数等于 target 的个数',
        'for x in nums': '看 `x = {x}`',
        'if x < target': '`{x} < {target}` → {"==成立，排序后它排在 target 前面，less += 1==" if x < target else "不成立"}',
        'less += 1': '`less` → {less}',
        'elif x == target': '`{x} == {target}` → {"==成立，equal += 1==" if x == target else "比 target 大，不影响答案"}',
        'equal += 1': '`equal` → {equal}',
        'return': '排序后 target 占 `[{less}, {less + equal - 1}]` 这段下标 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='不用排序：数出小于和等于 target 的个数就行',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 非递减排序后，返回所有 `nums[i] == target` 的下标（递增）',
                 '示例：`[1,2,5,2,3]`，`target = 2` → `[1,2]`',
                 '没有 target 返回空列表'],
        quote='由于排序后，相同的值是连续的，记小于 target 的元素个数为 less，等于 target 的元素个数为 equal，那么答案为 less, less+1, ..., less+equal-1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后相同的值连成一段，这段前面恰好有 `less` 个更小的数',
              '所以 target 的下标就是 `less` 到 `less + equal - 1`',
              '只需遍历一次计数，省掉排序的 `O(n log n)`'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计返回值）',
                 '易错点：区间是 `range(less, less + equal)`，右端点不含',
                 '`equal = 0` 时 `range` 为空，自然返回 `[]`',
                 '另一种写法是先排序再扫描，复杂度 `O(n log n)`'],
    ),
)
