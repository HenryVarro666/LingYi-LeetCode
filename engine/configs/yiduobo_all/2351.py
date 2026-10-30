CONFIG = dict(
    num=2351, title='第一个出现两次的字母', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 + 集合',
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
    call="Solution().repeatedCharacter('abccbaacz')",
    expect='c',
    views=[
        dict(type='string', var='s', label='s', cell=90, h=200,
             color=lambda S, i, v: 'blue' if S.get('char') == v else None),
        dict(type='set', var='char_set', label='char_set（已出现过的字符）', fmt=lambda x: f"'{x}'", h=200),
    ],
    watch=[('char', 'char', 'blue'), ('char_set', 'sorted(char_set)', 'green')],
    captions={
        'for char in s': '取出下一个字符 `{char}`',
        'char_set = set()': '准备一个空集合，==记录已经出现过的字符==',
        'if char in char_set': '`{char}` 在集合里吗？{"在 → 这是第二次见到它" if char in char_set else "不在 → 第一次见到它"}',
        'return char': '`{char}` 的第二次出现是所有字母里最早的 → 返回 ==\'{char}\'==',
        'char_set.add': '第一次见到 `{char}`，加入集合，继续向后走',
    },
    cards=dict(
        one_liner='用集合记住见过的字符，第一次撞上的就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 26 个字母）',
        problem=['给定小写字母字符串 `s`，返回第一个出现两次的字母',
                 '"第一个" 按第二次出现的位置先后来比',
                 '示例：`"abccbaacz"` → `"c"`'],
        quote='一趟遍历，使用集合记录以及出现过的字符。若当前遍历到的字符char在集合中，那么char就是最终答案，否则将char加入到集合中然后继续向后遍历。',
        quote_src='—— yiduobo 题解',
        idea=['从左到右扫，遇到的字符先查集合',
              '在集合里 = 第二次出现，因为是从左往右扫，它就是最早凑够两次的',
              '不在就放进去，继续'],
        summary=['时间 `O(n)`，集合最多 26 项所以空间 `O(1)`',
                 '先判断再加入，顺序不能反，否则每个字符都会"已存在"',
                 '题目保证有重复字母，所以一定会在循环里 return'],
    ),
)
