ORIG = [[7, 4, 2], [6, 5, 1]]


def _sim():
    import heapq
    h = [[ORIG[i][-1], i, len(ORIG[0]) - 1] for i in range(len(ORIG))]
    heapq.heapify(h)
    day = {}
    for k in range(len(ORIG) * len(ORIG[0])):
        v, x, y = heapq.heappop(h)
        day[(x, y)] = k + 1
        if y > 0:
            heapq.heappush(h, [ORIG[x][y - 1], x, y - 1])
    return day


DAY = _sim()


def _thr(S, x):
    """第 x 行：下标 >= thr 的格子已经买掉"""
    n = len(ORIG[0])
    for _, hx, hy in S.get('heap', []):
        if hx == x:
            return hy + 1
    if 'v' in S:
        return S['y'] if S['x'] == x else 0
    return n


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'heap' not in S:
        return
    m, n = len(ORIG), len(ORIG[0])
    cell = min(76, (x1 - x0 - 160) / n)
    rh = cell * 0.95
    sx, sy = x0 + 110, y0 + 42
    cv.text((x0 + 18, y0 + 4), 'values（灰 = 已买，角标 = 第几天；橙框 = 堆里这一行的候选）', 21, T['muted'], bold=True)
    cand = {(hx, hy) for _, hx, hy in S['heap']}
    for x in range(m):
        cv.text((sx - 16, sy + x * (rh + 8) + rh / 2), f'商店 {x}', 22, T['muted'], anchor='rm', bold=True)
        thr = _thr(S, x)
        for j in range(n):
            X, Y = sx + j * cell, sy + x * (rh + 8)
            bought = j >= thr
            top = (x, j) in cand
            cv.rect((X + 3, Y, X + cell - 3, Y + rh), fill=(52, 60, 72) if bought else T['panel2'], r=8,
                    outline=T['orange'] if top else T['border'], width=5 if top else 1)
            cv.text((X + cell / 2, Y + rh * 0.62), ORIG[x][j], 34, T['dim'] if bought else T['text'], anchor='mm', bold=True)
            if bought:
                cv.text((X + cell - 8, Y + 5), f'第{DAY[(x, j)]}天', 15, T['green'], anchor='ra', bold=True)


CONFIG = dict(
    num=2931, title='购买物品的最大开销', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='先便宜后贵 · k 路归并（堆）',
    tags=['堆（优先队列）', '贪心与思维', '难度分 1822'],
    code='''
class Solution(object):
    def maxSpending(self, values):

        heap = []
        m = len(values)
        n = len(values[0])
        for i in range(m):
            heapq.heappush(heap, [values[i][n - 1], i, n - 1])
        
        res = 0
        for i in range(m * n):
            v, x, y = heapq.heappop(heap)
            res += v * (i + 1)
            if y > 0:
                heapq.heappush(heap, [values[x][y - 1], x, y - 1])
        
        return res
''',
    call='Solution().maxSpending([[7,4,2],[6,5,1]])',
    expect=109,
    views=[
        dict(type='custom', draw=_draw, h=340),
        dict(type='heap', var='heap', fmt=lambda e: f'{e[0]}(店{e[1]})', label='heap：每个商店当前最右边的物品', h=130),
        dict(type='text', fn=lambda S: f"第 `{S['i'] + 1}` 天买 `{S['v']}`：`{S['v']} × {S['i'] + 1}` = =={S['v'] * (S['i'] + 1)}==，累计 `{S['res']}`" if 'v' in S and S.get('_line', 0) >= 13 else '', h=60),
    ],
    watch=[('第几天', lambda S: S['i'] + 1 if 'v' in S else 0, 'blue'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'for i in range(m):': lambda S, B, r: ('`m` 个商店各取最右边（最便宜）的一件放进堆' if 'v' not in S
                                               else f"第 `{S['i'] + 1}` 天：从堆里取全场最便宜的"),
        'heapq.heappush(heap, [values[i][n - 1]': '商店 `{i}` 最右边的 `{values[i][n - 1]}` 入堆：每个商店里它最便宜',
        'res = 0': '`res` 累计总开销',
        'v, x, y = heapq.heappop': '弹出堆顶：商店 `{x}` 第 `{y}` 件 `{v}` 是剩下里最便宜的 —— 第 `{i + 1}` 便宜',
        'res += v * (i + 1)': '先买便宜的：第 `{i + 1}` 天买它，`{v} × {i + 1}` = =={v * (i + 1)}==，`res` = {res}',
        'if y > 0': lambda S, B, r: (f"商店 {S['x']} 左边还有物品（下标 {S['y'] - 1}）→ 它成为新的候选" if S['y'] > 0
                                     else f"商店 {S['x']} 已经买光，不再入堆"),
        'heapq.heappush(heap, [values[x]': '把商店 `{x}` 左边那件 `{values[x][y - 1]}` 入堆 —— 就是 k 路归并（同 23 题思路）',
        'return res': '购买全部物品的最大总开销 = =={ret}==',
    },
    cards=dict(
        one_liner='先买便宜的、后买贵的；每行有序 → 用堆做 k 路归并',
        complexity='时间 `O(mn log m)`，空间 `O(m)`',
        problem=['`m` 个商店各有 `n` 件物品（每店从左到右非递增），第 `d` 天只能买某店最右边的一件，花费 `价值 × d`',
                 '求买完所有物品的最大总开销',
                 '示例：`[[7,4,2],[6,5,1]]` → ==109=='],
        quote='为了使得开销最大，那么很直观的想法就是先买便宜的再买贵的。……当前剩下的货物中最便宜的一定是所有商店最右侧商品中的某一个，也就是说一定可以在第k轮买到第k便宜的物品。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘数 `d` 越来越大，大乘数配==大价值==总和最大 → 便宜的先买',
              '每行已排序，所以「当前最便宜」只可能在 `m` 个行尾里',
              '问题变成 k 路归并：弹出堆顶，再补这一行左边的下一件'],
        summary=['时间 `O(mn log m)`，空间 `O(m)`',
                 '堆元素是 `[价值, 行, 列]`，弹出后要靠行列找到补进来的下一件',
                 '`y > 0` 才补位，否则这一行已经买光',
                 '作者提示：思路与第 23 题（合并 K 个排序链表）相同',
                 '灵神另给了「全部拍平后排序」的写法，更短但 `O(mn log mn)`'],
    ),
)
