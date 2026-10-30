from collections import Counter as _Cn


def _items(h, dd):
    if h is None or dd is None:
        return None
    c = _Cn(h)
    return sorted(c.elements())


def _draw_heaps(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mn, mx = S.get('min_heap'), S.get('max_heap')
    if mn is None or mx is None or 'f' in S:
        cv.text((x0 + 18, y0 + 6), '双堆：min_heap（较小一半）+ max_heap（较大一半）', 22, T['muted'], bold=True)
        return
    dd = S.get('del_dict') or {}
    # 实际元素：min_heap 存相反数；被标记删除的元素画成灰色
    Ls = sorted(-v for v in mn)
    Rs = sorted(mx)
    gone = _Cn({k: v for k, v in dd.items() if v > 0})
    cv.text((x0 + 18, y0 + 16), 'min_heap（较小一半）| max_heap（较大一半）；灰 = 已标记删除', 20, T['muted'], bold=True)
    cell, gap = 54, 30
    total = (len(Ls) + len(Rs)) * cell + gap
    xs = x0 + (x1 - x0 - total) / 2
    y = y0 + 48

    def box_(v, fill, top, ghost):
        nonlocal xs
        cv.rect((xs + 3, y, xs + cell - 3, y + cell - 6), fill=(70, 76, 86) if ghost else fill, r=8,
                outline=T['yellow'] if top else None, width=4 if top else 1)
        cv.text((xs + cell / 2, y + (cell - 6) / 2), v, 26, T['muted'] if ghost else T['bg'], anchor='mm', bold=True)
        xs += cell

    rem = _Cn(gone)
    for k, v in enumerate(Ls):
        gh = rem.get(v, 0) > 0
        if gh:
            rem[v] -= 1
        box_(v, T['blue'], k == len(Ls) - 1, gh)
    dx = xs + gap / 2
    cv.line([(dx, y - 8), (dx, y + cell)], T['muted'], 3)
    xs += gap
    for k, v in enumerate(Rs):
        gh = rem.get(v, 0) > 0
        if gh:
            rem[v] -= 1
        box_(v, T['pink'], k == 0, gh)
    ly = y + cell + 0
    cv.text((x0 + 20, ly), f's_min = {S.get("s_min")}（{len(Ls)} 个）', 20, T['blue'], bold=True)
    cv.text((x1 - 20, ly), f's_max = {S.get("s_max")}（{len(Rs)} 个）', 20, T['pink'], anchor='rt', bold=True)


def _w0(S):
    if 'cost' in S and 'index' in S and 'x' in S and 'n' in S:
        return max(0, S['index'] - S['x'] + 1)
    return None


def _w1(S):
    return S['index'] if 'cost' in S and 'index' in S else None


def _fcolor(S, r, c, v):
    if 'f' not in S or 'p' not in S or 'index' not in S:
        return None
    i, p, x = S['index'], S['p'], S['x']
    if (r, c) == (i, p):
        return 'yellow'
    if (r, c) in ((i - x, p - 1), (i - 1, p)):
        return 'blue'
    return None


def _pn(v):
    return f'({v})' if v < 0 else f'{v}'


def _cap_cost_at(S, idx):
    mid = -S.min_heap[0]
    return (f'窗口 `[{idx - S.x + 1}, {idx}]` 中位数 `{mid}`：小半边 `{S.min_size}×{_pn(mid)} − {_pn(S.s_min)}`，'
            f'大半边 `{_pn(S.s_max)} − {S.max_size}×{_pn(mid)}` → 合计 ==`cost[{idx}] = {S.cost[idx]}`==')


def _cap_cost(S, B, ret):
    return _cap_cost_at(S, S.index)


def _cap_cost0(S, B, ret):
    return _cap_cost_at(S, S.x - 1)


def _cap_del(S, B, ret):
    d = S.del_num
    big = bool(S.max_heap) and d >= S.max_heap[0]
    side = f'`{d} >= max_heap 堆顶 {S.max_heap[0]}` → 在大半边（max_heap）' if big else f'`{d}` 比 max_heap 堆顶小 → 在小半边（min_heap）'
    return f'窗口左端 `{d}` 要离开：先只做标记（懒删除）。{side}，两边大小差随之变化'


def _cap_add(S, B, ret):
    a = S.add_num
    if S.max_heap and a >= S.max_heap[0] and B.get('max_heap') != S.max_heap:
        return f'新进 `{a}` >= max_heap 堆顶 → 放大半边 max_heap'
    return f'新进 `{a}` 比 max_heap 堆顶小 → 放小半边 min_heap'


def _cap_f1(S, B, ret):
    return (f'`f[{S.index}][{S.p}] = f[{S.index - S.x}][{S.p - 1}] + cost[{S.index}]` = '
            f'`{S.f[S.index - S.x][S.p - 1]} + {S.cost[S.index]}` = =={S.f[S.index][S.p]}==（选这个窗口）')


def _cap_f2(S, B, ret):
    return f'再和不选末尾 `f[{S.index - 1}][{S.p}] = {S.f[S.index - 1][S.p]}` 比，取小 → ==`f[{S.index}][{S.p}] = {S.f[S.index][S.p]}`=='


CONFIG = dict(
    num=3505, title='使 K 个子数组内元素相等的最少操作数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='双堆滑窗中位数 + 划分型 DP',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def minOperations(self, nums, x, k):
        
        min_heap = []
        max_heap = []
        s_min = 0
        s_max = 0
        max_size = x // 2
        min_size = x - max_size

        for num in nums[:x]:
            heapq.heappush(min_heap, -num)
            s_min += num

        for index in range(x // 2):
            heapq.heappush(max_heap, -min_heap[0])
            s_min += min_heap[0]
            s_max -= min_heap[0]
            heapq.heappop(min_heap)

        n = len(nums)
        cost = [0] * n
        cost[x - 1] = min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0])
        del_dict = {}
        for index in range(x, n):

            del_num = nums[index - x]
            del_dict[del_num] = del_dict.get(del_num, 0) + 1

            delta = 0
            if max_heap and del_num >= max_heap[0]:
                delta = 1
                s_max -= del_num
            else:
                delta = -1
                s_min -= del_num

            add_num = nums[index]
            if max_heap and add_num >= max_heap[0]:
                heapq.heappush(max_heap, add_num)
                s_max += add_num
                delta -= 1
            else:
                heapq.heappush(min_heap, -add_num)
                s_min += add_num
                delta += 1
            
            if delta > 0:
                heapq.heappush(max_heap, -min_heap[0])
                s_min += min_heap[0]
                s_max -= min_heap[0]
                heapq.heappop(min_heap)
            elif delta < 0:
                heapq.heappush(min_heap, -max_heap[0])
                s_max -= max_heap[0]
                s_min += max_heap[0]
                heapq.heappop(max_heap)

            while max_heap and del_dict.get(max_heap[0], 0) > 0:
                del_dict[max_heap[0]] -= 1
                heapq.heappop(max_heap)

            while min_heap and del_dict.get(-min_heap[0], 0) > 0:
                del_dict[-min_heap[0]] -= 1
                heapq.heappop(min_heap)
            
            cost[index] = min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0])

        
        f = [[0] * (k + 1) for _ in range(n)]
        for p in range(1, k + 1):
            for index in range(p * x - 1, n):
                f[index][p] = f[index - x][p - 1] + cost[index]
                if index > p * x - 1:
                    f[index][p] = min(f[index][p], f[index - 1][p])
        
        return f[-1][-1]
