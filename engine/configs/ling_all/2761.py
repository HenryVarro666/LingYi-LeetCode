N = 20


def _isp(v):
    return v >= 2 and all(v % d for d in range(2, int(v ** 0.5) + 1))


def _line(S):
    return list(range(0, N + 1))


def _color(S, i, v):
    if 'ans' in S and any(i in p for p in S['ans']):
        return 'yellow'
    return 'green' if _isp(v) else None


def _txt(S):
    if 'x' not in S:
        return f'目标 `n = {N}`：用筛出的质数表枚举 `x`，`y = n − x`'
    x, y = S['x'], S['y'] if 'y' in S else N - S['x']
    ok = '都是质数' if _isp(x) and _isp(y) else '`y` 不是质数'
    return f'`x = {x}`，`y = {N} − {x} = {y}`：{ok}；已找到 =={len(S["ans"])}== 对'


CONFIG = dict(
    num=2761, title='和等于目标值的质数对', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='预处理质数表 · 枚举 x',
    tags=['灵神题单·数学算法', '难度分 1505'],
    code='''
MX = 10 ** 6 + 1
primes = []
is_prime = [True] * MX
for i in range(2, MX):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MX, i):
            is_prime[j] = False

class Solution:
    def findPrimePairs(self, n: int) -> List[List[int]]:
        if n % 2:
            return [[2, n - 2]] if n > 4 and is_prime[n - 2] else []
        ans = []
        for x in primes:
            y = n - x
            if y < x:
                break
            if is_prime[y]:
                ans.append([x, y])
        return ans
''',
    call=f'Solution().findPrimePairs({N})',
    expect=[[3, 17], [7, 13]],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var=_line, pointers={'x': 'blue', 'y': 'pink'}, color=_color, cell=60, h=300,
             label=f'数轴 0..{N}（绿 = 质数，蓝 = x，粉 = y = n − x，黄 = 已配对）'),
    ],
    watch=['n', ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'if n % 2': lambda S, B, r: (f'`n = {S.n}` 是偶数：奇偶都可以分，继续枚举' if S.n % 2 == 0
                                     else '`n` 是奇数：只有「奇数 + 偶数」才得奇数，偶质数只有 2，所以最多一对 `(2, n−2)`'),
        'ans = []': '`ans` 存放找到的质数对',
        'for x in primes': '`x` 取质数表里的下一个质数：`x = {x}`',
        'y = n - x': '另一个数必须是 `y = n − x = {n} − {x} = {y}`',
        'if y < x': lambda S, B, r: (f'`{S.y} < {S.x}`：`y` 已经比 `x` 小，==再往后全是重复==，直接 break' if S.y < S.x
                                     else f'`{S.y} >= {S.x}`：满足 `x <= y`，继续'),
        'if is_prime[y]': lambda S, B, r: (f'`is_prime[{S.y}]` 为真：`{S.y}` 也是质数' if _isp(S.y)
                                           else f'`is_prime[{S.y}]` 为假：`{S.y}` 不是质数，跳过'),
        'ans.append': '找到一对 `[{x}, {y}]`，加入答案：`ans = {ans}`',
        'break': '`x` 越来越大、`y` 越来越小，后面都不用看了',
        'return ans': '按 `x` 从小到大枚举，天然有序，返回 `{ans}`',
    },
    cards=dict(
        one_liner='先筛质数，再枚举 x，y = n − x 查表',
        complexity='时间 `O(n / log n)`，空间 `O(1)`（不计预处理）',
        problem=['找所有 `x <= y`、`x + y = n` 且 `x`、`y` 都是质数的 `[x, y]`',
                 '按 `x` 升序返回',
                 f'本视频：`n = {N}` → `[[3,17],[7,13]]`'],
        quote='然后就是暴力枚举质数 x 和 y=n-x 了，如果 x≤y 且 y 是质数，那么就把 [x,y] 加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['预处理 `10^6` 内的质数表 `primes` 和判质数表 `is_prime`（埃氏筛）',
              '只枚举质数 `x`，`y = n − x` 用 `is_prime` 一步查表',
              '奇数 `n` 的优化：偶质数只有 2，所以至多一对 `(2, n−2)`'],
        summary=['时间 `O(n / log n)`：`n` 以内约有 `n / log n` 个质数',
                 '`y < x` 就 break，保证 `x <= y`，`x = y` 的情况也被包含',
                 '易错：奇数 `n` 要 `n > 4` 才算，`n−2` 必须大于等于 2 且为质数',
                 '质数表在预处理里一次筛好，每次询问不用重筛'],
    ),
)
