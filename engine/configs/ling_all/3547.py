
import math


def _order(n):
    """奇数升序 + 偶数降序：大的和大的相邻"""
    return list(range(1, n + 1, 2)) + list(range(n if n % 2 == 0 else n - 1, 0, -2))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    cyc = len(S['edges']) == n
    seq = _order(n)
    started = 'ans' in S
    chain_sum = sum(seq[i] * seq[i + 1] for i in range(n - 1))
    closed = started and cyc and S['ans'] == chain_sum + 2
    cv.text((x0 + 18, y0 + 4), '节点值的最优排布（青 = 链上的边，黄 = 首尾闭合的边）' if cyc else '节点值的最优排布', 24, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 24
    R = min(x1 - x0 - 260, y1 - y0 - 150) / 2
    pts = [(cx + R * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + R * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    for i in range(n):
        j = (i + 1) % n
        if j == 0 and not cyc:
            continue
        last = j == 0
        a, b = pts[i], pts[j]
        col = T['yellow'] if last else T['cyan']
        if last and not closed:
            if started:
                cv.dashed(a, b, T['dim'], 3)
            else:
                cv.dashed(a, b, T['border'], 3)
        elif started or not last:
            cv.line([a, b], col if started else T['border'], 5 if started else 3)
        if started and (not last or closed):
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            ox, oy = mx - cx, my - cy
            d = math.hypot(ox, oy) or 1
            lx, ly = mx + ox / d * 52, my + oy / d * 52
            cv.text((lx, ly), f'{seq[i]}×{seq[j]}={seq[i] * seq[j]}', 24, col, anchor='mm', bold=True)
    for i, (px, py) in enumerate(pts):
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=T['blue'] if started else T['panel2'], r=34, outline=T['border'])
        cv.text((px, py), seq[i] if started else '?', 36, T['bg'] if started else T['muted'], anchor='mm', bold=True)
    if started:
        cv.text((cx, cy - 20), f'{n} 个节点', 26, T['muted'], anchor='mm')
        cv.text((cx, cy + 20), '环' if cyc else '链', 34, T['yellow'], anchor='mm', bold=True)
        tot = S['ans']
        cv.text((cx, cy + 62), f'边值之和 {tot}', 28, T['green'], anchor='mm', bold=True)


def _text(S):
    n = S['n']
    if 'ans' not in S:
        return '每个点最多 2 个邻居 → 图只能是==链==或==环=='
    if S['ans'] == sum(_order(n)[i] * _order(n)[i + 1] for i in range(n - 1)) + (2 if len(S['edges']) == n else 0) and len(S['edges']) == n:
        return f'环 = 链 + 首尾一条边 `1×2`：`{S["ans"] - 2} + 2` = =={S["ans"]}=='
    return f'链：`n(n−1) + Σ i(i+2)` = `(2n²+5n−6)(n−1)/6` = =={S["ans"]}=='


CONFIG = dict(
    num=3547, title='图中边值的最大和', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='排序不等式 · 链公式 + 环补 2',
    tags=[],
    code='''
class Solution:
    def maxScore(self, n: int, edges: List[List[int]]) -> int:
        ans = (n * n * 2 + n * 5 - 6) * (n - 1) // 6
        if n == len(edges):  # 环
            ans += 2
        return ans
''',
    call='Solution().maxScore(6, [[0,3],[4,5],[2,0],[1,3],[2,4],[1,5]])',
    expect=82,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=['n', ('m', 'len(edges)', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = (n': '先当成==链==：最优链是 `1-3-5-6-4-2` 型，边值和 = `(2·{n}²+5·{n}−6)(n−1)/6` = =={ans}==',
        'if n == len': lambda S, B, r: (f'边数 `m = {len(S.edges)}` 等于 `n = {S.n}` → 连通且每点度数 ≤ 2，是==环==' if S.n == len(S.edges)
                                        else f'边数 `m = {len(S.edges)}` = n − 1 → 是==链==，公式已经是答案'),
        'ans += 2': '环比链多一条首尾边：最优排布里首尾恰是 `1` 和 `2` → `ans += 1×2` → =={ans}==',
        'return ans': '最大得分 `{ans}`',
    },
    cards=dict(
        one_liner='大数和大数相乘：链按 1-3-5-…-6-4-2 排，环再补一条 1×2',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['无向连通图，每个节点最多 2 个邻居；给节点分配 `1~n` 的唯一值',
                 '边值 = 两端点值的乘积，求所有边值之和的最大值',
                 '示例：`n = 6` 的环 → `82`'],
        quote='每个节点最多与其他两个节点相连，意味着这个图要么是链，要么是环。类似排序不等式，让大的和大的相乘，小的和小的相乘，可以让乘积之和最大。',
        quote_src='—— 灵茶山艾府题解',
        before=[dict(heading='从大到小摆', lines=['`6` 的邻居取最大的 `5` 和 `4`',
                                              '`5` 的另一个邻居取 `3`，`4` 的另一个取 `2`，`3` 的另一个取 `1`',
                                              '得到链 `1-3-5-6-4-2`，边值和 `n(n−1) + Σ i(i+2)`'])],
        idea=['平方和公式化简：链的边值和 = `(2n²+5n−6)(n−1)/6`',
              '环：链首尾恰好是 `1` 和 `2`，闭合后再加 `1×2 = 2`',
              '用 `n == len(edges)` 区分环和链，不用建图'],
        summary=['时间 `O(1)`，空间 `O(1)`，完全不用遍历 `edges`',
                 '易错点：环和链的判断是 `m == n` 还是 `m == n−1`',
                 '易错点：公式里是整除 `// 6`，乘完再除，不会有余数',
                 '思考题：改求最小值，大数配小数（反向的排序不等式）'],
    ),
)
