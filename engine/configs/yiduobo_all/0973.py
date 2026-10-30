CONFIG = dict(
    num=973, title='最接近原点的 K 个点', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='快速选择 · top k 不需有序', tags=[],
    code='''
class Solution(object):
    def kClosest(self, points, k):

        dis = [[x * x + y * y, index] for index, (x, y) in enumerate(points)]
        
        self.qsort(dis, 0, len(dis) - 1, k)
        #print dis
        return [points[index] for _, index in dis[:k]]
    
    def qsort(self, dis, l, r, k):
        mid = dis[(l + r) // 2][0]
        i, j = l, r
        while i < j:
            while dis[i][0] < mid:
                i += 1
            while dis[j][0] > mid:
                j -= 1
            if i <= j:
                dis[i], dis[j] = dis[j], dis[i]
                i += 1
                j -= 1

        if j - l + 1 > k:
            self.qsort(dis, l, j, k)
        elif i - l < k and i < r:
            self.qsort(dis, i, r, k - (i - l))
''',
    call='Solution().kClosest([[1,3],[-2,2],[2,-2],[0,1],[3,3],[-1,0]], 2)',
    expect=[[-1, 0], [0, 1]],
    result_fn=sorted,
    views=[
        dict(type='text', fn=lambda S: f"区间 `[{S['l']}, {S['r']}]`，基准 mid = =={S['mid']}==，还要选出 `{S['k']}` 个" if 'mid' in S and 'l' in S else '`dis[t] = [距离², 原下标]`', size=30),
        dict(type='array', var=lambda S: [d for d, _ in S['dis']], label='dis 里的距离²（按位置）', h=300,
             pointers={'i': 'blue', 'j': 'pink'}, cell=110,
             window=('l', 'r'),
             dim=lambda S, i, v: 'l' in S and not (S['l'] <= i <= S['r']),
             color=lambda S, i, v: 'green' if S['_line'] >= 8 and S['_line'] <= 8 and i < S['k'] else None),
        dict(type='calls', h=200),
    ],
    watch=['l', 'r', 'k', 'mid', ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'dis = [[x': '先算每个点到原点的距离²：`dis[t] = [距离², 原下标]`，问题变成 ==top k==',
        'self.qsort(dis, 0': '只要前 `k = {k}` 小的，不要求有序 → 用==快速选择==，不必完整排序',
        'mid = dis[': '取中间位置的距离 `mid = {mid}` 做基准（区间 `[{l}, {r}]`）',
        'i, j = l, r': '`i` 从左往右、`j` 从右往左扫，把小的换到左边、大的换到右边',
        'while i < j': lambda S, B, r: f'`i = {S.i}`、`j = {S.j}`：' + ('还没相遇，继续划分' if S.i < S.j else '指针相遇或交错，划分结束'),
        'while dis[i][0] < mid': lambda S, B, r: f'`dis[{S.i}]` 的距离是 {S.dis[S.i][0]}，' + ('比 mid 小，已经在正确的一侧 → i 右移' if S.dis[S.i][0] < S.mid else '不小于 mid → i 停下，它要换到右边'),
        'while dis[j][0] > mid': lambda S, B, r: f'`dis[{S.j}]` 的距离是 {S.dis[S.j][0]}，' + ('比 mid 大，已经在正确的一侧 → j 左移' if S.dis[S.j][0] > S.mid else '不大于 mid → j 停下，它要换到左边'),
        'if i <= j': lambda S, B, r: ('`i <= j`：左边停下的数不小于 mid、右边停下的数不大于 mid → ==交换==' if S.i <= S.j else '`i > j`：已经错开，不交换'),
        'dis[i], dis[j] =': '交换 `dis[{i}]` 和 `dis[{j}]`：小的去左边，大的去右边',
        'if j - l + 1 > k': lambda S, B, r: f'左半段 `[{S.l}, {S.j}]` 有 {S.j - S.l + 1} 个数（都 ≤ mid），' + ('比 k = %d 还多 → 答案全在左半段，只递归左边' % S.k if S.j - S.l + 1 > S.k else '不多于 k = %d → 左半段全要，再看右边' % S.k),
        'self.qsort(dis, l, j, k)': '进入左半段 `[{l}, {j}]`，仍然要选 `{k}` 个',
        'elif i - l < k and i < r': lambda S, B, r: (f'左边共 {S.i - S.l} 个，不足 k = {S.k}，右半段 `[{S.i}, {S.r}]` 还要补 {S.k - (S.i - S.l)} 个 → 递归右边' if (S.i - S.l < S.k and S.i < S.r) else f'左边已有 {S.i - S.l} 个（够 k = {S.k}），或右边无可选 → 不用再递归，结束'),
        'self.qsort(dis, i, r': '进入右半段 `[{i}, {r}]`，还要选 `{k - (i - l)}` 个',
        'return [points': '`dis` 的前 `k` 项就是最近的 k 个点（组内不保证有序）：`{ret}`',
    },
    cards=dict(
        one_liner='top k 不需要有序：快速选择只递归一侧',
        complexity='时间平均 `O(n)`，空间 `O(1)`（递归栈平均 `O(log n)`）',
        problem=['给定平面上的点 `points`，返回离原点最近的 `k` 个点（顺序任意）',
                 '比较距离只需 `x² + y²`，不必开方',
                 '本视频：`[[1,3],[-2,2],[2,-2],[0,1],[3,3],[-1,0]]`，`k = 2` → `[[0,1],[-1,0]]`'],
        quote='注意到这里的top k并不需要top k也有序，因此可以使用快排中使用的快速选择法。……将小于mid的数放在区间的头部，将大于mid的数放在区间的尾部，接下来只需要判断小于mid的数的个数以及大于mid的数的个数与k的大小关系。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个点变成 `[距离², 下标]`，问题就是找前 k 小',
              '像快排一样按 mid 划分：左半段全部 `≤ mid`，右半段全部 `≥ mid`',
              '左半段够 k 个就只递归左边；不够就整段留下，再去右边补 `k - 左边个数`'],
        summary=['平均 `O(n)`；若基准总选到最差位置会退化到 `O(n²)`',
                 '易错：等于 mid 的数可能落在两侧，所以判断用 `j - l + 1` 与 `i - l`，而不是简单比较下标',
                 '易错：递归右边时 k 要减去左边已确定的个数',
                 '原文为 Python 2 写法，`(l + r) / 2` 是整数除法，已改为 `//`',
                 '另一种常见写法是大小为 k 的大根堆，`O(n log k)`'],
    ),
)
