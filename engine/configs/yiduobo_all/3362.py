def _q(S):
    q = S.get('queries')
    return None if q is None else [f'{a}~{b}' for a, b in q]


CONFIG = dict(
    num=3362, title='零数组变换 III', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='区间覆盖贪心 · 堆 + 差分',
    tags=['灵神题单·常用数据结构', '灵神题单·贪心与思维', '难度分 2424'],
    code='''
class Solution(object):
    def maxRemoval(self, nums, queries):
        
        n = len(nums)
        heap = []
        f = [0] * n
        cnt = 0
        res = len(queries)
        queries.sort()
        p = 0
        for index, v in enumerate(nums):
            while p < len(queries) and queries[p][0] == index:
                heapq.heappush(heap, -queries[p][1])
                p += 1
            cnt -= f[index]
            while cnt < v and heap and -heap[0] >= index:
                res -= 1
                cnt += 1
                if -heap[0] + 1 < n:
                    f[-heap[0] + 1] += 1
                heapq.heappop(heap)
            
            if cnt < v:
                return -1
        
        return res
''',
    call='Solution().maxRemoval([2,0,2], [[0,2],[0,2],[1,1]])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（index = 当前位置，v 要被覆盖 v 次）', pointers={'index': 'blue'}, pointer_labels={'index': 'i'}, h=215),
        dict(type='array', var=_q, label='queries（l~r，已排序，p = 下一个待入堆）', pointers={'p': 'pink'}, h=215, cell=110,
             dim=lambda S, i, v: S.get('p') is not None and i < S['p']),
        dict(type='heap', var='heap', label='heap（存右端点）', fmt=lambda x: f'r={-x}', h=150),
        dict(type='array', var='f', label='f（区间在 r+1 处闭合，cnt 要减去）', h=190),
    ],
    watch=['index', 'v', ('cnt', 'cnt', 'blue'), ('res', 'res', 'green'), 'p'],
    captions={
        'f = [0]': '`f[i]`：在下标 `i` 处闭合的区间个数（差分）',
        'res = len': '`res` 先假设 `queries` 全部可删：`res = {res}`，每选一个减一',
        'queries.sort': '排序后左端点从小到大，按下标依次放入堆',
        'while p < len': '`p = {p}`：{"左端点 == " + str(index) + "，入堆" if p < len(queries) and queries[p][0] == index else "没有左端点 == " + str(index) + " 的区间了"}',
        'heapq.heappush': '区间 `[{queries[p][0]}, {queries[p][1]}]` 入堆，存 `-{queries[p][1]}`，堆顶就是右边界最大的',
        'p += 1': '`p` → {p}',
        'cnt -= f': '`cnt -= f[{index}]` = {f[index]}：右边界在 `{index-1}` 的区间不再覆盖 `{index}` → `cnt = {cnt}`',
        'while cnt < v': lambda S, B, r: (f'`cnt = {S.cnt}` < `v = {S.v}`，堆顶右边界 `{-S.heap[0]} >= {S.index}` → 再选一个，右边界最大' if S.cnt < S.v and S.heap and -S.heap[0] >= S.index
                                      else (f'`cnt = {S.cnt} >= v = {S.v}`，已够，不选' if S.cnt >= S.v else '堆空或右边界不够，选不了')),
        'res -= 1': '选中一个区间，不能再删：`res` → {res}',
        'cnt += 1': '它覆盖 `{index}`，`cnt` → =={cnt}==',
        'if -heap[0] + 1 < n': '右边界 `{-heap[0]}` 之后失效，要在 `{-heap[0]+1}` 记闭合；`{-heap[0]+1} < {n}` → {"记" if -heap[0]+1 < n else "越界，不用记"}',
        'f[-heap[0] + 1] += 1': '`f[{-heap[0]+1}] += 1`：到那里 cnt 要减一',
        'heapq.heappop': '弹出这个已选区间，堆里只留未选的',
        'if cnt < v': lambda S, B, r: (f'`{S.cnt} < {S.v}`：能用的区间都用了还不够 → 返回 -1' if S.cnt < S.v else f'`{S.cnt} >= {S.v}`：下标 {S.index} 覆盖够了'),
        'return res': '`res` = 总数 - 选中的 = 最多删 `{res}` 个',
    },
    cards=dict(
        one_liner='从边界开始想：下标 0 只能靠左端点为 0 的区间，选右边界最大的',
        complexity='时间 `O(n + q log q)`，空间 `O(n + q)`',
        problem=['每个 `queries[i]` 可对 `nums` 的 `[l, r]` 中任意下标减 1',
                 '删掉尽量多的 query，剩下的仍能把 `nums` 变全 0',
                 '无法做到返回 -1',
                 '示例：`nums=[2,0,2]`，`queries=[[0,2],[0,2],[1,1]]` → `1`'],
        quote='对于区间覆盖类的贪心，比较常见的做法是从边界情况入手分析，因为越靠近边界就越难被区间覆盖到，因此需要进行的抉择就更少，更容易发现贪心的策略。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[0]` 只能被左端点为 0 的区间覆盖，必须选 `nums[0]` 个，取右边界最大的',
              '推到 `nums[index]`：已选区间覆盖了 `cnt` 个，还缺 `v - cnt` 个',
              '缺的从「起点 `<= index`、没选过」的区间里取右边界最大的，用堆维护',
              '`cnt` 用数组 `f` 记录区间在哪闭合，沿用 3355、3356 的差分办法'],
        summary=['时间 `O(n + q log q)`，空间 `O(n + q)`',
                 '`res` 从 `len(queries)` 开始，每选一个区间减一',
                 '`f` 只开 `n` 位，所以右边界 + 1 越界时不记',
                 '对比灵神：灵神把堆放在「先全部左端点 `<= i` 入堆」，这里用 `== index`（排序后等价），并用 `res` 递减代替最后数堆大小'],
    ),
)
