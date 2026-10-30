def _txt(S):
    s = S.get('s')
    if s is None:
        return ''
    return '句子拆开看：' + ' | '.join(s.split(' '))


def _pairs(s):
    return [(i, s[i - 1], s[i + 1]) for i, c in enumerate(s) if c == ' ']


def _cap(s, ret):
    out = f"先比首尾：`s[0] = '{s[0]}'`，`s[-1] = '{s[-1]}'`" + ('，相同；' if s[0] == s[-1] else '，不同 → ==False==')
    if s[0] != s[-1]:
        return out
    parts = []
    for i, l, r in _pairs(s):
        ok = l == r
        parts.append(f"空格 {i}：`{l}`{'＝' if ok else '≠'}`{r}`")
        if not ok:
            break
    return out + '再逐个空格比两侧：' + '；'.join(parts) + (' → 全部接得上 ==True==' if ret else ' → ==False==')


CONFIG = dict(
    num=2490, title='回环句', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='看首尾 + 看每个空格两侧',
    tags=[],
    code='''
class Solution:
    def isCircularSentence(self, s: str) -> bool:
        return s[0] == s[-1] and all(c != ' ' or s[i-1] == s[i+1] for i, c in enumerate(s))
''',
    call='Solution().isCircularSentence("ab bc ca ba")',
    expect=False,
    views=[
        dict(type='text', fn=_txt, size=28, h=60),
        dict(type='string', var='s', label='s（蓝 = 空格，粉 = 空格两侧要比较的字符）', cell=84, h=240,
                          color=lambda S, k, v: ('pink' if S['s'][k] != ' ' and any(abs(k - i) == 1 for i, _, _ in _pairs(S['s'])) else ('blue' if S['s'][k] == ' ' else None))),
    ],
    watch=[],
    captions={
        'return s[0] == s[-1]': lambda S, B, ret: _cap(S['s'], ret),
    },
    cards=dict(
        one_liner='回环句 = 首尾字符相同 + 每个空格两侧字符相同',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['句子由单词和空格组成；每个单词的==尾字符==等于下一个单词的==首字符==',
                 '最后一个单词的尾字符也要等于第一个单词的首字符',
                 '示例：`"leetcode exercises sound delightful"` → `true`',
                 '本视频：`"ab bc ca ba"` → `false`（最后一个空格两侧 `a`、`b` 不同）'],
        quote='转换成判断：1. 首尾字符是否相同。2. 每个空格左右的字符是否相同。',
        quote_src='—— 灵茶山艾府题解',
        idea=['空格左边是上一个单词的尾，右边是下一个单词的首',
              '所以不用 split，只看每个空格两侧的字符',
              '再把末尾接回开头：比较 `s[0]` 和 `s[-1]`'],
        after=[dict(heading='为什么能这样简化', lines=[
            '拆成单词比较：要处理 `words[i][-1]` 与 `words[i+1][0]`，还要拆分出新列表',
            '空格恰好是单词的分界：左邻是上一词的尾，右邻是下一词的首',
            '`all(...)` 遇到第一个接不上的空格就停，`c != \' \'` 让非空格字符直接通过',
            '首尾检查对应“最后一个单词接回第一个单词”这一条'])],
        summary=['时间 `O(n)`，空间 `O(1)`，不用拆分单词',
                 '`c != \' \' or ...`：不是空格就直接通过，是空格才比较两侧',
                 '题目保证无前导/尾随空格，所以 `s[i-1]`、`s[i+1]` 不会越界',
                 '单个单词时没有空格，只剩首尾检查'],
    ),
)
