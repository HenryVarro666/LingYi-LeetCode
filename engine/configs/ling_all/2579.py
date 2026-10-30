def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n', 1)
    R = max(n, 5)
    side = 2 * R - 1
    cell = min(60, (y1 - y0 - 90) / side, (x1 - x0 - 40) / side)
    cx, cy = (x0 + x1) / 2, y0 + 70 + cell * side / 2
    cv.text((x0 + 18, y0 + 4), f'第 {n} 分钟：蓝 = 之前染的，黄 = 这一分钟新增的 {4 * (n - 1) if n > 1 else 1} 格', 24, T['muted'], bold=True)
    for dy in range(-(R - 1), R):
        for dx in range(-(R - 1), R):
            d = abs(dx) + abs(dy)
            if d >= n:
                fill, ol = T['panel2'], T['border']
            elif d == n - 1:
                fill, ol = T['yellow'], None
            else:
                fill, ol = T['blue'], None
            X, Y = cx + dx * cell, cy + dy * cell
            cv.rect((X - cell / 2 + 2, Y - cell / 2 + 2, X + cell / 2 - 2, Y + cell / 2 - 2), fill=fill, outline=ol, r=6)


CONFIG = dict(
    num=2579, title='统计染色格子数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='找规律 · 求和公式',
    tags=['灵神题单', '数学算法', '难度分 1356'],
    code='''
class Solution:
    def coloredCells(self, n: int) -> int:
        return 1 + 2 * n * (n - 1)
''',
    call='[Solution().coloredCells(i) for i in (1, 2, 3, 4, 5)]',
    expect=[1, 5, 13, 25, 41],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: f"`f({S['n']}) = f({S['n']-1}) + 4×{S['n']-1}`，直接化简：`1 + 2×{S['n']}×{S['n']-1}` = =={1 + 2*S['n']*(S['n']-1)}==" if 'n' in S and S['n'] > 1 else ('第 1 分钟只有 1 格：`1 + 2×1×0` = ==1==' if 'n' in S else '')),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return 1 + 2': '`n = {n}`：`1 + 2×{n}×{n-1}` = =={ret}==。新增 `4×{n-1}` 格，累加起来就是 `1 + 4(1+2+...+{n-1})`',
    },
    cards=dict(
        after=[dict(heading='为什么是 4(n−1)', lines=['菱形的四条边，每条边（不含端点）各新增 `n-1` 个格子', '四个方向共 `4(n-1)`，所以第 n 圈比上一圈多这么多', '`n=3` 时：`5 + 4×2 = 13`；`n=4` 时：`13 + 4×3 = 25`'])],
        one_liner='每分钟多出 4 组 n−1 个格子，求和得 1 + 2n(n−1)',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['无穷网格，第 1 分钟染 1 格，之后每分钟把蓝格四周所有未染格染蓝',
                 '求 `n` 分钟后被染色的格子总数',
                 '示例：`n = 2` → `5`；演示 `n = 1..5` → `1, 5, 13, 25, 41`'],
        quote='`f(n)` 相当于在 `f(n-1)` 的基础上多了 4 组 `n-1` 的格子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['图形是菱形，第 n 圈比上一圈多 `4(n-1)` 个格子',
              '递推 `f(n) = f(n-1) + 4(n-1)`，`f(1) = 1`',
              '展开 `1 + 4(1+2+...+n-1)`，等差数列求和得 `1 + 2n(n-1)`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`n = 1` 时公式给 `1`，不用特判',
                 '`n` 到 `10^5`，Python 整数不会溢出',
                 '同类：找规律后用等差数列求和直接出公式'],
    ),
)
