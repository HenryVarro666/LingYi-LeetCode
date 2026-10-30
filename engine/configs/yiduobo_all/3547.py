
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
    if 'res' not in S:
        return '每个点最多 2 个邻居 → 图只能是==链==或==环==，看 m 是 n 还是 n−1'
    if len(S['edges']) == n and S['res'] == sum(_order(n)[i] * _order(n)[i + 1] for i in range(n - 1)) + 2:
        return f'环 = 链 + 边 `1×2`：`{S["res"] - 2} + 2` = =={S["res"]}=='
    return f'`Σk² − n − (n−1)` = `{n * (n + 1) * (2 * n + 1) // 6} − {n} − {n - 1}` = =={S["res"]}=='


CONFIG = dict(
    num=3547, title='图中边值的最大和', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='平方差推导通项 · m==n 补 1×2',
    tags=[],
    code='''
class Solution(object):
    def maxScore(self, n, edges):
        
        res = n * (n + 1) * (n * 2 + 1) // 6 - n * 2 + 1
        if len(edges) == n:
            res += 2
        
        return res
''',
    call='Solution().maxScore(6, [[0,3],[4,5],[2,0],[1,3],[2,4],[1,5]])',
    expect=82,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='custom', draw=lambda cv, S, B, box, T: _draw(cv, dict(S, ans=S['res']) if 'res' in S else S, B, box, T), h=620),
    ],
    watch=['n', ('m', 'len(edges)', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = n': '先按链算：大数放中间，配对相乘用平方差，化简成 `Σk² − 2n + 1` = `{n*(n+1)*(2*n+1)//6} − {2*n} + 1` = =={res}==',
        'if len(edges)': lambda S, B, r: (f'`m = {len(S.edges)}` 等于 `n = {S.n}` → 是==环==，要把 `1×2` 这条边补回去' if len(S.edges) == S.n
                                          else f'`m = {len(S.edges)}` = n − 1 → 是==链==，不用补'),
        'res += 2': '环在 `1×2` 处划开就是链：补上 `1 × 2 = 2` → `res` = =={res}==',
        'return res': '最大得分 `{res}`',
    },
    cards=dict(
        one_liner='大数强强联合，用平方差把边权和化成 Σk² 的通项',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 个点的无向连通图，每个点最多 2 个邻居，分配 `1~n` 作点值',
                 '边权 = 两端点值之积，求边权之和最大是多少',
                 '示例：`n = 6` 的环 → `82`'],
        quote='是链还是环，取决于m是等于n还是等于n - 1。对于链的情况，则应该让较大的元素处于中间，让较小的元素处于两端。',
        quote_src='—— yiduobo 题解原文',
        before=[dict(heading='放置顺序', lines=['先放 `n`，把 `n−1`、`n−2` 放在它两侧',
                                          '再把 `n−3` 放在 `n−1` 旁，`n−4` 放在 `n−2` 旁，依次类推',
                                          '这个放法是固定的，所以一定有通项公式'])],
        idea=['每条边 `(k−1)(k+1) = k²−1`：用平方差把乘积拆开',
              '合起来：`1²−1 + 2²−1 + … + n²−1 − (n−1)`',
              '平方和公式 + 减去 `n` 个 1 和一个 `n−1`：`n(n+1)(2n+1)/6 − 2n + 1`',
              '环就是在 `1×2` 处划开的链，再加上这条边'],
        summary=['时间 `O(1)`，空间 `O(1)`，只用到 `len(edges)`',
                 '易错点：`m == n` 才是环，`m == n−1` 是链',
                 '易错点：公式里的 `− n*2 + 1` 别漏掉常数 1',
                 '对比灵神：灵神用排序不等式直接写出链公式，yiduobo 用平方差一项项推',
                 '原文已是 Python 3 可运行写法（本来就用 `//`），代码未改动'],
    ),
)
