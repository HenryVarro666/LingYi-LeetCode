from math import gcd

NUMS = [1, 1, 2]
MA = max(NUMS)
HDR = lambda S: [str(k) for k in range(MA + 1)]


def _gtxt(S):
    f, s = S.get('first'), S.get('second')
    ln = S['_line']
    if f is None or s is None or 'seq_pair' not in S or not (27 <= ln <= 45) or 'final_pair' in S:
        return '`g[a][b]`：seq1 全是 a 的倍数、seq2 全是 b 的倍数、互不相交的方案数（gcd 只要求是倍数）'
    if ln < 37:
        return f'`g[{f}][{s}]`：先数 3 类元素：两边都是倍数 / 只是 {f} 的倍数 / 只是 {s} 的倍数'
    x, y, z = S['lcm_cnt'], S['mul'][f] - S['lcm_cnt'], S['mul'][s] - S['lcm_cnt']
    return f'`g[{f}][{s}] = 3^{x} × 2^{y} × 2^{z} − 2^{x+z} − 2^{x+y} + 1`（x、y、z = {x}、{y}、{z}）'


def _gcolor(S, i, j, v):
    if S['_line'] >= 44 or S.get('first') is None:
        return None
    return 'green' if v else None


def _fcolor(S, i, j, v):
    return 'green' if v and i == j else ('blue' if v else None)


