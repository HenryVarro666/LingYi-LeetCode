CONFIG = dict(
    num=1954, title='收集足够苹果的最小花园周长', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='数学公式 + 开立方', tags=['难度分 1759'],
    setup='''
def cbrt(x):
    r = x ** (1 / 3)
    k = round(r)
    return float(k) if abs(r - k) < 1e-9 else r
''',
    code='''
class Solution:
    def minimumPerimeter(self, neededApples: int) -> int:
        n = int(cbrt(neededApples / 4))
        if 2 * n * (n + 1) * (2 * n + 1) < neededApples:
            n += 1
        return 8 * n
''',
    call='Solution().minimumPerimeter(13)',
    expect=16,
    views=[
        dict(type='text', size=34, fn=lambda S: f"边长 `2n`，周长 `8n`：苹果数 = `2n(n+1)(2n+1)`"),
        dict(type='text', size=36, fn=lambda S: (f"`n = {S['n']}`：`2×{S['n']}×{S['n']+1}×{2*S['n']+1}` = =={2*S['n']*(S['n']+1)*(2*S['n']+1)}== ，需要 `{S['neededApples']}`" if 'n' in S else f"`neededApples = {S['neededApples']}`")),
        dict(type='array', var=lambda S: [2*k*(k+1)*(2*k+1) for k in range(0, 5)], h=240, label='n = 0..4 时正方形里的苹果数',
             pointers={'n': 'blue'}, cell=130,
             color=lambda S, i, v: ('green' if v >= S['neededApples'] else None)),
    ],
    watch=[('neededApples', 'neededApples', 'blue'), 'n'],
    captions={
        'n = int(cbrt': '`n(n+1)(n+1/2) ≥ 需求/4`，先取 `n = floor(cbrt({neededApples}/4))` = =={n}==',
        'if 2 * n': '`2n(n+1)(2n+1) = {2*n*(n+1)*(2*n+1)}`，和 `{neededApples}` 比：=={"不够，n 要加一" if 2*n*(n+1)*(2*n+1) < neededApples else "够了，n 就是答案"}==',
        'n += 1': '`n` 往下取整偏小：m 不满足，但 m+1 必满足 → `n = {n}`',
        'return 8 * n': '周长 `8 × {n} = {ret}`',
    },
    cards=dict(
        after=[dict(heading='为什么 m+1 一定够', lines=['`(m+1)(m+2)(m+3/2) > (m+1)^3 > 需求/4`', '所以 m+1 必满足要求，答案只可能是 m 或 m+1', '`m−1` 同理必不满足：`(m−1)m(m−1/2) < m^3 ≤ 需求/4`', '于是一次开立方 + 一次比较就够了'])],
        one_liner='周长 8n，苹果数 2n(n+1)(2n+1)，开立方直接定位',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['坐标 `(i, j)` 处的树有 `|i| + |j|` 个苹果',
                 '买下以原点为中心的正方形，求至少 `neededApples` 个苹果的最小周长',
                 '示例：`13` → `16`'],
        quote='设正方形的周长为 8n，则其边长为 2n。问题相当于求最小的 n，满足 2n(n+1)(2n+1) ≥ neededApples。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不等式变形为 `n(n+1)(n+1/2) ≥ 需求/4`，近似 `n^3`',
              '设 `m = floor(cbrt(需求/4))`：m−1 必不满足，m+1 必满足',
              '所以只要检查 m：不满足就加一'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文用 `math.cbrt`（Python 3.11+）；本视频在 setup 里补了等价实现',
                 '易错：周长是 `8n`，不是 `2n`；`n` 只可能是 m 或 m+1',
                 '相似题：1739 放置盒子'],
    ),
)
