NUMS = [7, 9, 5, 8, 1, 3]
M = len(NUMS)
N = M // 3


def _idx(S):
    """当前正在处理的 nums 下标（按行号判断在哪个循环里）"""
    ln = S.get('_line', 0)
    try:
        if ln == 7:
            return len(S['heap']) - 1
        if 10 <= ln <= 14:
            return N + len(S['f']) - 2
        if ln == 18:
            return M - len(S['heap'])
        if 21 <= ln <= 25:
            return M - 1 - N - (len(S['g']) - 2)
        if ln == 30:
            return None
    except Exception:
        return None
    return None


def _col(S, k, v):
    ln = S.get('_line', 0)
    i = _idx(S)
    if ln == 30:
        return 'cyan' if k <= N + S['index'] - 1 else 'green'
    if i is None:
        return None
    if k == i:
        return 'yellow'
    if ln <= 14:
        return 'cyan' if k < i else None
    return 'green' if k > i else None


def _dim(S, k, v):
    ln = S.get('_line', 0)
    i = _idx(S)
    if ln == 30 or i is None:
        return False
    return (k > i) if ln <= 14 else (k < i)


def _heap(S):
    h = S.get('heap')
    if h is None:
        return None
    return [-x for x in h] if S.get('_line', 0) <= 14 else list(h)


def _lab(S):
    return None


def _cmp1(S, B, r):
    num, top = S.num, -S.heap[0]
    if num < top:
        return f'`{num}` < 堆顶（现有最大）`{top}`：换进去能让和更小 → 有收益'
    return f'`{num}` ≥ 堆顶 `{top}`：换进去不会更小 → ==不换==，`f` 保持 {S.f[-1]}'


def _cmp2(S, B, r):
    num, top = S.num, S.heap[0]
    if num > top:
        return f'`{num}` > 堆顶（现有最小）`{top}`：换进去能让和更大 → 有收益'
    return f'`{num}` ≤ 堆顶 `{top}`：换进去不会更大 → ==不换==，`g` 保持 {S.g[-1]}'


def _res(S, B, r):
    i = S.index
    return (f'分割点 `{i}`：前缀最小和 `f[{i}] = {S.f[i]}` − 后缀最大和 `g[{i}] = {S.g[i]}` = {S.f[i] - S.g[i]}'
            f'，`res` → =={S.res}==')


def _fm(S):
    ln = S.get('_line', 0)
    if ln == 30:
        i = S['index']
        return f"`f[{i}] − g[{i}] = {S['f'][i]} − {S['g'][i]}` = =={S['f'][i] - S['g'][i]}==；`res` 取最小"
    if ln >= 17:
        return '`g[i]`：从右往左，每放进一个数就记下「当前最大 n 个之和」'
    return '`f[i]`：从左往右，每放进一个数就记下「当前最小 n 个之和」'


