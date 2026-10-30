CONFIG = dict(
    num=2599, title='使前缀和数组非负', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='堆 · 前缀和为负就删最小值',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def makePrefSumNonNegative(self, nums):

        now = 0
        res = 0
        heap = []
        for v in nums:
            now += v
            heapq.heappush(heap, v)
            if now < 0:
                now -= heap[0]
                heapq.heappop(heap)
                res += 1
        
        return res
''',
    call='Solution().makePrefSumNonNegative([2,3,-5,4,-3,2,-5,2])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 当前扫到的数）', color=lambda S, i, v: 'blue' if 'heap' in S and i == len(S['heap']) + S['res'] - 1 else None,
             dim=lambda S, i, v: 'heap' in S and i > len(S['heap']) + S['res'] - 1, h=170),
        dict(type='heap', var='heap', label='heap（前缀里留着的数）', h=230),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"前缀和 now = ==%d==%s" % (S['now'], '  < 0，要删最小值' if S['now'] < 0 else '  ≥ 0，不用动')) if 'now' in S else ''),
    ],
    watch=['v', ('now', 'now', 'blue'), ('res', 'res', 'green'), ('heap[0]', 'heap[0] if heap else None', 'pink')],
    captions={
        'now = 0': '`now` 是当前前缀和',
        'res = 0': '`res` 记录挪到末尾（等价于从前缀删掉）的次数',
        'heap = []': '堆里放前缀中的所有数，堆顶是最小值',
        'now += v': '前缀和加上 `{v}`：`now` = =={now}==',
        'heapq.heappush': '`{v}` 进堆，现在前缀里最小的是 `{heap[0]}`',
        'if now < 0': lambda S, B, r: (f'`now = {S.now} < 0`：前缀和为负，至少要删一个数' if S.now < 0
                                       else f'`now = {S.now} ≥ 0`：前缀合法，什么都不用做'),
        'now -= heap[0]': '删掉前缀里最小的数 `{B.heap[0]}`：`now` 变成 =={now}==（删最小的，前缀和涨得最多）',
        'heapq.heappop': '把它从堆里弹出',
        'res += 1': '多用了一次操作：`res` = {res}',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='前缀和变负，就从前缀里删掉最小的数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['操作：把 `nums` 里任意一个数移到数组末尾',
                 '要让每个前缀和都 `≥ 0`，求最少操作次数（保证有解）',
                 '示例：`[2,3,-5,4,-3,2,-5,2]` → `1`'],
        quote='操作实际上可以认为是将前缀中的某个数删去。……若前缀和小于0，那么至少需要从中删去一个数。很明显，此时应该删去当前前缀中的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['移到末尾 = 从当前前缀里拿掉，题目保证最后总能补回来',
              '前缀和 `≥ 0` 就不用管；一旦 `< 0`，必须删数',
              '删最小的数：前缀和提升最多，用堆维护最小值'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：先把 `v` 入堆，再判断；堆里可能包含刚加入的 `v`',
                 '每次最多只删一个：删最小值后前缀和一定回到 `≥ 0`',
                 '原文已是 Python 3 可运行写法，仅 `heapq` 由引擎预置'],
    ),
)
