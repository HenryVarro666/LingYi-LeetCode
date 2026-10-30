def _loop(S, B, r):
    if 'index' in B and B['index'] == S.index and B['word'] == S.word:
        return f'`{S.word}` 的每个字符都数完了，计数表：`{S.char_dict}`'
    return f'看下标 `{S.index}` 的字符 `{S.char}`'


CONFIG = dict(
    num=893, title='特殊等价字符串组', difficulty='Medium', category='字符串',
    author='yiduobo', technique='奇数位转大写 + 字符计数当哈希键',
    tags=[],
    code='''
class Solution(object):
    def numSpecialEquivGroups(self, A):

        word_set = set()
        res = 0
        for word in A:
            char_dict = {}
            for index, char in enumerate(word):
                if index & 1:
                    char = chr(ord(char) - 32)
                char_dict[char] = char_dict.get(char, 0) + 1
            word_set.add(tuple(sorted(char_dict.items())))

        return len(word_set)
''',
    call='Solution().numSpecialEquivGroups(["abcd", "cdab", "cbad", "xyzz", "zzxy", "zzyx"])',
    expect=3,
    views=[
        dict(type='array', var='A', h=150, label='A（黄 = 当前 word）',
             color=lambda S, i, v: 'yellow' if S.get('word') == v else None),
        dict(type='string', var='word', h=170, label='word（蓝 = 当前 index）', pointers={'index': 'blue'}),
        dict(type='map', var='char_dict', h=190, label='char_dict：大写 = 奇数位，小写 = 偶数位', fmt=lambda k, v: f'{k} : {v}'),
        dict(type='set', var='word_set', h=220, label='word_set：已出现的「签名」', fmt=lambda x: ''.join(f'{c}{n}' for c, n in x)),
    ],
    watch=['word', 'index', 'char', ('组数', lambda S: len(S['word_set']) if 'word_set' in S else 0, 'green')],
    captions={
        'word_set = set()': '`word_set` 存每个字符串的「签名」，等价的字符串签名相同',
        'res = 0': '`res` 在这份代码里没用上，答案是 `len(word_set)`',
        'for word in A': '处理下一个字符串 `{word}`',
        'char_dict = {}': '为 `{word}` 新建计数表：统计奇数位、偶数位上各字符的个数',
        'for index, char': _loop,
        'if index & 1': lambda S, B, r: (f'下标 `{S.index}` 是==奇数位== → 转成大写，和偶数位区分开' if S.index & 1 else f'下标 `{S.index}` 是偶数位 → 保持小写'),
        'char = chr': '奇数位字符转大写：`{B.char}` → `{char}`',
        'char_dict[char]': '`{char}` 的计数 +1 → `{char_dict[char]}`',
        'word_set.add': '`sorted` 把计数表排成固定顺序、变成元组才放得进集合 → 签名 `{tuple(sorted(char_dict.items()))}`；==奇偶位组成相同，签名就相同==',
        'return len': '`word_set` 里有 `{len(word_set)}` 种签名 → 共 `{len(word_set)}` 个特殊等价组',
    },
    cards=dict(
        one_liner='奇偶位上的字符可任意交换，只看各自的字符组成',
        complexity='时间 `O(n·L log L)`，空间 `O(n·L)`',
        problem=['一次操作可交换同一字符串中下标同奇偶的两个字符；能互相变出的字符串是特殊等价的',
                 '把 `A` 划分成最少的特殊等价组，返回组数',
                 '示例：`[abcd,cdab,cbad,xyzz,zzxy,zzyx]` → `3`'],
        quote='只要两个字符串奇数位上的字符组成一致，同时偶数位上的字符组成一致，那么这两个字符串就是特殊等价字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数位字符转成大写，和偶数位字符区分开',
              '统计每个字符出现次数，排序后得到唯一的签名',
              '签名相同就是同一组，放进集合，答案是集合大小'],
        summary=['时间 `O(n·L log L)`，空间 `O(n·L)`',
                 '`abcd` 与 `cdab`：偶数位 `{a,c}`、奇数位 `{b,d}` 相同 → 同一组',
                 '`sorted(char_dict.items())` 保证键的顺序固定，字典本身不能哈希，要转成元组',
                 '原文为 Python 2 风格，代码无需修改；变量 `res` 没有使用'],
    ),
)
