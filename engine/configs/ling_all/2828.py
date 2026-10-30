CONFIG = dict(
    num=2828, title='判别首字母缩略词', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='长度判断 + zip 逐个比较',
    tags=[],
    code='''
class Solution:
    def isAcronym(self, words: List[str], s: str) -> bool:
        return len(words) == len(s) and all(w[0] == c for w, c in zip(words, s))
''',
    call='[Solution().isAcronym(w, s) for w, s in ((["an","apple"], "a"), (["alice","bob","charlie"], "abc"), (["never","gonna","give","up","on","you"], "ngguoy"), (["x","y"], "xz"))]',
    expect=[False, True, True, False],
    views=[
        dict(type='array', var='words', label='words', cell=130, pointers={}),
        dict(type='string', var='s', label='s', cell=84),
        dict(type='text', size=28, fn=lambda S: (f"长度：`len(words) = {len(S['words'])}`，`len(s) = {len(S['s'])}`" if 'words' in S else '')),
    ],
    watch=[('len(words)', 'len(words)', 'blue'), ('len(s)', 'len(s)', 'pink')],
    captions={
        'return len': '先看长度 `{len(words)} == {len(s)}`；再用 `zip` 逐个比较每个单词首字母与 `s` 的对应字符，全部相等则返回 =={ret}==',
    },
    cards=dict(
        one_liner='长度一致，且每个单词首字母都等于 s 对应位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 是否正好由 `words` 每个单词的首字母按顺序拼成',
                 '示例：`["an","apple"]`, `"a"` → `false`',
                 '示例：`["never","gonna","give","up","on","you"]`, `"ngguoy"` → `true`'],
        quote='如果 words 长度和 s 长度不同，直接返回 false。如果存在 words[i][0] ≠ s[i]，也返回 false。否则返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先比长度：个数对不上，不可能拼成',
              '`zip(words, s)` 把单词和字符一一配对',
              '`all(...)` 遇到第一个不等就短路返回 `False`'],
        summary=['时间 `O(n)`，`n` 为 `s` 的长度；空间 `O(1)`',
                 '易错点：必须先判断长度，否则 `zip` 会悄悄截断较长的一边',
                 '生成器 + `all` 可以提前结束，不用先拼出完整字符串'],
    ),
)
