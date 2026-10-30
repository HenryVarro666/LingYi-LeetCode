CONFIG = dict(
    num=2336, title='无限集中的最小数字', difficulty='Medium', category='设计',
    author='yiduobo', technique='计数器 mi + 加回小顶堆 + 去重集合',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class SmallestInfiniteSet(object):

    def __init__(self):
        self.mi = 1
        self.back_heap = []
        self.back_set = set()

    def popSmallest(self):
        if not self.back_heap:
            res = self.mi
            self.mi += 1
        else:
            res = heapq.heappop(self.back_heap)
            self.back_set.remove(res)
        
        return res

    def addBack(self, num):
        if num >= self.mi or num in self.back_set:
            return
        
        self.back_set.add(num)
        heapq.heappush(self.back_heap, num)
''',
    call='''s = SmallestInfiniteSet()
out = []
out.append(s.popSmallest())
out.append(s.popSmallest())
out.append(s.popSmallest())
s.addBack(2)
s.addBack(2)
s.addBack(5)
out.append(s.popSmallest())
out.append(s.popSmallest())
out''',
    expect=[1, 2, 3, 2, 4],
    views=[
        dict(type='text', fn=lambda S: f'`mi` = =={S["self.mi"]}==：从没被拿走过的最小数；已拿走 `1 ~ {S["self.mi"] - 1}`' if 'self.mi' in S else '', size=28, h=60),
        dict(type='heap', var='self.back_heap', label='back_heap（加回的数，小顶堆）', top_color='yellow', h=110),
        dict(type='set', var='self.back_set', label='back_set（已加回、还没被拿走的数）', h=110),
        dict(type='array', var='out', label='out（每次 popSmallest 的返回值）', h=110),
    ],
    watch=[('num', 'num', 'orange'), ('res', 'res', 'green')],
    captions={
        'self.mi = 1': '`mi` = 从来没被拿走过的最小数，一开始是 ==1==；集合是 1,2,3,…… 无限的',
        'self.back_heap = []': '`back_heap`：存被加回来的数，用小顶堆随时取最小',
        'self.back_set = set()': '`back_set`：记录哪些数已经在加回的堆里，防止重复加回',
        'if not self.back_heap': lambda S, B, ret: ('没有加回的数，答案就是 `mi`' if not S['self.back_heap'] else f'有加回的数 `{S["self.back_heap"][0]}`，它们都比 `mi` 小，==答案在堆里=='),
        'res = self.mi': '堆空 → 最小的数就是 `mi` = ==`{res}`==',
        'self.mi += 1': '`mi` 拿走了，下一个从没拿过的数是 ==`{self.mi}`==',
        'res = heapq.heappop': '加回的数都被拿走过，必然 < `mi`；弹出堆顶 ==`{res}`== 就是当前最小',
        'self.back_set.remove': '这个数不在集合里了：从 `back_set` 删除 `{res}`，以后还能再加回',
        'return res': 'popSmallest 返回 ==`{ret}`==',
        'if num >= self.mi or num in self.back_set': lambda S, B, ret: (
            f'addBack({S.num})：`{S.num} >= mi({S["self.mi"]})` 说明它还在集合里，不用加回' if S.num >= S['self.mi']
            else (f'addBack({S.num})：它已经在 `back_set` 里了，重复加回无效' if S.num in S['self.back_set'] else f'addBack({S.num})：`{S.num} < mi` 且不在 `back_set` → 之前被拿走过，需要加回')),
        20: '加回无效（`num` 已在集合里），直接返回',
        'self.back_set.add(num)': '`{num}` 记进 `back_set`，标记它已经在堆里',
        'heapq.heappush': '`{num}` 放进 `back_heap`，之后 popSmallest 会优先拿它',
    },
    max_steps=70,
    cards=dict(
        one_liner='mi 记“从没拿过的最小数”，被加回的数放进小顶堆',
        complexity='popSmallest / addBack 均 `O(log n)`',
        problem=['有一个包含所有正整数 `1,2,3,……` 的无限集合，实现 `SmallestInfiniteSet`',
                 '`popSmallest()` 删除并返回最小的数；`addBack(num)` 把 `num` 加回集合（已在集合里则无效）',
                 '本视频：连拿 3 次，再加回 `2,2,5`，再拿 2 次 → ==[1,2,3,2,4]=='],
        quote='修改一下 mi 的定义，表示当前还从未被拿走过的数中的最小值，这样一来即使有加回操作，mi 的迭代方式依然是不受影响的。',
        quote_src='—— yiduobo 题解',
        idea=['只拿不加回时，一个变量 `mi` 就够了：每次返回 `mi` 再 `+1`',
              '加回的数 ==一定比 `mi` 小==，用小顶堆 `back_heap` 取最小；堆不空就先拿堆顶',
              '`back_set` 防止同一个数被重复加回；`num >= mi` 的数本来就在集合里，直接忽略'],
        summary=['每次操作 `O(log n)`（堆的压入 / 弹出），空间 `O(n)`',
                 '`popSmallest`：堆空返回 `mi` 并 `mi += 1`，否则弹出堆顶并从集合删除',
                 '`addBack`：只有 `num < mi` 且不在 `back_set` 时才真正加回',
                 '易错：弹出堆顶后别忘了从 `back_set` 删除，否则这个数以后加不回去',
                 '原文标题里的题号写作 2236，实为 2336；代码在 Python 3 下可直接运行'],
    ),
)
