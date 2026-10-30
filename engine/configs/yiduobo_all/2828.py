CONFIG = dict(
    num=2828, title='判别首字母缩略词', difficulty='Easy', category='字符串',
    author='yiduobo', technique='拼接首字母再比较',
    tags=[],
    code='''
class Solution(object):
    def isAcronym(self, words, s):

        return ''.join([w[0] for w in words]) == s
''',
    call='[Solution().isAcronym(w, s) for w, s in ((["an","apple"], "a"), (["alice","bob","charlie"], "abc"), (["never","gonna","give","up","on","you"], "ngguoy"), (["x","y"], "xz"))]',
    expect=[False, True, True, False],
    views=[
        dict(type='array', var='words', label='words', cell=130),
        dict(type='text', size=34, fn=lambda S: (f"首字母拼接：=={''.join(w[0] for w in S['words'])}==" if 'words' in S else '')),
        dict(type='string', var='s', label='s（目标）', cell=84),
    ],
    watch=[],
    captions={
        'return': "取每个单词首字母 `{[w[0] for w in words]}`，拼成 `{''.join([w[0] for w in words])}`，和 `s = {s}` 比较 → =={ret}==",
    },
    cards=dict(
        one_liner='把所有单词的首字母拼起来，直接和 s 比',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 是否正好由 `words` 每个单词的首字母按顺序拼成',
                 '示例：`["an","apple"]`, `"a"` → `false`',
                 '示例：`["never","gonna","give","up","on","you"]`, `"ngguoy"` → `true`'],
        quote='遍历words中的所有单词，将首字母拼接起来之后判断是否与s即可。',
        quote_src='—— yiduobo 题解',
        idea=['列表推导 `[w[0] for w in words]` 取出所有首字母',
              '`\'\'.join` 拼成字符串',
              '直接用 `==` 和 `s` 比较，长度不同自然不等'],
        summary=['时间 `O(n)`，需要额外存放拼出的字符串，空间 `O(n)`',
                 '易错点：每个单词至少 1 个字符，`w[0]` 不会越界',
                 '写法直白，不需要单独判断长度'],
    ),
)