CONFIG = dict(
    num=2163, title='删除元素后和的最小差值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='贪心 · 前后缀 Top n 堆',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2225'],
    code='''
class Solution(object):
    def minimumDifference(self, nums):

        n = len(nums) // 3
        heap = []
        for num in nums[:n]:
            heapq.heappush(heap, -num)
        f = [-sum(heap)]
        for num in nums[n : n + n]:
            f.append(f[-1])
            if num < -heap[0]:
                f[-1] += num + heap[0]
                heapq.heappush(heap, -num)
                heapq.heappop(heap)

        heap = []
        for num in nums[-1 : -n - 1: -1]:
            heapq.heappush(heap, num)
        g = [sum(heap)]
        for num in nums[-n - 1: -n - n - 1: -1]:
            g.append(g[-1])
            if num > heap[0]:
                g[-1] += num - heap[0]
                heapq.heappush(heap, num)
                heapq.heappop(heap)
        g.reverse()

        res = f[0] - g[0]
        for index in range(1, n + 1):
            res = min(res, f[index] - g[index])
        
        return res
''',
    call=f'Solution().minimumDifference({NUMS})',
    expect=1,
    skip=['for num in nums[:n]', 'for num in nums[n : n + n]', 'for num in nums[-1', 'for num in nums[-n - 1',
          'for index in range(1'],
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前数，青 = 前缀已处理，绿 = 后缀已处理）', h=170, cell=84,
             color=_col, dim=_dim),
        dict(type='heap', var=_heap, label='heap：前缀最小 n 个 / 后缀最大 n 个', h=150),
        dict(type='array', var='f', label='f[i]：nums[:n+i] 中最小 n 个之和', h=170, cell=84),
        dict(type='array', var='g', label='g[i]：nums[n+i:] 中最大 n 个之和', h=170, cell=84),
        dict(type='text', fn=_fm, size=24, h=90),
    ],
    watch=['n', 'num', ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`：删掉 `n` 个、剩两半各 `n` 个。差值取==最小==（不是绝对值），所以前半越小越好、后半越大越好',
        'heap = []': '准备一个空堆',
        'heapq.heappush(heap, -num)': lambda S, B, r: (f'先取反放进堆：`nums[{_idx(S)}] = {S.num}`（最小堆当最大堆用）' if S.get('_line') == 7
                                                      else f'`{S.num}` 先入堆（堆暂时多 1 个）'),
        'heapq.heappush(heap, num)': lambda S, B, r: (f'`nums[{_idx(S)}] = {S.num}` 放进堆' if S.get('_line') == 18
                                                     else f'`{S.num}` 先入堆（堆暂时多 1 个）'),
        'heapq.heappop(heap)': lambda S, B, r: ('弹出堆顶：被替换掉的 ==最大数==，堆回到 n 个' if S.get('_line') == 14
                                                else '弹出堆顶：被替换掉的 ==最小数==，堆回到 n 个'),
        'f = [-sum(heap)]': '`f[0] = {f[0]}`：分割点在 `n-1`，前 `n` 个全选，这是最小的和',
        'f.append(f[-1])': lambda S, B, r: f'新来 `nums[{_idx(S)}] = {S.num}`：先假设不换，`f` 沿用上一个值 {S.f[-1]}',
        'if num < -heap[0]': _cmp1,
        'f[-1] += num + heap[0]': '换掉最大的：`f[-1]` += `{num} − {-heap[0]}` → ==`{f[-1]}`==',
        'g = [sum(heap)]': '`g[0]` 暂记 `{g[0]}`：后缀只有 `n` 个数，全选（最后会 reverse，对应分割点 `2n-1`）',
        'g.append(g[-1])': lambda S, B, r: f'从右往左新来 `nums[{_idx(S)}] = {S.num}`：先假设不换，`g` 沿用 {S.g[-1]}',
        'if num > heap[0]': _cmp2,
        'g[-1] += num - heap[0]': '换掉最小的：`g[-1]` += `{num} − {heap[0]}` → ==`{g[-1]}`==',
        'g.reverse()': '把 `g` 翻转：`g[i]` 对应「前 `n+i` 个在左、其余在右」的分割点，==下标和 `f` 对齐==：`{g}`',
        'res = f[0] - g[0]': '分割点 `0`：`{f[0]} − {g[0]}` = `{res}`',
        'res = min': _res,
        'return res': '最小差值 = ==`{res}`==',
    },
    cards=dict(
        one_liner='前半选最小的 n 个，后半选最大的 n 个，枚举分割点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 有 `3n` 个数，恰好删掉 `n` 个，剩下的前 `n` 个为第一部分，后 `n` 个为第二部分',
                 '求 `sum_first − sum_second` 的==最小值==（不是绝对值最小）',
                 '示例：`[7,9,5,8,1,3]` → `1`'],
        quote='题目中的最小差值指的就是字面意义上差的最小值，而不是一般理解中的绝对值最小，因此在这里可以确定这是贪心法的题目。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心：前半和要最小、后半和要最大；两半不能交叉，所以先选一个分割点 `cut_pos`',
              '每个分割点对应「前缀最小 n 个之和」和「后缀最大 n 个之和」，和「数据流第 n 大」是同一个问题',
              '用大小为 n 的堆：新数比堆顶更优就替换并更新和，否则不动；前后各扫一遍得到 `f`、`g`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '前缀用大根堆（取反的小根堆）保留最小的 n 个；后缀用小根堆保留最大的 n 个',
                 '`g` 是从右往左算的，==用之前要 reverse==，才和 `f` 的下标对齐',
                 '原文为 Python 2 写法，`len(nums) / 3` 已改为 `//`',
                 '对比灵神：灵神用 `heappushpop` 一步替换，并边算前缀边更新答案；yiduobo 分别存 `f`、`g` 再合并'],
    ),
)
