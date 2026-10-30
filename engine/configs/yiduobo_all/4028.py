def _ftab(S):
    f = S.get('f')
    if not f:
        return [['']]
    rows = [ord(c) - 97 for c in sorted(set(S['s']))]
    w = max(len(f[i]) for i in rows)
    return [list(f[i]) + [''] * (w - len(f[i])) for i in rows]


def _frows(S):
    return sorted(set(S['s']))


def _fcols(S):
    f = S.get('f')
    return list(range(max(len(r) for r in f))) if f else [0]


def _gval(S):
    g = S.get('g')
    return list(g) if isinstance(g, list) else []


def _top(S):
    if 'm' not in S:
        return '`s = "' + S['s'] + '"`：要找「旋转几次 + 改字母」总代价最小的方案'
    if 'p' not in S:
        return f"`n = {S['n']}`，卷积长度要 `>= 2n-1 = {2*S['n']-1}`，所以 `m = {S['m']}`（2 的幂）"
    return f"模数 `p = {S['p']}`（=3×2^18+1），变换长度 `m = {S['m']}`"


CONFIG = dict(
    num=4028, title='得到旋转回文字符串的最少操作次数 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='按下标和归类代价 + NTT 卷积', tags=[],
    code='''
class Solution(object):
    def minOperations(self, s):

        def quick_power(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            x = quick_power(base, p >> 1, mod)
            x = x * x % mod
            if p & 1:
                x = x * base % mod
            return x

        n = len(s)
        f = [[0] * n for _ in range(26)]

        for index, c in enumerate(s):
            f[ord(c) - 97][index] = 1

        m = 1
        while m < n * 2 - 1:
            m <<= 1
        
        p = 3 * (1 << 18) + 1
        g = 10
        w = quick_power(g, (p - 1) // m, p)
        w_list = [1]
        for _ in range(m - 1):
            w_list.append(w_list[-1] * w % p)

        rw = w_list[-1]
        rw_list = [1]
        for _ in range(m - 1):
            rw_list.append(rw_list[-1] * rw % p)

        def ntt(f, m, w_list, mod):
            f.extend([0] * (m - len(f)))
            for index in range(m):
                v = index
                b = m >> 1
                x = 0
                while v:
                    if v & 1:
                        x |= b
                    b >>= 1
                    v >>= 1
                
                if index < x:
                    f[index], f[x] = f[x], f[index]
            
            length = 2
            while length <= m:
                for part in range(m // length):
                    for index in range(length // 2):
                        left = part * length + index
                        right = part * length + index + length // 2
                        u = f[left]
                        v = f[right] * w_list[m // length * index] % mod
                        f[left] = u + v
                        if f[left] >= mod:
                            f[left] -= mod
                        f[right] = u - v
                        if f[right] < 0:
                            f[right] += mod
                length <<= 1

        for x in range(26):
            ntt(f[x], m, w_list, p)

        g = [0] * m
        for x in range(26):
            for y in range(x + 1, 26):
                dis = abs(x - y)
                for index in range(m):
                    g[index] += min(dis, 26 - dis) * f[x][index] % p * f[y][index] % p
                    if g[index] >= p:
                        g[index] -= p

        ntt(g, m, rw_list, p)
        rm = p - (p - 1) // m
        for index in range(m):
            g[index] = g[index] * rm % p
        for index in range(n, m):
            g[index % n] += g[index]

        res = g[n - 1]
        for r in range(1, n):
            res = min(res, r + g[(r * 2 - 1) % n])
        return res
''',
    call='Solution().minOperations("aabc")',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='table', var=_ftab, rows=_frows, cols=_fcols, label='f[字母]：01 数组（做完 NTT 后变成点值）', h=260, cell=104),
        dict(type='array', var=_gval, label='g：按「下标和 mod n」归类的代价和', h=200, cell=110),
    ],
    watch=['n', 'm', ('ω', 'w', 'cyan'), ('res', 'res', 'green')],
    skip=list(range(4, 15)) + [19, 23, 28, 29, 30, 31, 34, 35, 36] + list(range(38, 68)) + [69, 70] + list(range(73, 80)) + [83, 84, 85, 86],
    max_steps=60,
    max_events=80000,
    captions={
        'n = len(s)': '`n = {n}`，字符串长度',
        'f = [[0]': '为每个字母 `c` 建一个长度 n 的 01 数组 `f[c]`：`s[i] = c` 就在第 i 位放 1',
        'f[ord(c) - 97][index] = 1': '`s[{index}] = "{c}"` → `f["{c}"][{index}] = 1`，位置变成了连续的数组',
        'm <<= 1': '两个长度 n 的多项式相乘，结果长度 `2n-1 = {2*n-1}`，`m` 取不小于它的 2 的幂 → {m}',
        'p = 3': 'NTT 用模数 `p = 3×2^18+1 = {p}`（素数），它的原根是 10',
        'g = 10': '`g = 10` 是 p 的原根（后面 `g` 会被重新用作代价数组）',
        'rw = w_list[-1]': '单位根 `ω = 10^((p-1)/m) mod p = {w}`，m 次幂回到 1；`w_list` 是 ω 的各次幂。`ω^(m-1)` 就是 ω 的逆元 `rw = {rw}`，逆变换要用它',
        'g = [0] * m': '每个出现的字母都做完 NTT：`f` 变成了「点值」（表里的数）。现在准备代价数组 `g`',
        'ntt(g, m, rw_list, p)': '所有字母对 `(x, y)` 的代价 `min(dis, 26-dis)` 乘上点值累加进 `g`，一共 325 对：点值相乘 = 卷积。这一步用 `rw_list` 做逆变换，还原出「下标和」数组',
        'rm = p - (p - 1) // m': '逆变换后每项多乘了 m，要乘 m 的逆元 `rm = {rm}`；`index >= n` 的项折回 `index % n`',
        'res = g[n - 1]': '`g[i]` 就是所有「下标和 mod n = i」的字符对的代价和：`g[:n] = {g[:n]}`。r = 0 时 `(2×0−1) % n = n−1`，`res = g[{n-1}] = {res}`',
        'res = min(res': '左旋 `{r}` 次：代价 `{r} + g[(2×{r}−1) % {n}] = {r} + {g[(r*2-1)%n]}` = {r + g[(r*2-1)%n]}，`res = min({B.res}, …)` = =={res}==',
        'return res': '最少操作次数 `{res}`',
    },
    cards=dict(
        one_liner='先把每对字符的代价按「下标和 mod n」收集好，再枚举旋转次数',
        complexity='时间 `O(26·n·log n + 325·n)`，空间 `O(26·n)`',
        problem=['字符串 `s`（长度 ≤ 50000），可任意次：某位字母 +1（z 后是 a）、左旋一位',
                 '求让 `s` 变成回文的最少操作次数',
                 '本视频用 `s = "aabc"`，答案 `2`（左旋 1 次，再把 b 变 c）'],
        quote='对于确定下来的旋转次数r，接下来需要计算的就是所有下标和对n取模等于(r * 2 - 1) % n的下标对。',
        quote_src='—— yiduobo 题解原文',
        idea=['左旋 r 次后，回文配对的两个字符原下标之和 mod n 恒为 `(2r-1) % n`',
              '所以先统计 `g[k]`：下标和 mod n = k 的所有字符对的代价之和，答案 = `min(r + g[(2r-1)%n])`',
              '字母只有 26 种：每种字母建 01 数组，字母对之间用多项式乘法，NTT 免去浮点误差'],
        after=[dict(heading='NTT 在这里做什么', lines=['两个 01 数组的卷积：第 k 项 = 满足 `i + j = k` 的 `(f[a][i], f[b][j])` 个数', '做 NTT 把数组变成点值，点值逐项相乘，再逆变换得到卷积', '模数 `p = 3×2^18+1`，原根 10，全程整数运算', '视频里 NTT 内部的蝶形循环太长，已快进，只看每个阶段的结果'])],
        summary=['时间 `O(26·n·log n + 325·n)`，空间 `O(26·n)`',
                 '`m` 要不小于 `2n-1`，否则卷积结果会绕回，下标和对不上',
                 '逆变换后要乘 `m` 的逆元，并把 `index >= n` 的项折回 `index % n`',
                 '字母对只有 `26×25/2 = 325` 种，相同字母代价 0，不用算',
                 '本视频只演示 n=4（m=8）的小例子，NTT 蝶形循环已快进；代码是 Python 3 写法，未改动'],
    ),
)
