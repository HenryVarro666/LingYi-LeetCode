def _col(S, i, v):
    if not v.isalpha():
        return None
    return 'green' if v in 'aeiou' else 'orange'

CONFIG = dict(
    num=3813, title='元音辅音得分', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='一次遍历模拟', tags=[],
    code='''
class Solution:
    def vowelConsonantScore(self, s: str) -> int:
        v = c = 0
        for ch in s:
            if not ch.isalpha():
                continue
            if ch in "aeiou":
                v += 1
            else:
                c += 1
        return v // c if c else 0
''',
    call='Solution().vowelConsonantScore("a e1 tsou")',
    expect=2,
    views=[
        dict(type='string', var='s', color=_col, h=200),
        dict(type='text', fn=lambda S: f"元音 v = =={S['v']}==，辅音 c = =={S['c']}==" if 'v' in S else '', h=120),
    ],
    watch=[('v', 'v', 'green'), ('c', 'c', 'orange'), 'ch'],
    captions={
        'v = c = 0': '`v` 数元音，`c` 数辅音，都从 0 开始',
        'if not ch.isalpha()': lambda S, B, r: (f'`{S.ch!r}` 不是字母 → ==跳过==，既不算元音也不算辅音' if not S.ch.isalpha() else f'`{S.ch!r}` 是字母，继续判断元音还是辅音'),
        'continue': '空格和数字不参与计数，直接看下一个字符',
        'if ch in "aeiou"': lambda S, B, r: (f'`{S.ch}` 属于 aeiou → 元音' if S.ch in 'aeiou' else f'`{S.ch}` 不在 aeiou 里 → 辅音'),
        'v += 1': '元音：`v` → {v}',
        'c += 1': '辅音：`c` → {c}',
        'return': '`c = {c}`：有辅音才能除；`v // c` = {v} // {c} = =={ret}==，没有辅音得 0',
    },
    cards=dict(
        one_liner='先过滤掉非字母，再分别数元音和辅音',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串由小写字母、空格、数字组成', '得分 = 元音数 `v` ÷ 辅音数 `c` 向下取整；`c = 0` 时得 0',
                 '示例：`"cooear"` → `2`；本视频：`"a e1 tsou"` → `2`'],
        quote='按题意模拟即可。注意 s 可能包含不是字母的字符。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用 `isalpha()` 把空格和数字先跳过', '剩下的字母：在 `aeiou` 里算元音，否则算辅音',
              '最后 `v // c if c else 0`，一行处理除零'],
        summary=['时间 `O(n)`，空间 `O(1)`', '易错点：数字和空格==不是辅音==，必须先排除',
                 '`c = 0` 时不能做除法，要返回 0', '`//` 对非负数就是 floor'],
    ),
)
