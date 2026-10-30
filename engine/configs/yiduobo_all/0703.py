def _sorted(S):
    h = S.get('self.heap')
    if h is None:
        return ''
    top = f"，堆顶 =={h[0]}== 就是第 k 大" if len(h) == S.get('self.k', -1) else ''
    return f"堆里的数从小到大：`{sorted(h)}`{top}"


def _cmp_init(S, B, r):
    t, x = S['self.heap'][0], S.nums[S.index]
    if t < x:
        return f'堆顶 `{t} < nums[{S.index}] = {x}`：`{x}` 能挤进前 k 大 → ==踢掉堆顶=='
    return f'堆顶 `{t} ≥ nums[{S.index}] = {x}`：`{x}` 进不了前 k 大，跳过'


def _len(S, B, r):
    n, k = len(S['self.heap']), S['self.k']
    if n < k:
        return f'add({S.val})：堆里只有 `{n} < k = {k}` 个，==直接加入=='
    return f'add({S.val})：堆已满 `{k}` 个，要和堆顶比一比'


def _cmp_add(S, B, r):
    t = S['self.heap'][0]
    if t < S.val:
        return f'堆顶 `{t} < {S.val}`：`{S.val}` 比当前第 k 大还大 → ==替换堆顶=='
    return f'堆顶 `{t} ≥ {S.val}`：`{S.val}` 排不进前 k 大，==什么都不做=='


CONFIG = dict(
    num=703, title='数据流中的第K大元素', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='大小为 k 的最小堆',
    tags=['labuladong', '灵神核心路线'],
    code='''
import heapq
class KthLargest(object):

    def __init__(self, k, nums):
        self.heap = nums[:k]
        self.k = k
        heapq.heapify(self.heap)
        for index in range(k, len(nums)):
            if self.heap[0] < nums[index]:
                heapq.heappop(self.heap)
                heapq.heappush(self.heap, nums[index])

    def add(self, val):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif self.heap[0] < val:
            heapq.heappop(self.heap)
            heapq.heappush(self.heap, val)

        return self.heap[0]
''',
    call='''obj = KthLargest(3, [4, 5, 8, 2])
[obj.add(3), obj.add(5), obj.add(10), obj.add(9), obj.add(4)]''',
    expect=[4, 5, 5, 8, 8],
    views=[
        dict(type='text', fn=_sorted, size=26, h=60),
        dict(type='array', var=lambda S: S.get('nums') or [4, 5, 8, 2], label='初始 nums（蓝 = index；add 阶段变暗）',
             pointers={'index': 'blue'}, dim=lambda S, i, v: 'nums' not in S, cell=84, h=170),
        dict(type='heap', var='self.heap', label='self.heap 最小堆（只留前 k 大）', top_color='pink', h=200),
    ],
    watch=[('k', lambda S: S.get('self.k'), 'purple'), ('val', 'val', 'orange'),
           ('堆顶', lambda S: S['self.heap'][0] if S.get('self.heap') else None, 'pink')],
    captions={
        'self.heap = nums[:k]': '先拿前 `k` 个数 `{self.heap}` 当作候选的“前 k 大”',
        'heapq.heapify': '建成==最小堆==：堆顶是这 k 个里最小的，也就是第 k 大',
        'if self.heap[0] < nums[index]': _cmp_init,
        'if len(self.heap) < self.k': _len,
        'heapq.heappush(self.heap, val)': '`{val}` 入堆 → `{self.heap}`',
        'elif self.heap[0] < val': _cmp_add,
        'return self.heap[0]': '返回堆顶 =={ret}==：当前第 `{self.k}` 大',
    },
    skip=['self.k = k', 'heapq.heappop(self.heap)'],
    cards=dict(
        one_liner='用大小为 k 的最小堆存前 k 大，堆顶就是第 k 大',
        complexity='每次 add `O(log k)`，初始化 `O(n log k)`，空间 `O(k)`',
        problem=['设计 `KthLargest(k, nums)`：数据流初始为 `nums`',
                 '`add(val)` 加入一个数，并返回当前数据流中==第 k 大==的元素（排序后，可重复）',
                 '示例：`k = 3, nums = [4,5,8,2]`，依次 add `3,5,10,9,4` → `[4,5,5,8,8]`'],
        quote='对于第k大或者第k小这类问题，经典的做法就是维护一个大小为k的堆来储存当前前k大或者前k小的元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['堆不满 k 个：新数直接加入',
              '堆满了且==堆顶 < 新数==：弹出堆顶，再放入新数；否则什么都不做',
              '每轮之后堆里有 k 个数时，堆顶就是第 k 大'],
        summary=['add `O(log k)`，空间只需 `O(k)`，不用存整个数据流',
                 '求第 k ==大== 用==最小==堆：堆顶是“门槛”，比它小的数永远进不来',
                 '初始 `nums` 可能不足 k 个，所以 `add` 里要先判断 `len < k`',
                 '原文为 Python 2 风格（`class KthLargest(object)`），代码未改动'],
    ),
)
