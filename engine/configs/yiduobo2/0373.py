def _mat(S):
    if 'pos_list' not in S:
        return None
    return [[a + b for b in S['tmp2']] for a in S['tmp1']]


def _color(S, r, c, v):
    pos = S['pos_list']
    if c < pos[r]:
        return 'green'
    if c == pos[r] and r in {idx for _, idx in S.get('heap', [])}:
        return 'blue'
    return None


def _info(S):
    if 'tmp1' not in S:
        return '把所有和排成矩阵：每一行都是==单调递增==的数组 → 多路归并，取前 k 个'
    if 'pos_list' not in S:
        return f"`nums1` 更长 → 交换：让 `tmp1 = {S['tmp1']}`（短）当行，`tmp2 = {S['tmp2']}` 当列"
    return f"`{len(S['tmp1'])}` 路归并：第 r 行下一个候选是 `M[r][pos_list[r]]`；堆里每行只放一个"


def _cap_swap_if(S, B, ret):
    if len(S.nums1) > len(S.nums2):
        return f'`len(nums1) = {len(S.nums1)} > len(nums2) = {len(S.nums2)}` → 交换，让==较短的数组当行==，堆更小'
    return '`nums1` 不更长，不用交换'


def _cap_pop(S, B, ret):
    return f'弹出堆顶 `[{S.val}, {S.index}]`：第 `{S.index}` 行的当前候选 `{S.val}` 是所有行里最小的'


def _cap_append(S, B, ret):
    return f'交换过 → 数对要==换回原顺序==写成 `[nums1 的数, nums2 的数]` = `{S.res[-1]}`'


