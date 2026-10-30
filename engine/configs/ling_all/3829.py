CALL = '''r = RideSharingSystem()
out = []
r.addRider(3)
r.addDriver(2)
r.addRider(1)
out.append(r.matchDriverWithRider())
r.addDriver(5)
r.cancelRider(3)
r.addRider(4)
r.cancelRider(1)
out.append(r.matchDriverWithRider())
out.append(r.matchDriverWithRider())
out'''


def _clean(S, B, ret):
    rd, w = S['self.riders'], S['self.waiting_riders']
    if not rd:
        return '乘客队列空了，没有乘客可检查'
    if rd[0] not in w:
        return f'队首乘客 `{rd[0]}` 已不在 `waiting_riders`：他取消过 → 要弹掉'
    return f'队首乘客 `{rd[0]}` 仍有效，停止清理'


def _chk(S, B, ret):
    if not S['self.riders'] or not S['self.drivers']:
        return '乘客或司机有一边为空 → 无法匹配'
    return '双方都有人：队首乘客与队首司机可以配对'


def _disc(S, B, ret):
    if S['riderId'] in B['self.riders']:
        return f"乘客 `{S['riderId']}` 还在队列里 → 从集合删掉；队列里的他等到队首再清理"
    return f"乘客 `{S['riderId']}` 早已被匹配、不在队列里 → 取消无效（只是顺手清掉集合里残留的编号）"


CONFIG = dict(
    num=3829, title='设计共享出行系统', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='双队列 + 哈希集合',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1594'],
    code='''
class RideSharingSystem:
    def __init__(self):
        self.riders = deque()
        self.drivers = deque()
        self.waiting_riders = set()

    def addRider(self, riderId: int) -> None:
        self.riders.append(riderId)
        self.waiting_riders.add(riderId)

    def addDriver(self, driverId: int) -> None:
        self.drivers.append(driverId)

    def matchDriverWithRider(self) -> List[int]:
        # 弹出队列中的已取消乘客
        while self.riders and self.riders[0] not in self.waiting_riders:
            self.riders.popleft()
        # 没有乘客或者司机
        if not self.riders or not self.drivers:
            return [-1, -1]
        # 配对（这里没有删除 waiting_riders 中的乘客编号，面试的话建议写上删除的逻辑）
        return [self.drivers.popleft(), self.riders.popleft()]

    def cancelRider(self, riderId: int) -> None:
        self.waiting_riders.discard(riderId)
''',
    call=CALL,
    expect=[[2, 3], [5, 4], [-1, -1]],
    views=[
        dict(type='queue', var='self.riders', label='riders 乘客队列（队首在左，先来先匹配）', fmt=lambda x: str(x), h=110),
        dict(type='queue', var='self.drivers', label='drivers 司机队列（队首在左）', fmt=lambda x: str(x), h=110),
        dict(type='set', var='self.waiting_riders', label='waiting_riders（在队列中且没取消的乘客）', fmt=lambda x: str(x), h=110),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=['riderId', 'driverId', ('out', 'out', 'green')],
    captions={
        'self.riders = deque()': '乘客按到达顺序排队：==队列==',
        'self.drivers = deque()': '司机也按到达顺序排队：再来一个队列',
        'self.waiting_riders = set()': '哈希集合：记录==在队列中且没取消==的乘客，用来做取消',
        'self.riders.append': '乘客 `{riderId}` 排到队尾',
        'self.waiting_riders.add': '同时记入 `waiting_riders`：他现在是有效乘客',
        'self.drivers.append': '司机 `{driverId}` 排到队尾，先到的先被匹配',
        'while self.riders and': _clean,
        17: '弹出已取消的乘客（==惰性删除==：取消时不动队列，到队首才清理）',
        'if not self.riders or not self.drivers': _chk,
        'return [-1, -1]': '没有可用匹配，返回 `[-1, -1]`',
        22: '最早的司机配最早的乘客，一起出队：返回 `{ret}`',
        'self.waiting_riders.discard': _disc,
    },
    cards=dict(
        one_liner='先来先匹配用两个队列，取消用集合做标记',
        complexity='match 均摊 `O(1)`，其余 `O(1)`；空间 `O(q)`',
        problem=['系统按到达顺序匹配==最早空闲的司机==和==最早等待的乘客==',
                 '`addRider` / `addDriver` 入队，`cancelRider` 取消乘客，`match` 返回 `[司机, 乘客]`，没有则 `[-1, -1]`',
                 '示例：加乘客 3、司机 2，匹配得 `[2, 3]`'],
        quote='既然是先来先匹配，那就用两个队列，分别保存乘客编号和司机编号。',
        quote_src='—— 灵茶山艾府题解',
        idea=['乘客、司机各一个队列，队首就是最早到的',
              '取消不去队列里找人（太慢），只把编号从 `waiting_riders` 删掉',
              '匹配时先把队首已取消的乘客弹掉，再配对'],
        summary=['每个乘客入队出队各一次，所以 match 均摊 `O(1)`',
                 '易错：必须先清理队首的已取消乘客，再判断队列是否为空',
                 '灵神吐槽：没叫车的乘客也能取消，所以用 `discard` 而不是 `remove`',
                 '原文提示：配对后没删 `waiting_riders`，面试建议写上删除逻辑'],
    ),
)
