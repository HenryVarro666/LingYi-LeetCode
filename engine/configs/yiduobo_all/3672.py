NUMS = [1, 2, 2, 3, 1, 1]


def _wlo(S):
    if 'index' in S:
        return S['index'] + 1
    return 0 if 'freq' in S else None


def _whi(S):
    if 'index' in S:
        return S['index'] + S['k']
    return S['k'] - 1 if 'freq' in S else None


def _top(S):
    h = S.get('heap')
    if not h:
        return '堆里存 `(−次数, 值)`：堆顶 = 次数最多、值最小的那个'
    f, v = -h[0][0], h[0][1]
    ok = S['freq'].get(v) == f
    return f'堆顶 `({h[0][0]}, {v})` → 众数 `{v}` 出现 `{f}` 次，权重 `{v}×{f} = {v * f}`' + ('' if ok else '（已过期，要弹掉）')


CONFIG = dict(
    num=3672, title='子数组中加权众数的总和', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='滑窗众数 · 哈希表 + 堆懒删除',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def modeWeight(self, nums, k):
        
        heap = []
        freq = {}
        for v in nums[:k]:
            freq[v] = freq.get(v, 0) + 1
        
        for v in freq:
            heapq.heappush(heap, (-freq[v], v))
        
        res = -heap[0][0] * heap[0][1]
        for index, v in enumerate(nums[k:]):
            if nums[index] != v:
                freq[nums[index]] -= 1
                if freq[nums[index]] > 0:
                    heapq.heappush(heap, (-freq[nums[index]], nums[index]))
                freq[v] = freq.get(v, 0) + 1
                heapq.heappush(heap, (-freq[v], v))
                while freq[heap[0][1]] != -heap[0][0]:
                    heapq.heappop(heap)

            res += -heap[0][0] * heap[0][1]
        
        return res
''',
    call=f'Solution().modeWeight({NUMS!r}, 3)',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前长为 k 的窗口）', cell=100, h=190,
             window=(_wlo, _whi)),
        dict(type='map', var='freq', label='freq（窗口内各值出现次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=34),
        dict(type='heap', var='heap', label='heap（元素 = (−次数, 值)，可能含过期项）', fmt=lambda x: f'({x[0]},{x[1]})', h=170),
        dict(type='text', h=80, size=28, fn=_top),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'heap = []': '`heap` 找众数：存 `(−次数, 值)`，最小堆的堆顶就是==次数最多、同次数时值最小==',
        'freq = {}': '`freq` 记录窗口内每个值的次数',
        'for v in nums[:k]': '先统计第一个窗口里每个值的次数',
        'freq[v] = freq.get(v, 0) + 1': lambda S, B, r: f'`{S.v}` 计数加一：`freq[{S.v}] = {S.freq[S.v]}`' if 'index' not in S else f'移入的 `{S.v}` 次数加一：`freq[{S.v}] = {S.freq[S.v]}`',
        'for v in freq': '把窗口里每种值以 `(−次数, 值)` 压进堆',
        'heapq.heappush(heap, (-freq[v], v))': lambda S, B, r: f'压入 `({-S.freq[S.v]}, {S.v})`，堆顶是 `{S.heap[0]}`' if 'index' not in S else f'压入新次数 `({-S.freq[S.v]}, {S.v})`',
        'res = -heap': '第一个窗口的权重 = 众数 × 次数 = `{-heap[0][0]} × {heap[0][1]}`，`res = {res}`',
        'for index, v in enumerate': lambda S, B, r: (f'窗口右移：`nums[{S.index}] = {S.nums[S.index]}` 移出，`{S.v}` 移入' if not ('index' in B and S.index == B.index) else '没有更多元素了，窗口扫完'),
        'if nums[index] != v': lambda S, B, r: (f'移出的 `{S.nums[S.index]}` ≠ 移入的 `{S.v}`：次数有变化，要更新' if S.nums[S.index] != S.v
                                                else f'移出和移入都是 `{S.v}`：次数不变，堆顶就是答案，==不用动=='),
        'freq[nums[index]] -= 1': '移出的值次数减一：`freq[{nums[index]}] = {freq[nums[index]]}`（堆里旧记录先不删，懒更新）',
        'if freq[nums[index]] > 0': lambda S, B, r: (f'还剩 `{S.freq[S.nums[S.index]]}` 次 > 0：把新次数压入堆' if S.freq[S.nums[S.index]] > 0
                                                       else '次数已经为 0：它不在窗口里了，不用再压入'),
        'heapq.heappush(heap, (-freq[nums[index]], nums[index]))': '压入 `({-freq[nums[index]]}, {nums[index]})`',
        'heapq.heappush(heap, (-freq[v], v))': '压入 `({-freq[v]}, {v})`',
        'while freq[heap[0][1]] != -heap[0][0]': lambda S, B, r: (f'堆顶 `{S.heap[0]}` 的次数与 `freq[{S.heap[0][1]}] = {S.freq[S.heap[0][1]]}` 不一致 → ==过期记录==，弹掉'
                                                                 if S.freq[S.heap[0][1]] != -S.heap[0][0]
                                                                 else f'堆顶 `{S.heap[0]}` 与 `freq` 一致 → 是有效的，众数确定'),
        'heapq.heappop(heap)': '弹出过期记录，堆顶现在是 `{heap[0]}`',
        'res += -heap[0][0] * heap[0][1]': '这个窗口的权重 `{heap[0][1]} × {-heap[0][0]} = {-heap[0][0] * heap[0][1]}`，`res = {res}`',
        'return res': '所有窗口权重之和 =={res}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='滑窗众数：哈希表数次数，堆顶取众数，过期项懒删除',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['对每个长为 `k` 的子数组：权重 = 众数 × 它的出现次数',
                 '出现次数相同时，众数取最小的那个',
                 '求所有长为 `k` 子数组的权重之和',
                 '本视频：`nums=[1,2,2,3,1,1], k=3` → `11`'],
        quote='题目实际上要计算的就是滑动窗口的众数，……只需要使用一个哈希表记录窗口内每种元素出现的次数，另外使用一个堆，使用懒更新的策略来维护窗口中的这些元素以及出现次数就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`freq` 记窗口里每个值的次数；堆里放 `(−次数, 值)`',
              '最小堆的堆顶：次数最大，次数相同取值最小，正好是题目要的众数',
              '窗口滑动时只压入新记录，旧记录==留在堆里==；堆顶与 `freq` 对不上就弹掉'],
        summary=['时间 `O(n log n)`（每步最多压入 2 项），空间 `O(n)`',
                 '移出和移入相同的值时次数不变，直接跳过更新',
                 '易错：堆顶过期要用 `while` 弹到有效为止；次数为 0 的值不用再压入',
                 '原文用了 `heapq`，是 Python 2/3 通用写法，除空行外未作改动',
                 '同类：滑动窗口中位数 480（双堆 + 懒删除）'],
    ),
)
