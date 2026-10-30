_E = "index % n if match is not None else None"


def _info(S):
    if 'match' not in S:
        return '`nxt[i]`：`t[:i+1]` 的最长相等真前后缀（KMP 失配时回退）；`p` = 当前已匹配的长度'
    if 'final' in S or 'res' in S or 'base' in S and S.get('_line', 0) >= 36:
        return '`match` 个位置能把 `s` 变成 `t`；转移矩阵 `base = [[match-1, n-match], [match, n-1-match]]`，求 `base^k`'
    return f"在循环 s 里用 KMP 数 `t` 出现的位置：目前 `match = {S.get('match', 0)}`"


CONFIG = dict(
    num=2851, title='字符串转换', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='KMP 数匹配位置 + f/g 两状态矩阵快速幂',
    tags=['难度分 2858'],
    code='''
class Solution(object):
    def numberOfWays(self, s, t, k):

        nxt = [0]
        n = len(s)
        p = 0
        for index in range(1, n):
            while p and t[p] != t[index]:
                p = nxt[p - 1]
            if t[p] == t[index]:
                p += 1
            nxt.append(p)
        
        match = 0
        p = 0
        for index in range(n + n - 1):
            while p > 0 and t[p] != s[index % n]:
                p = nxt[p - 1]
            if t[p] == s[index % n]:
                p += 1
            if p == n:
                match += 1
                p = nxt[p - 1]
        
        if s == t:
            f, g = 1, 0
        else:
            f, g = 0, 1
        
        #for i in range(k):
        #    f, g = f * (match - 1) + g * match, f * (n - match) + g * (n - 1 - match)
        mod = 10 ** 9 + 7
        base = [[match - 1, n - match], [match, n - 1 - match]]

        def matMul(a, b):
            c = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        c[i][j] += a[i][k] * b[k][j]
                        c[i][j] %= mod
            return c

        def quickPow(base, k):
            if k == 1:
                return base[:]
            
            res = quickPow(base, k // 2)
            res = matMul(res, res)

            if k % 2 == 1:
                res = matMul(res, base)
            
            return res

        final = quickPow(base, k)
        return (f * final[0][0] + g * final[1][0]) % mod
''',
    call='Solution().numberOfWays("abcd", "cdab", 5)',
    expect=61,
    skip=['c = [[0, 0], [0, 0]]', 'for i in range(2)', 'for j in range(2)', 'for k in range(2)', 'c[i][j]', 'return c'],
    max_steps=80,
    views=[
        dict(type='text', fn=_info, size=21, h=80),
        dict(type='string', var='t', label='t（粉 = 已匹配长度 p，下一个要比较的位置）', h=170, cell=60, pointers={'p': 'pink'}),
        dict(type='string', var='s', label='s（蓝 = 当前读到的位置 index % n，循环扫描）', h=170, cell=60,
             pointers={_E: 'blue'}, pointer_labels={_E: 'index'}),
        dict(type='array', var=lambda S: S.get('nxt') or [], label='nxt（前缀函数）', h=170, cell=60),
        dict(type='table', var=lambda S: S.get('res') or S.get('base') or [[0, 0], [0, 0]], label='res / base（先是 base，之后每层平方）', h=150, cell=70),
    ],
    watch=[('p', 'p', 'pink'), ('match', 'match', 'green'), ('k', 'k', 'blue')],
    captions={
        'nxt = [0]': '`nxt[0] = 0`：单个字符没有真前后缀',
        'n = len(s)': '`n = {n}`：每次操作有 `n - 1` 种选法',
        'p = 0': '`p` 是当前已匹配的长度',
        'for index in range(1, n)': lambda S, B, r: ('对 `t` 本身算前缀函数，`index` 从 1 开始' if S.index != B.get('index') else '`nxt` 算完了'),
        'while p and t[p] != t[index]': lambda S, B, r: (f'`t[{S.p}] = {S.t[S.p]} ≠ t[{S.index}] = {S.t[S.index]}` → ==失配，回退== `p = nxt[p-1]`' if S.p and S.t[S.p] != S.t[S.index]
                                                         else '`p = 0` 或能接上 → 不用回退'),
        'p = nxt[p - 1]': '`p` 回退到 `{p}`',
        'if t[p] == t[index]': lambda S, B, r: (f'`t[{S.p}] = t[{S.index}]` → 匹配长度 +1' if S.t[S.p] == S.t[S.index] else f'`t[{S.p}] ≠ t[{S.index}]` → `p` 保持'),
        'p += 1': '`p` = {p}',
        'nxt.append(p)': '`nxt` 末尾加入 `{p}`',
        'match = 0': '`match` 数 `t` 在循环 `s` 里出现的位置数（`s` 接成两倍，少最后一个字符）',
        'for index in range(n + n - 1)': lambda S, B, r: ('把 `s` 当作环：`index` 走 `2n - 1` 步，取 `index % n`' if S.index != B.get('index') else '走完 `2n - 1` 步，`match` 统计完毕'),
        'while p > 0 and t[p] != s[index % n]': lambda S, B, r: (f'`t[{S.p}] = {S.t[S.p]} ≠ s[{S.index % S.n}] = {S.s[S.index % S.n]}` → ==失配，回退==' if S.p > 0 and S.t[S.p] != S.s[S.index % S.n]
                                                                else '没有失配 → 不用回退'),
        'if t[p] == s[index % n]': lambda S, B, r: (f'`t[{S.p}] = s[{S.index % S.n}]` → 匹配长度 +1' if S.t[S.p] == S.s[S.index % S.n] else f'`t[{S.p}] ≠ s[{S.index % S.n}]` → 接不上'),
        'if p == n': lambda S, B, r: ('`p = n` → ==整个 t 匹配上了== 一次' if S.p == S.n else f'`p = {S.p}` 还没匹配完'),
        'match += 1': '`match` = {match}：又找到一个循环移位等于 `t`',
        'p = nxt[p - 1]': '`p` 回退到 `{p}`',
        'f, g = 1, 0': '`s == t`：初始“等于 t”的方案数 `f = 1`，`g = 0`',
        'f, g = 0, 1': '`s != t`：初始 `f = 0`，`g = 1`',
        'mod = ': '答案对 `10^9 + 7` 取模',
        'base = [[': '`base = [[match-1, n-match], [match, n-1-match]]`，`match = {match}`：“等于 t”保持有 `match-1` 种（不能不动）',
        'final = quickPow': '`final = base^k`，`k` 最大 `10^15`，用递归快速幂',
        'if k == 1': lambda S, B, r: ('`k = 1`：递归到底，`base^1` 就是 `base`' if S.k == 1 else f'`k = {S.k}`：继续对半拆'),
        'return base[:]': '返回 `base` 的拷贝',
        'res = quickPow': '先递归求 `base^(k//2)`',
        'res = matMul(res, res)': '平方：得到 `base^(2·(k//2))`',
        'if k % 2 == 1': lambda S, B, r: ('`k` 是奇数 → 平方后还差一个 `base`' if S.k % 2 else '`k` 是偶数 → 够了'),
        'res = matMul(res, base)': '补乘一个 `base`',
        'return res': '返回 `base^k`',
        'return (f *': '`f·final[0][0] + g·final[1][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='先用 KMP 数出能变成 t 的位置数，再把 f/g 转移写成 2×2 矩阵',
        complexity='时间 `O(n + log k)`，空间 `O(n + log k)`',
        problem=['每次操作：把 `s` 长为 `l`（`0 < l < n`）的后缀移到开头；求恰好 `k` 次把 `s` 变成 `t` 的方案数',
                 '`n` 最大 `5×10^5`，`k` 最大 `10^15`，答案对 `10^9+7` 取模',
                 '本视频：`s = "abcd", t = "cdab", k = 5` → `61`'],
        quote='对于循环字符串的问题通常是原样复制一份拼在后面，那么在这里就可以先利用kmp算法计算出t在循环s中所有的匹配位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`match` = `t` 在循环 `s` 里的匹配位置数（KMP），每个位置对应一种后缀长度',
              '当前是 `t`：保持为 `t` 有 `match-1` 种（不能不动），变成非 `t` 有 `n-match` 种',
              '当前不是 `t`：变成 `t` 有 `match` 种，仍非 `t` 有 `n-1-match` 种 → 2×2 矩阵，`base^k`'],
        summary=['时间 `O(n + log k)`，空间 `O(n)` + 递归栈 `O(log k)`',
                 '易错：循环扫描只走 `2n - 1` 步，否则会多数一次整圈；`s == t` 时初始状态不同',
                 '`f` / `g` 的列向量乘法顺序：答案 = `f·final[0][0] + g·final[1][0]`',
                 '原文为 Python 2 写法，`quickPow` 里的 `k / 2` 已改为 `k // 2`',
                 '对比灵神：灵神先拼接 `s + s[:-1]` 再用封装好的 KMP 数匹配，思路相同']
    ),
)
