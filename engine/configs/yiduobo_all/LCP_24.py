def _info(S):
    if 's_first' not in S or 'num' not in S:
        return '先让 nums[index] −= index，问题变成「全部变成同一个 x」'
    f, g = S['first_heap'], S['second_heap']
    if not g:
        return f'小堆和 `s_first = {S["s_first"]}`　大堆和 `s_second = {S["s_second"]}`'
    if len(g) > len(f):
        t = g[0]
        how = f'大堆多一个 → x = 大堆顶 = {t}'
    elif f:
        t = (-f[0] + g[0]) // 2
        how = f'一样多 → x = 两堆顶的中间 = {t}'
    else:
        return ''
    return f'`s_first = {S["s_first"]}`　`s_second = {S["s_second"]}`　{how}'


CONFIG = dict(
    num='LCP 24', title='数字游戏', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='减下标 + 大小堆求中位数',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution(object):
    def numsGame(self, nums):

        n = len(nums)
        for index in range(n):
            nums[index] -= index
        
        first_heap = []
        second_heap = []
        s_first = 0
        s_second = 0
        res = []
        mod = 10 ** 9 + 7
        for num in nums:
            if not first_heap:
                if not second_heap:
                    heapq.heappush(second_heap, num)
                    s_second = num
                else:
                    if second_heap[0] < num:
                        min_of_second = heapq.heappop(second_heap)
                        s_second -= min_of_second
                        num, min_of_second = min_of_second, num
                        heapq.heappush(second_heap, min_of_second)
                        s_second += min_of_second
                    heapq.heappush(first_heap, -num)
                    s_first += num
            else:
                if num >= second_heap[0]:
                    if len(first_heap) < len(second_heap):
                        min_of_second = heapq.heappop(second_heap)
                        s_second -= min_of_second
                        heapq.heappush(first_heap, -min_of_second)
                        s_first += min_of_second
                    heapq.heappush(second_heap, num)
                    s_second += num

                elif num <= -first_heap[0]:
                    if len(first_heap) == len(second_heap):
                        max_of_first = heapq.heappop(first_heap)
                        s_first += max_of_first
                        heapq.heappush(second_heap, -max_of_first)
                        s_second -= max_of_first
                    heapq.heappush(first_heap, -num)
                    s_first += num

                else:
                    if len(first_heap) < len(second_heap):
                        heapq.heappush(first_heap, -num)
                        s_first += num
                    else:
                        heapq.heappush(second_heap, num)
                        s_second += num

            if len(second_heap) > len(first_heap):
                target = second_heap[0]
            else:
                target = (-first_heap[0] + second_heap[0]) // 2
            
            res.append((s_second - len(second_heap) * target + len(first_heap) * target - s_first) % mod)
        
        return res
''',
    call='Solution().numsGame([1,1,1,2,3,4])',
    expect=[0, 1, 2, 3, 3, 3],
    views=[
        dict(type='array', var='nums', label='nums（已减去下标）', h=150),
        dict(type='heap', var=lambda S: [-x for x in S['first_heap']] if 'first_heap' in S else [], label='first_heap 小值堆（真实值）', top_color='blue', h=130),
        dict(type='heap', var='second_heap', label='second_heap 大值堆', top_color='pink', h=130),
        dict(type='array', var='res', label='res', h=165),
        dict(type='text', fn=_info, size=24, h=90),
    ],
    watch=[('num', 'num', 'orange'), ('s_first', 's_first', 'blue'), ('s_second', 's_second', 'pink'), 'target'],
    skip=['for index in range(n)', 'nums[index] -= index', 'n = len', 'first_heap = []', 'second_heap = []', 's_first = 0', 's_second = 0', 'res = []', 'mod = ', 18, 'if not first_heap', 'if not second_heap'],
    captions={
        14: lambda S, B, r: ('开头已把每个 `nums[index]` 减去 `index`（目标 `x, x+1, …` 变成都等于 `x`）。现在逐个放进两个堆，保持：小值堆的数 ≤ 大值堆的数，个数差不超过 1'
                             if not S.res else f'取下一个数 `{S.num}`，放进两堆之一，保持小值堆 ≤ 大值堆、个数差不超过 1'),
        17: '两个堆都空：第一个数 `{num}` 先放进大值堆，`s_second` = {num}（大值堆的元素和）',
        20: '小值堆空、大值堆已有 1 个数：比较 `{second_heap[0]}` 和 `{num}`，==小的那个要进小值堆==',
        23: '大值堆里的比新数小 → 两个数交换身份：较小的进小值堆',
        24: '把换下来的较大数放回大值堆',
        26: '`{num}` 放进小值堆（取负号存成最大堆）',
        27: '`s_first` 加上 `{num}` → {s_first}',
        36: '`s_second` 加上 `{num}` → {s_second}',
        45: '`s_first` 加上 `{num}` → {s_first}',
        29: lambda S, B, r: f'`{S.num}` 与大值堆顶 `{S.second_heap[0]}` 比较：' + ('不比它小 → 该进大值堆' if S.num >= S.second_heap[0] else '比它小 → 不能进大值堆，继续看小值堆'),
        30: '大值堆已经更多：先把大值堆最小的挪给小值堆，保持个数差不超过 1',
        35: '`{num}` 放进大值堆',
        38: '`{num}` ≤ 小值堆最大值 `{-first_heap[0]}` → 该进小值堆（上面一条 `num >= second_heap[0]` 不成立）',
        39: '两堆一样多：先把小值堆最大的 `{-first_heap[0]}` 挪给大值堆，再放新数，让大值堆多一个',
        40: '弹出小值堆最大值 `{max_of_first}`',
        41: '`s_first` 减去它（负号存储，这里 `+=` 负数）→ {s_first}',
        42: '把 `{max_of_first}` 放进大值堆',
        43: '`s_second` 加上 `{max_of_first}` → {s_second}',
        44: '`{num}` 放进小值堆（取负号存）',
        48: '`{num}` 落在两个堆顶之间：放进个数较少的那一堆',
        55: lambda S, B, r: ('大值堆比小值堆多一个 → 前缀长度为奇数，中位数就是大值堆顶'
                             if len(S.second_heap) > len(S.first_heap) else '两堆一样多 → 前缀长度为偶数，取两堆顶之间的数'),
        56: '奇数个：`target = {target}`',
        58: '偶数个：`target = (({-first_heap[0]}) + ({second_heap[0]})) // 2 = {target}`；偶数个时代价与 target 具体取哪个中间值无关',
        60: '代价 = `target×p − s_first + s_second − target×q`（p、q 是两堆个数）= `{len(first_heap)}×({target}) − ({s_first}) + ({s_second}) − {len(second_heap)}×({target})` = =={res[-1]}==',
        62: '每个前缀的最小操作数：`{res}`',
    },
    cards=dict(
        one_liner='先减下标，再用大小两个堆维护中位数和两半的和',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把每个前缀变成 `x, x+1, x+2, …`，每次操作可以让某个数加一或减一',
                 '对每个前缀求最少操作数，结果对 `10^9+7` 取模',
                 '示例：`[1,1,1,2,3,4]` → `[0,1,2,3,3,3]`'],
        quote='题目要求将nums[index]变为x + index，那么不妨在一开始就将nums[index]减去index，这样一来问题就变成了对于nums的各个前缀，分别找出一个整数x，将这个前缀都变为x所需的最少操作数是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['减去下标后，前缀最优的 `x` 就是==排好序后的中位数==',
              '不能每次排序 → 套用 295 题的大小堆：小值堆 ≤ 大值堆',
              '代价 = `x×p − s_first + s_second − x×q`，只要两个堆的大小和元素和'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`/ 2` 整数除法已改为 `// 2`（偶数个时代价与 target 取值无关）',
                 '这份写法先分类讨论放入哪个堆，再统一用 `x×p … − x×q` 算代价',
                 '易错点：小值堆存负数；`nums` 被原地改成 `nums[i]-i`；最后别忘取模',
                 '对照灵神：灵神把“放进去再挪出来”合并成两行，不用分类讨论'],
    ),
)
