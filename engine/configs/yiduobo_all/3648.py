
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
    if 'x' not in S:
        return ''
    n, m, x, k = S['n'], S['m'], S['x'], S['k']
    return f'左上角放 `({k},{k})`；每行 `({m}-1)//{x}+1 = {(m-1)//x+1}` 个，共 `({n}-1)//{x}+1 = {(n-1)//x+1}` 排 → =={((n-1)//x+1)*((m-1)//x+1)}=='


CONFIG = dict(
    num=3648, title='覆盖网格的最少传感器数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='左上角贪心 · 逐行排布',
    tags=['灵神题单', '数学算法', '难度分 1396'],
    code='''
class Solution(object):
    def minSensors(self, n, m, k):
        
        x = k * 2 + 1
        return ((n - 1) // x + 1) * ((m - 1) // x + 1)
''',
    call='[Solution().minSensors(*a) for a in ((5, 5, 1), (2, 2, 2), (4, 7, 1))]',
    expect=[4, 1, 6],
    views=[dict(type='custom', draw=_draw, h=470), dict(type='text', fn=_txt, size=28)],
    watch=[('n', 'n', 'blue'), ('m', 'm', 'pink'), ('k', 'k', 'yellow'), ('x', 'x', 'green')],
    captions={
        'x = k': '传感器 = 以它为中心、边长 `{k}×2+1` = =={x}== 的正方形，记作 `x`',
        'return': '每一行放 `({m}-1)//{x}+1 = {(m-1)//x+1}` 个，要排 `({n}-1)//{x}+1 = {(n-1)//x+1}` 行 → =={ret}==',
    },
    cards=dict(
        one_liner='左上角放 (k,k)，然后一格 x 一格 x 往外排',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n*m` 的网格，传感器覆盖与它切比雪夫距离 `≤ k` 的格子',
                 '问最少需要多少个传感器才能覆盖整个网格',
                 '本视频演示 `(5,5,1)`、`(2,2,2)`、`(4,7,1)`'],
        quote='对于网格的左上角，最优的覆盖方式显然是在(k, k)处放置一个传感器，这样一来在覆盖了(0, 0)的同时，对于其他位置的覆盖程度也最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['切比雪夫距离让覆盖区变成边长 `x = 2k+1` 的正方形',
              '左上角放 `(k,k)`，下一个放 `(k, x+k)`，一行行排下去',
              '每行 `(m-1)//x+1` 个，共 `(n-1)//x+1` 行，相乘'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`(a-1)//x+1` 就是 a 除以 x 向上取整',
                 '对比灵神：灵神先说覆盖范围再分段，这里从左上角贪心推出排布',
                 '原文代码无 Python 2 专有写法（`//` 已是整除），未做修改'],
    ),
)