CONFIG = dict(
    num=373, title='查找和最小的 K 对数字', difficulty='Medium', category='堆',
    author='yiduobo', technique='m 路归并 · 短数组当行',
    tags=['字节30天', '面试经典150'],
    code='''
import heapq

class Solution(object):
    def kSmallestPairs(self, nums1, nums2, k):
        swap_flag = False
        if len(nums1) > len(nums2):
            tmp1 = nums2
            tmp2 = nums1
            swap_flag = True
        else:
            tmp1 = nums1
            tmp2 = nums2

        pos_list = [0] * len(tmp1)
        heap = [[x + tmp2[0], index] for index, x in enumerate(tmp1)]
        heapq.heapify(heap)

        res = []
        while k > 0 and heap:
            val, index = heapq.heappop(heap)
            if swap_flag:
                res.append([tmp2[pos_list[index]], tmp1[index]])
            else:
                res.append([tmp1[index], tmp2[pos_list[index]]])
            pos_list[index] += 1
            if pos_list[index] < len(tmp2):
                heapq.heappush(heap, [tmp1[index] + tmp2[pos_list[index]], index])
            k -= 1

        return res
''',
    call='Solution().kSmallestPairs([1, 2, 4, 5], [3, 6], 4)',
    expect=[[1, 3], [2, 3], [4, 3], [1, 6]],
    views=[
        dict(type='text', fn=_info, size=26, h=80),
        dict(type='table', var=_mat, cell=84, h=250,
             label='M[r][c] = tmp1[r] + tmp2[c]（绿 = 已选，蓝 = 堆里的候选，黄框 = pos_list 指针）',
             rows=lambda S: S['tmp1'], cols=lambda S: S['tmp2'],
             color=_color, cursors=[('index', 'pos_list[index]', 'yellow')]),
        dict(type='array', var='pos_list', label='pos_list[r]：第 r 行下一个要取的列', cell=72, h=150),
        dict(type='set', var=lambda S: set(map(tuple, S['heap'])) if 'heap' in S else None, font=26,
             label='heap 里的 [和, 行号]：按和从小到大列出，最左 = 堆顶', fmt=lambda t: f'[{t[0]}, {t[1]}]', h=110),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`" if 'res' in S else '', size=24, h=56),
    ],
    watch=[('k', 'k', 'yellow'), ('swap_flag', 'swap_flag', 'pink'), ('val', 'val'), ('index', 'index', 'cyan')],
    captions={
        'swap_flag = False': '`swap_flag` 记录有没有交换过两个数组',
        'if len(nums1) > len(nums2)': _cap_swap_if,
        'tmp1 = nums2': '`tmp1 = nums2 = {tmp1}`：短的当行（m 路归并的 m 更小）',
        'tmp2 = nums1': '`tmp2 = nums1 = {tmp2}`：长的当列',
        'swap_flag = True': '记下：交换过，输出时要换回来',
        'pos_list = [0]': '每一行一个指针 `pos_list[r]`，初始都指向第 0 列',
        'heap = [[x + tmp2[0]': '每行的第一个数 `[tmp1[r] + tmp2[0], r]` 入堆：`{heap}`',
        'heapq.heapify': '建堆：堆顶 `{heap[0]}` 是最小的和',
        'res = []': '==边算边做==，不提前算出整个 m×n 矩阵',
        'while k > 0 and heap': lambda S, B, r: (f'`k = {B.k} > 0` 且堆非空 → 再取一个' if B.k > 0 and B.heap
                                                 else '`k = 0`：已经取够了'),
        'val, index = heapq.heappop': _cap_pop,
        'if swap_flag': lambda S, B, r: '`swap_flag = True` → 输出时把行列换回来' if S.swap_flag else '没交换过，直接输出',
        'res.append([tmp2[pos_list': _cap_append,
        'pos_list[index] += 1': '第 `{index}` 行的指针右移：`pos_list[{index}] = {pos_list[index]}`',
        'if pos_list[index] < len(tmp2)': lambda S, B, r: (f'第 `{S.index}` 行还有数 → 把新的候选放进堆'
                                                          if S.pos_list[S.index] < len(S.tmp2) else f'第 `{S.index}` 行取完了'),
        'heapq.heappush': '第 `{index}` 行还有数 → 下一个候选 `[{tmp1[index] + tmp2[pos_list[index]]}, {index}]` 入堆',
        'k -= 1': '还要取 `k = {k}` 个',
        'return res': '返回 =={ret}==',
    },
    skip=['if swap_flag', 'if pos_list[index] < len(tmp2)'],
    cards=dict(
        one_liner='把所有和看成 m 个递增数组，用堆做 m 路归并取前 k 个',
        complexity='时间 `O(k log min(m,n))`，空间 `O(min(m,n))`',
        problem=['两个==升序==数组 `nums1`、`nums2` 和整数 `k`',
                 '数对 `(u, v)`：`u` 来自 nums1，`v` 来自 nums2；找出和最小的 `k` 个数对',
                 '示例：`nums1 = [1,7,11], nums2 = [2,4,6], k = 3` → `[[1,2],[1,4],[1,6]]`',
                 '本视频：`nums1 = [1,2,4,5], nums2 = [3,6], k = 4`'],
        quote='将这些加和按下标排列好，可以形成一个m * n的矩阵，那么就可以视为==m个长度为n的单调递增数组，找出其中最小的k个数==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['转化为 m 路归并：每行一个指针 `pos_list[r]`，堆里放每行的当前候选',
              '弹出最小的，指针右移，把这一行的新候选放回堆',
              '让==较短的数组当行==，堆的大小是 `min(m, n)`；输出时注意把数对换回来'],
        result='返回 `[[1,3],[2,3],[4,3],[1,6]]` ✓ 和依次为 4, 5, 7, 7',
        summary=['时间 `O(k log min(m,n))`：每次出入堆 `O(log min(m,n))`',
                 '易错：不能先算出整个 m×n 矩阵，那样直接 `O(mn)`，要==边算边做==',
                 '交换过数组后，`res` 里要写 `[tmp2[..], tmp1[..]]` 恢复原来的顺序',
                 '对比灵神：思路相同（每行递增、多路归并）；yiduobo 用 `pos_list` 记列号，灵神把 `j` 放进三元组',
                 '原文为 Python 2 风格：删去了文档字符串，代码未改'],
    ),
)
