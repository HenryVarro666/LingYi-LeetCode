
PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, m, k = S.get('n'), S.get('m'), S.get('k')
    if n is None:
        return
    size = 2 * k + 1
    cv.text((x0 + 18, y0 + 4), f'{n}×{m} 网格，k={k}：每个传感器覆盖 {size}×{size} 的方块（同色 = 同一个传感器）', 24, T['muted'], bold=True)
    cell = min(80, (x1 - x0 - 60) / m, (y1 - y0 - 110) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * m) / 2
    sy = y0 + 60
    done = 'size' in S or 'x' in S
    for i in range(n):
        for j in range(m):
            b = (i // size) * (((m - 1) // size) + 1) + (j // size)
            col = T[PAL[b % len(PAL)]] if done else T['panel2']
            X, Y = sx + j * cell, sy + i * cell
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=col, alpha=150 if done else 255, r=5, outline=T['border'])
    if done:
        for bi in range((n - 1) // size + 1):
            for bj in range((m - 1) // size + 1):
                ci, cj = min(bi * size + k, n - 1), min(bj * size + k, m - 1)
                X, Y = sx + cj * cell + cell / 2, sy + ci * cell + cell / 2
                cv.rect((X - cell * 0.22, Y - cell * 0.22, X + cell * 0.22, Y + cell * 0.22), fill=T['text'], r=cell * 0.22)
                cv.text((X, Y), 'S', int(cell * 0.3), T['bg'], anchor='mm', bold=True)
        for bi in range(1, (n - 1) // size + 1):
            Y = sy + bi * size * cell
            cv.line([(sx, Y), (sx + m * cell, Y)], T['yellow'], 3)
        for bj in range(1, (m - 1) // size + 1):
            X = sx + bj * size * cell
            cv.line([(X, sy), (X, sy + n * cell)], T['yellow'], 3)


def _txt(S):
    if 'size' not in S:
        return ''
    n, m, size = S['n'], S['m'], S['size']
    return f'行方向 `ceil({n}/{size}) = {(n-1)//size+1}` 段，列方向 `ceil({m}/{size}) = {(m-1)//size+1}` 个，相乘 =={((n-1)//size+1)*((m-1)//size+1)}=='


CONFIG = dict(
    num=3648, title='覆盖网格的最少传感器数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='正方形分块 · 上取整转下取整',
    tags=['灵神题单', '数学算法', '难度分 1396'],
    code='''
class Solution:
    def minSensors(self, n: int, m: int, k: int) -> int:
        size = k * 2 + 1
        return ((n - 1) // size + 1) * ((m - 1) // size + 1)
''',
    call='[Solution().minSensors(*a) for a in ((5, 5, 1), (2, 2, 2), (4, 7, 1))]',
    expect=[4, 1, 6],
    views=[dict(type='custom', draw=_draw, h=470), dict(type='text', fn=_txt, size=28)],
    watch=[('n', 'n', 'blue'), ('m', 'm', 'pink'), ('k', 'k', 'yellow'), ('size', 'size', 'green')],
    captions={
        'size = k': '中心往左 `{k}` 步、往右 `{k}` 步，边长 `{k}+1+{k}` = =={size}==，问题变成用 `{size}×{size}` 的方块铺满 `{n}×{m}`',
        'return': '行方向 `({n}-1)//{size}+1 = {(n-1)//size+1}` 段，每段列方向 `({m}-1)//{size}+1 = {(m-1)//size+1}` 个，共 =={ret}==。上取整用下取整写，避免浮点',
    },
    cards=dict(
        one_liner='传感器覆盖的是正方形，转成用方块铺网格',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n×m` 网格，传感器覆盖切比雪夫距离 `≤ k` 的格子',
                 '求覆盖整个网格最少要几个传感器',
                 '示例 `(5,5,1)` → `4`；演示 `(5,5,1)`、`(2,2,2)`、`(4,7,1)`'],
        quote='覆盖范围是一个正方形。从正方形中心往左最多走 k 步，往右最多走 k 步，所以边长为 2k+1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['问题变成：用 `(2k+1)×(2k+1)` 的正方形盖住 `n×m`',
              '每 `2k+1` 行分一段，共 `ceil(n/(2k+1))` 段',
              '每段要 `ceil(m/(2k+1))` 个，两者相乘；上取整改写成 `(n-1)//size+1`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '方块比网格还大时公式给 1，符合实际',
                 '上取整 `ceil(a/b)` = `(a-1)//b+1`（a ≥ 1）',
                 '注意是 `2k+1`，不是 `2k`'],
    ),
)
