def _cur(S):
    return f"{S['s']}·{S['e']}" if 's' in S and 'e' in S else None


CONFIG = dict(
    num=1383, title='最大的团队表现值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='效率降序扫描 + 小顶堆维护速度 top k',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maxPerformance(self, n, speed, efficiency, k):
        
        heap = []
        now = 0
        res = 0
        mod = 10 ** 9 + 7
        for s, e in sorted(zip(speed, efficiency), key=lambda d:-d[1]):
            heapq.heappush(heap, s)
            now += s
            if len(heap) > k:
                now -= heap[0]
                heapq.heappop(heap)
                
            
            res = max(res, e * now)
        
        return res % mod
''',
    call='Solution().maxPerformance(7, [2,10,3,1,5,8,4], [5,4,3,9,7,2,6], 3)',
    expect=76,
    views=[
        dict(type='array', var=lambda S: [f'{a}·{b}' for a, b in sorted(zip(S['speed'], S['efficiency']), key=lambda d: -d[1])],
             label='按效率从大到小的 (速度·效率)；黄 = 当前员工', cell=90, h=170,
             color=lambda S, i, v: 'yellow' if v == _cur(S) else None),
        dict(type='heap', var='heap', label='heap：小顶堆，速度最大的至多 k 个人', top_color='pink', h=200),
        dict(type='text', fn=lambda S: (f"速度和 `now = {S['now']}` × 效率阈值 `e = {S['e']}` = =={S['now']*S['e']}==" if 'e' in S and S['_line'] == 14 else ''), h=60),
    ],
    watch=[('now', 'now', 'blue'), ('s', 's', 'orange'), ('e', 'e', 'cyan'), ('len(heap)', lambda S: len(S['heap']), 'pink'), ('res', 'res', 'green')],
    captions={
        'heap = []': '`heap`：小顶堆，装当前入选员工的速度',
        'now = 0': '`now`：堆里速度之和',
        'mod = ': '答案要对 `10^9+7` 取模，但比较大小时用真实值，最后才取模',
        'for s, e in sorted': '扫到速度 `{s}`、效率 `{e}` 的员工：把阈值设为 `{e}`，之前的人效率都 ≥ 它',
        'heappush(heap, s)': '先让他入选：速度 `{s}` 入堆，共 `{len(heap)}` 人',
        'now += s': '`now` 加上 `{s}` → {now}',
        'if len(heap) > k': lambda S, B, r: (f'`{len(S.heap)}` 人 > `k = {S.k}`：踢掉速度最小的' if len(S.heap) > S.k
                                             else f'`{len(S.heap)}` 人 ≤ `k = {S.k}`，不用踢'),
        'now -= heap[0]': '踢掉堆顶速度 `{B.heap[0]}`：`now` → =={now}==',
        'heappop(heap)': '弹出堆顶，保留速度最大的至多 `k` 个',
        'res = max': '`res = max({B.res}, {e} × {now})` = =={res}==（不足 k 人也允许，团队至多 k 人）',
        'return res': '最大表现值 `{res}`，取模后返回',
    },
    cards=dict(
        one_liner='按效率划阈值，阈值之上永远选速度最大的 k 个人',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 名工程师，速度 `speed`、效率 `efficiency`，最多选 `k` 人',
                 '表现值 = ==速度之和 × 效率最小值==，求最大值（对 `10^9+7` 取模）',
                 '本视频：`n=7`，`k=3`，速度 `[2,10,3,1,5,8,4]`，效率 `[5,4,3,9,7,2,6]`'],
        quote='我们可以按效率划一个阈值，对于效率在阈值之上人，我们显然应该选择速度最大的k个',
        quote_src='—— yiduobo 题解原文',
        idea=['效率从大到小排序，当前员工的效率就是阈值（最小效率）',
              '之前的员工效率都 ≥ 阈值，从中挑速度最大的 `k` 个',
              '大小为 `k` 的小顶堆：新人入堆，超过 `k` 就弹出速度最小的'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '取模只在最后做，中途要比较真实大小',
                 '题目是“至多 k 人”，所以不满 k 人时也更新答案',
                 '原文为 Python 2 风格，代码无需改动；简报缺题面，题意按题目原题补写',
                 '同类：2542 最大子序列的分数'],
    ),
)
