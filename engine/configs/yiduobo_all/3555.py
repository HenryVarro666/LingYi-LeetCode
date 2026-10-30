CONFIG = dict(
    num=3555, title='排序每个滑动窗口中最小的子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='单调栈求逆序对端点 + 堆处理区间赋值',
    tags=['滑动窗口与双指针', '单调栈'],
    code='''
class Solution(object):
    def minSubarraySort(self, nums, k):
        
        n = len(nums)
        f = [None] * n
        stack = []
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index]:
                f[stack.pop()] = index
            
            stack.append(index)
        
        g = [None] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[index]:
                g[stack.pop()] = index
            
            stack.append(index)

        mi_intervals = []
        ma_intervals = []
        for index in range(n):
            if f[index] is not None:
                start = max(0, f[index] - k + 1)
                if start <= index:
                    mi_intervals.append([start, index, index])
        
            if g[index] is not None:
                start = max(0, index - k + 1)
                if start <= g[index]:
                    ma_intervals.append([start, g[index], index])

        mi_intervals.sort()
        ma_intervals.sort()
        mi_heap = []
        ma_heap = []
        mi = []
        ma = []
        p = 0
        q = 0
        for index in range(n):
            while p < len(mi_intervals) and mi_intervals[p][0] == index:
                heapq.heappush(mi_heap, (mi_intervals[p][2], mi_intervals[p][1]))
                p += 1
            
            while mi_heap and mi_heap[0][1] < index:
                heapq.heappop(mi_heap)
            
            if mi_heap:
                mi.append(mi_heap[0][0])
            else:
                mi.append(None)

            while q < len(ma_intervals) and ma_intervals[q][0] == index:
                heapq.heappush(ma_heap, (-ma_intervals[q][2], ma_intervals[q][1]))
                q += 1
            
            while ma_heap and ma_heap[0][1] < index:
                heapq.heappop(ma_heap)
            
            if ma_heap:
                ma.append(-ma_heap[0][0])
            else:
                ma.append(None)

        res = []
        for index in range(n - k + 1):
            if mi[index] is None:
                res.append(0)
            else:
                res.append(ma[index] - mi[index] + 1)
        
        return res
''',
    call='Solution().minSubarraySort([3,1,2], 2)',
    expect=[2, 0],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'yellow'}, h=110, cell=60),
        dict(type='stack', var='stack', label='stack', h=110),
        dict(type='array', var='f', label='f 右边更小', h=80, cell=60, index=False),
        dict(type='array', var='g', label='g 左边更大', h=80, cell=60, index=False),
        dict(type='array', var='mi', label='mi 最左起点', h=80, cell=60, index=False),
        dict(type='array', var='ma', label='ma 最右终点', h=80, cell=60, index=False),
        dict(type='array', var='res', label='res 答案', h=80, cell=60, index=False),
    ],
    watch=['index', 'p', 'q', ('mi_intervals', 'mi_intervals', 'blue'), ('ma_intervals', 'ma_intervals', 'pink'),
           ('mi_heap', 'mi_heap', 'cyan'), ('ma_heap', 'ma_heap', 'orange')],
    skip=['stack = []', 'mi_intervals = []', 'ma_intervals = []', 'mi_heap = []', 'ma_heap = []',
          'mi = []', 'ma = []', 'p = 0', 'q = 0', 'n = len', 'ma_intervals.sort()', 'res = []', 'p += 1', 'q += 1', 'if mi_heap:', 'if ma_heap:', 'if start <= index', 'if start <= g[index]', 'heapq.heappop'],
    max_steps=130,
    captions={
        'f = [None] * n': '`f[i]`：`i` 右边==下一个更小==的下标（i 和它构成逆序对），先全设为空',
        7: '正向遍历，用单调栈找每个数「右边第一个更小」的数',
        'while stack and nums[stack[-1]] > nums[index]': lambda S, B, r: (
            f'栈空，没有可弹的' if not S.stack else
            f'栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` 对 当前 `nums[{S.index}] = {S.nums[S.index]}`：'
            + ('栈顶更大 → 当前数就是它右边第一个更小的，弹出' if S.nums[S.stack[-1]] > S.nums[S.index] else '栈顶不大于当前，不弹')),
        'f[stack.pop()] = index': '弹出的下标 `f` 记为 `{index}`：`f = {f}`',
        'stack.append(index)': '当前下标入栈，栈里的数从底到顶保持不降',
        'g = [None] * n': '`g[i]`：`i` 左边==上一个更大==的下标，反向遍历再来一遍',
        15: '反向遍历，找每个数「左边第一个更大」的数',
        'while stack and nums[stack[-1]] < nums[index]': lambda S, B, r: (
            f'栈空，没有可弹的' if not S.stack else
            f'栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` 对 当前 `nums[{S.index}] = {S.nums[S.index]}`：'
            + ('栈顶更小 → 当前数是它左边第一个更大的，弹出' if S.nums[S.stack[-1]] < S.nums[S.index] else '栈顶不小于当前，不弹')),
        'g[stack.pop()] = index': '弹出的下标 `g` 记为 `{index}`：`g = {g}`',
        23: lambda S, B, r: ('每个下标都处理完了' if getattr(B, 'index', None) == S.index == S.n - 1 else f'逐个下标记录窗口左端范围，`index = {S.index}`'),
        'if f[index] is not None': '`index` 能作逆序对起点吗？{"可以，它右边第一个更小的下标 f = " + str(f[index]) if f[index] is not None else "不行，右边没有更小的数"}',
        'start = max(0, f[index] - k + 1)': '窗口要同时盖住 `index` 和 `f[index]={f[index]}`：窗口左端在 `[{start}, {index}]`（窗口长 k = {k}）',
        'if start <= index': '`start <= index`（`{start} <= {index}`）：{"范围非空，记录" if start <= index else "范围为空（窗口放不下），不记录"}',
        'mi_intervals.append': '记录 `[窗口左端起, 左端止, 起点下标]`：左端在该范围的窗口里，`{index}` 是一个逆序对起点',
        'if g[index] is not None': '`index` 能作逆序对终点吗？{"可以，它左边第一个更大的下标 g = " + str(g[index]) if g[index] is not None else "不行，左边没有更大的数"}',
        'start = max(0, index - k + 1)': '窗口要同时盖住 `g[index]={g[index]}` 和 `index`：窗口左端在 `[{start}, {g[index]}]`',
        'if start <= g[index]': '`start <= g[index]`（`{start} <= {g[index]}`）：{"范围非空，记录" if start <= g[index] else "范围为空，不记录"}',
        'ma_intervals.append': '记录：左端在该范围的窗口里，`{index}` 是一个逆序对终点',
        'mi_intervals.sort()': '两组区间按「窗口左端起点」排序，之后只需一个指针配合堆扫一遍',
        42: lambda S, B, r: ('每个左端都处理完了' if getattr(B, 'index', None) == S.index == S.n - 1 else f'依次考察窗口左端 `index = {S.index}`，它能用到哪些记录'),
        'while p < len(mi_intervals)': lambda S, B, r: (f'区间起点 `{S.mi_intervals[S.p][0]} == index` → 这条记录从现在起生效，入堆' if S.p < len(S.mi_intervals) and S.mi_intervals[S.p][0] == S.index else '没有新的记录要生效了'),
        'heapq.heappush(mi_heap': '入堆 `(逆序对起点, 左端止)`：堆顶是==最左的逆序对起点==',
        'while mi_heap and mi_heap[0][1] < index': lambda S, B, r: (f'堆顶的左端止 `{S.mi_heap[0][1]} < index = {S.index}`：已失效，弹出' if S.mi_heap and S.mi_heap[0][1] < S.index else '堆顶仍有效（或堆空），不弹'),
        'mi.append(mi_heap[0][0])': '左端为 `{index}` 的窗口，最左的逆序对起点 = 堆顶 `{mi_heap[0][0]}`',
        'mi.append(None)': '左端为 `{index}` 的窗口里没有逆序对起点，窗口本身有序',
        'while q < len(ma_intervals)': lambda S, B, r: (f'终点记录 `{S.ma_intervals[S.q][0]} == index` → 生效，入堆' if S.q < len(S.ma_intervals) and S.ma_intervals[S.q][0] == S.index else '没有新的终点记录要生效'),
        'heapq.heappush(ma_heap': '入堆 `(-终点, 左端止)`：取负后堆顶就是==最右的逆序对终点==',
        'while ma_heap and ma_heap[0][1] < index': lambda S, B, r: (f'堆顶的左端止 `{S.ma_heap[0][1]} < index = {S.index}`：已失效，弹出' if S.ma_heap and S.ma_heap[0][1] < S.index else '堆顶仍有效（或堆空），不弹'),
        'ma.append(-ma_heap[0][0])': '左端为 `{index}` 的窗口，最右的逆序对终点 = `{-ma_heap[0][0]}`',
        'ma.append(None)': '左端为 `{index}` 的窗口没有逆序对终点',
        68: lambda S, B, r: (f'逐个窗口，窗口左端 `index = {S.index}`（窗口 `[{S.index}, {S.index + S.k - 1}]`）' if getattr(B, 'index', None) != S.index or S.index == 0 else '所有窗口都算完了'),
        'if mi[index] is None': '`mi[{index}] = {mi[index]}`：{"没有逆序对 → 已经有序" if mi[index] is None else "有逆序对，要排序的一段是 mi 到 ma"}',
        'res.append(ma[index] - mi[index] + 1)': '要排序的一段 `[{mi[index]}, {ma[index]}]`，长度 `{ma[index]} - {mi[index]} + 1` = =={ma[index]-mi[index]+1}==',
        'res.append(0)': '窗口已有序，需排序的长度为 0',
        'return res': '每个窗口需要排序的最短长度：`{ret}`',
    },
    cards=dict(
        one_liner='窗口里最左逆序对起点到最右逆序对终点，就是要排序的一段',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['对每个长度为 `k` 的窗口，求至少排序多长的一段才能让它有序',
                 '已经有序则为 `0`，只算长度，不真正排序',
                 '本视频：`nums=[3,1,2], k=2` → `[2,0]`'],
        quote='不妨设子数组中最左侧逆序对的起点下标为 start，最右侧逆序对的终点下标为 end，那么需要排序的就是 start 到 end 这一段，其长度为 end - start + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案 = 窗口内最左逆序对起点到最右逆序对终点',
              '反过来想：下标 `index` 能是哪些窗口的起点？用 `f`（下一个更小）算出左端点范围',
              '终点同理用 `g`（上一个更大）；`f`、`g` 用正反两趟单调栈',
              '得到若干「左端范围 → 取最值」，排序后用堆扫一遍'],
        summary=['时间 `O(n log n)`（排序与堆），空间 `O(n)`',
                 '`mi` 取最小的起点，堆里存 `(起点, 区间终点)`；`ma` 取最大的终点，所以入堆时取负',
                 '堆顶过期（区间终点 `< index`）要先弹出再读',
                 '没有逆序对的窗口，`mi[index]` 为 `None`，答案为 `0`'],
    ),
)
