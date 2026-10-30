ORIG = [[8, 5, 2], [6, 4, 1], [9, 7, 3]]


def _sim():
    import heapq
    vs = [r[:] for r in ORIG]
    h = [(a[-1], i) for i, a in enumerate(vs)]
    heapq.heapify(h)
    day = {}
    for d in range(1, len(vs) * len(vs[0]) + 1):
        v, i = heapq.heappop(h)
        day[(i, len(vs[i]) - 1)] = d
        vs[i].pop()
        if vs[i]:
            heapq.heappush(h, (vs[i][-1], i))
    return day


DAY = _sim()


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    vs = S.get('values')
    if vs is None:
        return
    m, n = len(ORIG), len(ORIG[0])
    cell = min(76, (x1 - x0 - 160) / n)
    sx, sy = x0 + 110, y0 + 42
    cv.text((x0 + 18, y0 + 4), 'values（灰 = 已买，角标 = 第几天；橙框 = 每行最右边、可买的最小数）', 21, T['muted'], bold=True)
    heap_i = {i for _, i in S.get('h', [])}
    for i in range(m):
        cv.text((sx - 16, sy + i * (cell * 0.95 + 8) + cell * 0.5), f'商店 {i}', 22, T['muted'], anchor='rm', bold=True)
        for j in range(n):
            X, Y = sx + j * cell, sy + i * (cell * 0.95 + 8)
            bought = j >= len(vs[i])
            top = (not bought) and j == len(vs[i]) - 1 and i in heap_i
            cv.rect((X + 3, Y, X + cell - 3, Y + cell * 0.95), fill=(52, 60, 72) if bought else T['panel2'], r=8,
                    outline=T['orange'] if top else T['border'], width=5 if top else 1)
            cv.text((X + cell / 2, Y + cell * 0.62), ORIG[i][j], 34, T['dim'] if bought else T['text'], anchor='mm', bold=True)
            if bought:
                cv.text((X + cell - 8, Y + 5), f'第{DAY[(i, j)]}天', 15, T['green'], anchor='ra', bold=True)


CONFIG = dict(
    num=2931, title='购买物品的最大开销', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='排序不等式 · 最小堆做 m 路归并',
    tags=['堆（优先队列）', '贪心与思维', '难度分 1822'],
    code='''
class Solution:
    def maxSpending(self, values: List[List[int]]) -> int:
        h = [(a[-1], i) for i, a in enumerate(values)]
        heapify(h)
        ans = 0
        for d in range(1, len(values) * len(values[0]) + 1):
            v, i = heappop(h)
            ans += v * d
            values[i].pop()
            if values[i]:
                heappush(h, (values[i][-1], i))
        return ans
''',
    call='Solution().maxSpending([[8,5,2],[6,4,1],[9,7,3]])',
    expect=285,
    views=[
        dict(type='custom', draw=_draw, h=340),
        dict(type='heap', var='h', fmt=lambda x: f'{x[0]}(店{x[1]})', label='h：各店最右边的数（最小堆）', h=130),
        dict(type='text', fn=lambda S: f"第 `{S['d']}` 天买 `{S['v']}`：`{S['v']} × {S['d']}` = =={S['v'] * S['d']}==，累计 `{S['ans']}`" if 'v' in S and 'd' in S and S.get('_line', 0) >= 9 else '', h=60),
    ],
    watch=[('d', 'd', 'blue'), ('v', 'v', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'h = [(': '每个商店最右边的数最小（每行非递增）：把 `(最右的数, 商店号)` 入堆，==堆顶 = 全场最小==',
        'heapify': '堆化：接下来每一天都从堆顶取最小的数',
        'for d in range': lambda S, B, r: ('所有物品都买完了，循环结束' if not any(S['values']) else
                                          f"第 `{S['d']}` 天：排序不等式 → ==越小的数越早买==，所以按从小到大的顺序取"),
        'v, i = heappop': '弹出堆顶：商店 `{i}` 最右边的 `{v}` 是剩下里最小的',
        'ans += v * d': '买它：`{v} × {d}` = =={v * d}==，`ans` = {ans}',
        'values[i].pop()': '商店 {i} 最右边的买掉了，下一个候选是它左边那个',
        'if values[i]': lambda S, B, r: (f"商店 {S['i']} 还有物品 → 把新的最右边数 `{S['values'][S['i']][-1]}` 入堆" if S['values'][S['i']]
                                         else f"商店 {S['i']} 买光了，不再入堆"),
        'heappush': '入堆：这就是 m 路归并（类似 23 题合并 K 个链表），堆里始终最多 `m` 个数',
        'return ans': '购买全部物品的最大总开销 = =={ret}==',
    },
    cards=dict(
        one_liner='越小的数越早买；用最小堆从小到大取数',
        complexity='时间 `O(mn log m)`，空间 `O(m)`',
        problem=['`m` 个商店，每店 `n` 件物品，价值按行非递增；第 `d` 天只能买某店最右边的一件，花费 `价值 × d`',
                 '求买完所有物品的最大总开销',
                 '示例：`[[8,5,2],[6,4,1],[9,7,3]]` → ==285=='],
        quote='根据排序不等式，values[i][j] 越小的数，应该越早购买。……去掉最小的数，然后考虑每行的最后一个数，这 m 个数中一定包含次小的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序不等式：大的数配大的天数（乘数）总和才最大 → ==小的先买==',
              '最小的数一定在最后一列，次小的一定在「去掉最小后的每行最后一个数」里',
              '所以每天只比较 m 个行尾元素：用最小堆取最小，再把那一行的下一个入堆'],
        summary=['时间 `O(mn log m)`，空间 `O(m)`',
                 '直接 `values[i].pop()` 会修改输入；空了的商店不能再入堆',
                 '灵神写法一更短：把所有数拍平排序，`sum(x * i)`，时间 `O(mn log mn)`（视频演示写法二：堆）',
                 '模板：m 个有序序列按从小到大归并 = 堆 + 弹出后补下一个'],
    ),
)
