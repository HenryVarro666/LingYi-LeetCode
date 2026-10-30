CONFIG = dict(
    num=1796, title='字符串中第二大的数字', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描 · 维护最大与次大',
    code='''
class Solution(object):
    def secondHighest(self, s):

        first = second = None
        for char in s:
            if char >= '0' and char <= '9':
                if first is None or first < char:
                    first, second = char, first
                elif first != char and (second is None or second < char):
                    second = char
        
        if second is None:
            return -1
        
        return int(second)
''',
    call="Solution().secondHighest('dfa12321afd')",
    expect=2,
    views=[
        dict(type='string', var='s', h=200, label='s',
             color=lambda S, i, v: 'yellow' if v == S.get('char') and S.get('char') is not None and v.isdigit() else None),
        dict(type='text', size=36, h=100, fn=lambda S: f"当前字符 `{S['char']}`" if 'char' in S else ''),
        dict(type='text', size=36, h=120, fn=lambda S: f"最大 `first = {S.get('first')}`，次大 `second = {S.get('second')}`" if 'first' in S else ''),
    ],
    watch=[('char', 'char', 'blue'), ('first', 'first', 'green'), ('second', 'second', 'yellow')],
    captions={
        'first = second': '`first` 记最大数字，`second` 记第二大，开始都还没有',
        'for char in s': '看字符 `{char}`',
        "if char >= '0'": lambda S, B, r: (f'`{S.char}` 是数字，参与比较' if '0' <= S.char <= '9' else f'`{S.char}` 不是数字，跳过'),
        'if first is None': lambda S, B, r: ('还没有最大值，或者 `{0}` 比最大值 `{1}` 更大 → 成立'.format(S.char, S.first) if (S.first is None or S.first < S.char)
                                              else f'`{S.first} < {S.char}` 不成立，不是新的最大'),
        'first, second = char': '新最大 `first = {first}`，旧最大退位成次大 `second = {second}`',
        'elif first != char': lambda S, B, r: (f'`{S.char}` 不等于最大 `{S.first}`，且次大是 `{S.second}`：{"比次大更大，更新次大" if (S.first != S.char and (S.second is None or S.second < S.char)) else "没有更大，不更新"}' if S.first != S.char
                                                else f'`{S.char}` 等于最大 `{S.first}`：重复数字不算第二大，跳过'),
        'second = char': '`second` 更新为 `{second}`',
        'if second is None': lambda S, B, r: ('`second` 仍为空：只有一种数字，返回 -1' if S.second is None else '`second` 有值，继续'),
        'return -1': '没有第二大的数字，返回 `-1`',
        'return int': '第二大的数字是 `{ret}`',
    },
    cards=dict(
        one_liner='一趟扫描，只维护最大和次大两个数字',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给字符串 `s`，返回其中出现的数字里==第二大的数字==，没有则返回 `-1`',
                 '重复数字只算一种，字母忽略',
                 '示例：`"dfa12321afd"` → `2`'],
        quote='比较基础的题目，一趟扫描，只针对数字选出其中第二大的即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['只看数字字符，用 `first`、`second` 记最大和次大',
              '遇到更大的数：旧最大退位成次大',
              '遇到不等于最大、又比次大大的数：更新次大；重复的最大值要排除'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`first != char` 必须判断，否则最大值重复会被当成次大',
                 '数字字符可直接按字符比较，最后才 `int(second)`',
                 '原文代码在 Python 3 下无需修改即可运行'],
    ),
)
