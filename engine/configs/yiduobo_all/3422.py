NUMS, K = [5, 1, 4, 2, 7, 3], 3


def _win(S):
    if 'del_dict' in S and 'index' in S:
        return S['index'] - S['k'] + 1
    return 0


def _winr(S):
    if 'del_dict' in S and 'index' in S:
        return S['index']
    return S['k'] - 1


def _cost_txt(S):
    if 'min_heap' not in S or not S['min_heap'] or 'res' not in S:
        return '`min_heap` 存相反数 → 堆顶是较小一半的==最大值==；`max_heap` 堆顶是较大一半的最小值'
    if 21 < S['_line'] < 65:
        return '维护中：堆里可能暂存已离开窗口的数（待 `del_dict` 清理），清理完才能读中位数'
    med = -S['min_heap'][0]
    c = S['min_size'] * med - S['s_min'] + S['s_max'] - S['max_size'] * med
    return (f'中位数 `{med}`：小堆 `{S["min_size"]}×{med} − {S["s_min"]}` + 大堆 `{S["s_max"]} − {S["max_size"]}×{med}` = =={c}==')


def _delta_why(S, B, ret):
    if S.del_num >= S.max_heap[0]:
        return f'`{S.del_num} >= max_heap[0] = {S.max_heap[0]}`：要移出的数在大堆 → 大堆少 1 个，`s_max` 减去它'
    return f'`{S.del_num} < max_heap[0] = {S.max_heap[0]}`：要移出的数在小堆 → 小堆少 1 个，`s_min` 减去它'


