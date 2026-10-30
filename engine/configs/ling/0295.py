from collections import Counter as _C


def _added(S, B, name):
    """name 堆里新多出来的那个数"""
    d = _C(S.get(name) or []) - _C(B.get(name) or [])
    return next(iter(d), None)


def _mv(S, B, src, dst, what):
    x = _added(S, B, 'self.' + dst)
    head = f'先把 `{S.num}` 加到 {src}，再把 {src} 的{what} =={x}== 挪到 {dst}'
    if x == S.num:
        return head + f'（就是 `{S.num}` 自己）'
    return head + f'：`{S.num}` 留在 {src}，==保证 left 的数都 ≤ right 的数=='


def draw_split(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    left, right = S.get('self.left'), S.get('self.right')
    if left is None or right is None:
        return
    Ls, Rs = sorted(left), sorted(right)
    cell, gap = 70, 34
    total = (len(Ls) + len(Rs)) * cell + gap
    sx = x0 + (x1 - x0 - total) / 2
    y = y0 + 64
    cv.rich(x0 + 20, y0 + 6, '把所有数排好序看：中位数把它们==均分成两半==', x1 - x0 - 40, size=22, color=T['muted'], accent=T['orange'])
    xs = sx
    for k, v in enumerate(Ls):
        top = k == len(Ls) - 1
        cv.rect((xs + 3, y, xs + cell - 3, y + cell - 6), fill=T['blue'], r=8,
                outline=T['yellow'] if top else None, width=4 if top else 1)
        cv.text((xs + cell / 2, y + (cell - 6) / 2), v, 28, T['bg'], anchor='mm', bold=True)
        xs += cell
    dx = xs + gap / 2
    if Ls:
        cv.text((dx - 12, y + cell + 4), f'left（最大堆）{len(Ls)} 个', 20, T['blue'], anchor='rt', bold=True)
    cv.line([(dx, y - 14), (dx, y + cell + 6)], T['muted'], 3)
    xs += gap
    rs = xs
    for k, v in enumerate(Rs):
        top = k == 0
        cv.rect((xs + 3, y, xs + cell - 3, y + cell - 6), fill=T['pink'], r=8,
                outline=T['yellow'] if top else None, width=4 if top else 1)
        cv.text((xs + cell / 2, y + (cell - 6) / 2), v, 28, T['bg'], anchor='mm', bold=True)
        xs += cell
    if Rs:
        cv.text((dx + 12, y + cell + 4), f'right（最小堆）{len(Rs)} 个', 20, T['pink'], anchor='lt', bold=True)
    if Ls:
        med = Ls[-1] if len(Ls) > len(Rs) else (Ls[-1] + Rs[0]) / 2
        how = f'奇数个 → left 的最大值 {Ls[-1]}' if len(Ls) > len(Rs) else f'偶数个 → ({Ls[-1]} + {Rs[0]}) / 2'
        cv.text((x0 + 20, y + cell + 48), f'黄框 = 两个堆顶　　中位数 = {how} = {med:g}', 22, T['yellow'])


CONFIG = dict(
    num=295, title='数据流的中位数', difficulty='Hard', category='堆',
    author='灵茶山艾府', technique='对顶堆（最大堆 + 最小堆）',
    code='''
class MedianFinder:
    def __init__(self):
        self.left = []  # 最大堆
        self.right = []  # 最小堆

    def addNum(self, num: int) -> None:
        if len(self.left) == len(self.right):
            heappush_max(self.left, heappushpop(self.right, num))
        else:
            heappush(self.right, heappushpop_max(self.left, num))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return self.left[0]
        return (self.left[0] + self.right[0]) / 2
''',
    # Python 3.14 才自带 heappush_max / heappushpop_max；这里用 heapq 的内部函数补上（不被追踪）
    setup='''
def heappush_max(heap, item):
    heap.append(item)
    heapq._siftdown_max(heap, 0, len(heap) - 1)

def heappushpop_max(heap, item):
    if heap and heap[0] > item:
        item, heap[0] = heap[0], item
        heapq._siftup_max(heap, 0)
    return item
''',
    call='''mf = MedianFinder()
mf.addNum(1); mf.addNum(5); mf.findMedian(); mf.addNum(6); mf.findMedian(); mf.addNum(2); mf.addNum(3); mf.addNum(4)
mf.findMedian()''',
    expect=3.5,
    views=[
        dict(type='custom', draw=draw_split, h=250),
        dict(type='heap', var='self.left', label='self.left 最大堆', top_color='blue', h=120),
        dict(type='heap', var='self.right', label='self.right 最小堆', top_color='pink', h=120),
    ],
    watch=[('num', 'num', 'orange'), ('len(left)', lambda S: len(S['self.left']), 'blue'),
           ('len(right)', lambda S: len(S['self.right']), 'pink')],
    captions={
        'self.left = []': '`left` 存==较小的一半==，用最大堆（堆顶 = 最大值）',
        'self.right = []': '`right` 存==较大的一半==，用最小堆（堆顶 = 最小值）',
        'if len(self.left) == len(self.right)': lambda S, B, ret: (
            f'addNum({S.num})：两边一样多（{len(S["self.left"])} = {len(S["self.right"])}），规定奇数个时 ==left 多 1 个=='
            if len(S['self.left']) == len(S['self.right'])
            else f'addNum({S.num})：left 比 right 多 1 个，这次要让 ==right 多 1 个=='),
        'heappush_max(self.left, heappushpop(self.right, num))': lambda S, B, ret: _mv(S, B, 'right', 'left', '最小值'),
        'heappush(self.right, heappushpop_max(self.left, num))': lambda S, B, ret: _mv(S, B, 'left', 'right', '最大值'),
        'if len(self.left) > len(self.right)': lambda S, B, ret: (
            f'findMedian：一共 {len(S["self.left"]) + len(S["self.right"])} 个，' +
            ('==奇数个==，left 多 1 个' if len(S['self.left']) > len(S['self.right']) else '==偶数个==，两边一样多')),
        'return self.left[0]': '中位数 = left 的堆顶（较小一半的最大值）= =={ret}==',
        'return (self.left[0] + self.right[0]) / 2': '中位数 = (left 堆顶 + right 堆顶) / 2 = `({self.left[0]} + {self.right[0]}) / 2` = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='中位数把数据均分两半：小的一半放最大堆，大的一半放最小堆',
        complexity='addNum `O(log q)`，findMedian `O(1)`，空间 `O(q)`',
        problem=['实现 `MedianFinder`：`addNum(num)` 加入一个数，`findMedian()` 返回当前所有数的中位数',
                 '偶数个时中位数是中间两个数的平均值',
                 '本视频：依次加入 `1,5,6,2,3,4`，中途查询 → `3`、`5`、==3.5=='],
        quote='中位数……可将数值集合划分为相等的两部分……我们要计算的中位数，就来自 left 中的最大值，以及 right 中的最小值。',
        quote_src='—— 灵茶山艾府题解（引用百科定义）',
        idea=['保证：`left` 和 `right` 大小尽量相等（奇数个时 ==left 多 1 个==）；`left` 的数都 ≤ `right` 的数',
              '两边一样多：不管 `num` 大小，==先加到 right，再把 right 的最小值挪到 left==',
              'left 多 1 个：先加到 left，再把 left 的最大值挪到 right；需要“取最值 + 删最值”→ 用堆'],
        summary=['addNum 每次两次堆操作 `O(log q)`；findMedian 直接看堆顶 `O(1)`',
                 '“先放进对面再挪回来”把分类讨论合并成一行，==自动保证 left ≤ right==',
                 '`heappush_max` / `heappushpop_max` 是 Python 3.14 新增的；旧版本可把数取相反数存进最小堆',
                 '思考题：支持删除任意元素 → 480. 滑动窗口中位数'],
    ),
)
