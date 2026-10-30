class _Named:
    def __init__(self, f, name):
        self.f, self.name = f, name

    def __call__(self, S):
        return self.f(S)

    def __str__(self):
        return self.name

    __repr__ = __str__


def _pt(name):
    def f(S):
        v = S.get(name)
        if 'index' not in S or v is None or not isinstance(v, int) or v < 0 or v >= len(S['word']):
            return None
        return v
    return _Named(f, name)


def _idx(S):
    return S.get('index') if 'index' in S and 'q' in S else None


def _end(S):
    """最小合法右端：max(v, p)"""
    if 'index' not in S or S.get('p') is None:
        return None
    v, p = S['v'], S['p']
    if v < 0 or p < 0 or max(v, p) >= len(S['word']) or max(v, p) < S['index']:
        return None
    if S['q'] <= max(v, p) and S['q'] <= S['p'] and S['q'] != 0 and v > p and False:
        return None
    return max(v, p)


def _txt(S):
    if 'res' not in S:
        return '`v`：元音凑齐的最小右端；`p`：辅音恰好 k 个的最小右端；`q`：p 之后的下一个辅音'
    if 'index' not in S:
        return f"`vowel = {S['vowel']}`，`consonant = {S['consonant']}`"
    v, p, q = S['v'], S['p'], S['q']
    return f"`vowel = {S['vowel']}` 种元音，`consonant = {S['consonant']}`；`v = {v}`，`p = {p}`，`q = {q}`"


