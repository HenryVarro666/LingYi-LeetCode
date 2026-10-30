C = [[0, 1, -1], [1, -2, 3]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f, g, h = S.get('f'), S.get('g'), S.get('h')
    if f is None:
        return
    m, n = len(C), len(C[0])
    I = S['_inner']
    ci, cj = I.get('i'), I.get('j')
    gap = 36
    cell = min(84, ((x1 - x0 - 40) - 3 * gap) / (4 * n))
    gw = cell * n
    sx = x0 + 20 + ((x1 - x0 - 40) - (4 * gw + 3 * gap)) / 2
    sy = y0 + 90
    specs = [('coins', C, T['text'], '路上的金币'), ('f（还有 2 次）', f, T['blue'], '2 次机会'),
             ('g（还有 1 次）', g, T['pink'], '1 次机会'), ('h（还有 0 次）', h, T['green'], '0 次机会')]
    bs = {1: B.get('f'), 2: B.get('g'), 3: B.get('h')}
    for k, (name, M, c, _) in enumerate(specs):
        X0 = sx + k * (gw + gap)
        cv.text((X0 + gw / 2, sy - 12), name, 22, c, anchor='mb', bold=True)
        for i in range(m):
            for j in range(n):
                X, Y = X0 + j * cell, sy + i * cell
                v = M[i][j]
                cur = (i, j) == (ci, cj)
                chg = k > 0 and bs[k] is not None and bs[k][i][j] != v
                neg = k == 0 and v < 0
                fill = T['pink'] if neg else T['panel2']
                cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6,
                        outline=T['yellow'] if (cur or chg) else T['border'], width=4 if (cur or chg) else 1)
                cv.text((X + cell / 2, Y + cell / 2), v, 28, T['bg'] if neg else T['text'], anchor='mm', bold=True)
    cv.text((x0 + 20, sy + m * cell + 24),
            'f / g / h = 还剩 2 / 1 / 0 次感化时的最大金币（黄框 = 当前 / 刚更新）', 19, T['muted'])
    if ci is not None and cj is not None and 'coins' in S:
        x = S['coins'][ci][cj]
        cv.text((x0 + 20, sy + m * cell + 62), f'当前格 ({ci},{cj}) 的值 = {x}' + ('，是强盗：g、h 多一个选择（感化）' if x < 0 else '，是金币：三张表都直接加上它'),
                24, T['yellow'], bold=True)


def _dir(S):
    i, j = S['i'], S['j']
    return '最左上角' if i == 0 and j == 0 else '第一行：只能从左边来' if i == 0 else '第一列：只能从上边来' if j == 0 else '内部格子：上、左都能来'


