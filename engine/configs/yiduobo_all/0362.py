CONFIG = dict(
    num=362, title='敲击计数器', difficulty='Medium', category='设计',
    author='yiduobo', technique='队列淘汰过期敲击',
    tags=['队列'],
    code='''
class HitCounter(object):

    def __init__(self):
        self.q = deque()
        self.s = 0

    def hit(self, timestamp):
        while self.s > 0:
            first = self.q.popleft()
            if timestamp - first < 300:
                self.q.appendleft(first)
                break
            else:
                self.s -= 1
        
        self.q.append(timestamp)
        self.s += 1

    def getHits(self, timestamp):
        while self.s > 0:
            first = self.q.popleft()
            if timestamp - first < 300:
                self.q.appendleft(first)
                break
            else:
                self.s -= 1

        return self.s
''',
    call='''h = HitCounter()
res = []
h.hit(1)
h.hit(2)
h.hit(3)
res.append(h.getHits(4))
h.hit(300)
res.append(h.getHits(301))
res''',
    expect=[3, 3],
    views=[
        dict(type='queue', var='self.q', label='队列 q（队首 → 队尾：敲击时间戳）', fmt=lambda x: str(x), h=200),
        dict(type='text', fn=lambda S: (f"过期线：时间差 ≥ 300 的敲击不再计数　队列里 `{S['self.s']}` 个" if 'self.s' in S else ''), size=28, h=60),
    ],
    watch=['timestamp', 'first', ('s', 'self.s', 'green')],
    captions={
        'self.q = deque()': '队列按时间顺序存所有还有效的敲击',
        'self.s = 0': '`s` 是队列里的敲击数，也就是答案',
        'while self.s > 0': lambda S, B, r: (f'队列里还有 `{S["self.s"]}` 个敲击 → 看看队首过期没有' if S['self.s'] > 0 else '队列空了 → 没有可淘汰的了'),
        'first = self.q.popleft()': '取出最老的敲击 `{first}`',
        'if timestamp - first < 300': lambda S, B, r: (f'`{S.timestamp} − {S.first} = {S.timestamp - S.first}` < 300 → ==还在 5 分钟内==' if S.timestamp - S.first < 300 else f'`{S.timestamp} − {S.first} = {S.timestamp - S.first}` ≥ 300 → ==已过期=='),
        'self.q.appendleft(first)': '最老的都没过期，后面更新的更不会 → 放回队首，停止淘汰',
        'break': '队首有效，后面的都有效，跳出循环',
        'self.s -= 1': '过期的敲击已被弹出不再放回，`s` 减一 → {self.s}',
        'self.q.append(timestamp)': '这次敲击的时间戳 `{timestamp}` 入队尾',
        'self.s += 1': '计数加一：`s` = =={self.s}==',
        'return self.s': '过期的都清掉了，5 分钟内共 =={ret}== 次敲击',
    },
    cards=dict(
        one_liner='队列里只留最近 5 分钟的敲击，过期的从队首弹掉',
        complexity='每个敲击入队、出队各一次，均摊 `O(1)`',
        problem=['`hit(t)` 记录时间 t 的一次敲击，`getHits(t)` 返回 t 之前 5 分钟（300 秒）内的敲击数',
                 '时间戳按非递减顺序给出',
                 '本视频：敲 1、2、3 → 查 4 → 敲 300 → 查 301'],
        quote='对于每次hit或getHits操作，首先都需要根据当前时间戳，将队列中所有五分钟之前的敲击从队列中弹出。',
        quote_src='—— yiduobo 题解原文',
        idea=['时间戳递增，所以最老的敲击一定在队首，过期的只会出现在队首',
              '每次操作先从队首清掉过期的，剩下的就是有效敲击',
              '`hit` 清完再把当前时间入队；`getHits` 清完直接返回个数 `s`'],
        summary=['判过期的条件：`timestamp - first >= 300`',
                 '先 `popleft` 看一眼，没过期要用 `appendleft` 放回去',
                 '进阶（敲击量很大）：原文提到再用哈希表按时刻合并计数，省空间',
                 '原文为 Python 2 风格写法，本题代码在 Python 3 下无需修改'],
    ),
)
