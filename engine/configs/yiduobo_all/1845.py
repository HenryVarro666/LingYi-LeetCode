N = 5


def _seats(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    heap = S.get('self.heap')
    if heap is None:
        return
    free = set(heap)
    cv.text((x0 + 18, y0 + 4), f'座位 1..{N}（绿 = 可预约，蓝 = 已预约；黄框 = 这一步变化的座位）', 22, T['muted'], bold=True)
    bfree = set(B.get('self.heap') or [])
    cell = min(110, (x1 - x0 - 60) / N)
    for i in range(1, N + 1):
        X = x0 + 30 + (i - 1) * cell
        y = y0 + 70
        changed = (i in free) != (i in bfree) and B.get('self.heap') is not None
        cv.rect((X + 5, y, X + cell - 5, y + cell * 0.8), fill=T['green'] if i in free else T['blue'], r=10,
                outline=T['yellow'] if changed else None, width=5)
        cv.text((X + cell / 2, y + cell * 0.4), i, 36, T['bg'], anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num=1845, title='座位预约管理系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最小堆（直接用 heapq）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1429'],
    code='''
class SeatManager(object):

    def __init__(self, n):
        self.heap = list(range(1, n + 1))

    def reserve(self):
        return heapq.heappop(self.heap)

    def unreserve(self, seatNumber):
        heapq.heappush(self.heap, seatNumber)

''',
    call='''sm = SeatManager(5)
out = []
out.append(sm.reserve())
out.append(sm.reserve())
sm.unreserve(2)
out.append(sm.reserve())
out.append(sm.reserve())
out.append(sm.reserve())
out.append(sm.reserve())
sm.unreserve(5)
out''',
    expect=[1, 2, 2, 3, 4, 5],
    views=[
        dict(type='custom', draw=_seats, h=190),
        dict(type='heap', var='self.heap', label='self.heap：可预约的座位（堆顶 = 最小编号）', top_color='green', h=170),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=[('可预约', 'self.heap', 'green'), ('seatNumber', lambda S: S.get('seatNumber'), 'orange'), ('返回值', lambda S: S.get('out'), 'blue')],
    captions={
        'self.heap = list': '`SeatManager(5)`：把 `1..5` 做成一个最小堆（有序数组本身就是合法的堆）',
        'heapq.heappop': '弹出堆顶 `{ret}`：当前可预约座位里编号最小的，它变为不可预约 → 返回 =={ret}==',
        'heapq.heappush': lambda S, B, r: f'`{S.seatNumber}` 号座位重新可以预约：入堆，堆里现在是 =={sorted(S["self.heap"])}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='三个操作 = 建堆、弹堆顶、入堆',
        complexity='初始化 `O(n)`，`reserve` / `unreserve` 均 `O(log n)`',
        problem=['管理座位 `1..n`：`reserve()` 返回可预约的==最小编号==并占用',
                 '`unreserve(x)` 把 `x` 重新变为可预约',
                 '本视频：`n = 5`，操作后依次返回 `[1,2,2,3,4,5]`'],
        quote='非常直观的使用堆的题目，题目中的三种操作分别对应了建堆、弹出堆顶和入堆三种操作。',
        quote_src='—— yiduobo 题解',
        idea=['需求是「每次取最小」+「随时放回」→ 最小堆',
              '构造函数：把 `1..n` 全放进堆；`reserve` = `heappop`；`unreserve` = `heappush`',
              '原文说有兴趣可以手动实现堆，这里直接用 `heapq`'],
        summary=['初始化 `O(n)`，其余操作 `O(log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`range(1, n + 1)` 在 Python 3 里不是列表，已改为 `list(range(1, n + 1))`',
                 '易错：`n` 很大时（如 `10^9`）这种写法会爆内存，只在 `n ≤ 10^5` 时适用',
                 '同类题：3275 第 K 近障碍物查询、2208 将数组和减半的最少操作次数'],
    ),
)
