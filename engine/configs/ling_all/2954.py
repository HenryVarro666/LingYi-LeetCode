def _cells(S):
    n, a = S['n'], S['a']
    return ['病' if i in a else '' for i in range(n)]


def _color(S, i, v):
    return 'pink' if i in S['a'] else None


def _txt(S):
    if 'ans' not in S:
        return '病人把两侧的空位分成若干段：==两头各 1 种传染方向，中间段每段 2^(k-1) 种=='
    n, a = S['n'], S['a']
    segs = [f'{a[0]}'] + [f'{q - p - 1}' for p, q in pairwise(a)] + [f'{n - 1 - a[-1]}']
    return f'各段空位数：`{" , ".join(segs)}`；中间段 k>1 时指数 `e += k-1`，现在 `e = {S.get("e", 0)}`'


CONFIG = dict(
    num=2954, title='统计感冒序列的数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='多重集排列数 + 2^e',
    tags=['组合数学', '难度分 2645'],
    code='''
class Solution:
    def numberOfSequence(self, n: int, a: List[int]) -> int:
        ans = fac[n - len(a)] * inv_fac[a[0]] * inv_fac[n - 1 - a[-1]] % MOD
        e = 0
        for p, q in pairwise(a):
            k = q - p - 1
            if k > 1:
                e += k - 1
                ans = ans * inv_fac[k] % MOD
        return ans * pow(2, e, MOD) % MOD
''',
    setup='''
MOD = 1_000_000_007
MX = 100_000

fac = [0] * MX
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD

inv_fac = [0] * MX
inv_fac[MX - 1] = pow(fac[MX - 1], -1, MOD)
for i in range(MX - 1, 0, -1):
    inv_fac[i - 1] = inv_fac[i] * i % MOD
''',
    call='Solution().numberOfSequence(10, [1, 4, 6])',
    expect=840,
    views=[
        dict(type='array', var=_cells, label='小朋友 0..n-1（粉 = 一开始就感冒）', color=_color, cell=84, h=190,
             pointers={'p': 'blue', 'q': 'green'}),
        dict(type='text', fn=_txt, size=30, h=90),
    ],
    watch=[('n', 'n'), ('a', 'a'), ('p', 'p', 'blue'), ('q', 'q', 'green'), ('k', 'k', 'orange'),
           ('e', 'e', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = fac': '先把所有没感冒的人排成一列：`(n-m)! = {n - len(a)}!`，再除以两头段内部的顺序 `{a[0]}!`、`{n - 1 - a[-1]}!`（两头只有一种传染方向，段内顺序固定）→ `ans = {ans}`',
        'e = 0': '`e` 记录最后要乘的 `2^e`，只记指数',
        'for p, q': '取相邻两个病人 `{p}`、`{q}`，它们之间就是一段空位',
        'k = q - p - 1': '这一段有 `k = {q} - {p} - 1 = {k}` 个没感冒的小朋友',
        'if k > 1': lambda S, B, r: (f'`k = {S.k} > 1`：段内 L/R 方向有 `2^(k-1)` 种，要累乘' if S.k > 1
                                     else f'`k = {S.k}`：只有 0 或 1 个人，方向只有 1 种，不用处理'),
        'e += k - 1': '这段有 `2^(k-1)` 种方向：指数加 `k-1 = {k - 1}` → `e = {e}`',
        'ans = ans * inv_fac': '这段内部的顺序不由我们决定，是多重集排列：除以 `k! = {k}!` → `ans = {ans}`',
        'return ans': '最后乘 `2^e = 2^{e}`，答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='先数每一段内部的方向，再把各段交错合并',
        complexity='时间 `O(m)`（预处理阶乘不计），空间 `O(1)`',
        problem=['`n` 个小朋友排成一排，`sick` 是一开始感冒的位置（升序）',
                 '每秒至多传染一个相邻的健康小朋友，求==所有不同的感冒顺序==数，模 `10^9+7`',
                 '示例：`n=5, sick=[0,4]` → `4`；本视频：`n=10, sick=[1,4,6]`'],
        quote='这 k 个小朋友中，如果是被左边的人传染的，记作 L；如果是被右边的人传染的，记作 R。……最后感冒的那个小朋友既可以记作 L，又可以记作 R，所以有 2^(k-1) 种方案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个病人之间的一段：每人是被左传染还是被右传染 → LR 序列，共 `2^(k-1)` 种',
              '两头的段只能朝一个方向传染，只有 1 种',
              '不同段之间任意交错：总长 `n-m` 的排列数 `(n-m)!`，再除以每段 `k_i!`（段内顺序已由 LR 决定）'],
        summary=['答案 = `2^e × (n-m)! / ∏ k_i!`，`e = Σ(k_i - 1)`',
                 '除法用阶乘的逆元 `inv_fac`，预处理放在 setup（视频里不追踪，MX = 100000）',
                 '只有 `k > 1` 的中间段才有指数；`k = 1` 时 `2^0 = 1`',
                 '灵神还给了方法一：逐段用组合数 `C(s,k)` 依次放入，结果相同'],
    ),
)