''',
    call='Solution().minOperations([9, -2, -2, -2, 1, 5], 2, 2)',
    expect=3,
    skip=[4, 5, 6, 7, 8, 9, 11, 13, 15, 16, 17, 18, 21, 22, 24, 25, 27, 30, 31, 32, 33, 34, 35, 36, 38, 39, 41, 42, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56, 59, 61, 63, 65, 70, 71, 72, 74],
    views=[
        dict(type='array', var='nums', label='nums', window=(_w0, _w1), h=110, cell=62),
        dict(type='custom', draw=_draw_heaps, h=150),
        dict(type='array', var='cost', label='cost[index]：以 index 结尾的长 x 窗口变成相同的操作数', pointers={'index': 'blue'}, h=175, cell=62),
        dict(type='table', var='f', label='f[index][p]：到 index 为止凑出 p 个窗口的最少操作数', color=_fcolor, h=260, cell=56),
    ],
    watch=[('index', 'index', 'blue'), 'p', 's_min', 's_max'],
    captions={
        12: lambda S, B, r: f'前 `x` 个数先放进 `min_heap`（存相反数）：现有 `{len(S.min_heap)}` 个，堆顶 = 最大 = `{-S.min_heap[0]}`',
        19: '把 `min_heap` 里最大的数挪进 `max_heap`：小半边留 `x − x//2` 个，大半边 `x//2` 个',
        23: _cap_cost0,
        28: _cap_del,
        40: _cap_add,
        44: _cap_add,
        52: '小半边多了一个 → 把 `min_heap` 最大的数挪到 `max_heap`，重新平衡',
        57: '大半边多了一个 → 把 `max_heap` 最小的数挪到 `min_heap`，重新平衡',
        60: '`max_heap` 堆顶已被标记删除 → 现在才真正弹出它',
        64: '`min_heap` 堆顶已被标记删除 → 现在才真正弹出它',
        67: _cap_cost,
        73: _cap_f1,
        75: _cap_f2,
        77: '`f[n−1][k]`：用完全部数、凑够 `k` 个窗口 → =={ret}==',
    },
    cards=dict(
        one_liner='先用双堆算出每个窗口的代价，再按「选 / 不选」划分',
        complexity='时间 `O(n log n + nk)`，空间 `O(nk)`',
        problem=['给整数数组 `nums`，每次可把一个元素加 1 或减 1',
                 '要凑出 `k` 个长度恰为 `x`、互不重叠的子数组，每个子数组内元素相等',
                 '示例：`nums=[9,-2,-2,-2,1,5], x=2, k=2` → `3`'],
        quote='可以发现，这又是经典的贪心问题，将区间中的所有元素变为中位数时所需的操作次数最少。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index][p]`：到 `index` 为止凑出 `p` 个窗口的最少操作数；放弃 `nums[index]` 或用它做窗口末尾',
              '`cost[index]`：窗口 `[index−x+1, index]` 变成中位数的操作数——先用双堆滑窗预处理',
              '双堆：`min_heap`（较小一半）、`max_heap`（较大一半）+ 两边的和 `s_min / s_max`，删除用 `del_dict` 懒删除'],
        summary=['时间 `O(n log n + nk)`，空间 `O(nk)`',
                 '堆里 `min_heap` 存相反数；`delta` 记录离开/进入后两堆的大小差，大于 0 / 小于 0 就挪一个数',
                 '懒删除：堆顶被标记时才真正弹出，所以每次最后要清理两个堆顶；`f[index − x]` 在 `index < x` 时取到 `f[-1][0]`，但 `p = 0` 列恒为 0，不影响',
                 '原文是 Python 2 风格的类写法，本题无需改动；对比灵神：灵神封装了 `LazyHeap` 并只维护 `left.size/right.size`'],
    ),
)
