CONFIG = dict(
    num=1167, title='连接棒材的最低费用', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈夫曼思路 · 最小堆',
    tags=['堆（优先队列）'],
    code='''
class Solution(object):
    def connectSticks(self, sticks):

        res = 0
        heapq.heapify(sticks)

        while len(sticks) > 1:
            first = heapq.heappop(sticks)
            second = heapq.heappop(sticks)
            first += second
            res += first
            heapq.heappush(sticks, first)
        
        return res
''',
    call='Solution().connectSticks([1,8,3,5,2])',
    expect=39,
    views=[
        dict(type='text', fn=lambda S: f"已花费 `{S['res']}`；堆里还剩 `{len(S['sticks'])}` 根棒子" if 'res' in S and 'sticks' in S else '', h=70),
        dict(type='heap', var='sticks', label='sticks（最小堆，最短的在最左）', h=220),
    ],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计总费用，每次连接的费用 = 两根棒子长度之和',
        'heapq.heapify': '把 `sticks` 原地堆化：最短的棒子在堆顶',
        'while len(sticks) > 1': lambda S, B, r: (f'堆里还有 `{len(S.sticks)}` 根，>1 → 还要继续连接' if len(S.sticks) > 1
                                                  else '只剩 1 根 → 全部连好了'),
        'first = heapq.heappop': '取出==最短==的一根：`first = {first}`',
        'second = heapq.heappop': '再取出==次短==的一根：`second = {second}`（哈夫曼：每次合并最短的两根）',
        'first += second': '连成一根：`{B.first} + {second}` = =={first}==',
        'res += first': '连接费用就是新棒子的长度：`res` = {B.res} + {first} = =={res}==',
        'heapq.heappush': '新棒子放回堆里，它可能还要被再次连接',
        'return res': '最低总费用 = =={ret}==',
    },
    cards=dict(
        one_liner='每次连接最短的两根，费用最省（哈夫曼树）',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地堆化）',
        problem=['`sticks[i]` 是棒材长度；把两根长 `x`、`y` 的棒材连接起来要花费 `x + y`',
                 '把所有棒材连成一根，求最低总费用',
                 '示例：`[1,8,3,5,2]` → ==39=='],
        quote='非常标准的哈夫曼树构造问题，最直观的思路就是每次选择当前剩下棒子中最短的两根合并，重复此过程直到完成合并。',
        quote_src='—— yiduobo 题解原文',
        idea=['短的棒子会被反复计入费用，所以让它们先合并、==层数深==；长的晚一点合并',
              '用堆维护剩余棒子：每轮取出堆顶两根，相加后记入答案',
              '合并后的新棒子再放回堆里，直到只剩一根'],
        summary=['时间 `O(n log n)`，`heapify` 本身 `O(n)`',
                 '费用累加的是==合并后的长度==，不是两根各自的长度',
                 '原文直接对入参 `sticks` 原地堆化，会改变输入',
                 '作者说明这个贪心的正确性证明较麻烦，文中没有展开',
                 '同类题：1046 最后一块石头的重量、合并果子'],
    ),
)
