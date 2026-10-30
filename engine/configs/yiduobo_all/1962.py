CONFIG = dict(
    num=1962, title='移除石子使总数最小', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='大顶堆（取负）+ 总数递减',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1419'],
    code='''
class Solution(object):
    def minStoneSum(self, piles, k):

        heap = [-x for x in piles]
        heapq.heapify(heap)
        res = sum(piles)
        for _ in range(k):
            max_n = -heapq.heappop(heap)
            res -= max_n // 2
            max_n = (max_n + 1) // 2
            heapq.heappush(heap, -max_n)

        return res
''',
    call='Solution().minStoneSum([5,4,9,7], 3)',
    expect=16,
    views=[
        dict(type='heap', var='heap', label='heap（存的是相反数，堆顶 = 最小负数 = 最多的石子堆）', fmt=lambda x: f'{x}', top_color='yellow', h=140),
        dict(type='text', fn=lambda S: '真实石子数：' + ', '.join(str(-x) for x in sorted(S['heap'])) if S.get('heap') is not None else '', size=26, h=60),
        dict(type='text', fn=lambda S: f'已移走 ==`{sum(S["piles"]) - S["res"]}`== 颗，剩余总数 `res` = ==`{S["res"]}`==' if 'res' in S else '', size=26, h=60),
    ],
    watch=[('max_n', 'max_n', 'yellow'), ('res', 'res', 'green')],
    captions={
        'heap = [': 'Python 只有小顶堆，把每堆石子数==取负==放进去，最小的负数就是最多的一堆',
        'heapify': '堆化：堆顶 `{heap[0]}` 对应最多的一堆 `{-heap[0]}`',
        'res = sum': '`res` 先记下总数 `{res}`，之后每次操作就从里面减去移走的颗数',
        'for _ in': lambda S, B, ret: (f'`k` = {S.k} 轮都做完了，循环结束' if (S.get('_') is not None and S.get('_') == B.get('_')) else f'开始第 {S["_"] + 1} 轮（共 {S.k} 轮）'),
        'max_n = -heapq.heappop': '弹出堆顶取负，得到当前最多的一堆 ==`{max_n}`== 颗',
        'res -= max_n': '移走一半 `{max_n}//2` = `{max_n // 2}` 颗，`res` = `{B.res} - {max_n // 2}` = =={res}==',
        'max_n = (max_n + 1)': '这堆剩 `{B.max_n} - {B.max_n // 2}` = ==`{max_n}`==（向上取整 `(x+1)//2`）',
        'heapq.heappush': '剩下的 `{max_n}` 取负放回堆里，它可能还是最大的，下一轮继续减',
        'return res': '`k` 轮结束，`res` = ==`{ret}`== 就是最小剩余总数',
    },
    max_steps=60,
    cards=dict(
        one_liner='先记总数，每轮从最大堆里取最大的一堆减半',
        complexity='时间 `O(n + k log n)`，空间 `O(n)`',
        problem=['`piles[i]` 是每堆石子数，恰好操作 `k` 次，每次选一堆移除 `floor(x/2)` 颗',
                 '求剩下石子总数的最小值',
                 '本视频：`piles=[5,4,9,7], k=3` → ==16=='],
        quote='为了使得剩余的石子数最小，那么就应该选择当前剩余石子数最多的那一堆，移除其中的一半。',
        quote_src='—— yiduobo 题解',
        idea=['想剩得最少，每次就要==移走最多==：选当前最多的一堆',
              '用大顶堆维护各堆石子数；Python 的 `heapq` 是小顶堆，所以存相反数',
              '每轮：弹出堆顶 → 总数减去一半 → 剩下的一半重新放回堆'],
        summary=['时间 `O(n + k log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`res -= max_n / 2` 和 `(max_n + 1) / 2` 已改为 `//` 整除',
                 '易错：堆里存的是负数，取出来要再取负；剩下的是向上取整 `(x+1)//2`',
                 '同类题：2530. 执行 K 次操作后的最大分数'],
    ),
)
