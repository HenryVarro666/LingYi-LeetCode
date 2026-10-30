def _room(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    seats = S.get('self.seats')
    av = set(S.get('self.available') or [])
    old = B.get('self.seats') or 0
    cv.text((x0 + 18, y0 + 4), '房间里的椅子（绿 = 空着，蓝 = 有人坐；黄框 = 刚新添的椅子）', 22, T['muted'], bold=True)
    if not seats:
        cv.text((x0 + 18, y0 + 70), '房间里还没有椅子', 26, T['dim'])
        return
    cell = min(96, (x1 - x0 - 60) / max(seats, 1))
    sx = x0 + 30
    y = y0 + 70
    for i in range(1, seats + 1):
        X = sx + (i - 1) * cell
        free = i in av
        cv.rect((X + 5, y, X + cell - 5, y + cell * 0.8), fill=T['green'] if free else T['blue'], r=10,
                outline=T['yellow'] if (i > old and i == seats and S.get('_line') == 9) else None, width=5)
        cv.text((X + cell / 2, y + cell * 0.4), i, 34, T['bg'], anchor='mm', bold=True, mono=True)
    cv.text((x0 + 30, y + cell * 0.8 + 18), f'一共 {seats} 把椅子，其中 {len(av)} 把空着', 22, T['text'])


CONFIG = dict(
    num=1845, title='座位预约管理系统', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最小堆维护取消预约的座位',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1429'],
    code='''
class SeatManager:
    def __init__(self, _: int):
        self.seats = 0  # 一开始没有椅子
        self.available = []

    def reserve(self) -> int:
        if self.available:  # 有空出来的椅子
            return heappop(self.available)  # 坐编号最小的
        self.seats += 1  # 添加一把新的椅子
        return self.seats

    def unreserve(self, seatNumber: int) -> None:
        heappush(self.available, seatNumber)  # 有人离开了椅子
''',
    call='''sm = SeatManager(5)
out = []
out.append(sm.reserve())
out.append(sm.reserve())
out.append(sm.reserve())
sm.unreserve(2)
sm.unreserve(1)
out.append(sm.reserve())
out.append(sm.reserve())
out.append(sm.reserve())
out''',
    expect=[1, 2, 3, 1, 2, 4],
    views=[
        dict(type='custom', draw=_room, h=210),
        dict(type='heap', var='self.available', label='self.available（最小堆：空出来的椅子编号，堆顶 = 最小）', top_color='green', h=170),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=[('seats', 'self.seats', 'blue'), ('空出来的', 'self.available', 'green'), ('返回值', lambda S: S.get('out'), 'orange')],
    captions={
        'self.seats = 0': '`SeatManager`：一开始==没有椅子==，`seats = 0`（不管 `n` 多大都不预先建座位）',
        'self.available = []': '最小堆 `available` 只存==空出来的==椅子编号，一开始为空',
        'if self.available': lambda S, B, r: ('堆里有空出来的椅子 `%s`，优先坐编号最小的' % sorted(S['self.available']) if S['self.available']
                                             else '没有空出来的椅子，只能添一把新的'),
        'return heappop': '弹出堆顶 `{ret}`：空椅子里编号最小的，坐上去 → 返回 =={ret}==',
        'self.seats += 1': '没有空椅子：添一把新椅子，编号恰好是 `{self.seats}`（新椅子编号一定比旧的都大）',
        'return self.seats': '新椅子就是最小的可预约编号 → 返回 =={ret}==',
        'heappush': lambda S, B, r: f'有人离开 `{S.seatNumber}` 号椅子，它重新空出来：入堆，堆里现在是 =={sorted(S["self.available"])}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='房间里先没有椅子：要坐就添一把，有人走了就优先坐空出来的',
        complexity='`reserve` / `unreserve` 均 `O(log q)`，空间 `O(q)`',
        problem=['设计 `SeatManager(n)`：座位编号 `1..n`',
                 '`reserve()` 返回==最小编号==的可预约座位；`unreserve(x)` 把 `x` 变回可预约',
                 '本视频：`reserve ×3`，`unreserve(2)`、`unreserve(1)`，再 `reserve ×3` → `[1,2,3,1,2,4]`'],
        quote='想象有一个空房间，一开始没有椅子。如果有人进入了房间，我们可以添加一把新的椅子给人坐（如果没有空出来的椅子）。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['方法一：把 `1..n` 全部入堆，`reserve` 弹堆顶，`unreserve` 入堆，但时空都和 `n` 有关',
              '方法二：只记==已经添过的椅子数== `seats`，和一个存「被取消的座位」的最小堆',
              '`reserve`：有空椅子就弹最小的，否则 `seats + 1` 添新椅子——新椅子的编号一定最大，所以顺序是对的'],
        summary=['`reserve`、`unreserve` 均 `O(log q)`，`q` 是 `unreserve` 的次数；初始化 `O(1)`',
                 '好处：即使 `n` 到 `10^9` 也不会超时、爆内存',
                 '易错：优先坐堆里的空椅子，只有堆空了才 `seats += 1`',
                 '方法一（初始 `1..n` 全入堆）更直观，但是 `O(n)` 时空'],
    ),
)
