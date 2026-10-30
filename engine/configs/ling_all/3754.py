CONFIG = dict(
    num=3754, title='连接非零数字并乘以其数字和 I', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位取模 + 拼接',
    code='''
class Solution:
    def sumAndMultiply(self, n: int) -> int:
        x, s, pow10 = 0, 0, 1
        while n:
            n, d = divmod(n, 10)
            if d > 0:
                x += d * pow10
                s += d
                pow10 *= 10
        return x * s
''',
    call='Solution().sumAndMultiply(10203004)',
    expect=12340,
    views=[
        dict(type='string', var=lambda S: str(S['n']) if S.get('n') else '（n 已为 0）', label='剩余的 n', h=170, cell=80),
        dict(type='text', size=30, h=70, fn=lambda S: (f"x = =={S['x']}==　　数字和 s = =={S['s']}==　　下一个数位权重 pow10 = {S['pow10']}" if 'x' in S else '')),
        dict(type='text', size=28, h=60, fn=lambda S: (f"本次取出数位 d = ==={S['d']}===" .replace('===', '==') if 'd' in S else '')),
    ],
    watch=['n', ('d', 'd', 'yellow'), ('x', 'x', 'green'), ('s', 's', 'blue'), 'pow10'],
    captions={
        'x, s, pow10': '`x` 是拼出的新数，`s` 是数字和，`pow10` 是下一个非零数位该放的位权，初始 1',
        'while n': lambda S, B, r: (f'`n = {S.n}` 还没取完，继续' if S.n else '`n = 0`：所有数位都取完了 → 退出循环'),
        'divmod': '`divmod({B.n}, 10)`：商 `n = {n}` 留着下一轮，余数 `d = {d}` 就是当前最低位',
        'if d > 0': lambda S, B, r: (f'`d = {S.d} > 0`：非零数位，要拼进 x' if S.d > 0 else '`d = 0`：是零，直接丢掉（不动 x、s、pow10）'),
        'x += d': '`x += d × pow10 = {d} × {B.pow10}` → x = =={x}==（新数位放在已有数位的左边）',
        's += d': '数字和累加：`s` = =={s}==',
        'pow10 *= 10': 'x 长了一位 → `pow10` 变成 {pow10}。==只有非零数位才让它变大==，所以零被“跳过”了',
        'return': '`x × s = {x} × {s}` = =={ret}==',
    },
    cards=dict(
        one_liner='从低位往高位取数，非零数位按位权直接拼成 x',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['去掉整数 `n` 里的所有 0，剩下的数字按原顺序连成新整数 `x`',
                 '答案是 `x × (x 的数字和)`',
                 '示例：`n = 10203004` → `x = 1234`，数字和 `10` → `12340`'],
        quote='不断地把 n 除以 10（下取整）直到 0……对于不为零的数位 d，通过 d·10^k 组合起来，其中 k 是当前 x 的十进制长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`divmod(n, 10)` 每次拿到最低位 `d`，商留给下一轮',
              '是零就跳过；非零就 `x += d * pow10`，再把 `pow10` 乘 10',
              '因为从低位往高位处理，新数位总放在 x 的最左边，位权正好是 x 当前长度对应的 10 的幂'],
        summary=['时间 `O(log n)`（十进制位数），空间 `O(1)`',
                 '易错：`pow10` 只在遇到非零数位时才乘 10，否则会把零也“占位”',
                 '`n = 0` 或全是零时循环不进入，`x = 0`，返回 0',
                 '相似题：3726 移除十进制表示中的所有零'],
    ),
)
