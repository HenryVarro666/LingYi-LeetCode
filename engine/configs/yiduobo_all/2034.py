CONFIG = dict(
    num=2034, title='股票价格波动', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='字典 + 两个堆（懒删除）',
    tags=[],
    code='''
class StockPrice(object):

    def __init__(self):
        self.num_dict = {}
        self.max_heap = []
        self.min_heap = []
        self.max_timestamp = 0

    def update(self, timestamp, price):
        self.num_dict[timestamp] = price
        heapq.heappush(self.max_heap, [-price, timestamp])
        heapq.heappush(self.min_heap, [price, timestamp])
        self.max_timestamp = max(self.max_timestamp, timestamp)

    def current(self):
        return self.num_dict[self.max_timestamp]

    def maximum(self):
        p, t = heapq.heappop(self.max_heap)
        while -p != self.num_dict[t]:
            p, t = heapq.heappop(self.max_heap)
        
        heapq.heappush(self.max_heap, [p, t])
        return -p

    def minimum(self):
        p, t = heapq.heappop(self.min_heap)
        while p != self.num_dict[t]:
            p, t = heapq.heappop(self.min_heap)
        
        heapq.heappush(self.min_heap, [p, t])
        return p
''',
    call='''s = StockPrice()
out = []
s.update(1, 10)
s.update(2, 5)
out.append(s.current())
out.append(s.maximum())
s.update(1, 3)
out.append(s.maximum())
s.update(4, 2)
out.append(s.minimum())
out''',
    expect=[5, 10, 5, 2],
    views=[
        dict(type='map', var='self.num_dict', label='num_dict（时间戳 → 最新价格）', fmt=lambda k, v: f't{k} → {v}', h=110),
        dict(type='heap', var='self.max_heap', label='max_heap（-价格@时间戳）', fmt=lambda x: f'{-x[0]}@t{x[1]}', top_color='orange', h=170),
        dict(type='heap', var='self.min_heap', label='min_heap（价格@时间戳）', fmt=lambda x: f'{x[0]}@t{x[1]}', top_color='blue', h=170),
        dict(type='text', fn=lambda S: f"已知最晚时间戳 `max_timestamp` = =={S['self.max_timestamp']}==" if 'self.max_timestamp' in S else '', h=50),
    ],
    watch=[('timestamp', 'timestamp', 'blue'), ('price', 'price', 'pink'), 'p', 't', ('max_timestamp', 'self.max_timestamp', 'orange')],
    skip=['self.max_heap = []', 'self.min_heap = []'],
    captions={
        'self.num_dict = {}': '`num_dict` 记录每个时间戳的==最新==价格',
        'self.max_timestamp = 0': '`max_timestamp` 记录当前最晚的时间戳',
        'self.num_dict[timestamp] = price': '`update({timestamp}, {price})`：字典里写入（或覆盖）这个时间戳的价格',
        'heapq.heappush(self.max_heap, [-price': '只把新价格压进最大堆（存负数），==旧价格不删==，留到查询时再清理',
        'heapq.heappush(self.min_heap, [price': '同样压进最小堆，不去找旧价格的位置',
        'self.max_timestamp = max': '最晚时间戳取较大者 → `{self.max_timestamp}`',
        'return self.num_dict[self.max_timestamp]': '最新价格 = `num_dict[{self.max_timestamp}]` = =={ret}==',
        'p, t = heapq.heappop(self.max_heap)': '取出最大堆堆顶：价格 `{-p}`、时间戳 `{t}`',
        'while -p != self.num_dict[t]': lambda S, B, r: (
            f'堆顶价格 `{-S.p}` 与字典里 t{S.t} 的 `{S["self.num_dict"][S.t]}` ==不一致== → 过期，继续弹'
            if -S.p != S['self.num_dict'][S.t] else f'堆顶价格 `{-S.p}` 与字典里 t{S.t} 的价格一致 → 有效'),
        'heapq.heappush(self.max_heap, [p, t])': '这个有效的堆顶只是查看，放回去',
        'return -p': '当前最高价 = =={ret}==',
        'p, t = heapq.heappop(self.min_heap)': '取出最小堆堆顶：价格 `{p}`、时间戳 `{t}`',
        'while p != self.num_dict[t]': lambda S, B, r: (
            f'堆顶价格 `{S.p}` 与字典里 t{S.t} 的 `{S["self.num_dict"][S.t]}` ==不一致== → 过期，继续弹'
            if S.p != S['self.num_dict'][S.t] else f'堆顶价格 `{S.p}` 与字典里 t{S.t} 的价格一致 → 有效'),
        'heapq.heappush(self.min_heap, [p, t])': '有效的堆顶放回去',
        'return p': '当前最低价 = =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='堆里的旧价格不急着删，查询时发现过期再弹',
        complexity='update `O(log n)`，current `O(1)`，max/min 均摊 `O(log n)`',
        problem=['时间戳乱序到达，同一时间戳的价格可被后来的记录==更正==',
                 '实现 `update`、`current`（最晚时间戳的价格）、`maximum`、`minimum`',
                 '本视频：update(1,10)、update(2,5)，再更正 t1 为 3，最后加入 t4=2'],
        quote='更简便的做法是只将最新的价格加入到堆中，但不删去老的价格。当需要查询时，若此时堆中保留的价格与操作1中dict记录的价格不一致，说明堆中的价格过期了，此时再执行删除操作也不迟',
        quote_src='—— yiduobo 题解原文',
        idea=['三个操作拆开处理：字典记价格、变量记最晚时间戳、两个堆管最高/最低',
              '更新时不去堆里改元素，只压入新价格',
              '查询时用字典核对堆顶：对不上就是旧价格，弹掉'],
        summary=['时间 `O(log n)`（均摊），空间 `O(n)`：每次 update 各压入一个元素',
                 '查看堆顶后要把有效元素 `heappush` 放回去，否则下一次查询会丢数据',
                 '最大堆用 `-price` 模拟；元素含时间戳，才能去字典里核对',
                 '原文为 Python 2 风格写法，在 Python 3 中可直接运行，未改动代码',
                 '题面库里缺失，题意据 yiduobo 文章与 LeetCode 原题补写'],
    ),
)
