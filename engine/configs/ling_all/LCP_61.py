A = [21, 18, 18, 18, 31]
B_ = [34, 32, 16, 16, 17]


def _i(S):
    """current pair index: first i with (A[i],B[i]) == (a1,b1) and (A[i+1],B[i+1]) == (a2,b2)"""
    if 'a1' not in S:
        return -1
    a, b = S['temperatureA'], S['temperatureB']
    for i in range(len(a) - 1):
        if (a[i], b[i], a[i + 1], b[i + 1]) == (S['a1'], S['b1'], S['a2'], S['b2']):
            return i
    return -1


def _sign(x, y):
    return (x > y) - (x < y)


def _name(s):
    return {1: '上升', 0: '平稳', -1: '下降'}[s]


def _text(S):
    if 'a1' not in S:
        return '把相邻两天的变化分成 上升(1) / 平稳(0) / 下降(-1)，两地相同就是 T'
    sa, sb = _sign(S['a1'], S['a2']), _sign(S['b1'], S['b2'])
    ok = sa == sb
    return (f"A：`{S['a1']}→{S['a2']}` ={_name(sa)}({sa})　B：`{S['b1']}→{S['b2']}` ={_name(sb)}({sb})　→ "
            + ('==趋势相同 T==' if ok else '==趋势不同 F=='))


def _inrun(S, k):
    i = _i(S)
    return i >= 0 and S['same'] > 0 and i - S['same'] + 1 <= k <= i + 1


CONFIG = dict(
    num='LCP 61', title='气温变化趋势', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='比较大小转 T/F · 最长连续 T',
    tags=[],
    code='''
class Solution:
    def temperatureTrend(self, temperatureA: List[int], temperatureB: List[int]) -> int:
        ans = same = 0
        for (a1, b1), (a2, b2) in pairwise(zip(temperatureA, temperatureB)):
            if (a1 > a2) - (a1 < a2) == (b1 > b2) - (b1 < b2):
                same += 1
                ans = max(ans, same)
            else:
                same = 0
        return ans
''',
    call=f'Solution().temperatureTrend({A!r}, {B_!r})',
    expect=2,
    views=[
        dict(type='array', var='temperatureA', label='temperatureA', h=200,
             pointers={'a1': 'blue'} if False else {},
             window=None,
             color=lambda S, i, v: 'green' if _inrun(S, i) else ('yellow' if _i(S) in (i, i - 1) and _i(S) >= 0 else None)),
        dict(type='array', var='temperatureB', label='temperatureB', h=200,
             color=lambda S, i, v: 'green' if _inrun(S, i) else ('yellow' if _i(S) in (i, i - 1) and _i(S) >= 0 else None)),
        dict(type='text', fn=_text, size=28, h=130),
    ],
    watch=[('same', 'same', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = same = 0': '`same` 是当前连续相同趋势的天数，`ans` 记最大值，都从 0 开始',
        'for (a1, b1)': lambda S, B, r: ('相邻两天都比完了，循环结束' if _i(S) == _i(B) and 'a1' in B
                                          else f'取相邻两天：A `{S.a1}→{S.a2}`，B `{S.b1}→{S.b2}`'),
        'if (a1 > a2)': lambda S, B, r: (f'趋势：A 是 `{_sign(S.a1, S.a2)}`，B 是 `{_sign(S.b1, S.b2)}` → '
                                         + ('==相同 (T)==' if _sign(S.a1, S.a2) == _sign(S.b1, S.b2) else '==不同 (F)==')),
        'same += 1': '趋势相同，连续相同天数 `same` → =={same}==',
        'ans = max': '`ans = max({B.ans}, {same})` = =={ans}==',
        'same = 0': '趋势不同，连续中断，`same` 清零',
        'return ans': '最长连续 T 的长度：==`{ans}`==',
    },
    cards=dict(
        one_liner='两地趋势相同记 T，不同记 F，求最长连续 T',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两地每天气温 `temperatureA`、`temperatureB`',
                 '相邻两天：升 / 平 / 降，两地趋势相同的最大连续天数',
                 '示例：`A=[21,18,18,18,31]`，`B=[34,32,16,16,17]` → `2`'],
        quote='把相同的变化趋势视作 T，不同的变化趋势视作 F，问题变成：计算最长连续 T 的长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`(x > y) - (x < y)` 把大小关系变成 `1 / 0 / -1`',
              '两地的值相等就是 T：`same += 1` 并更新答案',
              '不等就是 F：`same = 0`，重新数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 'bool 可隐式转 0/1，`(x > y) - (x < y)` 就是 `cmp(x, y)`',
                 '`pairwise(zip(A, B))` 一次取出相邻两天的两地温度',
                 '示例转成 `TFTT`，最长连续 T 为 2'],
    ),
)
