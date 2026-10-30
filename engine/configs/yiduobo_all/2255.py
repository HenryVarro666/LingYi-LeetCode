WORDS = ["a", "b", "c", "ab", "bc", "abc"]

_FRESH = []


def _for(S, B, r):
    if _FRESH:
        _FRESH.clear()
        return f'看 `word` 的第 `{S.index}` 个字符 `"{S.char}"`'
    if S.index == B.get('index'):
        return '`word` 的字符都比完了，没有不同 → 跳出循环'
    return f'看 `word` 的第 `{S.index}` 个字符 `"{S.char}"`'


def _cmp(S, B, r):
    i, c, t = S.index, S.char, S.s[S.index]
    if c != t:
        return f'`word[{i}] = {c}` ≠ `s[{i}] = {t}` → ==不匹配=='
    return f'`word[{i}] = {c}` == `s[{i}] = {t}`，这一位对上了'


CONFIG = dict(
    num=2255, title='统计是给定字符串前缀的字符串数目', difficulty='Easy', category='字符串',
    author='yiduobo', technique='朴素逐字符比较',
    tags=[],
    code='''
class Solution(object):
    def countPrefixes(self, words, s):

        res = 0
        for word in words:
            if len(word) > len(s):
                continue

            flag = True
            for index, char in enumerate(word):
                if char != s[index]:
                    flag = False
                    break
            
            if flag:
                res += 1
        
        return res
''',
    call='Solution().countPrefixes(%r, "abc")' % (WORDS,),
    expect=3,
    views=[
        dict(type='array', var='words', label='words（蓝 = 当前单词，绿 = 已确认是前缀）', cell=96, pointers={'words.index(word) if word is not None else None': 'blue'}, pointer_labels={'words.index(word) if word is not None else None': 'word'},
             color=lambda S, i, v: 'blue' if S.get('word') == v else None,
             dim=lambda S, i, v: 'word' in S and i < S['words'].index(S['word']) and not S['s'].startswith(v), h=190),
        dict(type='string', var='s', label='s（粉色箭头 = 正在比较的位置 index）', cell=84, pointers={'index if _line in (10, 11, 12, 13) else None': 'pink'}, pointer_labels={'index if _line in (10, 11, 12, 13) else None': 'index'}, h=170),
        dict(type='string', var='word', label='word（当前单词，逐字符与 s 对齐比较）', cell=84, pointers={'index if _line in (10, 11, 12, 13) else None': 'pink'}, pointer_labels={'index if _line in (10, 11, 12, 13) else None': 'index'},
             color=lambda S, i, v: ('green' if ((S['_line'] in (10, 11, 12, 13) and i < S.get('index', -1)) or (S.get('flag') and S['_line'] in (15, 16))) else None), h=170),
    ],
    watch=[('word', 'word', 'blue'), ('index', 'index', 'pink'), ('flag', 'flag'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计前缀个数',
        'for word in words': lambda S, B, r: ('`words` 都看完了，循环结束' if B.get('word') == S.word else f'取下一个单词 `word = "{S.word}"`'),
        'if len(word) > len(s)': lambda S, B, r: ('`len(word) = {}` > `len(s) = {}`：比 s 还长，不可能是前缀 → 跳过'.format(len(S.word), len(S.s))
                                                   if len(S.word) > len(S.s) else '`len(word) = {}` ≤ `len(s) = {}`，有可能是前缀，继续逐字符比'.format(len(S.word), len(S.s))),
        'continue': '换下一个单词',
        'flag = True': lambda S, B, r: _FRESH.append(1) or f'先假设 `"{S.word}"` 是前缀',
        'for index, char in enumerate(word)': _for,
        'if char != s[index]': _cmp,
        'flag = False': '有一位不同，`"{word}"` 不是前缀',
        'break': '不用再比后面的字符了，直接跳出',
        'if flag': lambda S, B, r: ('每一位都对上了 → `"{}"` ==是前缀==，计数'.format(S.word) if S.flag else '`flag` 是 False → 不计数'),
        'res += 1': '`res` → {res}',
        'return res': '所有单词检查完，返回 `{res}`',
    },
    cards=dict(
        one_liner='数据很小，直接逐个单词、逐个字符和 s 对比',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['给字符串数组 `words` 和字符串 `s`，数出 `words` 中是 `s` 的==前缀==的个数',
                 '重复的单词要重复计数',
                 '示例：`words = [a,b,c,ab,bc,abc]`，`s = "abc"` → `3`'],
        quote='由于题目中字符串的长度很短，同时words中单词的数量也很少，因此可以使用朴素算法，遍历words中的每个单词然后判断其是否为s的前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看长度：比 `s` 长的单词一定不是前缀，直接 `continue`',
              '否则从头逐字符比较，只要有一位不同就把 `flag` 置 False 并 `break`',
              '比完 `flag` 仍为 True，说明是前缀，`res += 1`'],
        after=[dict(heading='另一种思路：trie 树', lines=[
            '前缀匹配问题也可以用 trie 树：先把 `words` 都插入，单词末尾打标记',
            '再让 `s` 在树上走，路径上有标记的节点数 = 答案',
            '本题数据很小，所以作者实际用的是朴素算法'])],
        summary=['时间 `O(nm)`，空间 `O(1)`',
                 '易错：必须先判断 `len(word) > len(s)`，否则 `s[index]` 会越界',
                 '易错：`flag` 每个单词都要重新置为 True',
                 '原文为 Python 2 风格，代码无需改动，直接运行'],
    ),
)
