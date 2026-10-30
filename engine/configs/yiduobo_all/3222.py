def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = S['x'], S['y']
    k = min(x, y // 4)
    cv.text((x0 + 18, y0 + 4), f'75 元硬币 {x} 枚，10 元硬币 {y} 枚', 24, T['muted'], bold=True)
    cw = min(40, (x1 - x0 - 60) / max(x, y))
    base = y0 + 70
    # 75 元：前 k 枚会被拿走
    cv.text((x0 + 20, base), '75 元', 24, T['orange'], anchor='lm', bold=True)
    for i in range(x):
        X = x0 + 120 + i * (cw + 6)
        used = i < k
        cv.rect((X, base - 18, X + cw, base + 18), fill=T['orange'] if used else (70, 76, 86), r=6)
    cv.text((x0 + 20, base + 80), '10 元', 24, T['cyan'], anchor='lm', bold=True)
    for j in range(y):
        X = x0 + 120 + j * (cw + 6)
        used = j < 4 * k
        cv.rect((X, base + 62, X + cw, base + 98), fill=T['cyan'] if used else (70, 76, 86), r=6)
    cv.text((x0 + 20, base + 160), '亮色 = 会被取走（每回合 1 枚 75 + 4 枚 10），灰色 = 剩下', 22, T['muted'])
    cv.text((x0 + 20, base + 220), f'一共能取 min({x}, {y} // 4) = min({x}, {y // 4}) = {k} 轮', 30, T['text'], bold=True)
    names = ['Alice' if r % 2 == 0 else 'Bob' for r in range(k)]
    cv.text((x0 + 20, base + 280), ('轮流取：' + ' → '.join(names)) if k else '第一轮 Alice 就取不了', 28, T['blue'], bold=True)


CONFIG = dict(
    num=3222, title='求出硬币游戏的赢家', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模拟 · 数轮次奇偶',
    code='''
class Solution(object):
    def losingPlayer(self, x, y):
        rnd = min(x, y // 4)
        if rnd % 2 == 1:
            return 'Alice'
        else:
            return 'Bob'
''',
    call='Solution().losingPlayer(5, 14)',
    expect='Alice',
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: f"`rnd` = {S['rnd']}，是==奇数==" if S.get('rnd', 0) % 2 and 'rnd' in S else (f"`rnd` = {S['rnd']}，是==偶数==" if 'rnd' in S else ''), size=32),
    ],
    watch=['x', 'y', ('rnd', "rnd if 'rnd' in dir() else ''", 'green')] if False else ['x', 'y', 'rnd'],
    captions={
        'rnd = min': '115 只能拆成 1 枚 75 + 4 枚 10，没有策略，照着取就行。能取的轮次：`min({x}, {y} // 4)` = `min({x}, {y // 4})` = =={rnd}==',
        'if rnd % 2': '`rnd % 2 == 1`（{rnd} % 2 = {rnd % 2}）→ {"成立：Alice 取了最后一轮" if rnd % 2 == 1 else "不成立：Bob 取了最后一轮"}',
        "return 'Alice'": '轮次是奇数：Alice 取最后一轮，==Bob 取不了，Alice 赢==',
        "return 'Bob'": '轮次是偶数：Bob 取最后一轮，==Alice 取不了，Bob 赢==',
    },
    cards=dict(
        one_liner='115 元只有一种取法，数轮次的奇偶就知道谁赢',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['有 `x` 枚 75 元和 `y` 枚 10 元硬币，Alice、Bob 轮流取，每次取出价值和为 115',
                 '某一方无法再取，对方就是赢家',
                 '本视频：`x = 5, y = 14` → `"Alice"`'],
        quote='注意到115元只能由一枚75元以及四枚10元组成，因此在这里并没有策略这一说，只需按部就班来取就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看 115 能怎么凑：只能是 `75 + 4×10`',
              '每轮固定用掉 1 枚 75 和 4 枚 10，谁先拿都一样',
              '75 元的有 `x` 枚，10 元的够 `y // 4` 轮，取小的就是总轮次 `rnd`',
              '轮次奇数：最后一轮是 Alice 取的，Alice 赢；偶数则 Bob 赢'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：10 元硬币要除以 4 再和 `x` 比大小',
                 '`rnd = 0` 时 Alice 第一轮就取不了 → 走 `else` 返回 `Bob`',
                 '对比灵神：他把 if/else 压成一行 `min(x, y // 4) % 2`，思路完全一致'],
    ),
)
