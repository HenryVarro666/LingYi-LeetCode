CONFIG = dict(
    num=2227, title='加密解密字符串', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='逆向思维 · 先加密字典再哈希统计',
    tags=['灵神题单·贪心与思维', '难度分 1945'],
    code='''
class Encrypter(object):

    def __init__(self, keys, values, dictionary):
        
        self.mapping = {}
        for index in range(len(keys)):
            self.mapping[keys[index]] = values[index]

        self.en_dict = {}
        for word in dictionary:
            en_word = self.encrypt(word)
            if en_word is not None:
                self.en_dict[en_word] = self.en_dict.get(en_word, 0) + 1

    def encrypt(self, word1):
        res = []
        for char in word1:
            if char not in self.mapping:
                return None
            res.append(self.mapping[char])
        
        return ''.join(res)

    def decrypt(self, word2):
        return self.en_dict.get(word2, 0)
''',
    call='''e = Encrypter(['a','b','c','d'], ["ei","zf","ei","am"], ["abd","cbd","xb","dd"])
r1 = e.encrypt("abd")
r2 = e.decrypt("eizfam")
[r1, r2]''',
    expect=['eizfam', 2],
    views=[
        dict(type='map', var='self.mapping', label='mapping（字符 → 两位密文）', fmt=lambda k, v: f"'{k}' → {v}", h=110, font=30),
        dict(type='map', var='self.en_dict', label='en_dict（密文 → 字典里有几个词加密成它）', fmt=lambda k, v: f"{k}: {v}", h=110, font=30),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"加密 `{S['word']}` → `{S['en_word']}`" if 'word' in S and 'en_word' in S and S.get('_line') in (11, 12)
                           else (f"加密 `{S['word1']}`，已拼出 `{''.join(S['res'])}`" if 'word1' in S and 'res' in S
                                 else (f"解密 `{S['word2']}`：直接查 `en_dict`" if 'word2' in S else '')))),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=[('char', 'char', 'blue'), ('res', 'res', 'pink'), ('en_word', 'en_word', 'green'), ('word2', 'word2', 'orange')],
    max_steps=80,
    skip=['self.mapping = {}', 'self.en_dict = {}'],
    captions={
        'for index in range': lambda S, B, r: (f"第 `{S["index"]}` 对：`keys[{S["index"]}]` 配 `values[{S["index"]}]`" if len(S["self"].mapping) <= S["index"] else '四对都配好了，加密表建完'),
        'self.mapping[keys[index]]': '`{keys[index]}` → `{values[index]}`，加密表有 {len(self.mapping)} 项',
        'for word in dictionary': '取字典里的词 `{word}`，==先加密它==',
        'en_word = self.encrypt': '调用 `encrypt("{word}")`，看这个词能不能加密',
        'if en_word is not None': lambda S, B, r: (f'`{S.word}` 的密文是 `{S.en_word}`，要统计' if S.en_word is not None else '加密失败（`None`），这个词永远不会被解密出来，跳过'),
        'self.en_dict[en_word]': '`en_dict[{en_word}]` = =={self.en_dict[en_word]}==：这个密文又多一个字典词',
        'res = []': '用列表收集每个字符的密文',
        'for char in word1': lambda S, B, r: (f"取下一个字符 `{S.char}`" if len(S.res) < len(S.word1)
                                              else f"`{S.word1}` 的字符都处理完了"),
        'if char not in self.mapping': lambda S, B, r: (f"`{S.char}` 不在 keys 里 → 无法加密" if S.char not in S['self'].mapping
                                                       else f"`{S.char}` 在 keys 里，可以加密"),
        'return None': '字符不在 `keys` 里，整个词加密失败，返回 `None`',
        'res.append': '追加 `{self.mapping[char]}`，`res` = {res}',
        "return ''.join": '拼接得到密文 `{ret}`',
        'return self.en_dict.get': '解密不用枚举：字典词加密后等于 `{word2}` 的有 =={ret}== 个',
    },
    cards=dict(
        one_liner='解密一对多很麻烦，不如先把字典词全加密',
        complexity='构造 `O(字典总长)`，加密 `O(n)`，解密 `O(1)`',
        problem=['加密：每个字符按 `keys → values` 换成两位密文',
                 '解密：密文可能对应多个原文，统计有几个落在字典里',
                 '示例：`"eizfeiam"` 解密得 `2`'],
        quote='字典的规模也很小，因此不妨逆向思维，先求出字典中每个词加密后是什么样的，并使用哈希表统计这些密文可以由多少个字典中的词加密得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['加密一对一，解密一对多：正向解密要枚举所有组合',
              '只关心结果落在字典里的个数，字典又小 → 把字典全部加密',
              '`en_dict` 记录各密文出现次数，解密就是 `get`'],
        summary=['构造时遍历字典并加密，`encrypt` 失败返回 `None`，这样的词不计入',
                 '`decrypt` 用 `.get(word2, 0)`：查不到时返回 0',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神用 `Counter`，加密失败返回 `""`；yiduobo 用手写字典计数'],
    ),
)
