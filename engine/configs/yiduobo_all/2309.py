CONFIG = dict(
    num=2309, title='兼具大小写的最好英文字母', difficulty='Easy', category='位运算',
    author='yiduobo', technique='哈希集合 + 从 Z 到 A 倒着找',
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
    call="Solution().greatestLetter('arRAzFif')",
    expect='R',
    views=[
        dict(type='string', var='s', h=170,
             color=lambda S, i, v: 'blue' if 'upper_char' in S and v in (S['upper_char'], S['lower_char']) else None),
        dict(type='set', var='char_set', h=220),
        dict(type='text', fn=lambda S: (f"检查 `{S['upper_char']}` 和 `{S['lower_char']}` 是否都在集合里" if 'upper_char' in S and 'lower_char' in S else ''), h=60),
    ],
    watch=['index', 'upper_char', 'lower_char'],
    captions={
        'char_set = set': '把 `s` 里出现过的字符全放进集合：`{len(char_set)}` 个不同字符',
        'for index in range': '从 25 到 0 倒着枚举，也就是从 `Z` 到 `A`：最先找到的就是最好的字母',
        'upper_char = ': '`index = {index}` → 大写 `{upper_char}`（`index + 65`）',
        'lower_char = ': '对应小写 `{lower_char}`（`index + 97`）',
        'if upper_char in': '`{upper_char}` {"在" if upper_char in char_set else "不在"}集合，`{lower_char}` {"在" if lower_char in char_set else "不在"}集合 → {"两个都在，就是答案" if upper_char in char_set and lower_char in char_set else "不满足，换前一个字母"}',
        'return upper_char': '从 Z 往前第一个满足的就是最好的字母 =={upper_char}==',
        "return ''": '全部枚举完都没有 → 返回空串',
    },
    cards=dict(
        one_liner='先把字符都放进集合，再从 Z 到 A 找第一个大小写都在的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找出大小写形式都在 `s` 里出现的字母，取字母表最靠后的，返回大写',
                 '没有则返回空串',
                 '示例：`"arRAzFif"` → `"R"`'],
        quote='将s中的所有字符加入到哈希表中，然后从Z到A进行反向的遍历，若当前字符以及其小写形式都出现在哈希表中，那么该字符就是答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`set(s)` 一次建好，之后每次判断是 `O(1)`',
              '倒着枚举 26 个字母，第一个命中的一定是最好的',
              '`chr(index + 65)` 是大写，`chr(index + 97)` 是小写'],
        summary=['时间 `O(n)`，空间 `O(1)`（集合最多 52 个字符）',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '易错：必须倒着枚举，正着枚举会先找到最差的',
                 '对比灵神：灵神把大小写各压成一个整数，用按位与找出共有字母'],
    ),
)
