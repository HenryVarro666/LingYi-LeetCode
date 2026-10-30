def _s(x):
    return x.replace(' ', '*') if isinstance(x, str) else x


def _top(S):
    if 'searchWord' in S:
        w = S['searchWord']
        t = f"，替换成 `\"{_s(S['tmp'])}\"`" if 'tmp' in S and S.get('_line', 0) >= 16 else ''
        return f'search(`"{w}"`){t}'
    if 'word' in S:
        t = f"，替换成 `\"{_s(S['tmp'])}\"`" if 'tmp' in S and S.get('_line', 0) >= 11 else ''
        return f'buildDict：当前单词 `"{S["word"]}"`{t}'
    return 'buildDict(`["hit", "hot", "dog"]`)　然后 search `dot`、`hit`、`dog`'


def _formula(S):
    if 'searchWord' not in S or 'tmp' not in S or S.get('_line', 0) < 16:
        return '把每个位置换成特殊字符（这里画成 `*`），统计每个替换结果出现的次数'
    c = S['self.change_word_dict'].get(S['tmp'], 0)
    w = S['self.word_dict'].get(S['searchWord'], 0)
    ok = c - w > 0
    return (f"`cnt[\"{_s(S['tmp'])}\"] − word_dict[\"{S['searchWord']}\"] = {c} − {w} = {c - w}`"
            + ('　→ ==有其他单词==' if ok else '　→ 没有别的单词'))


def _if(S, B, ret):
    c = S.self.change_word_dict.get(S.tmp, 0)
    w = S.self.word_dict.get(S.searchWord, 0)
    t = _s(S.tmp)
    if c - w > 0:
        if w:
            return f'`"{t}"` 出现 {c} 次，减去 `"{S.searchWord}"` 自己的 {w} 次还剩 {c - w} → ==另有单词能换出来=='
        return f'`"{t}"` 出现 {c} 次，`"{S.searchWord}"` 不在词表里 → 词表中有单词只差这一位'
    if c and w:
        return f'`"{t}"` 出现 {c} 次，但==全是 {S.searchWord} 自己贡献的== → 不算'
    return f'`"{t}"` 出现 {c} 次 → 没有单词只差这一位'


CONFIG = dict(
    num=676, title='实现一个魔法字典', difficulty='Medium', category='设计',
    author='yiduobo', technique='通配符替换 + 计数 · 减去自身',
    tags=['字节30天'],
    code='''
class MagicDictionary(object):

    def __init__(self):
        self.word_dict = {}
        self.change_word_dict = {}

    def buildDict(self, dictionary):
        for word in dictionary:
            self.word_dict[word] = 1
            for index in range(len(word)):
                tmp = word[:index] + ' ' + word[index + 1:]
                self.change_word_dict[tmp] = self.change_word_dict.get(tmp, 0) + 1

    def search(self, searchWord):
        for index in range(len(searchWord)):
            tmp = searchWord[:index] + ' ' + searchWord[index + 1:]
            if self.change_word_dict.get(tmp, 0) - self.word_dict.get(searchWord, 0) > 0:
                return True

        return False
''',
    call='''md = MagicDictionary()
md.buildDict(["hit", "hot", "dog"])
[md.search("dot"), md.search("hit"), md.search("dog")]''',
    expect=[True, True, False],
    skip=['for index in range(len(word))', 'for index in range(len(searchWord))'],
    views=[
        dict(type='text', size=28, h=64, fn=_top),
        dict(type='map', var='self.word_dict', font=28, h=120, label='word_dict：原始词表',
             fmt=lambda k, v: f'"{k}"'),
        dict(type='map', var='self.change_word_dict', font=28, h=260,
             label='change_word_dict（记作 cnt）：替换结果 → 出现次数（* 是特殊字符）',
             fmt=lambda k, v: f'"{_s(k)}": {v}'),
        dict(type='text', size=26, h=90, lines=2, fn=_formula),
    ],
    watch=[('index', 'index', 'cyan'), ('tmp', lambda S: _s(S['tmp']), 'yellow')],
    captions={
        'self.word_dict = {}': '`word_dict`：记录原始词表里有哪些单词',
        'self.change_word_dict = {}': '`change_word_dict`：每个“替换一位后的结果”出现了几次',
        'for word in dictionary': lambda S, B, r: (f'处理单词 `"{S.word}"`' if 'word' not in B or B.word != S.word
                                                   else '词表处理完毕'),
        'self.word_dict[word] = 1': '`"{word}"` 记入原始词表',
        11: lambda S, B, r: f'把第 `{S.index}` 位换成特殊字符：`"{S.word}"` → `"{_s(S.tmp)}"`',
        12: lambda S, B, r: f'`cnt["{_s(S.tmp)}"]` → `{S.self.change_word_dict[S.tmp]}`'
                            + ('：==两个单词只差这一位，撞到同一个 key==' if S.self.change_word_dict[S.tmp] > 1 else ''),
        16: lambda S, B, r: (f'search(`"{S.searchWord}"`)：第 `{S.index}` 位换成特殊字符 → `"{_s(S.tmp)}"`'),
        17: _if,
        'return True': '找到了：换掉第 `{index}` 位能变成词表里的==其他==单词 → `True`',
        'return False': '每一位都试过了，除了它自己没有别的单词 → `False`',
    },
    max_steps=60,
    cards=dict(
        one_liner='每个位置换成通配符计数；查询时减去单词自己的那一份',
        complexity='build `O(Σ L²)`，search `O(L²)`（拼接字符串），空间 `O(Σ L²)`',
        problem=['`buildDict(dictionary)` 存入词表；`search(word)` 判断：能否==恰好改一个字母==变成词表中的某个单词',
                 '必须改一个字母：`search("hello")` 不能匹配 `"hello"` 自己',
                 '本视频：词表 `["hit","hot","dog"]`，查 `dot`(T)、`hit`(T)、`dog`(F)'],
        quote='查找替换结果在dict中出现的次数。==若这个次数大于这个单词本身在原始词表中出现的次数==，那么说明至少有一个其他单词可以进行替换。',
        quote_src='—— yiduobo 题解原文',
        idea=['`hit`、`hot` 第 1 位换掉后都是 `h*t` → 只差一位的单词会撞到同一个 key',
              'search 时同样逐位替换，查 `cnt[替换结果]`',
              '单词本身在词表里时，它自己也贡献了 1 次，==要减掉==，剩下的才是“别的单词”'],
        summary=['设词长 `L`：每个单词产生 `L` 个替换结果，每个拼接 `O(L)`',
                 '易错：不减去自身，`search("dog")` 会因为 `dog` 自己而误判为 True',
                 '特殊字符要选单词里不会出现的（原文用空格）',
                 '原文为 Python 2 写法：只删去了文档字符串和 LeetCode 模板注释，逻辑未改'],
    ),
)
