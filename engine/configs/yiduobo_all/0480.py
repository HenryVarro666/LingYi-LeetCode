def _in_loop(S):
    return 'del_dict' in S and 'res' in S


def _wl(S):
    if 'index' not in S or 'min_heap' not in S:
        return None
    if _in_loop(S) and 'add_num' in S:
        return S['index'] - S['k'] + 1 if False else S['index'] - S['k'] + 1
    return 0 if 'nums' in S else None


def _wr(S):
    if _in_loop(S) and 'add_num' in S:
        return S['index']
    return S['k'] - 1


def _ptr(S):
    return S['index'] if _in_loop(S) and 'add_num' in S else None


def _marks(h, neg, dd):
    c = dict(dd)
    out = []
    for v in sorted(h):
        r = -v if neg else v
        if c.get(r, 0) > 0:
            c[r] -= 1
            out.append((r, True))
        else:
            out.append((r, False))
    return sorted(out)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mn, mx = S.get('min_heap'), S.get('max_heap')
    if mn is None or mx is None:
        return
    dd = S.get('del_dict') or {}
    Ls, Rs = _marks(mn, True, dd), _marks(mx, False, dd)
    cv.text((x0 + 18, y0 + 4), '窗口排好序：min_heap（蓝）存较小一半，max_heap（粉）存较大一半；灰色划线 = 已记入 del_dict、还没弹出', 19, T['muted'], bold=True)
    n = len(Ls) + len(Rs)
    cell = min(70, (x1 - x0 - 80) / max(1, n))
    y = y0 + 56
    xs = x0 + 20
    tl = max((v for v, d in Ls if not d), default=None)
    tr = min((v for v, d in Rs if not d), default=None)
    for grp, col, hot_v in ((Ls, 'blue', tl), (Rs, 'pink', tr)):
        for v, d in grp:
            hot = (v == hot_v and not d)
            cv.rect((xs + 3, y, xs + cell - 3, y + 60), fill=(70, 76, 86) if d else T[col], r=8,
                    outline=T['yellow'] if hot else None, width=4 if hot else 1)
            cv.text((xs + cell / 2, y + 30), v, 26, T['muted'] if d else T['bg'], anchor='mm', bold=True)
            if d:
                cv.line([(xs + 8, y + 30), (xs + cell - 8, y + 30)], T['red'], 3)
            xs += cell
        if col == 'blue':
            cv.line([(xs + 6, y - 8), (xs + 6, y + 68)], T['muted'], 3)
            xs += 14
    cv.text((x0 + 20, y + 84), f'min_heap {len(mn)} 个，max_heap {len(mx)} 个（含灰色的）', 22, T['yellow'])
    if dd:
        pend = {k: v for k, v in dd.items() if v > 0}
        cv.text((x0 + 20, y + 118), f'待删除记录 del_dict = {pend if pend else "空"}', 22, T['muted'])


