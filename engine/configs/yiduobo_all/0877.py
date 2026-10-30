PILES = ([5, 3, 4, 5], [3, 7, 2, 3], [1, 4, 2, 3, 5, 8])

# 4 堆时 yiduobo 枚举的 4 种情况：(先手第一手, 后手应对, 剩下两堆)
CASES = [('1-1', 0, 1, (2, 3)), ('1-2', 0, 3, (1, 2)), ('2-1', 3, 0, (1, 2)), ('2-2', 3, 2, (0, 1))]


def _row(cv, T, p, x0, x1, Y):
    n = len(p)
    c = 90
    sx = x0 + (x1 - x0 - n * c) / 2
    for i, v in enumerate(p):
        X = sx + i * c
        col = T['blue'] if i % 2 == 0 else T['pink']
        cv.rect((X + 4, Y, X + c - 4, Y + 66), fill=col, r=10)
        cv.text((X + c / 2, Y + 33), v, 30, T['bg'], anchor='mm', bold=True)
        cv.text((X + c / 2, Y + 70), f'第{i}堆', 17, T['dim'], anchor='mt')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S.get('piles')
    if p is None:
        return
    n = len(p)
    cv.text((x0 + 18, y0 + 4), 'piles（蓝 = 偶数堆，粉 = 奇数堆）', 22, T['muted'], bold=True)
    _row(cv, T, p, x0, x1, y0 + 44)
    Y = y0 + 150
    ev, od = sum(p[0::2]), sum(p[1::2])
    if n == 4:
        cv.text((x0 + 30, Y), '枚举 4 堆的所有走法（先手前两手之后，剩两堆再选一堆）：', 22, T['muted'], bold=True)
        Y += 40
        for tag, f, b, (u, v) in CASES:
            a1 = sorted((f, u))
            a2 = sorted((f, v))

            def comb(a):
                if a in ([0, 2], [1, 3]):
                    return f'=={a[0]} + {a[1]}（{p[a[0]] + p[a[1]]}）=='
                return f'`{a[0]} + {a[1]} = {p[a[0]] + p[a[1]]}`'
            line = f'{tag}）先手拿第 {f} 堆，后手拿第 {b} 堆 → 先手 {comb(a1)} 或 {comb(a2)}'
            cv.rich(x0 + 40, Y, line, x1 - x0 - 60, size=23, color=T['text'], accent=T['yellow'])
            Y += 44
        Y += 8
        best = '0 + 2' if ev > od else '1 + 3'
        first = 0 if ev > od else 3
        cv.rich(x0 + 40, Y, f'先手拿第 0 堆 → 必能拿到 `0 + 2 = {ev}`；拿第 3 堆 → 必能拿到 `1 + 3 = {od}`', x1 - x0 - 60,
                size=23, color=T['muted'])
        cv.rich(x0 + 40, Y + 44, f'两者必有一个更大 → 第一手拿第 {first} 堆，拿到 =={best}==，先手胜', x1 - x0 - 60,
                size=24, color=T['green'], accent=T['orange'])
    else:
        cv.text((x0 + 30, Y), f'推广到 n = {n} 堆：', 22, T['muted'], bold=True)
        lines = [
            '先手拿第 0 堆 → 后手只能拿第 1 或第 n − 1 堆（都是奇数）',
            '先手==顺势==拿走第 2 或第 n − 2 堆……一直拿到==全部偶数堆==',
            '同理，先拿第 n − 1 堆就能拿到==全部奇数堆==',
            f'偶数堆 `{ev}`，奇数堆 `{od}` → 先手选 =={"偶数堆" if ev > od else "奇数堆"}==，必胜',
        ]
        Y += 44
        for s in lines:
            cv.rich(x0 + 40, Y, s, x1 - x0 - 60, size=24, color=T['text'], accent=T['orange'])
            Y += 50
    cur = next(k for k, q in enumerate(PILES) if list(q) == list(p))
    Y3 = y1 - 52
    X = x0 + 30
    for k, q in enumerate(PILES):
        txt = f'{list(q)} → ' + ('True' if k <= cur else '?')
        w = cv.tlen(txt, 21, True, True) + 26
        cv.rect((X, Y3, X + w, Y3 + 42), fill=T['blue'] if k == cur else T['panel2'], r=10, outline=T['border'])
        cv.text((X + w / 2, Y3 + 21), txt, 21, T['bg'] if k == cur else (T['text'] if k < cur else T['dim']),
                anchor='mm', bold=True, mono=True)
        X += w + 12


CONFIG = dict(
    num=877, title='石子游戏', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='从 4 堆的枚举推广到 n 堆',
    tags=['labuladong', '灵神题单·动态规划', '难度分 1590'],
    code='''
class Solution(object):
    def stoneGame(self, piles):
        return True
''',
    call=f'[Solution().stoneGame(p) for p in {[list(p) for p in PILES]}]',
    expect=[True, True, True],
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('堆数', lambda S: len(S['piles']) if 'piles' in S else None),
           ('偶数堆之和', lambda S: sum(S['piles'][0::2]) if 'piles' in S else None, 'blue'),
           ('奇数堆之和', lambda S: sum(S['piles'][1::2]) if 'piles' in S else None, 'pink')],
    captions={
        'return True': lambda S, B, r: (
            f'4 堆：先手要么稳拿 `0 + 2 = {sum(S.piles[0::2])}`，要么稳拿 `1 + 3 = {sum(S.piles[1::2])}` → 选大的，=={r}=='
            if len(S.piles) == 4 else
            f'{len(S.piles)} 堆：偶数堆 `{sum(S.piles[0::2])}`、奇数堆 `{sum(S.piles[1::2])}`，先手都能整组拿走 → =={r}=='),
    },
    cards=dict(
        one_liner='先拿 4 堆的情况硬枚举，发现先手能锁定“全偶数堆”或“全奇数堆”',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['偶数堆石子排成一行，两人轮流从==行首或行尾==拿走一整堆，先手先拿',
                 '石子总数为奇数，拿得多的人赢；双方都最优，先手赢返回 `true`',
                 '示例：`[5,3,4,5]` → `true`'],
        quote='当先手第一轮拿第0块石头时，其==必然可以拿到0 + 2的组合==；而当先手第一轮拿第3块石头时，其必然可以拿到1 + 3的组合。',
        quote_src='—— yiduobo 题解原文',
        idea=['只有两堆：先手拿大的，显然必胜',
              '四堆：枚举先手、后手的前两手，共 4 种情况',
              '结论能推广：先手总能拿到全部奇数堆或全部偶数堆，选多的那组'],
        summary=['时间 `O(1)`，空间 `O(1)`：代码就是 `return True`',
                 '思路来源：从小规模（2 堆、4 堆）枚举找规律，再推广到 n 堆',
                 '总数为奇数 → 奇数堆之和 ≠ 偶数堆之和，不会平局',
                 '和灵神的区别：灵神直接给出奇偶策略；yiduobo 先枚举 4 堆再归纳',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
