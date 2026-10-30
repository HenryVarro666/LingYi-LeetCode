S_IN, K = 'abacbab', 2


def _color(S, i, v):
    if 'p' in S and 'index' in S and S.get('_line') == 18 and i >= S['p']:
        return 'green'
    return None


def _top(S):
    if 'index' not in S:
        return '对每个左边界 index，找最小合法右边界 p：贡献 `len(s) − p` 个'
    i, p, n = S['index'], S['p'], len(S['s'])
    if p >= n:
        return f'`p = {p}` 越界：从 index 开始再也凑不出 k 次，结束'
    if S.get('_line') == 18:
        return f"`s[{i}..{p}]` 中 `{S['s'][p]!r}` 恰好 {S['k']} 次：右端点取 `{p}..{n - 1}` 都合法 → =={n - p}== 个"
    return f"左边界 `index = {i}`，候选右边界 `p = {p}`"


def _wh(S, B, ret):
    p, n = S.p, len(S.s)
    if p >= n:
        return f'`p = {p}` 到头了，停止扩展'
    v = S.freq.get(S.s[p], 0)
    if v < S.k:
        return f'`freq[{S.s[p]!r}] = {v} < {S.k}`：把 `s[{p}]` 纳入窗口试试'
    return f'`freq[{S.s[p]!r}] = {v}` 已经是 k：上一轮的 p 仍然合法，==不用动=='


CONFIG = dict(
    num=3325, title='字符至少出现 K 次的子字符串 I', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左边界 · 最小右边界 p 单调右移',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def numberOfSubstrings(self, s, k):
        
        freq = {}
        p = 0
        res = 0

        for index, char in enumerate(s):
            while p < len(s) and freq.get(s[p], 0) < k:
                freq[s[p]] = freq.get(s[p], 0) + 1
                if freq[s[p]] == k:
                    break
                p += 1

            if p == len(s):
                break
            
            res += len(s) - p

            freq[char] -= 1
            if freq[char] == k - 1:
                p += 1

        return res
''',
    call=f'Solution().numberOfSubstrings({S_IN!r}, {K})',
    expect=12,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（框 = [index, p]，绿 = 合法右端点 p..n−1）',
             pointers={'index': 'blue', 'p': 'pink'}, window=('index', 'p'), color=_color, cell=110, h=280),
        dict(type='map', var='freq', label='freq（窗口 [index, p] 内的字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('p', 'p', 'pink'), ('k', 'k', 'orange'), ('res', 'res', 'green')],
    captions={
        'freq = {}': '`freq`：窗口内每种字母的次数',
        'p = 0': '`p`：当前左边界的==最小==合法右边界',
        'res = 0': '`res = 0`',
        'for index, char': lambda S, B, r: f'左边界 `index = {S.index}`（`{S.char!r}`）',
        'while p < len(s)': _wh,
        'freq[s[p]] = freq.get': '`freq[{s[p]!r}]` → {freq[s[p]]}',
        'if freq[s[p]] == k': lambda S, B, r: (f'`{S.s[S.p]!r}` 恰好 {S.k} 次 → `p = {S.p}` 就是最小右边界' if S.freq[S.s[S.p]] == S.k
                                               else f'`{S.s[S.p]!r}` 只有 {S.freq[S.s[S.p]]} 次，还不够'),
        'if p == len(s)': lambda S, B, r: ('`p == len(s)`：找不到合法右边界，后面的左边界更不可能 → 结束' if S.p == len(S.s)
                                           else f'找到了 `p = {S.p}`'),
        'res += len(s) - p': '以 `{index}` 为左边界：右端点 `{p}..{len(s) - 1}` 共 `{len(s)} − {p}` 个 → `res` = =={res}==',
        'freq[char] -= 1': '`{char!r}` 移出窗口：`freq[{char!r}]` → {freq[char]}',
        'if freq[char] == k - 1': lambda S, B, r: (f"移出的正是 `s[p] = {S.char!r}`，它掉到 k−1 次 → ==p 必须后移==" if S.freq[S.char] == S.k - 1
                                                   else f"移出的不是关键字母，`s[p]` 仍有 k 个 → ==p 不动=="),
        'p += 1': lambda S, B, r: (f'`p` → {S.p}' if S._line == 13 else f'`p` → {S.p}，下一轮从这里继续扩展'),
        12: '`break`：p 停在这里，不再右移',
        16: '`break`：剩下的左边界都不用看了',
        'return res': '一共 =={ret}== 个合法子串',
    },
    max_steps=75,
    cards=dict(
        one_liner='枚举左边界，最小右边界 p 只会右移：每个左边界贡献 len(s) − p',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['给字符串 `s` 和整数 `k`',
                 '求==至少有一个字符出现至少 k 次==的子串个数',
                 '示例：`s = "abacb", k = 2` → `4`',
                 f'本视频：`s = "{S_IN}", k = {K}` → `12`'],
        quote='s[p]必然是唯一一个恰好出现了k次的字符……只有当上一轮被移出窗口的字符恰好就是s[p]时，才有必要将p向后移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['左边界 index 固定，最小右边界 p 之后的右端点==都合法==：`len(s) − p` 个',
              'p 是第一个让某字母到 k 次的位置，那个字母就是 `s[p]`',
              '左边界右移只会让 p ==不动或右移==，均摊 `O(1)`'],
        summary=['时间 `O(n)`：index 和 p 都只右移',
                 '`while` 里先加次数，恰好 k 就 `break`，p 停在关键位置',
                 '移出字母后用 `== k − 1` 判断是否正是关键字母',
                 '对比灵神：灵神枚举右端点加 left，这里枚举左端点加 `len(s) − p`',
                 '代码本身可在 Python 3 运行，未做改动'],
    ),
)
