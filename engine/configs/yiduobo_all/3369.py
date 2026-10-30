CONFIG = dict(
    num=3369, title='设计数组统计跟踪器', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='队列 + 对顶堆懒删除 + 频次堆',
    tags=[],
    code='''
class StatisticsTracker(object):

    def __init__(self):
        self.q = deque()

        self.s = 0

        self.big_heap = []
        self.big_size = 0
        self.big_removed = {}
        self.small_heap = []
        self.small_size = 0
        self.small_removed = {}

        self.freq = {}
        self.freq_heap = []

    def remove(self):
        while self.small_heap and self.small_removed.get(-self.small_heap[0], 0) > 0:
            self.small_removed[-self.small_heap[0]] -= 1
            heapq.heappop(self.small_heap)
        
        while self.big_heap and self.big_removed.get(self.big_heap[0], 0) > 0:
            self.big_removed[self.big_heap[0]] -= 1
            heapq.heappop(self.big_heap)

    def maintainHeap(self):
        if self.small_size <= self.big_size <= self.small_size + 1:
            return

        if self.small_size > self.big_size:
            from_heap = self.small_heap
            to_heap = self.big_heap
            self.small_size -= 1
            self.big_size += 1
        else:
            from_heap = self.big_heap
            to_heap = self.small_heap
            self.small_size += 1
            self.big_size -= 1

        heapq.heappush(to_heap, -heapq.heappop(from_heap))

    def addNumber(self, number):
        self.q.append(number)
        self.s += number

        self.remove()
        if self.big_size == 0 or number >= self.big_heap[0]:
            heapq.heappush(self.big_heap, number)
            self.big_size += 1
        else:
            heapq.heappush(self.small_heap, -number)
            self.small_size += 1
        self.maintainHeap()
        
        self.freq[number] = self.freq.get(number, 0) + 1
        heapq.heappush(self.freq_heap, (-self.freq[number], number))

    def removeFirstAddedNumber(self):
        number = self.q.popleft()
        self.s -= number

        self.remove()
        if self.big_heap[0] <= number:
            self.big_size -= 1
            self.big_removed[number] = self.big_removed.get(number, 0) + 1
        else:
            self.small_size -= 1
            self.small_removed[number] = self.small_removed.get(number, 0) + 1
        
        self.maintainHeap()
        
        self.freq[number] -= 1
        heapq.heappush(self.freq_heap, (-self.freq[number], number))

    def getMean(self):
        return self.s // len(self.q)

    def getMedian(self):
        
        self.remove()
        return self.big_heap[0]

    def getMode(self):
        
        while self.freq[self.freq_heap[0][1]] != -self.freq_heap[0][0]:
            heapq.heappop(self.freq_heap)
        return self.freq_heap[0][1]
''',
    call='''t = StatisticsTracker()
res = []
t.addNumber(4); t.addNumber(2); t.addNumber(4)
res.append(t.getMedian()); res.append(t.getMode())
t.removeFirstAddedNumber()
res.append(t.getMedian()); res.append(t.getMode())
res''',
    expect=[4, 4, 4, 2],
    skip=['self.big_size = 0', 'self.small_size = 0', 'self.small_removed = {}', 'self.freq_heap = []', 'self.big_heap = []', 'self.s -= number', 'self.s += number', 'self.big_size += 1', 'self.small_size += 1', 'self.big_size -= 1', 'self.small_size -= 1', 19, 29],
    views=[
        dict(type='queue', var='self.q', label='self.q 加入顺序（左边最早）', h=100),
        dict(type='heap', var='self.small_heap', label='small_heap 大顶堆（存相反数）', fmt=lambda x: str(-x), top_color='blue', h=120),
        dict(type='heap', var='self.big_heap', label='big_heap 小顶堆', top_color='pink', h=120),
        dict(type='map', var='self.freq', label='freq 出现次数', h=100),
        dict(type='heap', var='self.freq_heap', label='freq_heap（-次数, 值）', fmt=lambda x: f'({x[0]},{x[1]})', top_color='orange', h=120),
    ],
    watch=[('s', 'self.s', 'green'), ('small_size', 'self.small_size', 'blue'), ('big_size', 'self.big_size', 'pink'),
           ('big_removed', 'self.big_removed', 'pink')],
    captions={
        'self.q = deque()': '队列 `q`：先进先出，用来找==最早加入==的数；`s` 记所有数的和',
        'self.s = 0': '`s` 记当前所有数的和，求平均数用',
        'self.small_heap = []': '`small_heap`：大顶堆（存相反数），存==较小的一半==；`big_heap` 是小顶堆，存较大的一半',
        'self.big_heap = []': '`big_heap`：小顶堆，存==较大的一半==，堆顶 = 中位数',
        'self.big_removed = {}': '`big_removed`：记下 big_heap 里待删的数，==懒删除==（堆不支持删中间元素）',
        'self.freq = {}': '`freq` 记每个数现在出现几次；`freq_heap` 按（次数大、值小）取众数',
        'self.q.append(number)': '`addNumber({number})`：先进队列，`q` = {list(self.q)}，`s` 累加成 {self.s + number}',
        'self.remove()': '先清理两个堆顶上已经被标记删除的数，保证堆顶有效',
        'self.big_size == 0 or number >= self.big_heap[0]': lambda S, B, r: (
            '`big_size == 0`：big 还是空的 → 放 big' if S['self.big_size'] == 0
            else f'`{S.number} >= big 堆顶 {S["self.big_heap"][0]}`？' + ('成立 → 放进较大的一半' if S.number >= S['self.big_heap'][0] else '不成立 → 放进较小的一半')),
        'heapq.heappush(self.big_heap, number)': '`{number}` 进 big_heap，`big_size` 加 1 → {self.big_size + 1}',
        'heapq.heappush(self.small_heap, -number)': '`{number}` 进 small_heap（存 `-{number}`），`small_size` 加 1 → {self.small_size + 1}',
        'if self.small_size <= self.big_size <= self.small_size + 1': lambda S, B, r: (
            f'平衡条件 `small_size <= big_size <= small_size + 1`（{S["self.small_size"]}, {S["self.big_size"]}）→ ' +
            ('成立，不用动' if S['self.small_size'] <= S['self.big_size'] <= S['self.small_size'] + 1 else '不成立，要挪一个数')),
        'if self.small_size > self.big_size': lambda S, B, r: (
            'small 多了 → 把 small 的堆顶挪到 big' if S['self.small_size'] > S['self.big_size']
            else 'big 多了 2 个 → 把 big 的堆顶挪到 small'),
        'heapq.heappush(to_heap, -heapq.heappop(from_heap))': '弹出一边堆顶，取相反数压进另一边（大小顶堆互换要变号）',
        'self.freq[number] = self.freq.get': '`freq[{number}]` = {self.freq[number]}',
        'heapq.heappush(self.freq_heap, (-self.freq[number], number))': '把新的（次数，值）压进 `freq_heap`；旧记录留着，取众数时再校验',
        'number = self.q.popleft()': '`removeFirstAddedNumber`：队首最早加入的是 =={number}==',
        'if self.big_heap[0] <= number': lambda S, B, r: (
            f'`big 堆顶 {S["self.big_heap"][0]} <= {S.number}`？' + ('成立 → 它在 big 里，只标记 `big_removed`' if S['self.big_heap'][0] <= S.number else '不成立 → 它在 small 里，标记 `small_removed`')),
        'self.big_removed[number] = ': '`big_size` 减 1 → {self.big_size}，`big_removed[{number}]` = {self.big_removed[number]}：堆里的数先不动',
        'self.small_removed[number] = ': '`small_size` 减 1 → {self.small_size}，`small_removed[{number}]` = {self.small_removed[number]}：堆里的数先不动',
        'self.maintainHeap()': '删完后大小可能失衡，重新平衡',
        'self.freq[number] -= 1': '`freq[{number}]` 减为 {self.freq[number]}',
        'return self.s // len(self.q)': '平均数 = `{self.s} // {len(self.q)}` = =={ret}==',
        'return self.big_heap[0]': '清掉无效堆顶后，big 的堆顶就是中位数 = =={ret}==',
        'while self.freq[self.freq_heap[0][1]] != -self.freq_heap[0][0]': lambda S, B, r: (
            f'堆顶记录次数 {-S["self.freq_heap"][0][0]}，`freq` 里现在是 {S["self.freq"][S["self.freq_heap"][0][1]]} → ' +
            ('不一致，说明是过期记录，弹掉' if S['self.freq'][S['self.freq_heap'][0][1]] != -S['self.freq_heap'][0][0] else '一致，有效')),
        'heapq.heappop(self.freq_heap)': '弹掉过期记录（懒删除）',
        'return self.freq_heap[0][1]': '堆顶 = 次数最多、值最小的数 = =={ret}==',
    },
    max_steps=200,
    cards=dict(
        one_liner='队列管顺序，对顶堆管中位数，频次堆管众数，删除一律懒处理',
        complexity='每次操作 `O(log n)`（均摊），空间 `O(n)`',
        problem=['设计 `StatisticsTracker`：`addNumber` 加数，`removeFirstAddedNumber` 删最早加入的数',
                 '`getMean` 向下取整平均数，`getMedian` 中位数，`getMode` 众数（并列取最小）',
                 '本视频：加入 `5,3,3` → 查中位数、众数；删最早的，再加 `7` 再查'],
        quote='python的heapq里面的堆是不支持删除指定元素操作的，所以在这里要么自己手搓一个，要么采用懒删除的方法',
        quote_src='—— yiduobo 题解原文',
        idea=['先看每个查询需要什么：删最早 → 队列；平均 → 维护和 `s`',
              '中位数：小顶堆存较大一半、大顶堆存较小一半，==big 比 small 多 0 或 1 个==，big 堆顶即中位数',
              '删除时只记到 `removed` 哈希表，堆顶碰到时再真正弹出；众数堆则比对 `freq` 判断是否过期'],
        summary=['原文代码已能在 Python 3 直接运行（平均数本来就是 `//`），未做修改',
                 '时间：每次操作 `O(log n)` 均摊，空间 `O(n)`',
                 '易错：删除时要先清堆顶再判断数在哪个堆；两堆大小要用 `size` 变量，不能用 `len`（含待删元素）',
                 '同类题：480. 滑动窗口中位数（本题中位数思路的来源）'],
    ),
)
