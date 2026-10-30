_I = lambda S: S['_inner'].get('i') if S['_line'] <= 14 else None


def _state(S):
    I = S['_inner']
    if 'left1' in I and S['_line'] <= 14:
        lim = '==贴着 s 的上界==（这一位最多填 s[i]）' if I['is_limit'] else '已经比 s 小，这一位随便填 0/1'
        return f"`dfs(i={I['i']}, left1={I['left1']})`：还要放 {I['left1']} 个 1，{lim}"
    if 'i' in I and 'f' in S:
        return f"枚举 `i = {I['i']}`：`f[{I['i']}] = {S['f'][I['i']]}`（`i` 约简到 1 的次数）" + ('，==≤ k，数它== ' if S['f'][I['i']] <= S['k'] else '，超过 k，不数')
    return '数位 DP：数 `[1, s)` 里恰好有 `i` 个 1 的二进制数，`i` 满足 `f[i] ≤ k`'


CONFIG = dict(
    num=3352, title='统计小于 N 的 K 可约简整数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='f*(x) 递推 + 数位 DP 数恰好 i 个 1',
    tags=['灵神题单', '动态规划', '难度分 2451'],
    code='''
class Solution:
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        MOD = 1_000_000_007
        n = len(s)

        @cache
        def dfs(i: int, left1: int, is_limit: bool) -> int:
            if i == n:
                return 0 if is_limit or left1 else 1
            up = int(s[i]) if is_limit else 1
            res = 0
            for d in range(min(up, left1) + 1):
                res += dfs(i + 1, left1 - d, is_limit and d == up)
            return res % MOD

        ans = 0
        f = [0] * n
        for i in range(1, n):
            f[i] = f[i.bit_count()] + 1
            if f[i] <= k:
                # 计算有多少个二进制数恰好有 i 个 1
                ans += dfs(0, i, True)
        dfs.cache_clear()  # 防止爆内存
        return ans % MOD
''',
    call="Solution().countKReducibleNumbers('1000', 2)",
    expect=6,
    skip=['MOD =', 'res = 0', 'for d in range', 'dfs.cache_clear'],
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 当前填第 i 位）', cell=80, h=210,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             color=lambda S, i, v: 'blue' if i == _I(S) else None),
        dict(type='array', var='f', label='f[x]：x 约简到 1 的最少次数', cell=80, h=170,
             pointers={lambda S: S['_inner'].get('i') if S['_line'] > 14 else None: 'pink'},
             pointer_labels={lambda S: S['_inner'].get('i') if S['_line'] > 14 else None: 'i'}),
        dict(type='text', fn=_state, size=24, h=70),
        dict(type='calls', h=200),
    ],
    watch=[('i', lambda S: S['_inner'].get('i', '-'), 'blue'),
           ('left1', lambda S: S['_inner'].get('left1', '-'), 'yellow'),
           ('is_limit', lambda S: S['_inner'].get('is_limit', '-'), 'pink'),
           ('ans', 'ans', 'green')],
    captions={
        'n = len(s)': '`n = {n}`：`s` 有 {n} 位，所以 `[1, s)` 里的数最多有 {n - 1} 个 1',
        'if i == n': lambda S, B, r: (('填完了：' + ('仍贴着上界 → 等于 s，不是「小于 s」，返回 0' if S['_inner']['is_limit'] else
                                      ('还剩 1 没放完 → 个数不对，返回 0' if S['_inner']['left1'] else '1 恰好用完，且比 s 小 → ==返回 1==')))
                                      if S['_inner']['i'] == S.n else f"`i = {S['_inner']['i']}`，还没填完 {S.n} 位"),
        'up = int': lambda S, B, r: f"这一位最多填 `up = {S['_inner']['up']}`：贴着上界就是 `s[i]`，否则可以填到 1",
        'res += dfs': '逐个尝试这一位填 0 还是 1，交给下一位继续填。==d 最多到 min(up, left1)：1 不够放就不能再填 1==',
        'return res % MOD': '这一层试完，方案数 ==`{ret}`==（记得取模）',
        'f = [0] * n': '`f[x]` = x 约简到 1 的最少次数；`f[0]` 不会用到，`f[1]` 记为 1',
        'for i in range(1, n)': lambda S, B, r: f"枚举「1 的个数」`i = {S['_inner']['i']}`（`s` 有 {S.n} 位，不可能有 {S.n} 个 1）",
        'f[i] = f[i.bit_count()]': '`f[{i}] = f[popcount({i})] + 1 = f[{i.bit_count()}] + 1` = =={f[i]}==：先变成 1 的个数，再多一次操作',
        'if f[i] <= k': lambda S, B, r: (f"`f[{S['_inner']['i']}] = {S.f[S['_inner']['i']]} ≤ k = {S.k}` → 任何恰好有 {S['_inner']['i']} 个 1 的数都满足，去数它们"
                                         if S.f[S['_inner']['i']] <= S.k else f"`f[{S['_inner']['i']}] = {S.f[S['_inner']['i']]} > k = {S.k}` → 超过 k 次，不数"),
        'ans += dfs': '数 `[1, s)` 里恰好有 `{B.i}` 个 1 的数：交给 dfs，从最高位开始填，一开始贴着上界',
        'return ans % MOD': '答案 ==`{ans % MOD}`==',
    },
    max_steps=52,
    cards=dict(
        one_liner='先约简一次，再数「恰好有 i 个 1」的二进制数',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['二进制字符串 `s` 表示 `n`；一次操作把 `x` 变成它二进制里 1 的个数',
                 '最多 `k` 次操作能变成 1 的数叫 ==k-可约简==，数出 `[1, n)` 里有多少个，结果取模',
                 '本视频：`s="1000", k=2` → `6`（1 到 6）'],
        quote='对于满足 f*(x) ≤ k 的所有 x，我们需要计算，[1,s) 中有多少个二进制数，恰好有 x 个 1？这些恰好有 x 个 1 的二进制数，满足 f*(x) ≤ k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f*(x) = f*(f(x)) + 1`：线性递推出前 `n` 个 `f`',
              '`f[i] ≤ k` 的 `i`：数恰好有 i 个 1 的数',
              '数位 DP：`left1` 剩几个 1，`is_limit` 是否贴着 `s`'],
        summary=['时间 `O(n²)`，空间 `O(n²)`',
                 '易错点：严格小于 `s`，所以 `i == n` 时 `is_limit` 为真要返回 0',
                 '定义 `f[1] = 1` 后，条件直接写 `f[i] <= k`；不需要 `is_num`，前导零不影响 1 的个数',
                 '用完 `dfs.cache_clear()` 防止爆内存'],
    ),
)
