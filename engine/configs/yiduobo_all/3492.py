def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, w, mw = S['n'], S['w'], S['maxWeight']
    res = S.get('res')
    cv.text((x0 + 18, y0 + 4), f'{n}×{n} 甲板（{n * n} 格）；箱重 {w}，限重 {mw}', 24, T['muted'], bold=True)
    cell = min(90, (y1 - y0 - 140) / n, (x1 - x0 - 60) / n)
    X0 = x0 + (x1 - x0 - cell * n) / 2
    Y0 = y0 + 60
    for k in range(n * n):
        r, c = divmod(k, n)
        full = res is not None and k < min(res, n * n)
        cv.rect((X0 + c * cell + 3, Y0 + r * cell + 3, X0 + (c + 1) * cell - 3, Y0 + (r + 1) * cell - 3),
                fill=T['green'] if full else (36, 42, 52), r=8)
        if full:
            cv.text((X0 + c * cell + cell / 2, Y0 + r * cell + cell / 2), w, 26, T['bg'], anchor='mm', bold=True)
    if res is not None:
        cv.text((x0 + (x1 - x0) / 2, Y0 + n * cell + 20), f'res = {res}（装满的格子数）', 24, T['text'], anchor='mt', bold=True)


CONFIG = dict(
    num=3492, title='船上可以装载的最大集装箱数量', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模拟 · 重量上限与空间上限取小',
    code='''
class Solution(object):
    def maxContainers(self, n, w, maxWeight):
        
        res = maxWeight // w
        if res > n * n:
            res = n * n
        return res
''',
    call='Solution().maxContainers(3, 5, 20)',
    expect=4,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=['n', 'w', 'maxWeight', ('res', 'res', 'green')],
    captions={
        'res = maxWeight // w': '只看重量：`{maxWeight} // {w}` = =={res}== 个箱子',
        'if res > n * n': lambda S, B, r: (f'`res = {S.res} > n × n = {S.n * S.n}` → 放不下这么多，得砍到格子数' if S.res > S.n * S.n
                                           else f'`res = {S.res} ≤ n × n = {S.n * S.n}` → 格子够用，不用改'),
        'res = n * n': '受空间限制，最多 `n × n` = =={res}== 个',
        'return res': '最终答案 =={res}==',
    },
    cards=dict(
        one_liner='重量和空间各有上限，取较小的那个',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n × n` 的甲板，每格最多放一个重 `w` 的箱子',
                 '总重不能超过 `maxWeight`',
                 '示例：`n=3, w=5, maxWeight=20` → `4`'],
        quote='受空间限制，船上集装箱的数量不超过n * n。另一方面，受重量限制，船上集装箱的数量不超过maxWeight // w。取二者的较小值即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算重量允许的数量 `maxWeight // w`',
              '若超过格子数 `n × n`，就砍到 `n × n`',
              '等价于取两者的较小值'],
        before=[dict(heading='两个限制', lines=['空间限制：箱子数不超过 `n * n`', '重量限制：箱子数不超过 `maxWeight // w`', '两者的较小值就是答案'])],
        after=[dict(heading='再看示例 1', lines=['`n=2, w=3, maxWeight=15`：`res = 15 // 3 = 5`', '`5 > n * n = 4` → 砍到 `4`', '这次是空间先卡住；示例 2 是重量先卡住'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：用整除 `//`，向下取整',
                 '原文已是 `//`，无需修改',
                 '对比灵神：灵神一行 `min(...)`；yiduobo 用 `if` 写成两步'],
    ),
)
