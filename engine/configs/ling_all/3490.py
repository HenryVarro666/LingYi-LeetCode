_I = lambda S: S['_inner'].get('i')


def _LP(S):
    i = S['_inner'].get('i')
    return i - S['diff_lh'] if i is not None and i >= S['diff_lh'] else None


def _state(S):
    I = S['_inner']
    if 'm' not in I:
        return '数位 DP：逐位填，记录 ==数位乘积 m== 和 ==数位之和 s==，最后看 `m % s == 0`'
    lo = '受 low 约束' if I['limit_low'] else 'low 不再约束'
    hi = '受 high 约束' if I['limit_high'] else 'high 不再约束'
    return f"`dfs(i={I['i']})`：乘积 `m = {I['m']}`，数位和 `s = {I['s']}`，{lo}，{hi}"


def _end(S, B, ret):
    I = S['_inner']
    if I['i'] != S.n:
        return f"`i = {I['i']}`，还没填完 {S.n} 位"
    m, s = I['m'], I['s']
    if s and m % s == 0:
        return f"填完了：乘积 `m = {m}`，数位和 `s = {s}`，`m % s == 0` → ==美丽整数，返回 1=="
    if not s:
        return '填完了：什么都没填（`s = 0`），不算数，返回 0'
    return f"填完了：`{m} % {s} = {m % s} ≠ 0` → 不是美丽整数，返回 0"


CONFIG = dict(
    num=3490, title='统计美丽整数的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='上下界数位 DP（乘积、数位和作状态）',
    tags=['灵神题单', '动态规划', '难度分 2502'],
    code='''
class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        low = list(map(int, str(l)))
        high = list(map(int, str(r)))
        n = len(high)
        diff_lh = n - len(low)  # 这样写无需给 low 补前导零，也无需 is_num 参数

        @cache
        def dfs(i: int, m: int, s: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1 if s and m % s == 0 else 0

            lo = low[i - diff_lh] if limit_low and i >= diff_lh else 0
            hi = high[i] if limit_high else 9

            res = 0
            if limit_low and i < diff_lh:
                res += dfs(i + 1, 1, 0, True, False)  # 什么也不填
                d = 1  # 下面循环从 1 开始
            else:
                d = lo
            # 枚举填数字 d
            for d in range(d, hi + 1):
                res += dfs(i + 1, m * d, s + d, limit_low and d == lo, limit_high and d == hi)
            return res

        return dfs(0, 1, 0, True, True)
''',
    call='Solution().beautifulNumbers(8, 12)',
    expect=3,
    skip=['low = list', 'high = list', 'diff_lh =', 'res = 0', 'for d in range', 'else:', 'd = lo', 'd = 1  #'],
    views=[
        dict(type='array', var='high', label='high = r 的数位（蓝箭头 = 当前填第 i 位）', cell=70, h=170,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             color=lambda S, i, v: 'blue' if i == _I(S) else None),
        dict(type='array', var='low', label='low = l 的数位（比 high 短，靠右对齐；箭头指 i − diff_lh）', cell=70, h=170,
             pointers={_LP: 'blue'}, pointer_labels={_LP: 'i'}),
        dict(type='text', fn=_state, size=24, h=70),
        dict(type='calls', h=210),
    ],
    watch=[('i', lambda S: S['_inner'].get('i', '-'), 'blue'),
           ('m 乘积', lambda S: S['_inner'].get('m', '-'), 'yellow'),
           ('s 数位和', lambda S: S['_inner'].get('s', '-'), 'cyan'),
           ('lo', lambda S: S['_inner'].get('lo', '-'), 'pink'),
           ('hi', lambda S: S['_inner'].get('hi', '-'), 'pink')],
    captions={
        'n = len(high)': '`n = {n}`：最多 {n} 位',
        'if i == n': _end,
        'lo = low': '这一位至少填 `lo = {lo}`（受 low 约束时是 low 的这一位，否则 0）',
        'hi = high': '这一位至多填 `hi = {hi}`（受 high 约束时是 high 的这一位，否则 9）',
        'if limit_low and i < diff_lh': lambda S, B, r: ('`low` 比 `high` 短，高位 `i < diff_lh` 还在补的区域 → ==可以什么也不填==（少一位的数）'
                                                          if S['_inner']['limit_low'] and S['_inner']['i'] < S.diff_lh else '没有「不填」的选项，直接枚举 d'),
        'res += dfs(i + 1, 1, 0': '什么也不填：乘积保持 1（乘法单位元），数位和保持 0，==不用 is_num 参数==',
        'res += dfs(i + 1, m * d': '枚举填数字 `d = {d}`：乘积 `m × d`，数位和 `s + d`，再看是否继续受 low / high 约束',
        'return res': '这一层方案数 ==`{ret}`==',
        'return dfs(0': '入口：还没填数字，乘积 1（乘法单位元）、数位和 0（加法单位元），同时受 low 和 high 约束',
    },
    max_steps=54,
    cards=dict(
        one_liner='数位和很小、不同乘积不多，直接把乘积和数位和当状态',
        complexity='时间 `O(n⁶D²)`，空间 `O(n⁶D)`',
        problem=['数位乘积能被数位之和整除的正整数是==美丽整数==',
                 '数出 `[l, r]` 里有多少个美丽整数，`r < 10^9`',
                 '本视频：`l=8, r=12` → `3`（8、9、10）'],
        quote='注意到，数位之和是很小的，最多 9n≤81，所以可以用数位之和作为 DP 的状态之一。注意到，9 个 0 到 9 的数相乘，只有 K(9)=3026 种不同的乘积，所以可以直接用数位乘积作为 DP 的状态之一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, m, s, limit_low, limit_high)`：已填前 i 位，乘积 m，数位和 s',
              '`m` 初始 1，`s` 初始 0；到末尾 `s > 0 且 m % s == 0` 才算',
              'low 比 high 短时，高位可以==什么也不填==，省掉 `is_num`'],
        summary=['时间 `O(n⁶D²)`，空间 `O(n⁶D)`（D=10）',
                 '易错点：什么也不填时 `m=1, s=0`；到末尾要先判 `s != 0` 避免除零',
                 '`lo` / `hi` 取决于是否还受 low / high 约束，`diff_lh` 对齐两者长度',
                 '写法二：算 `[1,r] − [1,l−1]`，把 `dfs` 写在外面用 `memo` 跨测试复用'],
    ),
)
