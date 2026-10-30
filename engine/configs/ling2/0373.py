A = [1, 7, 11]
B_ = [2, 4, 6]
K = 5


def _popped(S):
    """ans 里已有的 (i, j)；本例 nums1、nums2 的值互不相同，可以从值反查下标"""
    return {(A.index(a), B_.index(b)) for a, b in S.get('ans', [])}


def _in_heap(S):
    return {(i, j) for _, i, j in S.get('h', [])}


def _color(S, i, j, v):
    if (i, j) in _popped(S):
        return 'green'
    if (i, j) in _in_heap(S):
        return 'blue'
    return None


def _info(S):
    if 'h' not in S:
        return '矩阵 `M[i][j] = nums1[i] + nums2[j]`：==每一行都递增== → 合并 n 个升序列表，取前 k 小'
    if 'ans' not in S:
        return '初始：把每一行的==第一个数== `(i, 0)` 都放进堆'
    return f"已选 `{len(S['ans'])}` / `{K}` 个；蓝 = 堆里的候选，堆顶就是下一个最小"


def _cap_pop(S, B, ret):
    return (f'弹出堆顶 `({S.i}, {S.j})`：`{A[S.i]} + {B_[S.j]} = {A[S.i] + B_[S.j]}` 是剩下的数对里==最小的==')


def _cap_if(S, B, ret):
    if S.j + 1 < len(B_):
        return f'同一行右边还有 `({S.i}, {S.j + 1})` → 它可能成为下一个最小，入堆'
    return f'`({S.i}, {S.j})` 已是这一行最后一个，没有右边的候选了'


CONFIG = dict(
    num=373, title='查找和最小的 K 对数字', difficulty='Medium', category='堆',
    author='灵茶山艾府', technique='最小堆 · 一开始把 (i,0) 都入堆',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        h = [(nums1[i] + nums2[0], i, 0) for i in range(min(len(nums1), k))]
        # nums1 是递增的，无需堆化

        ans = []
        for _ in range(k):
            _, i, j = heappop(h)
            ans.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heappush(h, (nums1[i] + nums2[j + 1], i, j + 1))
        return ans
''',
    call=f'Solution().kSmallestPairs({A}, {B_}, {K})',
    expect=[[1, 2], [1, 4], [1, 6], [7, 2], [7, 4]],
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='table', var=lambda S: [[a + b for b in B_] for a in A], cell=84, h=330,
             label='M[i][j] = nums1[i] + nums2[j]（绿 = 已选，蓝 = 在堆里，黄框 = 刚弹出）',
             rows=lambda S: [f'{a}' for a in A], cols=lambda S: [f'{b}' for b in B_],
             color=_color, cursors=[('i', 'j', 'yellow')]),
        dict(type='set', var=lambda S: set(S['h']) if 'h' in S else None, font=26,
             label='最小堆 h 里的 (和, i, j)：按和从小到大列出，最左 = 堆顶（黄 = 新入堆）',
             fmt=lambda t: f'{t[0]}:({t[1]},{t[2]})', h=110),
        dict(type='text', fn=lambda S: f"`ans = {S['ans']}`" if 'ans' in S else '', size=24, h=80),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('len(ans)', lambda S: len(S['ans']) if 'ans' in S else None, 'green')],
    captions={
        'h = [(nums1[i]': '每一行的第一个 `(i, 0)` 都入堆：`{h}`（nums1 递增，==已经是堆==，无需堆化）',
        'ans = []': '`ans` 按从小到大收集数对',
        'for _ in range(k)': lambda S, B, r: (f'第 `{len(S.ans) + 1}` 次：从堆里取当前最小的数对' if len(S.ans) < K
                                              else f'已经取够 `k = {K}` 个，循环结束'),
        '_, i, j = heappop': _cap_pop,
        'ans.append': '`[{nums1[i]}, {nums2[j]}]` 加入答案',
        'if j + 1 < len(nums2)': _cap_if,
        'heappush': '`({nums1[i] + nums2[j + 1]}, {i}, {j + 1})` 入堆，堆：`{h}`',
        'return ans': '循环 k 次，得到和最小的 k 个数对：=={ret}==',
    },
    cards=dict(
        one_liner='把每行的 (i,0) 全放进堆，每次弹出堆顶后只把它右边的 (i,j+1) 入堆',
        complexity='时间 `O(k log min(n,k))`，空间 `O(min(n,k))`',
        problem=['两个==升序==数组 `nums1`、`nums2` 和整数 `k`',
                 '数对 `(u, v)`：`u` 来自 nums1，`v` 来自 nums2；找出和最小的 `k` 个数对',
                 '示例：`nums1 = [1,7,11], nums2 = [2,4,6], k = 3` → `[[1,2],[1,4],[1,6]]`',
                 '本视频取 `k = 5`'],
        quote='不妨==规定== (i,j−1) 出堆时，将 (i,j) 入堆；而 (i−1,j) 出堆时只计入答案，其它什么也不做。……所以初始不仅要把 (0,0) 入堆，(1,0),(2,0),⋯ 这些都要入堆。',
        quote_src='—— 灵茶山艾府题解',
        idea=['朴素做法：`(i,j)` 出堆时把 `(i+1,j)`、`(i,j+1)` 都入堆，会==重复==，要哈希表去重',
              '规定只由左边的 `(i,j-1)` 负责把 `(i,j)` 入堆 → 每次只推 `(i,j+1)`，不重复',
              '另一角度：M 的每一行递增，相当于==合并 n 个升序列表==（同 23 题）'],
        result='返回 `[[1,2],[1,4],[1,6],[7,2],[7,4]]` ✓ 和依次为 3, 5, 7, 9, 11',
        summary=['时间 `O(k log min(n,k))`：堆里至多 `min(n,k)` 个三元组',
                 '初始只取前 `min(n, k)` 行：第 k 行以后不可能进入前 k 小',
                 '易错：入堆的是 `(和, i, j)` 三元组，第一个元素是和，才能按和比较',
                 '写法二：循环中遇到 `j == 0` 时再把 `(i+1, 0)` 入堆，堆更小、更快'],
    ),
)
