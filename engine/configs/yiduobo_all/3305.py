def _pos(S, name):
    v = S.get(name)
    return v if isinstance(v, int) and v >= 0 else None


def _top(S):
    if 'res' not in S:
        return ''
    k, v, p, q = S['k'], S['v'], S.get('p'), S['q']
    ps = '无' if p is None else p
    return f"右边界：元音凑齐 `v = {v}`，辅音恰好 k={k} 个 `p = {ps}`，下一个辅音 `q = {q}`　答案 `res` = =={S['res']}=="


def _cmp(S, B, ret):
    v, p, q = S['v'], S['p'], S['q']
    if v < p:
        return f'`v = {v} < p = {p}`：p 到 q-1 都合法，加 `q - p = {q - p}`'
    if v < q:
        return f'`p = {p} <= v = {v} < q = {q}`：v 到 q-1 才合法，加 `q - v = {q - v}`'
    return ''


CONFIG = dict(
    num=3305, title='元音辅音字符串计数 I', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='两个变长窗口 · 固定左端点',
    tags=[],
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
    call='Solution().countOfSubstrings("aeiouqa", 1)',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='word', h=210,
             pointers={'index': 'blue', 'v': 'pink', 'p': 'green', 'q': 'orange'},
             color=lambda S, i, c: 'purple' if c not in 'aeiou' else None),
        dict(type='map', var='vowel_freq', h=190, fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('p', 'p', 'green'), ('q', 'q', 'orange'),
           'vowel', 'consonant', ('res', 'res', 'green')],
    captions={
        'vowel_freq = {': '`vowel_freq`：窗口里五个元音各出现几次',
        'consonant = 0': '`consonant`：窗口内辅音个数',
        'vowel = 0': '`vowel`：已经凑齐的元音种类数',
        'v = -1': '`v`：元音窗口的右边界，==刚好凑齐 5 种元音的最小右端==',
        'p = -1': '`p`：辅音窗口右边界，==刚好含 k 个辅音的最小右端==',
        'q = 0': '`q`：p 之后下一个辅音的位置，p 到 q-1 都含同样 k 个辅音',
        'for index, char': '固定左端点 `index = {index}`（`{char}`），看它能形成多少合法子串',
        'while v + 1 < n and vowel < 5': lambda S, B, r: (f'元音只凑了 `{S.vowel}` 种，右边界 `v` 继续右扩' if S.vowel < 5 and S.v + 1 < S.n
                                                       else f'元音已凑齐 5 种（或到末尾）→ `v = {S.v}` 停下'),
        'if word[v + 1] in vowel_freq': '`{word[v + 1]}` 是元音吗？{word[v + 1] in vowel_freq}',
        'vowel_freq[word[v + 1]] += 1': '元音 `{word[v + 1]}` 计数 +1',
        'if vowel_freq[word[v + 1]] == 1': '第一次出现吗？是 → 元音种类 `vowel` +1',
        'v += 1': '`v` 右移到 {v}',
        'if vowel < 5': lambda S, B, r: ('元音不够 5 种：再往右也凑不齐 → ==直接 break==' if S.vowel < 5 else '元音已凑齐，继续'),
        'if k == 0': 'k 是 0 吗？{k == 0}：k=0 时辅音窗口就是空窗口',
        26: lambda S, B, r: (f"左端点 `{S.char}` 是元音：k=0 时 `p = index = {S.index}`" if S.char in S.vowel_freq
                                                  else f"左端点 `{S.char}` 是辅音：k=0 不可能合法，`p = None`，这一轮不更新答案"),
        'p = index': '`p = {p}`',
        'p = None': '`p = None`',
        'while p + 1 < n and consonant < k': lambda S, B, r: (f'辅音只有 `{S.consonant}` < k=`{S.k}`，`p` 继续右扩' if S.consonant < S.k
                                                              else f'辅音恰好 `{S.k}` 个 → `p = {S.p}` 停下'),
        'if word[p + 1] not in vowel_freq': '`{word[p + 1]}` 是辅音吗？{word[p + 1] not in vowel_freq}',
        'consonant += 1': '辅音数 `consonant` = {consonant}',
        'p += 1': '`p` 右移到 {p}',
        'if consonant < k': lambda S, B, r: ('辅音凑不够 k 个：后面的左端点更不行 → ==直接 break==' if S.consonant < S.k else '辅音够了，继续'),
        'if p is not None': 'p 存在吗？{p is not None}',
        'if q <= p': lambda S, B, r: (f'`q = {S.q} <= p = {S.p}`：q 过期了，重新找 p 之后第一个辅音' if S.q <= S.p else f'`q = {S.q} > p`：q 仍有效，不用重找'),
        'q = p + 1': '`q` 从 `p + 1 = {q}` 开始找',
        'while q < n and word[q] in vowel_freq': lambda S, B, r: (f'`word[{S.q}]` 是元音，`q` 继续右移' if S.q < S.n and S.word[S.q] in S.vowel_freq
                                                                  else f'遇到辅音（或到末尾）→ `q = {S.q}`'),
        'q += 1': '`q` → {q}',
        'if v < p': lambda S, B, r: f'比较 `v = {S.v}` 和 `p = {S.p}`：' + ('元音早就够了，右端点可取 p 到 q-1' if S.v < S.p else '元音后够，不满足 v < p'),
        'res += q - p': '右端点取 p..q-1，共 `q - p = {q - p}` 个子串 → `res = {res}`',
        'elif v < q': '`v = {v} < q = {q}` ？{v < q}：右端点只能取 v..q-1',
        'res += q - v': '右端点取 v..q-1，共 `q - v = {q - v}` 个子串 → `res = {res}`',
        50: '左端点 `{char}` 要离开窗口：它是元音吗？{char in vowel_freq}',
        'vowel_freq[char] -= 1': '左端点 `{char}` 出窗口：它的元音计数 -1',
        'if vowel_freq[char] == 0': lambda S, B, r: (f'`{S.char}` 的计数降到 0 → 元音种类 `vowel` -1，下一轮 v 要重新右扩' if S.vowel_freq[S.char] == 0 else f'`{S.char}` 还剩 `{S.vowel_freq[S.char]}` 个，元音仍凑齐'),
        'vowel -= 1': '`vowel = {vowel}`',
        'elif k > 0': '左端点是辅音且 k > 0：{k > 0}',
        'consonant -= 1': '辅音出窗口，`consonant = {consonant}`',
        'return res': '一共 `{res}` 个合法子串',
    },
    max_steps=100,
    skip=['v += 1', 'p += 1', 'q += 1'],
    cards=dict(
        one_liner='固定左端点，两个窗口各找一个最小右边界，相减数个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `word` 和整数 `k`，数有多少子串：五个元音都至少出现一次，且恰好 `k` 个辅音',
                 '示例：`word = "aeiou", k = 0` → `1`',
                 '本视频：`"aeiouqa", k = 1` → `3`'],
        quote='需两个变长的滑动窗口。固定住窗口的左边界：处理元音字母的窗口右边界需要保证窗口内每种元音字母至少都出现了一次，且这个右边界最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['`v`：元音凑齐的最小右端；`p`：辅音恰好 k 个的最小右端；`q`：p 之后下一个辅音',
              '`v < p` 加 `q - p`；`p <= v < q` 加 `q - v`；`q <= v` 没有合法子串',
              '左端点右移时只更新计数，两个右边界都不回退'],
        summary=['时间 `O(n)`，空间 `O(1)`：`v`、`p`、`q` 都只向右走',
                 '易错：k=0 时 p 取决于左端点本身是不是元音，是辅音就不能更新答案',
                 '元音或辅音不够时直接 `break`，后面的左端点只会更不够',
                 '原文已是 Python 3 可运行写法，代码未做修改'],
    ),
)
