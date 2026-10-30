def _cnt_txt(S):
    if 'timestamps' not in S or 'left' not in S:
        return ''
    ts = list(S['timestamps'])
    lo = S['self.des_left'].get(S['destination'], 0) if 'self.des_left' in S else 0
    if 'start_index' not in S:
        return f'`destination = {S["destination"]}`：时间戳 `{ts}`，有效部分从下标 `des_left = {lo}` 开始'
    return f'有效区间 `[{lo}, {len(ts) - 1}]` 内：`start_index = {S["start_index"]}`，`end_index = {S["left"]}`'


def _pk(x):
    return f'({x[0]},{x[1]},{x[2]})'


CONFIG = dict(
    num=3508, title='设计路由器', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='队列 + 数组模拟队列 + 两次手写二分',
    tags=['灵神题单·二分算法', '灵神题单·常用数据结构', '难度分 1851'],
    code='''
class Router(object):

    def __init__(self, memoryLimit):
        
        self.q = deque()
        self.memoryLimit = memoryLimit
        self.packet_set = set()
        self.des_hash = {}
        self.des_left = {}

    def addPacket(self, source, destination, timestamp):
        
        key = (source, destination, timestamp)
        if key not in self.packet_set:
            self.packet_set.add(key)
            self.q.append(key)
            if destination not in self.des_hash:
                self.des_hash[destination] = []
                self.des_left[destination] = 0
            self.des_hash[destination].append(timestamp)
            
            if self.memoryLimit < len(self.q):
                rm_key = self.q.popleft()
                self.packet_set.remove(rm_key)
                self.des_left[rm_key[1]] += 1

            return True

        return False

    def forwardPacket(self):
        
        res = []
        if self.q:
            key = self.q.popleft()
            res = list(key)
            self.packet_set.remove(key)
            self.des_left[key[1]] += 1
        
        return res

    def getCount(self, destination, startTime, endTime):
        
        if destination not in self.des_hash:
            return 0
        
        timestamps = self.des_hash[destination]
        left = self.des_left[destination]
        right = len(timestamps) - 1
        if left > right:
            return 0

        if timestamps[-1] < startTime:
            return 0

        if timestamps[left] > endTime:
            return 0
        
        while left < right:
            mid = (left + right) // 2
            if timestamps[mid] < startTime:
                left = mid + 1
            else:
                right = mid
        
        start_index = left

        left = self.des_left[destination]
        right = len(timestamps) - 1
        while left < right:
            mid = (left + right + 1) // 2
            if timestamps[mid] <= endTime:
                left = mid
            else:
                right = mid - 1
        
        end_index = left

        return end_index - start_index + 1
''',
    call='''r = Router(2)
out = [r.addPacket(1, 4, 90), r.addPacket(2, 5, 90), r.addPacket(1, 4, 90)]
out.append(r.addPacket(3, 5, 95))
out.append(r.forwardPacket())
out.append(r.addPacket(4, 5, 105))
out.append(r.getCount(5, 95, 105))
out''',
    expect=[True, True, False, True, [2, 5, 90], True, 2],
    skip=['res = []', 'return res', 'return False', 'self.des_left[destination] = 0', 'self.packet_set.remove', 'self.packet_set.add(key)', 'res = list(key)'],
    max_steps=90,
    views=[
        dict(type='queue', var='self.q', label='q（队首在左：最旧）', fmt=_pk, h=120),
        dict(type='map', var='self.des_hash', label='des_hash：destination → 时间戳数组（只增不删）', fmt=lambda k, v: f'{k} → {v}', h=120, font=30),
        dict(type='map', var='self.des_left', label='des_left：数组里第一个还没过期的下标', fmt=lambda k, v: f'{k} → {v}', h=120, font=30),
        dict(type='array', var='timestamps', label='timestamps（二分的对象）', cell=100, h=230,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, window=('left', 'right')),
        dict(type='text', h=90, size=28, fn=_cnt_txt),
    ],
    watch=[('memoryLimit', 'self.memoryLimit', 'blue'), ('队列长度', 'len(self.q)', 'green'), 'destination', 'left', 'right', 'mid'],
    captions={
        'self.q = deque()': '先进先出 → 用队列 `q` 存当前所有数据包',
        'self.memoryLimit = memoryLimit': '最多存 `{memoryLimit}` 个包',
        'self.packet_set = set()': '`packet_set`：判重用',
        'self.des_hash = {}': '`des_hash[d]`：目的地 `d` 的时间戳数组（用数组代替队列，方便二分）',
        'self.des_left = {}': '`des_left[d]`：数组里最小的还没被转发/丢弃的下标，二分的下界',
        'key = (source': '三元组 `{key}` 作为这个包的 key',
        'if key not in self.packet_set': lambda S, B, ret: ('`{}` 不在集合里 → 不是重复'.format(S.key) if S.key not in B['self.packet_set']
                                                            else '`{}` 已经存在 → 重复，添加失败'.format(S.key)),
        'self.packet_set.add(key)': '加入集合',
        'self.q.append(key)': '入队尾',
        17: lambda S, B, ret: ('第一次见目的地 `{}`：建数组，下界设 0'.format(S.destination) if S.destination not in B['self.des_hash']
                                                                  else '目的地 `{}` 已有数组'.format(S.destination)),
        'self.des_hash[destination] = []': '为目的地 `{destination}` 建时间戳数组',
        'self.des_hash[destination].append(timestamp)': '追加时间戳 `{timestamp}`（addPacket 按时间戳递增，数组天然有序）',
        'if self.memoryLimit < len(self.q)': lambda S, B, ret: (
            '队列 `{}` 个 > 上限 `{}`：超了，丢最旧的'.format(len(S['self.q']), S['self.memoryLimit']) if S['self.memoryLimit'] < len(S['self.q'])
            else '队列 `{}` 个 ≤ 上限 `{}`：没超'.format(len(S['self.q']), S['self.memoryLimit'])),
        'rm_key = self.q.popleft()': '队首出队：丢掉最旧的 `{rm_key}`',
        'self.packet_set.remove(rm_key)': '同步从集合删除',
        'self.des_left[rm_key[1]] += 1': '数组不真删，只把 `des_left[{rm_key[1]}]` 加一：{self.des_left[rm_key[1]]}',
        'return True': '添加成功',
        'if self.q:': lambda S, B, ret: '队列非空，转发队首' if S['self.q'] else '队列为空，返回空数组',
        'key = self.q.popleft()': '队首出队：`{key}`',
        'res = list(key)': '转成 `list` 作为返回值：`{res}`',
        'self.packet_set.remove(key)': '同步从集合删除',
        'self.des_left[key[1]] += 1': '它是 `des_hash[{key[1]}]` 里最旧的 → `des_left[{key[1]}]` 加一：{self.des_left[key[1]]}',
        44: '没有这个目的地的包 → 个数 0；有的话继续',
        'timestamps = self.des_hash[destination]': '目的地 `{destination}` 的时间戳数组 `{timestamps}`',
        'left = self.des_left[destination]': '二分下界取 `des_left` = `{left}`（之前的已过期）',
        'right = len(timestamps) - 1': '上界取最后一个下标 `{right}`',
        'if left > right': lambda S, B, ret: '有效区间为空 → 返回 0' if S.left > S.right else '有效区间 `[{}, {}]` 非空'.format(S.left, S.right),
        'if timestamps[-1] < startTime': lambda S, B, ret: ('最大时间戳 `{} < {}`：全在区间左边 → 0'.format(S.timestamps[-1], S.startTime) if S.timestamps[-1] < S.startTime
                                                           else '最大时间戳 `{} >= {}`：可能有解'.format(S.timestamps[-1], S.startTime)),
        'if timestamps[left] > endTime': lambda S, B, ret: ('最小有效时间戳 `{} > {}`：全在区间右边 → 0'.format(S.timestamps[S.left], S.endTime) if S.timestamps[S.left] > S.endTime
                                                           else '最小有效时间戳 `{} <= {}`：可能有解'.format(S.timestamps[S.left], S.endTime)),
        'while left < right': lambda S, B, ret: '`left < right`，继续二分' if S.left < S.right else '`left == right`：定位完成',
        'mid = (left + right) // 2': '第一次二分（找最小的 `>= startTime`）：`mid = {mid}`',
        'if timestamps[mid] < startTime': lambda S, B, ret: (
            '`{} < {}`：mid 太早 → 答案在右边 `left = mid + 1`'.format(S.timestamps[S.mid], S.startTime) if S.timestamps[S.mid] < S.startTime
            else '`{} >= {}`：mid 可能是答案 → `right = mid`'.format(S.timestamps[S.mid], S.startTime)),
        'left = mid + 1': '`left` → {left}',
        64: '`right` → {right}',
        'start_index = left': '最小的 `>= startTime` 的下标：`start_index = {start_index}`',
        'mid = (left + right + 1) // 2': '第二次二分（找最大的 `<= endTime`）：上取整 `mid = {mid}`',
        'if timestamps[mid] <= endTime': lambda S, B, ret: (
            '`{} <= {}`：mid 可能是答案 → `left = mid`'.format(S.timestamps[S.mid], S.endTime) if S.timestamps[S.mid] <= S.endTime
            else '`{} > {}`：太晚了 → `right = mid - 1`'.format(S.timestamps[S.mid], S.endTime)),
        'left = mid': '`left` → {left}',
        'right = mid - 1': '`right` → {right}',
        'end_index = left': '最大的 `<= endTime` 的下标：`end_index = {end_index}`',
        'return end_index - start_index + 1': '闭区间 `[{start_index}, {end_index}]` 的个数：`{end_index} - {start_index} + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='用数组代替队列存每个目的地的时间戳，des_left 记下界，两次二分数个数',
        complexity='`getCount` 为 `O(log n)`，其余 `O(1)`；空间 `O(q)`',
        problem=['设计路由器：`addPacket` 去重并限容、`forwardPacket` 先进先出、`getCount` 统计目的地在时间区间内的包',
                 '超过 `memoryLimit` 就移除最旧的包；`addPacket` 的时间戳按序到来',
                 '示例 2：限制 2，加 `[7,4,90]` 后转发得到它，再转发得到 `[]`'],
        quote='在具体实现上，由于不确定python中的deque的下标访问是O(n)的还是O(1)的，所以在这里还是采用了数组模拟队列的处理方法，因此在这里还需要额外维护一个哈希表des_left。',
        quote_src='—— yiduobo 题解原文',
        idea=['`q` 管先进先出，`packet_set` 管去重，`des_hash[d]` 记目的地 `d` 的所有时间戳',
              '数组不删元素：被转发或丢弃时只让 `des_left[d]` 加一，当作队首下标',
              '`getCount`：先两次判边界，再二分出最小的 `>= startTime` 和最大的 `<= endTime`，下标相减加一'],
        summary=['与灵神对比：灵神用 `bisect_left/right`；yiduobo 手写两次二分，一次找左端点，一次找右端点',
                 '易错：二分前要先判 `left > right`、`timestamps[-1] < startTime`、`timestamps[left] > endTime`，否则区间为空时会数错',
                 '第二次二分用 `mid = (l + r + 1) // 2` 配合 `left = mid`，避免死循环',
                 '原文本身是 Python 3 可运行的写法，未做修改（`//` 原文已是整除）'],
    ),
)
