def _kmp(S):
    return 'pi' in S or 'text' in S


def _text(S):
    if not _kmp(S):
        return S.get('s') or ''
    return S['text'] if 'match_cnt' in S else S['s']


def _pat(S):
    if not _kmp(S):
        return S.get('t') or ''
    return S['pattern'] if 'match_cnt' in S else S['s']


def _info(S):
    ln = S.get('_line', 0)
    if 'text' in S:
        return f"在 `s + s[:-1]` 里数 `t` 出现几次（KMP）：已找到 `match_cnt = {S.get('match_cnt', 0)}` 个循环同构"
    if 'pi' in S and 'text' not in S and ln < 38:
        return '`pi[i]`：模式串 `t[:i+1]` 的最长相等真前后缀长度（KMP 失配时回退用）'
    if 'n' in S and S.get('res') is not None:
        return f"`res` = M 的若干次幂；剩余次数 `k = {S.get('n')}`"
    return '`f0 = 操作后等于 t`，`f1 = 不等于 t`；`c` = s 的循环同构里等于 t 的个数；`M = [[c-1, c], [n-c, n-1-c]]`'


CONFIG = dict(
    num=2851, title='字符串转换', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='KMP 数循环同构 + 2×2 矩阵快速幂',
    tags=['难度分 2858'],
    code='''
class Solution:
    def numberOfWays(self, s, t, k):
        n = len(s)
        c = self.kmp_search(s + s[:-1], t)
        m = [
            [c - 1, c],
            [n - c, n - 1 - c]
        ]
        m = self.pow(m, k)
        return m[0][s != t]

    # KMP 模板
    def calc_pi(self, s: str) -> List[int]:
        pi = [0] * len(s)
        c = 0
        for i in range(1, len(s)):
            v = s[i]
            while c and s[c] != v:
                c = pi[c - 1]
            if s[c] == v:
                c += 1
            pi[i] = c
        return pi

    # KMP 模板
    # 返回 text 中出现了多少次 pattern（允许 pattern 重叠）
    def kmp_search(self, text: str, pattern: str) -> int:
        pi = self.calc_pi(pattern)
        match_cnt = c = 0
        for i, v in enumerate(text):
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            if c == len(pattern):
                match_cnt += 1
                c = pi[c - 1]
        return match_cnt

    # 矩阵乘法
    def multiply(self, a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        c = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                c[i][j] = (a[i][0] * b[0][j] + a[i][1] * b[1][j]) % 1_000_000_007
        return c

    # 矩阵快速幂
    def pow(self, a: List[List[int]], n: int) -> List[List[int]]:
        res = [[1, 0], [0, 1]]
        while n:
            if n % 2:
                res = self.multiply(res, a)
            a = self.multiply(a, a)
            n //= 2
        return res
''',
    call='Solution().numberOfWays("abcd", "cdab", 5)',
    expect=61,
    skip=['c = [[0, 0], [0, 0]]', 'for i in range(2)', 'for j in range(2)', 'c[i][j] =', 'return c', 'v = s[i]', 'm = [', '[c - 1, c],', '[n - c, n - 1 - c]', ']\n'],
    max_steps=80,
    views=[
        dict(type='text', fn=_info, size=21, h=80),
        dict(type='string', var=_text, label='被扫描的字符串（蓝 = 当前读到的位置 i）', h=170, cell=60, pointers={'i': 'blue'}),
        dict(type='string', var=_pat, label='模式串 t（粉 = 已匹配长度 c，下一个要比较的位置）', h=170, cell=60, pointers={'c if pi is not None else None': 'pink'}, pointer_labels={'c if pi is not None else None': 'c'}),
        dict(type='array', var=lambda S: S.get('pi') or [], label='pi（前缀函数）', h=130, cell=60),
        dict(type='table', var=lambda S: S.get('a') or S.get('m') or [[0, 0], [0, 0]], label='a（先是 M，之后每轮自乘）', h=150, cell=70),
    ],
    watch=[('c', 'c', 'pink'), ('match_cnt', 'match_cnt', 'green'), ('n', 'n', 'blue')],
    captions={
        'n = len(s)': '`n = {n}`：每次操作有 `n - 1` 种选法（后缀长度 1 到 n-1）',
        'c = self.kmp_search': '`c` = 有多少种循环移位得到 `t` = ==`{c}`==。把 `s` 接成 `s + s[:-1]`，数 `t` 出现几次',
        'm = self.pow': '`c = {c}`，矩阵 `M = [[c-1, c], [n-c, n-1-c]]`；`M^k` 就是 `k` 次操作的转移，`k` 最大 `10^15`',
        'return m[0][s != t]': '`s != t` 为真时取第 1 列（初始“不等于 t”），答案 = =={ret}==',
        'pi = [0] * len(s)': '`pi[i]` 先全填 0',
        'c = 0': '`c` = 当前已经匹配的长度',
        'while c and s[c] != v': lambda S, B, r: (f'`c = {S.c}`，`s[{S.c}] = {S.s[S.c]} ≠ {S.v}` → ==失配，回退== `c = pi[c-1]`' if S.c and S.s[S.c] != S.v
                                                   else '`c = 0` 或能接上 → 不用回退'),
        'c = pi[c - 1]': '`c` 回退到 `{c}`',
        'if s[c] == v': lambda S, B, r: (f'`s[{S.c}] = {S.s[S.c]}` 与 `{S.v}` 相等 → 匹配长度 +1' if S.s[S.c] == S.v else f'`s[{S.c}] ≠ {S.v}` → 不匹配，`c` 保持'),
        'c += 1': '`c` 变成 `{c}`',
        'pi[i] = c': '`pi[{i}] = {c}`',
        'return pi': '前缀函数算完：`pi = {pi}`',
        'pi = self.calc_pi': '先对模式串算前缀函数',
        'match_cnt = c = 0': '`match_cnt` 记匹配次数，`c` 是当前已匹配长度',
        'for i, v in enumerate(text)': '逐个读 `text` 的字符',
        'while c and pattern[c] != v': lambda S, B, r: (f'`pattern[{S.c}] = {S.pattern[S.c]} ≠ {S.v}` → ==失配，回退== 到 `pi[{S.c - 1}]`' if S.c and S.pattern[S.c] != S.v
                                                         else '没有失配 → 不用回退'),
        'if pattern[c] == v': lambda S, B, r: (f'`pattern[{S.c}] = {S.pattern[S.c]} == {S.v}` → 匹配长度 +1' if S.pattern[S.c] == S.v else f'`pattern[{S.c}] ≠ {S.v}` → 这个字符接不上'),
        'if c == len(pattern)': lambda S, B, r: ('`c` 等于模式串长度 → ==整串匹配成功== 一次' if S.c == len(S.pattern) else f'`c = {S.c}` 还没匹配完'),
        'match_cnt += 1': '`match_cnt` = {match_cnt}',
        'c = pi[c - 1]': '`c` 回退到 `{c}`（允许重叠匹配）',
        'return match_cnt': '`t` 在 `s+s[:-1]` 中出现 `{match_cnt}` 次',
        'res = [[1, 0], [0, 1]]': '`res` 先放单位矩阵 `M^0`',
        'while n': lambda S, B, r: (f'`k = {S.n}` 还没用完 → 看最低位' if S.n else '次数用完了，`res = M^k`'),
        'if n % 2': lambda S, B, r: ('最低位是 1 → ==把当前 a（M 的 2^j 次幂）乘进 res==' if S.n % 2 else '最低位是 0 → 这一块不用'),
        'res = self.multiply(res, a)': '`res = res × a`',
        'a = self.multiply(a, a)': '`a` 自乘：一次走 `2^j` 步 → `2^(j+1)` 步',
        'n //= 2': '`k` 减半 → {n}',
        'return res': '返回 `M^k`',
    },
    cards=dict(
        one_liner='操作 = 循环移位；只关心“等于 t / 不等于 t”两种状态',
        complexity='时间 `O(n + log k)`，空间 `O(n)`',
        problem=['每次操作：把 `s` 长为 `l`（`0 < l < n`）的后缀移到开头；求恰好 `k` 次把 `s` 变成 `t` 的方案数',
                 '`n` 最大 `5×10^5`，`k` 最大 `10^15`，答案对 `10^9+7` 取模',
                 '本视频：`s = "abcd", t = "cdab", k = 5` → `61`'],
        quote='操作得到的是 s 的循环同构字符串，这意味着，只要 s+s 中包含 t，就可以从 s 变成 t。……定义 f[i][0] 表示 i 次操作后等于 t 的方案数，f[i][1] 表示 i 次操作后不等于 t 的方案数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`c` = `s` 的循环同构里等于 `t` 的个数，用 KMP 在 `s+s[:-1]` 里数',
              '`f[i][0]` / `f[i][1]` = 操作后等于 / 不等于 `t`：转移系数 `c-1, c, n-c, n-1-c`',
              '转移是固定的 2×2 矩阵 → `M^k` 用快速幂，答案 `m[0][s != t]`'],
        summary=['时间 `O(n + log k)`，空间 `O(n)`',
                 '易错：`s + s[:-1]`（去掉最后一个字符）才不会多数一次；矩阵取模；`s == t` 时初始状态是“等于”',
                 '“等于 t”后保持等于 t 有 `c-1` 种（不能不动），不等于时变成 t 有 `c` 种',
                 '同类：矩阵快速幂优化 DP（790、3337、3700）']
    ),
)
