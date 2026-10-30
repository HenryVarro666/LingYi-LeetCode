def _info(S):
    if 'p' not in S or 'index' not in S:
        return ''
    i, p, n = S['index'], S['p'], len(S['nums'])
    w = S['nums'][i:p]
    if not w:
        return '窗口为空'
    out, m = [], 0
    for v in w:
        m = max(m, v)
        out.append(m)
    return f'窗口 `[{i}, {p - 1}]` = `{w}` 抬成非递减：`{out}`，操作数 `cost` = =={S["cost"]}==（k = {S["k"]}）'


CONFIG = dict(
    num=3420, title='统计 K 次操作以内得到非递减子数组的数目', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='左端点枚举 + 最大堆 + 单调栈 + 前缀和修正',
    tags=['灵神题单·单调栈', '难度分 2855'],
    code='''
class Solution(object):
    def countNonDecreasingSubarrays(self, nums, k):
        
        n = len(nums)
        f = [n] * n
        s = [0]
        stack = []
        heap = []
        removed = {}

        p = 0
        cost = 0
        res = 0
        for index, v in enumerate(nums):
            while p < n and (not heap or max(-heap[0] - nums[p], 0) + cost <= k):
                if heap:
                    cost += max(-heap[0] - nums[p], 0)
                heapq.heappush(heap, -nums[p])
                s.append(s[-1] + nums[p])

                while stack and nums[p] > nums[stack[-1]]:
                    f[stack.pop()] = p
                stack.append(p)

                p += 1

            res += p - index

            bound = min(f[index], p) - 1
            cost -= v * (bound - index)
            cost += s[bound + 1] - s[index + 1]

            left = index + 1
            while left < bound:
                right = min(f[left] - 1, bound)
                cost += nums[left] * (right - left)
                cost -= s[right + 1] - s[left + 1]
                left = right + 1
        
            removed[v] = removed.get(v, 0) + 1
            while heap and removed.get(-heap[0], 0) > 0:
                removed[-heap[0]] -= 1
                heapq.heappop(heap)

        return res
''',
    call='Solution().countNonDecreasingSubarrays([4,2,1,2], 3)',
    expect=8,
    max_steps=90,
    views=[
        dict(type='text', fn=_info, size=24),
        dict(type='array', var='nums', pointers={'index': 'blue', 'p': 'pink'}, window=('index', 'p - 1'), h=230,
             dim=lambda S, i, v: 'p' in S and 'index' in S and not (S['index'] <= i < S['p'])),
        dict(type='array', var='f', label='f[i]：右边第一个更大数的下标（n = 4 表示没有）', h=170, cell=70,
             color=lambda S, i, v: 'green' if 'p' in S and v < S['p'] else None),
        dict(type='heap', var='heap', label='heap（存相反数，堆顶 = 窗口最大值）', fmt=lambda x: str(-x), h=170),
        dict(type='stack', var='stack', label='stack（下标，栈底到栈顶对应的值递减）', fmt=lambda i: str(i), h=130),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('cost', 'cost', 'orange'), ('k', 'k', 'cyan'), ('res', 'res', 'green')],
    skip=['n = len(nums)', 'f = [n] * n', 'stack = []', 'heap = []', 'removed = {}', 'p = 0', 'cost = 0', 'res = 0', 'left = index + 1', 'if heap:', 's.append', 'removed[-heap[0]] -= 1', 'p += 1', 'stack.append(p)', 'removed[v] = ', 'heapq.heappop', 'left = right + 1', 'while left < bound'],
    captions={
        's = [0]': '`s` 是前缀和，`s[i+1] - s[j]` 是 `nums[j..i]` 的和；每入窗口一个数就追加一项',
        'for index, v in enumerate(nums)': '枚举窗口左端点 `index = {index}`（`v = {v}`）',
        'while p < n and': lambda S, B, r: (
            f'窗口为空，`nums[{S.p}] = {S.nums[S.p]}` 直接放进来' if (S.p < len(S.nums) and not S.heap) else
            f'窗口 `[{S.index}, {S.p - 1}]`：把 `nums[{S.p}] = {S.nums[S.p]}` 加进来，要补 `max({-S.heap[0] if S.heap else 0} − {S.nums[S.p]}, 0)`，`cost` 会变成 `{S.cost + max(-S.heap[0] - S.nums[S.p], 0) if S.heap else S.cost}`，≤ k 才能扩'
            if S.p < len(S.nums) and (not S.heap or max(-S.heap[0] - S.nums[S.p], 0) + S.cost <= S.k) else
            ('右端点到头了' if S.p >= len(S.nums) else f'再加 `nums[{S.p}] = {S.nums[S.p]}` 会让 `cost` 超过 `k = {S.k}` → 窗口不再扩')),
        'cost += max(': '新元素比窗口最大值 `{-heap[0]}` 小，要抬到最大值：`cost` += `{max(-heap[0] - nums[p], 0)}` → `{cost}`',
        'heapq.heappush': '`nums[{p}] = {nums[p]}` 入堆（存 `{-nums[p]}`，最小堆当最大堆用），同时 `s` 追加前缀和',
        'while stack and nums[p] > nums[stack[-1]]': lambda S, B, r: (
            f'`nums[{S.p}] = {S.nums[S.p]}` 比栈顶下标 `{S.stack[-1]}` 的值 `{S.nums[S.stack[-1]]}` 大 → 栈顶找到了右边第一个更大数'
            if S.stack and S.nums[S.p] > S.nums[S.stack[-1]] else
            ('栈空' if not S.stack else f'`{S.nums[S.p]}` 不比栈顶 `{S.nums[S.stack[-1]]}` 大 → 停')),
        'f[stack.pop()] = p': '弹出的下标找到了右边第一个更大数：`f = {f}`',
        'p += 1': '右端点后移，`p` → {p}（窗口现在是 `[{index}, {p - 1}]`）',
        'res += p - index': '左端点 `{index}`，右端点可取 `{index}..{p - 1}`，共 `{p - index}` 个 → `res = {res}`',
        'bound = min(f[index], p) - 1': '`nums[{index}] = {v}` 离开窗口前，它管着 `[{index + 1}, bound]`：`bound = min(f[{index}], {p}) − 1 = {bound}`',
        'cost -= v * (bound - index)': '这些数原来都被抬到了 `{v}`，先撤销：`cost` −= `{v} × ({bound} − {index})` → `{cost}`',
        'cost += s[bound + 1] - s[index + 1]': '再加回它们本身的和 `s[{bound + 1}] − s[{index + 1}]` → `cost = {cost}`（相当于每个数回到原值）',
        'right = min(f[left] - 1, bound)': '`left = {left} < bound`：以 `nums[{left}]` 为新基准，它管到 `right = min(f[{left}] − 1, {bound}) = {right}`',
        'cost += nums[left] * (right - left)': '`[{left + 1}, {right}]` 要抬到 `{nums[left]}`：`cost` += `{nums[left]} × ({right} − {left})` → `{cost}`',
        'cost -= s[right + 1] - s[left + 1]': '再减去这段本身的和 → `cost = {cost}`',
        'while heap and removed.get': lambda S, B, r: (
            f'`removed` 记着堆顶 `{-S.heap[0]}` 已离开窗口（懒删除）→ 弹掉' if S.heap and S.removed.get(-S.heap[0], 0) > 0 else '堆顶还在窗口里，停止'),
        'removed[-heap[0]] -= 1': '`removed[{-heap[0]}]` 减一',
        'return res': '共 `{res}` 个',
    },
    cards=dict(
        one_liner='窗口右端只增不减，左端离开时把「抬高的代价」撤销并重算',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次操作可让子数组里一个数加 1，问有多少个子数组最多 `k` 次操作就能变成非递减',
                 '每个数要抬到它左边最大值，操作数 = Σ(前缀最大 − 自身)',
                 '示例：`[6,3,1,2,4,4]`，`k = 7` → `17`',
                 '本视频：`[4,2,1,2]`，`k = 3`'],
        quote='对于nums[index]，不妨设其在数组中下一个更大的元素值为f[index]，这个f[index]可以通过单调栈来求解……将其中的nums[index]提出来，可以发现这是一个乘积减去一个区间和的形式。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定起点 `index`，终点越大操作越多；起点右移终点只会更靠右 → 滑动窗口',
              '右端进窗口：用堆里最大值算要补多少；左端离开：用 `f` 找到它管的范围，`乘积 − 区间和` 撤销',
              '撤销后，后面的数要换成新基准继续抬，每个下标只当一次基准 → 均摊 `O(1)`'],
        summary=['时间 `O(n log n)`（堆），空间 `O(n)`',
                 '堆里存相反数，离开窗口的数用 `removed` 字典懒删除',
                 '`bound` 之后的数本来就不是以 `nums[index]` 为基准抬的，不用动',
                 '原文是 Python 2 风格，没有需要改动的写法，代码原样运行',
                 '对比灵神：灵神倒序滑窗，只用单调队列合并/删树；这里正序 + 堆 + 前缀和'],
    ),
)
