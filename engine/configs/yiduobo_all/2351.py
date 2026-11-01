CONFIG = dict(
    num=2351, title='第一个出现两次的字母', difficulty='Easy', category='位运算',
    author='yiduobo', technique='一趟遍历 · 集合记录已出现字符',
    tags=[],
    code='''
class Solution(object):
    def repeatedCharacter(self, s):

        char_set = set()
        for char in s:
            if char in char_set:
                return char
            char_set.add(char)
''',
    call="Solution().repeatedCharacter('zabcab')",
    expect='a',
    views=[
        dict(type='string', var='s', label='s（黄 = 当前遍历的字符）', cell=100, h=190,
             color=lambda S, i, v: 'yellow' if 'char' in S and i == len(S['char_set']) - (1 if S['_line'] == 8 else 0) else None),
        dict(type='set', var='char_set', label='char_set（已经出现过的字符）', fmt=lambda x: str(x), h=190, font=36),
    ],
    watch=[('char', 'char', 'blue')],
    captions={
        'char_set = set()': '准备一个集合 `char_set`，记录已经见过的字符',
        'for char in s': lambda S, B, r: (f'往后看下一个字符 `{S.char}`' if 'char' in S else '遍历结束'),
        'if char in char_set': lambda S, B, r: (f'`{S.char}` 在集合里 → ==第二次遇到它了==' if S.char in S.char_set
                                                else f'`{S.char}` 不在集合 {sorted(S.char_set)} 里，第一次见'),
        'return char': '第一个遇到“已经在集合里”的字符就是答案，返回 `{char}`',
        'char_set.add(char)': '`{char}` 加入集合，继续往后看',
    },
    cards=dict(
        one_liner='边扫边记：碰到已经记过的字符，它就是第一个出现两次的',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 26 个字符）',
        problem=['小写字母串 `s`，返回第一个出现==两次==的字母',
                 '比较的是字母的第二次出现位置，越靠前越优先',
                 '本视频：`"zabcab"` → `"a"`'],
        quote='一趟遍历，使用集合记录以及出现过的字符。若当前遍历到的字符char在集合中，那么char就是最终答案，否则将char加入到集合中然后继续向后遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左到右扫，扫到的第一个“已在集合里”的字符，其第二次出现下标最小',
              '正好符合题目对“先出现两次”的定义',
              '不在集合就加入，继续扫'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：先判断再加入集合，否则每个字符都会判为重复',
                 '题目保证有重复字母，所以不会走到循环结束',
                 '代码未做修改（原文已可在 Python 3 运行）'],
    ),
)
