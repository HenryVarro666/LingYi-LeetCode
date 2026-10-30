CONFIG = dict(
    num=1712, title='将数组分成三个子数组的方案数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举 l + 双指针 min_r / max_r',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·常用数据结构', '难度分 2079'],
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
    call='Solution().waysToSplit([1,2,2,2,5,0])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=240, label='nums（蓝 = 左段，框 = min_r..max_r）',
             pointers={'l': 'blue', 'min_r': 'green', 'max_r': 'pink'},
             color=lambda S, i, v: ('blue' if i <= S['l'] else None) if 'l' in S else None,
             window=('min_r', 'max_r')),
        dict(type='text', fn=lambda S: (
            f"左段和 `l_sum = {S['l_sum']}`，右段和 `s − l_sum − m_sum_min = {S['s'] - S['l_sum'] - S['m_sum_min']}`" if 'm_sum_min' in S and 'l_sum' in S and 's' in S else '')),
        dict(type='text', fn=lambda S: (
            f"中段和最小 `{S['m_sum_min']}`（右端点 `min_r = {S['min_r']}`），最大 `{S['m_sum_max']}`（右端点 `max_r = {S['max_r']}`）" if 'm_sum_max' in S and 'max_r' in S else '')),
        dict(type='text', fn=lambda S: f"当前 `l = {S['l']}` 可行的中段右端点有 =={S['max_r'] - S['min_r'] + 1 if S['max_r'] >= S['min_r'] else 0}== 个" if 'max_r' in S and 'l' in S and S['_line'] in (27, 28, 29) else ''),
    ],
    skip=['if res >= mod', 'res = 0', 'mod = 10', 'n = len(nums)'],
    watch=[('l', 'l', 'blue'), ('min_r', 'min_r', 'green'), ('max_r', 'max_r', 'pink'), 'l_sum', 'm_sum_min', 'm_sum_max', ('res', 'res', 'yellow')],
    captions={
        'l = 0': '`l` 是第一个子数组的右边界，从 0 开始往右枚举',
        'min_r = max_r = 1': '`min_r` / `max_r`：中间段右边界的最小 / 最大可行位置，先都放在 1',
        'l_sum = nums[0]': '第一段 `nums[0..l]` 的和：`l_sum = {l_sum}`',
        'm_sum_min = m_sum_max': '中间段先只含 `nums[1]`，和 = {m_sum_min}',
        's = sum': '整个数组总和 `s = {s}`，第三段和 = `s − l_sum − m_sum`',
        'while l < n - 2': lambda S, B, r: f'枚举 `l = {S.l}`：后面还要留出中、右两段，所以 `l < n − 2`' if S.l < S.n - 2 else '`l` 枚举完了，退出',
        'while min_r + 1 < n - 1 and m_sum_min < l_sum': lambda S, B, r: (
            f'中段和 `{S.m_sum_min}` < 左段和 `{S.l_sum}` 不满足 `left <= mid`，且 min_r 还能右移 → 继续' if (S.min_r + 1 < S.n - 1 and S.m_sum_min < S.l_sum)
            else f'`min_r` 已到极限或 `m_sum_min = {S.m_sum_min} >= l_sum = {S.l_sum}`：最小右边界找到了'),
        'min_r += 1': '中段还不够大，`min_r` 右移到 {min_r}',
        'm_sum_min += nums[min_r]': '把 `nums[{min_r}]` 并入中段：`m_sum_min = {m_sum_min}`',
        'if m_sum_min >= l_sum and': lambda S, B, r: (
            f'`left={S.l_sum} <= mid={S.m_sum_min}` 且 `right={S.s - S.l_sum - S.m_sum_min} >= mid` → ==这个 l 有解==' if (S.m_sum_min >= S.l_sum and S.s - S.l_sum - S.m_sum_min >= S.m_sum_min)
            else f'`left={S.l_sum}`、`mid={S.m_sum_min}`、`right={S.s - S.l_sum - S.m_sum_min}` 不满足 left≤mid≤right → 这个 `l` 没有合法分法'),
        'if min_r > max_r': lambda S, B, r: ('`max_r` 落在 `min_r` 左边，不可能：把它追到 `min_r`' if S.min_r > S.max_r else '`max_r` 已不小于 `min_r`，沿用上一轮的位置'),
        'max_r = min_r': '`max_r` 追上 `min_r`：`max_r = {max_r}`（`m_sum_max` 下一行同步）',
        'm_sum_max = m_sum_min': '`m_sum_max` 同步为 `m_sum_min = {m_sum_max}`',
        'while max_r + 1 < n - 1 and s': lambda S, B, r: (
            f'再并入 `nums[{S.max_r + 1}]` 后：中段 `{S.m_sum_max + S.nums[S.max_r + 1]}`，右段 `{S.s - S.l_sum - S.m_sum_max - S.nums[S.max_r + 1]}`，右段 ≥ 中段 → 可以继续右移'
            if (S.max_r + 1 < S.n - 1 and S.s - S.l_sum - S.m_sum_max - S.nums[S.max_r + 1] >= S.m_sum_max + S.nums[S.max_r + 1])
            else '再右移一格，右段就会比中段小（或到了边界）→ `max_r` 停在这里'),
        'max_r += 1': '`max_r` 右移到 {max_r}',
        'm_sum_max += nums[max_r]': '`m_sum_max = {m_sum_max}`',
        'res += max_r - min_r + 1': '右边界可取 `min_r..max_r`，共 `{max_r} - {min_r} + 1` = =={max_r - min_r + 1}== 种：`res = {res}`',
        'if res >= mod': '答案对 `10^9 + 7` 取模（这里还很小，不触发）',
        'l += 1': '`l` 右移：`nums[{l}]` 从中段挪到左段',
        'm_sum_min -= nums[l]': '中段（最小版）失去 `nums[{l}]`：`m_sum_min = {m_sum_min}`',
        'm_sum_max -= nums[l]': '中段（最大版）同样失去它：`m_sum_max = {m_sum_max}`',
        'l_sum += nums[l]': '左段变大：`l_sum = {l_sum}`',
        'if min_r == l': lambda S, B, r: (
            f'`min_r == l`：中段被吃空了！必须马上把 `min_r` 推到 `l + 1`，不能靠 m_sum 去判断（有 0 时会卡住）' if S.min_r == S.l
            else '`min_r` 还在 `l` 右边，不用特殊处理'),
        'min_r = l + 1': '`min_r = {min_r}`',
        'm_sum_min = nums[min_r]': '中段重新只含 `nums[{min_r}]`：`m_sum_min = {m_sum_min}`',
        'return res': '所有 `l` 枚举完，方案数 ==`{res}`==',
    },
    cards=dict(
        one_liner='枚举第一段右边界 l，双指针夹出中段右边界的区间',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把非负数组切成三段非空连续子数组，要求 左和 ≤ 中和 ≤ 右和',
                 '返回方案数，对 `10^9+7` 取余',
                 '示例：`[1,2,2,2,5,0]` → `3`'],
        quote='数组中的数都是非负数，那么在枚举了l之后，可以利用双指针确定中间这个区间的最小右边界min_r以及最大右边界max_r。',
        quote_src='—— yiduobo 题解',
        idea=['朴素做法枚举 l 再枚举 r，是 `O(n^2)`',
              '非负 → l 右移时 `min_r`、`max_r` 都不会左退，只增不减，均摊 `O(1)`',
              '每个 l 提供 `max_r - min_r + 1` 种分法，累加即可'],
        after=[dict(heading='yiduobo 强调的特殊情况', lines=[
            '`l` 追上 `min_r` 时，必须立即把 `min_r` 更新为 `l + 1`',
            '不能指望靠 `m_sum` 去推动 `min_r`',
            '数组里有 0 且 `l_sum` 为 0 时，`min_r` 会一直不更新'])],
        summary=['时间 `O(n)`：`l`、`min_r`、`max_r` 都只增不减',
                 '易错点：`min_r == l` 时要立即重置，否则中段为空',
                 '易错点：`max_r` 可能落后于 `min_r`，要先追上再继续右移',
                 '取模：每次累加后若 `res >= mod` 就减一次 `mod`',
                 '原文已是 Python 3 可运行写法，代码未作改动（仅删去行尾空白）'],
    ),
)
