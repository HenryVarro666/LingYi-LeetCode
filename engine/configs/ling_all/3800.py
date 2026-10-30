def _col(S, i, v):
    s, t = S['s'], S['t']
    if s[i] == t[i]:
        return None
    return 'cyan' if s[i] == '0' else 'orange'


def _txt(S, B):
    if 'a' not in S:
        return '把不相等的下标分成 `01` 和 `10` 两类：青色 = `01`，橙色 = `10`'
    if 'res1' not in S:
        return f"`01` 共 a = =={S['a']}==，`10` 共 b = =={S['b']}==（保证 a ≤ b）"
    out = f"情况一 只翻转 `{S['res1']}`"
    if 'res2' in S:
        out += f"　情况二 串内交换 `{S['res2']}`"
    if 'res3' in S:
        out += f"　情况三 串间交换 `{S['res3']}`"
    return out


CONFIG = dict(
    num=3800, title='使二进制字符串相等的最小成本', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 三种情况取最小', tags=['灵神题单', '难度分 1841'],
    code='''
class Solution:
    def minimumCost(self, s: str, t: str, flipCost: int, swapCost: int, crossCost: int) -> int:
        # 更快的写法见【Python3 写法二】
        cnt = Counter(x + y for x, y in zip(s, t))

        a = cnt["01"]
        b = cnt["10"]
        if a > b:
            a, b = b, a

        res1 = (a + b) * flipCost
        res2 = a * swapCost + (b - a) * flipCost
        avg, rem = divmod(a + b, 2)
        res3 = (avg - a) * crossCost + avg * swapCost + rem * flipCost
        return min(res1, res2, res3)
''',
    call='Solution().minimumCost("01000", "10111", 10, 2, 2)',
    expect=16,
    views=[
        dict(type='string', var='s', label='s', h=170, cell=80, color=_col),
        dict(type='string', var='t', label='t', h=170, cell=80, color=_col),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k} → {v}', h=150),
        dict(type='text', fn=_txt, size=24, h=110),
    ],
    watch=['a', 'b', ('res1', 'res1', 'blue'), ('res2', 'res2', 'pink'), ('res3', 'res3', 'cyan')],
    captions={
        'cnt = Counter': '按下标把 `s[i]t[i]` 拼成两位串并计数：`01` 和 `10` 就是不相等的下标，`00`、`11` 已经相等',
        'a = cnt': '`s[i]=0` 且 `t[i]=1` 的下标有 `a = {a}` 个',
        'b = cnt': '`s[i]=1` 且 `t[i]=0` 的下标有 `b = {b}` 个',
        'if a > b': lambda S, B, r: ('`a > b`：交换 a、b，保证 a ≤ b' if S.a > S.b else '`a ≤ b`，不用交换'),
        'a, b = b, a': '交换后 `a = {a}`，`b = {b}`，后面公式要求 ==a ≤ b==',
        'res1 =': '情况一：只翻转，`(a+b) × flipCost` = `{a+b} × {flipCost}` = =={res1}==',
        'res2 =': '情况二：串内交换 a 对（每对省 2 次翻转）再翻转剩余 `b-a`：`{a}×{swapCost} + {b-a}×{flipCost}` = =={res2}==',
        'avg, rem': '情况三：用串间交换让两类尽量均匀，`avg = (a+b)//2 = {avg}`，余 `{rem}` 个只能翻转',
        'res3 =': '情况三：`(avg−a)×crossCost + avg×swapCost + rem×flipCost` = `{avg-a}×{crossCost} + {avg}×{swapCost} + {rem}×{flipCost}` = =={res3}==',
        'return min': '三种情况取最小：`min({res1}, {res2}, {res3})` = =={min(res1, res2, res3)}==',
    },
    cards=dict(
        one_liner='先数 01 和 10 各几个，再在三种策略里取最便宜',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`、`t` 等长，可翻转一位（flip）、串内交换两位（swap）、同下标跨串交换（cross）',
                 '各有一个成本，求让 `s == t` 的最小总成本',
                 '示例：`s=01000, t=10111`，成本 `10, 2, 2` → `16`'],
        quote='所以要么不交换，要么全交换，没有中间选项。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心 `01` 的个数 a 和 `10` 的个数 b，不妨 a ≤ b',
              '情况一只翻转；情况二先串内交换 a 对，再翻转 `b−a` 个',
              '情况三用串间交换让 a、b 更均匀，多做串内交换，最后余 1 个翻转',
              '成本都是线性的，最小值只在端点或交点取到，三种取最小即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：必须先保证 `a ≤ b` 再套公式',
                 '易错：情况三 `avg` 取 `(a+b)//2`，余数个下标只能翻转',
                 '灵神还给了写法二：用位运算 `bit_count` 统计 a、b，更快，公式相同'],
    ),
)
