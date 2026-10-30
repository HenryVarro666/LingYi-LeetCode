def _in(S, k):
    return S['_inner'].get(k)


def _txt(S):
    inn = S['_inner']
    if 'i' not in inn or 'lo' not in inn:
        return '数位 DP：逐位填数字，`pre` = 上一位填的数，相邻差不能超过 `k`'
    return (f"第 {inn['i']} 位：能填 `[{inn.get('start', inn['lo'])}, {inn['hi']}]`；"
            f"`pre = {inn['pre']}`，`k = {S['k']}`，|d − pre| ≤ k 才能填")


CONFIG = dict(
    num=3966, title='统计范围内的好整数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP v2.1（上下界，无 isNum）',
    tags=['灵神题单', '动态规划', '难度分 2006'],
    code='''
class Solution:
    def goodIntegers(self, l: int, r: int, k: int) -> int:
        low_s = list(map(int, str(l)))  # 避免在 dfs 中频繁调用 int()
        high_s = list(map(int, str(r)))
        n = len(high_s)
        diff_lh = n - len(low_s)

        @cache
        def dfs(i: int, pre: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1  # 找到一个好数

            lo = low_s[i - diff_lh] if limit_low and i >= diff_lh else 0
            hi = high_s[i] if limit_high else 9

            res = 0
            start = lo

            if limit_low and i < diff_lh:
                # 不填数字，上界不受约束
                res = dfs(i + 1, 0, True, False)
                start = 1  # 下面填数字，从 1 开始填

            # 如果在 diff_lh 之前填过数字，那么 limit_low 一定是 False
            is_first_num = limit_low and i <= diff_lh
            for d in range(start, hi + 1):
                if is_first_num or abs(d - pre) <= k:
                    res += dfs(i + 1, d, limit_low and d == lo, limit_high and d == hi)

            return res

        # pre 的初始值随意
        return dfs(0, 0, True, True)
''',
    call='Solution().goodIntegers(9, 14, 1)',
    expect=4,
    views=[
        dict(type='array', var='high_s', label='high_s = r 的数位（蓝 = 当前位）', cell=70, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('i') else None),
        dict(type='array', var='low_s', label='low_s = l 的数位（l 比 r 短，高位对不上）', cell=70, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('i', -9) - S.get('diff_lh', 0) else None),
        dict(type='text', fn=_txt, size=24, h=90),
        dict(type='calls', h=230),
    ],
    watch=[('i', lambda S: _in(S, 'i'), 'blue'), ('pre', lambda S: _in(S, 'pre'), 'cyan'),
           ('lo', lambda S: _in(S, 'lo'), 'green'), ('hi', lambda S: _in(S, 'hi'), 'orange'),
           ('res', lambda S: _in(S, 'res'), 'yellow'), ('k', 'k', 'pink')],
    skip=['res = 0', 'start = lo', 'low_s = list', 'high_s = list', 'n = len'],
    captions={
        'diff_lh = ': '`l` 比 `r` 少 `{diff_lh}` 位：前 `{diff_lh}` 位 `l` 相当于没填数字（前导零）',
        'return dfs(0, 0, True, True)': '从最高位出发：同时受 `l`、`r` 约束；`pre` 初值随意，因为第一个数字不看 pre',
        'if i == n': lambda S, B, ret: ('`i == n`：每一位都填完 → 找到一个好数，返回 `1`' if S.i == S.n
                                        else f'`i = {S.i} < n`：还没填完，继续枚举这一位'),
        'lo = low_s': lambda S, B, ret: (
            f'`lo = {S.lo}`：受 low 约束，这一位不能比 `l` 的对应位 `{S.lo}` 小' if S.limit_low and S.i >= S.diff_lh else
            f'`lo = 0`：`l` 在这一位没有对应数位（或已不受约束）→ 下限 0'),
        'hi = high_s': '`hi = {hi}`：受 high 约束时，这一位不能比 `r` 的这一位大；否则上限 9',
        'res = dfs(i + 1, 0, True, False)': '`l` 的前导位：==这一位不填数字==，上界 `r` 的约束解除（位数更少一定更小）→ 先去算这条分支',
        'is_first_num = ': '`is_first_num = {is_first_num}`：为真说明这是数字的最高位，没有前一位，不用比较相邻差',
        'for d in range': lambda S, B, ret: (
            f'`d` 已枚举到上限 `hi = {S.hi}`，这一位结束' if S.d >= S.hi and B.get('d') == S.d and B.get('pre') == S.pre else
            f'枚举这一位的数字 `d`（从 `{S.start}` 到 `{S.hi}`），轮到 `d = {S.d}`'),
        'if is_first_num or': lambda S, B, ret: (
            f'`d = {S.d}` 是最高位 → 直接可填' if S.is_first_num else
            f'`|{S.d} − {S.pre}| = {abs(S.d - S.pre)}` ' + ('≤' if abs(S.d - S.pre) <= S.k else '>') + f' `k = {S.k}` → ' +
            ('可以填' if abs(S.d - S.pre) <= S.k else '==相邻差太大，跳过==')),
        'res += dfs(i + 1, d': '填 `d = {d}`，进入下一位：`pre = {d}`；是否继续贴 low：`{limit_low and d == lo}`，贴 high：`{limit_high and d == hi}`',
        'return res': '这一位及之后的好数共 `{res}` 个',
    },
    max_steps=80,
    cards=dict(
        one_liner='数位 DP：多记一个 pre，填 d 前先看 |d−pre| 是否超过 k',
        complexity='时间 `O(D²·log r)`，空间 `O(D·log r)`，`D = 10`',
        problem=['三个整数 `l, r, k`：相邻数位绝对差都 `≤ k` 的数叫好数，求 `[l, r]` 里好数个数',
                 '示例：`l=10, r=15, k=1` → `3`（10、11、12）',
                 '本视频：`l=9, r=14, k=1` → `4`（9、10、11、12）'],
        quote='本题需要记录上一个填的数字 pre。枚举当前填的数字 d。如果 d 是最高位（之前没有填过数字），或者 |d−pre|≤k，那么可以填 d，继续递归。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `(i, pre, limit_low, limit_high)`：同时受 `l` 下界和 `r` 上界约束',
              '`l` 比 `r` 短时，把 `l` 看成前面补零：前 `diff_lh` 位可以==不填数字==',
              '不填数字等于位数变少，不再受 `r` 约束；v2.1 用 `is_first_num` 代替 `isNum` 参数'],
        summary=['每个状态只算一次：状态数 `O(D·log r)`，每个状态枚举 `O(D)`',
                 '只在 `limit_low` 和 `limit_high` 都为假时记忆化（Python 的 `@cache` 无需操心，贴边状态只出现一次）',
                 '易错点：最高位不看 pre；跳过的位 `pre` 传 0 没有影响',
                 '同类题：1012、3519、3906（数位 DP 上下界模板）'],
    ),
)
