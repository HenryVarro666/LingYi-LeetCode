CONFIG = dict(
    num=3275, title='第 K 近障碍物查询', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='大顶堆（存相反数）动态求第 k 小',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1420'],
    code='''
class Solution(object):
    def resultsArray(self, queries, k):

        heap = []
        res = []
        for x, y in queries:
            d = abs(x) + abs(y)
            heapq.heappush(heap, -d)

            if len(heap) < k:
                res.append(-1)
            else:
                if len(heap) > k:
                    heapq.heappop(heap)
                res.append(-heap[0])
        
        return res
''',
    call='Solution().resultsArray([[1,2],[3,4],[2,3],[-3,0],[5,5],[0,1]], 3)',
    expect=[-1, -1, 7, 5, 5, 3],
    views=[
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['queries']], label='queries',
             cell=110, h=170),
        dict(type='heap', var='heap', label='heap：存的是距离的相反数，堆顶 = -最大距离', top_color='orange', h=170,
             fmt=lambda x: f'{x}'),
        dict(type='array', var='res', label='res（每次询问的答案）', color=lambda S, i, v: 'green' if v != -1 else None, h=170),
        dict(type='text', fn=lambda S: (f"`d = |{S['x']}| + |{S['y']}|` = =={S['d']}==，入堆的是 `-d` = {-S['d']}" if 'd' in S and 'x' in S else '距离 = 曼哈顿距离 `|x| + |y|`'), size=24, h=50),
    ],
    watch=[('k', 'k', 'blue'), ('d', lambda S: S.get('d'), 'orange'), ('len(heap)', lambda S: len(S['heap']), 'pink'),
           ('答案 -heap[0]', lambda S: -S['heap'][0] if S.get('heap') else None, 'green')],
    captions={
        'heap = []': '`heap` 是 Python 的小顶堆，存==距离的相反数==，就当成大顶堆用',
        'res = []': '`res` 按询问顺序记录每次的答案',
        'for x, y in queries': lambda S, B, r: ('询问都处理完了，退出循环' if (B.get('x'), B.get('y')) == (S.x, S.y) else f'处理下一个询问：在 `({S.x}, {S.y})` 建障碍物'),
        'd = abs(x)': '曼哈顿距离 `d = |{x}| + |{y}|` = =={d}==',
        'heapq.heappush': '把 `-d = {-d}` 入堆；堆里最小的相反数 = 最大的距离',
        'if len(heap) < k': lambda S, B, r: (f'堆里只有 `{len(S.heap)}` 个，不足 `k = {S.k}` 个 → 答案 `-1`' if len(S.heap) < S.k
                                            else f'堆里有 `{len(S.heap)}` 个，已经够 `k = {S.k}` 个，可以给出答案'),
        'res.append(-1)': '不足 `k` 个：`res` 追加 `-1`',
        'if len(heap) > k': lambda S, B, r: (f'堆里 `{len(S.heap)}` 个，超过 `k` 了' if len(S.heap) > S.k
                                            else f'刚好 `{S.k}` 个，不用弹'),
        'heapq.heappop': '弹出堆顶：把当前最远的那个扔掉，堆里只保留最近的 `k` 个',
        'res.append(-heap[0])': lambda S, B, r: f'堆顶是 `{S.heap[0]}`，取反 =={-S.heap[0]}== 就是第 `k` 近的距离',
        'return res': '返回 `res`',
    },
    max_steps=70,
    cards=dict(
        one_liner='动态求第 k 小：维护一个大小为 k 的大顶堆',
        complexity='时间 `O(m log k)`，空间 `O(k)`',
        problem=['无限平面上依次建障碍物，距离按曼哈顿距离 `|x| + |y|`',
                 '每次建完，问离原点==第 k 近==的障碍物距离，不足 `k` 个返回 `-1`',
                 '本视频：`k = 3`，6 个询问 → `[-1,-1,7,5,5,3]`'],
        quote='静态的求第k小的数之前遇到过，可以使用排序、堆或者快速选择算法，而本题则是动态的求第k小的问题，依然可以使用堆来处理。',
        quote_src='—— yiduobo 题解',
        idea=['维护大小为 `k` 的大顶堆：堆里是目前最近的 `k` 个距离，堆顶 = 其中最远的 = 第 `k` 近',
              '每次询问：距离入堆；超过 `k` 个就弹掉堆顶；不足 `k` 个答案是 `-1`',
              'Python 的 `heapq` 是小顶堆，所以==存距离的相反数==，就相当于大顶堆'],
        summary=['每个询问入堆 / 出堆各一次，`O(m log k)`；堆大小不超过 `k + 1`',
                 '易错：堆里存的是 `-d`，答案要取反 `-heap[0]`',
                 '易错：先判断「不足 k 个」，再判断是否要弹堆顶',
                 '同类题：347 前 K 个高频元素、215 数组中第 K 个最大元素'],
    ),
)
