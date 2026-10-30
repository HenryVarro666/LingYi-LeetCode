_A = [1, 2, 3, 5]


def _fr(t):
    return f'{_A[t[1]]}/{_A[t[2]]}'


CONFIG = dict(
    num=786, title='第K个最小的素数分数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='最小堆 · 按行推进',
    tags=['二分算法', '常用数据结构'],
    code='''
import heapq

class Solution(object):
    def kthSmallestPrimeFraction(self, A, K):

        n = len(A)
        pos_list = [0] * n
        heap = []
        for index in range(1, n):
            heapq.heappush(heap, (A[0] * 1.0 / A[index], 0, index))

        while K:
            v, x, y = heapq.heappop(heap)
            if x < y - 1:
                heapq.heappush(heap, (A[x + 1] * 1.0 / A[y], x + 1, y))
            K -= 1
            if K == 0:
                return [A[x], A[y]]
''',
    call='Solution().kthSmallestPrimeFraction([1, 2, 3, 5], 3)',
    expect=[2, 5],
    views=[
        dict(type='array', var='A', label='A：蓝 = 分子下标 x，粉 = 分母下标 y（刚弹出的分数 A[x]/A[y]）', cell=84, h=190,
             pointers={'x': 'blue', 'y': 'pink'}),
        dict(type='heap', var='heap', fmt=_fr, h=300),
        dict(type='text', size=28, fn=lambda S: (
            f"刚弹出 `{S['A'][S['x']]}/{S['A'][S['y']]}` = =={S['v']:.3g}==，还剩 `K = {S['K']}`" if 'v' in S and 'x' in S else '')),
    ],
    watch=[('K', 'K', 'orange'), 'x', 'y', ('v', lambda S: None if 'v' not in S else round(S['v'], 3), 'green')],
    skip=['n = len(A)', 'pos_list'],
    captions={
        'for index in range(1, n)': '分母 `A[{index}]` 对应矩阵的一行，行首是最小分子 `A[0]`',
        'heapq.heappush(heap, (A[0]': '`{A[0]}/{A[index]}` 入堆：每一行（固定分母）最小的数都在堆里',
        'while K': lambda S, B, r: (f'还要再弹 `K = {S.K}` 次' if S.K else '`K = 0`，结束'),
        'heappop': '堆顶是所有行里最小的分数 `{A[x]}/{A[y]}` = =={v:.3g}=={""}，这就是整个矩阵当前最小',
        'if x < y - 1': lambda S, B, r: (f'`x = {S.x} < y - 1 = {S.y - 1}` → 这一行还有下一个分子，把它补进堆' if S.x < S.y - 1
                                         else f'`x = {S.x}` 已经挨着 y（分子必须小于分母），这一行没有下一个了'),
        'heapq.heappush(heap, (A[x + 1]': '同一行下一个：`{A[x+1]}/{A[y]}` 入堆，保证每行最小的仍在堆中',
        'K -= 1': '已经弹出一个最小值，`K` → {K}',
        'if K == 0': lambda S, B, r: (f'`K = 0`：刚弹出的就是第 K 小 → 返回 `[{S.A[S.x]}, {S.A[S.y]}]`' if S.K == 0
                                      else f'`K = {S.K}` 还没弹够，继续'),
        'return [A[x], A[y]]': '第 K 次弹出的分数 `{A[x]}/{A[y]}` 就是答案 → `{ret}`',
    },
    cards=dict(
        one_liner='把分数看成行列递增的矩阵，用最小堆弹 K 次',
        complexity='时间 `O((n + K) log n)`，空间 `O(n)`',
        problem=['有序数组 `A`（1 和素数，升序），任取 `i < j` 组成分数 `A[i]/A[j]`',
                 '返回第 K 小的分数，格式 `[A[i], A[j]]`',
                 '本视频：`A = [1,2,3,5], K = 3` → `[2, 5]`'],
        quote='我的做法是维护最小堆，初始化的时候将所有的1/m加入到堆中。接下来执行k轮，每轮弹出堆中最小值，同时将最小值所在行的下一个数加入到堆中。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定分母 `A[j]`，分子越大分数越大 → 每一行都是递增的',
              '堆里始终放着==每一行最小的那个==，所以堆顶就是全局最小',
              '弹出后把同一行的下一个补进去，弹到第 K 次即答案'],
        summary=['时间 `O((n + K) log n)`，空间 `O(n)`',
                 '作者没有用二分：实数上二分再还原成分数比较麻烦',
                 '用浮点数做堆的键，分数值很接近时要留意精度',
                 '同类题：378. 有序矩阵中第 K 小的元素'],
    ),
)
