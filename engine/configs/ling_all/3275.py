CONFIG = dict(
    num=3275, title='第 K 近障碍物查询', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='大小为 k 的最大堆',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1420'],
    code='''
class Solution:
    def resultsArray(self, queries: List[List[int]], k: int) -> List[int]:
        m = len(queries)
        ans = [-1] * m
        if m < k:
            return ans

        h = [abs(x) + abs(y) for x, y in queries[:k]]
        heapify_max(h)
        ans[k - 1] = h[0]

        for i in range(k, m):
            x, y = queries[i]
            heappushpop_max(h, abs(x) + abs(y))
            ans[i] = h[0]
        return ans
''',
    # Python 3.14 才自带 heapify_max / heappushpop_max；这里用 heapq 的内部函数补上（不被追踪）
    setup='''
def heapify_max(heap):
    heapq._heapify_max(heap)

def heappushpop_max(heap, item):
    if heap and heap[0] > item:
        item, heap[0] = heap[0], item
        heapq._siftup_max(heap, 0)
    return item
''',
    call='Solution().resultsArray([[1,2],[3,4],[2,3],[-3,0],[5,5],[0,1],[-1,-1]], 3)',
    expect=[-1, -1, 7, 5, 5, 3, 3],
    views=[
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['queries']], label='queries（黄箭头 = 当前查询 i）', pointers={'i': 'yellow'}, cell=110, h=190),
        dict(type='heap', var='h', label='h：最大堆（最左 = 堆顶 = 第 k 近）', top_color='orange', h=190),
        dict(type='array', var='ans', label='ans', pointers={'i': 'yellow'}, color=lambda S, i, v: 'green' if v != -1 else None, h=190),
        dict(type='text', fn=lambda S: (f"当前查询 `({S['x']}, {S['y']})` 的距离 `|x|+|y|` = =={abs(S['x']) + abs(S['y'])}==" if 'x' in S and 'y' in S and not isinstance(S.get('x'), list) else '距离 = `|x| + |y|`（曼哈顿距离）'), size=24, h=50),
    ],
    watch=[('k', 'k', 'blue'), ('i', 'i', 'yellow'), ('堆顶 h[0]', lambda S: S['h'][0] if S.get('h') else None, 'orange')],
    captions={
        'm = len(queries)': '一共 `{m}` 个查询，`k = {k}`',
        'ans = [-1] * m': '先全填 `-1`：障碍物不到 `k` 个时答案就是 `-1`',
        'if m < k': lambda S, B, r: (f'`m = {S.m} < k = {S.k}`：永远凑不够 k 个，直接返回全 -1' if S.m < S.k
                                    else f'`m = {S.m} >= k = {S.k}`：总会凑够，答案前 `k-1` 项都是 `-1`'),
        'h = [abs(x)': '先把前 `k` 个查询的距离放进 `h`：=={h}==',
        'heapify_max(h)': '原地堆化成==最大堆==：堆顶 `{h[0]}` 是这 `k` 个里最远的，也就是第 `k` 近',
        'ans[k - 1] = h[0]': '凑够 `k` 个了：第 `k` 近 = 堆顶 =={h[0]}==，记到 `ans[{k - 1}]`',
        'for i in range(k, m)': lambda S, B, r: (f'处理第 `{S.i}` 个查询：堆里始终只留最近的 `k` 个' if B.get('i') != S.i else '查询都处理完了，退出循环'),
        'x, y = queries[i]': '新障碍物 `({x}, {y})`，距离 `{abs(x) + abs(y)}`',
        'heappushpop_max': lambda S, B, r: (
            f'新距离 `{abs(S.x) + abs(S.y)}` 比堆顶 `{B.h[0]}` 还大 → 它进不了前 `k` 近，==堆不变=='
            if abs(S.x) + abs(S.y) >= B.h[0] else
            f'新距离 `{abs(S.x) + abs(S.y)}` < 堆顶 `{B.h[0]}`：替换堆顶，原来的第 `k` 近 `{B.h[0]}` 被挤出去，堆顶变成 =={S.h[0]}=='),
        'ans[i] = h[0]': '第 `k` 近 = 堆顶 =={h[0]}==，记到 `ans[{i}]`',
        'return ans': '返回 `ans`',
    },
    max_steps=70,
    cards=dict(
        one_liner='维护前 k 小：大小为 k 的最大堆，堆顶就是第 k 近',
        complexity='时间 `O(k + (m-k) log k)`，空间 `O(k)`',
        problem=['无限平面上依次建障碍物，距离 = `|x| + |y|`',
                 '每建一个，求离原点==第 k 近==的障碍物距离，不足 `k` 个返回 `-1`',
                 '本视频：`k = 3`，7 个查询 → `[-1,-1,7,5,5,3,3]`'],
        quote='维护前 k 小元素，可以用最大堆。……当堆的大小等于 k 时，堆顶就是第 k 小的距离。',
        quote_src='—— 灵茶山艾府题解',
        idea=['堆里只留当前最近的 `k` 个距离，最大堆的堆顶就是其中最远的 = 第 `k` 近',
              '优化：前 `k-1` 项答案一定是 `-1`，先把前 `k` 个==一次性堆化==',
              '之后每来一个新距离：不比堆顶小就丢掉，比堆顶小就==替换堆顶==（`heappushpop_max`）'],
        summary=['时间 `O(k + (m-k) log k)`，空间 `O(k)`，思路同 347 前 K 个高频元素',
                 '原文先给了「先入堆、超过 k 就弹出」的写法 `O(m log k)`，本视频演示优化版',
                 '易错：`m < k` 要直接返回全 `-1`；堆顶是最大堆的最大值才是第 k 近',
                 '`heapify_max` / `heappushpop_max` 是 Python 3.14 新增的；旧版本可存相反数用最小堆'],
    ),
)
