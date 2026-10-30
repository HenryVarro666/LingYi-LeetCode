A, Bn, K = [1, 2, 4], [1, 3, 5], 5


def _order(a, b, k):  # 与题解同样的堆过程，预先算出出堆顺序，只用来给表格上色
    import heapq
    h, out = [(a[0] + b[0], 0, 0)], []
    while h and len(out) < k:
        _, i, j = heapq.heappop(h)
        out.append((i, j))
        if j == 0 and i + 1 < len(a):
            heapq.heappush(h, (a[i + 1] + b[0], i + 1, 0))
        if j + 1 < len(b):
            heapq.heappush(h, (a[i] + b[j + 1], i, j + 1))
    return out


ORDER = _order(A, Bn, K)


def _popped(S):
    done = set(ORDER[:len(S.get('ans') or [])])
    if S.get('i') is not None and S.get('j') is not None and S.get('h') is not None:
        done.add((S['i'], S['j']))
    return done


def _cell(S, r, c, v):
    if (r, c) in _popped(S):
        return 'green'
    if any((i, j) == (r, c) for _, i, j in S.get('h', [])):
        return 'yellow'
    return None


def _txt(S):
    if 'h' not in S:
        return '表格第 `i` 行第 `j` 列 = `nums1[i] + nums2[j]`：每行、每列都递增'
    return '==绿色==是已选进答案，==黄色==是堆里的候选；每行只有「最靠左的未选格子」待在堆里'


def cap_pop(S, B, ret):
    return (f'堆顶最小的是 `{S.i, S.j}`，和 `{S.nums1[S.i] + S.nums2[S.j]}` → 出堆，'
            f'它就是当前第 {len(B.ans) + 1} 小')


def cap_app(S, B, ret):
    return f'记下数对 `[{S.nums1[S.i]}, {S.nums2[S.j]}]`，答案已有 {len(S.ans)} 对'


def cap_row(S, B, ret):
    return (f'`j == 0`：这是该行第一个出堆的格子，==把下一行的起点 `({S.i + 1}, 0)` 入堆==，'
            f'和 `{S.nums1[S.i + 1] + S.nums2[0]}`')


def cap_right(S, B, ret):
    return f'同一行向右一格：`({S.i}, {S.j + 1})` 入堆，和 `{S.nums1[S.i] + S.nums2[S.j + 1]}`'


CONFIG = dict(
    num='LCR 061', title='查找和最小的 K 对数字', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最小堆 · 下标对只向右扩展',
    code='''
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        ans = []
        h = [(nums1[0] + nums2[0], 0, 0)]
        while h and len(ans) < k:
            _, i, j = heappop(h)
            ans.append([nums1[i], nums2[j]])
            if j == 0 and i + 1 < len(nums1):
                heappush(h, (nums1[i + 1] + nums2[0], i + 1, 0))
            if j + 1 < len(nums2):
                heappush(h, (nums1[i] + nums2[j + 1], i, j + 1))
        return ans
''',
    call=f'Solution().kSmallestPairs({A}, {Bn}, {K})',
    expect=[[1, 1], [2, 1], [1, 3], [2, 3], [4, 1]],
    views=[
        dict(type='text', h=70, size=26, fn=_txt),
        dict(type='grid', var=lambda S: [[a + b for b in S['nums2']] for a in S['nums1']], label='和表：行 = nums1[i]，列 = nums2[j]',
             rows=lambda S: S['nums1'], cols=lambda S: S['nums2'], color=_cell, cell=84, h=300,
             cursors=[(lambda S: S.get('i'), lambda S: S.get('j'), 'blue')]),
        dict(type='heap', var='h', fmt=lambda t: f'{t[0]}({t[1]},{t[2]})', label='h（和, i, j）最小堆', top_color='pink', h=130),
        dict(type='text', h=80, size=30, fn=lambda S: 'ans = ' + ' '.join(f'`{p}`' for p in S.get('ans', [])) if S.get('ans') else 'ans = `[]`'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('len(ans)', lambda S: len(S['ans']) if 'ans' in S else None, 'green'), ('k', 'k')],
    captions={
        'h = [(nums1[0]': '堆里放元组 `(和, i, j)`：先比和。==初始只放 `(0, 0)`==，其余下标对以后再入堆',
        'while h and len(ans) < k': lambda S, B, r: (f'堆非空且答案只有 {len(S.ans)} 对 < `k = {S.k}` → 继续取下一小的数对'
                                                      if S.h and len(S.ans) < S.k else
                                                      ('已经凑够 `k` 对 → 结束' if len(S.ans) >= S.k else '堆空了 → 数对全取完，结束')),
        'heappop(h)': cap_pop,
        'ans.append': cap_app,
        'if j == 0': lambda S, B, r: (cap_row(S, B, r) if S.j == 0 and S.i + 1 < len(S.nums1) else
                                      (f'`j = {S.j}` 不是第 0 列 → 这一行早已开过，不用再开新行' if S.j != 0 else
                                       '已经是最后一行 → 没有下一行可开')),
        'heappush(h, (nums1[i + 1]': '`({i + 1}, 0)` 入堆：新的一行从它的第一个格子开始参与比较',
        'ans = []': '`ans` 存按和从小到大取出的数对',
        'if j + 1 < len(nums2)': lambda S, B, r: (f'`j + 1 = {S.j + 1} < {len(S.nums2)}`：本行右边还有格子 → 它成为新的候选'
                                                  if S.j + 1 < len(S.nums2) else '本行已到最右 → 没有新候选'),
        'heappush(h, (nums1[i] + nums2[j + 1]': cap_right,
        'return ans': '一共取了 `{len(ans)}` 对，按和从小到大：`{ans}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='堆里只放「候选」：每次弹出最小，再补上它右边那一格',
        complexity='时间 `O(k log min(n,k))`，空间 `O(min(n,k))`',
        problem=['两个升序数组 `nums1`、`nums2`，各取一个数组成数对 `(u, v)`',
                 '求和最小的 `k` 个数对',
                 '本视频：`[1,2,4]`、`[1,3,5]`，`k = 5` → `[1,1] [2,1] [1,3] [2,3] [4,1]`'],
        quote='规定 (i,j-1) 出堆时，将 (i,j) 入堆；而 (i-1,j) 出堆时只计入答案，其它什么也不做。',
        quote_src='—— 灵茶山艾府题解「优化后的算法」',
        idea=['把所有 `nums1[i] + nums2[j]` 摆成表：每行每列都递增，==最小的一定在候选的最左端==',
              '(i,j) 只由左边的 (i,j-1) 带进堆 → ==不会重复入堆，不需要哈希表==',
              '每一行的起点 (i,0) 在循环中才入堆：上一行第一个出堆时带入下一行'],
        summary=['时间 `O(k log min(n,k))`，空间 `O(min(n,k))`',
                 '易错：`j == 0` 才入下一行起点；否则同一格会被两个来源入堆',
                 '另一写法：开头一次性把 `(nums1[i] + nums2[0], i, 0)` 全入堆，更简洁但开局堆更大',
                 '同类：378. 有序矩阵中第 K 小的元素、786. 第 K 个最小的素数分数'],
    ),
)
