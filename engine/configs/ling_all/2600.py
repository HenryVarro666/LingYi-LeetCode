A, Z, N_, K = 3, 2, 4, 7
ITEMS = [1] * A + [0] * Z + [-1] * N_


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(ITEMS)
    cell = min(80, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = y0 + 90
    cv.text((x0 + 18, y0 + 4), f'袋子里的物品（从左到右按 1、0、-1 的顺序拿，k = {K}，框住的是被选中的）', 22, T['muted'], bold=True)
    for i, v in enumerate(ITEMS):
        X = sx + i * cell
        c = T['green'] if v == 1 else (T['cyan'] if v == 0 else T['pink'])
        cv.rect((X + 4, ys, X + cell - 4, ys + cell - 8), fill=c, r=12)
        cv.text((X + cell / 2, ys + cell / 2 - 4), v, 30, T['bg'], anchor='mm', bold=True, mono=True)
        if i < K:
            cv.rect((X + 1, ys - 4, X + cell - 1, ys + cell - 4), outline=T['yellow'], width=4, r=14)
    for lab, a, b, c in (('numOnes', 0, A, T['green']), ('numZeros', A, A + Z, T['cyan']), ('numNegOnes', A + Z, n, T['pink'])):
        xa, xb = sx + a * cell + 4, sx + b * cell - 4
        cv.line([(xa, ys + cell + 14), (xb, ys + cell + 14)], c, 4)
        cv.text(((xa + xb) / 2, ys + cell + 24), f'{lab}', 20, c, anchor='mt', bold=True)
    sel = ITEMS[:K]
    cv.text((x0 + 18, ys + cell + 100), f'拿满 k 件：1 × {sel.count(1)}，0 × {sel.count(0)}，-1 × {sel.count(-1)}  →  和 = {sum(sel)}', 28, T['text'], bold=True)


CONFIG = dict(
    num=2600, title='K 件物品的最大和', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='贪心 · 按 1,0,-1 顺序选',
    tags=[],
    code='''
class Solution:
    def kItemsWithMaximumSum(self, numOnes: int, numZeros: int, _: int, k: int) -> int:
        if k <= numOnes + numZeros:
            return min(k, numOnes)
        return numOnes * 2 + numZeros - k
''',
    call='Solution().kItemsWithMaximumSum(3, 2, 4, 7)',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=lambda S: f"`numOnes + numZeros = {S['numOnes'] + S['numZeros']}`，`k = {S['k']}`：" + ('1 和 0 够拿' if S['k'] <= S['numOnes'] + S['numZeros'] else '==1 和 0 不够，被迫拿 -1=='), size=34),
        dict(type='text', fn=lambda S: f"被迫拿的 -1：`k − numOnes − numZeros = {S['k'] - S['numOnes'] - S['numZeros']}` 个；答案 = `{S['numOnes']}×2 + {S['numZeros']} − {S['k']}` = =={S['numOnes'] * 2 + S['numZeros'] - S['k']}==" if S['k'] > S['numOnes'] + S['numZeros'] else '', size=30),
    ],
    watch=['numOnes', 'numZeros', 'k'],
    captions={
        'if k <= numOnes + numZeros': '`k = {k}` 与 `numOnes + numZeros = {numOnes + numZeros}` 比：{k} <= {numOnes + numZeros} 吗？成立 → 只用 1 和 0 就够，不必碰 -1；不成立 → ==要被迫拿 -1==',
        'return min(k, numOnes)': '1 和 0 够拿：先拿 1，最多拿 `numOnes` 个，其余拿 0 补足 → 答案 `min({k}, {numOnes})` = =={ret}==',
        'return numOnes * 2': '1 和 0 全拿了还差 `{k - numOnes - numZeros}` 件，只能拿 -1：`{numOnes} + ({k} − {numOnes} − {numZeros}) × (−1)` = `{numOnes}×2 + {numZeros} − {k}` = =={ret}==',
    },
    cards=dict(
        after=[dict(heading='验算本例', lines=['`1×3, 0×2, -1×4`，`k=7`：先拿 3 个 1 → 3', '再拿 2 个 0 → 仍是 3', '还差 2 件只能拿 -1 → `3 − 2 = 1`'])],
        one_liner='先拿 1，再拿 0，最后被迫才拿 -1',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['袋子里有 `numOnes` 个 1、`numZeros` 个 0、`numNegOnes` 个 -1',
                 '恰好选 `k` 件，求数字之和的最大值',
                 '本视频：`1×3, 0×2, -1×4, k=7` → `1`'],
        quote='贪心，按照 1,0,-1 的顺序选：先选 1，再选 0，最后选 -1（题目要求恰好选 k 个）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k <= numOnes + numZeros`：不会碰 -1，答案是 `min(k, numOnes)`',
              '否则 1、0 全选，还剩 `k - numOnes - numZeros` 个只能选 -1',
              '合并成一个式子：`numOnes*2 + numZeros - k`；第三个参数用不上，写成 `_`'],
        summary=['时间、空间都是 `O(1)`，不用循环',
                 '易错点：k 在 1 和 0 的范围内时，答案是 `min(k, numOnes)`，不是 `k`',
                 '1、0 都拿完后，每多拿一个 -1 就少 1：公式里的 `- k` 就是这个'],
    ),
)
