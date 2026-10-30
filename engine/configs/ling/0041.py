NUMS = [3, 4, -1, 1, 1]


def _while_cap(S, B, ret):
    i, n, nums = B.i, B.n, B.nums
    v = nums[i]
    if not 1 <= v <= n:
        return f'座位 `{i + 1}` 上的学号 `{v}` 不在 `[1, {n}]` 中 → ==忽略==，看下一个座位'
    if nums[v - 1] == v:
        if v - 1 == i:
            return f'学号 `{v}` 已经坐在自己的座位 `{v}` 上，看下一个座位'
        return f'座位 `{v}` 上已经坐着 `{v}` 的真身：当前是==影分身==，跳过（交换会死循环）'
    return f'学号 `{v}` 应该坐座位 `{v}`，那里坐的是 `{nums[v - 1]}`（不是真身）→ 交换'


def _if_cap(S, B, ret):
    i, v = B.i, B.nums[B.i]
    if v != i + 1:
        return f'座位 `{i + 1}` 上坐的是 `{v}`：==没有学号为 {i + 1} 的学生=='
    return f'座位 `{i + 1}` 上是 `{v}`，匹配'


CONFIG = dict(
    num=41, title='缺失的第一个正数', difficulty='Hard', category='普通数组',
    author='灵茶山艾府', technique='原地哈希（换座位）',
    code='''
class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)
        for i in range(n):
            # 如果当前学生的学号在 [1,n] 中，但（真身）没有坐在正确的座位上
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                # 那么就交换 nums[i] 和 nums[j]，其中 j 是 i 的学号
                j = nums[i] - 1  # 减一是因为数组下标从 0 开始
                nums[i], nums[j] = nums[j], nums[i]

        # 找第一个学号与座位编号不匹配的学生
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        # 所有学生都坐在正确的座位上
        return n + 1
''',
    call=f'Solution().firstMissingPositive({NUMS})',
    expect=2,
    views=[
        dict(type='array', var=lambda S: list(range(1, len(NUMS) + 1)), label='座位编号（= 下标 + 1）', index=False,
             color=lambda S, k, v: 'cyan' if 'i' in S and k == S['i'] else None, cell=100, h=150),
        dict(type='array', var='nums', label='nums：坐在每个座位上的学号（绿 = 坐对了）', pointers={'i': 'yellow', 'j': 'pink'},
             color=lambda S, k, v: 'green' if v == k + 1 else None,
             dim=lambda S, k, v: not 1 <= v <= len(NUMS), cell=100, h=240),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'pink'), 'n', ('nums', 'nums', 'cyan')],
    captions={
        4: lambda S, B, ret: (f'看座位 `{S.i + 1}`（下标 `i = {S.i}`）' if 'i' not in B or S.i != B.i else '换座位结束'),
        12: lambda S, B, ret: (f'从左往右找第一个对不上的：看座位 `{S.i + 1}`' if S.i != B.i else '全部看完'),
        'n = len(nums)': '`n = {n}` 个座位，编号 1 到 `{n}`；学号不在 `[1, {n}]` 的学生可以忽略',
        'while 1 <= nums[i] <= n': _while_cap,
        'j = nums[i] - 1': '学号 `{nums[i]}` 的座位下标 `j = {nums[i]} − 1 = {j}`',
        'nums[i], nums[j] = nums[j], nums[i]': '交换：学号 `{nums[j]}` 坐到座位 `{j + 1}`；换过来的 `{nums[i]}` 留在座位 `{i + 1}`，继续看它',
        'if nums[i] != i + 1': _if_cap,
        'return i + 1': '缺失的第一个正数是 =={ret}==',
        'return n + 1': '所有学生都坐对了，答案是 `n + 1 = {ret}`',
    },
    cards=dict(
        one_liner='换座位：让学号 x 的学生坐到第 x 个座位，第一个对不上的座位号就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找出未排序整数数组中==没有出现的最小正整数==',
                 '要求时间 `O(n)`，只用常数额外空间',
                 '示例：`[3,4,-1,1]` → `2`；`[7,8,9,11,12]` → `1`',
                 '演示用 `[3,4,-1,1,1]` → `2`（含重复的「影分身」）'],
        quote='把 nums[i] 当作坐在第 i 个座位上的学生的学号。我们要做的事情，就是让学号在 1 到 n 中的学生，都坐到编号与自己学号相同的座位上。',
        quote_src='—— 灵茶山艾府题解「换座位」',
        idea=['学号不在 `[1, n]` 的忽略；换完再看当前座位上新来的学生，直到换不动',
              '判断 `nums[nums[i]-1] != nums[i]`：==真身已就座就不换==（自己或影分身都适用），否则会死循环',
              '最后从左往右找第一个 `nums[i] ≠ i + 1`，答案是 `i + 1`；全都对上就是 `n + 1`'],
        summary=['时间 `O(n)`：每次交换都让一个学生坐对，总交换至多 `n` 次',
                 '不能用 `nums[i] != i + 1` 当交换条件：有重复元素时会死循环',
                 'Python 要先算 `j` 再交换：写成 `nums[i], nums[nums[i]-1] = …` 会先改掉 `nums[i]`',
                 '答案一定在 `[1, n + 1]` 里，所以只关心 `1..n` 的数'],
    ),
)