CONFIG = dict(
    num=3336, title='最大公约数相等的子序列数量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='倍数计数 + 倒序容斥（沿用 3312 的思路）',
    tags=['多维 DP', '数学算法', '难度分 2403'],
    code='''
class Solution(object):
    def subsequencePairCount(self, nums):
        
        ma = max(nums)
        cnt = [0] * (ma + 1)
        for v in nums:
            cnt[v] += 1
        
        mul = [0] * (ma + 1)
        for v in range(1, ma + 1):
            for x in range(v, ma + 1, v):
                mul[v] += cnt[x]

        pow3 = [1]
        pow2 = [1]
        mod = 10 ** 9 + 7
        for index in range(1, max(mul) + 1):
            pow3.append(pow3[-1] * 3 % mod)
            pow2.append(pow2[-1] * 2 % mod)

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        seq_pair = [[0] * (ma + 1) for _ in range(ma + 1)]
        for first in range(1, ma + 1):
            for second in range(1, ma + 1):
                if mul[first] == 0 or mul[second] == 0:
                    continue
                lcm = first * second // gcd(first, second)
                if lcm <= ma:
                    lcm_cnt = mul[lcm]
                else:
                    lcm_cnt = 0

                seq_pair[first][second] = pow3[lcm_cnt] * pow2[mul[first] - lcm_cnt] % mod * pow2[mul[second] - lcm_cnt] % mod
                seq_pair[first][second] -= pow2[mul[first]]
                if seq_pair[first][second] < 0:
                    seq_pair[first][second] += mod
                seq_pair[first][second] -= pow2[mul[second]]
                if seq_pair[first][second] < 0:
                    seq_pair[first][second] += mod
                seq_pair[first][second] += 1
                if seq_pair[first][second] >= mod:
                    seq_pair[first][second] -= mod

        final_pair = [[0] * (ma + 1) for _ in range(ma + 1)]
        for s in range(ma + ma, 1, -1):
            for first in range(ma, 0, -1):
                second = s - first
                if second <= 0 or second > ma or seq_pair[first][second] == 0:
                    continue
                final_pair[first][second] = seq_pair[first][second]
                for x in range(first, ma + 1, first):
                    for y in range(second, ma + 1, second):
                        if x > first or y > second:
                            final_pair[first][second] -= final_pair[x][y]
                            if final_pair[first][second] < 0:
                                final_pair[first][second] += mod

        res = 0
        for v in range(1, ma + 1):
            res += final_pair[v][v]
            if res >= mod:
                res -= mod
        return res
''',
    call=f'Solution().subsequencePairCount({NUMS})',
    expect=6,
    skip=['pow3.append', 'pow2.append', 'for index in range', 'pow3 = [1]', 'pow2 = [1]', 'mod = 10',
          'x, y = y, x % y', 'while y:', 'return x', 'def gcd', 'for x in range(v', 'for v in nums', 'for v in range',
          'for first in range', 'for second in range', 'for s in range', 'for y in range', 'if mul[first] == 0',
          'if lcm <= ma', 'lcm_cnt = mul[lcm]', 'lcm_cnt = 0', 'else:', 'if seq_pair[first][second] < 0',
          'if seq_pair[first][second] >= mod', 'seq_pair[first][second] += mod', 'seq_pair[first][second] -= mod',
          'final_pair[first][second] += mod', 'if final_pair[first][second] < 0', 'if res >= mod', 'res -= mod',
          'res += final_pair[v][v]', 'second = s - first', 'continue', 'if second <= 0 or', 'if x > first or y > second',
          'for x in range(first'],
    views=[
        dict(type='array', var='mul', label='mul[v]：nums = [1, 1, 2] 中 v 的倍数的个数', cell=70, h=140),
        dict(type='text', fn=_gtxt, size=22, h=90),
        dict(type='table', var='seq_pair', label='g（seq_pair）', cell=90, h=250, rows=HDR, cols=HDR,
             cursors=[('first', 'second', 'yellow')], color=_gcolor),
        dict(type='table', var='final_pair', label='f（final_pair）：gcd 恰好是 (行, 列)', cell=90, h=250, rows=HDR, cols=HDR,
             cursors=[('first', 'second', 'yellow')], color=_fcolor),
    ],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'pink'), ('lcm', 'lcm', 'cyan'), ('lcm_cnt', 'lcm_cnt', 'orange'),
           ('res', 'res', 'green')],
    captions={
        'ma = max(nums)': '`ma = {ma}`：gcd 的取值不会超过最大元素',
        'cnt[v] += 1': '数出每个值的个数：`cnt[{v}] = {cnt[v]}`',
        'mul[v] += cnt[x]': '`mul[{v}] += cnt[{x}]` → {mul[v]}：筛法，从 v 开始每次加 v，累计 ==v 的倍数个数==',
        'lcm = first': lambda S, B, r: (f'`first = {B.first}`，`second = {B.second}`：两边都能放的数，是 `lcm = {B.first * B.second // gcd(B.first, B.second)}` 的倍数'
                                        f'；`mul[{B.first}] = {B.mul[B.first]}`，`mul[{B.second}] = {B.mul[B.second]}`'),
        'seq_pair[first][second] = pow3': lambda S, B, r: (
            f'三类元素：两边都行 `{S.lcm_cnt}` 个 → 3 种选法；只能放 seq1 `{S.mul[S.first] - S.lcm_cnt}` 个、只能放 seq2 `{S.mul[S.second] - S.lcm_cnt}` 个 → 各 2 种'
            f' → `3^{S.lcm_cnt} × 2^{S.mul[S.first] - S.lcm_cnt} × 2^{S.mul[S.second] - S.lcm_cnt}`'),
        'seq_pair[first][second] -= pow2[mul[first]]': '减去 seq2 为空的方案：全部放进 seq1，`2^{mul[first]}` 种',
        'seq_pair[first][second] -= pow2[mul[second]]': '减去 seq1 为空的方案：全部放进 seq2，`2^{mul[second]}` 种',
        'seq_pair[first][second] += 1': '两个都空的方案被减了两次，==加回 1== → 取模后 `g[{first}][{second}] = {seq_pair[first][second] % mod}`',
        'final_pair = [[0]': '`g` 里的 gcd 只是「倍数」；现在从大到小容斥，求出 gcd ==恰好==是 (first, second) 的方案',
        'final_pair[first][second] = seq_pair': '`s = {s}`：按 `first+second` 从大到小处理，更大的格子已算好。`f[{first}][{second}]` 先取 `g` = {seq_pair[first][second]}，再减去 gcd 更大的格子',
        'final_pair[first][second] -= final_pair[x][y]': '减去 `f[{x}][{y}] = {final_pair[x][y]}`：它的 gcd 是 `({x}, {y})`，不是恰好 `({first}, {second})` → `f[{first}][{second}] = {final_pair[first][second]}`',
        'res = 0': '`res` 累加所有 gcd 相等的格子 `f[v][v]`',
        'return res': '一共 `{res}` 对',
    },
    max_steps=90,
    cards=dict(
        one_liner='先算倍数版 g，再从大到小减掉更大的 gcd，得到恰好版 f',
        complexity='时间 `O(U^2 · (U/a)(U/b))`，空间 `O(U^2)`',
        problem=['`nums` 里选两个==不相交==的非空子序列，要求两者 gcd 相等',
                 '数有多少对 `(seq1, seq2)`，答案对 `10^9+7` 取模',
                 '本视频：`[1, 1, 2]` → `6`'],
        quote='先计算由值为first的倍数的元素构成seq1，由值为second的倍数的元素构成seq2，且seq1和seq2不相交的序列对的数目g[first][second]，然后用g[first][second]减去f[first * 2][second]……之后，得到的就是f[first][second]。',
        quote_src='—— yiduobo 题解原文',
        idea=['gcd 难直接数，就从「倍数」入手：先数 `g[a][b]`（seq1 全是 a 的倍数，seq2 全是 b 的倍数）',
              '元素分三类：两边都行（3 选）、只能放一边（2 选）；再扣掉空序列：`3^x·2^y·2^z − …+ 1`',
              '`g` 里混着 gcd 更大的情况，按 `first+second` 从大到小，把更大的 `f` 减掉',
              '最后把 `f[v][v]` 加起来'],
        summary=['`mul[v]` 用筛法累加，不用对每个 `v` 扫整个数组',
                 '易错：空序列要扣掉；「两个都空」被扣两次，要加回 1',
                 '易错：容斥的遍历顺序必须让更大的格子先算好',
                 '原文已是可在 Python 3 运行的写法，无需改动',
                 '对比灵神：灵神先写 `dfs(i, j, k)` 选或不选；这里直接做倍数计数 + 容斥'],
    ),
)
