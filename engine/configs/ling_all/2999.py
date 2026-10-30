def _ph(S):
    i = S['_inner'].get('i')
    return i if isinstance(i, int) and i < len(S['high']) else None


def _info(S):
    I = S['_inner']
    if 'limit_low' not in I:
        return '把 `start` 补前导零，和 `finish` 对齐，逐位构造：前缀自由，后缀固定为 `s`'
    part = '==前缀位：自由填 0~limit==' if I['i'] < S['diff'] else '==后缀位：只能填 s 对应数字=='
    return (f"第 `{I['i']}` 位：{part}\n"
            f"贴下界 `{I['limit_low']}` · 贴上界 `{I['limit_high']}`")


CONFIG = dict(
    num=2999, title='统计强大整数的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='上下界数位 DP · 前缀自由 + 后缀固定',
    tags=['灵神题单', '数位 DP', '难度分 2351'],
    code='''
class Solution:
    def numberOfPowerfulInt(self, start: int, finish: int, limit: int, s: str) -> int:
        high = list(map(int, str(finish)))  # 避免在 dfs 中频繁调用 int()
        n = len(high)
        low = list(map(int, str(start).zfill(n)))  # 补前导零，和 high 对齐
        diff = n - len(s)

        @cache
        def dfs(i: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1

            # 第 i 个数位可以从 lo 枚举到 hi
            # 如果对数位还有其它约束，应当只在下面的 for 循环做限制，不应修改 lo 或 hi
            lo = low[i] if limit_low else 0
            hi = high[i] if limit_high else 9

            res = 0
            if i < diff:  # 枚举这个数位填什么
                for d in range(lo, min(hi, limit) + 1):
                    res += dfs(i + 1, limit_low and d == lo, limit_high and d == hi)
            else:  # 这个数位只能填 s[i-diff]
                x = int(s[i - diff])
                if lo <= x <= hi:  # 题目保证 x <= limit，无需判断
                    res = dfs(i + 1, limit_low and x == lo, limit_high and x == hi)
            return res

        return dfs(0, True, True)
''',
    call='Solution().numberOfPowerfulInt(15, 215, 6, "10")',
    expect=2,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='array', var='high', label='finish = 215 的数位（蓝箭头 = 第 i 位）', pointers={_ph: 'blue'},
             pointer_labels={_ph: 'i'}, cell=70, h=190),
        dict(type='array', var='low', label='start = 15，补前导零对齐', pointers={_ph: 'pink'},
             pointer_labels={_ph: 'i'}, cell=70, h=190),
        dict(type='calls', h=230),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('lo', "_inner.get('lo')", 'cyan'), ('hi', "_inner.get('hi')", 'cyan'),
           ('diff', 'diff', 'orange'), ('res', "_inner.get('res')", 'green')],
    skip=[4, 18],
    max_steps=60,
    captions={
        'high = list': '`finish` 拆成数位 `high = {high}`，`n = {len(high)}` 位',
        'low = list': '`start` 补前导零成 `{low}`：这样两个数位一一对齐',
        'diff = n': '`diff = n - len(s) = {diff}`：前 `diff` 位是自由前缀，后面是固定后缀 `s`',
        'if i == n': lambda S, B, r: ('`i = n`：数位全部构造完成' if S['_inner']['i'] == S.n else '还有数位要填，继续'),
        'return 1': '成功构造出一个合法数字 → ==返回 1==',
        'lo = low[i]': '下界约束：`limit_low = {limit_low}` 时至少填 `low[i]`，否则至少 0 → `lo = {lo}`',
        'hi = high[i]': '上界约束：`limit_high = {limit_high}` 时至多填 `high[i]`，否则至多 9 → `hi = {hi}`',
        'if i < diff': lambda S, B, r: (f'`i = {S.i} < diff = {S.diff}`：这是前缀位，可以自由填' if S.i < S.diff
                                        else f'`i = {S.i} ≥ diff = {S.diff}`：这是后缀位，只能填 `s` 里对应的数字'),
        'for d in range': '枚举 `d`：范围 `[lo, min(hi, limit)]` = `[{lo}, {min(hi, limit)}]`——`limit` 只在循环里限制，==不能改 hi==',
        'res += dfs': '填 `d = {d}`：只有 `d` 恰好等于边界才继续贴边界',
        'x = int': '后缀位必须填 `s[{i - diff}]`，即 `x = {x}`',
        'if lo <= x <= hi': lambda S, B, r: (f'`{S.lo} ≤ {S.x} ≤ {S.hi}` → ==成立，可以填 x==' if S.lo <= S.x <= S.hi
                                             else f'`x = {S.x}` 超出 `[{S.lo}, {S.hi}]` → ==这条路走不通，方案数 0=='),
        'res = dfs(i + 1, limit_low and x': '填 `x = {x}`，继续往下一位构造',
        'return res': '这一层合法方案数 `res = {res}`，返回上一层',
        'return dfs(0': '入口：从最高位开始，同时受 `start` 和 `finish` 约束',
    },
    cards=dict(
        one_liner='前缀位自由填 0~limit，后缀位只能是 s，上下界数位 DP',
        complexity='时间 `O(nD)`，空间 `O(n)`',
        problem=['正整数 `x` 以字符串 `s` 结尾，且每个数位都 `≤ limit`，称为强大整数',
                 '求 `[start, finish]` 内强大整数的个数',
                 '示例：`start=15, finish=215, limit=6, s="10"` → `2`（110 和 210）'],
        quote='如果 i < n - |s|，那么可以填 [lo, min(hi, limit)] 内的数，否则只能填 s[i-(n-|s|)]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, limit_low, limit_high)`：构造第 `i` 位及之后的合法方案数',
              '`low`、`high` 数位对齐；前 `diff` 位自由，后 `|s|` 位固定',
              '`limit` 只能在 for 循环里卡范围，不能写成 `hi = min(hi, limit)`，否则贴上界的判断会错'],
        summary=['时间 `O(nD)`，`n` 是 `finish` 的位数，`D = 10`',
                 '答疑：只记忆化 `i` 也可以，因为受约束的状态只会递归访问一次',
                 '易错点：`limit_high and d == hi` 里 `hi` 必须是真正的上界，不能被 `limit` 截断',
                 '`start` 要补前导零和 `finish` 对齐'],
    ),
)
