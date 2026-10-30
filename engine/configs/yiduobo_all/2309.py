def _chk(S):
    if 'index' not in S:
        return ''
    cs = S['char_set']
    u, l = chr(S['index'] + 65), chr(S['index'] + 97)
    a = '==有==' if u in cs else '没有'
    b = '==有==' if l in cs else '没有'
    return f"大写 `{u}`：{a}      小写 `{l}`：{b}"


CONFIG = dict(
    num=2309, title='兼具大小写的最好英文字母', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希集合 · 从 Z 到 A 反向找',
    tags=[],
    code='''
class Solution(object):
    def greatestLetter(self, s):

        char_set = set(s)
        
        for index in range(25, -1, -1):
            upper_char = chr(index + 65)
            lower_char = chr(index + 97)
            if upper_char in char_set and lower_char in char_set:
                return upper_char

        return ''
''',
    call='Solution().greatestLetter("arRAzFif")',
    expect='R',
    views=[
        dict(type='text', fn=_chk, size=34, h=90),
        dict(type='string', var='s', h=200, label='s',
             color=lambda S, i, v: None if 'index' not in S else (
                 'green' if v in (chr(S['index'] + 65), chr(S['index'] + 97)) and chr(S['index'] + 65) in S['char_set'] and chr(S['index'] + 97) in S['char_set']
                 else ('blue' if v in (chr(S['index'] + 65), chr(S['index'] + 97)) else None))),
        dict(type='set', var='char_set', h=220, fmt=lambda x: str(x)),
    ],
    skip=['upper_char = chr', 'lower_char = chr'],
    watch=[('index', 'index', 'blue'), ('upper_char', 'upper_char', 'cyan'), ('lower_char', 'lower_char', 'pink')],
    captions={
        'char_set = set(s)': '`s` 里出现过的字符全放进集合 `char_set`，查“出没出现”只要 `O(1)`',
        'for index in range': '`index = {index}`：倒着找，第一个满足的就是最好的字母（`{index}` 对应 `{chr(index + 65)}`/`{chr(index + 97)}`）',
        'upper_char = chr': '`chr({index} + 65)` = 大写 `{upper_char}`',
        'lower_char = chr': '`chr({index} + 97)` = 小写 `{lower_char}`',
        'if upper_char in char_set': lambda S, B, r: (f"`{S.upper_char}` 和 `{S.lower_char}` 都在集合里 → ==找到了=="
                                                       if S.upper_char in S.char_set and S.lower_char in S.char_set else
                                                       f"`{S.upper_char}` {'在' if S.upper_char in S.char_set else '不在'}集合，`{S.lower_char}` {'在' if S.lower_char in S.char_set else '不在'}集合 → 不是大小写都有，往前找前一个字母"),
        'return upper_char': '从大到小第一个大小写都有的字母，就是最好的：返回 `{upper_char}`',
        "return ''": '26 个字母都没找到 → 返回空串',
    },
    cards=dict(
        one_liner='从 Z 往 A 倒着找，第一个大小写都出现的就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 52 个字符）',
        problem=['找出 `s` 中大小写形式都出现的字母里，字母表上最靠后的一个，返回大写',
                 '没有这样的字母就返回空串',
                 '示例：`"arRAzFif"` → `"R"`（`A`、`F`、`R` 都有，`R` 最靠后）'],
        quote='将s中的所有字符加入到哈希表中，然后从Z到A进行反向的遍历，若当前字符以及其小写形式都出现在哈希表中，那么该字符就是答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用集合记下所有出现过的字符',
              '要“最靠后”，就从 `Z` 倒着枚举到 `A`',
              '第一个大写、小写都在集合里的字母，立刻返回，不用比较大小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：返回的是大写字母；找不到要返回空串 `\'\'`',
                 '易错：`chr(index + 65)` 是大写，`chr(index + 97)` 是小写，别写反',
                 '原文为 Python 2 写法（`class Solution(object)`），Python 3 可直接运行，代码未改动'],
    ),
)
