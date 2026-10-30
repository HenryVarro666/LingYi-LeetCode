def _idx(S):
    try:
        return S['nums'].index(S['x'])
    except Exception:
        return None


def _heap_txt(S):
    h = S.get('heap')
    if h is None:
        return ''
    if not h:
        return '堆还是空的'
    return f"堆顶（取负后）= `{h[0]}` → 最优区间左端点 `best = {-h[0]}`　累计操作 `res = {S['res']}`"


def _cmp(S, B, ret):
    x, best = S.x, S.best
    if x < best:
        return f'`x = {x} < best = {best}`：==x 落在最优区间左边==，最优取值区间变成 `[{x}, {best}]`，这一轮至少要多花 `{best - x}`'
    return f'`x = {x} ≥ best = {best}`：x 本身就在最优区间内（或右侧）→ ==不用多花操作==，最优值就是 x'


CONFIG = dict(
    num=2263, title='数组变为有序的最小操作次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='凸函数 · 堆维护斜率拐点',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def convertArray(self, nums):

        
        def calc():
            heap = []
            res = 0

            for x in nums:
                if not heap:
                    heap.append(-x)
                else:
                    best = -heap[0]

                    if x < best:
                        heapq.heappop(heap)
                        heapq.heappush(heap, -x)
                        heapq.heappush(heap, -x)
                        res += best - x
                    else:
                        heapq.heappush(heap, -x)

            return res

        v1 = calc()
        nums.reverse()
        v2 = calc()
        return min(v1, v2)
''',
    call='Solution().convertArray([3,2,4,0])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前 x）', cell=84, h=130,
             color=lambda S, i, v: 'blue' if i == _idx(S) and 'heap' in S else None),
        dict(type='heap', var='heap', label='heap（大顶堆）', fmt=lambda x: str(-x), top_color='yellow', h=170),
        dict(type='text', fn=_heap_txt, size=24, h=56),
    ],
    watch=[('x', 'x', 'blue'), ('best', lambda S: S['_inner'].get('best'), 'yellow'), ('res', 'res', 'green'),
           ('v1', lambda S: S.get('v1'), 'cyan')],
    captions={
        'heap = []': '`heap` 维护「最优取值区间的左端点」等斜率拐点，用大顶堆（存相反数）',
        'res = 0': '`res` 累计最少操作次数',
        'for x in nums': '依次处理每个数 `x`',
        'if not heap': lambda S, B, r: ('第一个数：堆是空的，没有上一轮的最优区间' if not B.get('heap') else
                                        f'堆非空 → 看上一轮最优区间的左边界'),
        'heap.append(-x)': '第一个数 `{x}` 就是最优取值：`f[0][j] = |{x} − j|`，最小在 `j = {x}`，入堆',
        'best = -heap[0]': '堆顶取负 → 上一轮最优区间的左边界 `best = {best}`',
        'if x < best': _cmp,
        'heapq.heappop(heap)': '弹出旧的堆顶：斜率为 −1 的那段不存在了',
        17: '把 `{x}` 放进堆（存 `-x`）',
        18: '再放一次：`{x}` 出现两次，补上斜率为 −2 的位置',
        21: '`x` 就是新的最优位置，直接放进堆（存 `-x`）',
        'res += best - x': '要多花 `best − x = {best} − {x}`：`res` → =={res}==',
        'return res': '一共需要 `{res}` 次操作（变成非递减）',
        'v1 = calc()': '先求把 `nums` 变成==单调不减==的最少操作',
        'nums.reverse()': '单调不增 = 把数组翻转后求单调不减：翻转得 `{nums}`',
        'v2 = calc()': '再对翻转后的数组求一次',
        'return min(v1, v2)': '`min({v1}, {v2})` = =={ret}==',
    },
    skip=['for x in nums'],
    max_steps=110,
    cards=dict(
        one_liner='f 是凸函数：用堆记住最优区间的左端点，x 落在左边就多花 best − x',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次操作可把某个 `nums[i]` 加 1 或减 1',
                 '求让 `nums` 变成==非递减或非递增==的最少操作次数',
                 '示例：`[3,2,4,5,0]` → `4`；本视频：`[3,2,4,0]` → `2`'],
        quote='若其小于上一轮最优区间的左边界……需要从堆中弹出堆顶元素，然后加入两次nums[i]，同时将上一轮最优区间的左边界减去x累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 前 i 个数变不减、末尾为 j 的最少操作；是绝对值函数累加 → ==凸函数==',
              '堆顶 = 最优区间的左边界 `best`；`x ≥ best` 时最优不变，直接入堆',
              '`x < best` 时答案多 `best − x`；堆里弹出一个、再放两个 `-x`',
              '单调不增：翻转数组再算一次，取较小者'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '堆里存相反数来当大顶堆；`best = -heap[0]`',
                 '==两次都要算==：一次不减，一次翻转后的不减（即不增），最后取 `min`',
                 '`nums.reverse()` 会原地翻转，第二次 `calc` 用的就是翻转后的数组',
                 '同一思路见 LCP 59 搭桥过河（更复杂的堆维护）；原文为 Python 2 风格，只删去了类型说明'],
    ),
)
