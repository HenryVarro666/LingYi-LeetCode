VALS = [1, 2, 3, 4, 10, -10, -20]
EDGES = [[0, 1], [1, 2], [1, 3], [3, 4], [3, 5], [3, 6]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    vals = S['vals']
    hl = S.get('heap_list')
    s = S.get('s')
    k = S['k']
    cv.text((x0 + 18, y0 + 4), f'每个节点：小根堆（至多 k={k} 个正邻居）与当前星和 s[i]', 22, T['muted'], bold=True)
    y = y0 + 50
    rowh = min(62, (y1 - y - 10) / len(vals))
    x, yy = S.get('x'), S.get('y')
    for i, v in enumerate(vals):
        hot = i in (x, yy) and S['_line'] in range(9, 22)
        cv.text((x0 + 24, y + rowh / 2), f'节点 {i}', 24, T['yellow'] if hot else T['muted'], anchor='lm', bold=hot)
        cv.rect((x0 + 130, y + 6, x0 + 200, y + rowh - 6), fill=T['blue'], r=8)
        cv.text((x0 + 165, y + rowh / 2), v, 26, T['bg'], anchor='mm', bold=True)
        if hl is not None:
            cv.text((x0 + 220, y + rowh / 2), '堆', 20, T['dim'], anchor='lm')
            for j, w in enumerate(hl[i]):
                X = x0 + 262 + j * 64
                cv.rect((X, y + 8, X + 56, y + rowh - 8), fill=T['green'] if j == 0 else T['border'], r=8,
                        outline=T['yellow'] if hot else None, width=3 if hot else 1)
                cv.text((X + 28, y + rowh / 2), w, 24, T['bg'] if j == 0 else T['text'], anchor='mm', bold=True)
            if s is not None:
                cv.text((x1 - 24, y + rowh / 2), f's[{i}] = {s[i]}', 24, T['yellow'], anchor='rm', bold=True)
        y += rowh


CONFIG = dict(
    num=2497, title='图中最大星和', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='遍历边 + 每节点大小为 k 的小根堆',
    tags=[],
    code='''
class Solution(object):
    def maxStarSum(self, vals, edges, k):

        n = len(vals)
        heap_list = [[] for _ in range(n)]
        s = vals[:]

        for x, y in edges:
            if vals[y] > 0:
                s[x] += vals[y]
                heapq.heappush(heap_list[x], vals[y])
                if len(heap_list[x]) > k:
                    s[x] -= heap_list[x][0]
                    heapq.heappop(heap_list[x])
            
            if vals[x] > 0:
                s[y] += vals[x]
                heapq.heappush(heap_list[y], vals[x])
                if len(heap_list[y]) > k:
                    s[y] -= heap_list[y][0]
                    heapq.heappop(heap_list[y])
        
        return max(s)
''',
    call=f'Solution().maxStarSum({VALS}, {EDGES}, 2)',
    expect=16,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('k', 'k', 'orange'), ('max(s)', lambda S: max(S['s']) if 's' in S else None, 'green')],
    captions={
        'heap_list = ': '每个节点一个小根堆，保存它==当前选中==的正邻居，堆大小不超过 `k = {k}`',
        's = vals[:]': '`s[i]` 先是节点自己的值（中心必选），之后不断加上选中的邻居',
        'for x, y in edges': lambda S, B, ret: (f'处理边 `({S.x}, {S.y})`：两个方向都要更新' if (B.get('x'), B.get('y')) != (S.x, S.y) else '所有边都处理完了'),
        'if vals[y] > 0': lambda S, B, ret: (f'`vals[{S.y}] = {S.vals[S.y]}` > 0：可以作为 `{S.x}` 的邻居' if S.vals[S.y] > 0
                                             else f'`vals[{S.y}] = {S.vals[S.y]}` ≤ 0：负数不该被选，跳过'),
        's[x] += vals[y]': '先把它算进来：`s[{x}]` → `{s[x]}`',
        'heapq.heappush(heap_list[x]': '`{vals[y]}` 入 `{x}` 的堆：`{heap_list[x]}`',
        'if len(heap_list[x]) > k': lambda S, B, ret: (f'堆里有 `{len(S.heap_list[S.x])}` 个 > k = {S.k} → ==超了，踢掉最小的=='
                                                       if len(S.heap_list[S.x]) > S.k else f'堆里 `{len(S.heap_list[S.x])}` 个，未超过 k = {S.k}'),
        's[x] -= heap_list[x][0]': '堆顶是最小的 `{B.s[x] - s[x]}`，从 `s[{x}]` 里减掉 → `{s[x]}`',
        'heapq.heappop(heap_list[x])': '弹出堆顶，`{x}` 的堆剩 `{heap_list[x]}`',
        'if vals[x] > 0': lambda S, B, ret: (f'`vals[{S.x}] = {S.vals[S.x]}` > 0：可以作为 `{S.y}` 的邻居' if S.vals[S.x] > 0
                                             else f'`vals[{S.x}] = {S.vals[S.x]}` ≤ 0：负数不该被选，跳过'),
        's[y] += vals[x]': '先把它算进来：`s[{y}]` → `{s[y]}`',
        'heapq.heappush(heap_list[y]': '`{vals[x]}` 入 `{y}` 的堆：`{heap_list[y]}`',
        'if len(heap_list[y]) > k': lambda S, B, ret: (f'堆里有 `{len(S.heap_list[S.y])}` 个 > k = {S.k} → ==超了，踢掉最小的=='
                                                       if len(S.heap_list[S.y]) > S.k else f'堆里 `{len(S.heap_list[S.y])}` 个，未超过 k = {S.k}'),
        's[y] -= heap_list[y][0]': '堆顶是最小的 `{B.s[y] - s[y]}`，从 `s[{y}]` 里减掉 → `{s[y]}`',
        'heapq.heappop(heap_list[y])': '弹出堆顶，`{y}` 的堆剩 `{heap_list[y]}`',
        'return max(s)': '每个节点的 `s` 就是以它为中心的最大星和：`{s}`，取最大 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='遍历每条边，给每个节点维护大小为 k 的小根堆',
        complexity='时间 `O(n + m log k)`，空间 `O(n + m)`',
        problem=['无向图，节点有值；星图 = 一个中心加至多 `k` 个邻居',
                 '星和 = 星图所有节点值之和，求最大星和',
                 '示例：`vals=[1,2,3,4,10,-10,-20]`，`k=2` → `16`'],
        quote='对于这个问题，一种可行的处理方法是遍历每行，对于每行使用一个大小为k的堆来选择最大的k个数。当然也不一定需要k个，例如负数就不应该被选择。',
        quote_src='—— yiduobo 题解原文',
        idea=['把图看成 n 行的二维数组：第 i 行 = 节点 i 所有邻居的值',
              '不必真建这个数组，遍历每条边就等于遍历了所有行',
              '每次加入一个正邻居就累加到 `s`，堆超过 `k` 个就弹出最小的并从 `s` 里减去'],
        summary=['时间 `O(n + m log k)`，空间 `O(n + m)`',
                 '`s` 一直保持“中心值 + 当前堆内的邻居之和”，最后取 `max(s)`',
                 '易错：先入堆再判断 `len > k`，减掉的是弹出的堆顶（最小值）',
                 '原文本身就是 Python 3 可运行的写法，未做修改；`heapq` 由引擎预置',
                 '对比灵神：灵神先建好邻居表再 `nlargest`；这里边读边维护堆'],
    ),
)
