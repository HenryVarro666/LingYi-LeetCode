S0, K0 = 'abacb', 2


def _txt(S):
    if 'p' not in S:
        return '对每个左端点 `index`，找最小的合法右端点 `p`，则 `p ~ n-1` 都合法'
    return f'左端点 `{S.get("index")}`，最小合法右端点 `p = {S["p"]}` → 贡献 `n − p = {len(S["s"]) - S["p"]}`　`res = {S["res"]}`'


CONFIG = dict(
    num=3329, title='字符至少出现 K 次的子字符串 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · 最小合法右端点 p',
    tags=[],
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
    call=f'Solution().numberOfSubstrings({S0!r}, {K0})',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 左端点 index 到 p 的窗口）', cell=100, h=230,
             pointers={'index': 'blue', 'p': 'pink'},
             window=('index', lambda S: min(S['p'], len(S['s']) - 1))),
        dict(type='map', var='freq', label='freq（窗口 [index, p] 内各字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('k', 'k', 'yellow'), ('res', 'res', 'green')],
    captions={
        'freq = {}': '`freq` 记录窗口里各字母出现次数',
        'p = 0': '`p` 是当前左端点对应的最小合法右端点',
        'res = 0': '`res` 累计答案',
        'for index, char': '左端点 `index = {index}`（字母 `{char}`）',
        'while p < len(s)': lambda S, B, r: (f'`freq[s[{S.p}]] = {S.freq.get(S.s[S.p], 0)} < k = {S.k}`：窗口还不合法，`p` 继续向右扩' if S.p < len(S.s) and S.freq.get(S.s[S.p], 0) < S.k
                                              else f'`p = {S.p}`：窗口已合法或 `p` 到头，停止扩张'),
        'freq[s[p]] = freq.get': '`s[p] = {s[p]}` 进入窗口：`freq` 中次数 → {freq[s[p]]}',
        'if freq[s[p]] == k': lambda S, B, r: (f'`freq[{S.s[S.p]!r}] == {S.k}`：==恰好第 k 次==，`p` 就是最小合法右端点 → break' if S.freq[S.s[S.p]] == S.k
                                                else f'`freq[{S.s[S.p]!r}] = {S.freq[S.s[S.p]]} < k`：还没到 k 次'),
        'p += 1': '`p` → {p}',
        'if p == len(s)': lambda S, B, r: ('`p` 越界：后面再也凑不出 k 次 → 结束' if S.p == len(S.s)
                                            else f'`p = {S.p}` 有效：从 `index` 起到 `p` 合法'),
        'res += len(s) - p': '右端点取 `p ~ {len(s) - 1}` 都合法，共 `{len(s)} − {p}` 个 → `res = {res}`',
        'freq[char] -= 1': '左端点 `{char}` 离开窗口：`freq[{char!r}]` → {freq[char]}',
        'if freq[char] == k - 1': lambda S, B, r: (f'`freq[{S.char!r}] = {S.k - 1}`：移走的恰是凑到 k 次的字母 → `p` 要右移' if S.freq[S.char] == S.k - 1
                                                    else f'`freq[{S.char!r}] = {S.freq[S.char]}`：`s[p]` 仍有 k 个，`p` 不用动'),
        'return res': '返回 =={res}==',
    },
    cards=dict(
        one_liner='对每个左端点找最小合法右端点 p，p 之后全都合法',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['给定字符串 `s` 和整数 `k`，统计子串中「至少有一个字符出现至少 k 次」的子串个数',
                 '示例：`s = "abacb", k = 2` → `4`',
                 '第二题数据规模更大，要线性做法'],
        quote='s[p]必然是唯一一个恰好出现了k次的字符，因为若其他字符已经出现了k次，那么在p之前必然存在其他满足条件的右边界，与p的定义矛盾',
        quote_src='—— yiduobo 题解原文',
        idea=['固定左端点 `index`，最小合法右端点记为 `p`，以 `p ~ n-1` 为右端点都合法，共 `n − p` 个',
              '`index` 右移时 `p` 只会不动或右移',
              '只有移出去的字符恰好是 `s[p]` 时才需要把 `p` 右移'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '`p == len(s)` 时后面再也凑不出，直接 `break`',
                 '`freq[s[p]] == k` 时要 `break`，此时不能再 `p += 1`',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神枚举右端点、收缩到不合法；yiduobo 枚举左端点、扩到刚合法'],
    ),
)
