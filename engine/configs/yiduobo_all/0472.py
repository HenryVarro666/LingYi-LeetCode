WORDS = ["a", "b", "ab", "abc"]


def _piece(S):
    w, a, p = S.get('word'), S.get('start_pos'), S.get('pos')
    if not isinstance(w, str):
        return '依次取出每个单词，判断它能不能由 `word_set` 里的更短单词拼成'
    if a is None:
        return f'当前单词 `{w}`：`f` 全是 None，表示从各位置开始的结果==还没算过=='
    if p is None:
        return f'从位置 {a} 开始：整个后缀 `{w[a:]}` 是不是 `word_set` 里的词？'
    return f'试探：前缀 `{w[a:p] or "(空)"}`（`word[{a}:{p}]`）是词吗？是的话，从 {p} 继续往后拆'


def _win(S):
    a, p = S.get('start_pos'), S.get('pos')
    if a is None or p is None or p <= a:
        return None
    return a


def _winr(S):
    a, p = S.get('start_pos'), S.get('pos')
    if a is None or p is None or p <= a:
        return None
    return p - 1


CONFIG = dict(
    num=472, title='连接词', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按长度排序 + set + 记忆化搜索',
    tags=['动态规划', '常用数据结构'],
    code='''
class Solution(object):
    def findAllConcatenatedWordsInADict(self, words):

        if not words:
            return []

        words = sorted(words, key=lambda d:len(d))
        word_set = set()
        res = []
        for word in words:
            if not word:
                continue
            f = [None] * len(word)
            if self.check(word, 0, word_set, f):
                res.append(word)
            else:
                word_set.add(word)

        return res

    def check(self, word, start_pos, word_set, f):
        if f[start_pos] is not None:
            return f[start_pos]
        if word[start_pos:] in word_set:
            f[start_pos] = True
            return True

        for pos in range(start_pos, len(word)):
            if word[start_pos:pos] in word_set:
                if self.check(word, pos, word_set, f):
                    f[start_pos] = True
                    return True
            
        f[start_pos] = False
        return False
''',
    call=f'Solution().findAllConcatenatedWordsInADict({WORDS!r})',
    expect=['ab'],
    skip=['for pos in range', 'if not word:', 'word_set = set()', 'res = []', 'if not words'],
    max_steps=90,
    views=[
        dict(type='calls', h=140, hide=('word_set', 'f')),
        dict(type='string', var=lambda S: S['word'] if isinstance(S.get('word'), str) else '', label='word（框 = 正在试的前缀 word[start_pos:pos]）', h=270, cell=80,
             pointers={'start_pos': 'blue', 'pos': 'pink'}, window=(_win, _winr)),
        dict(type='array', var=lambda S: S['f'] if isinstance(S.get('f'), list) else [], label='f[i]：从 i 开始能否拆成词（点 = None 没算过，蓝 = 当前 start_pos）', h=190, cell=70, index=True,
             color=lambda S, i, v: 'green' if v is True else 'pink' if v is False else ('blue' if i == S.get('start_pos') else None)),
        dict(type='set', var='word_set', label='word_set（已确认“不是连接词”的短词）', h=130, fmt=lambda x: repr(x), font=28),
        dict(type='array', var='res', label='res（连接词）', h=110, cell=56),
    ],
    watch=[('word', lambda S: S.get('word') if isinstance(S.get('word'), str) else '', 'blue'),
           ('start_pos', 'start_pos', 'blue'), ('pos', 'pos', 'pink')],
    captions={
        4: '有单词才处理',
        7: '==按长度从短到长排序==：长词才可能由短词拼成，所以短的先判断、先放进 set：`{words}`',
        8: '`word_set`：保存已处理过的短词',
        10: lambda S, B, r: (f'取下一个单词 `{S.word}`' if 'word' in S and S.word != B.get('word') else '所有单词都判断完了'),
        13: '`f` 记忆化：`f[i]` 表示 `word[i:]` 能否由 set 里的词拼成，初始都是 None',
        14: lambda S, B, r: (f'`check(word, 0, ...)`：`{S["word"]}` 能由 set 里的词拼成吗？' if 'word' in S else ''),
        15: '能拼成 → ==是连接词==，加入 `res`：`{res}`',
        17: '不能拼成 → 它只能当“零件”，加入 `word_set`（它不进 res）',
        19: '返回所有连接词 `{res}`',
        22: lambda S, B, r: (f'`f[{S.start_pos}] = {S.f[S.start_pos]}`：之前算过 → ==直接返回，不再重复搜索==' if S.f[S.start_pos] is not None
                             else f'`f[{S.start_pos}]` 还是 None，没算过，往下算'),
        23: '命中记忆，返回 `{ret}`',
        24: lambda S, B, r: (f'后缀 `{S.word[S.start_pos:]}` 在 set 里 → ==整段后缀本身就是一个词==，拆分成功'
                             if S.word[S.start_pos:] in S.word_set else f'后缀 `{S.word[S.start_pos:]}` 不在 set 里，继续枚举第一刀切在哪'),
        25: '`f[{start_pos}] = True`',
        26: '这一段能拆 → 返回 True',
        29: lambda S, B, r: (f'枚举切点 `pos = {S.pos}`：前缀 `{S.word[S.start_pos:S.pos] or "(空)"}` 是 set 里的词 → 剩下的 `word[{S.pos}:]` 交给递归' if S.word[S.start_pos:S.pos] in S.word_set
                             else f'枚举切点 `pos = {S.pos}`：前缀 `{S.word[S.start_pos:S.pos] or "(空)"}` 不是词，换下一个切点'),
        30: lambda S, B, r: f'递归判断从 `{B.pos}` 开始的后缀 `{S.word[B.pos:]}` 能否拆开',
        31: '后缀也能拆 → `f[{start_pos}] = True`，==提前结束==',
        32: '返回 True',
        34: '所有切点都试过了，没有一种能拆 → `f[{start_pos}] = False`，==记住失败==，下次直接用',
        35: '返回 False',
    },
    cards=dict(
        one_liner='短词先入库，长词用 set 查前缀、记忆化递归拆后缀',
        complexity='时间约 `O(L^2)`/词（L 为词长，含切片），空间 `O(L)`',
        problem=['给定不含重复词的字符串数组 `words`，找出其中所有的==连接词==',
                 '连接词：完全由数组里至少两个更短的单词拼接而成',
                 '本视频：`["a","b","ab","abc"]` → `["ab"]`（`abc` 拆不成）'],
        quote='首先对所有单词按长度从短到长进行排序，这一步的理由是只可能是较长的单词由较短的单词组成，因此优先判断短的单词。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，处理到某个词时，==set 里恰好是所有比它短（或等长）的词==',
              '`check(word, start_pos)`：先看整个后缀是不是词，再枚举切点 `pos`，前缀是词就递归后缀',
              '`f[start_pos]` 记录成功或失败，同一位置不会重复搜索；拆不成的词放进 set 当零件'],
        summary=['时间：每个词最多 `L` 个起点 × `L` 个切点 × 切片 `O(L)`，即 `O(L^3)` 量级；`f` 记忆化避免指数爆炸',
                 '易错：拆不成的词才加入 `word_set`；连接词本身不加入（它由别的词拼成，没必要当零件）',
                 '易错：必须先排序，否则长词判断时短零件还没入 set',
                 '`pos` 从 `start_pos` 开始，第一个前缀是空串，不在 set 里，不会误判',
                 '原文已是 Python 3 可运行写法，无修改；上面的 trie 也可替代 set'],
    ),
)
