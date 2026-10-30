def _loop(name, text, done):
    def f(S, B, ret):
        if name in B and B[name] == S[name]:
            return done
        return text.format(**{name: S[name]})
    return f


def _q(S):
    pre, suf = S.get('prefix'), S.get('suffix')
    if pre is None:
        return '把每个单词的「前缀 + 空格 + 后缀」全部存进哈希表，查询就是一次 `get`'
    return f"查询 `f({pre!r}, {suf!r})`：拼出键 ==`{pre}|{suf}`==（`|` 代表中间的空格）"


CONFIG = dict(
    num=745, title='后缀和前缀搜索', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举所有前后缀组合存哈希表',
    tags=[],
    code='''
class WordFilter(object):

    def __init__(self, words):
        self.word_dict = {}
        for index, word in enumerate(words):
            l = len(word)
            for i in range(l + 1):
                for j in range(l + 1):
                    self.word_dict[word[:i] + ' ' + word[j:]] = index

    def f(self, prefix, suffix):
        return self.word_dict.get(prefix + ' ' + suffix, -1)
''',
    call='''wf = WordFilter(["ab", "a"])
[wf.f("a", "b"), wf.f("a", ""), wf.f("b", "a")]''',
    expect=[0, 1, -1],
    skip=['l = len(word)'],
    views=[
        dict(type='array', var='words', label='words（下标 = 权重，越靠后越大）', h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='text', fn=lambda S: (f"当前：`word[:{S['i']}]` = =={S['word'][:S['i']]!r}== ，`word[{S['j']}:]` = =={S['word'][S['j']:]!r}==" if 'j' in S and 'word' in S and S.get('_line') is not None and 'i' in S else _q(S)), h=90),
        dict(type='map', var='self.word_dict', label='word_dict（键中的 | 是空格；同键后写入的覆盖前面的）',
             fmt=lambda k, v: f'{k.replace(" ", "|")} → {v}', font=24, h=420),
    ],
    watch=['index', 'word', 'i', 'j', 'prefix', 'suffix'],
    captions={
        'self.word_dict = {}': '哈希表：键 = `前缀 + 空格 + 后缀`，值 = 单词下标',
        'for index, word in enumerate': lambda S, B, r: ('所有单词都存完了，哈希表建好' if 'index' in B and B['index'] == S['index'] else f"从头往后扫：==后面的单词权重更大==，直接覆盖前面写入的同名键即可 → 当前 `{S['word']!r}`，权重 `{S['index']}`"),
        'for i in range(l + 1)': _loop('i', '前缀长度 `i = {i}`（0 到 len 都要枚举，包括空前缀）', '这个单词的所有前缀都枚举完了'),
        'for j in range(l + 1)': _loop('j', '后缀起点 `j = {j}`（`word[j:]` 就是一个后缀，`j = len` 即空后缀）', '后缀枚举完了，换下一个前缀'),
        'self.word_dict[': '写入：`{word[:i]!r} + " " + {word[j:]!r}` → 权重 =={index}==（已存在就被覆盖）',
        'return self.word_dict.get': lambda S, B, ret: f"查表 `{S.prefix + ' ' + S.suffix!r}` → ==权重 {ret}==" + ('（没写入过，返回 -1）' if ret == -1 else ''),
    },
    max_steps=75,
    cards=dict(
        one_liner='单词只有 10 个字母：把所有前缀+后缀组合都存下来，查询 O(1)',
        complexity='构造 `O(N·L^3)`，查询 `O(L)`（拼键），`L` 为单词长度',
        problem=['`WordFilter(words)` 用词典初始化；`f(prefix, suffix)` 返回前缀为 `prefix`、后缀为 `suffix` 的单词中==权重（下标）最大==的那个',
                 '没有符合条件的单词就返回 `-1`',
                 '本视频：`words = ["ab", "a"]`，查 `("a","b")`→0，`("a","")`→1，`("b","a")`→-1'],
        quote='对于后缀与前缀相关的问题，经典的做法是使用trie树。不过注意到这里每个单词的长度不超过10，因此直接将所有的后缀与前缀进行组合，然后存入哈希表也是可行的做法。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词长度不超过 10 → 一个单词的「前缀 × 后缀」组合只有 `(L+1)^2` 个',
              '按下标从小到大写入，==后面的单词覆盖前面的==，自然保留最大权重',
              '用空格把前缀和后缀拼成一个键，查询时同样拼接再 `get`'],
        summary=['查询是一次哈希查找，没有匹配就返回 `-1`（`get` 的默认值）',
                 '前缀、后缀都要枚举到 `l`（包含空串），否则查不了只给前缀/后缀的情形',
                 '空间是代价：每个单词存 `(L+1)^2` 个键；单词再长就要改用 trie',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
