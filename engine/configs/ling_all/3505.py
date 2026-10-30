from collections import Counter as _Cn


def _items(h):
    if h is None or not hasattr(h, 'heap'):
        return None
    c = _Cn(h.heap)
    for v, cnt in h.remove_cnt.items():
        if cnt > 0 and v in c:
            c[v] = max(0, c[v] - cnt)
    return sorted(c.elements())


def _draw_heaps(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    left, right = S.get('left'), S.get('right')
    Ls, Rs = _items(left), _items(right)
    if Ls is None or Rs is None:
        cv.text((x0 + 18, y0 + 6), '对顶堆（left 最大堆 + right 最小堆）在滑动窗口阶段使用', 22, T['muted'], bold=True)
        return
    Ls = sorted(-v for v in Ls)
    cv.text((x0 + 18, y0 + 16), '把窗口排好序：left（较小的一半，堆顶=中位数）| right（较大的一半）', 21, T['muted'], bold=True)
    cell, gap = 54, 30
    total = (len(Ls) + len(Rs)) * cell + gap
    xs = x0 + (x1 - x0 - total) / 2
    y = y0 + 48
    for k, v in enumerate(Ls):
        top = k == len(Ls) - 1
        cv.rect((xs + 3, y, xs + cell - 3, y + cell - 6), fill=T['blue'], r=8,
                outline=T['yellow'] if top else None, width=4 if top else 1)
        cv.text((xs + cell / 2, y + (cell - 6) / 2), v, 26, T['bg'], anchor='mm', bold=True)
        xs += cell
    dx = xs + gap / 2
    cv.line([(dx, y - 8), (dx, y + cell)], T['muted'], 3)
    xs += gap
    for k, v in enumerate(Rs):
        cv.rect((xs + 3, y, xs + cell - 3, y + cell - 6), fill=T['pink'], r=8)
        cv.text((xs + cell / 2, y + (cell - 6) / 2), v, 26, T['bg'], anchor='mm', bold=True)
        xs += cell
    ly = y + cell + 0
    cv.text((x0 + 20, ly), f'left 和 = {left.sum * -1}（{len(Ls)} 个）', 20, T['blue'], bold=True)
    cv.text((x1 - 20, ly), f'right 和 = {right.sum}（{len(Rs)} 个）', 20, T['pink'], anchor='rt', bold=True)


def _dis_var(S):
    d = S.get('dis')
    return d if d is not None else S.get('ans')


def _w1(S):
    return S.get('i') if 'ans' in S and 'dis' not in S else None


def _w0(S):
    if 'ans' in S and 'dis' not in S and 'l' in S and S['l'] >= 0:
        return S['l']
    return None


def _fcolor(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if 'dis' not in S or i is None or j is None or 'x' not in S:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i, j - 1), (i - 1, j - S['x'])):
        return 'blue'
    return None


def _cap_push(S, B, ret):
    return None


def _cap_ans(S, B, ret):
    l = S.l
    return (f'窗口 `[{l}, {S.i}]` 中位数 `v = {S.v}`：left 里每个数差 `v−x`，right 里每个数差 `x−v`，'
            f'两边之和 `{S.s1} + {S.s2}` → ==`dis[{l}] = {S.ans[l]}`==')


SKIP = list(range(1, 48)) + [53, 59, 55, 57, 64, 65, 66, 69, 70, 71, 75, 77, 78, 81, 82, 88, 93]


def _cap_leave(S, B, ret):
    its = _items(S.left)
    top = -min(its) if its else None
    X = S.nums[S.l]
    if top is not None and X <= top:
        return f'窗口左端 `{X}` 要离开：`{X} <= left 堆顶 {top}` → 它在 ==left== 里，懒删除（堆里存的是 `{-X}`），必要时从 right 补一个'
    return f'窗口左端 `{X}` 要离开：`{X} > left 堆顶 {top}` → 它在 ==right== 里，懒删除，必要时从 left 挪一个给 right'


def _cap_f(S, B, ret):
    i, j, x = S.i, S.j, S.x
    a, b, d = S.f[i][j - 1], S.f[i - 1][j - x], S.dis[j - x]
    return (f'前 `{j}` 个数选 `{i}` 个窗口：不选末尾 `f[{i}][{j - 1}] = {a}`，'
            f'选 `[{j - x}, {j - 1}]`：`f[{i - 1}][{j - x}] + dis[{j - x}] = {b} + {d}`；取小 → ==`f[{i}][{j}] = {S.f[i][j]}`==')


