def _pair(S, par):
    s1, s2 = S.get('s1'), S.get('s2')
    if not s1:
        return ''
    a, b = s1[par::2], s2[par::2]
    nm = '偶数下标' if par == 0 else '奇数下标'
    return f'{nm}：`{a}` vs `{b}` → ' + ('==字符个数相同==' if sorted(a) == sorted(b) else '==字符个数不同==')


CONFIG = dict(
    num=2839, title='判断通过操作能否让字符串相等 I', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='奇偶下标分组计数',
    code='''
class Solution:
    def canBeEqual(self, s1: str, s2: str) -> bool:
        return Counter(s1[::2]) == Counter(s2[::2]) and \\
               Counter(s1[1::2]) == Counter(s2[1::2])
''',
    call='[Solution().canBeEqual("abcd", "cdab"), Solution().canBeEqual("abcd", "dacb")]',
    expect=[True, False],
    views=[
        dict(type='string', var='s1', label='s1', h=150,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='string', var='s2', label='s2', h=150,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='text', fn=lambda S: _pair(S, 0), h=70),
        dict(type='text', fn=lambda S: _pair(S, 1), h=70),
    ],
    watch=['s1', 's2'],
    captions={
        'return Counter': lambda S, B, ret: (
            f'偶数下标 `{S.s1[::2]}` 与 `{S.s2[::2]}`：个数' + ('==一样==' if sorted(S.s1[::2]) == sorted(S.s2[::2]) else '==不一样==，直接短路')
            + (f'；奇数下标 `{S.s1[1::2]}` 与 `{S.s2[1::2]}`：个数' + ('==一样==' if sorted(S.s1[1::2]) == sorted(S.s2[1::2]) else '==不一样==')
               if sorted(S.s1[::2]) == sorted(S.s2[::2]) else '')
            + (f'。两组都要一样才行 → 返回 =={ret}==' if ret is not None else '')),
        'Counter(s1[1::2])': lambda S, B, ret: (
            f'奇数下标 `{S.s1[1::2]}` 与 `{S.s2[1::2]}`：个数' + ('==一样==' if sorted(S.s1[1::2]) == sorted(S.s2[1::2]) else '==不一样==')
            + (f' → 返回 =={ret}==' if ret is not None else '')),
    },
    cards=dict(
        one_liner='相距 2 的交换 = 偶数下标、奇数下标各自随便排',
        complexity='时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
        problem=['两个长度为 4 的字符串，可以交换同一字符串中相距 2 的两个字符，问能否变成相等',
                 '示例：`"abcd"` 和 `"cdab"` → `true`；`"abcd"` 和 `"dacb"` → `false`',
                 '本视频连着演示这两个示例'],
        quote='所有相距为偶数的字符都可以随意交换。所以只需要看下标为偶数的字符个数是否都一样，以及下标为奇数的字符个数是否都一样。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相距 4 的字符也能换：x-y-z 经三次相邻交换变成 z-y-x',
              '于是偶数下标的字符可任意重排，奇数下标同理',
              '`s1[::2]`、`s1[1::2]` 切出两组，用 `Counter` 比较个数',
              '`and` 会短路：偶数组不一样就不再看奇数组'],
        summary=['时间 `O(n+|Σ|)`，空间 `O(|Σ|)`，|Σ| = 26',
                 '易错点：偶、奇两组要分别比较，不能把整串放一起数',
                 '思考题 j-i=3：下标 0 与 3 互换、1 与 2 互换，要换一种分组'],
    ),
)
