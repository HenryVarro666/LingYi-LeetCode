_I = lambda S: S['_inner'].get('i')
_LOW = lambda S: [0] * S['diff_lh'] + S['low_s']


def _range(S, B, ret):
    return (f"`lo = {S.lo}`，`hi = {S.hi}`：第 {S.i} 位可填 `{S.lo}` 到 `{S.hi}`"
            + ('，==受 low 约束，下限抬高==' if S.limit_low and S.lo > 0 else '')
            + ('，==受 high 约束，上限收紧==' if S.limit_high else ''))


def _sub(S, B, ret):
    bi = B['_inner']
    d, i = bi['d'], bi['i']
    nd = bi['diff'] + (d if i % 2 else -d)
    if S.i == bi['i']:  # 准备参数
        return (f"第 {i} 位（{'偶' if i % 2 else '奇'}数位）填 `d = {d}`：`diff {'+' if i % 2 else '−'} {d}` → 新 diff = `{nd}`")
    return (f"递归进入第 {i + 1} 位：`limit_low = {bi['limit_low'] and d == bi['lo']}`，"
            f"`limit_high = {bi['limit_high'] and d == bi['hi']}`（只有填到边界值才继续受约束）")


def _for(S, B, ret):
    bi = B['_inner']
    if 'd' not in bi:
        return f"枚举第 `{bi['i']}` 位填的数字 `d`，范围 `{bi['lo']}` 到 `{bi['hi']}`"
    if bi['d'] == bi['hi']:
        return f"子问题返回，累计 `res = {bi['res']}`；`d` 已枚举到 `hi = {bi['hi']}`，这一位填完了"
    return f"子问题返回，累计 `res = {bi['res']}`；换下一个数字 `d = {bi['d'] + 1}`"


CONFIG = dict(
    num=3791, title='给定范围内平衡整数的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='上下界数位 DP · 只记 diff',
    tags=['灵神题单', '难度分 2132'],
    code='''
class Solution:
    def countBalanced(self, low: int, high: int) -> int:
        # 最小的满足要求的数是 11
        if high < 11:
            return 0

        low = max(low, 11)
        low_s = list(map(int, str(low)))  # 避免在 dfs 中频繁调用 int()
        high_s = list(map(int, str(high)))
        n = len(high_s)
        diff_lh = n - len(low_s)

        @cache
        def dfs(i: int, diff: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1 if diff == 0 else 0

            lo = low_s[i - diff_lh] if limit_low and i >= diff_lh else 0
            hi = high_s[i] if limit_high else 9

            res = 0
            for d in range(lo, hi + 1):
                res += dfs(i + 1,
                           diff + (d if i % 2 else -d),
                           limit_low and d == lo,
                           limit_high and d == hi)
            return res

        return dfs(0, 0, True, True)
''',
    call='Solution().countBalanced(95, 121)',
    expect=3,
    views=[
        dict(type='array', var='high_s', label='high_s（上界 121 的每一位）', cell=70, h=175, pointers={_I: 'pink'}, pointer_labels={_I: 'i'}),
        dict(type='array', var=_LOW, label='low_s（下界 95，左边补 0 对齐）', cell=70, h=175, pointers={_I: 'pink'}, pointer_labels={_I: 'i'}),
        dict(type='text', size=34, fn=lambda S: (f"diff = 奇数位和 − 偶数位和 = ==`{S['_inner']['diff']}`==，等于 0 才平衡"
                                                   if 'diff' in S['_inner'] else '')),
        dict(type='calls', h=220),
    ],
    watch=[('i', _I, 'pink'), ('diff', lambda S: S['_inner'].get('diff'), 'cyan'), 'lo', 'hi', ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=['n = len(high_s)', 'res = 0', 'low_s = list', 'high_s = list', 'diff + (d if', 'limit_low and d == lo,', 'limit_high and d == hi)'],
    max_steps=52,
    captions={
        'if high < 11': '`high = {high}`，不小于 11 → 还有可能有平衡数；11 是最小的平衡数',
        'low = max(low, 11)': '`low` 抬到 `max(low, 11) = {low}`：保证至少两位数',
        'diff_lh = ': '`diff_lh = n - len(low_s) = {diff_lh}`：low 比 high 短几位，==前导零对 diff 没有影响==，所以不用单独处理',
        'return 1 if diff == 0': lambda S, B, ret: (f'填满 {S.n} 位，`diff = {S.diff}` → ' + ('==等于 0，平衡，计 1 个==' if S.diff == 0 else '不等于 0，不平衡，计 0 个')),
        'lo = low_s': '`lo`：受 low 约束时这一位不能比 low 的对应位小；没有对应位（补零部分）就是 0',
        'hi = high_s': _range,
        'for d in range': _for,
        'res += dfs': _sub,
        'return res': lambda S, B, ret: f'`dfs({S.i}, {S.diff}, {S.limit_low}, {S.limit_high})` 的方案数 = ==`{ret}`==（记忆化，下次直接用）',
        'return dfs(0, 0': '入口：从最高位出发，`diff = 0`，同时受 low 和 high 约束',
    },
    cards=dict(
        one_liner='平衡 ⇔ 奇数位和 − 偶数位和 = 0，只需维护一个 `diff`',
        complexity='时间 `O(n²D²)`，空间 `O(n²D)`',
        problem=['一个数至少两位，且偶数位数字之和等于奇数位数字之和，称为平衡整数',
                 '求 `[low, high]` 内平衡整数个数，`high ≤ 10^15`',
                 '示例：`[1, 100]` → `9`；本视频：`[95, 121]` → `3`（99、110、121）'],
        quote='所以只需维护 diff = 奇数位之和 - 偶数位之和。此外，还需要知道当前填的是奇数位还是偶数位，可以用 i 的奇偶性表示。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `dfs(i, diff, limit_low, limit_high)`：同时受 low、high 约束的数位 DP',
              '`lo` / `hi` 是这一位的上下限，填到边界值才继续受约束',
              '前导零不影响 diff，所以去掉 is_num，写法一里“不填数字”的分支可以省掉'],
        summary=['时间 `O(n²D²)`：状态 `O(n²D)`，每个状态枚举 `D` 个数字',
                 '先处理 `high < 11` 与 `low = max(low, 11)`，保证至少两位数',
                 '`low_s[i - diff_lh]`：low 比 high 短，要对齐位置',
                 '本视频用写法二；写法一显式处理“不填数字”（前导零），结果相同',
                 '同类题：上下界数位 DP 模板（600、902、2719 等）'],
    ),
)
