def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['k'] + 1)


def _real(h, neg):
    """堆里每个元素：(真实值, 是否已被懒删除)，按真实值从小到大"""
    c = dict(h.remove_cnt)
    out = []
    for v in sorted(h.heap):
        if c.get(v, 0) > 0:
            c[v] -= 1
            out.append((-v if neg else v, True))
        else:
            out.append((-v if neg else v, False))
    return sorted(out)


def _tl(S):
    return max((v for v, d in _real(S['left'], True) if not d), default=None)


def _tr(S):
    return min((v for v, d in _real(S['right'], False) if not d), default=None)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    left, right = S.get('left'), S.get('right')
    if left is None or right is None:
        return
    Ls, Rs = _real(left, True), _real(right, False)
    cv.text((x0 + 18, y0 + 4), '把窗口排好序：left（蓝）存较小一半，right（粉）存较大一半；灰色划线 = 已懒删除、还留在堆里', 20, T['muted'], bold=True)
    n = len(Ls) + len(Rs)
    cell = min(70, (x1 - x0 - 80) / max(1, n))
    sx = x0 + 20
    y = y0 + 56
    xs = sx
    top_l = max((v for v, d in Ls if not d), default=None)
    top_r = min((v for v, d in Rs if not d), default=None)
    for v, d in Ls:
        hot = (v == top_l and not d)
        cv.rect((xs + 3, y, xs + cell - 3, y + 60), fill=(70, 76, 86) if d else T['blue'], r=8,
                outline=T['yellow'] if hot else None, width=4 if hot else 1)
        cv.text((xs + cell / 2, y + 30), v, 26, T['muted'] if d else T['bg'], anchor='mm', bold=True)
        if d:
            cv.line([(xs + 8, y + 30), (xs + cell - 8, y + 30)], T['red'], 3)
        xs += cell
    cv.line([(xs + 6, y - 8), (xs + 6, y + 68)], T['muted'], 3)
    xs += 14
    for v, d in Rs:
        hot = (v == top_r and not d)
        cv.rect((xs + 3, y, xs + cell - 3, y + 60), fill=(70, 76, 86) if d else T['pink'], r=8,
                outline=T['yellow'] if hot else None, width=4 if hot else 1)
        cv.text((xs + cell / 2, y + 30), v, 26, T['muted'] if d else T['bg'], anchor='mm', bold=True)
        if d:
            cv.line([(xs + 8, y + 30), (xs + cell - 8, y + 30)], T['red'], 3)
        xs += cell
    ls, rs = left.size, right.size
    cv.text((x0 + 20, y + 84), f'left.size = {ls}，right.size = {rs}（真实大小，不含已懒删除的）', 22, T['yellow'])
    if top_l is not None:
        cv.text((x0 + 20, y + 118), f'黄框 = 两个堆真正的堆顶：left 顶 {top_l}，right 顶 {top_r if top_r is not None else "无"}', 22, T['muted'])


