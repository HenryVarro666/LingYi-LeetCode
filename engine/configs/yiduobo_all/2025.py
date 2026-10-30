NUMS, K = [3, 1, -2, 2, 0, 2], 2


CONFIG = dict(
    num=2025, title='分割数组的最多方案数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 左右两个哈希表',
    tags=['前缀和与哈希表', '难度分 2218'],
    code='''
class Solution(object):
    def waysToPartition(self, nums, k):

        s = [nums[0]]
        n = len(nums)
        for num in nums[1:]:
            s.append(s[-1] + num)

        left_cnt = {}
        for index in range(n - 1):
            left_cnt[s[index]] = left_cnt.get(s[index], 0) + 1

        if s[-1] % 2 == 0:
            res = left_cnt.get(s[-1] // 2, 0)
        else:
            res = 0

        if (s[-1] + k - nums[-1]) % 2 == 0:
            res = max(res, left_cnt.get((s[-1] + k - nums[-1]) // 2, 0))

        right_cnt = {}
        for index in range(n - 2, -1, -1):
            left_cnt[s[index]] -= 1
            right_cnt[s[index]] = right_cnt.get(s[index], 0) + 1
            delta = k - nums[index]

            if (s[-1] + delta) % 2 == 0:
                res = max(res, left_cnt.get((s[-1] + delta) // 2, 0) + right_cnt.get((s[-1] + delta) // 2 - delta, 0))

        return res
''',
    call=f'Solution().waysToPartition({NUMS}, {K})',
    expect=2,
    skip=['n = len', 's.append', 'for num in nums[1:]', 'else:', 'right_cnt = {}'],
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=170, pointers={'index': 'blue'}),
        dict(type='array', var='s', label='s（原始前缀和，s[i] = nums[0..i] 之和）', cell=84, h=170, pointers={'index': 'blue'}),
        dict(type='map', var='left_cnt', label='left_cnt（pivot 左侧的前缀和 → 个数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
        dict(type='map', var='right_cnt', label='right_cnt（pivot 右侧的原始前缀和 → 个数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
    ],
    watch=[('index', 'index', 'blue'), ('delta', 'delta', 'pink'), ('res', 'res', 'green')],
    captions={
        's = [nums[0]]': '`s` 记录原始前缀和，`s[i]` = `nums[0..i]` 之和',
        'for index in range(n - 1)': lambda S, B, r: (f'`s[{S.index}] = {S.s[S.index]}` 能当 pivot 左侧的和（pivot = {S.index + 1}）' if 'index' not in B or S.index != B.index else '各个前缀和都登记完了'),
        'left_cnt[s[index]] =': '`left_cnt[{s[index]}]` = `{left_cnt[s[index]]}`：先假设都在左侧',
        's[-1] % 2 == 0': lambda S, B, r: (f'总和 `{S.s[-1]}` 是偶数：不改数组时，需要前缀和 = `{S.s[-1] // 2}`' if S.s[-1] % 2 == 0
                                           else f'总和 `{S.s[-1]}` 是奇数：不改数组无解'),
        'res = left_cnt.get(s[-1] // 2, 0)': '不修改：前缀和等于 `{s[-1] // 2}` 的个数就是方案数 → `res = {res}`',
        'res = 0': '总和是奇数，不改的话方案数 `res = 0`',
        '(s[-1] + k - nums[-1]) % 2 == 0': lambda S, B, r: (f'把最后一个数改成 `k`：新总和 `{S.s[-1] + S.k - S.nums[-1]}`'
                                                           + ('，是偶数' if (S.s[-1] + S.k - S.nums[-1]) % 2 == 0 else '，是奇数，无解')),
        'res = max(res, left_cnt.get((s[-1] + k': '改最后一个数：所有分割点都在它左边，只看 `left_cnt` 里等于 `{(s[-1] + k - nums[-1]) // 2}` 的个数 → `res = {res}`',
        'left_cnt[s[index]] -= 1': '假设改的是 `nums[{index}]`：`s[{index}]` 起都在它之后 → 从 `left_cnt` 挪走',
        'right_cnt[s[index]] =': '`s[{index}]` 加入 `right_cnt`：它们的真实值会整体加上 `delta`',
        'delta = k - nums[index]': '修改 `nums[{index}]` 为 `{k}`：`delta = {k} − {nums[index]} = {delta}`，右侧前缀和都加 `delta`',
        '(s[-1] + delta) % 2 == 0': lambda S, B, r: (f'新总和 `{S.s[-1] + S.delta}`，偶数 → 目标前缀和 `{(S.s[-1] + S.delta) // 2}`'
                                                    if (S.s[-1] + S.delta) % 2 == 0 else f'新总和 `{S.s[-1] + S.delta}` 是奇数，这个位置改了也不行'),
        'res = max(res, left_cnt.get((s[-1] + delta)': lambda S, B, r: (
            f'左侧原样等于 `{(S.s[-1] + S.delta) // 2}` 的有 `{S.left_cnt.get((S.s[-1] + S.delta) // 2, 0)}` 个，'
            f'右侧原始前缀和等于 `{(S.s[-1] + S.delta) // 2 - S.delta}` 的有 `{S.right_cnt.get((S.s[-1] + S.delta) // 2 - S.delta, 0)}` 个 → `res = {S.res}`'),
        'return res': '最多 `{res}` 种分割',
    },
    cards=dict(
        one_liner='改第 index 个数：左边前缀和不变，右边前缀和整体加 delta',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`pivot` 把数组分成左右两段，两段和相等就是一种方案',
                 '可以把一个数改成 `k`（或不改），求最多有多少种分割',
                 '本视频：`nums = [3,1,-2,2,0,2]`，`k = 2` → `2`'],
        quote='对于index - 1以及之前的所有位置，对应的前缀和都不会发生变化。而对于s[index]以及之后的s，则都会在原始s的基础上加上k - nums[index]。',
        quote_src='—— yiduobo 题解原文',
        idea=['不改：前缀和等于 `总和/2` 的个数（总和须为偶数）',
              '改 `nums[index]`：新目标 `(总和 + delta)/2`，左侧前缀和照旧去找它',
              '右侧前缀和各加 `delta`，所以要去找原始值 `目标 − delta`',
              '`left_cnt`、`right_cnt` 随 index 从右往左挪动，每个位置 O(1)'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '总和（含修改后）必须是偶数，否则这个位置不可能分割',
                 '修改最后一个元素是特例：所有 pivot 都在它左边，单独算一次',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '因为先判断了偶数，`//` 与原文的 `/` 结果一致'],
    ),
)
