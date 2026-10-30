_CT = [3, 6, 1, 3, 4]


def _cost(S):
    if 'r' not in S or 'cost' not in S or 'index' not in S:
        return ''
    return f"试把 `r = {S['r']}` 并进窗口 [{S['index']}, {S['r']}]：总开销 = =={S['cost']}== （budget {S['budget']}）"


CONFIG = dict(
    num=2398, title='预算内的最多机器人数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='左端点枚举 + 右端点只进不退 + 堆',
    tags=['单调队列', '滑动窗口', '难度分 1917'],
    code='''
class Solution(object):
    def maximumRobots(self, chargeTimes, runningCosts, budget):

        heap = []
        remove_dict = {}
        s = [runningCosts[0]]
        for cost in runningCosts[1:]:
            s.append(s[-1] + cost)
        
        n = len(chargeTimes)
        in_heap = set()
        r = 0
        res = 0
        for index in range(n):
            r = max(index, r)
            while r < n:
                while heap and remove_dict.get(-heap[0], 0) > 0:
                    remove_dict[-heap[0]] -= 1
                    heapq.heappop(heap)
                
                cost = chargeTimes[r]
                if heap:
                    cost = max(-heap[0], cost)

                cost += s[r] * (r - index + 1)
                if index > 0:
                    cost -= s[index - 1] * (r - index + 1)

                if cost <= budget:
                    heapq.heappush(heap, -chargeTimes[r])
                    in_heap.add(r)
                    r += 1
                else:
                    break

            res = max(res, r - index)
            if index in in_heap:
                remove_dict[chargeTimes[index]] = remove_dict.get(chargeTimes[index], 0) + 1

        return res
''',
    call='Solution().maximumRobots([3,6,1,3], [2,1,3,4], 25)',
    expect=3,
    views=[
        dict(type='text', fn=_cost, h=64),
        dict(type='array', var='chargeTimes', label='chargeTimes（框 = 已并入的 [index, r)，粉箭头 r = 待试的）', pointers={'index': 'blue', 'r': 'pink'},
             window=('index', 'r-1'), h=205),
        dict(type='array', var='s', label='s（runningCosts 的前缀和）', pointers={'index': 'blue', 'r': 'pink'}, h=205),
        dict(type='heap', var='heap', label='heap（存 −充电时间，堆顶 = 最大充电时间）', fmt=lambda x: str(-x), h=120),
        dict(type='map', var='remove_dict', label='remove_dict（待删除计数）', h=100),
    ],
    watch=[('index', 'index', 'blue'), ('r', 'r', 'pink'), ('cost', 'cost', 'orange'), ('res', 'res', 'green')],
    captions={
        'heap = []': '用小根堆存 `−chargeTimes`，堆顶就是窗口里最大的充电时间',
        'remove_dict = {}': '`remove_dict`：左端点走了，值还留在堆里 → 先记账，等它浮到堆顶再真正删（惰性删除）',
        'for cost in runningCosts[1:]': '先算前缀和 `s`，之后区间和 `s[r] − s[index−1]` 一步得到',
        'in_heap = set()': '`in_heap`：记录哪些位置真的进过堆',
        'r = 0': '`r`：窗口右边界（不含），只会往右走',
        'for index in range(n)': '枚举左端点 `index = {index}`',
        'r = max(index, r)': lambda S, B, ret: (
            f'上一轮的 `r = {B.r}` ≤ `index`：窗口是空的，从 `index` 重新找 → `r = {S.r}`' if B.r <= S.index
            else f'上一轮 `r = {B.r}`，左端点右移后窗口 [{S.index}, {B.r}) 只会更短更便宜 → ==r 不用回退=='),
        'while r < n': lambda S, B, ret: (f'`r = {S.r} < n`：试着把第 {S.r} 个机器人并进来' if S.r < len(S.chargeTimes)
                                          else f'`r = {S.r}` 到头了，停止扩张'),
        'while heap and remove_dict': lambda S, B, ret: (
            '堆顶已被左端点淘汰过（记账里有）→ 真正弹掉' if S.heap and S.remove_dict.get(-S.heap[0], 0) > 0
            else '堆顶仍在窗口里，不用清理'),
        'remove_dict[-heap[0]] -= 1': '销一笔账：`remove_dict` 里这个值的计数 −1',
        'heapq.heappop(heap)': '弹出这个过期的堆顶',
        'cost = chargeTimes[r]': '先假设窗口最大充电时间就是新来的 `{cost}`',
        'cost = max(-heap[0], cost)': '和堆顶（旧窗口最大值）比，取大的：`max({-heap[0]}, {B.cost}) = {cost}`',
        'cost += s[r] * (r - index + 1)': '试把 `r = {r}` 并进窗口：最大充电时间 + `s[r] × 长度` → cost = {cost}',
        'cost -= s[index - 1]': '`index > 0`：减去 `s[index−1]` 部分，得到区间和 × 长度：cost = =={cost}==',
        'if cost <= budget': lambda S, B, ret: (f'`{S.cost} ≤ {S.budget}`：预算够 → 这个机器人并进窗口，`r` 右移' if S.cost <= S.budget
                                               else f'`{S.cost} > {S.budget}`：超预算 → 窗口到此为止'),
        'heapq.heappush(heap, -chargeTimes[r])': '充电时间 `{chargeTimes[r]}` 入堆（存负数）',
        'in_heap.add(r)': '记下：位置 `{r}` 进过堆',
        'r += 1': '右边界右移，`r = {r}`',
        'break': '超预算，跳出，不再扩张',
        'res = max(res, r - index)': '以 `index = {index}` 为左端点，最长到 `r − 1`，长度 `{r} − {index}` = {r - index}，`res` = =={res}==',
        'if index in in_heap': lambda S, B, ret: (
            f'左端点 {S.index} 当初进过堆，现在要离开窗口 → 先记账，不立刻删堆' if S.index in S.in_heap
            else f'左端点 {S.index} 根本没进过堆，什么都不用做'),
        'remove_dict[chargeTimes[index]] =': '`remove_dict[{chargeTimes[index]}]` 记一笔待删：{remove_dict}',
        'return res': '最多连续运行 =={ret}== 个机器人',
    },
    max_steps=140,
    skip=['s.append(s[-1] + cost)', 'while r < n', 'if index > 0', 'if heap:', 'in_heap.add', 'break', 'cost = chargeTimes[r]', 'r += 1'],
    cards=dict(
        one_liner='左端点逐个枚举，右边界只进不退，最大充电时间交给堆',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['连续运行 `k` 个机器人：总开销 = `max(充电) + k × sum(运行)`',
                 '求不超 `budget` 的最长连续段',
                 '本视频：`[3,6,1,3]`、`[2,1,3,4]`、`25` → `3`'],
        quote='当上一轮对应的r <= l时，当前这一轮的r\'就应该从l\' = l + 1开始向后找，否则就直接从上一轮的r开始向后找。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定左端点 `l`，能走到的最远右端 `r` 随 `l` 增大不会变小',
              '所以 `r` 只进不退，左右各扫一遍，整体 `O(n)` 次尝试',
              '区间和用前缀和；区间最大充电时间用堆，左端点离开时==惰性删除=='],
        summary=['时间 `O(n log n)`（堆），空间 `O(n)`',
                 '惰性删除：用 `remove_dict` 记账、`in_heap` 标记谁进过堆，避免误删同值的别的位置',
                 '总开销里的区间和 = `s[r] − s[index−1]`，`index = 0` 时不用减',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神用单调队列（O(n)），yiduobo 用堆 + 惰性删除'],
    ),
)
