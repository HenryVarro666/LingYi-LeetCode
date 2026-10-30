PILES = ([5, 3, 4, 5], [3, 7, 2, 3], [2, 9, 4, 1, 6, 5])


def _play(p):
    """Alice 用奇偶策略，Bob 贪心拿较大的一端；返回每一手 (谁, 下标)"""
    n = len(p)
    ev, od = sum(p[0::2]), sum(p[1::2])
    l, r = 0, n - 1
    moves = []
    if ev > od:
        moves.append(('A', l)); l += 1
    else:
        moves.append(('A', r)); r -= 1
    while l <= r:
        if p[l] >= p[r]:
            moves.append(('B', l)); l += 1
            if l <= r:
                moves.append(('A', l)); l += 1
        else:
            moves.append(('B', r)); r -= 1
            if l <= r:
                moves.append(('A', r)); r -= 1
    return moves


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S.get('piles')
    if p is None:
        return
    n = len(p)
    ev, od = sum(p[0::2]), sum(p[1::2])
    cv.text((x0 + 18, y0 + 4), 'piles（蓝 = 偶数下标，粉 = 奇数下标）', 22, T['muted'], bold=True)
    c = 96
    sx = x0 + (x1 - x0 - n * c) / 2
    Y = y0 + 48
    for i, v in enumerate(p):
        X = sx + i * c
        col = T['blue'] if i % 2 == 0 else T['pink']
        cv.rect((X + 4, Y, X + c - 4, Y + 76), fill=col, r=10)
        cv.text((X + c / 2, Y + 38), v, 32, T['bg'], anchor='mm', bold=True)
        cv.text((X + c / 2, Y + 82), i, 18, T['dim'], anchor='mt', mono=True)
    Y += 124
    big_even = ev > od
    cv.rich(x0 + 40, Y, f'偶数下标之和 `S_even = {" + ".join(map(str, p[0::2]))} = {ev}`', x1 - x0 - 80, size=24,
            color=T['blue'] if big_even else T['muted'])
    cv.rich(x0 + 40, Y + 44, f'奇数下标之和 `S_odd = {" + ".join(map(str, p[1::2]))} = {od}`', x1 - x0 - 80, size=24,
            color=T['pink'] if not big_even else T['muted'])
    first = f'`S_even > S_odd` → Alice 第一手拿 ==piles[0]==，之后 Bob 只能拿奇数下标' if big_even else \
        f'`S_even < S_odd` → Alice 第一手拿 ==piles[{n - 1}]==，之后 Bob 只能拿偶数下标'
    cv.rich(x0 + 40, Y + 96, first, x1 - x0 - 80, size=24, color=T['text'], accent=T['orange'])
    # 模拟一局：Bob 贪心，Alice 跟着 Bob 拿同一端
    Y += 150
    cv.text((x0 + 40, Y), '模拟一局（Bob 拿哪一端，Alice 就跟着拿哪一端）：', 22, T['muted'], bold=True)
    X = x0 + 40
    Y += 40
    sa = sb = 0
    for who, i in _play(p):
        txt = f'{"A" if who == "A" else "B"}:{p[i]}'
        w = cv.tlen(txt, 24, True, True) + 24
        col = T['blue'] if i % 2 == 0 else T['pink']
        cv.rect((X, Y, X + w, Y + 44), fill=col if who == 'A' else T['panel2'], r=8,
                outline=col, width=3)
        cv.text((X + w / 2, Y + 22), txt, 24, T['bg'] if who == 'A' else T['text'], anchor='mm', bold=True, mono=True)
        X += w + 10
        if who == 'A':
            sa += p[i]
        else:
            sb += p[i]
    cv.rich(X + 16, Y + 6, f'Alice 共 =={sa}==，Bob 共 `{sb}`', x1 - X - 30, size=24, color=T['text'], accent=T['green'])
    cur = next(k for k, q in enumerate(PILES) if list(q) == list(p))
    Y3 = y1 - 56
    X = x0 + 40
    for k, q in enumerate(PILES):
        txt = f'{list(q)} → ' + ('true' if k <= cur else '?')
        w = cv.tlen(txt, 22, True, True) + 28
        cv.rect((X, Y3, X + w, Y3 + 44), fill=T['blue'] if k == cur else T['panel2'], r=10, outline=T['border'])
        cv.text((X + w / 2, Y3 + 22), txt, 22, T['bg'] if k == cur else (T['text'] if k < cur else T['dim']),
                anchor='mm', bold=True, mono=True)
        X += w + 14


CONFIG = dict(
    num=877, title='石子游戏', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='奇偶下标分组 · 先手必胜',
    tags=['labuladong', '灵神题单·动态规划', '难度分 1590'],
    code='''
class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        return True
''',
    call=f'[Solution().stoneGame(p) for p in {[list(p) for p in PILES]}]',
    expect=[True, True, True],
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('n', lambda S: len(S['piles']) if 'piles' in S else None),
           ('S_even', lambda S: sum(S['piles'][0::2]) if 'piles' in S else None, 'blue'),
           ('S_odd', lambda S: sum(S['piles'][1::2]) if 'piles' in S else None, 'pink')],
    captions={
        'return True': lambda S, B, r: (
            f'`piles = {S.piles}`：`S_even = {sum(S.piles[0::2])}`，`S_odd = {sum(S.piles[1::2])}`，'
            f'Alice 选和更大的那组下标全拿走 → =={r}=='),
    },
    cards=dict(
        one_liner='n 是偶数：Alice 能保证拿走全部偶数下标，或全部奇数下标',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['==偶数==堆石子排成一行，Alice 和 Bob 轮流从==两端==取走一整堆，Alice 先手',
                 '石子总数是奇数（没有平局），双方都最优，Alice 赢返回 `true`',
                 '示例：`[5,3,4,5]` → `true`；`[3,7,2,3]` → `true`'],
        quote='这一策略可以保证 ==Alice 总是取走偶数下标的石子堆==，而 Bob 总是只能取走奇数下标的石子堆。最终 Alice 先手必胜。',
        quote_src='—— 灵茶山艾府题解',
        idea=['下标 0 是偶数、`n − 1` 是奇数：Alice 拿走一端后，剩下两端==奇偶相同==',
              'Bob 只能拿另一种奇偶的堆；Bob 拿哪端，Alice 就跟着拿哪端',
              '`S_even ≠ S_odd`（总数是奇数）→ Alice 选大的那组，必胜'],
        summary=['时间 `O(1)`，空间 `O(1)`：直接 `return True`',
                 '前提是 `n` 为偶数；`n` 不保证偶数时就是 486. 预测赢家，要用区间 DP',
                 '本视频模拟时 Bob 用贪心，但无论 Bob 怎么拿，Alice 的奇偶策略都成立',
                 '同类：灵神数学题单「博弈论」'],
    ),
)
