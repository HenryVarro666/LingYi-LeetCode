def draw_split(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    first, second = S.get('self.fisrt_heap'), S.get('self.second_heap')
    if first is None or second is None:
        return
    Ls, Rs = sorted(-x for x in first), sorted(second)
    cell, gap = 66, 34
    total = (len(Ls) + len(Rs)) * cell + gap
    sx = x0 + (x1 - x0 - total) / 2
    y = y0 + 64
    cv.rich(x0 + 20, y0 + 6, '排好序看：==小数堆==放较小的 `n/2` 个，==大数堆==放其余的（奇数个时大数堆多 1 个）',
            x1 - x0 - 40, size=21, color=T['muted'], accent=T['orange'])
    xs = sx
    for k, v in enumerate(Ls):
        top = k == len(Ls) - 1
        cv.rect((xs + 3, y, xs + cell - 3, y + cell - 6), fill=T['blue'], r=8,
                outline=T['yellow'] if top else None, width=4 if top else 1)
        cv.text((xs + cell / 2, y + (cell - 6) / 2), v, 27, T['bg'], anchor='mm', bold=True)
        xs += cell
    dx = xs + gap / 2
    cv.line([(dx, y - 14), (dx, y + cell + 6)], T['muted'], 3)
    if Ls:
        cv.text((dx - 12, y + cell + 4), f'小数堆 {len(Ls)} 个', 20, T['blue'], anchor='rt', bold=True)
    xs += gap
    for k, v in enumerate(Rs):
        top = k == 0
        cv.rect((xs + 3, y, xs + cell - 3, y + cell - 6), fill=T['pink'], r=8,
                outline=T['yellow'] if top else None, width=4 if top else 1)
        cv.text((xs + cell / 2, y + (cell - 6) / 2), v, 27, T['bg'], anchor='mm', bold=True)
        xs += cell
    if Rs:
        cv.text((dx + 12, y + cell + 4), f'大数堆 {len(Rs)} 个', 20, T['pink'], anchor='lt', bold=True)
    num = S.get('num')
    if isinstance(num, int) and 'num' in S:
        cv.text((x1 - 24, y0 + 40), f'新来的 num = {num}', 22, T['orange'], anchor='ra', bold=True)
    if Rs and 'num' not in S:  # addNum 中途两堆可能暂时不平衡，只在 findMedian 时显示
        if len(Ls) < len(Rs):
            how = f'奇数个 → 大数堆最小的 {Rs[0]}'
            med = Rs[0]
        else:
            how = f'偶数个 → ({Ls[-1]} + {Rs[0]}) / 2'
            med = (Ls[-1] + Rs[0]) / 2
        cv.text((x0 + 20, y + cell + 48), f'黄框 = max_of_min / min_of_max　　中位数 = {how} = {med:g}', 21, T['yellow'])


def _cmp(S, B, ret):
    num, top = S.num, S['self.second_heap'][0]
    if num >= top:
        return f'`num = {num} ≥ min_of_max = {top}`：==num 属于较大的那一部分=='
    return f'`num = {num} < min_of_max = {top}`：不属于较大的部分'


CONFIG = dict(
    num=295, title='数据流的中位数', difficulty='Hard', category='堆',
    author='yiduobo', technique='双堆 · 分三种大小关系讨论',
    code='''
import heapq

class MedianFinder(object):

    def __init__(self):
        self.fisrt_heap = []
        self.second_heap = []

    def addNum(self, num):
        if not self.fisrt_heap:
            if not self.second_heap:
                heapq.heappush(self.second_heap, num)
            else:
                if self.second_heap[0] < num:
                    min_of_second = heapq.heappop(self.second_heap)
                    num, min_of_second = min_of_second, num
                    heapq.heappush(self.second_heap, min_of_second)
                heapq.heappush(self.fisrt_heap, -num)
        else:
            if num >= self.second_heap[0]:
                if len(self.fisrt_heap) < len(self.second_heap):
                    min_of_second = heapq.heappop(self.second_heap)
                    heapq.heappush(self.fisrt_heap, -min_of_second)
                heapq.heappush(self.second_heap, num)
            elif num <= -self.fisrt_heap[0]:
                if len(self.fisrt_heap) == len(self.second_heap):
                    max_of_fisrt = heapq.heappop(self.fisrt_heap)
                    heapq.heappush(self.second_heap, -max_of_fisrt)
                heapq.heappush(self.fisrt_heap, -num)
            else:
                if len(self.fisrt_heap) < len(self.second_heap):
                    heapq.heappush(self.fisrt_heap, -num)
                else:
                    heapq.heappush(self.second_heap, num)

    def findMedian(self):
        if len(self.fisrt_heap) < len(self.second_heap):
            return self.second_heap[0]
        else:
            return (-self.fisrt_heap[0] + self.second_heap[0]) / 2.0
''',
    call='''mf = MedianFinder()
mf.addNum(1); mf.addNum(5); mf.addNum(6); mf.findMedian(); mf.addNum(2); mf.addNum(3); mf.addNum(4); mf.findMedian(); mf.addNum(0)
mf.findMedian()''',
    expect=3,
    views=[
        dict(type='custom', draw=draw_split, h=250),
        dict(type='heap', var='self.fisrt_heap', label='fisrt_heap 小数堆（存 -x，堆顶 = -max_of_min）', h=120),
        dict(type='heap', var='self.second_heap', label='second_heap 大数堆（最小堆，堆顶 = min_of_max）', h=120),
    ],
    watch=[('num', 'num', 'orange'), ('小数堆个数', lambda S: len(S['self.fisrt_heap']), 'blue'),
           ('大数堆个数', lambda S: len(S['self.second_heap']), 'pink')],
    captions={
        'self.fisrt_heap = []': '小数堆：保存较小的 `n/2` 个数，存相反数模拟最大堆',
        'self.second_heap = []': '大数堆：保存较大的数（最小堆），奇数个时多 1 个',
        'if not self.fisrt_heap:': lambda S, B, ret: (f'addNum({S.num})：小数堆为空 → 特殊处理' if not S['self.fisrt_heap']
                                                      else f'addNum({S.num})：两个堆中都有数，要比较三个数的大小关系'),
        'if not self.second_heap:': lambda S, B, ret: ('大数堆也为空 → 根据约定加入大数堆' if not S['self.second_heap']
                                                       else '大数堆有数、小数堆没有：对比 `min_of_max` 和 num'),
        12: '根据约定，第一个数加入大数堆',
        24: '`{num}` 加入大数堆',
        34: '`{num}` 加入大数堆，现在大数堆多 1 个',
        21: lambda S, B, ret: ('小数堆比大数堆少：num 进大数堆之前，先把 `min_of_max` 挪去小数堆'
                               if len(S['self.fisrt_heap']) < len(S['self.second_heap']) else '两堆一样多：num 直接进大数堆，大数堆多 1 个'),
        31: lambda S, B, ret: (f'小数堆更少 → `{S.num}` 放小数堆' if len(S['self.fisrt_heap']) < len(S['self.second_heap'])
                               else f'两堆一样多 → `{S.num}` 放大数堆'),
        37: lambda S, B, ret: (f'findMedian：小数堆 {len(S["self.fisrt_heap"])} 个 < 大数堆 {len(S["self.second_heap"])} 个 → ==奇数个=='
                               if len(S['self.fisrt_heap']) < len(S['self.second_heap'])
                               else f'findMedian：两堆各 {len(S["self.second_heap"])} 个 → ==偶数个=='),
        'if self.second_heap[0] < num': lambda S, B, ret: (
            f'`min_of_max = {S["self.second_heap"][0]} < num = {S.num}`：num 应该进大数堆，`min_of_max` 换到小数堆'
            if S['self.second_heap'][0] < S.num else f'`min_of_max ≥ num`：num 直接进小数堆'),
        'min_of_second = heapq.heappop(self.second_heap)': '弹出大数堆最小的数 `{min_of_second}`',
        'num, min_of_second = min_of_second, num': '交换：`num` ← {num}，`min_of_second` ← {min_of_second}',
        'heapq.heappush(self.second_heap, min_of_second)': '`{min_of_second}` 放回大数堆',
        'heapq.heappush(self.fisrt_heap, -num)': '`{num}` 加入小数堆（存的是 `{-num}`）',
        'if num >= self.second_heap[0]': _cmp,
        'heapq.heappush(self.fisrt_heap, -min_of_second)': '大数堆最小的 `{min_of_second}` 挪去小数堆，给 num 腾位置',
        'elif num <= -self.fisrt_heap[0]': lambda S, B, ret: (
            f'`num = {S.num} ≤ max_of_min = {-S["self.fisrt_heap"][0]}`：==num 属于较小的那一部分=='
            if S.num <= -S['self.fisrt_heap'][0]
            else f'`max_of_min = {-S["self.fisrt_heap"][0]} < num < min_of_max = {S["self.second_heap"][0]}`：==夹在中间==，放哪边都行'),
        'if len(self.fisrt_heap) == len(self.second_heap)': lambda S, B, ret: (
            '两堆一样多：为了奇数时“大数堆多 1 个”的约定，先把 `max_of_min` 挪到大数堆'
            if len(S['self.fisrt_heap']) == len(S['self.second_heap']) else '小数堆更少，不用挪'),
        'max_of_fisrt = heapq.heappop(self.fisrt_heap)': '弹出小数堆的最大数 `{-max_of_fisrt}`（存的是 `{max_of_fisrt}`）',
        'heapq.heappush(self.second_heap, -max_of_fisrt)': '`{-max_of_fisrt}` 加入大数堆',
        'return self.second_heap[0]': '奇数个 → 第 `n/2+1` 大的数就是大数堆最小的数 =={ret}==',
        'return (-self.fisrt_heap[0] + self.second_heap[0]) / 2.0': '偶数个 → `(max_of_min + min_of_max) / 2` = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='只关心最中间的一两个数：用小数堆、大数堆把数据劈成两半',
        complexity='addNum `O(log n)`，findMedian `O(1)`',
        problem=['实现 `MedianFinder`：`addNum(num)` 加入一个数，`findMedian()` 返回当前所有数的中位数',
                 '偶数个时中位数是中间两个数的平均值',
                 '本视频：依次加入 `1,5,6`（中位数 5）、`2,3,4`（3.5）、`0`（==3==）'],
        quote='每次需要查找的只是当前数据结构中最中间的一个或者两个数，那么可以使用两个堆来解决……分别保存当前数据较大的n/2个数以及较小的n/2个数。',
        quote_src='—— yiduobo 题解',
        idea=['约定：n 为奇数时==大数堆多 1 个==，中位数 = 大数堆最小的 `min_of_max`；偶数时取两堆顶平均',
              '`num ≥ min_of_max` 进大数堆，`num ≤ max_of_min` 进小数堆，否则夹在中间',
              '放进去之前先看数量：会破坏约定就先把对面的堆顶挪过去'],
        summary=['最多三次堆操作 `O(log n)`；查询只看堆顶 `O(1)`',
                 '和灵神写法相比：这里是==大数堆多 1 个==，并显式分三种大小关系讨论',
                 'Python 只有最小堆：小数堆存 `-num` 来模拟最大堆',
                 '原文为 Python 2 写法：删去了文档字符串和模板注释，`/ 2.0` 照常可用'],
    ),
)
