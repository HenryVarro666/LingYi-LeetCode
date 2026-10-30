def _ranges(pos, m):
    out = set()
    for p in pos:
        out.update(range(p, p + m))
    return out


def _col(S, i, v):
    inn = S['_inner']
    a, b = S.get('a', ''), S.get('b', '')
    if 'pattern' in inn and 'res' in inn and 'text' in inn:      # KMP 扫描文本阶段
        pat, res, ci, c = inn['pattern'], inn['res'], inn.get('i', -1), inn.get('c', 0)
        done = _ranges(res, len(pat))
        if i == ci:
            return 'blue'
        if c > 0 and ci - c < i < ci:
            return 'green'
        if i in done:
            return 'yellow' if pat == a else 'purple'
        return None
    if 'pos_a' in S:
        ra, rb = _ranges(S['pos_a'], len(a)), (_ranges(S['pos_b'], len(b)) if 'pos_b' in S else set())
        if i == S.get('i') and S.get('i') in S['pos_a']:
            return 'blue'
        if 'pos_b' in S and 'j' in S and S['j'] < len(S['pos_b']) and S['pos_b'][S['j']] <= i < S['pos_b'][S['j']] + len(b):
            return 'pink'
        if i in ra:
            return 'yellow'
        if i in rb:
            return 'purple'
    return None


def _txt(S):
    inn = S['_inner']
    a, b = S.get('a', ''), S.get('b', '')
    if 'pattern' in inn and 'text' in inn:
        pat = inn['pattern']
        who = 'a' if pat == a else 'b'
        if 'res' in inn:
            return (f"KMP 在 s 里找 {who} = `{pat}`：已匹配 `c = {inn.get('c', 0)}` 个字符，已找到起点 `{inn['res']}`")
        return f"先给 {who} = `{pat}` 建 `pi` 表（前缀函数）：`pi = {inn.get('pi')}`"
    if 'pos_a' in S and 'pos_b' in S:
        j = S.get('j')
        extra = ''
        if j is not None and j < len(S['pos_b']) and 'i' in S:
            extra = f"；当前 `i = {S['i']}`，`pos_b[{j}] = {S['pos_b'][j]}`"
        return f"`pos_a = {S['pos_a']}`（黄），`pos_b = {S['pos_b']}`（紫），要求 |i − j| ≤ {S['k']}{extra}"
    return f"在 s = `{S.get('s')}` 中分别找 a = `{a}`、b = `{b}` 的所有位置"


def _w1(S, B, r):
    if S.c and S.pattern[S.c] != S.v:
        return f'`pattern[{S.c}] = {S.pattern[S.c]}` ≠ `{S.v}`：失配 → ==c 退到 pi[c-1]=={S.pi[S.c - 1]}（不用从头来）'
    return '不再失配（或 c 已是 0）：停止回退'


def _w2(S, B, r):
    if S.c and S.pattern[S.c] != S.v:
        return f'`pattern[{S.c}] = {S.pattern[S.c]}` ≠ `{S.v}`：失配 → ==c 退到 pi[c-1]=={S.pi[S.c - 1]}'
    return '字符对得上或 c 已为 0：不用回退'


def _jw(S, B, r):
    if S.j < S.m and S.pos_b[S.j] < S.i - S.k:
        return f'`pos_b[{S.j}] = {S.pos_b[S.j]}` < `i − k = {S.i - S.k}`：太靠左，对 i 和之后的 i 都没用 → ==j 右移=='
    if S.j < S.m:
        return f'`pos_b[{S.j}] = {S.pos_b[S.j]}` ≥ `i − k = {S.i - S.k}`：这是 ≥ i−k 的最小 b 位置，不用再移'
    return '`pos_b` 用完了'


def _jif(S, B, r):
    if S.j < S.m and abs(S.pos_b[S.j] - S.i) <= S.k:
        return f'`|{S.pos_b[S.j]} − {S.i}| = {abs(S.pos_b[S.j] - S.i)} ≤ {S.k}` → ==i 是美丽下标=='
    if S.j < S.m:
        return f'`|{S.pos_b[S.j]} − {S.i}| = {abs(S.pos_b[S.j] - S.i)} > {S.k}`：最近的 b 也太远 → i 不是'
    return '右边没有 b 了 → i 不是'


