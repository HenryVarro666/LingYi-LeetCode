_I = lambda S: S['_inner'].get('i') if S['_line'] <= 21 else None
_P = lambda S: S['_inner'].get('i') if S['_line'] > 21 else None


def _state(S):
    I = S['_inner']
    if 'left1' in I and S['_line'] <= 21:
        lim = '==贴着 n 的上界==（这一位最多填 n 的这一位）' if I['is_limit'] else '已经比 n 小，这一位随便填 0/1'
        return f"`dfs(i={I['i']}, left1={I['left1']})`：还要放 {I['left1']} 个 1，{lim}"
    if 'i' in I and 'f' in S and I['i'] < len(S['f']):
        return f"枚举 1 的个数 `i = {I['i']}`：`f[{I['i']}] = {S['f'][I['i']]}`（深度），目标 `k = {S['k']}`"
    return '`n` 的二进制是 `s`：数 `[1, n]` 里恰好有 `i` 个 1 且 `f[i] == k` 的数'


CONFIG = dict(
    num=3621, title='位计数深度为 K 的整数数目 I', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='同 3352：f 递推 + 数位 DP 数恰好 i 个 1',
    tags=['灵神题单', '动态规划', '难度分 3352'],
    code='''
class Solution:
    def popcountDepth(self, n: int, k: int) -> int:
        if k == 0:
            return 1

        # 注：也可以不转成字符串，下面 dfs 用位运算取出 n 的第 i 位
        # 但转成字符串的通用性更好
        s = list(map(int, bin(n)[2:]))
        m = len(s)
        if k == 1:
            return m - 1

        @cache
        def dfs(i: int, left1: int, is_limit: bool) -> int:
            if i == m:
                return 0 if left1 else 1
            up = s[i] if is_limit else 1
            res = 0
            for d in range(min(up, left1) + 1):
                res += dfs(i + 1, left1 - d, is_limit and d == up)
            return res

        ans = 0
        f = [0] * (m + 1)
        for i in range(1, m + 1):
            f[i] = f[i.bit_count()] + 1
            if f[i] == k:
                # 计算有多少个二进制数恰好有 i 个 1
                ans += dfs(0, i, True)
        return ans
''',
    call='Solution().popcountDepth(6, 2)',
    expect=3,
    skip=['res = 0', 'for d in range', 'if k == 0', 'return 1', 'if k == 1', 'return m - 1'],
    views=[
        dict(type='array', var='s', label='s = n 的二进制数位（蓝箭头 = 当前填第 i 位）', cell=80, h=210,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             color=lambda S, i, v: 'blue' if i == _I(S) else None),
        dict(type='array', var='f', label='f[x]：x 的 popcount-depth（f[1] = 1）', cell=80, h=170,
             pointers={_P: 'pink'}, pointer_labels={_P: 'i'}),
        dict(type='text', fn=_state, size=24, h=70),
        dict(type='calls', h=200),
    ],
    watch=[('i', lambda S: S['_inner'].get('i', '-'), 'blue'),
           ('left1', lambda S: S['_inner'].get('left1', '-'), 'yellow'),
           ('is_limit', lambda S: S['_inner'].get('is_limit', '-'), 'pink'),
           ('ans', 'ans', 'green')],
    captions={
        's = list': '`n = 6` 的二进制 `110`，拆成数位 `{s}`',
        'm = len(s)': '`m = {m}`：`n` 有 {m} 位，所以 `[1, n]` 里的数最多有 {m} 个 1',
        'if i == m': lambda S, B, r: (('填完了：' + ('1 还没放完 → 个数不对，返回 0' if S['_inner']['left1'] else '1 恰好用完 → ==返回 1==（本题 ≤ n，贴着上界也算）'))
                                      if S['_inner']['i'] == S.m else f"`i = {S['_inner']['i']}`，还没填完 {S.m} 位"),
        'up = s[i]': lambda S, B, r: f"这一位最多填 `up = {S['_inner']['up']}`：贴着上界就是 `n` 的这一位，否则可以填到 1",
        'res += dfs': '逐个尝试这一位填 0 还是 1，交给下一位继续。==d 最多到 min(up, left1)：1 不够放就不能再填 1==',
        'return res': '这一层试完，方案数 ==`{ret}`==',
        'ans = 0': '`ans` 累计满足条件的数的个数',
        'f = [0]': '`f[x]` = x 的 popcount-depth；`f[1]` 记为 1（和 3352 一样把 1 也算一次）',
        'for i in range(1, m + 1)': lambda S, B, r: f"枚举「1 的个数」`i = {S['_inner']['i']}`（本题 ≤ n，所以 1 的个数最多 {S.m}）",
        'f[i] = f[i.bit_count()]': '`f[{i}] = f[popcount({i})] + 1 = f[{i.bit_count()}] + 1` = =={f[i]}==',
        'if f[i] == k': lambda S, B, r: (f"`f[{S['_inner']['i']}] = {S.f[S['_inner']['i']]} == k = {S.k}`：==恰好等于 k==（3352 是 ≤ k）→ 去数恰好有 {S['_inner']['i']} 个 1 的数"
                                         if S.f[S['_inner']['i']] == S.k else f"`f[{S['_inner']['i']}] = {S.f[S['_inner']['i']]} ≠ k = {S.k}` → 不数"),
        'ans += dfs': '数 `[1, n]` 里恰好有 `{B.i}` 个 1 的数：交给 dfs，从最高位开始填，一开始贴着上界',
        'return ans': '答案 ==`{ans}`==',
    },
    max_steps=56,
    cards=dict(
        one_liner='和 3352 几乎一样：数恰好 i 个 1 的数，条件改成 f[i] == k',
        complexity='时间 `O(log² n)`，空间 `O(log² n)`',
        problem=['`popcount-depth`：不断取二进制 1 的个数，变成 1 所需的最少次数',
                 '数出 `[1, n]` 里深度==恰好==等于 `k` 的整数个数',
                 '本视频：`n=6, k=2` → `3`（3、5、6）'],
        quote='本题和 3352. 统计小于 N 的 K 可约简整数 几乎一样。如果 k=0，那么只有 x=1 满足要求，返回 1。如果 k=1，那么只有 x=2^1,2^2,…,2^(m-1) 满足要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k = 0` 只有 1；`k = 1` 只有 2 的幂，共 `m - 1` 个',
              '`k ≥ 2`：对 `f[i] == k` 的 `i`，数恰好有 i 个 1 的数',
              '对比 3352：小于改成小于等于，≤ k 改成恰好 k，不用取模'],
        summary=['时间 `O(log² n)`，空间 `O(log² n)`',
                 '`k = 0`、`k = 1` 要特判：`f[1] = 1` 的约定会让 `x = 1` 混进 `k = 1`',
                 '`i == m` 时不判断 `is_limit`：本题含 `n` 自己',
                 '`f` 要开到 `m`，因为 1 的个数最多是 `m`'],
    ),
)
