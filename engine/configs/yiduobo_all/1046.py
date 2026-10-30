CONFIG = dict(
    num=1046, title='最后一块石头的重量', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='大顶堆模拟（存负数）',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def lastStoneWeight(self, stones):

        heap = [-x for x in stones]
        heapq.heapify(heap)

        while len(heap) > 1:
            num1 = -heapq.heappop(heap)
            num2 = -heapq.heappop(heap)
            num1 -= num2
            if num1 > 0:
                heapq.heappush(heap, -num1)
        
        if not heap:
            return 0
        return -heap[0]
''',
    call='Solution().lastStoneWeight([2,7,4,1,8,1])',
    expect=1,
    views=[
        dict(type='heap', var='heap', fmt=lambda x: str(-x), label='heap（存负数，图中显示重量）', top_color='orange', h=330),
        dict(type='text', fn=lambda S: (f"这一轮：`{S['num1']} − {S['num2']}` = =={S['num1']}==" if 'num2' in S and 'num1' in S and S.get('_line') in (10, 11) else ''), h=60),
    ],
    watch=[('num1', lambda S: S.get('num1'), 'orange'), ('num2', lambda S: S.get('num2'), 'pink'), ('剩余块数', lambda S: len(S['heap']) if 'heap' in S else 0, 'green')],
    captions={
        'heap = [-x': '把石头取负数放进列表：Python 只有最小堆，==取负后最小堆的堆顶就是最重的石头==：`{heap}`',
        'heapq.heapify': '`heapify` 原地建堆：堆顶 `{heap[0]}`，即最重的石头 `{-heap[0]}`',
        'while len(heap) > 1': lambda S, B, r: (f'还剩 {len(S.heap)} 块石头，>= 2 块，==继续撞==' if len(S.heap) > 1 else f'只剩 {len(S.heap)} 块（或没有），停止'),
        'num1 = -': '取出最重的石头：`num1 = {num1}`',
        'num2 = -': '再取出第二重的石头：`num2 = {num2}`',
        'num1 -= num2': '两块相撞，较重的减去较轻的：`{B.num1} − {num2}` = =={num1}==（相等就都粉碎）',
        'if num1 > 0': lambda S, B, r: (f'`num1 = {S.num1}` > 0：还剩一块碎石，要放回堆里' if S.num1 > 0 else '`num1 = 0`：两块一样重，同归于尽，什么都不放回'),
        'heappush': '把剩下的 `{num1}` 放回堆（存 `-{num1}`），堆自动调整，下一轮它可能又是最重的',
        'if not heap': lambda S, B, r: '堆空了：全部粉碎，答案是 0' if not S.heap else f'堆里还剩 1 块：重量 `{-S.heap[0]}`',
        'return -heap[0]': '最后剩下的那块石头重量：=={ret}==',
    },
    cards=dict(
        one_liner='每次取最重的两块相撞，剩下的碎石放回堆里',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['一堆石头，每次选最重的两块相撞：相等则都粉碎，不等则剩下差值那块',
                 '最后至多剩一块，返回它的重量（没有则返回 0）',
                 '示例：`[2,7,4,1,8,1]` → `1`'],
        quote='由于这里石头的个数非常少，所以想怎么做都可以。我在这里采用的是堆来模拟这个过程，每次从堆中取出最重的两块石头，计算二者之差。',
        quote_src='—— yiduobo 题解原文',
        idea=['Python 的 `heapq` 只有最小堆 → ==所有数取负数==存进去',
              '每轮弹出两次，得到最重和次重的石头',
              '差大于 0 就把差值取负放回堆，直到堆里不足 2 块'],
        summary=['时间 `O(n log n)`：每块石头最多入堆、出堆有限次，每次 `O(log n)`',
                 '取负数是用最小堆当最大堆的常用技巧，==弹出后记得再取负还原==',
                 '最后分两种情况：堆空返回 0，否则返回 `-heap[0]`',
                 '原文为标准 Python 写法，未做改动'],
    ),
)
