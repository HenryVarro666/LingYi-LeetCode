def _kind(S):
    if 'char' not in S:
        return '先判长度，再扫一遍：元音 → v_flag，其他字母 → c_flag，其他非数字 → 非法'
    c = S['char']
    k = '元音' if c in S['vowel'] else '辅音字母' if c.isalpha() else '数字' if c.isdigit() else '非法字符'
    return f"当前字符 `'{c}'`：=={k}==　　v_flag = `{S['v_flag']}`　c_flag = `{S['c_flag']}`"


CONFIG = dict(
    num=3136, title='有效单词', difficulty='Easy', category='字符串',
    author='yiduobo', technique='元音集合 + 两个标志',
    tags=[],
    code='''
class Solution(object):
    def isValid(self, word):

        vowel = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])

        v_flag = False
        c_flag = False

        if len(word) < 3:
            return False
        
        for char in word:
            if char in vowel:
                v_flag = True
            elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                c_flag = True
            elif not '0' <= char <= '9':
                return False
        
        return v_flag and c_flag
''',
    call='Solution().isValid("ab$e")',
    expect=False,
    skip=['vowel = set', 'v_flag = False', 'c_flag = False'],
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前字符）', cell=110, h=200,
             color=lambda S, i, v: 'blue' if 'char' in S and v == S['char'] else None),
        dict(type='set', var='vowel', label='vowel（元音集合）', fmt=lambda x: x, h=130),
        dict(type='text', fn=_kind, size=28, h=110),
    ],
    watch=[('v_flag', 'v_flag', 'green'), ('c_flag', 'c_flag', 'blue')],
    captions={
        'len(word) < 3': lambda S, B, r: f'长度 `{len(B.word)}`，' + ('不足 3 → ==直接返回 False==' if len(B.word) < 3 else '≥ 3，继续'),
        'for char in word': '依次遍历每个字符 `char`',
        'if char in vowel': lambda S, B, r: f"`'{S.char}'` 在 vowel 里吗？" + ('在 → 是元音' if S.char in S.vowel else '不在 → 往下判断'),
        'v_flag = True': '遇到元音，`v_flag = True`',
        'elif \'a\'': lambda S, B, r: f"`'{S.char}'` 是字母吗？" + ('是；不是元音，==必然是辅音==' if S.char.isalpha() else '不是字母，往下看是不是数字'),
        'c_flag = True': '遇到辅音，`c_flag = True`',
        'elif not': lambda S, B, r: f"`'{S.char}'` 不是数字 → ==出现了 `@#$` 这类非法字符，返回 False==" if not S.char.isdigit() else f"`'{S.char}'` 是数字，合法，跳过",
        'return v_flag and c_flag': '`v_flag = {v_flag}`，`c_flag = {c_flag}` → 返回 {ret}',
    },
    cards=dict(
        one_liner='先建元音集合，扫一遍：元音、辅音、数字各自处理，其余直接否决',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['有效单词：长度 ≥ 3，由字母和数字组成，含元音也含辅音',
                 '判断给定字符串是否有效',
                 '演示用 `"ab$e"`：有元音 a、辅音 b，但含非法字符 `$`'],
        quote='若其出现在vowel，那么就将v_flag置为true；否则就检测其是否为字符，如果是那么其必然为辅音字符，那么就将c_flag置为true；否则检测其是否为数字，如果不是说明出现了其他字符，此时直接返回false。',
        quote_src='—— yiduobo 题解原文',
        idea=['元音少，先放进集合 `vowel`，查询是 O(1)',
              '三层 if/elif：元音 → 辅音 → 非数字即非法',
              '字母里先排除了元音，剩下的必是辅音'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：元音集合要含大写',
                 '易错：长度 < 3 要最先判断，非法字符随时返回 False',
                 '最后必须 v_flag 和 c_flag 同时为 True'],
    ),
)
