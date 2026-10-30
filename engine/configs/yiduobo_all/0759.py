SCHED = [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]


def _busy(S):
    b = [list(p) for p in S.get('busy_time', [])]
    if S.get('nowx') is not None and not (b and b[-1] == [S['nowx'], S['nowy']]):
        b.append([S['nowx'], S['nowy']])
    return b


def _free(S):
    return [[i.start, i.end] for i in S.get('res', [])]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴：蓝 = 合并后的忙碌时间，绿 = 空闲时间', 22, T['muted'], bold=True)
    lo, hi = 1, 10
    L, R = x0 + 50, x1 - 50
    X = lambda v: L + (v - lo) / (hi - lo) * (R - L)
    y = y0 + 50
    for name, rows, c in (('busy_time（含正在合并的段）', _busy(S), T['blue']), ('res 空闲', _free(S), T['green'])):
        cv.text((x0 + 18, y), name, 20, T['muted'])
        y += 28
        if not rows:
            y += 26
        for a, b in rows:
            cv.rect((X(a), y, max(X(b), X(a) + 6), y + 20), fill=c, r=10)
            cv.text((X(a) - 6, y + 10), str(a), 18, T['muted'], anchor='rm')
            cv.text((max(X(b), X(a) + 6) + 6, y + 10), str(b), 18, T['muted'], anchor='lm')
            y += 28
        y += 14
    for v in range(lo, hi + 1):
        cv.text((X(v), y1 - 26), str(v), 16, T['dim'], anchor='mt')


def _top(S):
    s = '　'.join(f"员工{k}: " + ' '.join(f'[{a},{b}]' for a, b in e) for k, e in enumerate(SCHED))
    return s


def _pop(S, B, ret):
    x, y, idx = S.x, S.y, S.index
    if B.nowx is None:
        return f'弹出最小起点的区间 `[{x},{y}]`（员工{idx}）：第一个区间，当作 ==当前合并段=='
    if B.nowy < x:
        return f'弹出 `[{x},{y}]`：起点 `{x}` > 当前合并段终点 `{B.nowy}` → 中间有缝，`[{B.nowx},{B.nowy}]` ==固定为一段忙碌时间==，从 `[{x},{y}]` 重新开始'
    return f'弹出 `[{x},{y}]`：起点 `{x}` ≤ 终点 `{B.nowy}`，重叠 → 终点取 `max({B.nowy}, {y}) = {max(B.nowy, y)}`'