CONFIG = dict(
    num=3422, title='将子数组元素变为相等所需的最小操作数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='滑动窗口中位数（对顶堆 + 延迟删除）',
    tags=['堆', '滑动窗口'],
    code='''
class Solution(object):
    def minOperations(self, nums, k):
        
        min_heap = []
        max_heap = []
        s_min = 0
        s_max = 0
        max_size = k // 2
        min_size = k - max_size

        for num in nums[:k]:
            heapq.heappush(min_heap, -num)
            s_min += num

        for index in range(k // 2):
            heapq.heappush(max_heap, -min_heap[0])
            s_min += min_heap[0]
            s_max -= min_heap[0]
            heapq.heappop(min_heap)

        res = min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0])
        del_dict = {}
        for index in range(k, len(nums)):

            del_num = nums[index - k]
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
            
            res = min(res, min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0]))

        return res
''',
    call=f'Solution().minOperations({NUMS!r}, {K})',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前长度 k 的窗口）', cell=84, h=150, window=(_win, _winr)),
        dict(type='heap', var='min_heap', label='min_heap（存相反数；较小的一半）', fmt=lambda x: str(-x), top_color='blue', h=120),
        dict(type='heap', var='max_heap', label='max_heap（较大的一半）', top_color='pink', h=120),
        dict(type='text', h=70, size=26, fn=_cost_txt),
    ],
    watch=[('s_min', 's_min', 'blue'), ('s_max', 's_max', 'pink'), ('del_num', 'del_num', 'orange'), ('res', 'res', 'green')],
    skip=['s_min += num', 'del_dict[max_heap[0]] -= 1', 'del_dict[-min_heap[0]] -= 1', 's_min += add_num', 's_max += add_num', 'max_size = ', 'min_size = ', 's_min = 0', 's_max = 0', 'del_dict[del_num] =', 'delta = 0', 'delta = 1', 'delta = -1', 'delta -= 1', 'delta += 1'],
    captions={
        'min_heap = []': '小堆 `min_heap` 装较小的一半：Python 只有最小堆，所以==存相反数==，堆顶就是这一半的最大值',
        'max_heap = []': '大堆 `max_heap` 装较大的一半，堆顶是这一半的最小值；两堆顶就是中位数的位置',
        'for num in nums[:k]': '先把第一个窗口的 `k` 个数全放进 `min_heap`',
        'heapq.heappush(min_heap, -num)': '`{num}` 入小堆（存 `{-num}`），`s_min` 累加 `{num}`',
        'for index in range(k // 2)': '再把小堆里最大的 `k // 2` 个挪到大堆',
        'heapq.heappush(max_heap, -min_heap[0])': '小堆堆顶 `{-min_heap[0]}` 是最大的，挪到大堆',
        'res = min_size': '把窗口里所有数变成中位数 `{-min_heap[0]}` 的操作数：小堆 `{min_size}×{-min_heap[0]} − s_min` + 大堆 `s_max − {max_size}×{-min_heap[0]}` = =={res}==',
        'del_dict = {}': '`del_dict` 记下“待删除”的数：堆不能随机删，==延迟删除==，等它跑到堆顶再弹',
        'for index in range(k, len(nums))': lambda S, B, ret: (f'窗口右移：加入 `nums[{S.index}] = {S.nums[S.index]}`，移出 `nums[{S.index - S.k}] = {S.nums[S.index - S.k]}`' if S.get('index') is not None and S.index < len(S.nums) and S.get('del_num') is None or S.get('index') != B.get('index') else '窗口扫完'),
        'del_num = nums[index - k]': '要移出的数 `del_num = {del_num}`，先记进 `del_dict`',
        'if max_heap and del_num >= max_heap[0]': _delta_why,
        'add_num = nums[index]': '要加入的数 `add_num = {add_num}`',
        'if max_heap and add_num >= max_heap[0]': lambda S, B, ret: (f'`{S.add_num} >= max_heap[0] = {S.max_heap[0]}`：属于较大的一半 → 进大堆，`s_max` 加上它' if S.add_num >= S.max_heap[0] else f'`{S.add_num} < max_heap[0] = {S.max_heap[0]}`：属于较小的一半 → 进小堆，`s_min` 加上它'),
        'if delta > 0': lambda S, B, ret: (f'`delta = {S.delta}`：小堆多了 1 个、大堆少了 1 个 → 把小堆最大的挪给大堆' if S.delta > 0 else f'`delta = {S.delta}`：小堆没有多出来，看下一个分支'),
        'elif delta < 0': lambda S, B, ret: (f'`delta = {S.delta}`：大堆多了 1 个、小堆少了 1 个 → 把大堆最小的挪回小堆' if S.delta < 0 else '`delta = 0`：出一个进一个都在同一边，两堆个数合规，不用挪'),
        'heapq.heappush(min_heap, -max_heap[0])': '大堆最小的 `{max_heap[0]}` 挪回小堆（存 `{-max_heap[0]}`）',
        19: '小堆最大的已挪走，把它从小堆弹出；小堆 `k - k//2` 个，大堆 `k//2` 个',
        50: '小堆最大的已挪给大堆，从小堆弹出它（`s_min`、`s_max` 同步调整过）',
        55: '大堆最小的已挪回小堆，从大堆弹出它',
        59: '弹出这个已离开窗口的数',
        63: '弹出这个已离开窗口的数',
        'while max_heap and': lambda S, B, ret: (f'大堆顶 `{S.max_heap[0]}` 在 `del_dict` 里还欠着删除 → 真正弹出' if S.max_heap and S.del_dict.get(S.max_heap[0], 0) > 0 else '大堆顶没有待删，停止清理'),
        'while min_heap and': lambda S, B, ret: (f'小堆顶 `{-S.min_heap[0]}` 在 `del_dict` 里还欠着删除 → 真正弹出' if S.min_heap and S.del_dict.get(-S.min_heap[0], 0) > 0 else '小堆顶没有待删，停止清理；中位数 = 小堆堆顶'),
        'del_dict[max_heap[0]] -= 1': '`del_dict` 的欠账减一',
        'del_dict[-min_heap[0]] -= 1': '`del_dict` 的欠账减一',
        'res = min(res': lambda S, B, ret: (f'当前窗口的操作数 =={S.min_size * (-S.min_heap[0]) - S.s_min + S.s_max - S.max_size * (-S.min_heap[0])}==，' + (f'`res` {B.res} → =={S.res}==' if S.res != B.res else f'不比 `res = {S.res}` 小')),
        'return res': '最少操作数 `{res}`',
    },
    max_steps=85,
    cards=dict(
        one_liner='窗口里全变成中位数最省：用两个堆维护滑动窗口中位数',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['每次可以把一个元素 `+1` 或 `-1`，要让 `nums` 里有一个长为 `k` 的子数组==元素全相等==',
                 '求最少操作次数',
                 '本视频：`nums = [5,1,4,2,7,3]`，`k = 3` → `3`'],
        quote='对于一个数组arr，将arr中所有元素都变为相等的最优方案就是将所有元素都变为arr的中位数。',
        quote_src='—— yiduobo 题解原文',
        idea=['只需考察每个长 `k` 的窗口，操作数 = 全变成该窗口的中位数的代价',
              '两堆各存一半，再维护两堆元素之和：小堆代价 `n×中位数 − s_min`，大堆 `s_max − n×中位数`',
              '堆不能随机删除 → `del_dict` 记账，等到堆顶再弹（同 480 题）'],
        summary=['时间 `O(n log k)`，空间 `O(n)`',
                 '`min_heap` 存相反数，`s_min` 却存真实值，别混淆',
                 '`delta` 记录两堆个数的变化，之后统一挪一个数来平衡',
                 '弹出堆顶时才处理 `del_dict`：堆里可能暂存已离开窗口的数',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
