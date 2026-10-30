_ST = {0: '至多填了一个数', 1: '严格递增', 2: '严格递减', 3: '不是好数'}


def _ptr_hi(S):
    i = S['_inner'].get('i')
    return i if isinstance(i, int) and i < len(S['high_s']) else None


def _ptr_lo(S):
    i = S['_inner'].get('i')
    if not isinstance(i, int):
        return None
    j = i - S['diff_lh']
    return j if 0 <= j < len(S['low_s']) else None


def _info(S):
    I = S['_inner']
    if 'state' not in I:
        return '数位 DP：逐位填数，同时记录数位和、上一位、递增/递减状态'
    return (f"第 `{I['i']}` 位 · 状态 =={I['state']} {_ST[I['state']]}==\n"
            f"贴下界 `{I['limit_low']}` · 贴上界 `{I['limit_high']}`")


CONFIG = dict(
    num=3869, title='统计区间内奇妙数的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='上下界数位 DP · 数位和 + 单调状态',
    tags=['灵神题单', '数位 DP', '难度分 2255'],
    code='''
class Solution:
    # 判断数位和 s 是否为好数
    def is_good(self, s: int) -> bool:
        if s < 100:  # s 是个位数或者两位数
            return s // 10 != s % 10  # 十位和个位不相等即为好数
        # s 是三位数，其百位一定是 1
        return 1 < s // 10 % 10 < s % 10  # 只能严格递增

    def countFancy(self, l: int, r: int) -> int:
        STATE_INIT = 0      # 已经填了至多一个数（不含前导零）
        STATE_INC = 1       # 已填数字是严格递增的
        STATE_DEC = 2       # 已填数字是严格递减的
        STATE_NOT_GOOD = 3  # 已填数字不是好数

        low_s = list(map(int, str(l)))  # 避免在 dfs 中频繁调用 int()
        high_s = list(map(int, str(r)))
        n = len(high_s)
        diff_lh = n - len(low_s)

        @cache
        def dfs(i: int, digit_sum: int, prev: int, state: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1 if state != STATE_NOT_GOOD or self.is_good(digit_sum) else 0

            lo = low_s[i - diff_lh] if limit_low and i >= diff_lh else 0
            hi = high_s[i] if limit_high else 9

            res = 0
            start = lo

            # 通过 limit_low 和 i 可以判断能否不填数字，无需 is_num 参数
            if limit_low and i < diff_lh:
                # 不填数字，上界不受约束
                res = dfs(i + 1, 0, 0, STATE_INIT, True, False)
                start = 1  # 下面填数字，从 1 开始填

            for d in range(start, hi + 1):
                new_state = state
                if state == STATE_INIT:
                    if prev > 0:  # 之前填过数
                        if d > prev:
                            new_state = STATE_INC
                        elif d < prev:
                            new_state = STATE_DEC
                        else:
                            new_state = STATE_NOT_GOOD
                elif state == STATE_INC:
                    if d <= prev:
                        new_state = STATE_NOT_GOOD
                elif state == STATE_DEC:
                    if d >= prev:
                        new_state = STATE_NOT_GOOD

                res += dfs(i + 1,
                           digit_sum + d,
                           d,
                           new_state,
                           limit_low and d == lo,
                           limit_high and d == hi)

            return res

        return dfs(0, 0, 0, STATE_INIT, True, True)
''',
    call='Solution().countFancy(8, 12)',
    expect=5,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='array', var='high_s', label='上界 r = 12 的数位（蓝箭头 = 当前填第 i 位）', pointers={_ptr_hi: 'blue'},
             pointer_labels={_ptr_hi: 'i'}, cell=70, h=205),
        dict(type='array', var='low_s', label='下界 l = 8 的数位（右对齐，j = i-diff_lh）', pointers={_ptr_lo: 'pink'},
             pointer_labels={_ptr_lo: 'j'}, cell=70, h=205),
        dict(type='calls', h=230),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('digit_sum', "_inner.get('digit_sum')", 'orange'),
           ('prev', "_inner.get('prev')", 'pink'), ('state', "_inner.get('state')", 'purple'),
           ('lo', "_inner.get('lo')", 'cyan'), ('hi', "_inner.get('hi')", 'cyan'), ('res', "_inner.get('res')", 'green')],
    skip=[10, 11, 12, 13, 28, 29, 38, 55, 56, 57, 58, 59],
    max_steps=46,
    captions={
        'if i == n': lambda S, B, r: (f'`i = n`：所有数位都填完了' if S['_inner']['i'] == S.n else '`i < n`，还有数位要填，继续'),
        'return 1 if state': lambda S, B, r: (
            f"数位和 `{S.digit_sum}`，状态 `{S.state}`（{_ST[S.state]}）："
            + ('数字本身是好数 → ==奇妙数，返回 1==' if S.state != 3
               else ('数字不是好数，但数位和是好数 → ==奇妙数，返回 1==' if r == 1 else '数字和数位和都不是好数 → 返回 0'))),
        'lo = low_s': '下界约束：`limit_low = {limit_low}` 时这位至少填 `low_s` 对应位，否则从 0 起 → `lo = {lo}`',
        'hi = high_s': '上界约束：`limit_high = {limit_high}` 时这位至多填 `high_s[i]`，否则至多 9 → `hi = {hi}`',
        'res = dfs(i + 1, 0, 0': '`l` 比 `r` 短，高位可以不填数字：往后递归时上界不再约束，数位和、上一位、状态都重置为 0',
        'start = 1': '下面要填数字了，首位不能是前导零 → 从 1 开始填',
        'for d in range': '枚举这一位填 `d`，范围 `[{start}, {hi}]`',
        'new_state = STATE_NOT_GOOD': '`d` 和上一位相等或违反递增/递减 → 状态变为 ==3（不是好数）==',
        'new_state = STATE_INC': '`d = {d}` > `prev = {prev}` → 状态 1，严格递增',
        'new_state = STATE_DEC': '`d = {d}` < `prev = {prev}` → 状态 2，严格递减',
        'if prev > 0': '`prev = {prev}`：非零说明之前填过数；为 0 表示这是第一个数，状态保持 0',
        'res += dfs': '填 `d = {d}`：数位和 += d，`prev = d`，两个约束只在 `d` 恰好等于边界时才继续保留',
        'return res': '这一层方案数 `res = {res}`，返回给上一层',
        'return dfs(0': '入口：从最高位开始，数位和、上一位、状态都是 0，同时受 `l` 和 `r` 约束',
    },
    cards=dict(
        one_liner='上下界数位 DP，额外记录数位和、上一位和单调状态',
        complexity='时间 `O(D² log² r)`，空间 `O(D log² r)`',
        problem=['数位严格递增或严格递减的数是好数；数本身或数位和是好数 → 奇妙数',
                 '统计 `[l, r]` 内奇妙数的个数，`r ≤ 10^15`',
                 '本视频：`l = 8, r = 12` → `5`（8、9、10、11、12 都是奇妙数）'],
        quote='`state` 表示已填数字的状态：0 表示已经填了至多一个数（不含前导零），1 表示严格递增，2 表示严格递减，3 表示不是好数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['在上下界数位 DP 模板上加三个参数：`digit_sum`、`prev`、`state`',
              '`state` 是一个小自动机：0 → 1/2/3，1 或 2 一旦被破坏就掉到 3',
              '边界：`state != 3`（数本身是好数）或数位和是好数 → 返回 1'],
        summary=['时间 `O(D² log² r)`，`D = 10`；状态数约 `D log² r`',
                 '数位和最多 `9 × 15 = 135`，好数判断只需看两位、三位（百位必为 1）',
                 '易错点：`prev = 0` 才表示没填过数，所以前导零要靠 `limit_low` 和 `i < diff_lh` 判断',
                 '`lo`、`hi` 只由上下界决定，额外约束只放在循环里'],
    ),
)