CONFIG = dict(
    num=759, title='员工空闲时间', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='堆多路归并忙碌区间 + 取补集',
    tags=['常用数据结构', '贪心与思维'],
    setup='''
class Interval(object):
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
    def __repr__(self):
        return f'[{self.start},{self.end}]'

_sched = [[Interval(1, 2), Interval(5, 6)], [Interval(1, 3)], [Interval(4, 10)]]
''',
    code='''
class Solution(object):
    def employeeFreeTime(self, schedule):

        heap = []
        n = len(schedule)
        pos = [0] * n
        for index, sch in enumerate(schedule):
            if len(sch) > 0:
                heapq.heappush(heap, [sch[0].start, sch[0].end, index])
                pos[index] += 1
        
        nowx, nowy = None, None
        busy_time = []
        while heap:
            x, y, index = heapq.heappop(heap)
            if nowx is None or nowy < x:
                if nowx is not None:
                    busy_time.append([nowx, nowy])
                nowx, nowy = x, y
            else:
                nowy = max(nowy, y)
            
            if pos[index] < len(schedule[index]):
                heapq.heappush(heap, [schedule[index][pos[index]].start, schedule[index][pos[index]].end, index])
                pos[index] += 1

        busy_time.append([nowx, nowy])

        res = []
        for index in range(1, len(busy_time)):
            if busy_time[index][0] > busy_time[index - 1][1]:
                res.append(Interval(busy_time[index - 1][1], busy_time[index][0]))
        
        return res
''',
    call='Solution().employeeFreeTime(_sched)',
    result_fn=lambda r: [[i.start, i.end] for i in r],
    expect=[[3, 4]],
    views=[
        dict(type='text', fn=lambda S: '输入 ' + _top(S), size=22, h=64),
        dict(type='heap', var='heap', fmt=lambda x: f'[{x[0]},{x[1]}]#{x[2]}', label='heap：[起点,终点]#员工号（每人一个）', top_color='yellow', h=130),
        dict(type='custom', draw=_draw, h=270),
        dict(type='text', fn=lambda S: (f"当前合并段 `[{S['nowx']}, {S['nowy']}]`" if S.get('nowx') is not None else ''), h=50),
    ],
    watch=[('x,y', lambda S: (S['x'], S['y']) if 'x' in S else '-', 'yellow'), ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'pink'),
           ('busy_time', 'busy_time', 'cyan')],
    captions={
        'heap = []': '`heap` 做多路归并：每位员工各出一个==当前最靠前的区间==',
        'pos = [0] * n': '`pos[i]`：员工 i 下一个要入堆的区间下标',
        'heapq.heappush(heap, [sch[0]': '员工 `{index}` 的第一个区间入堆：`[{heap[0][0] if False else sch[0].start}, {sch[0].end}]`，`pos[{index}] = 1`',
        'nowx, nowy = None, None': '`nowx, nowy` 是正在合并的忙碌段，先置空',
        'while heap': lambda S, B, r: (f'堆里还有 `{len(S.heap)}` 个区间，继续' if S.heap else '堆空了：所有区间都处理完'),
        'x, y, index = heapq.heappop(heap)': '堆顶 = 所有员工里起点最小的区间 `[{x}, {y}]`（员工 {index}）',
        'if nowx is None or nowy < x': _pop,
        'busy_time.append([nowx, nowy])': lambda S, B, r: f'忙碌段 `[{B.nowx}, {B.nowy}]` 加入 `busy_time`',
        'nowx, nowy = x, y': '新的合并段从 `[{x}, {y}]` 开始',
        'nowy = max(nowy, y)': '重叠：合并段终点更新为 `{nowy}`',
        'if pos[index] < len(schedule[index])': '员工 {index} 还有区间吗？`pos = {pos[index]}`，共 `{len(schedule[index])}` 个',
        'heapq.heappush(heap, [schedule': '员工 {index} 的下一个区间入堆，补上刚弹出的位置，`pos[{index}] = {pos[index]}`',
        'if nowx is not None': lambda S, B, r: ('还没有合并段（`nowx` 为空）：不用保存，直接开始新段' if S.nowx is None else f'已有合并段 `[{S.nowx},{S.nowy}]`：==先把它存进 busy_time=='),
        'res = []': '忙碌时间已经合并完：相邻两段之间的缝就是==所有人都空闲==的时间',
        'if busy_time[index][0] > busy_time[index - 1][1]': '第 `{index}` 段起点 `{busy_time[index][0]}` 对比 前一段终点 `{busy_time[index-1][1]}`',
        'res.append': '有缝：空闲区间 `[{busy_time[index-1][1]}, {busy_time[index][0]}]`',
        'return res': '返回空闲区间 `{ret}`',
    },
    cards=dict(
        one_liner='空闲 = 忙碌并集的补集：先合并所有人的忙碌时间，再取相邻缝隙',
        complexity='时间 `O(N log k)`（N 个区间，k 位员工），空间 `O(k + N)`',
        problem=['给出每位员工的==忙碌==时间段（每人已按时间排序），求所有员工==共同空闲==的有限区间',
                 '示例：`[[[1,2],[5,6]],[[1,3]],[[4,10]]]` → `[[3,4]]`',
                 '空闲区间是 `Interval` 对象，不含 `-inf`、`+inf` 两端'],
        quote='补集的交集相当于并集的补集，那么在这里可以先求这些忙碌时间段的并集，然后再反推空闲的时间。……不过注意到每个人的时间段都已经排好序了，那么也可以采用堆辅助的多路归并的方法来合并区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['「所有人都空闲」= 取补再取交，但转成「忙碌的并集」的补集更简单',
              '每人的区间已有序：堆里只放每人下一个区间，弹出的就是全局起点最小的',
              '合并后相邻忙碌段的缝，就是答案'],
        summary=['时间 `O(N log k)`，不用把全部区间排序',
                 '合并条件是 `nowy < x` 才断开；`x == nowy` 视为相接，仍合并',
                 '最后一段忙碌时间要在循环外补加入 `busy_time`',
                 '原文 `Interval` 类在注释里，本视频在 `setup` 里补了一个等价的定义',
                 '这是会员题：只有一个缝时返回的是 `Interval` 对象列表'],
    ),
)
