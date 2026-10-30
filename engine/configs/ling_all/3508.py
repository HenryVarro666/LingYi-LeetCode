def _tmap(k, v):
    return f'{k} → {list(v)}'


def _pk(x):
    return f'({x[0]},{x[1]},{x[2]})'


def _cnt_txt(S):
    if 'timestamps' not in S or 'left' not in S:
        return ''
    ts = list(S['timestamps'])
    if 'right' not in S:
        return f'`dest = {S["destination"]}` 的时间戳队列 `{ts}`，找 `>= {S["startTime"]}` 的第一个位置：`left = {S["left"]}`'
    return (f'`bisect_left(>= {S["startTime"]}) = {S["left"]}`，`bisect_right(> {S["endTime"]}) = {S["right"]}`'
            f' → 个数 = `{S["right"]} - {S["left"]}` = =={S["right"] - S["left"]}==')


CONFIG = dict(
    num=3508, title='设计路由器', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='队列 + 哈希表套队列 + 二分',
    tags=['灵神题单·二分算法', '灵神题单·常用数据结构', '难度分 1851'],
    code='''
class Router:
    def __init__(self, memoryLimit: int):
        self.memory_limit = memoryLimit
        self.packet_q = deque()  # packet 队列
        self.packet_set = set()  # packet 集合
        self.dest_to_timestamps = defaultdict(deque)  # destination -> [timestamp]

    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        packet = (source, destination, timestamp)
        if packet in self.packet_set:
            return False
        self.packet_set.add(packet)
        if len(self.packet_q) == self.memory_limit:  # 太多了
            self.forwardPacket()
        self.packet_q.append(packet)  # 入队
        self.dest_to_timestamps[destination].append(timestamp)
        return True

    def forwardPacket(self) -> List[int]:
        if not self.packet_q:
            return []
        packet = self.packet_q.popleft()  # 出队
        self.packet_set.remove(packet)
        self.dest_to_timestamps[packet[1]].popleft()
        return packet  # list(packet)

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        timestamps = self.dest_to_timestamps[destination]
        left = bisect_left(timestamps, startTime)  # deque 访问不是 O(1) 的，可以看另一份代码【Python3 list】
        right = bisect_right(timestamps, endTime)
        return right - left
''',
    call='''r = Router(2)
out = [r.addPacket(1, 4, 90), r.addPacket(2, 5, 90), r.addPacket(1, 4, 90)]
out.append(r.addPacket(3, 5, 95))
out.append(list(r.forwardPacket()))
out.append(r.addPacket(4, 5, 105))
out.append(r.getCount(5, 95, 105))
out''',
    expect=[True, True, False, True, [2, 5, 90], True, 2],
    views=[
        dict(type='queue', var='self.packet_q', label='packet_q（队首在左：最旧）', fmt=_pk, h=140),
        dict(type='set', var='self.packet_set', label='packet_set（判重）', fmt=_pk, h=120),
        dict(type='map', var='self.dest_to_timestamps', label='dest_to_timestamps：destination → 时间戳队列', fmt=_tmap, h=170, font=30),
        dict(type='text', h=100, size=28, fn=_cnt_txt),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('memory_limit', 'self.memory_limit', 'blue'), ('队列长度', 'len(self.packet_q)', 'green'), 'destination', 'timestamp'],
    captions={
        'self.memory_limit = memoryLimit': '最多存 `{memoryLimit}` 个数据包',
        'self.packet_q = deque()': '先进先出 → 用==队列==存数据包',
        'self.packet_set = set()': '用集合判重：同样的 `(source, destination, timestamp)` 视为重复',
        'self.dest_to_timestamps = defaultdict': '`getCount` 按 destination 查 → 哈希表套队列，只存时间戳',
        'packet = (source, destination, timestamp)': '三元组 `{packet}` 可哈希，直接放进集合',
        'if packet in self.packet_set': lambda S, B, ret: ('`{}` 已经在路由器里 → 重复'.format(S.packet) if S.packet in B['self.packet_set']
                                                           else '`{}` 不在集合里 → 不是重复'.format(S.packet)),
        'return False': '重复数据包，返回 `False`',
        'self.packet_set.add(packet)': '记进集合',
        'if len(self.packet_q) == self.memory_limit': lambda S, B, ret: (
            '队列已满（`{}` 个），要先挤掉最旧的'.format(len(S['self.packet_q'])) if len(S['self.packet_q']) == S['self.memory_limit']
            else '还没满（{} < {}），直接入队'.format(len(S['self.packet_q']), S['self.memory_limit'])),
        'self.forwardPacket()': '挤掉最旧的包：直接复用 `forwardPacket`',
        'self.packet_q.append(packet)': '新包入队尾：`{packet}`',
        'self.dest_to_timestamps[destination].append': '`destination = {destination}` 的时间戳队列追加 `{timestamp}`（题目保证时间戳非递减，所以队列有序）',
        'return True': '添加成功，返回 `True`',
        'if not self.packet_q': lambda S, B, ret: '队列为空 → 没有包可转发' if not S['self.packet_q'] else '队列非空，转发队首',
        'packet = self.packet_q.popleft()': '队首（最旧）出队：`{packet}`',
        'self.packet_set.remove(packet)': '同步从集合删掉',
        'self.dest_to_timestamps[packet[1]].popleft()': '同一个包一定是它 destination 队列里最旧的 → `popleft` 去掉 `{packet[2]}`',
        'return packet': '返回被转发的包 `{packet}`',
        'timestamps = self.dest_to_timestamps[destination]': '只看 `destination = {destination}` 的时间戳 `{list(timestamps)}`',
        'left = bisect_left': '第一个 `>= startTime = {startTime}` 的位置：`left = {left}`',
        'right = bisect_right': '第一个 `> endTime = {endTime}` 的位置：`right = {right}`',
        'return right - left': '区间 `[left, right)` 里的数就是在 `[{startTime}, {endTime}]` 内的：`{right} - {left}` = =={ret}==',
    },
    cards=dict(
        one_liner='队列管 FIFO，集合管判重，按 destination 分组的队列配合二分查个数',
        complexity='`getCount` 为 `O(log min(q, memoryLimit))`，其余 `O(1)`；空间 `O(min(q, memoryLimit))`',
        problem=['设计路由器：`addPacket` 去重并限容、`forwardPacket` 按先进先出转发、`getCount` 统计某目标在时间区间内的包数',
                 '超过 `memoryLimit` 时先丢掉最旧的包；`addPacket` 的时间戳非递减',
                 '示例 1：限制 3，加 4 个包后转发 `[2,5,90]`，`getCount(5,100,110)` → `1`'],
        quote='题目要求 FIFO（先进先出），这可以用队列实现。为了判重，可以用哈希表记录数据包。对于 getCount，需要按照 destination 分组，所以要用哈希表套队列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三个结构：`packet_q` 队列、`packet_set` 判重、`dest_to_timestamps` 按目标分组',
              '`addPacket`：满了先 `forwardPacket` 挤掉最旧的，再入队；`forwardPacket` 要同步更新三个结构',
              '时间戳非递减 → 每个 destination 的队列有序，`getCount` 用 `bisect_left/right` 相减'],
        summary=['`getCount` = `bisect_right(endTime) - bisect_left(startTime)`',
                 '`deque` 下标访问不是 `O(1)`，原文另给了「列表 + head 下标」写法，二分更稳',
                 '易错：转发时三处都要删；`packet_set` 先 `add` 再判满，也就是先挤掉旧包',
                 '`forwardPacket` 原文返回元组，LeetCode 允许；本视频把结果转成 `list` 再收集'],
    ),
)
