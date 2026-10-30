CONFIG = dict(
    num=521, title='最长特殊序列 Ⅰ', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 脑筋急转弯',
    tags=['灵神题单', '贪心算法', '难度分 1400'],
    code='''
class Solution:
    def findLUSlength(self, a: str, b: str) -> int:
        return -1 if a == b else max(len(a), len(b))
''',
    call='Solution().findLUSlength("aba", "cdc")',
    expect=3,
    views=[
        dict(type='string', var='a', label='a', h=200),
        dict(type='string', var='b', label='b', h=200),
        dict(type='text', fn=lambda S: f"`a == b` ？ ==" + ('相等' if S['a'] == S['b'] else '不相等') + f"==　　`len(a) = {len(S['a'])}`，`len(b) = {len(S['b'])}`" if 'a' in S else '', size=30, h=120),
    ],
    watch=[('a', 'a'), ('b', 'b'), ('a == b', 'a == b', 'yellow'), ('max(len)', 'max(len(a), len(b))', 'green')],
    captions={
        'return': lambda S, B, ret: (f"`a == b`？{'是' if S.a == S.b else '否'}。" +
                                      ('互为子序列，没有独有的子序列 → 返回 ==-1==' if S.a == S.b
                                       else f"a ≠ b：把更长的（或等长时任意一个）整串当独有子序列，它不可能是对方的子序列 → 返回 `max({len(S.a)}, {len(S.b)})` = =={ret}==")),
    },
    cards=dict(
        one_liner='两串不相等，整串就是答案；相等才是 -1',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['找「只属于其中一个字符串」的最长子序列，返回它的长度，没有就返回 `-1`',
                 '示例：`a = "aba"`，`b = "cdc"` → `3`',
                 '`a = b` 时每个子序列两边都有 → `-1`'],
        quote='如果 a 比 b 长，答案的最大值为 a 的长度，能否做到？可以，把字符串 a 作为独有子序列，它不是 b 的子序列，所以答案为 a 的长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分类讨论：先看 `a == b`，相等就没有独有子序列 → `-1`',
              '`a ≠ b` 时，较长的串不可能是较短串的子序列',
              '一样长但不相等，也不可能互为子序列 → 答案总是 `max(len(a), len(b))`'],
        summary=['时间 `O(n+m)`：长度不同时比较是 `O(1)`，长度相同才逐字比较',
                 '易错点：不要真的去枚举子序列，脑筋急转弯一行搞定',
                 '思考题：输入变成多个字符串 → 522 题，要逐个检查是否是别人的子序列'],
        after=[dict(heading='三种情况一次看清', lines=['`a == b`（如 `"aaa"`, `"aaa"`）→ `-1`',
                                                 '长度不同（如 `"aba"`, `"c"`）→ 较长串的长度 `3`',
                                                 '长度相同但内容不同（如 `"aaa"`, `"bbb"`）→ `3`'])],
    ),
)
