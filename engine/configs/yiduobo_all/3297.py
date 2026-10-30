W1, W2 = 'abcab', 'abc'


def _pe(S):
    """窗口右边界（开区间）：L14-L16 已把 word1[p] 加入 freq1，但 p 还没 +1"""
    return S['p'] + 1 if S['_line'] in (14, 15, 16) else S['p']


def _left(S):
    if 'freq1' not in S:
        return None
    return _pe(S) - sum(S['freq1'].values())


def _win(S):
    return _left(S)


def _wr(S):
    return _pe(S) - 1 if 'freq1' in S else None


def _col(S, i, v):
    if 'freq1' not in S:
        return None
    l = _left(S)
    return 'green' if S['cnt'] >= len(S['freq2']) and l <= i < _pe(S) else None


def _txt(S):
    if 'cnt' not in S:
        return ''
    ok = S['cnt'] >= len(S['freq2'])
    l = _left(S)
    s = f"窗口 `[{l}, {_pe(S)})`：达标字符 `cnt = {S['cnt']}`，需要 `{len(S['freq2'])}` 种 → " + ('==窗口合法==' if ok else '==还不够==')
    return s


CONFIG = dict(
    num=3297, title='统计重新排列后包含另一个字符串的子字符串数目 I', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · cnt 记录达标字符数',
    tags=[],
    code='''
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
''',
    call=f'Solution().validSubstringCount({W1!r}, {W2!r})',
    expect=6,
    views=[
        dict(type='string', var='word1', label='word1（框 = 窗口 [left, p)，绿 = 窗口合法）', cell=96, h=190,
             pointers={'p': 'pink'}, window=(_win, _wr), color=_col),
        dict(type='map', var='freq2', label='freq2（word2 中每个字符需要的个数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='map', var='freq1', label='freq1（窗口里每个字符的个数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='text', h=90, size=30, fn=_txt),
    ],
    watch=['char', ('p', 'p', 'pink'), ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'freq2 = {}': '`freq2` 统计 `word2` 里每种字符需要多少个：子串能重排，只看个数，不看顺序',
        'freq2[char] =': '`freq2` 里 `{char}` 的需求个数 → {freq2[char]}',
        'cnt = 0': '`cnt` = 窗口里已经==达标==的字符种数；不用每次比较整个哈希表',
        'freq1 = {}': '`freq1` 统计当前窗口里每种字符的个数',
        'p = 0': '`p` 是窗口右边界（开区间）：窗口 = `word1[left : p]`，`left` 由外层 for 推进',
        'res = 0': '`res` 累计合法子串数',
        'for char in word1': '枚举左边界：这一轮窗口从 `{char}` 开始，先把右边界 `p` 推到刚好合法',
        'while p < len': lambda S, B, r: (f'`p = {S.p}`、`cnt = {S.cnt} < {len(S.freq2)}`：窗口还不合法 → 继续扩大右边界'
                                           if (S.p < len(S.word1) and S.cnt < len(S.freq2))
                                           else ('`cnt` 已经达标，窗口合法 → 右边界停下' if S.cnt >= len(S.freq2) else '`p` 已到末尾，不能再扩大')),
        'freq1[word1[p]] = freq1': '把 `word1[p] = {word1[p]}` 加入窗口：`freq1[{word1[p]}]` → {freq1[word1[p]]}',
        'if freq1[word1[p]] ==': lambda S, B, r: (f"`{S.word1[S.p]}` 的个数刚好等于需求 `{S.freq2.get(S.word1[S.p], 0)}` → 这种字符刚达标" if S.freq1[S.word1[S.p]] == S.freq2.get(S.word1[S.p], 0)
                                                  else f"`{S.word1[S.p]}` 的个数 `{S.freq1[S.word1[S.p]]}` ≠ 需求 `{S.freq2.get(S.word1[S.p], 0)}` → `cnt` 不变"),
        'cnt += 1': '又有一种字符达标：`cnt` → =={cnt}==',
        'p += 1': '右边界右移：`p` → {p}',
        'if cnt < len(freq2)': lambda S, B, r: ('`cnt < %d`：即使 p 推到末尾也凑不齐 → 之后的左边界更不可能，==跳出循环==' % len(S.freq2) if S.cnt < len(S.freq2)
                                                 else '`cnt` 达标：窗口 `word1[left:p]` 合法，继续统计'),
        'res += ': '合法的最短窗口是 `[left, p)`，右端取 `p-1` 到末尾都合法，共 `{len(word1)} - {p} + 1` = =={len(word1) - p + 1}== 个 → `res` = {res}',
        'freq1[char] -= 1': '左边界右移：把 `{char}` 移出窗口，`freq1[{char}]` → {freq1[char]}',
        'if freq1[char] ==': lambda S, B, r: (f"`{S.char}` 的个数降到 `{S.freq1[S.char]}`，比需求 `{S.freq2.get(S.char, 0)}` 少 1 → 这种字符不再达标" if S.freq1[S.char] == S.freq2.get(S.char, 0) - 1
                                              else f"`{S.char}` 的个数 `{S.freq1[S.char]}` 仍满足需求 `{S.freq2.get(S.char, 0)}`（或本来就不需要）→ `cnt` 不变"),
        'cnt -= 1': '`cnt` 减 1 → =={cnt}==，下一轮右边界要继续向右补齐',
        'return res': '所有左边界处理完，合法子串共 `{res}` 个',
    },
    cards=dict(
        one_liner='子串能重排，只要窗口里每种字符都够数，就合法',
        complexity='时间 `O(n + m)`，空间 `O(26)`',
        problem=['`word1` 的子串 `x` 重排后以 `word2` 为前缀，则 `x` 合法，求合法子串个数',
                 '重排后 `word2` 是前缀 ⇔ `x` 中每种字符的个数都 ≥ `word2` 中的个数',
                 '本视频：`word1 = "abcab"`，`word2 = "abc"` → `6`'],
        quote='注意到子串可以重新排列，那么对于word2中出现的所有字符，只要子串中同样的字符数量充足，那么子串就是合法的。这是一个非常标准的变长滑动窗口的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表 `freq2` 是需求，`freq1` 是窗口里的现状',
              '`cnt` 记已达标的字符种数：某字符个数从 需求-1 变成 需求，`cnt+1`；反过来 `cnt-1`',
              '对每个左边界找最小合法右边界 `p`，则右端点 `p-1..n-1` 共 `n-p+1` 个子串都合法'],
        summary=['时间 `O(n + m)`，空间 `O(26)`（`n`、`m` 是两个字符串长度）',
                 '易错点：`p` 是开区间右端，所以个数是 `len(word1) - p + 1`',
                 '`cnt` 只在个数"刚好等于需求"和"刚好低于需求"时才变化',
                 '窗口凑不齐（`cnt < len(freq2)`）就 `break`：更靠右的左边界只会更难',
                 '代码本身是 Python 3 可直接运行的写法，无需修改'],
    ),
)
