def _fmt(t):
    return f"{t[0]}·[{','.join(str(c) for c in t[1])}]"


CONFIG = dict(
    num=1439, title='有序矩阵中的第 k 个最小数组和', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='最小堆 · 每次把某一行右移一列 · tuple 去重',
    tags=['二分算法', '常用数据结构', '难度分 2134'],
    code='''
class Solution(object):
    def kthSmallest(self, mat, k):

        m = len(mat)
        n = len(mat[0])

        s = 0
        for index in range(m):
            s += mat[index][0]
        
        heap = [[s, [0] * m]]
        used = set()
        for _ in range(k):
            while True:
                res, choose = heapq.heappop(heap)
                if tuple(choose) not in used:
                    used.add(tuple(choose))
                    for index in range(m):
                        if choose[index] < n - 1:
                            tmp = choose[:]
                            tmp[index] += 1
                            heapq.heappush(heap, [res - mat[index][choose[index]] + mat[index][choose[index] + 1], tmp])

                    break
        
        return res
''',
    call='Solution().kthSmallest([[1, 3, 11], [2, 4, 6]], 6)',
    expect=9,
    views=[
        dict(type='grid', var='mat', label='mat（黄 = 刚弹出的方案每行选的列）', h=170, cell=70,
             color=lambda S, i, j, v: 'yellow' if 'choose' in S and S['choose'][i] == j else None),
        dict(type='heap', var='heap', fmt=_fmt, h=230),
        dict(type='set', var='used', fmt=lambda x: '[' + ','.join(str(c) for c in x) + ']', label='used（已弹出过的列下标方案）', h=130),
        dict(type='text', size=26, fn=lambda S: (
            f"弹出 `{S['choose']}`（每行选的列下标），数组和 =={S['res']}==，第 `{S['_'] + 1}` / `{S['k']}` 个" if 'choose' in S and '_' in S else '')),
    ],
    watch=[('k', 'k', 'orange'), ('第几次', lambda S: None if S.get('_') is None else S['_'] + 1, 'cyan'), ('res', 'res', 'green'), 'choose', 'index'],
    skip=['m = len(mat)', 'n = len(mat[0])', 's = 0', 'for index in range(m):\n            s +=', 'tmp = choose[:]', 'while True', 'break', 'for index in range(m)', 'tmp[index] += 1'],
    max_steps=90,
    captions={
        's += mat[index][0]': '最小的数组和：每行都选第 0 列 → `s` = {s}',
        'heap = [[s': '堆里放 `[数组和, 每行选的列下标]`：先放入最小的 `[{s}, {heap[0][1]}]`',
        'used = set()': '`used` 记录弹出过的方案（用 tuple 去重）',
        'for _ in range(k)': lambda S, B, r: f'第 `{S._ + 1}` 次取最小数组和（共 k = {S.k} 次）',
        'heappop': '弹出堆顶 `{res}`：方案 `{choose}`，这是当前最小的数组和',
        'if tuple(choose) not in used': lambda S, B, r: (f'`{S.choose}` 没出现过 → ==这是新的第 {S._ + 1} 小==，展开它的后继' if tuple(S.choose) not in S.used
                                                         else f'`{S.choose}` 已经弹出过（重复）→ ==丢掉==，再弹下一个'),
        'used.add': '记入 `used`：`{choose}` 已用',
        'for index in range(m)': lambda S, B, r: ('把每一行各右移一列，得到 m 种候选' if S['_line'] == 18 else '先累加每一行的第 0 列'),
        'if choose[index] < n - 1': lambda S, B, r: (f'第 `{S.index}` 行还能右移（`{S.choose[S.index]} < {S.n - 1}`）' if S.choose[S.index] < S.n - 1
                                                     else f'第 `{S.index}` 行已在最后一列，不能再右移'),
        'tmp[index] += 1': '第 `{index}` 行右移一列：候选方案 `{tmp}`',
        'heapq.heappush': '第 `{index}` 行右移一列 → 候选 `{tmp}`，候选和 = `{res}` − 旧值 + 新值 = =={res - mat[index][choose[index]] + mat[index][choose[index] + 1]}==，入堆',
        'return res': '最后一次弹出的数组和就是第 k 小：==`{ret}`==',
    },
    cards=dict(
        one_liner='从最小数组和出发，每次弹堆顶、把某一行右移一列，弹 k 次',
        complexity='时间约 `O(k·m·log(km))`，空间 `O(km)`',
        problem=['`m × n` 矩阵每行非递减，每行选一个数得到数组和，求第 `k` 小的数组和',
                 '示例：`mat=[[1,3,11],[2,4,6]], k=5` → `7`',
                 '本视频：就用示例 1，`k=6` → `9`（中途会遇到重复方案）'],
        quote='每当我们得到一个第p小的数组和之后，将任意一行往后移动一列之后得到的新数组都可能成为第p + 1小的数组和的，也就是新增了m中备选答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小的必然是第 0 列之和；之后每个方案把某一行往右挪一列，就得到 m 个候选',
              '候选放进最小堆，每次弹堆顶，弹 k 次就是第 k 小',
              '同一个方案能从不同前驱走到 → ==会重复==，用 `tuple(choose)` 记在 `used` 里去重'],
        summary=['k 很小，所以堆的大小不是问题：时间约 `O(k·m·log(km))`',
                 '弹出时才去重：重复的方案直接丢掉，再弹下一个',
                 '作者提到可以用「前驱都已弹出才入堆」（拓扑排序）减少候选，但本代码没有做',
                 '`heapq` 是 LeetCode 预置模块，代码未写 import',
                 '对比灵神：灵神用二分答案 + 回溯计数，或逐行合并（373 题）'],
    ),
)
