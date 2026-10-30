def _pre():
    ip = [0, 0] + [1] * 999
    for i in range(2, 32):
        if ip[i]:
            for j in range(i * i, 1001, i):
                ip[j] = 0
    pr = ip[:]
    for i in range(1, 1001):
        ip[i] = ip[i - 1] + (i if ip[i] else 0)
    return pr, ip


_ISP, _PRE = _pre()
_RNG = list(range(13, 32))


def _txt(S):
    if 'r' not in S:
        return '先把 `n` 反转成 `r`，再用质数前缀和 `O(1)` 求区间质数和'
    if 'x' in S and S['x'] > 0:
        return f"`r = {S['r']}`：`n` 的数字从个位起依次接到 `r` 末尾，还剩 `x = {S['x']}`"
    n, r = S['n'], S['r']
    lo, hi = min(n, r), max(n, r)
    return f"`[{lo}, {hi}]` 的质数和 = `前缀[{hi}] − 前缀[{lo - 1}]` = `{_PRE[hi]} − {_PRE[lo - 1]}` = =={_PRE[hi] - _PRE[lo - 1]}=="


CONFIG = dict(
    num=3918, title='数与其逆序数之间的质数和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='埃氏筛 + 质数前缀和 + 数位反转',
    tags=['灵神题单·数学算法', '数学算法', '难度分 1301'],
    code='''
MX = 1001
is_prime = [0, 0] + [1] * (MX - 2)
for i in range(2, isqrt(MX) + 1):
    if is_prime[i]:
        for j in range(i * i, MX, i):
            is_prime[j] = 0

# 原地计算 is_prime 的质数前缀和
for i in range(1, MX):
    is_prime[i] = is_prime[i - 1] + (i if is_prime[i] else 0)

class Solution:
    def sumOfPrimesInRange(self, n: int) -> int:
        r = 0
        x = n
        while x > 0:
            r = r * 10 + x % 10
            x //= 10
        return is_prime[max(n, r)] - is_prime[min(n, r) - 1]
''',
    call='Solution().sumOfPrimesInRange(13)',
    expect=132,
    views=[
        dict(type='array', var=_RNG, label='区间 [13, 31]（粉 = 质数）', h=190, cell=50,
             color=lambda S, i, v: 'pink' if _ISP[v] else None,
             dim=lambda S, i, v: 'x' in S and 'r' in S and S['x'] == 0 and not (min(S['n'], S['r']) <= v <= max(S['n'], S['r']))),
        dict(type='text', size=32, h=130, fn=_txt),
        dict(type='text', size=28, h=90, fn=lambda S: '质数：`13 + 17 + 19 + 23 + 29 + 31 = 132`' if 'x' in S and S['x'] == 0 else ''),
    ],
    watch=[('n', 'n', 'blue'), ('x', 'x', 'cyan'), ('r', 'r', 'pink')],
    max_steps=40,
    captions={
        'r = 0': '`r` 存反转后的数，从 0 开始',
        'x = n': '用 `x` 拆数位，保留原来的 `n`（最后要比较大小）',
        'while x > 0': lambda S, B, r: (f'`x = {S.x} > 0`，还有数位' if S.x > 0 else '`x = 0`，数位拆完'),
        'r = r * 10': '最低位 `d = {x % 10}`（`x % 10`）接到 `r` 末尾：`{B.r} × 10 + {x % 10}` = =={r}==',
        'x //= 10': '去掉个位：`x` → =={x}==',
        'return is_prime': lambda S, B, r: f'`[{min(S.n, S.r)}, {max(S.n, S.r)}]` 内质数和 = `is_prime[{max(S.n, S.r)}] − is_prime[{min(S.n, S.r) - 1}]` = `{_PRE[max(S.n, S.r)]} − {_PRE[min(S.n, S.r) - 1]}` = =={r}==',
    },
    cards=dict(
        one_liner='质数前缀和一减，反转数字用除十取余',
        complexity='时间 `O(log n)`，空间 `O(1)`（不计预处理）',
        problem=['`r` 是把 `n` 的数字反转得到的整数',
                 '求 `[min(n, r), max(n, r)]` 内所有==质数的和==',
                 '示例：`n = 13`，`r = 31`，质数 13、17、19、23、29、31，和为 `132`',
                 '示例：`n = 10`，`r = 1` → `17`；`n = 8` → `0`'],
        quote='用筛法预处理每个数是不是质数，然后把非质数视作 0，计算前缀和。……不断地把 n 除以 10（下取整）直到 0……计算 r·10+d，可以把数字 d 添加到 r 的末尾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n <= 1000`，先筛出 `[0, 1000]` 的质数',
              '非质数当 0，原地做前缀和：`is_prime[i]` = `1..i` 的质数和',
              '区间和 = `pre[hi] − pre[lo−1]`，不用字符串反转数字'],
        before=[dict(heading='预处理：筛 + 前缀和', lines=['埃氏筛：`is_prime[j] = 0`，`j` 是质数 `i` 的倍数', '再原地累加：`is_prime[i] += is_prime[i-1]`，非质数加 0', '之后 `is_prime[i]` 就是 `1..i` 的质数和', '例如 `is_prime[10] = 2+3+5+7 = 17`'])],
        summary=['时间 `O(log n)`，预处理 `O(MX log log MX)` 只做一次',
                 '易错点：反转后 `r` 可能比 `n` 小（如 `10 → 1`），要用 `max/min`',
                 '易错点：左端点要减 `is_prime[min − 1]`，不是 `min`；`min >= 1` 所以不越界',
                 '原地复用同一个数组既当质数表又当前缀和，省空间'],
    ),
)
