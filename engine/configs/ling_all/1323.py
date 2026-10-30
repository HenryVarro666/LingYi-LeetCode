def _digits(S):
    return list(str(S['num']))


def _cur(S):
    n = len(str(S['num']))
    x = S['x']
    consumed = n if x == 0 else n - len(str(x))
    return n - consumed if 'd' in S else None


def _best(S):
    m = S.get('max_base', 0)
    return len(str(S['num'])) - len(str(m)) if m else None


class _P:
    def __call__(self, S):
        return _cur(S)

    def __str__(self):
        return '位'


def _txt(S):
    if 'base' not in S:
        return '从低位往高位取数位；记下==最高位的 6== 对应的权值 `base`'
    if S.get('_line') == 11:
        return f"答案 = `{S['num']} + {S['max_base']} × 3` = =={S['num'] + S['max_base'] * 3}=="
    return f"`base = {S['base']}`（当前位的权值），`max_base = {S['max_base']}`（目前见到的最高位 6 的权值）"


CONFIG = dict(
    num=1323, title='6 和 9 组成的最大数字', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='改最高位的 6 · 取数位',
    tags=['灵神题单', '难度分 1194'],
    code='''
class Solution:
    def maximum69Number(self, num: int) -> int:
        max_base = 0
        base = 1
        x = num
        while x:
            x, d = divmod(x, 10)
            if d == 6:
                max_base = base
            base *= 10
        return num + max_base * 3
''',
    call='Solution().maximum69Number(9669)',
    expect=9969,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var=_digits, label='num 的各位数字（黄 = 刚取出的位，绿 = 最高位的 6）',
             pointers={_P(): 'yellow'}, color=lambda S, i, v: 'green' if i == _best(S) else None, h=220),
    ],
    watch=[('x', 'x', 'blue'), ('d', 'd', 'yellow'), ('base', 'base', 'cyan'), ('max_base', 'max_base', 'green')],
    captions={
        'max_base = 0': '`max_base` 记录最高位 6 的权值；没有 6 就保持 `0`，答案不变',
        'base = 1': '`base` 是当前位的权值：个位 1，十位 10，……',
        'x = num': '复制一份 `x`，用来不断去掉最低位',
        'while x': lambda S, B, r: (f'`x = {S["x"]}` 还有数位，继续' if S['x'] else '`x = 0`：所有数位都看过了，退出循环'),
        'divmod(x, 10)': '`divmod(x, 10)`：取出最低位 `d = {d}`，`x` 去掉末位变成 `{x}`',
        'if d == 6': lambda S, B, r: (f'`d = 6`：这一位可以改成 9' if S['d'] == 6 else f'`d = {S["d"]}`：是 9，不用改'),
        'max_base = base': '从低到高扫，后遇到的 6 位更高 → 覆盖 `max_base = {max_base}`',
        'base *= 10': '权值乘 10，准备看更高一位：`base` → {base}',
        'return': '6 改成 9 增加 `3 × max_base`：`{num} + {max_base} × 3` = =={num + max_base * 3}==',
    },
    cards=dict(
        one_liner='6 改 9 才会变大，改最高位的 6 最划算',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['正整数 `num` 只含数字 6 和 9，最多翻转一位（6 变 9 或 9 变 6）',
                 '返回能得到的最大数字',
                 '示例：`9669` → `9969`'],
        quote='要想把数字变大，只能把 6 改成 9。……改高位的 6 比改低位的 6 更好。由于至多改一次，所以改最高位的 6。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用字符串：不断 `divmod(x, 10)` 取最低位',
              '用 `base` 记权值，遇到 6 就记下 `max_base = base`，最后记下的就是最高位的 6',
              '6 变 9 增加 `3 × 权值`，所以答案是 `num + max_base * 3`'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '没有 6 时 `max_base = 0`，答案就是 `num` 本身',
                 '方法一：`str(num).replace(\'6\', \'9\', 1)` 一行替换第一个 6，也是同一个贪心',
                 '思考题：求最小数字则改最高位的 9；至多翻转 k 位则从高到低改 k 个 6'],
    ),
)