CAPS = {
    54: '两个堆：`left` 最大堆（存相反数）放较小一半，`right` 最小堆放较大一半；堆顶就是中位数',
    60: '`left.size == right.size`：`{nums[i]}` 先进 right，right 最小的数再挪进 left → left 多一个，中位数是 left 堆顶',
    62: '`left` 比 `right` 多一个：`{nums[i]}` 先进 left，left 最大的数挪进 right → 两边一样大',
    72: _cap_ans,
    76: _cap_leave,
    79: 'left 比 right 少了 → 从 right 弹出最小的补给 left，保持 left 大小 = right 或 right+1',
    83: 'left 比 right 多太多 → 从 left 弹出最大的给 right，重新平衡',
    89: lambda S, B, r: ('先调用滑窗中位数：算出每个长 `x` 窗口变成中位数的操作数 `dis`' if 'dis' not in S else f'`dis[l]` = 以 `l` 为左端点的长 `x` 窗口变成中位数的操作数：`{S.dis}`'),
    90: '`f[i][j]`：前 `j` 个数里选 `i` 个长 `x` 的窗口，最少操作数；`f[0][j] = 0`',
    91: lambda S, B, r: (f'开始选第 `{S.i}` 个窗口' if B.get('i') != S.i else '`k` 个窗口都选完了'),
    92: '`f[{i}][{i * x - 1}] = inf`：前 `{i * x - 1}` 个数放不下 `{i}` 个长 `{x}` 的窗口',
    94: _cap_f,
    95: '`f[k][n]`：全部 `n` 个数里选 `k` 个窗口 → =={ret}==',
}


CONFIG = dict(
    num=3505, title='使 K 个子数组内元素相等的最少操作数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='对顶堆滑窗中位数 + 划分型 DP',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class LazyHeap:
    def __init__(self):
        self.heap = []
        self.remove_cnt = defaultdict(int)  # 每个元素剩余需要删除的次数
        self.size = 0  # 实际大小
        self.sum = 0  # 堆中元素总和

    # 删除
    def remove(self, x: int) -> None:
        self.remove_cnt[x] += 1  # 懒删除
        self.size -= 1
        self.sum -= x

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
        self.sum -= self.heap[0]
        return heappop(self.heap)

    # 入堆
    def push(self, x: int) -> None:
        if self.remove_cnt[x] > 0:
            self.remove_cnt[x] -= 1  # 抵消之前的删除
        else:
            heappush(self.heap, x)
        self.size += 1
        self.sum += x

    # push(x) 然后 pop()
    def pushpop(self, x: int) -> int:
        self.apply_remove()
        if not self.heap or x <= self.heap[0]:
            return x
        self.sum += x - self.heap[0]
        return heappushpop(self.heap, x)

class Solution:
    # 480. 滑动窗口中位数（有改动）
    # 返回 nums 的所有长为 k 的子数组的（到子数组中位数的）距离和
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        ans = [0] * (len(nums) - k + 1)
        left = LazyHeap()  # 最大堆（元素取反）
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
            v = -left.top()
            s1 = v * left.size + left.sum  # sum 取反
            s2 = right.sum - v * right.size
            ans[l] = s1 + s2

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

    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        dis = self.medianSlidingWindow(nums, x)
        f = [[0] * (n + 1) for _ in range(k + 1)]
        for i in range(1, k + 1):
            f[i][i * x - 1] = inf
            for j in range(i * x, n - (k - i) * x + 1):  # 左右留出足够空间给其他子数组
                f[i][j] = min(f[i][j - 1], f[i - 1][j - x] + dis[j - x])  # j-x 为子数组左端点
        return f[k][n]
''',
    call='Solution().minOperations([9, -2, -2, -2, 1, 5], 2, 2)',
    expect=3,
    skip=SKIP,
    views=[
        dict(type='array', var='nums', label='nums', window=(_w0, _w1), h=120, cell=62),
        dict(type='custom', draw=_draw_heaps, h=170),
        dict(type='array', var=_dis_var, label='dis[l]：窗口 [l, l+x) 变成中位数的操作数（ans）', h=110, cell=62),
        dict(type='table', var='f', label='f[i][j]：前 j 个数里选 i 个长 x 的子数组', color=_fcolor, h=230, cell=62),
    ],
    watch=[('i', 'i', 'blue'), 'l', 'v', 'j'],
    captions=CAPS,
    cards=dict(
        one_liner='窗口内变成中位数最省；对顶堆算距离和，再做划分型 DP',
        complexity='时间 `O(n log n + (n−kx)k)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，每次操作可把一个数加 1 或减 1',
                 '要得到至少 `k` 个==长度恰好为 `x`、互不重叠==的子数组，且每个子数组内元素全相等',
                 '示例：`nums=[9,-2,-2,-2,1,5], x=2, k=2` → `3`'],
        quote='把所有数都变成数组的中位数是最优的。……需要额外维护堆中元素之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定长滑窗 + ==对顶堆==（`left` 最大堆、`right` 最小堆）维护窗口中位数，同时维护两堆的和',
              '都变成中位数 `v`：`v·|left| − left.sum + right.sum − v·|right|`，结果记在窗口左端点 `dis[l]`',
              '划分型 DP：`f[i][j] = min(f[i][j−1], f[i−1][j−x] + dis[j−x])`——不选 / 选以 `j−1` 结尾的窗口'],
        summary=['时间 `O(n log n + (n−kx)k)`，空间 `O(n)`；懒删除堆让滑窗里的删除也是 `O(log n)`',
                 '初始值 `f[0][j] = 0`，`f[i][i·x−1] = inf`；`j` 的范围要给后面的子数组留出 `(k−i)·x` 的空间',
                 '题解还给出滚动数组的空间优化写法，转移完全一样',
                 '本视频跳过了 `LazyHeap` 内部逐行执行，只看窗口与两个堆的变化'],
    ),
)