CONFIG = dict(
    num=480, title='滑动窗口中位数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='定长滑窗 + 对顶堆 + 懒删除堆',
    tags=['堆（优先队列）', '对顶堆'],
    code='''
class LazyHeap:
    def __init__(self):
        self.heap = []
        self.remove_cnt = defaultdict(int)  # 每个元素剩余需要删除的次数
        self.size = 0  # 实际大小

    # 删除
    def remove(self, x: int) -> None:
        self.remove_cnt[x] += 1  # 懒删除
        self.size -= 1

    # 正式执行删除操作
    def apply_remove(self) -> None:
        while self.heap and self.remove_cnt[self.heap[0]] > 0:
            self.remove_cnt[self.heap[0]] -= 1
            heappop(self.heap)

    # 查看堆顶
    def top(self) -> int:
        self.apply_remove()
        return self.heap[0]

    # 出堆
    def pop(self) -> int:
        self.apply_remove()
        self.size -= 1
        return heappop(self.heap)

    # 入堆
    def push(self, x: int) -> None:
        heappush(self.heap, x)
        self.size += 1

    # push(x) 然后 pop()
    def pushpop(self, x: int) -> int:
        self.apply_remove()
        return heappushpop(self.heap, x)

class Solution:
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[float]:
        ans = [0] * (len(nums) - k + 1)
        left = LazyHeap()   # 最大堆（元素取反）
        right = LazyHeap()  # 最小堆

        for i, x in enumerate(nums):
            # 1. 进入窗口
            if left.size == right.size:
                left.push(-right.pushpop(x))
            else:
                right.push(-left.pushpop(-x))

            l = i + 1 - k
            if l < 0:  # 窗口大小不足 k
                continue

            # 2. 计算答案
            if k % 2:
                ans[l] = -left.top()
            else:
                ans[l] = (right.top() - left.top()) / 2

            # 3. 离开窗口
            x = nums[l]
            if x <= -left.top():
                left.remove(-x)
                if left.size < right.size:
                    left.push(-right.pop())  # 平衡两个堆的大小
            else:
                right.remove(x)
                if left.size > right.size + 1:
                    right.push(-left.pop())  # 平衡两个堆的大小

        return ans
''',
    call='Solution().medianSlidingWindow([1, 3, -1, -3, 5], 3)',
    expect=[1, -1, -1],
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口，k = 3）', pointers={'i': 'blue'}, window=(_wl, 'i'), h=190),
        dict(type='custom', draw=_draw, h=240),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=[('i', 'i', 'blue'), ('l', 'l', 'cyan'), ('left.size', lambda S: S['left'].size if 'left' in S else None, 'blue'),
           ('right.size', lambda S: S['right'].size if 'right' in S else None, 'pink'), ('ans', 'ans', 'green')],
    skip=['self.heap = []', 'self.remove_cnt = defaultdict', 'self.size = 0', 'left = LazyHeap()', 'right = LazyHeap()',
          'ans = [0]', 'return heappop(self.heap)', 'self.size += 1', 'self.size -= 1', 'self.apply_remove()', 'def ',
          'return self.heap[0]', 'return heappushpop', 'while self.heap and', 'self.remove_cnt[x] += 1', 'self.remove_cnt[self.heap[0]] -= 1',
          'l = i + 1 - k', 'continue'],
    max_steps=110,
    captions={
        'if left.size == right.size': lambda S, B, r_: (
            f'`x = {S.x}` 进窗口：两堆一样大（{S.left.size} = {S.right.size}）→ 先放 right 再把最小的挪给 left，让 ==left 多 1 个=='
            if S.left.size == S.right.size else f'`x = {S.x}` 进窗口：left 比 right 多 1 个 → 先放 left 再把最大的挪给 right'),
        'left.push(-right.pushpop(x))': '`{nums[i]}` 先放进 right，再把 right 最小的挪给 left（可能就是它自己）',
        'right.push(-left.pushpop(-x))': '`{nums[i]}` 先放进 left，再把 left 最大的挪给 right（可能就是它自己）',
        'for i, x in enumerate': lambda S, B, r_: ('所有数都处理完了' if B.get('i') == S.i else f'窗口右端点 `i = {S.i}`，新进来的数 `x = {S.x}`'),
        'heappush(self.heap, x)': '放进堆里，`size` 加 1',
        'if l < 0': lambda S, B, r_: ('`l = i + 1 - k = {}`：窗口里才 {} 个 < k = {}，继续进数'.format(S.i + 1 - S.k, S.i + 1, S.k) if S.i + 1 - S.k < 0 else '`l = {}`：窗口满了（`k` 个），可以算中位数'.format(S.i + 1 - S.k)),
        'x = nums[l]': '准备让最左边的 `nums[{l}]` = `{x}` 离开窗口',
        'if k % 2': lambda S, B, r_: ('`k` 是奇数：中位数 = left 的堆顶' if S.k % 2 else '`k` 是偶数：中位数 = 两个堆顶的平均'),
        'ans[l] = -left.top()': lambda S, B, r_: f'中位数 = left 堆顶 = ==`{_tl(S)}`==（`top()` 会先清掉堆顶的过期元素）',
        'ans[l] = (right.top() - left.top()) / 2': lambda S, B, r_: f'中位数 = ({_tr(S)} + {_tl(S)}) / 2 = =={(_tr(S) + _tl(S)) / 2}==',
        'if x <= -left.top()': lambda S, B, r_: (f'`x = {S.x}` ≤ left 堆顶 `{_tl(S)}` → x 在 ==left== 里' if S.x <= _tl(S)
                                                  else f'`x = {S.x}` > left 堆顶 `{_tl(S)}` → x 在 ==right== 里'),
        'left.remove(-x)': '不去堆里找，只记一笔：`remove_cnt[{-x}]` 加 1，`left.size` 减 1 → ==懒删除==',
        'right.remove(x)': '不去堆里找，只记一笔：`remove_cnt[{x}]` 加 1，`right.size` 减 1 → ==懒删除==',
        'if left.size < right.size': lambda S, B, r_: (f'`left.size = {S.left.size} < right.size = {S.right.size}`：left 少了 → 从 right 拿一个最小的过来' if S.left.size < S.right.size
                                                        else f'`left.size = {S.left.size} ≥ right.size = {S.right.size}`：不用平衡'),
        'if left.size > right.size + 1': lambda S, B, r_: (f'`left.size = {S.left.size} > right.size + 1 = {S.right.size + 1}`：left 多了 → 挪一个最大的给 right' if S.left.size > S.right.size + 1
                                                           else f'`left.size = {S.left.size} ≤ right.size + 1 = {S.right.size + 1}`：不用平衡'),
        'left.push(-right.pop())': '`right.pop()` 取最小的，取反后放进 left（`pop` 会先真正删掉堆顶的过期元素）',
        'right.push(-left.pop())': '`left.pop()` 取最大的，取反后放进 right',
        'heappop(self.heap)': '堆顶是待删除的元素 → 现在才真正弹出',
        'return ans': '所有窗口的中位数：`{ans}`',
    },
    cards=dict(
        one_liner='窗口里的数分成两半；要删的数先记账，等到了堆顶再真删',
        complexity='时间 `O(n log n)`（堆里有 O(n) 个元素），空间 `O(n)`',
        problem=['长为 `k` 的窗口从左滑到右，每次输出窗口的中位数',
                 '偶数个时取中间两数的平均',
                 '本视频：`nums = [1,3,-1,-3,5]`，`k = 3` → `[1,-1,-1]`'],
        quote='删除的时候，我们只记录「要删除一个值为 x 的数」，并不去「执行」删除操作。等到要出堆（或者查看堆顶）时才真正地执行删除操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['框架：定长滑窗「入 → 算 → 出」；入窗口和算中位数同 295 题的对顶堆',
              '出窗口的 `x` 在哪个堆？和 left 堆顶比：`x ≤ 堆顶` 在 left，否则在 right',
              '用 `remove_cnt` 懒删除，`size` 另记真实大小；删完看两堆大小，不平衡就挪一个'],
        summary=['时间 `O(n log n)`：堆里含未清理的元素，最多 O(n) 个；空间 `O(n)`',
                 '易错：堆的 `len` 不是真实大小，平衡两堆必须用 `size`',
                 '易错：`pop` / `top` 前要先 `apply_remove`，否则取到的是已删除的数',
                 '前置：295 数据流的中位数（对顶堆）；同类：离线用两个有序集合也行'],
    ),
)
