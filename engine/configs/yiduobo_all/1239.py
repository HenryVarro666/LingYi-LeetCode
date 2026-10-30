def _letters(x):
    s = ''.join(chr(97 + i) for i in range(26) if x >> i & 1)
    return s or '∅'


def _txt(S):
    if S.get('_line') in (12, 14, 15) and 'word' in S and 'num' in S:
        return f"单词 `{S['word']}` 的字母集合：=={_letters(S['num'])}==（编码 `{S['num']}`）"
    if 'candidate' in S and 'cnt' in S and S.get('_line', 0) >= 28:
        return f"集合 =={_letters(S['candidate'])}== 里还剩 `{bin(S['candidate']).count('1')}` 个 1，已数 `{S['cnt']}` 个"
    if 'num' in S and 'tmp' in S:
        return f"新单词 =={_letters(S['num'])}== 逐个和 `candidate_set` 里的集合比较"
    return ''


CONFIG = dict(
    num=1239, title='串联字符串的最大长度', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='位掩码 + 集合递推',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def maxLength(self, arr):

        num_list = []
        for word in arr:
            num = 0
            flag = True
            for char in word:
                if num & (1 << (ord(char) - 97)):
                    flag = False
                    break
                num |= (1 << (ord(char) - 97))
            
            if flag:
                num_list.append(num)
        
        candidate_set = set([0])
        for num in num_list:
            tmp = set()
            for candidate in candidate_set:
                if candidate & num == 0:
                    tmp.add(candidate | num)
            candidate_set.update(tmp)
        
        res = 0
        for candidate in candidate_set:
            cnt = 0
            while candidate:
                cnt += 1
                candidate &= candidate - 1
            res = max(res, cnt)
        
        return res
''',
    call="Solution().maxLength(['ab', 'bc', 'bd', 'aa'])",
    expect=2,
    views=[
        dict(type='array', var='arr', label='arr（候选字符串）', h=190, cell=110),
        dict(type='array', var='num_list', label='num_list（合法单词的字母位掩码）', h=190, cell=90),
        dict(type='set', var='candidate_set', label='candidate_set（所有合法拼接的字母集合）',
             fmt=lambda x: _letters(x), h=170, font=28),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    skip=['flag = True', 'num = 0', 'for char in word', 'break', 'tmp = set()', 'cnt = 0', 'while candidate', 'cnt += 1'],
    max_steps=100,
    watch=['word', ('num', 'num', 'yellow'), 'flag', ('candidate', 'candidate', 'blue'), 'cnt', ('res', 'res', 'green')],
    captions={
        'num = 0': '`num` 用 26 位二进制记录这个单词用了哪些字母',
        'if num & (1 << (ord(char) - 97))': lambda S, B, r: (f"字母 `{S.char}` 对应第 `{ord(S.char) - 97}` 位，这一位已经是 1 → ==字母重复=="
                                                           if B.num & (1 << (ord(S.char) - 97))
                                                           else f"字母 `{S.char}` 对应第 `{ord(S.char) - 97}` 位还是 0 → 没出现过"),
        'flag = False': '单词自己内部有重复字母，==标记不合法==',
        'num |= (1 <<': '把 `{char}` 那一位置 1：`num = {num}`（字母 {_letters(num)}）',
        'num_list.append': '单词 `{word}` 合法，编码 `{num}` 加入 `num_list`',
        'candidate_set = set([0])': '空集合 `0` 是起点：什么都不选也合法',
        'for num in num_list': '取下一个合法单词的编码 `{num}`（字母 {_letters(num)}）',
        'tmp = set()': '`tmp` 暂存这一轮新生成的集合，避免遍历时改 `candidate_set`',
        'if candidate & num == 0': lambda S, B, r: (
            f"`{_letters(S.candidate)} & {_letters(S.num)}` = 0 → 没有公共字母，==可以拼接=="
            if S.candidate & S.num == 0 else f"`{_letters(S.candidate)}` 和 `{_letters(S.num)}` 有公共字母 → 不能拼"),
        'tmp.add': '拼接后的字母集合 `{_letters(candidate | num)}` 放进 `tmp`',
        'candidate_set.update': '把新集合并入 `candidate_set`，现在有 `{len(candidate_set)}` 种',
        'for candidate in candidate_set': '检查集合 `{_letters(candidate)}` 有几个字母',
        'cnt = 0': '`cnt` 计数 1 的个数',
        'while candidate': lambda S, B, r: (f"`candidate = {S.candidate}` 还有 1 → 继续数" if S.candidate else "没有 1 了，数完"),
        'candidate &= candidate - 1': '`x &= x - 1` 去掉最低位的 1：`candidate = {candidate}`',
        'res = max': '`res = max({B.res}, {cnt}) = {res}`',
        'return res': '最长的合法拼接长度是 `{res}`',
    },
    cards=dict(
        one_liner='用 26 位二进制表示字母集合，位与为 0 就能拼接',
        complexity='时间 `O(2^n)` 级，空间 `O(2^n)`',
        problem=['给字符串数组 `arr`，从中挑出若干个串联',
                 '串联结果的每个字母都==不重复==，求最长长度',
                 '示例：`["un","iq","ue"]` → `4`（`un+iq` 或 `iq+ue`）',
                 '本视频：`["ab","bc","bd","aa"]` → `2`'],
        quote='将所有字符按照二进制编码，即a到z分别对应2^0到2^25。接下来我们使用一个set储存当前合法的字符串',
        quote_src='—— yiduobo 题解原文',
        idea=['每个单词压成一个整数；单词自己有重复字母就直接丢掉',
              '`candidate_set` 存所有合法的字母集合，从 `{0}` 起步',
              '来一个新单词，只和无公共字母的集合拼，结果加入集合',
              '最后用 `x &= x - 1` 数每个集合里 1 的个数，取最大'],
        summary=['集合最多 `2^n` 个，`n` 是合法单词数，但字母只有 26 个，实际更少',
                 '遍历 `candidate_set` 时不能往里加，所以先放到 `tmp`',
                 '不同单词组成同一字母集合时，集合里只存一份',
                 '原文为 Python 2 风格，这里无需改动，直接可在 Python 3 运行'],
    ),
)
