def _info(S):
    if 'min_heap' not in S or 's' not in S:
        return '窗口大小 `dist + 1`，求窗口内最小的 `k` 个数之和（k 已减 1）'
    live = [x for x in S['max_heap'] if S['del_dict'].get(x, 0) == 0]
    return f'小数堆（最小的 k 个）和 `s = {S["s"]}`　总代价 = nums[0] + s = ==​{S["nums"][0] + S["s"]}==　当前最优 `res = {S["res"]}`'


CONFIG = dict(
    num=3013, title='将数组分成最小总代价的子数组 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='滑动窗口 · 小数堆 + 大数堆 + 懒删除',
    tags=['常用数据结构', '常用数据结构', '难度分 2540'],
    code='''
class Solution(object):
    def minimumCost(self, nums, k, dist):

        min_heap = []
        max_heap = []
        k -= 1
        for num in nums[1: 1 + dist + 1]:
            heapq.heappush(max_heap, num)

        for index in range(k):
            heapq.heappush(min_heap, -max_heap[0])
            heapq.heappop(max_heap)

        s = nums[0] - sum(min_heap)
        res = s

        del_dict = Counter()

        for index in range(1 + dist + 1, len(nums)):
            del_num = nums[index - dist - 1]
            del_dict[del_num] += 1

            delta = 0
            if max_heap and del_num >= max_heap[0]:
                delta = 1
            else:
                delta = -1
                s -= del_num

            add_num = nums[index]
            if max_heap and add_num >= max_heap[0]:
                heapq.heappush(max_heap, add_num)
                delta -= 1
            else:
                heapq.heappush(min_heap, -add_num)
                s += add_num
                delta += 1
            
            if delta > 0:
                heapq.heappush(max_heap, -min_heap[0])
                s += min_heap[0]
                heapq.heappop(min_heap)
            elif delta < 0:
                heapq.heappush(min_heap, -max_heap[0])
                s += max_heap[0]
                heapq.heappop(max_heap)

            while max_heap and del_dict.get(max_heap[0], 0) > 0:
                del_dict[max_heap[0]] -= 1
                heapq.heappop(max_heap)

            while min_heap and del_dict.get(-min_heap[0], 0) > 0:
                del_dict[-min_heap[0]] -= 1
                heapq.heappop(min_heap)
            res = min(res, s)

        return res
''',
    call='Solution().minimumCost([2,5,3,8,1,4,6,2], 3, 3)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（框 = 滑动窗口）', h=215,
             pointers={'index': 'blue'},
             window=(lambda S: max(1, S['index'] - 3) if 'index' in S and S['index'] >= 5 else None, 'index'),
             dim=lambda S, i, v: i == 0),
        dict(type='heap', var=lambda S: [-x for x in S['min_heap']] if 'min_heap' in S else [], label='min_heap 小数堆（真实值）', top_color='blue', h=125),
        dict(type='heap', var='max_heap', label='max_heap 大数堆（含失效元素）', top_color='pink', h=125),
        dict(type='map', var='del_dict', label='del_dict 待删除计数', h=100),
        dict(type='text', fn=_info, size=24, h=80),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'green'), ('res', 'res', 'orange'), 'delta'],
    skip=['del_num = nums', 'delta = 1', 'delta = -1', 'delta -= 1', 'delta += 1', 'for num in nums[1:', 'for index in range(k)', 'min_heap = []', 'max_heap = []', 'delta = 0', 'del_dict = Counter()'],
    captions={
        'k -= 1': '第一段的代价 `nums[0]` 固定，还要再选 `k-1 = {k}` 个段首：`k` 减一',
        8: '窗口大小 `dist + 1`：先把 `nums[1..dist+1]` 的数逐个放进大数堆',
        11: '再把大数堆里最小的 `k` 个逐个挪进小数堆：大数堆最小的 `{max_heap[0]}` 放进小数堆（存负数，==小数堆堆顶是它们的最大值==）',
        's = nums[0] - sum(min_heap)': '初始 `s = nums[0] + 小数堆之和 = {s}`：第一个窗口的代价',
        'res = s': '`res = {res}`：先记下第一个窗口的答案',
        'for index in range(1 + dist + 1': '窗口右移：`index = {index}` 进入窗口，左边出去的元素要懒删除',
        'del_dict[del_num] += 1': '离开窗口的是 `nums[{index} − dist − 1] = {del_num}`。堆不能直接删中间元素 → 先在 `del_dict` 记一笔：欠删 {del_dict[del_num]} 次',
        'if max_heap and del_num >= max_heap[0]': lambda S, B, r: (
            f'`{S.del_num} ≥ 大数堆顶 {S.max_heap[0]}` → 删的在大数堆里，小数堆相对多 1：`delta = 1`（`delta` 记小数堆相对多几个）'
            if S.max_heap and S.del_num >= S.max_heap[0] else
            f'`{S.del_num}` 比大数堆顶小 → 删的在小数堆里，小数堆相对少 1：`delta = −1`'),
        's -= del_num': '小数堆之和 `s` 立刻减去 `{del_num}` → {s}',
        'add_num = nums[index]': '新进入窗口的是 `{add_num}`',
        'if max_heap and add_num >= max_heap[0]': lambda S, B, r: (
            f'`{S.add_num} ≥ 大数堆顶 {S.max_heap[0]}` → 新数属于大数堆'
            if S.max_heap and S.add_num >= S.max_heap[0] else f'`{S.add_num}` 比大数堆顶小 → 新数属于小数堆'),
        'heapq.heappush(max_heap, add_num)': '新数进大数堆：小数堆相对少 1，`delta` 减一',
        'heapq.heappush(min_heap, -add_num)': '新数进小数堆（存负数）',
        's += add_num': '新数进小数堆：`delta` 加一；小数堆多了 `{add_num}`，`s` → {s}',
        'if delta > 0': lambda S, B, r: (f'`delta = {S.delta} > 0`：小数堆多出来了，要把它最大的挪给大数堆' if S.delta > 0 else f'`delta = {S.delta}` 不大于 0'),
        'heapq.heappush(max_heap, -min_heap[0])': '小数堆最大的 `{-min_heap[0]}` 挪去大数堆',
        's += min_heap[0]': '`min_heap[0]` 是负数，所以这是从 `s` 里减去被挪走的数 → {s}',
        'elif delta < 0': lambda S, B, r: (f'`delta = {S.delta} < 0`：小数堆少了，要从大数堆补一个最小的过来' if S.delta < 0 else f'`delta = {S.delta}`：两堆已平衡，不用挪'),
        44: '大数堆最小的 `{max_heap[0]}` 补进小数堆（存负数）',
        's += max_heap[0]': '补进来的数加到 `s` → {s}（注意：这里用的是堆顶，失效元素稍后再清）',
        'while max_heap and del_dict': lambda S, B, r: (
            f'大数堆顶 `{S.max_heap[0]}` 欠删 `{S.del_dict.get(S.max_heap[0], 0)}` 次 → 是失效元素，弹掉' if S.max_heap and S.del_dict.get(S.max_heap[0], 0) > 0
            else '大数堆顶没有失效，停止清理'),
        'del_dict[max_heap[0]] -= 1': '销账：欠删次数减一。==弹失效元素不再改 `s`==',
        'while min_heap and del_dict': lambda S, B, r: (
            f'小数堆顶 `{-S.min_heap[0]}` 欠删 `{S.del_dict.get(-S.min_heap[0], 0)}` 次 → 失效，弹掉' if S.min_heap and S.del_dict.get(-S.min_heap[0], 0) > 0
            else '小数堆顶没有失效，停止清理'),
        'del_dict[-min_heap[0]] -= 1': '销账：欠删次数减一',
        'res = min(res, s)': '`res = min({B.res}, {s}) = {res}`：窗口内最小 k 个数之和 + `nums[0]` 即这个窗口的最小总代价',
        'return res': '最小总代价 `{res}`',
    },
    cards=dict(
        one_liner='窗口内最小的 k 个数之和：小数堆 + 大数堆 + 懒删除',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把数组分成 `k` 段，第 2 段与第 `k` 段的段首下标相差不超过 `dist`，代价 = 各段第一个数之和',
                 '`nums[0]` 必选；要再选 `k-1` 个段首，且都落在长为 `dist+1` 的窗口内',
                 '本视频：`[2,5,3,8,1,4,6,2]`，`k=3`，`dist=3` → `5`'],
        quote='本题实际上就是给出一个大小为dist + 1的滑动窗口，问窗口内最小的k个数之和是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['窗口大小固定 `dist+1`，用 480 题的两个堆：小数堆装最小的 `k` 个，其余在大数堆',
              '变量 `s` 记小数堆之和，答案 = `nums[0] + s` 的最小值',
              '堆不好删中间元素 → 用 `del_dict` 懒删除，==弹出失效元素时不再改 `s`=='],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`delta` 记录“删一个、加一个”后两堆个数的偏差，再挪一次就能恢复平衡',
                 '易错点：失效元素在堆顶时才清理，且清理时不能再动 `s`',
                 '原文本身可在 Python 3 运行，未做修改；`min_heap` 存的是负数',
                 '前置题：480 滑动窗口中位数、3010'],
    ),
)