CONFIG = dict(
    num=3418, title='机器人可以获得的最大金币数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='网格 DP + 三张表对应感化次数',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1798'],
    code='''
class Solution(object):
    def maximumAmount(self, coins):

        m = len(coins)
        n = len(coins[0])

        f = [[0] * n for _ in range(m)]
        g = [[0] * n for _ in range(m)]
        h = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = coins[i][j]
                        if coins[i][j] < 0:
                            g[i][j] = 0
                            h[i][j] = 0
                        else:
                            g[i][j] = coins[i][j]
                            h[i][j] = coins[i][j]

                    else:
                        f[i][j] = f[i][j - 1] + coins[i][j]
                        if coins[i][j] >= 0:
                            g[i][j] = g[i][j - 1] + coins[i][j]
                            h[i][j] = h[i][j - 1] + coins[i][j]
                        else:
                            g[i][j] = max(f[i][j - 1], g[i][j - 1] + coins[i][j])
                            h[i][j] = max(g[i][j - 1], h[i][j - 1] + coins[i][j])

                elif j == 0:
                    f[i][j] = f[i - 1][j] + coins[i][j]
                    if coins[i][j] >= 0:
                        g[i][j] = g[i - 1][j] + coins[i][j]
                        h[i][j] = h[i - 1][j] + coins[i][j]
                    else:
                        g[i][j] = max(f[i - 1][j], g[i - 1][j] + coins[i][j])
                        h[i][j] = max(g[i - 1][j], h[i - 1][j] + coins[i][j])

                else:
                    f[i][j] = max(f[i - 1][j], f[i][j - 1]) + coins[i][j]
                    if coins[i][j] >= 0:
                        g[i][j] = max(g[i - 1][j], g[i][j - 1]) + coins[i][j]
                        h[i][j] = max(h[i - 1][j], h[i][j - 1]) + coins[i][j]
                    else:
                        g[i][j] = max(max(f[i - 1][j], f[i][j - 1]), max(g[i - 1][j], g[i][j - 1]) + coins[i][j])
                        h[i][j] = max(max(g[i - 1][j], g[i][j - 1]), max(h[i - 1][j], h[i][j - 1]) + coins[i][j])

        return h[-1][-1]
''',
    call=f'Solution().maximumAmount({C})',
    expect=4,
    skip=['for j in range', 'm = len', 'n = len', 'if i == 0:', 'elif j == 0', 'g[i][j] = 0', 'h[i][j] = 0'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=lambda S: ('位置：' + _dir(S['_inner'])) if 'i' in S['_inner'] and 'f' in S else '', size=24, h=50),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('j', "_inner.get('j')", 'pink'),
           ('coins[i][j]', "coins[_inner['i']][_inner['j']] if 'i' in _inner else None", 'yellow')],
    captions={
        'f = [[0]': '三张 `m × n` 的表：`f` / `g` / `h` 对应还有 ==2 / 1 / 0== 次感化机会',
        'g = [[0]': '`g`：还有 1 次机会',
        'h = [[0]': '`h`：还有 0 次机会，最后答案取 `h[-1][-1]`',
        'if j == 0:': lambda S, B, r: ('第一行的第一格：起点 `(0,0)`' if S['j'] == 0 else f"第一行 `j = {S['j']}`：只能从左边走来"),
        'h[i][j] = coins[i][j]': '起点是金币 → `h` 也拿 `{coins[i][j]}`',
        'f[i][j] = coins[i][j]': '起点：`f = {coins[i][j]}`（没得选，必须过这格）',
        'g[i][j] = coins[i][j]': '起点是金币 → 有没有感化机会都拿 `{coins[i][j]}`',
        'f[i][j] = f[i][j - 1] + coins[i][j]': '`f` 不用感化，只能从左边来：`{f[i][j - 1]} + {coins[i][j]}` = =={f[i][j]}==',
        'g[i][j] = g[i][j - 1] + coins': '金币格：`g` 从左边直接加：`{g[i][j - 1]} + {coins[i][j]}` = =={g[i][j]}==',
        'h[i][j] = h[i][j - 1] + coins': '金币格：`h` 从左边直接加：`{h[i][j - 1]} + {coins[i][j]}` = =={h[i][j]}==',
        'g[i][j] = max(f[i][j - 1], g': '强盗格：`g` 要么==感化==（从 `f[i][j-1] = {f[i][j - 1]}` 转来，不扣钱），要么被抢 `{g[i][j - 1]} + {coins[i][j]}` → =={g[i][j]}==',
        'h[i][j] = max(g[i][j - 1], h': '强盗格：`h` 要么==感化==（从 `g[i][j-1] = {g[i][j - 1]}` 转来），要么被抢 `{h[i][j - 1]} + {coins[i][j]}` → =={h[i][j]}==',
        'f[i][j] = f[i - 1][j] + coins': '`f` 不用感化，只能从上边来：`{f[i - 1][j]} + {coins[i][j]}` = =={f[i][j]}==',
        'g[i][j] = g[i - 1][j] + coins': '金币格：`g` 从上边直接加 → =={g[i][j]}==',
        'h[i][j] = h[i - 1][j] + coins': '金币格：`h` 从上边直接加 → =={h[i][j]}==',
        'g[i][j] = max(f[i - 1][j], g': '强盗格：`g` 要么==感化==（从 `f[i-1][j] = {f[i - 1][j]}`），要么被抢 `{g[i - 1][j]} + {coins[i][j]}` → =={g[i][j]}==',
        'h[i][j] = max(g[i - 1][j], h': '强盗格：`h` 要么==感化==（从 `g[i-1][j] = {g[i - 1][j]}`），要么被抢 `{h[i - 1][j]} + {coins[i][j]}` → =={h[i][j]}==',
        'f[i][j] = max(f[i - 1][j], f[i][j - 1])': '内部格 `f`：上、左取大再加 `{coins[i][j]}`：`max({f[i - 1][j]}, {f[i][j - 1]}) + {coins[i][j]}` = =={f[i][j]}==',
        'g[i][j] = max(g[i - 1][j], g[i][j - 1])': '内部金币格 `g`：上、左取大再加 → =={g[i][j]}==',
        'h[i][j] = max(h[i - 1][j], h[i][j - 1])': '内部金币格 `h`：上、左取大再加 → =={h[i][j]}==',
        'g[i][j] = max(max(f[i - 1][j]': '内部强盗格 `g`：==感化==取 `max(f上, f左) = {max(f[i - 1][j], f[i][j - 1])}`；不感化取 `max(g上, g左) + {coins[i][j]}` = {max(g[i - 1][j], g[i][j - 1]) + coins[i][j]} → =={g[i][j]}==',
        'h[i][j] = max(max(g[i - 1][j]': '内部强盗格 `h`：==感化==取 `max(g上, g左) = {max(g[i - 1][j], g[i][j - 1])}`；不感化取 `max(h上, h左) + {coins[i][j]}` = {max(h[i - 1][j], h[i][j - 1]) + coins[i][j]} → =={h[i][j]}==',
        'return h[-1][-1]': '终点的 `h`（用完最多 2 次机会后能拿到的最大值）= =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='感化次数也放进状态：f、g、h 三张表对应还剩 2、1、0 次',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 网格，机器人从左上走到右下，只能向右或向下',
                 '格子 `>= 0` 得金币，`< 0` 被抢；==最多感化 2 个强盗==免于被抢',
                 '示例：`[[0,1,-1],[1,-2,3]]`（本视频）→ `4`'],
        quote='对于本题，由于感化的次数有限，于是可以考虑将感化的次数也加入到状态表示中。令f[i][j]、g[i][j]、h[i][j]分别表示走到单元格(i, j)，且还有两次、一次、零次感化的机会时可以获得的最大金币数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['没有感化的版本：`f[i][j] = max(上, 左) + coins[i][j]`',
              '金币格：三张表更新方式不变',
              '强盗格：`g` 还可以从 `f` 感化转来，`h` 还可以从 `g` 转来',
              '第一行、第一列只有一个来源，要单独写'],
        summary=['时间/空间 `O(mn)`，最终答案 `h[-1][-1]`',
                 '易错：强盗格 `f` 仍然被抢；`g`、`h` 感化时==不加== `coins[i][j]`',
                 '易错：第 0 行、第 0 列要单独处理，否则下标 -1 会读到另一端',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：他把 k 压成长度 3 的数组并滚动掉行维度，这里是三张完整的表'],
    ),
)
