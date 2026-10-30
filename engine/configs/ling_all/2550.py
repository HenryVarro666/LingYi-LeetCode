def _outcomes(S):
    n = S['n']
    return list(range(2 ** n))


def _color(S, i, v):
    n = S['n']
    return 'green' if i in (0, 2 ** n - 1) else 'red'


def _text(S):
    n = S['n']
    return f'`{n}` 只猴子各 2 种走法，共 `2^{n} = {2 ** n}` 种；只有全顺 / 全逆 2 种安全 → 碰撞 `{2 ** n} − 2 = {2 ** n - 2}`'


CONFIG = dict(
    num=2550, title='猴子碰撞的方法数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='正难则反 · 快速幂',
    tags=['灵神题单', '难度分 1663'],
    code='''
class Solution:
    def monkeyMove(self, n: int) -> int:
        MOD = 1_000_000_007
        return (pow(2, n, MOD) - 2) % MOD
''',
    call='Solution().monkeyMove(4)',
    expect=14,
    views=[
        dict(type='text', fn=_text, h=110),
        dict(type='array', var=_outcomes, color=_color, label='全部 2^n 种走法（数字的二进制位 = 每只猴子的方向；绿 = 不碰撞，红 = 碰撞）', index=False, h=260),
    ],
    watch=['n', ('MOD', 'MOD', 'cyan')],
    captions={
        'MOD =': '答案要对 `10^9 + 7` 取余，先记下 `MOD`',
        'return (pow': '`pow(2, n, MOD)` 用==快速幂==直接算 `2^n mod MOD` = `{pow(2, n, MOD)}`，再 `- 2` 去掉不碰撞的两种；`% MOD` 保证结果非负 → =={ret}==',
    },
    cards=dict(
        one_liner='正难则反：只有全顺时针、全逆时针才不碰撞',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['正 `n` 边形每个顶点一只猴子，同时沿顺时针或逆时针走一步',
                 '有两只猴子到同一顶点，或在一条边上相遇，就算碰撞',
                 '求至少碰撞一次的走法数，对 `10^9 + 7` 取余；示例 `n=3` → `6`，`n=4` → `14`'],
        before=[dict(heading='为什么只有两种不碰撞', lines=['有一只猴子方向和邻居不同，要么撞在顶点上，要么撞在边上',
                                                         '所以所有猴子必须方向一致',
                                                         '全顺时针 或 全逆时针，一共 `2` 种',
                                                         '`n = 4`：总走法 `2^4 = 16`，碰撞 `16 − 2 = 14`'])],
        quote='正难则反，只有全部顺时针和全部逆时针才不会碰撞。答案「所有移动方法」减去「不会碰撞的移动方法」，即 2^n-2。用快速幂计算。注意为了避免负数，需要在 -2 后再转换到非负数上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每只猴子两种选择，总方案 `2^n`',
              '碰撞数 = 总数 − 不碰撞数 = `2^n − 2`',
              '`n` 到 `10^9`：用 `pow(2, n, MOD)`，对 `MOD` 取余后再减 2'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`pow(2, n, MOD)` 可能是 `0`、`1`，减 2 会变负，所以要再 `% MOD`',
                 '`pow(a, b, m)` 是 Python 内置的快速幂，无需手写',
                 '正难则反：直接数碰撞很难，数不碰撞的很容易'],
    ),
)
