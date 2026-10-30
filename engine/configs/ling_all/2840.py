CONFIG = dict(
    num=2840, title='判断通过操作能否让字符串相等 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='等价转化 · 奇偶下标分组',
    tags=['灵神题单', '难度分 1486'],
    code='''
class Solution:
    def checkStrings(self, s1: str, s2: str) -> bool:
        return Counter(s1[::2]) == Counter(s2[::2]) and \\
               Counter(s1[1::2]) == Counter(s2[1::2])
''',
    call='Solution().checkStrings("abcdba", "cabdab")',
    expect=True,
    views=[
        dict(type='string', var='s1', label='s1', h=190,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='string', var='s2', label='s2', h=190,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='map', var=lambda S: dict(Counter(S['s1'][::2])), label='s1 偶数下标（蓝）字符计数', h=125, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='map', var=lambda S: dict(Counter(S['s2'][::2])), label='s2 偶数下标（蓝）字符计数', h=125, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='map', var=lambda S: dict(Counter(S['s1'][1::2])), label='s1 奇数下标（粉）字符计数', h=125, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='map', var=lambda S: dict(Counter(S['s2'][1::2])), label='s2 奇数下标（粉）字符计数', h=125, fmt=lambda k, v: f'{k}:{v}'),
    ],
    watch=[('s1[::2]', 's1[::2]', 'blue'), ('s2[::2]', 's2[::2]', 'blue'), ('s1[1::2]', 's1[1::2]', 'pink'), ('s2[1::2]', 's2[1::2]', 'pink')],
    captions={
        'return Counter': lambda S, B, r: ('两组都一致 → 能让两串相等：==' + str(r) + '==' if r is not None else f'先比偶数下标：`{S.s1[::2]}` 与 `{S.s2[::2]}`，字符个数一致吗？（同奇偶可随意换位，只看个数）'),
        'Counter(s1[1::2])': '再比奇数下标：`{s1[1::2]}` 与 `{s2[1::2]}`，字符个数也一致 → 两组都满足才返回 True',
    },
    cards=dict(
        one_liner='相距偶数可任意交换，只看奇偶两组的字符个数',
        complexity='时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
        problem=['两个等长小写字符串，可对任一个交换下标差为偶数的两个字符，次数不限',
                 '问能否让 `s1` 和 `s2` 相等',
                 '本视频：`s1 = "abcdba"`，`s2 = "cabdab"` → `true`'],
        quote='既然可以交换相距为 `2` 的字符，那么相距为 `4` 的字符可以通过多次交换实现。……所有相距为偶数的字符都可以随意交换。',
        quote_src='—— 灵茶山艾府题解',
        idea=['下标差为偶数 = 同奇偶；相距 2 的交换就能拼出任意同奇偶交换',
              '所以偶数下标的字符可以任意排列，奇数下标的字符也可以',
              '只需比较两个字符串偶数位的字符个数、奇数位的字符个数是否分别一致'],
        after=[dict(heading='为什么相距 2 就够了', lines=['`x y z` 想变成 `z y x`（相距 4 交换）：', '`x y z` → `y x z` → `y z x` → `z y x`，每步都只换相距 2 的两个字符', '所以任意偶数距离的交换都能由相距 2 的交换拼出来'])],
        summary=['时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
                 '易错：下标 0 起算，`[::2]` 是偶数下标，`[1::2]` 是奇数下标',
                 '偶数组和奇数组要分别比较，不能混在一起',
                 '`Counter` 比较的是字符出现次数，顺序无关',
                 '思考题：`j-i=3` 时，奇偶组可以互相换，要换个思路'],
    ),
)
