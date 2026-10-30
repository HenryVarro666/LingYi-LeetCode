def _sp(k, v):
    return f'({k[0]!r}, {k[1]:04b}) → {v}'


CONFIG = dict(
    num=966, title='元音拼写检查器', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='三级哈希 · 元音位置状态压缩', tags=[],
    code='''
class Solution(object):
    def spellchecker(self, wordlist, queries):

        word_dict = {}
        for index, word in enumerate(wordlist):
            word_dict[word] = index
        
        low_case_dict = {}
        for index, word in enumerate(wordlist):
            low_case_word = ''.join([x if ord(x) >= 97 else chr(ord(x) + 32) for x in word])
            if low_case_word not in low_case_dict:
                low_case_dict[low_case_word] = index
        
        spell_dict = {}
        for index, word in enumerate(wordlist):
            rest_word = ''
            spell_state = 0
            for p, char in enumerate(word):
                if ord(char) < 97:
                    char = chr(ord(char) + 32)

                if char in ('a', 'e', 'i', 'o', 'u'):
                    spell_state += (1 << p)
                else:
                    rest_word += char
            
            if (rest_word, spell_state) not in spell_dict:
                spell_dict[(rest_word, spell_state)] = index
        
        res = []
        for word in queries:
            if word in word_dict:
                res.append(wordlist[word_dict[word]])
            else:
                low_case_word = ''.join([x if ord(x) >= 97 else chr(ord(x) + 32) for x in word])
                if low_case_word in low_case_dict:
                    res.append(wordlist[low_case_dict[low_case_word]])
                else:
                    rest_word = ''
                    spell_state = 0
                    for p, char in enumerate(word):
                        if ord(char) < 97:
                            char = chr(ord(char) + 32)

                        if char in ('a', 'e', 'i', 'o', 'u'):
                            spell_state += (1 << p)
                        else:
                            rest_word += char
                    
                    if (rest_word, spell_state) in spell_dict:
                        res.append(wordlist[spell_dict[(rest_word, spell_state)]])
                    else:
                        res.append('')
        
        return res
''',
    call='Solution().spellchecker(["KiTe","kite"], ["kite","Kite","keti"])',
    expect=['kite', 'KiTe', 'KiTe'],
    skip=['res = []', "if ord(char) < 97", "char = chr(ord(char) + 32)", "rest_word = ''", "spell_state = 0"],
    max_steps=80,
    views=[
        dict(type='array', var='wordlist', label='wordlist', h=150, cell=100,
             color=lambda S, i, v: 'purple' if S.get('index') == i and S['_line'] in range(5, 34) else None),
        dict(type='map', var='word_dict', label='word_dict（原词→下标，区分大小写）', h=100, font=24),
        dict(type='map', var='low_case_dict', label='low_case_dict（小写词→最早下标）', h=100, font=24),
        dict(type='map', var='spell_dict', label='spell_dict（(辅音串, 元音位置状态)→最早下标）', fmt=_sp, h=110, font=24),
        dict(type='array', var='queries', label='queries', pointers={}, h=150, cell=100,
             color=lambda S, i, v: 'blue' if S.get('word') == v and S['_line'] >= 36 else None),
    ],
    watch=['word', 'low_case_word', 'rest_word', ('state', 'spell_state', 'cyan'), ('res', 'res', 'green')],
    captions={
        'word_dict[word] = index': '`word_dict[{word!r}] = {index}`：记下原词，后面判断==完全匹配==',
        'low_case_dict[low_case_word] = index': '小写词 `{low_case_word}` 第一次出现才记，保证取==最靠前==的匹配',
        'if low_case_word not in low_case_dict': lambda S, B, r: f'`{S.low_case_word}` 已记录过？{"没有，记下" if S.low_case_word not in S.low_case_dict else "已有，跳过（留最靠前的）"}',
        'spell_dict = {}': '第三级：key 是二元组（辅音串, 元音位置的二进制状态）',
        'if char in': lambda S, B, r: f'`{S.char}` 是元音？' + ('是，第 ' + str(S.p) + ' 位记 1' if S.char in 'aeiou' else '不是，当作辅音留下'),
        'spell_state += (1 << p)': '元音在第 `{p}` 位 → `spell_state = {spell_state:04b}`（二进制）',
        'rest_word += char': '辅音留下：`rest_word = {rest_word!r}`',
        'if (rest_word, spell_state) not in spell_dict': lambda S, B, r: f'二元组 `({S.rest_word!r}, {S.spell_state:04b})` ' + ('是新的，记下' if (S.rest_word, S.spell_state) not in S.spell_dict else '已有，跳过'),
        'spell_dict[(rest_word, spell_state)] = index': '`spell_dict[({rest_word!r}, {spell_state:04b})] = {index}`：元音换成什么都不影响这个二元组',
        'res = []': '预处理完毕，开始逐个处理查询',
        'for word in queries': '处理查询 `{word}`',
        'if word in word_dict': lambda S, B, r: f'`{S.word}` 在 word_dict 里？' + ('是：完全匹配' if S.word in S.word_dict else '否：降一级'),
        'res.append(wordlist[word_dict': '完全匹配，答案就是原词 `{res[-1]}`',
        'low_case_word = ': '`{word}` 变全小写：`{low_case_word}`',
        'if low_case_word in low_case_dict': lambda S, B, r: f'`{S.low_case_word}` 在 low_case_dict 里？' + ('是：大小写匹配' if S.low_case_word in S.low_case_dict else '否：再降一级，试元音替换'),
        'res.append(wordlist[low_case_dict': '大小写匹配，取最靠前的 `{res[-1]}`',
        'if (rest_word, spell_state) in spell_dict': lambda S, B, r: f'二元组 `({S.rest_word!r}, {S.spell_state:04b})` 在 spell_dict 里？' + ('是：元音替换匹配' if (S.rest_word, S.spell_state) in S.spell_dict else '否：无匹配'),
        'res.append(wordlist[spell_dict': '元音替换匹配，取最靠前的 `{res[-1]}`',
        "res.append('')": '三级都没匹配上，答案是空串',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='三级优先：原词、小写词、(辅音串, 元音位置)二元组',
        complexity='时间 `O((n+m)L)`，空间 `O(nL)`',
        problem=['按优先级把查询词纠正成单词表里的词：完全匹配 > 大小写匹配 > 元音错误匹配',
                 '后两级都取单词表里==第一个==匹配项，都不匹配返回空串',
                 '本视频：词表 `[KiTe,kite]`，查询 `[kite,Kite,keti]` → `[kite,KiTe,KiTe]`'],
        quote='对于元音替换且大小写匹配的单词，注意到这里单词的长度不超过7，那么我可以先找出word中元音出现的位置，然后使用二进制编码进行状态压缩得到元音字母位置的状态表示state，同时收集剩下的辅音字母形成rest_word。',
        quote_src='—— yiduobo 题解原文',
        idea=['元音换成哪个都无所谓：只要==元音的位置==和==辅音串==相同，就算匹配',
              '用 `spell_state` 的二进制位记录元音位置，`rest_word` 收集辅音',
              '从前往后建表，同一个 key 只记第一次，天然满足“第一个匹配项”'],
        summary=['时间 `O((n+m)L)`，`L <= 7`，所以用整数位压缩很轻',
                 '易错：大小写转换要先判 `ord(char) < 97`，且元音判断在转小写之后',
                 '没匹配上就 append 空串；易错：建表时要 `not in` 才写入，否则会留下最靠后的下标',
                 '原文只是 Python 2 的类写法，代码在 Python 3 下无需改动',
                 '对比灵神：他倒序覆盖、元音换成 `?` 拼 key；这里用位压缩二元组'],
    ),
)