CONFIG = dict(
    num=3306, title='元音辅音字符串计数 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='双窗口 · 元音边界 v 与辅音边界 p/q',
    tags=['难度分 2200'],
    code='''
class Solution(object):
    def countOfSubstrings(self, word, k):

        vowel_freq = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
        consonant = 0
        vowel = 0
        n = len(word)

        v = -1 
        p = -1
        q = 0
        res = 0

        for index, char in enumerate(word):
            while v + 1 < n and vowel < 5:
                if word[v + 1] in vowel_freq:
                    vowel_freq[word[v + 1]] += 1
                    if vowel_freq[word[v + 1]] == 1:
                        vowel += 1
                v += 1

            if vowel < 5:
                break
            
            if k == 0:
                if char in vowel_freq:
                    p = index
                else:
                    p = None
            else:
                while p + 1 < n and consonant < k:
                    if word[p + 1] not in vowel_freq:
                        consonant += 1
                    p += 1
                
                if consonant < k:
                    break

            if p is not None:
                if q <= p:
                    q = p + 1
                    while q < n and word[q] in vowel_freq:
                        q += 1
            
                if v < p:
                    res += q - p
                elif v < q:
                    res += q - v

            if char in vowel_freq:
                vowel_freq[char] -= 1
                if vowel_freq[char] == 0:
                    vowel -= 1
            
            elif k > 0:
                consonant -= 1
            

        return res
''',
    call='Solution().countOfSubstrings("aeiouqeb", 1)',
    expect=2,
    views=[
        dict(type='string', var='word', label='word（蓝 = 左端点 index，粉 = v，橙 = p，青 = q）', cell=100, h=240,
             pointers={_Named(_idx, 'index'): 'blue', _pt('v'): 'pink', _pt('p'): 'orange', _pt('q'): 'cyan'}),
        dict(type='map', var='vowel_freq', label='vowel_freq（窗口里 5 种元音的次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('p', 'p', 'orange'), ('q', 'q', 'cyan'), ('res', 'res', 'green')],
    captions={
        'vowel_freq = ': '`vowel_freq`：窗口里每种元音的次数',
        'consonant = 0': '`consonant` 记窗口里的辅音个数，`vowel` 记元音凑齐了几种',
        'v = -1': '`v`：元音凑齐的最小右端（包含），`p`：辅音刚好 k 个的最小右端，`q`：p 之后下一个辅音的位置',
        'res = 0': '`res` 累计答案',
        'for index, char in enumerate(word)': lambda S, B, ret: (f'固定左端点 `index = {S.index}`（`{S.char!r}`）：算它的合法右端范围' if 'index' in S else '结束'),
        'while v + 1 < n and vowel < 5': lambda S, B, ret: (
            f'`vowel = {S.vowel} < 5`：元音还没凑齐，`v` 继续右移' if S.v + 1 < S.n and S.vowel < 5
            else (f'`vowel = 5`：元音凑齐了，`v = {S.v}` 就是最小右端' if S.vowel >= 5 else '`v` 到头了')),
        'if word[v + 1] in vowel_freq': lambda S, B, ret: (f'`word[{S.v + 1}] = {S.word[S.v + 1]!r}` 是元音：计数' if S.word[S.v + 1] in S.vowel_freq else f'`word[{S.v + 1}] = {S.word[S.v + 1]!r}` 是辅音：跳过'),
        'vowel_freq[word[v + 1]] += 1': '`vowel_freq[{word[v + 1]!r}]` → `{vowel_freq[word[v + 1]]}`',
        'if vowel_freq[word[v + 1]] == 1': lambda S, B, ret: ('第一次出现 → ==元音种类 +1==' if S.vowel_freq[S.word[S.v + 1]] == 1 else '这种元音已经有了，种类不变'),
        'vowel += 1': '元音凑齐 `{vowel}` 种',
        'v += 1': '`v` → `{v}`',
        'if vowel < 5': lambda S, B, ret: ('元音凑不齐，之后的左端点也不行 → ==break==' if S.vowel < 5 else '元音凑齐了，继续看辅音'),
        'if k == 0': lambda S, B, ret: ('`k == 0`：不能有辅音，单独处理' if S.k == 0 else f'`k = {S.k} > 0`：用 `p` 扩出恰好 k 个辅音'),
        'while p + 1 < n and consonant < k': lambda S, B, ret: (
            f'`consonant = {S.consonant} < k = {S.k}`：辅音不够，`p` 继续右移' if S.p + 1 < S.n and S.consonant < S.k
            else (f'`consonant = {S.consonant}`：恰好 k 个了，`p = {S.p}` 是最小右端' if S.consonant >= S.k else '`p` 到头了')),
        'if word[p + 1] not in vowel_freq': lambda S, B, ret: (f'`word[{S.p + 1}] = {S.word[S.p + 1]!r}` 是辅音：计数' if S.word[S.p + 1] not in S.vowel_freq else f'`word[{S.p + 1}]` 是元音：不计辅音'),
        'consonant += 1': '辅音个数 → `{consonant}`',
        'p += 1': '`p` → `{p}`',
        'if consonant < k': lambda S, B, ret: ('辅音凑不够 k 个 → ==break==' if S.consonant < S.k else f'辅音恰好 `{S.consonant}` 个'),
        'if p is not None': '`p` 存在才有合法子串',
        'if q <= p': lambda S, B, ret: (f'`q = {S.q} <= p = {S.p}`：q 过期了，重新找 p 之后的下一个辅音' if S.q <= S.p else f'`q = {S.q}` 还在 p 右边，不用动'),
        'q = p + 1': '从 `p + 1` 往右找',
        'while q < n and word[q] in vowel_freq': lambda S, B, ret: (f'`word[{S.q}] = {S.word[S.q]!r}` 是元音：q 继续右移' if S.q < S.n and S.word[S.q] in S.vowel_freq else f'`q = {S.q}`：下一个辅音（或末尾）。右端到 `q-1` 之前辅音数都恰好 k'),
        'q += 1': '`q` → `{q}`',
        'if v < p': '`v < p`：元音已经凑齐，右端从 `p` 到 `q-1` 都合法 → 增加 `q - p = {q - p}`，`res = {res}`',
        'res += q - p': '右端取 `p ~ q-1`，共 `q - p = {q - p}` 个 → `res = {res}`',
        'elif v < q': '`p <= v < q`：右端得从 `v` 开始',
        'res += q - v': '右端取 `v ~ q-1`，共 `q - v = {q - v}` 个 → `res = {res}`',
        'if char in vowel_freq': lambda S, B, ret: (f'左端点 `{S.char!r}` 是元音：右移时要移出窗口' if S.char in S.vowel_freq else f'左端点 `{S.char!r}` 是辅音：右移时辅音少一个'),
        'vowel_freq[char] -= 1': '`vowel_freq[{char!r}]` → `{vowel_freq[char]}`',
        'if vowel_freq[char] == 0': lambda S, B, ret: ('次数变 0 → ==元音种类 −1==' if S.vowel_freq[S.char] == 0 else '这种元音还有，种类不变'),
        'vowel -= 1': '元音种类 → `{vowel}`',
        'elif k > 0': '`k > 0` 才需要维护辅音个数',
        'consonant -= 1': '辅音个数 → `{consonant}`',
        'return res': '返回 `{res}`',
    },
    skip=['n = len(word)', 'vowel = 0', 'p = -1', 'q = 0', 'if v < p:', 'elif v < q', 'v += 1', 'p += 1', 'q += 1', 'elif k > 0'],
    max_steps=110,
    cards=dict(
        one_liner='固定左端点，元音边界 v 与辅音边界 p/q 夹出合法右端范围',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `word` 的子串中：==5 个元音都至少出现一次==，且==恰好含 k 个辅音==的个数',
                 '示例：`word = "aeiou", k = 0` → `1`',
                 '本视频：`word = "aeiouqeb", k = 1` → `2`'],
        quote='处理元音字母的窗口右边界需要保证窗口内每种元音字母至少都出现了一次，且这个右边界最小。……处理辅音字母的窗口右边界需要保证窗口内的辅音字母数量恰好为k个，且这个右边界最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举左端点：`v` = 凑齐 5 种元音的最小右端；`p` = 凑够 k 个辅音的最小右端',
              '`q` = p 之后的下一个辅音：右端在 `[p, q-1]` 时辅音数恰好为 k',
              '合法右端是 `[max(v, p), q-1]`：`v < p` 加 `q-p`；`p <= v < q` 加 `q-v`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '元音或辅音凑不齐时直接 `break`，后面的左端点只会更短',
                 '`k == 0` 单独处理：左端点是元音时 `p = index`，否则不存在',
                 '对比灵神：灵神用 `f(k) − f(k+1)` 两个滑窗相减；yiduobo 用 v、p、q 三个边界直接数'],
    ),
)
