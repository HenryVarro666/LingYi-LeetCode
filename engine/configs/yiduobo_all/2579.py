def _terms(S):
    n = S.get('n')
    if n is None:
        return ''
    t = ' + '.join(f'4×{i}' for i in range(1, n))
    return f'`1{" + " + t if t else ""}` = `1 + 4×{n*(n-1)//2}` = =={1 + 2*n*(n-1)}=='


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n', 1)
    cv.text((x0 + 18, y0 + 4), '每一轮新增的格子数（柱高 = 4×(轮数−1)）', 24, T['muted'], bold=True)
    N = 5
    cell = min(130, (x1 - x0 - 60) / N)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * N) / 2
    base, top = y1 - 70, y0 + 70
    unit = (base - top) / 16
    for r in range(1, N + 1):
        add = 1 if r == 1 else 4 * (r - 1)
        X = sx + (r - 1) * cell
        on = r <= n
        fill = (T['yellow'] if r == n else T['blue']) if on else T['panel2']
        cv.rect((X + 12, base - add * unit, X + cell - 12, base), fill=fill, r=6, outline=None if on else T['border'])
        cv.text((X + cell / 2, base - add * unit - 4), add if on else '?', 28, T['text'] if on else T['dim'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 8), f'第{r}轮', 22, T['dim'], anchor='mt')
    cv.line([(sx, base), (sx + cell * N, base)], T['border'], 2)


CONFIG = dict(
    num=2579, title='统计染色格子数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='找规律 · 套求和公式',
    tags=['灵神题单', '数学算法', '难度分 1356'],
    code='''
class Solution(object):
    def coloredCells(self, n):

        return n * (n - 1) * 2 + 1
''',
    call='[Solution().coloredCells(i) for i in (1, 2, 3, 4, 5)]',
    expect=[1, 5, 13, 25, 41],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_terms, size=30),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return n': '`n = {n}`：`{n} × {n-1} × 2 + 1` = =={ret}==，等价于 1 加上前面各轮的 `4×k`',
    },
    cards=dict(
        one_liner='第 n 轮比上一轮多 4×(n−1) 个，直接套求和公式',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['无穷网格第 1 分钟染 1 格，之后每分钟染蓝格周围所有未染格',
                 '问 `n` 分钟后一共多少格被染色',
                 '示例 `n = 2` → `5`；本视频演示 `n = 1..5`'],
        quote='分析样例可以发现，第n轮相当于在第n - 1的轮的基础上额外添加了4 * (n - 1)个格子',
        quote_src='—— yiduobo 题解原文',
        idea=['这是一道==找规律==的题：先看样例 1、5、13 的差',
              '差值 4、8 恰好是 `4×1`、`4×2`，所以每轮加 `4×(n-1)`',
              '总数 = `1 + 4×1 + 4×2 + ... + 4×(n-1)`，求和即得公式'],
        after=[dict(heading='求和怎么化简', lines=['`4×(1+2+...+(n-1))` = `4 × n(n-1)/2` = `2n(n-1)`', '再加上第 1 分钟的 1 格：`2(n-1)n + 1`', '`n=4`：`2×3×4 + 1 = 25`，和逐轮累加一致'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`n = 1` 时 `1×0×2 + 1 = 1`，不用特判',
                 '找规律题：先写出前几项的差，再套等差数列求和',
                 '原文代码无 Python 2 专有写法，未做修改'],
    ),
)
