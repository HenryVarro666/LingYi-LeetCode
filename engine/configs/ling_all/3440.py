EV, ST, ET = 10, [0, 3, 7, 9], [1, 4, 8, 10]


def _gaps():
    return [ST[0]] + [ST[i] - ET[i - 1] for i in range(1, len(ST))] + [EV - ET[-1]]


def _gcol(S, i, v):
    if 'ans' in S and 'i' in S and S['_line'] >= 26 and S['i'] in (i, i - 1):
        return 'yellow'
    return None


def _txt(S):
    g = _gaps()
    if 'ans' not in S or 'sz' not in S:
        return f'空位长度 `{g}`（共 n+1 = {len(g)} 个）；桌子（会议）长度 `{[e - s for s, e in zip(ST, ET)]}`'
    i = S['i']
    return f"桌子 {i}：长 `{S['sz']}`，左右空位 `{g[i]}` 和 `{g[i + 1]}`；最大三空位下标 a={S['a']} b={S['b']} c={S['c']}"


CONFIG = dict(
    num=3440, title='重新安排会议得到最多空余时间 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='前三大空位 · 枚举桌子',
    tags=['灵神题单', '思维题', '难度分 1998'],
    code='''
class Solution:
    def maxFreeTime(self, eventTime: int, startTime: List[int], endTime: List[int]) -> int:
        n = len(startTime)

        # 计算空位长度
        def get(i: int) -> int:
            if i == 0:
                return startTime[0]
            if i == n:
                return eventTime - endTime[n - 1]
            return startTime[i] - endTime[i - 1]

        # 有 n+1 个空位，计算前三大的空位在哪
        a, b, c = 0, -1, -1
        for i in range(1, n + 1):
            sz = get(i)
            if sz > get(a):
                a, b, c = i, a, b
            elif b < 0 or sz > get(b):
                b, c = i, b
            elif c < 0 or sz > get(c):
                c = i

        ans = 0
        # 枚举桌子
        for i, (s, e) in enumerate(zip(startTime, endTime)):
            sz = e - s
            if i != a and i + 1 != a and sz <= get(a) or \\
               i != b and i + 1 != b and sz <= get(b) or \\
               sz <= get(c):  # 可以移出去
                ans = max(ans, get(i) + sz + get(i + 1))
            else:
                ans = max(ans, get(i) + get(i + 1))
        return ans
''',
    call=f'Solution().maxFreeTime({EV}, {ST}, {ET})',
    expect=6,
    skip=['n = len', 'def get', 'if i == 0:', 'if i == n:', 'return startTime[0]', 'return eventTime', 'return startTime[i]', 'a, b, c = 0'],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var=lambda S: _gaps(), label='空位长度（下标 0..n）：蓝 a 最大，粉 b 次大，紫 c 第三大，黄 当前桌子两侧',
             cell=96, pointers={'a': 'blue', 'b': 'pink', 'c': 'purple'}, color=_gcol, h=300),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('c', 'c', 'purple'), 'sz', ('ans', 'ans', 'green')],
    captions={
        'for i in range(1, n + 1)': '从下标 1 起扫描所有空位，维护最大的三个：`a ≥ b ≥ c`（下标）',
        'sz = get(i)': lambda S, B, r: f'空位 `{B.i}` 的长度 `sz = {_gaps()[B.i]}`',
        'if sz > get(a)': lambda S, B, r: (f'`{B.sz}` 比最大空位 `{_gaps()[B.a]}` 大 → ==成为新的 a==，原 a、b 顺位降为 b、c' if B.sz > _gaps()[B.a]
                                           else f'`{B.sz}` 不比最大空位 `{_gaps()[B.a]}` 大，看能不能当 b'),
        'elif b < 0': lambda S, B, r: (f'`b` 还没有（-1）→ ==直接成为 b==' if B.b < 0 else
                                       f'`{B.sz}` 比次大空位 `{_gaps()[B.b]}` 大 → 成为新的 b' if B.sz > _gaps()[B.b]
                                       else f'`{B.sz}` 不比次大空位 `{_gaps()[B.b]}` 大，看能不能当 c'),
        'elif c < 0': lambda S, B, r: ('`c` 还没有（-1）→ 成为 c' if B.c < 0 else
                                       f'`{B.sz}` 比第三大 `{_gaps()[B.c]}` 大 → 成为新的 c' if B.sz > _gaps()[B.c]
                                       else f'`{B.sz}` 不比第三大 `{_gaps()[B.c]}` 大，丢弃'),
        'a, b, c = i, a, b': '新最大：`a={a}, b={b}, c={c}`（三个空位的下标）',
        'b, c = i, b': '新次大：`b={b}, c={c}`',
        'c = i': '新第三大：`c={c}`',
        'ans = 0': '前三大空位：a={a}、b={b}、c={c}。==一张桌子只挨着两个空位==，三个里必有一个能用',
        'for i, (s, e)': '枚举桌子 `{i}`：左边是空位 `{i}`，右边是空位 `{i + 1}`',
        'sz = e - s': '桌子长度 `sz = {e} - {s} = {sz}`',
        'if i != a and': lambda S, B, r: (f"桌子 `{B.i}` 长 `{B.sz}`：先试 a（不相邻且 `{B.sz} <= {_gaps()[B.a]}`）"
                                          f"{'→ ==能移进 a==' if (B.i != B.a and B.i + 1 != B.a and B.sz <= _gaps()[B.a]) else '→ 不行'}"),
        'i != b and': lambda S, B, r: (f"再试 b（不相邻且 `{B.sz} <= {_gaps()[B.b]}`）"
                                       f"{'→ ==能移进 b==' if (B.i != B.b and B.i + 1 != B.b and B.sz <= _gaps()[B.b]) else '→ 不行'}"),
        'sz <= get(c)': lambda S, B, r: (f"最后试 c：`{B.sz} <= {_gaps()[B.c]}`" +
                                         ('，==能移出去==' if B.sz <= _gaps()[B.c] else '，放不下 → 这张桌子移不出去')),
        'ans = max(ans, get(i) + sz': lambda S, B, r: f'移出去后空位合并：`{_gaps()[B.i]} + {B.sz} + {_gaps()[B.i + 1]} = {_gaps()[B.i] + B.sz + _gaps()[B.i + 1]}`，`ans = {max(B.ans, _gaps()[B.i] + B.sz + _gaps()[B.i + 1])}`',
        'ans = max(ans, get(i) + get(i + 1))': lambda S, B, r: f'只能贴着邻居：`{_gaps()[B.i]} + {_gaps()[B.i + 1]} = {_gaps()[B.i] + _gaps()[B.i + 1]}`，`ans = {max(B.ans, _gaps()[B.i] + _gaps()[B.i + 1])}`',
        'return ans': '最长连续空余 `{ans}`',
    },
    cards=dict(
        one_liner='会议是桌子，空余是空位：只看最大的三个空位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['活动时长 `eventTime`，`n` 个不重叠会议，可以把==至多一个==会议平移（时长不变）',
                 '求移动后最长的连续空余时间',
                 '示例：`eventTime=10, start=[0,3,7,9], end=[1,4,8,10]` → `6`'],
        quote='计算长度最长的三个空位在哪，其中一定有一个空位不在移出去的桌子的左右两侧。如果空位长度大于等于桌子的长度，我们把桌子移到这个空位中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举桌子，想把它塞进别的空位；最大空位可能就挨着它',
              '一个桌子只有左右两个邻居空位，所以最大的三个空位里==至少有一个不相邻==',
              '能移出去：新空位 = 桌子长 + 左右空位；不能：只能贴邻居，= 左右空位之和'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '空位有 `n+1` 个（含两端），`get(0)` 和 `get(n)` 要单独处理',
                 '三个空位的更新用 `a, b, c = i, a, b` 级联顺位',
                 '灵神还给了写法二：先把空位存成数组 `free`，逻辑相同',
                 '本视频演示的是写法一（用 `get` 函数）'],
    ),
)
