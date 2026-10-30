def _b(v, w):
    return format(v, 'b').zfill(w)


def _panel(S):
    n = S['n']
    w = len(format(n, 'b')) + 1
    out = [f"n　　　 = `{_b(n, w)}`", f"n >> 1　= `{_b(n >> 1, w)}`"]
    if S.get('_line', 0) >= 4 or 'x' in S:
        x = (n >> 1) ^ n
        out.append(f"x　　　 = `{_b(x, w)}`　异或：1 表示相邻两位不同")
        out.append(f"x + 1　 = `{_b(x + 1, w)}`")
        out.append(f"(x+1)&x = `{_b((x + 1) & x, w)}`")
    return '\n'.join(out)


def _cap_x(S, B, ret):
    n, x = S.n, S.x
    w = len(format(n, 'b')) + 1
    return (f"`n >> 1` 与 `n` 错开一位，一次异或就比较了==所有==相邻比特："
            f"`{_b(n >> 1, w)}` ^ `{_b(n, w)}` = `{_b(x, w)}`，每个 1 都代表“相邻两位不同”")


def _cap_ret(S, B, ret):
    x = S.x
    return (f"全 1 的数加一会一路进位成 100…0：`x + 1 = {format(x + 1, 'b')}`，与 `x` 没有公共位，"
            f"`(x+1) & x = {(x + 1) & x}` → =={ret}==")


CONFIG = dict(
    num=693, title='交替位二进制数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='错位异或 + 判全 1',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def hasAlternatingBits(self, n: int) -> bool:
        x = (n >> 1) ^ n
        return (x + 1) & x == 0
''',
    call='Solution().hasAlternatingBits(21)',
    expect=True,
    views=[
        dict(type='string', var="format(n, '06b')", label='n', h=150, index=False),
        dict(type='string', var="format(n >> 1, '06b')", label='n >> 1（错开一位）', h=150, index=False),
        dict(type='string', var=lambda S: format(S['x'], '06b') if 'x' in S else '------',
             label='x = (n >> 1) ^ n（1 = 相邻位不同）', h=150, index=False,
             color=lambda S, i, v: 'green' if v == '1' and 'x' in S else None),
        dict(type='text', fn=lambda S: (f"x + 1 = `{format(S['x'] + 1, '07b')}`　x & (x+1) = `{format((S['x'] + 1) & S['x'], '07b')}`"
                                        if S.get('_line', 0) >= 4 and 'x' in S else ''), size=34, h=90),
    ],
    watch=['n', 'x'],
    captions={
        'x = (n >> 1) ^ n': _cap_x,
        'return (x + 1) & x': _cap_ret,
    },
    cards=dict(
        one_liner='错位异或：一次判断所有相邻位是否都不同',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['判断正整数 `n` 的二进制是不是 0、1 交替出现',
                 '示例：`5 = 101` → `true`；`7 = 111` → `false`',
                 '本视频：`21 = 10101` → `true`'],
        quote='可以把 n 右移一位，得到 01010，再与 10101 做异或运算，计算的就是所有相邻比特位的异或值了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['异或：两位不同得 1，相同得 0', '`n >> 1` 与 `n` 错开一位，对应位就是相邻两位',
              '异或结果全为 1 ⇒ 所有相邻位都不同'],
        after=[dict(heading='怎么判断「全为 1」', lines=[
            '`x` 全为 1，则 `x + 1` 是 `100…0`',
            '`100…0` 与 `x` 没有公共位 → `(x + 1) & x == 0`',
            '这和 231. 2 的幂 是同一个技巧'])],
        summary=['时间、空间都是 `O(1)`，不用逐位循环',
                 '易错：别漏掉 `x + 1` 的括号，`+` 优先级高于 `&`，但写括号更清晰',
                 '`n` 为正，所以 `x` 至少有一位 1，不会误判全 0',
                 '同类：231. 2 的幂、191. 位 1 的个数'],
    ),
)
