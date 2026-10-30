_L = lambda S: S['_inner'].get('level') if S['_line'] in (22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42) else None


def _state(S):
    I = S['_inner']
    if 'level' in I and 'rest_one' in I:
        fl = '==等于 s 的前缀==' if I['flag'] else '已经 ==小于 s 的前缀=='
        return f"`g[level={I['level']}][rest_one={I['rest_one']}][flag={I['flag']}]`：还要放 {I['rest_one']} 个 1，{fl}"
    if 'one' in I and 'f' in S and I['one'] < len(S['f']):
        return f"枚举 1 的个数 `one = {I['one']}`：`f[{I['one']}] = {S['f'][I['one']]}`，`f[one] + 1 = {S['f'][I['one']] + 1}`（`k = {S['k']}`）"
    return '先算 `f[one]`，再数「恰好 one 个 1、且小于 n」的数'


CONFIG = dict(
    num=3352, title='统计小于 N 的 K 可约简整数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='预处理 f[one] + 记忆化数位 DP（flag 表示是否等于前缀）',
    tags=['灵神题单', '动态规划', '难度分 2451'],
    code='''
class Solution(object):
    def countKReducibleNumbers(self, s, k):
        
        m = len(s)
        f = [0, 0]
        for v in range(2, m + 1):
            x = v
            one = 0
            while x:
                x -= x & -x
                one += 1
            f.append(f[one] + 1)
        
        g = [[[None] * 2 for _ in range(m + 1)] for _ in range(m)]
        res = 0
        mod = 10 ** 9 + 7

        def dfs(level, rest_one, flag, g):
            if level == m:
                if rest_one == 0 and flag == 0:
                    return 1
                return 0

            if g[level][rest_one][flag] is None:
                g[level][rest_one][flag] = 0
                if rest_one > 0:
                    if not flag:
                        g[level][rest_one][flag] += dfs(level + 1, rest_one - 1, flag, g)
                        g[level][rest_one][flag] %= mod
                    elif s[level] == '1':
                        g[level][rest_one][flag] += dfs(level + 1, rest_one - 1, flag, g)
                        g[level][rest_one][flag] %= mod
                
                if flag and s[level] == '0':
                    g[level][rest_one][flag] += dfs(level + 1, rest_one, flag, g)
                    g[level][rest_one][flag] %= mod
                else:
                    g[level][rest_one][flag] += dfs(level + 1, rest_one, 0, g)
                    g[level][rest_one][flag] %= mod
            
            return g[level][rest_one][flag]

        for one in range(1, m + 1):
            if f[one] + 1 <= k:
                res = (res + dfs(1, one - 1, 1, g) + dfs(1, one, 0, g)) % mod
        
        return res
''',
    call="Solution().countKReducibleNumbers('1000', 2)",
    expect=6,
    skip=['x = v', 'one = 0', 'x -= x & -x', 'g = [[[', 'res = 0', 'mod = ', 'g[level][rest_one][flag] = 0',
          '%= mod', 'for v in range', 'while x'],
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 正在填第 level 位）', cell=80, h=210,
             pointers={_L: 'blue'}, pointer_labels={_L: 'level'},
             color=lambda S, i, v: 'blue' if i == _L(S) else None),
        dict(type='array', var='f', label='f[one]：把 one 约简到 1 需要的操作数', cell=80, h=170),
        dict(type='text', fn=_state, size=24, h=70),
        dict(type='calls', h=210, hide=('g',)),
    ],
    watch=[('one', lambda S: S.get('one', '-'), 'cyan'),
           ('level', lambda S: S['_inner'].get('level', '-'), 'blue'),
           ('rest_one', lambda S: S['_inner'].get('rest_one', '-'), 'yellow'),
           ('flag', lambda S: S['_inner'].get('flag', '-'), 'pink'),
           ('res', 'res', 'green')],
    captions={
        'm = len(s)': '`m = {m}`：`s` 有 {m} 位，1 到 n 的数经一次操作都变成 1 到 {m} 之间的数',
        'f = [0, 0]': '`f[one]`：把 `one` 约简到 1 的操作数，`f[0]`、`f[1]` 都是 0',
        'f.append': '`one` 是 `{v}` 的二进制里 1 的个数 = `{one}`，所以 `f[{v}] = f[{one}] + 1 =` =={f[v]}==',
        'for one in range': lambda S, B, r: (f"枚举「一次操作后变成的数」`one = {S['_inner']['one']}`" if S['_inner']['one'] <= S.m else '枚举结束'),
        'if f[one] + 1 <= k': lambda S, B, r: (f"`f[{S['_inner']['one']}] + 1 = {S.f[S['_inner']['one']] + 1} ≤ k = {S.k}`：所有恰好有 {S['_inner']['one']} 个 1 的数，总操作数都 ≤ k → 去数"
                                               if S.f[S['_inner']['one']] + 1 <= S.k else
                                               f"`f[{S['_inner']['one']}] + 1 = {S.f[S['_inner']['one']] + 1} > k = {S.k}` → 超过 k 次，不数"),
        'res = (res + dfs': '最高位填 1：`dfs(1, one-1, 1)`，填 0：`dfs(1, one, 0)`。两部分相加，累计进 `res`',
        'if level == m': lambda S, B, r: (f"填满 {S.m} 位：`rest_one = {S['_inner']['rest_one']}`，`flag = {S['_inner']['flag']}` → " +
                                          ('1 恰好用完且小于 s，==算 1 种==' if S['_inner']['rest_one'] == 0 and S['_inner']['flag'] == 0
                                           else '1 没用完，或和 s 相等（要求小于 s），算 0 种'))
                                         if S['_inner']['level'] == S.m else f"`level = {S['_inner']['level']}`，还没填满",
        'if g[level][rest_one][flag] is None': '备忘录：这个状态没算过才往下算，算过直接返回结果',
        'if rest_one > 0': lambda S, B, r: ('还有 1 要放，可以考虑在这一位填 1' if S['_inner']['rest_one'] > 0 else '1 已经放完了，这一位只能填 0'),
        'if not flag': '`flag = 0`：前缀已经小于 s，这一位随便填 1',
        "elif s[level] == '1'": lambda S, B, r: (f"`flag = 1`（前缀等于 s）且 `s[{S['_inner']['level']}] = 1`：可以填 1，前缀依然等于 s"
                                                 if S.s[S['_inner']['level']] == '1' else
                                                 f"`flag = 1` 且 `s[{S['_inner']['level']}] = 0`：填 1 就比 s 大，不行"),
        'dfs(level + 1, rest_one - 1': '这一位填 1：还剩 `rest_one - 1` 个 1，交给下一位',
        "if flag and s[level] == '0'": '这一位填 0：前缀等于 s 且 `s[level]` 是 0，填 0 后依然等于 s',
        'dfs(level + 1, rest_one, flag': '这一位填 0，`flag` 保持（前缀仍等于 s）',
        'dfs(level + 1, rest_one, 0': '其他情况填 0 后前缀必然小于 s，`flag` 变成 0',
        'return g[level]': '这个状态的方案数 ==`{ret}`==',
        'return res': '答案 ==`{res}`==',
    },
    max_steps=52,
    cards=dict(
        one_liner='一次操作后数变小，先预处理 f，再用数位 DP 数「恰好 one 个 1」',
        complexity='时间 `O(m²)`，空间 `O(m²)`',
        problem=['二进制串 `s` 表示 `n`；一次操作把 `x` 变成它二进制里 1 的个数',
                 '最多 `k` 次能变成 1 的数是 ==k 可约简数==，数出小于 `n` 的个数（取模）',
                 '本视频：`s="1000", k=2` → `6`'],
        quote='s的长度可以达到800位，也就是说n最多是一个800位的二进制数，暴力枚举显然是不行的，必须从数位上先办法解决。……可以反过来思考',
        quote_src='—— yiduobo 题解原文',
        idea=['任何数一次操作后落在 `1..m`：先算好 `f[one]`',
              '`f[one] + 1 ≤ k`：恰好有 `one` 个 1 的数都算',
              '`g[level][rest_one][flag]`：flag 记前缀是否等于 s'],
        summary=['时间 `O(m²)`，空间 `O(m²)`',
                 '`flag = 1` 才受 `s` 的限制；到末尾要 `flag == 0`，保证严格小于 `n`',
                 '统计的是 `dfs(1, one-1, 1)`（最高位填 1）加 `dfs(1, one, 0)`（最高位填 0）',
                 '原文已是 Python 3 可运行的写法，代码未做修改',
                 '对比灵神：灵神用 `@cache` + `bit_count`，yiduobo 手写备忘录 `g` 并用 `x & -x` 数 1'],
    ),
)
