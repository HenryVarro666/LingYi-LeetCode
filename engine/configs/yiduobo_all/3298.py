class _Named:
    def __init__(self, f, name):
        self.f, self.name = f, name

    def __call__(self, S):
        return self.f(S)

    def __str__(self):
        return self.name

    __repr__ = __str__


def _left(S):
    """窗口 [left, p) 的左端点：p - 窗口内字符数"""
    if 'freq1' not in S or 'p' not in S or 'char' not in S:
        return None
    left = S['p'] - sum(S['freq1'].values())
    if S['_line'] in (_L19, _L20, _L21):
        left -= 1
    return left


def _lp(S):
    return _left(S)


def _rp(S):
    l = _left(S)
    return None if l is None else min(S['p'] - 1, len(S['word1']) - 1)


def _txt(S):
    if 'cnt' not in S:
        return '`cnt` = 已经达标的字符种数；`cnt == len(freq2)` 才合法'
    return f"`cnt = {S['cnt']}`，需要 `len(freq2) = {len(S['freq2'])}`：{'==合法==' if S['cnt'] >= len(S['freq2']) else '还没凑齐'}"


CODE = '''
class Solution(object):
    def validSubstringCount(self, word1, word2):

        freq2 = {}
        for char in word2:
            freq2[char] = freq2.get(char, 0) + 1
        
        cnt = 0
        freq1 = {}
        p = 0
        res = 0
        for char in word1:
            while p < len(word1) and cnt < len(freq2):
                freq1[word1[p]] = freq1.get(word1[p], 0) + 1
                if freq1[word1[p]] == freq2.get(word1[p], 0):
                    cnt += 1
                p += 1
            
            if cnt < len(freq2):
                break
            
            res += len(word1) - p + 1

            freq1[char] -= 1
            if freq1[char] == freq2.get(char, 0) - 1:
                cnt -= 1
        
        return res
'''
_LS = CODE.strip('\n').split('\n')
_L19 = [i + 1 for i, s in enumerate(_LS) if 'freq1[char] -= 1' in s][0]
_L20 = _L19 + 1
_L21 = _L19 + 2

