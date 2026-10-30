def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = S['x'], S['y']
    k = min(x, y // 4)
    cv.text((x0 + 18, y0 + 4), f'每一回合拿 1 枚 75 + 4 枚 10（共 115）。x = {x}，y = {y}', 24, T['muted'], bold=True)
    rows = k + 1
    rh = min(78, (y1 - y0 - 150) / max(rows, 1))
    cw = 56
    for r in range(rows):
        Y = y0 + 60 + r * rh
        who = 'Alice' if r % 2 == 0 else 'Bob'
        col = T['blue'] if who == 'Alice' else T['pink']
        if r < k:
            cv.text((x0 + 24, Y + rh / 2 - 6), f'第 {r + 1} 回合 {who}', 24, col, anchor='lm', bold=True)
            cv.rect((x0 + 250, Y, x0 + 250 + cw, Y + rh - 12), fill=T['orange'], r=8)
            cv.text((x0 + 250 + cw / 2, Y + rh / 2 - 6), '75', 24, T['bg'], anchor='mm', bold=True)
            for j in range(4):
                X = x0 + 250 + (j + 1) * (cw + 8) + 10
                cv.rect((X, Y, X + cw, Y + rh - 12), fill=T['cyan'], r=8)
                cv.text((X + cw / 2, Y + rh / 2 - 6), '10', 24, T['bg'], anchor='mm', bold=True)
        else:
            cv.text((x0 + 24, Y + rh / 2 - 6), f'第 {r + 1} 回合 {who}：拿不出 115 → {who} 输', 24, T['red'], anchor='lm', bold=True)
    cv.text((x0 + 24, y1 - 50), f'能玩 k = min(x, y // 4) = min({x}, {y // 4}) = {k} 回合', 28, T['text'], bold=True)
    cv.text((x0 + 24, y1 - 14), f'k = {k} 是{"奇" if k % 2 else "偶"}数 → 最后一个拿的是 {"Alice" if k % 2 else "Bob"}，他赢', 28, T['green'], bold=True)


CONFIG = dict(
    num=3222, title='求出硬币游戏的赢家', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='二元一次不定方程 · 奇偶判断',
    code='''
class Solution:
    def losingPlayer(self, x: int, y: int) -> str:
        return "Alice" if min(x, y // 4) % 2 else "Bob"
''',
    call='Solution().losingPlayer(5, 14)',
    expect='Alice',
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['x', 'y', ('回合数', 'min(x, y // 4)', 'green')],
    captions={
        'return "Alice"': '115 只能是 `75×1 + 10×4`，没有别的拿法 → 回合数 `min({x}, {y} // 4)` = `min({x}, {y // 4})` = =={min(x, y // 4)}== → ==奇数 Alice 赢，偶数 Bob 赢==，所以返回 `{ret}`',
    },
    cards=dict(
        one_liner='115 只有一种拿法，数一数能玩几回合，看奇偶',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两堆硬币：`x` 枚 75，`y` 枚 10；Alice 先手，每次拿走总价值恰为 115',
                 '拿不出来的人输；示例 `x = 2, y = 7` → `"Alice"`',
                 '本视频：`x = 5, y = 14` → `"Alice"`'],
        quote='面额为 75 的硬币要恰好选 1 个。……面额为 10 的硬币要恰好选 4 个。本质上来说，我们在求解二元一次不定方程 75a+10b=115，它有唯一正整数解 a=1,b=4。',
        quote_src='—— 灵茶山艾府题解',
        idea=['10 的倍数凑不出 115，所以必须带 75；而 `75×2 = 150 > 115`，75 只能拿 1 枚',
              '剩下 `115 − 75 = 40`，只能是 4 枚 10',
              '每回合固定消耗 `(1, 4)`，没有策略可言：回合数 `k = min(x, y // 4)`',
              '`k` 奇数 → Alice 拿了最后一次；偶数 → Bob 拿了最后一次'],
        after=[dict(heading='手算 x = 5, y = 14', lines=['`y // 4 = 3`，`min(5, 3) = 3` 回合', 'Alice、Bob、Alice 各拿一次，轮到 Bob 时只剩 `y = 2`', 'Bob 拿不出 → ==Alice 赢==，`3 % 2 = 1`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：别忘了 `y // 4`（每回合要 4 枚 10），不是 `y`',
                 '回合数为 0 时 Alice 先输 → `0 % 2 = 0` → `"Bob"`，也被覆盖',
                 '函数名叫 `losingPlayer`，但题目要的是赢家'],
    ),
)
