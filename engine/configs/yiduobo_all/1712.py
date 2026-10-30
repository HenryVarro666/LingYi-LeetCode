CONFIG = dict(
    num=1712, title='将数组分成三个子数组的方案数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举 l + 双指针 min_r / max_r',
    tags=['滑动窗口与双指针', '常用数据结构', '难度分 2079'],
    code='''
class Solution(object):
    def waysToSplit(self, nums):
        l = 0
        min_r = max_r = 1
        l_sum = nums[0]
        m_sum_min = m_sum_max = nums[1]
        s = sum(nums)

        res = 0
        mod = 10 ** 9 + 7
        n = len(nums)

        while l < n - 2:
            while min_r + 1 < n - 1 and m_sum_min < l_sum:
                min_r += 1
                m_sum_min += nums[min_r]

            if m_sum_min >= l_sum and s - l_sum - m_sum_min >= m_sum_min:
                if min_r > max_r:
                    max_r = min_r
                    m_sum_max = m_sum_min

                while max_r + 1 < n - 1 and s - l_sum - m_sum_max - nums[max_r + 1] >= m_sum_max + nums[max_r + 1]:
                    max_r += 1
                    m_sum_max += nums[max_r]

                res += max_r - min_r + 1
                if res >= mod:
                    res -= mod

            l += 1
            m_sum_min -= nums[l]
            m_sum_max -= nums[l]
            l_sum += nums[l]
            if min_r == l:
                min_r = l + 1
                m_sum_min = nums[min_r]

        return res
''',
    call='Solution().waysToSplit([1, 2, 2, 2, 5, 0])',
    expect=3,
    skip=['mod = 10', 'n = len(nums)', 'if res >= mod', 'm_sum_max += nums', 'm_sum_max -= nums', 'm_sum_max = m_sum_min', 'm_sum_min = nums[min_r]'],
    views=[
        dict(type='array', var='nums', label='nums（蓝：左段到 l；粉/黄：中段右端可取 min_r ~ max_r）', h=200, cell=80,
             pointers={'l': 'blue', 'min_r': 'pink', 'max_r': 'yellow'},
             color=lambda S, i, x: ('blue' if i <= S['l'] else 'pink' if i == S['min_r'] else 'yellow' if i == S['max_r'] else None) if 'max_r' in S else None),
        dict(type='text', h=90, size=24,
             fn=lambda S: (f"左段和 `{S['l_sum']}`，中段（到 min_r）`{S['m_sum_min']}`，右段 `{S['s'] - S['l_sum'] - S['m_sum_min']}`" if 's' in S and 'm_sum_min' in S else '')),
    ],
    watch=[('l', 'l', 'blue'), ('min_r', 'min_r', 'pink'), ('max_r', 'max_r', 'yellow'), 'l_sum', 'm_sum_min', 'm_sum_max', ('res', 'res', 'green')],
    captions={
        'l = 0': '`l` 是左段的右端点，从 0 开始枚举',
        'min_r = max_r = 1': '中段右端点范围 `[min_r, max_r]`，初始都是 1（中段至少一个数）',
        'l_sum = nums[0]': '`l_sum` = 左段之和，`m_sum_min` / `m_sum_max` = 中段到 `min_r` / `max_r` 的和',
        's = sum(nums)': '`s` = 整个数组之和 = {s}',
        'while l < n - 2': '枚举左段右端 `l = {l}`（后面要留给中段、右段各至少 1 个）',
        'while min_r + 1 < n - 1 and m_sum_min < l_sum': lambda S, B, r: (f'中段和 `{S.m_sum_min}` < 左段和 `{S.l_sum}`：中段太小，`min_r` 要右移' if S.m_sum_min < S.l_sum and S.min_r + 1 < len(S.nums) - 1 else '中段已经 ≥ 左段（或到头了），`min_r` 不用再动'),
        'min_r += 1': '`min_r` → {min_r}',
        'm_sum_min += nums[min_r]': '中段变长，`m_sum_min` = {m_sum_min}',
        'if m_sum_min >= l_sum and s': lambda S, B, r: (f'中段 `{S.m_sum_min}` ≥ 左段 `{S.l_sum}`，右段 `{S.s - S.l_sum - S.m_sum_min}` ≥ 中段 → `min_r` 合法' if S.m_sum_min >= S.l_sum and S.s - S.l_sum - S.m_sum_min >= S.m_sum_min
                                                         else '`min_r` 处不满足（中段太小或右段不够大）→ 这个 `l` 没有方案'),
        'if min_r > max_r': lambda S, B, r: ('`max_r` 落在 `min_r` 左边：先把它拉到 `min_r`' if S.min_r > S.max_r else '`max_r` 已经在 `min_r` 右边，从这里继续'),
        'max_r = min_r': '`max_r = {max_r}`，`m_sum_max = {m_sum_max}`',
        'while max_r + 1 < n - 1 and s - l_sum': lambda S, B, r: (f'再多放 `nums[{S.max_r + 1}] = {S.nums[S.max_r + 1]}` 进中段，右段 `{S.s - S.l_sum - S.m_sum_max - S.nums[S.max_r + 1]}` 仍 ≥ 中段 `{S.m_sum_max + S.nums[S.max_r + 1]}` → `max_r` 可右移'
                                                                  if S.max_r + 1 < len(S.nums) - 1 and S.s - S.l_sum - S.m_sum_max - S.nums[S.max_r + 1] >= S.m_sum_max + S.nums[S.max_r + 1]
                                                                  else '再放一个数右段就小于中段了 → `max_r` 到头'),
        'max_r += 1': '`max_r` → {max_r}',
        'res += max_r - min_r + 1': '`min_r..max_r` 内任取一个都合法：`res` += `{max_r} − {min_r} + 1` → =={res}==',
        'if res >= mod': '取模保持 `res < mod`',
        'l += 1': '`l` 右移到 {l}：`nums[{l}]` 从中段挪进左段',
        'm_sum_min -= nums[l]': '中段少了 `nums[{l}]`',
        'l_sum += nums[l]': '左段多了 `nums[{l}]`：`l_sum` = {l_sum}',
        'if min_r == l': lambda S, B, r: (f'`min_r` 追上了 `l`：中段空了，必须立刻重置为 `min_r = {S.l + 1}`' if S.min_r == S.l else '`min_r` 还在 `l` 右边，不用重置'),
        'min_r = l + 1': '`min_r = {min_r}`，`m_sum_min = nums[{min_r}]` = {nums[min_r]}',
        'return res': '全部 `l` 枚举完，方案数 `{ret}`',
    },
    cards=dict(
        one_liner='枚举左段右端 l，中段右端的合法范围只会单调右移',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组分成 3 段非空连续子数组 `left, mid, right`',
                 '要求 `sum(left) ≤ sum(mid) ≤ sum(right)`，求方案数（对 `10^9+7` 取模）',
                 '示例：`[1,2,2,2,5,0]` → `3`'],
        quote='数组中的数都是非负数，那么在枚举了l之后，可以利用双指针确定中间这个区间的最小右边界min_r以及最大右边界max_r。……此时就可以提供max_r - min_r + 1组可行的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素枚举两个端点是 `O(n^2)`；数全非负，所以 `l` 右移时 `min_r`、`max_r` 都不会左移',
              '`min_r`：使中段 ≥ 左段的最小右端；`max_r`：使右段 ≥ 中段的最大右端',
              '每个 `l` 贡献 `max_r - min_r + 1` 种方案'],
        summary=['时间 `O(n)`，空间 `O(1)`（两个指针总共只右移 `O(n)` 次）',
                 '易错：`l` 追上 `min_r` 后必须立刻重置 `min_r = l + 1`，不能靠 `m_sum_min` 更新（有 0 时会卡住）',
                 '易错：`min_r > max_r` 时要先把 `max_r` 和 `m_sum_max` 同步到 `min_r`',
                 '原文为 Python 2 风格写法，在 Python 3 下无需改动，只删去了多余空行'],
    ),
)
