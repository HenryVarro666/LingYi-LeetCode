CONFIG = dict(
    num=1317, title='将整数转换为两个无零整数的和', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位构造 · 借位',
    tags=['随机算法', '构造题', '难度分 1278'],
    code='''
class Solution:
    def getNoZeroIntegers(self, n: int) -> List[int]:
        a = 0
        base = 1  # 10**k
        x = n
        while x > 1:
            x, d = divmod(x, 10)
            if d <= 1:
                d += 10
                x -= 1  # 借位
            # a 这一位填 d//2，比如百位数就是 d//2 * 100
            a += d // 2 * base
            base *= 10
        return [a, n - a]
''',
    call='Solution().getNoZeroIntegers(400)',
    expect=[145, 255],
    views=[
        dict(type='text', h=90, size=34,
             fn=lambda S: f"n = ==`{S['n']}`==，a = ==`{S['a']}`==，b = n − a = ==`{S['n'] - S['a']}`==" if 'a' in S else ''),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"还没处理的高位 x = `{S['x']}`，当前这一位 d = `{S['d']}`" if 'd' in S else (f"还没处理的高位 x = `{S['x']}`" if 'x' in S else '')),
    ],
    watch=[('x', 'x', 'blue'), ('d', 'd', 'yellow'), ('base', 'base', 'cyan'), ('a', 'a', 'green')],
    captions={
        'a = 0': '`a` 从 0 开始，逐位拼出来；`b` 最后用 `n - a` 得到',
        'base = 1': '`base` 是当前位的权重，个位是 `1`',
        'x = n': '`x` 是还没处理的高位部分，先是整个 `n = {x}`',
        'while x > 1': lambda S, B, r: (f'`x = {S.x} > 1` → 还有数位要拆' if S.x > 1 else f'`x = {S.x} ≤ 1`：最高位 1（或已空）不用再拆，它整个给 b，a 的这一位是前导零'),
        'x, d = divmod': '取出最低位：`d = {d}`，剩下高位 `x = {x}`',
        'if d <= 1': lambda S, B, r: (f'`d = {S.d} ≤ 1`：拆不成两个非零数字 → 要借位' if S.d <= 1 else f'`d = {S.d} ≥ 2` → 可以拆成 `{S.d//2}` 和 `{S.d - S.d//2}`，两边都非零'),
        'd += 10': '借来 10：`d = {d}`，就能拆成两个非零数',
        'x -= 1': '高位借出 1：`x` → {x}',
        'a += d // 2': '`a` 这一位填 `d // 2 = {d // 2}`（权重 `{B.base}`）：`a` = =={a}==；`b` 这一位自然是另一半，也非零',
        'base *= 10': '权重进一位：`base = {base}`',
        'return [a': '`a = {a}`，`b = {n} - {a} = {n - a}`，两个数都不含 0',
    },
    cards=dict(
        one_liner='每一位都拆成两个非零数字，拆不动就向高位借 10',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['无零整数：十进制里不含数字 `0` 的正整数',
                 '给 `n`，返回 `[a, b]`，两个都是无零整数且 `a + b = n`',
                 '本视频：`n = 400` → `[145, 255]`'],
        quote='如果 d<=1，那么借位，把 d 变成 d+10，这样就能和上面一样分成两个非零数字，分配给 a 和 b。代码实现时，可以只考虑 a 怎么构造，最后用 n-a 得到 b。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`666 = 333 + 333`、`777 = 333 + 444`：每一位 `d ≥ 2` 拆成 `d//2` 和 `d - d//2`',
              '`d` 是 0 或 1 拆不开：==向高位借 1，当成 `d+10`==，如 `400 = 390 + 10`',
              '最高位若是 1，整个给 b，a 在这位是前导零，不算 0'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错点：借位时高位要同步 `x -= 1`，否则和不等于 n',
                 '易错点：循环条件是 `x > 1`，最高位为 1 时不用拆',
                 '另外两种写法：枚举 a 判断有没有 0（`O(n log n)`）；随机取 a，期望几次就找到'],
    ),
)