CONFIG = dict(
    num=3298, title='统计重新排列后包含另一个字符串的子字符串数目 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑窗 · 枚举左端点 + cnt 达标数',
    tags=['难度分 1909'],
    code=CODE,
    call='Solution().validSubstringCount("abcabc", "abc")',
    expect=10,
    views=[
        dict(type='string', var='word1', label='word1（框 = 窗口 [left, p)，p 指向下一个要加入的字符）', cell=100, h=230,
             pointers={_Named(_lp, 'left'): 'blue', 'p': 'pink'}, window=(_lp, _rp)),
        dict(type='map', var='freq1', label='freq1（窗口内字符次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='map', var='freq2', label='freq2（word2 的字符次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='text', h=90, size=30, fn=_txt),
    ],
    watch=[('char', 'char', 'blue'), ('p', 'p', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'freq2 = {}': '`freq2` 记录 `word2` 里每种字符要几个',
        'for char in word2': '统计 `word2`',
        'freq2[char] = freq2.get': '`freq2[{char!r}]` = `{freq2[char]}`',
        'cnt = 0': '`cnt`：窗口里==已经达标==的字符种数',
        'freq1 = {}': '`freq1` 统计当前窗口里每种字符的数量',
        'p = 0': '`p`：窗口右边界（开区间），只会右移',
        'res = 0': '`res` 累计合法子串个数',
        'for char in word1': lambda S, B, ret: (f'固定左端点：`char = {S.char!r}`，找最小的 `p` 使 `[left, p)` 合法' if S.get('res') is not None and S.char != B.get('char', None) or 'char' not in B
                                                else '遍历结束'),
        'while p < len(word1) and cnt < len(freq2)': lambda S, B, ret: (
            f'`cnt = {S.cnt} < {len(S.freq2)}`：还没凑齐 word2 的字符，继续把 `word1[{S.p}] = {S.word1[S.p]!r}` 加进窗口'
            if S.p < len(S.word1) and S.cnt < len(S.freq2) else
            (f'`cnt = {S.cnt}`：已经凑齐，`p` 停下' if S.cnt >= len(S.freq2) else '`p` 到头了，不能再扩')),
        'freq1[word1[p]] = freq1.get': '窗口里 `{word1[p]!r}` 的数量 → `{freq1[word1[p]]}`',
        'if freq1[word1[p]] == freq2.get': lambda S, B, ret: (f'`freq1[{S.word1[S.p]!r}] = {S.freq1[S.word1[S.p]]}` 刚好等于需要的 `{S.freq2.get(S.word1[S.p], 0)}` → ==这种字符刚达标=='
                                                              if S.freq1[S.word1[S.p]] == S.freq2.get(S.word1[S.p], 0)
                                                              else f'`freq1[{S.word1[S.p]!r}] = {S.freq1[S.word1[S.p]]}` ≠ 需要的 `{S.freq2.get(S.word1[S.p], 0)}`：达标状态没变'),
        'cnt += 1': '达标种数加一 → `cnt = {cnt}`',
        'p += 1': '`p` 右移到 `{p}`',
        'if cnt < len(freq2)': lambda S, B, ret: (f'`cnt = {S.cnt} < {len(S.freq2)}`：加到头也凑不齐，之后的左端点更不行 → ==break=='
                                                  if S.cnt < len(S.freq2) else f'`cnt = {S.cnt}` 凑齐了，这个左端点有合法子串'),
        'res += len(word1) - p + 1': '`[left, p)` 合法，右边界取 `p-1 ~ n-1` 都行，共 `{len(word1)} - {p} + 1 = {len(word1) - p + 1}` 个 → `res = {res}`',
        'freq1[char] -= 1': '左端点右移：把 `{char!r}` 移出窗口 → `freq1[{char!r}] = {freq1[char]}`',
        'if freq1[char] == freq2.get(char, 0) - 1': lambda S, B, ret: (f'`{S.freq1[S.char]}` 刚好比需要的少 1：{S.char!r} ==由达标变成不达标=='
                                                                       if S.freq1[S.char] == S.freq2.get(S.char, 0) - 1
                                                                       else f'`{S.char!r}` 还有富余，达标状态不变'),
        'cnt -= 1': '达标种数减一 → `cnt = {cnt}`',
        'return res': '返回 `{res}`',
    },
    max_steps=100,
    cards=dict(
        one_liner='枚举左端点，找最小右边界；用 cnt 记达标的字符种数',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['`word1` 的子串 `x` 重新排列后以 `word2` 为前缀，`x` 就是==合法==的',
                 '统计 `word1` 里合法子串的个数，要求线性时间',
                 '示例：`word1 = "abcabc", word2 = "abc"` → `10`'],
        quote='对于word2中出现的所有字符，只要子串中同样的字符数量充足，那么子串就是合法的。……为了避免每次都需要对比整个哈希表，可以使用一个变量cnt表示目前freq1中已经达标的字符数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['重排后可以放成前缀 ⇔ 窗口里每种字符都 ≥ `word2` 的需要量',
              '`cnt` 只在“刚好达标 / 刚好掉出达标”时加减，不用每次比较整个哈希表',
              '每个左端点找最小 `p`，贡献 `len(word1) - p + 1` 个'],
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '`p` 是开区间：合法右边界从 `p-1` 到 `n-1`，所以是 `n - p + 1`',
                 '`cnt < len(freq2)` 时 `break`：窗口扩到头也不合法，后面更不行',
                 '对比灵神：灵神枚举右端点 `ans += left`，用 diff 数组记差；yiduobo 枚举左端点，用 freq1 / freq2 对比'],
    ),
)