CONFIG = dict(
    num=480, title='滑动窗口中位数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='大小堆 + 延迟删除（del_dict）',
    tags=['堆（优先队列）', '对顶堆'],
    code='''
import heapq

class Solution(object):
    def medianSlidingWindow(self, nums, k):

        min_heap = []
        max_heap = []

        for num in nums[:k]:
            heapq.heappush(min_heap, -num)

        for index in range(k // 2):
            heapq.heappush(max_heap, -min_heap[0])
            heapq.heappop(min_heap)

        res = []
        del_dict = {}
        for index in range(k, len(nums)):
            if k % 2 == 1:
                res.append(float(-min_heap[0]))
            else:
                res.append((max_heap[0] - min_heap[0]) / 2.0)
            del_num = nums[index - k]
            del_dict[del_num] = del_dict.get(del_num, 0) + 1

            delta = 0
            if max_heap and del_num >= max_heap[0]:
                delta = 1
            else:
                delta = -1

            add_num = nums[index]
            if max_heap and add_num >= max_heap[0]:
                heapq.heappush(max_heap, add_num)
                delta -= 1
            else:
                heapq.heappush(min_heap, -add_num)
                delta += 1

            if delta > 0:
                heapq.heappush(max_heap, -min_heap[0])
                heapq.heappop(min_heap)
            elif delta < 0:
                heapq.heappush(min_heap, -max_heap[0])
                heapq.heappop(max_heap)

            while max_heap and del_dict.get(max_heap[0], 0) > 0:
                del_dict[max_heap[0]] -= 1
                heapq.heappop(max_heap)

            while min_heap and del_dict.get(-min_heap[0], 0) > 0:
                del_dict[-min_heap[0]] -= 1
                heapq.heappop(min_heap)

        if k % 2 == 1:
            res.append(float(-min_heap[0]))
        else:
            res.append((max_heap[0] - min_heap[0]) / 2.0)

        return res
''',
    call='Solution().medianSlidingWindow([1, 3, -1, -3, 5], 3)',
    expect=[1.0, -1.0, -1.0],
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口，k = 3）', window=(_wl, _wr), h=190),
        dict(type='custom', draw=_draw, h=240),
        dict(type='calls', label='正在执行', h=90),
    ],
    watch=[('index', 'index', 'blue'), ('del_num', 'del_num', 'red'), ('add_num', 'add_num', 'green'), ('delta', 'delta', 'orange'),
           ('res', 'res', 'cyan')],
    skip=['import heapq', 'min_heap = []', 'max_heap = []', 'res = []', 'del_dict = {}', 'delta = 0', 'delta = 1', 'delta = -1', 'delta -= 1', 'delta += 1'],
    max_steps=110,
    captions={
        'for num in nums[:k]': '先把前 `k` 个数全放进 `min_heap`（存相反数，堆顶 = 最大）',
        'heapq.heappush(min_heap, -num)': '`{num}` 入 min_heap（存相反数 `{-num}`）',
        'for index in range(k // 2)': '把 min_heap 里最大的一半挪给 max_heap',
        'heapq.heappush(max_heap, -min_heap[0])': lambda S, B, r_: '把 min_heap 的堆顶（最大值）搬到 max_heap',
        'heapq.heappop(min_heap)': '从 min_heap 弹出堆顶',
        'heapq.heappop(max_heap)': '从 max_heap 弹出堆顶',
        'for index in range(k, len(nums))': lambda S, B, r_: ('窗口要右移一格：`index = {}`，左边出去 `nums[{}]`，右边进来 `nums[{}]`'.format(S.index, S.index - S.k, S.index)
                                                              if B.get('index') != S.index else '窗口已经到最右边，退出循环，再补记最后一个窗口的中位数'),
        'if k % 2 == 1': lambda S, B, r_: ('`k` 是奇数：中位数 = min_heap 堆顶' if S.k % 2 == 1 else '`k` 是偶数：中位数 = 两个堆顶的平均'),
        'res.append(float(-min_heap[0]))': '先记下当前窗口的中位数 `{-min_heap[0]}`',
        'res.append((max_heap[0] - min_heap[0]) / 2.0)': '先记下当前窗口的中位数 `({max_heap[0]} + {-min_heap[0]}) / 2`',
        'del_num = nums[index - k]': '窗口左边要滑出去的数 `del_num = {del_num}`',
        'del_dict[del_num] = del_dict.get(del_num, 0) + 1': '不去堆里找，只在 `del_dict` 里记一笔：`{del_num}` 要删 `{del_dict[del_num]}` 次',
        'if max_heap and del_num >= max_heap[0]': lambda S, B, r_: (
            f'`del_num = {S.del_num}` ≥ max_heap 堆顶 `{S.max_heap[0]}` → 它在 ==max_heap==，大堆少 1 个：delta = +1'
            if S.max_heap and S.del_num >= S.max_heap[0] else f'`del_num = {S.del_num}` 比 max_heap 堆顶小 → 它在 ==min_heap==，小堆少 1 个：delta = -1'),
        'add_num = nums[index]': '窗口右边新进来的数 `add_num = {add_num}`',
        'if max_heap and add_num >= max_heap[0]': lambda S, B, r_: (
            f'`add_num = {S.add_num}` ≥ max_heap 堆顶 `{S.max_heap[0]}` → 放进 ==max_heap==，大堆多 1 个：delta - 1'
            if S.max_heap and S.add_num >= S.max_heap[0] else f'`add_num = {S.add_num}` 比 max_heap 堆顶小 → 放进 ==min_heap==，小堆多 1 个：delta + 1'),
        'heapq.heappush(max_heap, add_num)': '`{add_num}` 入 max_heap，`delta` = {delta}',
        'heapq.heappush(min_heap, -add_num)': '`{add_num}` 入 min_heap（存 `{-add_num}`），`delta` = {delta}',
        'if delta > 0': lambda S, B, r_: (f'`delta = {S.delta} > 0`：小堆多了 1 个 → 把 min_heap 堆顶搬到 max_heap' if S.delta > 0 else
                                          f'`delta = {S.delta}`：不是正数，看是否为负'),
        'elif delta < 0': lambda S, B, r_: (f'`delta = {S.delta} < 0`：大堆多了 1 个 → 把 max_heap 堆顶搬到 min_heap' if S.delta < 0 else
                                            f'`delta = 0`：出一个进一个，两堆大小没变，不用搬'),
        'heapq.heappush(min_heap, -max_heap[0])': '把 max_heap 的堆顶（最小的大值）搬到 min_heap',
        'while max_heap and del_dict.get(max_heap[0], 0) > 0': lambda S, B, r_: (
            '`max_heap` 堆顶是待删除的数 → 现在真正弹出' if S.max_heap and S.del_dict.get(S.max_heap[0], 0) > 0
            else '`max_heap` 堆顶没有待删记录，不用清'),
        'while min_heap and del_dict.get(-min_heap[0], 0) > 0': lambda S, B, r_: (
            '`min_heap` 堆顶是待删除的数 → 现在真正弹出' if S.min_heap and S.del_dict.get(-S.min_heap[0], 0) > 0
            else '`min_heap` 堆顶没有待删记录，不用清'),
        'del_dict[max_heap[0]] -= 1': '划掉一次待删记录',
        'del_dict[-min_heap[0]] -= 1': '划掉一次待删记录',
        'return res': '全部窗口的中位数：`{res}`',
    },
    cards=dict(
        one_liner='大小堆管中位数；滑出去的数先记在字典里，到堆顶再删',
        complexity='时间 `O(n log k)` 量级（均摊），空间 `O(n)`',
        problem=['长为 `k` 的窗口从左滑到右，每次输出窗口的中位数',
                 '偶数个时取中间两数的平均',
                 '本视频：`nums = [1,3,-1,-3,5]`，`k = 3` → `[1.0,-1.0,-1.0]`'],
        quote='不需要立即删除某个元素，而是将其记录下来，直到其被推到堆顶时再一次性删除。',
        quote_src='—— yiduobo 题解原文',
        idea=['前 `k` 个数先进 `min_heap`（取反当大顶堆），再搬一半到 `max_heap`',
              '每次滑动：左边出一个、右边进一个，有四种情况；前两种两堆大小不变',
              '另两种用 `delta` 记录哪个堆多了，把多的那个堆的堆顶搬到另一边',
              '出去的数只记在 `del_dict`，每次滑动后检查两个堆顶，是待删的就弹出'],
        summary=['时间均摊 `O(n log n)`（堆里含未清理的数），空间 `O(n)`',
                 '易错：只清理堆顶，非堆顶的待删数会暂时留在堆里，但不影响中位数',
                 '易错：`delta` 先由出窗口的数决定，再由进窗口的数修正，最后才搬堆顶',
                 '原文为 Python 2 写法，`range(k / 2)` 已改为 `range(k // 2)`',
                 '对比灵神：灵神把懒删除封装成 `LazyHeap` 并用 `size` 记真实大小；yiduobo 用 `delta` 保持平衡'],
    ),
)
