def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, w, mw = S['n'], S['w'], S['maxWeight']
    cnt = min(mw // w, n * n)
    cv.text((x0 + 18, y0 + 4), f'{n}×{n} 甲板：共 {n * n} 格；每个箱子重 {w}，总重不超过 {mw}', 24, T['muted'], bold=True)
    cell = min(90, (y1 - y0 - 140) / n, (x1 - x0 - 60) / n)
    X0 = x0 + (x1 - x0 - cell * n) / 2
    Y0 = y0 + 60
    for k in range(n * n):
        r, c = divmod(k, n)
        full = k < cnt
        cv.rect((X0 + c * cell + 3, Y0 + r * cell + 3, X0 + (c + 1) * cell - 3, Y0 + (r + 1) * cell - 3),
                fill=T['green'] if full else (36, 42, 52), r=8)
        if full:
            cv.text((X0 + c * cell + cell / 2, Y0 + r * cell + cell / 2), w, 26, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + (x1 - x0) / 2, Y0 + n * cell + 20),
            f'重量限制：{mw} ÷ {w} 取整 = {mw // w} 个；空间限制：{n * n} 个 → 取较小的 {cnt}', 24, T['text'], anchor='mt', bold=True)


CONFIG = dict(
    num=3492, title='船上可以装载的最大集装箱数量', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='数学 · 两个上界取小',
    code='''
class Solution:
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
        return min(maxWeight // w, n * n)
''',
    call='Solution().maxContainers(3, 5, 20)',
    expect=4,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=['n', 'w', 'maxWeight', ('maxWeight // w', 'maxWeight // w', 'orange'), ('n * n', 'n * n', 'cyan')],
    captions={
        'return min': '重量上限 `w · x ≤ maxWeight` → `x ≤ {maxWeight} // {w} = {maxWeight // w}`；格子上限 `n² = {n * n}`；两个都要满足，取小：==`{ret}`==',
    },
    cards=dict(
        one_liner='解不等式 w·x ≤ maxWeight，再和 n² 取较小值',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n × n` 的甲板，每格放一个重 `w` 的集装箱',
                 '所有箱子总重不能超过 `maxWeight`',
                 '示例：`n=3, w=5, maxWeight=20` → `4`'],
        quote='每个单元格装 w 重量，设装了 x 个单元格，那么有 w·x ≤ maxWeight，解得 x 最大为 floor(maxWeight / w)。上式不能超过 n²，所以答案为 min(floor(maxWeight / w), n²)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['装 `x` 个箱子：总重 `w·x`，必须 `≤ maxWeight`',
              '解出 `x ≤ maxWeight // w`',
              '同时 `x` 不能超过格子数 `n²`，两个上界取小'],
        before=[dict(heading='两个限制', lines=['重量限制：`w · x ≤ maxWeight`', '空间限制：`x ≤ n²`', '答案要同时满足两个，所以取较小者'])],
        after=[dict(heading='再看示例 1', lines=['`n=2, w=3, maxWeight=15`：`15 // 3 = 5`，`n² = 4`', '取小得 `4`：这次是==空间==先卡住', '示例 2 则是==重量==先卡住'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：重量用整除 `//`，向下取整',
                 '示例：`20 // 5 = 4`，`3 × 3 = 9`，取 4'],
    ),
)
