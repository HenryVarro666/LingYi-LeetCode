CONFIG = dict(
    num=288, title='单词的唯一缩写', difficulty='Medium', category='设计',
    author='yiduobo', technique='哈希表 + 冲突集合',
    code='''
class ValidWordAbbr(object):

    def __init__(self, dictionary):
        self.dict = {}
        self.multi_key = set()
        for s in dictionary:
            if len(s) > 2:
                key = s[0] + str(len(s) - 2) + s[-1]
            else:
                key = s

            if key in self.dict and self.dict[key] != s:
                self.multi_key.add(key)
            else:
                self.dict[key] = s

    def isUnique(self, word):

        if len(word) > 2:
            key = word[0] + str(len(word) - 2) + word[-1]
        else:
            key = word

        if key in self.multi_key:
            return False

        return self.dict.get(key, word) == word
''',
    call='''v = ValidWordAbbr(["deer", "door", "cake"])
[v.isUnique("dear"), v.isUnique("cart"), v.isUnique("cane"), v.isUnique("make")]''',
    expect=[False, True, False, True],
    views=[
        dict(type='map', var='self.dict', label='dict（缩写 → 单词）', h=150, fmt=lambda k, v: f'{k} → {v}'),
        dict(type='set', var='self.multi_key', label='multi_key（有多个不同单词的缩写）', h=110),
        dict(type='text', fn=lambda S: (f"当前缩写 key = ==`{S['key']}`==" if 'key' in S else ''), h=60),
    ],
    watch=['s', 'word', 'key', ('multi_key', 'self.multi_key', 'red')],
    captions={
        'self.dict = {}': '`dict`：缩写 → 单词',
        'self.multi_key = set()': '`multi_key`：记录哪些缩写对应了==多个不同单词==',
        'for s in dictionary': '取字典里的单词 `{s}`',
        'key = s[0] + str(len(s) - 2) + s[-1]': '长度 > 2：缩写 = 首字母 + 中间字母数 + 尾字母 = ==`{key}`==',
        'key = word[0]': '查询单词 `{word}` 的缩写 = ==`{key}`==（算法和构造时相同）',
        'if key in self.dict and': lambda S, B, r: (
            f'缩写 `{S.key}` 已存在且对应的单词不同 → 冲突' if (S.key in S['self.dict'] and S['self.dict'][S.key] != S.s) else
            f'缩写 `{S.key}` 还没出现过，或对应的是同一个单词 → 没冲突'),
        'self.multi_key.add': '缩写 `{key}` 对应多个单词 → 放入 `multi_key`，以后它都不唯一',
        'self.dict[key] = s': '记录 `{key}` → `{s}`',
        'if key in self.multi_key': lambda S, B, r: (
            f'`{S.key}` 在 `multi_key` 里 → 字典里多个不同单词共用它，一定不唯一，返回 False' if S.key in S['self.multi_key']
            else f'`{S.key}` 不在 `multi_key` 里 → 继续看它对应的单词是不是 `{S.word}` 本身'),
        'return False': '返回 ==False==',
        'return self.dict.get': lambda S, B, r: (
            f"`dict.get({S.key!r}, {S.word!r})` = {S['self.dict'].get(S.key, S.word)!r}"
            + ('（没收录这个缩写，默认取 word 自己）' if S.key not in S['self.dict'] else '（字典里已有别的单词用这个缩写）' if S['self.dict'][S.key] != S.word else '')
            + f' → 和 `{S.word}` 比较，=={r}==')
    },
    cards=dict(
        one_liner='缩写当 key 存哈希表，缩写冲突的单独记下来',
        complexity='构造 `O(总字符数)`，`isUnique` `O(1)`（只算首尾和长度）',
        problem=['单词缩写 = ==首字母 + 中间字母个数 + 尾字母==，长度不超过 2 的单词缩写就是它自己',
                 '给定字典，`isUnique(word)`：字典中==没有其他单词==与 word 缩写相同则为 True',
                 '例：`deer` 和 `door` 缩写都是 `d2r`',
                 '本视频：字典 `deer, door, cake`，查 `dear, cart, cane, make`'],
        quote='若dictionary中有多个单词的缩写一致，那么这个缩写对应的所有单词都不是唯一的。',
        quote_src='—— yiduobo 题解原文',
        idea=['构造时算出每个单词的缩写，存进哈希表 `dict`',
              '同一缩写遇到==不同单词==就加入 `multi_key`，此后这个缩写永远不唯一',
              '查询时：在 `multi_key` 里 → False；否则看 `dict` 里的那个单词是不是 word 自己（没有则视为唯一）'],
        summary=['`isUnique` 每次 `O(1)`，构造一次遍历字典',
                 '易错点：字典里有重复的同一个单词时不算冲突（`dict[key] != s` 才算）',
                 '易错点：字典里没有这个缩写，也要返回 True，所以用 `get(key, word)`',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
