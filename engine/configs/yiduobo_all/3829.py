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
    rd, w = S['self.riders'], S['self.waiting']
    if not rd:
        return '`riders` 空了'
    if rd[0] not in w:
        return f'队首乘客 `{rd[0]}` 不在 `waiting`：订单取消了 → 弹出'
    return f'队首乘客 `{rd[0]}` 还在 `waiting` → 有效，停止弹出'


def _cancel(S, B, ret):
    if S['riderId'] in S['self.waiting']:
        return f"`{S['riderId']}` 在 `waiting` 中 → 取消有效"
    return f"`{S['riderId']}` 不在 `waiting`（已匹配或不存在）→ 什么也不做"


CONFIG = dict(
    num=3829, title='设计共享出行系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='双队列 + 懒删除',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1594'],
    code='''
class RideSharingSystem(object):

    def __init__(self):
        self.drivers = deque()
        self.riders = deque()
        self.waiting = set()

    def addRider(self, riderId):
        self.riders.append(riderId)
        self.waiting.add(riderId)

    def addDriver(self, driverId):
        self.drivers.append(driverId)

    def matchDriverWithRider(self):
        if not self.drivers:
            return [-1, -1]

        while self.riders and self.riders[0] not in self.waiting:
            self.riders.popleft()

        if not self.riders:
            return [-1, -1]

        res = [self.drivers[0], self.riders[0]]
        self.drivers.popleft()
        self.riders.popleft()
        self.waiting.remove(res[1])
        return res

    def cancelRider(self, riderId):
        if riderId in self.waiting:
            self.waiting.remove(riderId)
''',
    call=CALL,
    expect=[[2, 3], [5, 4], [-1, -1]],
    views=[
        dict(type='queue', var='self.drivers', label='drivers 空闲司机队列（队首在左）', fmt=lambda x: str(x), h=110),
        dict(type='queue', var='self.riders', label='riders 等待乘客队列（队首在左）', fmt=lambda x: str(x), h=110),
        dict(type='set', var='self.waiting', label='waiting（还在等、没取消的乘客）', fmt=lambda x: str(x), h=110),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=['riderId', 'driverId', ('res', 'res', 'cyan'), ('out', 'out', 'green')],
    captions={
        'self.drivers = deque()': '`drivers`：空闲司机队列，新司机加到队尾',
        'self.riders = deque()': '`riders`：等待乘客队列',
        'self.waiting = set()': '`waiting`：记录哪些乘客还在队列中（为==懒删除==准备）',
        'self.riders.append': '新乘客 `{riderId}` 加到 `riders` 末尾',
        'self.waiting.add': '`waiting` 里登记乘客 `{riderId}`',
        'self.drivers.append': '新司机 `{driverId}` 加到 `drivers` 末尾',
        'if not self.drivers': lambda S, B, r: ('没有空闲司机 → 直接无法匹配' if not S['self.drivers'] else '有空闲司机，继续看乘客'),
        'while self.riders and': _clean,
        20: '把取消的乘客从 `riders` 队首弹掉',
        'if not self.riders': lambda S, B, r: ('清理完乘客队列为空 → 无法匹配' if not S['self.riders'] else '两个队列都非空 → 可以匹配'),
        'res = [': '两个队首配对：`res = [司机 {res[0]}, 乘客 {res[1]}]`',
        'self.drivers.popleft()': '司机 `{res[0]}` 出队',
        27: '乘客 `{res[1]}` 出队',
        'self.waiting.remove(res[1])': '乘客已匹配，从 `waiting` 删掉',
        'return res': '匹配成功，返回 `{ret}`',
        'return [-1, -1]': '返回 `[-1, -1]`',
        'if riderId in self.waiting': _cancel,
        'self.waiting.remove(riderId)': '只从 `waiting` 删掉 `{riderId}`；队列里的他等到队首再清理',
    },
    cards=dict(
        one_liner='队列管顺序，集合标记谁取消了，到队首再清理',
        complexity='match 均摊 `O(1)`，其余 `O(1)`',
        problem=['管理乘客叫车请求和空闲司机，按到达顺序匹配',
                 '`match` 返回最早空闲司机和最早等待乘客 `[司机, 乘客]`，没有则 `[-1, -1]`',
                 '`cancelRider` 取消还没被匹配的乘客'],
        quote='由于还存在取消操作，而实时从队列中进行删除的时间复杂度较高，因此在这里可以采用懒删除的策略，使用一个集合waiting记录哪些乘客还存在于队列中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先到先匹配 → `drivers`、`riders` 两个队列',
              '取消时不在队列中间删，只把 `riderId` 从 `waiting` 弹出',
              '匹配时先弹掉队首已取消的乘客，再判断能否配对'],
        summary=['每个乘客最多入队、出队一次，match 均摊 `O(1)`',
                 '易错：司机为空时要先返回；弹完取消乘客后 `riders` 可能变空',
                 '匹配成功后要把乘客从 `waiting` 删掉，保证集合状态一致',
                 '对比灵神：灵神用 `discard` 且配对后不删集合；yiduobo 先判断再删，更严谨'],
    ),
)
