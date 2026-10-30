CONFIG = dict(
    num=3120, title='统计特殊字母的数量 I', difficulty='Easy', category='位运算',
    author='yiduobo', technique='两个集合 · 小写找大写', tags=[],
    code='''
class Solution(object):
    def numberOfSpecialChars(self, word):

        upper = set()
        lower = set()
        for char in word:
            if 'a' <= char <= 'z':
                lower.add(char)
            else:
                upper.add(char)
        
        res = 0
        for char in lower:
            if chr(ord(char) - 32) in upper:
                res += 1
        
        return res
''',
    call='Solution().numberOfSpecialChars("aaAbcBC")',
    expect=3,
    views=[
        dict(type='string', var='word', h=200, cell=100,
             color=lambda S, i, v: ('blue' if v == S['char'] else None) if 'char' in S and 'res' not in S else None),
        dict(type='set', var='lower', label='lower（小写）', h=150),
        dict(type='set', var='upper', label='upper（大写）', h=150),
        dict(type='text', h=70, fn=lambda S: (f"小写 `{S['char']}` 的大写版本 `{chr(ord(S['char']) - 32)}` {'在' if chr(ord(S['char']) - 32) in S['upper'] else '不在'} upper 中" if 'res' in S and 'char' in S else '')),
    ],
    watch=[('char', 'char', 'blue'), ('res', 'res', 'green')],
    captions={
        'for char in word': lambda S, B, r: ('第一趟遍历完' if S.char == B.get('char') and S.char == S.word[-1] and (S.char in S.lower or S.char in S.upper) else f'读到字符 `{S.char}`'),
        "'a' <= char <= 'z'": lambda S, B, r: f"`'a' <= '{S.char}' <= 'z'` → {'是小写' if 'a' <= S.char <= 'z' else '不是，是大写'}",
        'lower.add': '小写 `{char}` 记进 `lower`',
        'upper.add': '大写 `{char}` 记进 `upper`',
        'res = 0': '第一趟结束：两个集合已经记全。接下来只看 lower 里的每个小写字母',
        'for char in lower': lambda S, B, r: ('lower 遍历完，不再有小写字母' if S.char == B.get('char') else f'取出 lower 中的小写 `{S.char}`'),
        'chr(ord(char) - 32)': lambda S, B, r: f"`{S.char}` 的 ASCII 码减 32 得大写 `{chr(ord(S.char) - 32)}`：{'在 upper 里 → 大小写都出现过' if chr(ord(S.char) - 32) in S.upper else '不在 upper → 不特殊'}",
        'res += 1': '`{char}` 是特殊字母，`res` → =={res}==',
        'return': '统计完毕：特殊字母 ==`{ret}`== 个',
    },
    cards=dict(
        one_liner='先把大小写分开记，再看每个小写有没有大写搭档',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`word` 中一个字母的小写、大写都出现，就是特殊字母', '返回特殊字母的数量',
                 '示例：`"aaAbcBC"` → `3`'],
        quote='一趟遍历，使用两个集合upper和lower分别记录字符串中出现的大写字符和小写字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：小写进 `lower`，大写进 `upper`', '第二趟：遍历 `lower`，把小写的 ASCII 码减 32 就是大写',
              '大写也在 `upper` 里，答案加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`（最多 26 个字母）',
                 '大小写 ASCII 码相差 32：`ord(\'a\') - 32 == ord(\'A\')`',
                 '集合里的字母只记一次，所以重复出现不会重复计数',
                 '对比灵神：灵神用位运算，一个整数当集合，AND 求交集；这里是两个 set + 一次查找'],
    ),
)
