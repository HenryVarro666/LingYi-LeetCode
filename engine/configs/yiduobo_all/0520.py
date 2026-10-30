W = 'FlaG'

CONFIG = dict(
    num=520, title='检测大写字母', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按首字母、次字母分情况判断',
    code='''
class Solution(object):
    def detectCapitalUse(self, word):

        if word[0] >= 'a':
            for char in word[1:]:
                if char < 'a':
                    return False
            return True

        if len(word) == 1:
            return True

        if word[1] >= 'a':
            for char in word[2:]:
                if char < 'a':
                    return False
            return True
        
        for char in word[2:]:
            if char >= 'a':
                return False
        return True
''',
    call=f'Solution().detectCapitalUse({W!r})',
    expect=False,
    views=[
        dict(type='string', var='word', label='word（绿 = 大写字母，蓝 = 正在检查的字母）', cell=110, h=260,
             color=lambda S, i, v: 'blue' if ('char' in S and v == S['char'] and i >= 2 and S['_line'] >= 15) else ('green' if v < 'a' else None)),
        dict(type='text', size=26, fn=lambda S: '首字母大写、第二个小写 → 后面不能再出现大写；首二都大写 → 后面不能出现小写'),
    ],
    watch=[('word[0]', 'word[0]'), ('word[1]', 'word[1]'), ('char', 'char', 'blue')],
    captions={
        "if word[0] >= 'a'": "首字母 `{word[0]}` 是==小写==吗？{word[0] >= 'a'} → 首字母大写，进入后面的情况",
        'if len(word) == 1': '长度为 1 的大写单词，直接合法？`len = {len(word)}` → 不是，继续',
        "if word[1] >= 'a'": "第二个字母 `{word[1]}` 是小写吗？{word[1] >= 'a'} → 首字母大写、第二个小写，后面==必须全是小写==",
        "if char < 'a'": lambda S, B, r: f"`{S.char}` 是大写吗？" + ('==是=={}'.format('，这里后面不允许大写 → 不合法') if S.char < 'a' else '不是，是小写，没问题'),
        'return False': '发现不该出现的大写字母，返回 `False`',
        'return True': '没有发现违规字母，返回 `True`',
    },
    cards=dict(
        one_liner='先看首字母，再看第二个字母，决定后面该全大写还是全小写',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['单词大写用法正确：全大写、全小写、仅首字母大写',
                 '判断给定的 `word` 是否正确',
                 '示例：`"USA"` → `true`，`"FlaG"` → `false`'],
        quote='若单词首字母为大写字母，第二个字母也是大写字母，那么判断后续字母中是否有小写字母。如果有，那么就不合法，否则合法。',
        quote_src='—— yiduobo 题解原文',
        idea=['首字母小写 → 后面不能有大写',
              '首字母大写且长度为 1 → 合法',
              '第二个字母小写 → 后面不能有大写；第二个字母大写 → 后面不能有小写',
              '本视频 `"FlaG"`：`F` 大写、`l` 小写，后面 `a`、`G` 里不能有大写，`G` 违规'],
        after=[dict(heading='四种情况对照', lines=[
            '首字母小写：后面不能有大写 → 如 `"leetcode"`',
            '首字母大写、长度 1：直接合法 → 如 `"A"`',
            '首字母大写、第二个小写：后面不能有大写 → 如 `"Google"`',
            '首字母大写、第二个大写：后面不能有小写 → 如 `"USA"`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '代码里比较字符 `>= \'a\'` 判断小写（大写 ASCII 码更小）',
                 '易错：长度为 1 的单词要单独处理，否则 `word[1]` 越界',
                 '原文为 Python 2 风格，代码未改'],
    ),
)