CONFIG = dict(
    num=3006, title='找出数组中的美丽下标 I', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='KMP 找位置 + 双指针',
    code='''
class Solution:
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        pos_a = self.kmp(s, a)
        pos_b = self.kmp(s, b)

        ans = []
        j, m = 0, len(pos_b)
        for i in pos_a:
            while j < m and pos_b[j] < i - k:
                j += 1
            if j < m and abs(pos_b[j] - i) <= k:
                ans.append(i)
        return ans

    def kmp(self, text: str, pattern: str) -> List[int]:
        m = len(pattern)
        pi = [0] * m
        c = 0
        for i in range(1, m):
            v = pattern[i]
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            pi[i] = c

        res = []
        c = 0
        for i, v in enumerate(text):
            v = text[i]
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            if c == len(pattern):
                res.append(i - m + 1)
                c = pi[c - 1]
        return res
''',
    call="Solution().beautifulIndices('abxab', 'ab', 'x', 1)",
    expect=[3],
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='string', var='s', color=_col, h=190),
        dict(type='array', var='pi', h=120, label='pi'),
    ],
    watch=['c', 'i', ('pos_a', 'pos_a', 'yellow'), ('pos_b', 'pos_b', 'purple'), ('ans', 'ans', 'green')],
    skip=['v = pattern[i]', 'v = text[i]', 'm = len(pattern)', 'c = 0', 'ans = []', 'res = []'],
    max_steps=130,
    captions={
        'pos_a = self.kmp': '用 KMP 找出 a 在 s 中的所有出现位置：`pos_a = {pos_a}`',
        'pos_b = self.kmp': '再用 KMP 找出 b 的所有位置：`pos_b = {pos_b}`',
        'j, m = 0': '`pos_a`、`pos_b` 都是==有序==的 → 双指针：`j` 指向 `pos_b` 里当前候选，只会右移',
        'for i in pos_a': lambda S, B, r: ('`pos_a` 枚举完了' if S.get('i') == B.get('i')
                                           else f'枚举 a 的每个起点 `i = {S.i}`'),
        'while j < m and pos_b[j] < i - k': _jw,
        'j += 1': '`j` → {j}',
        'if j < m and abs': _jif,
        'ans.append(i)': '`ans = {ans}`',
        'return ans': '美丽下标：`{ans}`',
        'pi = [0] * m': '`pi[i]`：pattern[:i+1] 的最长相等真前后缀长度，先全部置 0',
        'for i in range(1, m)': lambda S, B, r: ('`pi` 表建完' if S.get('i') == B.get('i')
                                                 else f'建 pi 表：处理 `pattern[{S.i}]`'),
        'while c and pattern[c] != v': _w1,
        'pi[i] = c': '`pi[{i}] = {c}`',
        'res = []': 'pi 建好了，开始在 `text` 上扫描，`res` 收集起点',
        'for i, v in enumerate(text)': lambda S, B, r: ('`text` 扫描完了' if S.get('i') == B.get('i')
                                                        else f'`text[{S.i}] = {S.v}`'),
        'if c == len(pattern)': lambda S, B, r: (f'`c = {S.c}` 等于 `len(pattern)`：==完整匹配一次==' if S.c == len(S.pattern)
                                                 else f'`c = {S.c}` < `len(pattern) = {len(S.pattern)}`：还没匹配完'),
        'res.append': '起点 = `i − m + 1 = {i - m + 1}`，`res = {res}`',
        'c = pi[c - 1]': '`c` 退到 `pi[c-1]`，为可能重叠的下一次匹配做准备：`c = {c}`',
        'return res': '`{res}` 就是 pattern 在 text 中的所有出现位置',
    },
    cards=dict(
        one_liner='KMP 找出 a、b 的所有位置，再用双指针匹配距离 ≤ k',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s[i..]` 等于 `a` 且附近（距离 ≤ k）存在 `b` 的下标 `i` 是美丽下标',
                 '按从小到大返回所有美丽下标',
                 '本视频：`s=abxab, a=ab, b=x, k=1` → `[3]`'],
        quote='用 KMP 求出 a 在 s 中的所有出现位置，记作 posA。用 KMP 求出 b 在 s 中的所有出现位置，记作 posB。由于 posA 和 posB 都是有序的，也可以用双指针做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把「找所有出现位置」交给 `kmp`，得到两个有序数组 `pos_a`、`pos_b`',
              '`i` 在 `pos_a` 中递增，`pos_b[j] < i - k` 的 b 以后也没用，`j` 只增不减',
              '`j` 停下后 `pos_b[j]` 是 ≥ i−k 的最近 b，判断 `|pos_b[j] − i| ≤ k` 即可'],
        after=[dict(heading='另一种写法：二分', lines=['题解写法一：在 `pos_b` 中 `bisect_left` 找离 i 最近的 j', '检查左右两个相邻位置，时间 `O(n log n)`', '本视频演示的是更快的双指针版本'])],
        summary=['时间 `O(n)`：`j` 总共右移不超过 n 次；空间 `O(n)`',
                 '`kmp` 里匹配成功后要 `c = pi[c - 1]`，才能找到重叠出现的位置',
                 '`pos_b[j] < i - k` 的 `j` 不会回退，因为 `i` 单调递增',
                 '易错：`abs(pos_b[j] - i) <= k` 要先判断 `j < m`'],
    ),
)
