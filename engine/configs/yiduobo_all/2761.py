N = 14


def _isp(v):
    return v >= 2 and all(v % d for d in range(2, int(v ** 0.5) + 1))


def _line(S):
    return list(range(0, N + 1))


def _color(S, i, v):
    f = S.get('f')
    if f is None or 'res' not in S:
        return None
    if any(i in p for p in S['res']):
        return 'yellow'
    return 'green' if f[i] else None


def _dim(S, i, v):
    f = S.get('f')
    return f is not None and i < len(f) and not f[i] and 'res' not in S


def _txt(S):
    if 'f' not in S:
        return f'目标 `n = {N}`'
    if 'res' not in S:
        return '第一步：筛法，每个质数 `p` 的倍数都划掉（灰 = 已标合数）'
    return f'质数表建好（绿）；已找到 =={len(S["res"])}== 对：`{S["res"]}`'


CONFIG = dict(
    num=2761, title='和等于目标值的质数对', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛法 + 枚举 x（单独处理 x = y）',
    tags=['灵神题单·数学算法', '难度分 1505'],
    code='''
class Solution(object):
    def findPrimePairs(self, n):

        f = [True] * (n + 1)
        f[0] = f[1] = False
        p = 2
        while p * p <= n:
            if f[p]:
                for x in range(p + p, n + 1, p):
                    f[x] = False
            
            p += 1
        
        res = []
        for x in range(2, (n + 1) // 2):
            y = n - x
            if f[x] and f[y]:
                res.append([x, y])
        
        if n % 2 == 0 and f[n // 2]:
            res.append([n // 2, n // 2])
        return res
''',
    call=f'Solution().findPrimePairs({N})',
    expect=[[3, 11], [7, 7]],
    max_steps=90,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var=_line, pointers={'x': 'blue', 'y': 'pink'}, color=_color, dim=_dim, cell=60, h=300,
             label=f'数轴 0..{N}（灰 = 合数；筛完后绿 = 质数；蓝 = x，粉 = y）'),
    ],
    watch=['n', ('p', 'p', 'orange'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = [True]': '`f[i]` 表示 `i` 是否为质数，先假设 0..{n} 全是',
        'f[0] = f[1]': '`0` 和 `1` 不是质数',
        'p = 2': '从 `p = 2` 开始筛',
        'while p * p <= n': '只需筛到 `p * p <= n`：`{p}×{p} = {p*p}` 与 `{n}` 比较',
        'if f[p]': lambda S, B, r: (f'`f[{S.p}]` 为真：`{S.p}` 是质数，把它的倍数划掉' if S.f[S.p]
                                    else f'`f[{S.p}]` 为假：`{S.p}` 已是合数，它的倍数早被更小的质数划过'),
        'for x in range(p + p': lambda S, B, r: ('`' + str(S.p) + '` 的倍数划完了' if 'x' in B and B.x == S.x
                                                else f'划掉 `{S.p}` 的倍数 `{S.p*2}, {S.p*3}, ...`：`x = {S.x}`'),
        'f[x] = False': '`{x}` 是 `{p}` 的倍数 → 合数',
        'p += 1': '`p` → {p}',
        'res = []': '筛完了。接下来枚举 `x`，`y = n − x`，`res` 存答案',
        'for x in range(2': lambda S, B, r: ('`x` 枚举完了（到 `(n+1)//2` 之前）' if 'y' in B and B.x == S.x
                                             else f'枚举 `x = {S.x}`：只到 `(n+1)//2` 之前，保证 `x < y`'),
        'y = n - x': '`y = n − x = {n} − {x} = {y}`',
        'if f[x] and f[y]': lambda S, B, r: (f'`f[{S.x}]`、`f[{S.y}]` 都为真 → 是质数对' if S.f[S.x] and S.f[S.y]
                                             else f'`x = {S.x}`、`y = {S.y}` 至少有一个不是质数，跳过'),
        'res.append([x, y])': '找到 `[{x}, {y}]`：`res = {res}`',
        'if n % 2 == 0': lambda S, B, r: (f'`n = {S.n}` 是偶数，且 `f[{S.n//2}]` 为{"真" if S.f[S.n//2] else "假"}：'
                                          + ('`x = y = ' + str(S.n // 2) + '` 也可以' if S.f[S.n // 2] else '`n/2` 不是质数，没有 `x = y`')),
        'res.append([n': '`x = y = {n // 2}`：这一对单独补上，不重不漏 → `{res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='筛法标出质数，枚举 x < y，再单独补 x = y',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['找 `x <= y`、`x + y = n`，且 `x`、`y` 都是质数的 `[x, y]`，按 `x` 升序',
                 '示例：`n = 10` → `[[3,7],[5,5]]`',
                 f'本视频：`n = {N}` → `[[3,11],[7,7]]`'],
        quote='另外需要注意x和y相等的情况，需要特殊处理保证不重不漏。',
        quote_src='—— yiduobo 题解原文',
        idea=['暴力对每个 `x` 试除是 `O(n√n)`，太慢；先用筛法把 `1..n` 的质数一次标好',
              '遍历 `p`，质数的倍数全部标成合数；次数小于 `n(1/1 + 1/2 + ... )`，约 `O(n log n)`',
              '枚举 `x` 到 `(n+1)//2` 之前（`x < y`），最后单独判 `n/2`'],
        summary=['原文为 Python 2 写法，`(n + 1) / 2` 和 `n / 2` 的整数除法已改为 `//`',
                 '`x = y` 只可能是 `n/2`：偶数 `n` 才有，且 `n/2` 必须是质数',
                 '易错：range 右端是开区间，`(n+1)//2` 刚好不含 `x = y`',
                 '对比灵神：灵神只枚举质数表并用 `y < x` 提前 break，这里是枚举全部 `x`'],
    ),
)
