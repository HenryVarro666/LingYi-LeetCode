def _cands(a):
    return [a[-3] - a[0], a[-2] - a[1], a[-1] - a[2]]


def _color(S, i, v):
    n = len(S['a'])
    if i in (0, 1, 2):
        return 'pink'
    if i in (n - 1, n - 2, n - 3):
        return 'orange'
    return None


CONFIG = dict(
    num=2567, title='修改两个元素的最小分数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 枚举三种改法',
    tags=['灵神题单', '难度分 1609'],
    code='''
class Solution:
    def minimizeSum(self, a: List[int]) -> int:
        a.sort()
        return min(a[-3] - a[0], a[-2] - a[1], a[-1] - a[2])
''',
    call='Solution().minimizeSum([1,4,7,8,5,10,3])',
    expect=5,
    views=[
        dict(type='text', size=28, fn=lambda S: ('排序后：改最大的两个数、改一大一小、改最小的两个数，三选一' if 'a' in S and S['a'] == sorted(S['a']) else '先排序，才能说“最大的”“最小的”')),
        dict(type='array', var='a', h=240, color=_color, label='a（粉 = 最小的三个，橙 = 最大的三个）'),
        dict(type='text', size=28, fn=lambda S: (
            f"改最大两个：`a[-3] − a[0] = {S['a'][-3]} − {S['a'][0]} = {S['a'][-3]-S['a'][0]}`　"
            f"改一大一小：`a[-2] − a[1] = {S['a'][-2]} − {S['a'][1]} = {S['a'][-2]-S['a'][1]}`　"
            f"改最小两个：`a[-1] − a[2] = {S['a'][-1]} − {S['a'][2]} = {S['a'][-1]-S['a'][2]}`") if 'a' in S and S['a'] == sorted(S['a']) else ''),
    ],
    watch=[],
    captions={
        'a.sort()': '从小到大排序：`{a}`。最大得分最优时，只会和两端的元素有关',
        'return min': lambda S, B, r: f"三种改法的最大得分：`{_cands(S.a)}`，最小得分都能变成 `0`（改出两个相同的数）→ 取最小 ==`{r}`==",
    },
    cards=dict(
        one_liner='只能改两个数：要么改两头的，三种方案取最小',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['分数 = 最大得分 + 最小得分，两个得分都是任意两数之差的绝对值',
                 '最多改 2 个元素，求最小分数',
                 '示例：`[1,4,7,8,5]` → `3`；本视频用 `[1,4,7,8,5,10,3]` → `5`'],
        quote='对于更内部的元素，比如 nums[3]，一定不可能参与最大得分的计算。反证法：如果 nums[3] 参与最大得分的计算，这意味着我们把 nums[0],nums[1],nums[2] 都改了，不符合题目要求，矛盾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，最小得分总能是 `0`：把一个数改成另一个数',
              '最大得分取决于改完后的最大、最小，只能删掉两个端点',
              '`a[-3]-a[0]`、`a[-2]-a[1]`、`a[-1]-a[2]` 三种，取最小'],
        after=[dict(heading='三种改法', lines=['改最大的两个为 `a[n-3]` → 最大得分 `a[n-3] − a[0]`',
                                            '改最小的、最大的 → 最大得分 `a[n-2] − a[1]`',
                                            '改最小的两个为 `a[2]` → 最大得分 `a[n-1] − a[2]`'])],
        summary=['时间 `O(n log n)`，瓶颈在排序；用快速选择可做到 `O(n)`',
                 '最小得分一定是 `0`，因为三种方案里都会“造出”重复的数',
                 '`n >= 3`，所以 `a[2]`、`a[-3]` 不会越界',
                 '“删掉两端若干个”是这类题的常见贪心套路'],
    ),
)
