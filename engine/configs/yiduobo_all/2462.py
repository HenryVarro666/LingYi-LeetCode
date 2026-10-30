CONFIG = dict(
    num=2462, title='雇佣 K 位工人的总代价', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='一个堆 + 头尾边界 left / right',
    tags=['堆（优先队列）', '难度分 1764'],
    code='''
class Solution(object):
    def totalCost(self, costs, k, candidates):

        n = len(costs)
        heap = []
        res = 0

        if candidates * 2 < n:
            left = candidates - 1
            right = n - candidates
            for index in range(left + 1):
                heapq.heappush(heap, [costs[index], index])
            for index in range(right, n):
                heapq.heappush(heap, [costs[index], index])

            while left + 1 < right and k > 0:
                min_cost, index = heapq.heappop(heap)
                res += min_cost
                if index <= left:
                    left += 1
                    heapq.heappush(heap, [costs[left], left])
                else:
                    right -= 1
                    heapq.heappush(heap, [costs[right], right])

                k -= 1

        else:
            for index in range(n):
                heapq.heappush(heap, [costs[index], index])

        while k > 0:
            min_cost, index = heapq.heappop(heap)
            res += min_cost
            k -= 1

        return res
''',
    call='Solution().totalCost([17,12,10,2,7,2,11,20,8,5,9], 3, 3)',
    expect=22,
    views=[
        dict(type='text', fn=lambda S: (f"头部已入堆到下标 `{S['left']}`，尾部已入堆到下标 `{S['right']}`；已雇总代价 =={S['res']}==" if 'right' in S and 'left' in S else '')),
        dict(type='array', var='costs', pointers={'left': 'blue', 'right': 'pink'}, h=220, label='costs（left = 头部已入堆的最大下标，right = 尾部已入堆的最小下标）'),
        dict(type='heap', var='heap', fmt=lambda x: f'{x[0]}@{x[1]}', h=200, label='heap：[代价, 下标]，显示 代价@下标'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green'), ('k', 'k', 'purple')],
    captions={
        'if candidates * 2 < n': lambda S, B, r: (f'`{S.candidates}×2 = {S.candidates*2} < n = {S.n}` → 成立：一开始只能从头尾挑，用堆维护' if S.candidates * 2 < S.n
                                                  else f'`{S.candidates}×2 = {S.candidates*2} ≥ n = {S.n}`：所有人都能选，直接全入堆'),
        'left = candidates - 1': '`left = {left}`：头部已入堆的最大下标',
        'right = n - candidates': '`right = {right}`：尾部已入堆的最小下标',
        'heapq.heappush(heap, [costs[index], index])': '`[{costs[index]}, {index}]` 入堆：代价第一关键字，下标第二关键字（并列取下标小的）',
        'while left + 1 < right': lambda S, B, r: (f'`left + 1 = {S.left+1} < right = {S.right}` 且 `k = {S.k} > 0` → 继续' if S.left + 1 < S.right and S.k > 0
                                                  else '头尾交汇（剩余工人都在堆里）或已雇够 → 退出'),
        'min_cost, index = heapq.heappop(heap)': lambda S, B, r: f'弹出堆顶 `[{S.min_cost}, {S.index}]`：最便宜的工人，下标 {S.index}',
        'res += min_cost': '雇佣：`res = {res}`',
        'if index <= left': lambda S, B, r: (f'`index = {S.index} <= left = {S.left}` → 成立：他来自头部' if S.index <= S.left else f'`index = {S.index} > left = {S.left}` → 他来自尾部'),
        'left += 1': '头部窗口前进：`left` → {left}',
        'right -= 1': '尾部窗口前进：`right` → {right}',
        'heapq.heappush(heap, [costs[left], left])': '头部补位：`costs[{left}] = {costs[left]}` 入堆',
        'heapq.heappush(heap, [costs[right], right])': '尾部补位：`costs[{right}] = {costs[right]}` 入堆',
        'k -= 1': '还剩 `k = {k}` 轮',
        'return res': '总代价 `{res}`',
    },
    cards=dict(
        one_liner='一个堆装头尾候选，弹出谁就让那一侧补位',
        complexity='时间 `O((c+k) log (c+k))`，空间 `O(c)`',
        problem=['共 `k` 轮，每轮从最前 `candidates` 和最后 `candidates` 个工人里选代价最小的（并列取下标小的）',
                 '示例：`costs=[17,12,10,2,7,2,11,20,8]`，`k=3`，`candidates=4` → `11`',
                 '本视频：`[17,12,10,2,7,2,11,20,8,5,9]`，`k=3`，`candidates=3` → `22`'],
        quote='使用两个变量left和right分别表示当前已经加入堆中的头部工人的最大下标，以及已经加入堆中的尾部工人的最小下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['头尾候选放进同一个堆，元素是 `[代价, 下标]`',
              '弹出的下标 `<= left` 属于头部，就让 `left` 右移补一个',
              '否则属于尾部，`right` 左移补一个；两边交汇后剩下的都在堆里'],
        summary=['时间 `O((c+k) log (c+k))`，空间 `O(c)`',
                 '易错点：`candidates*2 >= n` 时所有人都可选，直接全部入堆取前 k 个',
                 '易错点：循环条件 `left + 1 < right`，交汇后再继续补位会重复入堆',
                 '对比灵神：灵神用前后两个堆，yiduobo 用一个堆加边界判断来源',
                 '原文代码在 Python 3 下无需修改'],
    ),
)
