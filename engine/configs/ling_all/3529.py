_G = [['a', 'a', 'b', 'a'], ['b', 'a', 'a', 'a']]


def _scan(S):
    ln = S['_line']
    if ln <= 13:
        return S.get('pattern')
    if ln <= 28:
        return S.get('text')
    return S.get('h_text')


def _flat_cell(S, i, j):
    m, n = len(S['grid']), len(S['grid'][0])
    return i * n + j, j * m + i


def _gcolor(S, i, j, v):
    if 'grid' not in S:
        return None
    ln = S['_line']
    m, n = len(S['grid']), len(S['grid'][0])
    ih, iv = i * n + j, j * m + i
    if ln >= 14 and 'text' in S and S.get('i') is not None and ln <= 27:
        vert = 'in_pattern_h' in S
        cur = (S['i'] % m, S['i'] // m) if vert else (S['i'] // n, S['i'] % n)
        if (i, j) == cur:
            return 'yellow'
    if ln >= 39 and S.get('i') is not None and (i, j) == (S['i'] // n, S['i'] % n):
        return 'yellow'
    ph, pv = S.get('in_pattern_h'), S.get('in_pattern_v')
    h = bool(ph and ph[ih] > 0)
    vv = bool(pv and pv[iv] > 0)
    if h and vv:
        return 'green'
    if h:
        return 'blue'
    if vv:
        return 'pink'
    return None


def _diffv(S):
    ln = S['_line']
    if 14 <= ln <= 27:
        return S.get('diff')
    return S.get('in_pattern_h') if ln >= 34 else None


CONFIG = dict(
    num=3529, title='统计水平子串和垂直子串重叠格子的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='KMP 匹配 + 差分标记',
    tags=['灵神题单·常用数据结构', '灵神题单·字符串'],
    code='''
class Solution:
    def calc_pi(self, pattern: str) -> List[int]:
        pi = [0] * len(pattern)
        cnt = 0
        for i in range(1, len(pi)):
            b = pattern[i]
            while cnt > 0 and pattern[cnt] != b:
                cnt = pi[cnt - 1]
            if pattern[cnt] == b:
                cnt += 1
            pi[i] = cnt
        return pi

    def kmp_search(self, text: List[str], pattern: str, pi: List[int]) -> List[int]:
        n, k = len(text), len(pattern)
        diff = [0] * (n + 1)
        cnt = 0
        for i, b in enumerate(text):
            while cnt > 0 and pattern[cnt] != b:
                cnt = pi[cnt - 1]
            if pattern[cnt] == b:
                cnt += 1
            if cnt == k:
                diff[i - k + 1] += 1
                diff[i + 1] -= 1
                cnt = pi[cnt - 1]
        return list(accumulate(diff[:n]))

    def countCells(self, grid: List[List[str]], pattern: str) -> int:
        h_text = [c for row in grid for c in row]
        v_text = [c for col in zip(*grid) for c in col]

        pi = self.calc_pi(pattern)
        in_pattern_h = self.kmp_search(h_text, pattern, pi)
        in_pattern_v = self.kmp_search(v_text, pattern, pi)

        m, n = len(grid), len(grid[0])
        ans = 0
        for i, in_h in enumerate(in_pattern_h):
            if in_h and in_pattern_v[i % n * m + i // n]:
                ans += 1
        return ans
''',
    call='Solution().countCells([["a","b"],["a","b"]], "ab")',
    expect=2,
    max_steps=90,
    skip=['b = pattern[i]', 'n, k = len(text)', 'cnt = 0', 'diff = [0]', 'for i, b in enumerate(text)', 'for i in range(1, len(pi))', 'if cnt == k', 'ans = 0'],
    views=[
        dict(type='string', var=_scan, label='被扫描的串（pi 阶段 = pattern，匹配阶段 = 文本串，统计阶段 = 按行拉直）',
             color=lambda S, i, v: 'blue' if i == S.get('i') else None, h=150, cell=76),
        dict(type='string', var='pattern', label='pattern（cnt = 已匹配长度，指向下一个要比的字符）',
             pointers={'cnt': 'pink'}, h=200, cell=76),
        dict(type='array', var='pi', label='pi（前缀函数：失配时 cnt 退回 pi[cnt-1]）', h=120, cell=76, index=False),
        dict(type='array', var=_diffv, label='diff / inPattern（差分后的前缀和 > 0 即在某个匹配里）', h=120, cell=76, index=False),
        dict(type='grid', var='grid', label='grid（蓝=水平命中，粉=垂直命中，绿=都命中）', color=_gcolor, h=180, cell=76),
    ],
    watch=['i', 'cnt', ('k', 'k', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'pi = [0]': '`pi[i]` = pattern[:i+1] 的最长相等前后缀长度；先全填 0',
        'for i in range(1, len(pi))': lambda S, B, r: f'计算 `pi[{S.i}]`，`cnt` 是前一个位置的前后缀长度 `{S.cnt}`' if 'i' in S else '开始算 pi',
        'while cnt > 0 and pattern[cnt] != b': lambda S, B, r: (('读 `text[%d] = %s`：' % (S.i, S.b) if 'text' in S else '算 `pi[%d]`：' % S.i) + f'`cnt = {S.cnt}`，`pattern[{S.cnt}] = {S.pattern[S.cnt]}` 与 `b = {S.b}` {"不等" if S.pattern[S.cnt] != S.b else "相等"}'
                                                              + ('，失配 → 退回前一个前后缀' if S.cnt > 0 and S.pattern[S.cnt] != S.b else '，不用退')),
        'cnt = pi[cnt - 1]': lambda S, B, r: f'失配退回：`cnt = pi[{B.cnt - 1}]` = =={S.cnt}==，不用从头重来',
        'if pattern[cnt] == b': lambda S, B, r: (f'`pattern[{S.cnt}] = {S.pattern[S.cnt]}` {"==" if S.pattern[S.cnt] == S.b else "!="} `{S.b}`' + ('，匹配 → cnt + 1' if S.pattern[S.cnt] == S.b else '，仍不等，cnt 保持')),
        'pi[i] = cnt': '`pi[{i}] = {cnt}`',
        'return pi': '`pi = {pi}`：下面匹配时失配可以跳',
        'for i, b in enumerate(text)': lambda S, B, r: f'逐个读文本串：`text[{S.i}] = {S.b}`，`cnt = {S.cnt}` 是已匹配 pattern 的长度',
        'cnt += 1': lambda S, B, r: f'匹配一位：`cnt` → =={S.cnt}==' + (f'，`== k`：pattern 在 `[{S.i - S.k + 1}, {S.i}]` 完整出现' if 'k' in S and 'text' in S and S.cnt == S.k else ''),
        'if cnt == k': lambda S, B, r: (f'`cnt = {S.cnt} == k = {S.k}`：pattern 在 `[{S.i - S.k + 1}, {S.i}]` 完整出现' if S.cnt == S.k else f'`cnt = {S.cnt} != k = {S.k}`，还没匹配完'),
        'diff[i - k + 1] += 1': '差分标记匹配区间 `[{i-k+1}, {i}]` 的起点：`diff[{i-k+1}] += 1`',
        'diff[i + 1] -= 1': '区间结束：`diff[{i+1}] -= 1`。前缀和 > 0 的格子都在某个匹配里',
        'cnt = pi[cnt - 1]': lambda S, B, r: f'匹配完后不清零：`cnt = pi[{B.cnt - 1}]` = =={S.cnt}==，重叠的下一次匹配接着用' if B.cnt == B.k else f'失配退回：`cnt = pi[{B.cnt - 1}]` = =={S.cnt}==',
        'return list(accumulate': '前缀和：`{ret}`，值 > 0 的位置就在某个匹配子串里',
        'h_text =': '水平子串：把每行首尾相接拉成一条长串，换行也算连续',
        'v_text =': '垂直子串：按列拉直，`zip(*grid)` 取每一列',
        'pi = self.calc_pi': '先算 `pattern` 的前缀函数，水平、垂直共用，只算一次',
        'in_pattern_h =': '水平：在 `h_text` 上跑 KMP，`in_pattern_h[i] > 0` 表示该格在某个水平匹配里',
        'in_pattern_v =': '垂直：在 `v_text` 上跑 KMP，得到 `in_pattern_v`',
        'm, n =': '`m = {m}` 行，`n = {n}` 列：下标 `i` ↔ 格子 `(i // n, i % n)`',
        'for i, in_h': '枚举水平数组下标 `i = {i}`，对应格子 `({i // n}, {i % n})`',
        'if in_h and': lambda S, B, r: (f'格子 `({S.i // S.n}, {S.i % S.n})`：水平 `{S.in_h}`；它在垂直串里的下标 `{S.i} % {S.n} * {S.m} + {S.i} // {S.n}` = `{S.i % S.n * S.m + S.i // S.n}`，垂直值 `{S.in_pattern_v[S.i % S.n * S.m + S.i // S.n]}`'
                                       + (' → ==两边都命中==' if S.in_h and S.in_pattern_v[S.i % S.n * S.m + S.i // S.n] else ' → 不满足')),
        'ans += 1': '计数：`ans` → =={ans}==',
        'return ans': '共 `{ans}` 个格子',
    },
    cards=dict(
        one_liner='拉直成字符串做 KMP，差分标出被覆盖的格子，再按下标换算求交',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['字符矩阵 `grid`，水平子串按行拉直、垂直子串按列拉直',
                 '统计同时属于至少一个水平匹配和一个垂直匹配的格子数',
                 '本视频：`[["a","b"],["a","b"]]`，`pattern="ab"` → `2`'],
        quote='把 grid 每一行首尾相接，得到一个长为 mn 的文本串 text，我们需要在文本串 text 中找到所有模式串 pattern 的出现位置，这正是 KMP 算法的标准应用。',
        quote_src='—— 灵茶山艾府题解',
        idea=['水平 = 按行拉直，垂直 = 按列拉直，各跑一次 KMP',
              '匹配到 `text[i]` 时，把 `[i-k+1, i]` 用差分加一，前缀和 > 0 即被覆盖',
              '两个方向的下标换算：`(r, c)` 在水平里是 `r*n+c`，在垂直里是 `c*m+r`',
              '封装成 `kmp_search`，垂直方向直接复用'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '匹配完整后 `cnt = pi[cnt-1]`，让重叠的匹配也不漏',
                 '垂直下标是 `i % n * m + i // n`，别和水平的 `i` 混了',
                 '差分只需标记区间的头和尾，匹配之间重叠也不会重复计数',
                 '同类题：差分 §2.1 一维差分，KMP 模板题 28、686'],
    ),
)
