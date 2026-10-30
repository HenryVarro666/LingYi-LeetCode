def _pair(S):
    if 'xa' not in S:
        return ''
    f = lambda x, y: '尚未确定' if x is None else f'把 {x} 换成 {y}'
    return f'a（最小）：{f(S["xa"], S["ya"])}　　b（最大）：{f(S["xb"], S["yb"])}'


def _build(S):
    if 'a' not in S or 'now_num' not in S or 'index' in S and S['_line'] < 25:
        return ''
    return f'`a = {S["a"]}`　`b = {S["b"]}`'


CONFIG = dict(
    num=1432, title='改变一个整数能得到的最大差值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='高位决定 x · 逐位拼出 a 和 b',
    tags=['灵神题单', '难度分 1427'],
    code='''
class Solution(object):
    def maxDiff(self, num):
        num_list = []
        tmp = num
        while tmp:
            num_list.append(tmp % 10)
            tmp //= 10

        num_list.reverse()

        xa = ya = None
        xb = yb = None
        for index, now_num in enumerate(num_list):
            if now_num != 9 and xb is None:
                xb = now_num
                yb = 9

            if xa is None:
                if index == 0 and now_num != 1:
                    xa = now_num
                    ya = 1
                elif index > 0:
                    if  now_num != num_list[0] and now_num != 0:
                        xa = now_num
                        ya = 0
                    elif now_num > 1:
                        xa = now_num
                        ya = 1

        a = b = 0
        for now_num in num_list:
            a *= 10
            if xa == now_num:
                a += ya
            else:
                a += now_num

            b *= 10
            if xb == now_num:
                b += yb
            else:
                b += now_num

        return b - a
''',
    call='Solution().maxDiff(9288)',
    expect=8700,
    views=[
        dict(type='text', fn=lambda S: f'`num = {S["num"]}`，拆成数位后高位在前' if 'num' in S else '', size=26),
        dict(type='array', var='num_list', label='num_list（粉 = 当前处理的数位）', cell=84,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'pink' if 'index' in S and i == S['index'] else None),
        dict(type='text', fn=_pair, size=26),
        dict(type='text', fn=lambda S: (f'逐位拼出：`a = {S["a"]}`，`b = {S["b"]}`' if 'a' in S else ''), size=28),
    ],
    watch=[('index', 'index', 'pink'), ('xa', 'xa', 'blue'), ('ya', 'ya', 'blue'), ('xb', 'xb', 'green'), ('yb', 'yb', 'green'),
           ('a', 'a', 'cyan'), ('b', 'b', 'orange')],
    skip=['num_list.append', 'tmp = num', 'tmp //= 10', 'num_list = []'],
    captions={
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}`，还有数位 → 用 `% 10` 取个位，`//= 10` 去掉个位' if S.tmp else '`tmp = 0`：数位取完了'),
        'num_list.reverse()': '反转后高位在前：`{num_list}`',
        'xa = ya = None': '`a` 要最小：`xa` 是被换掉的数字，`ya` 是换成的数字，先设为空',
        'xb = yb = None': '`b` 要最大：同样的 `xb`、`yb`',
        'for index, now_num in enumerate': lambda S, B, r: (f'处理第 `{S.index}` 位：`now_num = {S.now_num}`' if S.get('index') != B.get('index') or 'index' not in B else '数位遍历完，`xa/ya`、`xb/yb` 都定好了'),
        'if now_num != 9 and xb is None': lambda S, B, r: (
            f'`{S.now_num} != 9` 且 `xb` 还没定 → 这是最高的非 9 数字' if S.now_num != 9 and S.xb is None
            else ('这位是 9，换了反而变小，跳过' if S.now_num == 9 else '`xb` 已经定下，不再改')),
        'yb = 9': '`b` 最大：把 `{xb}` 全换成 `9`',
        'if xa is None': lambda S, B, r: ('`xa` 还没确定，继续找可替换的数字' if S.xa is None else '`xa` 已经确定，不用再找'),
        'if index == 0 and now_num != 1': lambda S, B, r: (
            f'最高位 `{S.now_num}` 不是 1 → 把它换成 1' if S.index == 0 and S.now_num != 1
            else ('最高位已经是 1，不能再换（不能换成 0），看后面' if S.index == 0 else '不是最高位，看下面的分支')),
        'xa = now_num': '`xa` = `{xa}`',
        'ya = 1': '`ya = 1`：换成 1（首位不能换成 0，会有前导 0）',
        'ya = 0': '`ya = 0`：这位不同于最高位且不为 0，换成 0 不会出现前导 0',
        'if  now_num != num_list[0] and now_num != 0': lambda S, B, r: (
            f'`{S.now_num}` 不同于最高位 `{S.num_list[0]}` 且不为 0 → 可以换成 0' if S.now_num != S.num_list[0] and S.now_num != 0
            else f'`{S.now_num}` 与最高位相同或为 0 → 换成 0 会出问题，看下一个条件'),
        'elif now_num > 1': lambda S, B, r: (f'`{S.now_num} > 1` → 可以换成 1' if S.now_num > 1 else f'`{S.now_num}` 不大于 1，没法再变小'),
        'a = b = 0': '替换方案定好了，再逐位拼出 `a`（最小）和 `b`（最大）',
        'a *= 10': '`a` 左移一位',
        'if xa == now_num': lambda S, B, r: (f'`{S.now_num}` 就是 `xa` → 这一位用 `ya = {S.ya}`' if S.xa == S.now_num else f'`{S.now_num}` 不是 `xa` → 保持原样'),
        'b *= 10': '`b` 左移一位',
        'if xb == now_num': lambda S, B, r: (f'`{S.now_num}` 就是 `xb` → 这一位用 `yb = {S.yb}`' if S.xb == S.now_num else f'`{S.now_num}` 不是 `xb` → 保持原样'),
        'a += ya': '`a` → {a}',
        'a += now_num': '`a` → {a}',
        'b += yb': '`b` → {b}',
        'b += now_num': '`b` → {b}',
        'return b - a': '`b − a` = `{b} − {a}` = =={ret}==',
    },
    cards=dict(
        one_liner='a 取最小、b 取最大，二者之差就是最大差值',
        complexity='时间 `O(log num)`，空间 `O(log num)`',
        problem=['对整数 `num` 做两次「把所有数字 `x` 换成 `y`」，结果 `a`、`b` 不能有前导 0 且不为 0',
                 '求 `a` 和 `b` 的最大差值',
                 '示例：`9288` → `8700`'],
        quote='为了让b尽可能小，我们应当将位数最高，且不是0的数替换成0。但是还有一个条件是替换后的数字不能有前导0，因此在这里需要做一些调整。',
        quote_src='—— yiduobo 题解原文（原文中 a 取最大，代码里为 b 最大 / a 最小）',
        idea=['先把数位拆出来，高位在前',
              '最大：最高的非 9 数字换成 9；最小：最高位不是 1 就换成 1',
              '最高位是 1 时：后面第一个「不同于首位且不为 0」的换成 0，或大于 1 的换成 1',
              '定好 `x`、`y` 后逐位拼出两个数，相减'],
        summary=['时间 `O(log num)`，空间 `O(log num)`',
                 '易错：最小值不能把首位换成 0（前导 0）',
                 '原文为 Python 2 写法，整数除法 `tmp /= 10` 已改为 `tmp //= 10`',
                 '代码里 `a` 是最小、`b` 是最大，最后返回 `b - a`',
                 '对比灵神：灵神直接用 `s.replace` 一次换完；这里手工拆位再逐位拼数'],
    ),
)
