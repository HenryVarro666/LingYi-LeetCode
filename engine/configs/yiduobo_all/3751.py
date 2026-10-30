def _st(S):
    if 'state' not in S or 'level' not in S:
        return ''
    r, up, lo = S['state'] // 4, S['state'] & 2, S['state'] & 1
    rn = {0: '最后一位 < 前一位', 1: '相等', 2: '最后一位 > 前一位', 3: '还没有大小关系（前导 0 / 最高位）'}[r]
    return f"level={S['level']}  last_d={S['last_d']}  r={r}（{rn}）  顶着上界：{'是' if up else '否'}  顶着下界：{'是' if lo else '否'}"


def _tight(S, i, v, key):
    if 'level' not in S or 'state' not in S:
        return None
    if i == S['level']:
        return 'blue'
    return None



CONFIG = dict(
    num=3751, title='范围内总波动值 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='数位 DP（f 记波动值，g 记个数）',
    tags=['数位 DP'],
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
    call='Solution().totalWaviness(120, 122)',
    expect=2,
    skip=['nxt_state = 0', 'nxt_state |= ', 'f[level][last_d][state] = 0', 'g[level][last_d][state] = 0', 'upper = state', 'lower = state',
          'start = ', 'end = ', 'nxt_r = ', 'delta = ', 'elif d < last_d', 'elif d > last_d', 'else:', 'if lower and d ==', 'if upper and d ==', 'g[level][last_d][state] +='],
    max_steps=110,
    views=[
        dict(type='array', var='d1', label='d1（num1 的数位）', h=140, cell=80, color=lambda S, i, v: 'blue' if S.get('level') == i else None),
        dict(type='array', var='d2', label='d2（num2 的数位）', h=140, cell=80, color=lambda S, i, v: 'blue' if S.get('level') == i else None),
        dict(type='text', size=22, h=60, fn=_st),
        dict(type='calls', h=200, hide=('f', 'g')),
    ],
    watch=['level', 'last_d', 'state', 'r', 'start', 'end', ('d', 'd', 'yellow'), 'nxt_r', ('delta', 'delta', 'orange'), ('df', 'df', 'blue'), ('dg', 'dg', 'pink')],
    captions={
        'd2 = [': '`d2` 是 num2 的各位数字：`{d2}`',
        'n = len': '位数 `n = {n}`',
        'd1 = [int': '`d1` 是 num1 的各位数字：`{d1}`',
        'd1 = [0]': '`d1` 前面补 0 到和 `d2` 等长：`{d1}`',
        'f = [[[None]': '`f` 记波动值之和，初值 None 表示还没算（记忆化）',
        'g = [[[None]': '`g` 记满足范围的数的个数',
        'if level == n': lambda S, B, r: ('`level == n`：数位填完了，这一条路径算 1 个数，波动值 0' if S.level == S.n else f'`level = {S.level} < n = {S.n}`：还没填完，往下算'),
        'if f[level][last_d][state] is None': '状态 `({level}, {last_d}, {state})` 还没算过 → 开始枚举这一位（算过的会直接复用）',
        'r = state // 4': lambda S, B, r: f"`r = {S.r}`：{['最后一位比前一位小', '最后一位与前一位相等', '最后一位比前一位大', '还没有大小关系（前导 0 或最高位）'][S.r]}",
        'if lower:': lambda S, B, r: (f'==顶着下界==：这一位从 `d1[{S.level}] = {S.d1[S.level]}` 起，不能再小' if S.lower else '没顶着下界：这一位从 0 起'),
        'if upper:': lambda S, B, r: (f"==顶着上界==：这一位到 `d2[{S.level}] = {S.d2[S.level]}` 止，不能再大（范围 {S.d1[S.level] if S.lower else 0}~{S.d2[S.level]}）" if S.upper else f"没顶着上界：这一位最多 9（范围 {S.d1[S.level] if S.lower else 0}~9）"),
        'for d in range': lambda S, B, r: ('这一位的所有填法都枚举完了 → 返回这个状态的结果' if B.get('dg') is not None and B.get('d') == S.d else f'这一位填 `d = {S.d}`'),
        'if lower and d == d1[level]': lambda S, B, r: ('这一位正好等于下界数位 → 下一位仍顶着下界（`nxt_state` 最低位置 1）' if S.lower and S.d == S.d1[S.level] else '没有继续顶着下界'),
        'if upper and d == d2[level]': lambda S, B, r: ('这一位正好等于上界数位 → 下一位仍顶着上界（`nxt_state` 次低位置 1）' if S.upper and S.d == S.d2[S.level] else '没有继续顶着上界'),
        'if r == 3 and last_d == 0': lambda S, B, r: (
            '前导 0 / 最高位：还不能比较大小，`nxt_r = 3`' if S.r == 3 and S.last_d == 0 else
            f'比较 `d = {S.d}` 与 `last_d = {S.last_d}`：' + ('更小，`nxt_r = 0`' if S.d < S.last_d else '更大，`nxt_r = 2`' if S.d > S.last_d else '相等，`nxt_r = 1`')),
        'if r + nxt_r == 2 and r != 1': lambda S, B, r: (f'`r = {S.r}`，`nxt_r = {S.nxt_r}`：先升后降或先降后升 → ==形成峰或谷==，`delta = 1`' if S.r + S.nxt_r == 2 and S.r != 1 else f'`r = {S.r}`，`nxt_r = {S.nxt_r}`：没有形成峰或谷，`delta = 0`'),
        'df, dg = calc': '递归算下一位：`df` = 后面的波动总和，`dg` = 后面合法的数的个数',
        'f[level][last_d][state] +=': '`f += df + delta × dg` = `{df} + {delta} × {dg}` → =={f[level][last_d][state]}==（峰/谷对后面 `dg` 个数都算一次）；`g` 同样加上 `dg`',
        'g[level][last_d][state] +=': '`g += dg` → {g[level][last_d][state]}',
        'return f[level]': '这个状态的结果：波动值 `{ret[0]}`，个数 `{ret[1]}`',
        'return calc(0, 0, 15': '从最高位开始 `calc(0, 0, 15)`：状态 15 = 还没有大小关系 + 顶着上下界；返回 `f[0][0][15]` 即答案',
    },
    cards=dict(
        one_liner='f 记波动值之和，g 记个数：峰谷对其后所有数都有贡献',
        complexity='时间约 `O(位数 × 10 × 16 × 10)`，空间 `O(位数 × 10 × 16)`',
        problem=['数字的波动值 = 峰和谷的个数（严格大于/小于两侧相邻数位，首尾不算）',
                 '求闭区间 `[num1, num2]` 内所有数字的波动值之和',
                 '示例：`[120, 130]` → `120`、`121`、`130` 各 1 → `3`',
                 '数据范围小时可暴力，yiduobo 给出能通吃 II（`10^15`）的数位 DP'],
        quote='除了将f[nxt_state]和g[nxt_state]分别累加到f[state]和g[state]之外，还需要将g[nxt_state]累加到f[state]中，表示这个峰或者谷，在后续所有的g[nxt_state]个数中都需要被计入答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['按位填数，状态 = 位置 + 最后一位 + (与前一位的大小关系 r，顶上界，顶下界)',
              '`r` 取 0/1/2/3：小于/等于/大于/还没有关系（前导 0）',
              '`r + nxt_r == 2 且 r != 1` 即 (0,2) 或 (2,0)：形成了峰或谷',
              '用 `f[level][last_d][state]` 记忆化，`g` 统计后续合法数的个数'],
        summary=['时间 `O(位数 × 10 × 16 × 10)`，空间 `O(位数 × 10 × 16)`',
                 '易错：峰/谷要乘上后面所有数的个数 `dg`，而不是只加 1',
                 '`d1` 前面补 0 与 `d2` 等长，前导 0 靠 `r = 3` 排除，不会误算峰谷',
                 '本题 `num2 <= 10^5` 其实可以暴力；此做法同样适用于 II（`10^15`）',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串，其余无需改动'],
    ),
)
