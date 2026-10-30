R_NAME = {0: '<', 1: '=', 2: '>', 3: '—'}


def _fmt_state(S):
    st = S.get('state')
    if st is None:
        return ''
    r = st // 4
    return f"r={R_NAME[r]}  顶下界={st & 1}  顶上界={(st >> 1) & 1}"


def _text(S):
    if 'level' not in S['_inner'] or 'last_d' not in S['_inner']:
        return '`f` 记波动值，`g` 记数字个数：峰谷对后面所有 `g` 个数各贡献一次'
    I = S['_inner']
    level, last_d, st = I['level'], I['last_d'], I['state']
    r = st // 4
    return (f"第 `{level}` 位：上一位 `{last_d}`，`r` = =={R_NAME[r]}==（0 小于 1 等于 2 大于 — 未定），"
            f"顶下界 `{st & 1}` 顶上界 `{(st >> 1) & 1}`")


def _cap_d(S, B, ret):
    I = S['_inner']
    return (f"枚举这一位填 `d = {I['d']}`（范围 `{I['start']}..{I['end']}`）")


CONFIG = dict(
    num=3753, title='范围内总波动值 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 记忆化（f 记波动值，g 记个数）',
    tags=['灵神题单·动态规划', '难度分 2297'],
    code='''
class Solution(object):
    def totalWaviness(self, num1, num2):
        
        d2 = [int(x) for x in list(str(num2))]
        n = len(d2)
        d1 = [int(x) for x in list(str(num1))]
        d1 = [0] * (n - len(d1)) + d1

        f = [[[None] * 16 for _ in range(10)] for _ in range(n)]
        g = [[[None] * 16 for _ in range(10)] for _ in range(n)]

        def calc(level, last_d, state, f, g):
            if level == n:
                return 0, 1
            
            if f[level][last_d][state] is None:
                f[level][last_d][state] = 0
                g[level][last_d][state] = 0
                
                r = state // 4
                upper = state & 2
                lower = state & 1

                if lower:
                    start = d1[level]
                else:
                    start = 0
                
                if upper:
                    end = d2[level]
                else:
                    end = 9

                for d in range(start, end + 1):
                    nxt_state = 0
                    if lower and d == d1[level]:
                        nxt_state |= 1
                    if upper and d == d2[level]:
                        nxt_state |= 2

                    if r == 3 and last_d == 0:
                        nxt_r = 3
                    elif d < last_d:
                        nxt_r = 0
                    elif d > last_d:
                        nxt_r = 2
                    else:
                        nxt_r = 1
                    
                    if r + nxt_r == 2 and r != 1:
                        delta = 1
                    else:
                        delta = 0

                    df, dg = calc(level + 1, d, nxt_r * 4 + nxt_state, f, g)
                    f[level][last_d][state] += df + delta * dg
                    g[level][last_d][state] += dg
                    
            
            return f[level][last_d][state], g[level][last_d][state]
        
        return calc(0, 0, 15, f, g)[0]
''',
    call='Solution().totalWaviness(120, 121)',
    expect=2,
    skip=['f[level][last_d][state] = 0', 'g[level][last_d][state] = 0', 'upper = state & 2', 'lower = state & 1',
          'nxt_state = 0', 'delta = 0', 'delta = 1', 'd2 = [int', 'd1 = [int', 'd1 = [0]', 'n = len(d2)', 'if lower:', 'if upper:', 'if lower and d', 'if upper and d', 'elif d < last_d', 'elif d > last_d', 'if r == 3 and last_d == 0', 'r = state // 4', 'g[level][last_d][state] += dg', 'f = [[[None]', 'g = [[[None]'],
    views=[
        dict(type='array', var='d1', label='d1（下界 num1 的数位）', h=190, cell=90, pointers={'level': 'blue'}),
        dict(type='array', var='d2', label='d2（上界 num2 的数位）', h=190, cell=90, pointers={'level': 'blue'}),
        dict(type='text', h=70, size=22, fn=_text),
        dict(type='calls', h=200, hide=('f', 'g')),
    ],
    watch=[('level', 'level', 'blue'), ('last_d', 'last_d', 'cyan'), ('state', 'state', 'purple'), ('d', 'd', 'yellow'),
           ('nxt_r', 'nxt_r', 'orange'), ('delta', 'delta', 'pink'), ('df', 'df', 'green'), ('dg', 'dg', 'green')],
    max_steps=90,
    captions={
        'return calc(0, 0, 15': '从第 0 位开始：`last_d = 0`，`state = 15`（二进制 `11 11`：关系未定，顶着下界，顶着上界）',
        'if level == n': lambda S, B, r: ('`level == n`：整个数字填完了，返回 `(0, 1)`：波动值 0（峰谷由上层累加），个数 1'
                                         if S.level == S.n else f'`level = {S.level} < n = {S.n}`：还有位没填'),
        'if f[level][last_d][state] is None': lambda S, B, r: ('这个状态还没算过 → 往下算（算过的会直接用缓存）'
                                                              if S['f'][S.level][S.last_d][S.state] is None else '这个状态算过了 → 直接返回缓存'),
        'r = state // 4': '`r = {r}`：上一位与再上一位的关系（0 小于，1 等于，2 大于，3 还没有）',
        'start = d1[level]': '顶着下界：这一位至少填 `d1[{level}]` = =={start}==',
        'start = 0': '没顶着下界：这一位可以从 0 开始',
        'end = d2[level]': '顶着上界：这一位至多填 `d2[{level}]` = =={end}==',
        'end = 9': '没顶着上界：这一位可以填到 9',
        'for d in range(start, end + 1)': lambda S, B, r: ('这一位 `start..end` 都试完了，把结果返回'
                                                          if 'd' in B['_inner'] and B['_inner'].get('d') == S['_inner'].get('d')
                                                          else f'枚举这一位填 `d = {S.d}`（范围 `{S.start}..{S.end}`）'),
        'if lower and d == d1[level]': lambda S, B, r: ('填的正好是下界这一位 → 下一位仍要顶着下界' if S.lower and S.d == S.d1[S.level]
                                                         else '没顶着下界，或者比下界这一位大 → 下一位不再受下界约束'),
        'nxt_state |= 1': '填的正好是下界这一位 `d = d1[level]` → 下一位仍顶着下界：`nxt_state` = {nxt_state}',
        'if upper and d == d2[level]': lambda S, B, r: ('填的正好是上界这一位 → 下一位仍要顶着上界' if S.upper and S.d == S.d2[S.level]
                                                         else '没顶着上界，或者比上界这一位小 → 下一位不再受上界约束'),
        'nxt_state |= 2': '填的正好是上界这一位 `d = d2[level]` → 下一位仍顶着上界：`nxt_state` = {nxt_state}',
        'nxt_r = 3': '还在最高位 / 前导零：还没有大小关系，`nxt_r = 3`',
        'nxt_r = 0': '`d = {d}` < 上一位 `{last_d}`：下降，`nxt_r = 0`；上一段 `r = {r}`，下一步看是否一升一降',
        'nxt_r = 2': '`d = {d}` > 上一位 `{last_d}`：上升，`nxt_r = 2`；上一段 `r = {r}`',
        'nxt_r = 1': '`d = {d}` = 上一位 `{last_d}`：持平，`nxt_r = 1`',
        'if r == 3 and last_d == 0': lambda S, B, r: ('还在前导零 / 最高位：没有大小关系，`nxt_r = 3`' if S.r == 3 and S.last_d == 0
                                                      else '已经有前一位，可以比较大小'),
        'elif d < last_d': lambda S, B, r: (f'`d = {S.d} < last_d = {S.last_d}` → 下降，`nxt_r = 0`' if S.d < S.last_d else '`d` 不小于上一位'),
        'elif d > last_d': lambda S, B, r: (f'`d = {S.d} > last_d = {S.last_d}` → 上升，`nxt_r = 2`' if S.d > S.last_d else '`d` 等于上一位 → `nxt_r = 1`'),
        'if r + nxt_r == 2 and r != 1': lambda S, B, r: (
            f'`r = {S.r}`，`nxt_r = {S.nxt_r}`：一升一降（和为 2 且 r ≠ 1）→ ==形成峰/谷==，`delta = 1`'
            if S.r + S.nxt_r == 2 and S.r != 1 else f'`r = {S.r}`，`nxt_r = {S.nxt_r}`：不是一升一降 → 没有峰谷，`delta = 0`'),
        'df, dg = calc(': '填 `{d}` 后进入下一位：新状态 `nxt_r × 4 + nxt_state` = {nxt_r * 4 + nxt_state}',
        'f[level][last_d][state] += df': '`f` += `df + delta × dg` = {df} + {delta} × {dg}：峰谷对后面 `dg` 个数各贡献一次；`g` += `dg` 累计个数',
        'return f[level][last_d][state], g': lambda S, B, r: f'这个状态返回 `(f, g)` = ==`{r}`==：波动值之和，数字个数',
        'return 0, 1': '一个完整数字：`(0, 1)`',
    },
    cards=dict(
        result='`f[0][0][15]` = ==2==：`120`、`121` 各有一个峰',
        one_liner='f 记波动值，g 记个数：高位的峰谷对后面所有数各算一次',
        complexity='时间 `O(10·n·10·16)`，空间 `O(n·10·16)`（n = 位数）',
        problem=['波动值 = 数字里峰（比两邻都大）与谷（比两邻都小）的个数',
                 '求 `[num1, num2]` 内所有数的波动值之和，`num2` 最大 `10^15`',
                 '示例：`[120, 130]` → `3`；本视频 `[120, 121]` → `2`'],
        quote='若某个数的高位上出现了一个峰或者谷，那么无论低位如何构成，只要其处于num1到num2，这个数的这个峰或者谷都应该被计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['数位 DP 要同时记两个数组：`f` 是波动值之和，`g` 是数字个数',
              '填到某一位形成峰/谷时，`f` 除了累加子状态的 `f`，还要加上子状态的 `g`',
              '状态 `[level][last_d][state]`：填到第几位、上一位是几、`state` = 与再上一位的关系 + 顶上下界',
              ],
        summary=['记忆化：`f[level][last_d][state]` 不为 `None` 就直接返回',
                 '`r + nxt_r == 2 and r != 1`：上一段上升、这一段下降（或反过来）才是峰谷',
                 '前导零：`r == 3 and last_d == 0` 时关系保持「未定」',
                 '原文为 Python 2 风格，这里无需改动（`//` 本来就是整除）',
                 '对比灵神：灵神用 `(l, m, r)` 三元组公式 `O(log n)`；yiduobo 用 f/g 双数组的数位 DP'],
    ),
)
