def _enc(S):
    if 'word' not in S or 'morse' not in S:
        return ''
    w = S['word']
    return f"`{w}` → " + ' '.join(f"{c}=`{S['morse'][ord(c) - 97]}`" for c in w) + f" → ==`{''.join(S['morse'][ord(c) - 97] for c in w)}`=="


CONFIG = dict(
    num=804, title='唯一的摩尔斯密码词', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='转成摩尔斯码 · set 去重',
    code='''
class Solution:
    def uniqueMorseRepresentations(self, words):

        morse = [".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]
        word_set = set()
        for word in words:
            word_set.add(''.join([morse[ord(char) - 97] for char in word]))
        
        return len(word_set)
''',
    call="Solution().uniqueMorseRepresentations(['gin', 'zen', 'gig', 'msg'])",
    expect=2,
    views=[
        dict(type='array', var='words', label='words（蓝 = 当前单词）', cell=100, h=170,
             color=lambda S, i, v: 'blue' if S.get('word') == v else None),
        dict(type='text', h=100, size=28, fn=_enc),
        dict(type='set', var='word_set', label='word_set（不同的密码，重复的只留一份）', fmt=lambda x: x, font=30, h=230),
    ],
    watch=[('word', 'word', 'blue'), ('len(word_set)', 'len(word_set)', 'green')],
    skip=['morse = ['],
    captions={
        'word_set = set()': '准备一个 `set`：相同的摩尔斯码只会留一份，最后数个数就是答案',
        'for word in words': lambda S, B, r: (f"取出单词 `{S.word}`" if 'word' not in B or S.word != B.word else '单词都处理完了'),
        'word_set.add': lambda S, B, r: (f"`{S.word}` 转成 `{[x for x in S.word_set if x not in B.word_set][0]}`，==加入集合==，现在有 {len(S.word_set)} 种" if len(S.word_set) > len(B.word_set)
                                         else f"`{S.word}` 的密码集合里==已经有了==，set 自动去重，仍是 {len(S.word_set)} 种"),
        'return len': '集合里有 `{len(word_set)}` 种不同的摩尔斯码，返回它',
    },
    cards=dict(
        one_liner='全部转成摩尔斯码，丢进 set 去重，数个数',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['国际摩尔斯码给每个小写字母规定了一串点和横，如 `a → ".-"`',
                 '把单词里每个字母的码拼起来就是该单词的密码，求 `words` 中有多少种==不同的密码==',
                 '示例：`["gin","zen","gig","msg"]` → `2`（gin 与 zen 同为 `--...-.`，gig 与 msg 同为 `--...--.`）'],
        quote='由于单词的数量不超过100，长度也在12之内，因此可以直接将所有单词转化为摩尔斯密码，然后使用set来去重。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据量很小，不需要任何技巧，直接模拟转换',
              '字母 `char` 对应表里的下标是 `ord(char) - 97`（`a` 的 ASCII 码是 97）',
              '`set` 天然去重，最后 `len(word_set)` 就是答案'],
        summary=['时间、空间都是 `O(总字符数)`',
                 '易错：下标是 `ord(char) - 97`，别忘了减 97',
                 '原文为 Python 2 风格（`class Solution(object)`），这里只改成 `class Solution`，逻辑未动',
                 '同类：用 `set` / `dict` 对“变换后的结果”去重或计数'],
    ),
)
