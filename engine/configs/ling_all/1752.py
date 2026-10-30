def _top(S):
    if 'is_sorted' not in S:
        return ''
    n = S['nums']
    if 'x' in S and S['_line'] in (5, 6, 7, 8, 9):
        return f"相邻一对：`{S['x']}, {S['y']}`　是否已出现过严格递减：`{not S['is_sorted']}`"
    return f"`is_sorted = {S['is_sorted']}`（还没出现过严格递减）" if S['is_sorted'] else '`is_sorted = False`：已经遇到一次严格递减'


CONFIG = dict(
    num=1752, title='检查数组是否经排序和轮转得到', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='统计严格递减的次数',
    code='''
class Solution:
    def check(self, nums: list[int]) -> bool:
        is_sorted = True
        for x, y in pairwise(nums):
            if x > y:  # 严格递减
                if not is_sorted:  # 之前出现过严格递减，说明至少有三个递增段
                    return False
                is_sorted = False  # 标记遇到了严格递减
        return is_sorted or nums[0] >= nums[-1]
''',
    call='Solution().check([3,4,5,1,2])',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='nums', label='nums（蓝 = x，粉 = y）', cell=90,
             pointers={'nums.index(x)': 'blue', 'nums.index(y)': 'pink'},
             pointer_labels={'nums.index(x)': 'x', 'nums.index(y)': 'y'},
             color=lambda S, i, v: ('blue' if 'x' in S and v == S['x'] else 'pink' if 'y' in S and v == S['y'] else None)),
        dict(type='text', fn=lambda S: f"首尾比较：`nums[0] = {S['nums'][0]}`，`nums[-1] = {S['nums'][-1]}`", size=24),
    ],
    watch=[('is_sorted', 'is_sorted', 'green'), 'x', 'y'],
    captions={
        'is_sorted = True': '`is_sorted` 表示==至今没出现过严格递减==，先设为 True',
        'for x, y in pairwise': '看相邻一对 `x = {x}`，`y = {y}`',
        'if x > y': lambda S, B, r: (f'`{S.x} > {S.y}` → ==严格递减==，旋转点就在这里' if S.x > S.y
                                     else f'`{S.x} <= {S.y}`，还在同一个递增段里'),
        'if not is_sorted': '之前已经递减过一次了吗？`is_sorted = {is_sorted}` → 还没有，这是第一次',
        'return False': '这是第二次递减 → 至少三个递增段，旋转一次最多两段 → 返回 `False`',
        'is_sorted = False': '记下：已经遇到一次严格递减，再来一次就不行了',
        'return is_sorted or': lambda S, B, ret: (
            f'递减出现了一次，两段递增还要首尾接得上：`nums[0] = {S.nums[0]} >= nums[-1] = {S.nums[-1]}` → ==返回 {ret}=='),
    },
    cards=dict(
        one_liner='旋转后的递增数组：至多一处严格递减，且首尾能接上',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是否能由一个非递减数组轮转若干位得到',
                 '示例：`[3,4,5,1,2]` → `true`（源数组 `[1,2,3,4,5]` 轮转 2 位）',
                 '示例：`[2,1,3,4]` → `false`'],
        quote='`nums` 至多有一对相邻元素是严格递减的，即 `nums[i-1] > nums[i]` 至多出现一次。此外，如果有两个递增段，第二段的最大值不能超过第一段的最小值，即 `nums[0] >= nums[n-1]`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['轮转后的数组最多分成==两个递增段==，段与段之间就是那一处严格递减',
              '遍历相邻对，数严格递减的次数：第二次出现就返回 `False`',
              '只有一次递减时，还要保证第二段整体不超过第一段：`nums[0] >= nums[-1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：一次递减都没有（本来就有序）也是 `True`，所以最后是 `is_sorted or ...`',
                 '易错：只有一次递减还不够，`[2,1,3]` 首尾 `2 < 3` 接不上 → `False`',
                 '写法二：先算 `nums[0] >= nums[-1]` 当作 `is_sorted` 的初值，循环后直接返回 `True`'],
    ),
)
