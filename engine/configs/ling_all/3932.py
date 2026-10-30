CONFIG = dict(
    num=3932, title='统计区间内的完全 K 次幂数量', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='前缀差 + 开 k 次根',
    tags=[],
    code='''
class Solution:
    def f(self, n: int, k: int) -> int:
        if n < 0:
            return 0
        x = floor(n ** (1 / k))
        # 可能 x 的正确值是 6，但算出来的 x = floor(5.99999...) = 5
        if (x + 1) ** k <= n:  # 为避免浮点误差，这里用整数计算 pow
            x += 1
        return x + 1

    def countKthRoots(self, l: int, r: int, k: int) -> int:
        return self.f(r, k) - self.f(l - 1, k)
''',
    call='Solution().countKthRoots(9, 216, 3)',
    expect=4,
    setup='from math import floor',
    views=[
        dict(type='text', size=34, h=120, fn=lambda S: (
            f"求 `[0, {S['n']}]` 里的完全 {S['k']} 次幂：`x^{S['k']} ≤ {S['n']}`" if 'n' in S and 'k' in S and 'l' not in S else
            (f"`[{S['l']}, {S['r']}]` 内个数 = f({S['r']}) − f({S['l']-1})" if 'l' in S else ''))),
        dict(type='text', size=40, h=150, fn=lambda S: (
            f"`{S['n']} ** (1/{S['k']})` = =={S['n'] ** (1 / S['k'])!r}==" if 'n' in S and 'k' in S else '')),
        dict(type='text', size=40, h=150, fn=lambda S: (
            f"x = =={S['x']}==，`(x+1)^k = {(S['x']+1) ** S['k']}`，n = {S['n']}" if 'x' in S and 'n' in S else '')),
    ],
    watch=['l', 'r', 'k', 'n', 'x', ('ans', 'ans', 'green')],
    captions={
        'if n < 0': '`n = {n}`：`n < 0` 时区间里没有非负数 → {"返回 0" if n < 0 else "继续计算"}',
        'x = floor': '`x = floor({n} ** (1/{k}))` = =={x}==：浮点开根，可能有误差',
        'if (x + 1) ** k <= n': '`({x}+1)^{k} = {(x+1)**k}` 与 `n = {n}` 比：{"==≤ n，说明浮点算小了==" if (x+1)**k <= n else "> n，x 没算错"}',
        'x += 1': '整数验算发现 `x` 少 1，修正：`x` → =={x}==',
        'return x + 1': 'x 取 `0..{x}` 共 =={x + 1}== 个，所以 `f({n}, {k}) = {x + 1}`',
        'return self.f(r, k)': lambda S, B, ret: ('答案 = `f(r,k) − f(l−1,k)`：先算 `f(r,k)`，再算 `f(l−1,k)`' if ret is None else f'答案 = `f(r,k) − f(l−1,k)` = =={ret}=='),
        'return 0': '`n < 0`：没有完全 k 次幂，返回 0',
    },
    cards=dict(
        one_liner='前缀差：f(r) − f(l−1)，f(n) 就是 floor(n^(1/k)) + 1',
        complexity='时间 `O(log k)`，空间 `O(1)`',
        problem=['给整数 `l`、`r`、`k`，数 `[l, r]` 里有多少个 `y = x^k`（`x` 为整数）',
                 '示例：`l=8, r=30, k=2` → `3`（9、16、25）',
                 '本视频：`l=9, r=216, k=3` → `4`（27、64、125、216）'],
        quote='定义 f(n,k) 表示 [0,n] 中的完全 k 次幂的个数，那么答案为 f(r,k)-f(ℓ-1,k)',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x^k ≤ n` 即 `x ≤ n^(1/k)`，`x` 取 `0..floor(n^(1/k))`，共 `+1` 个',
              '`216 ** (1/3)` 算出 `5.999…`，floor 后是 5，少了 216 本身',
              '所以再用整数乘方验算 `(x+1)^k ≤ n`，成立就把 `x` 加一'],
        summary=['时间 `O(log k)`（整数快速幂），空间 `O(1)`',
                 '易错点：==浮点开根有误差==，必须用整数 pow 验算一步',
                 '易错点：`l = 0` 时 `f(-1)` 要返回 0，所以有 `n < 0` 判断',
                 '0 也是完全 k 次幂（`0^k = 0`），所以个数是 `x + 1`'],
    ),
)
