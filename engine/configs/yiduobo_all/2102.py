def _fm(x):
    return f'{x.name}:{x.score}'


def _rank(S):
    top, rest = S.get('self.top_heap'), S.get('self.rest_heap')
    if top is None or rest is None:
        return ''
    allv = sorted(list(top) + list(rest), key=lambda o: (-o.score, o.name))
    k = S.get('self.k', 1)
    return '从好到坏：' + '　'.join(
        (f'[{o.name}]' if o in top else o.name) for o in allv) + f'　（[ ] = 在 top 里）'


CONFIG = dict(
    num=2102, title='序列顺序查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='top 小根堆 + rest 大根堆',
    tags=['堆（优先队列）', '难度分 2159'],
    code='''
class Top(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        if self.score < other.score or (self.score == other.score and self.name > other.name):
            return True
        return False

class Rest(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        if self.score > other.score or (self.score == other.score and self.name < other.name):
            return True
        return False

class SORTracker(object):

    def __init__(self):
        self.top_heap = []
        self.rest_heap = []
        self.k = 1

    def add(self, name, score):

        if len(self.top_heap) < self.k:
            heapq.heappush(self.top_heap, Top(name, score))
        else:
            if score > self.top_heap[0].score or (score == self.top_heap[0].score and name < self.top_heap[0].name):
                heapq.heappush(self.top_heap, Top(name, score))
                min_top = heapq.heappop(self.top_heap)
                name, score = min_top.name, min_top.score

            heapq.heappush(self.rest_heap, Rest(name, score))

    def get(self):
        res = heapq.heappop(self.top_heap)
        heapq.heappush(self.top_heap, res)
        self.k += 1
        if self.rest_heap:
            max_rest = heapq.heappop(self.rest_heap)
            heapq.heappush(self.top_heap, Top(max_rest.name, max_rest.score))

        return res.name
''',
    call='''t = SORTracker()
r = []
t.add("bradford", 2)
t.add("branford", 3)
r.append(t.get())
t.add("alps", 2)
r.append(t.get())
t.add("orland", 2)
r.append(t.get())
t.add("orlando", 3)
r.append(t.get())
r''',
    expect=['branford', 'alps', 'bradford', 'bradford'],
    views=[
        dict(type='text', fn=_rank, size=20, h=90),
        dict(type='heap', var='self.top_heap', label='top：最好的 k 个（小根堆）', fmt=_fm, top_color='yellow', h=130),
        dict(type='heap', var='self.rest_heap', label='rest：其余（大根堆）', fmt=_fm, top_color='pink', h=130),
        dict(type='calls', label='正在执行', h=90),
    ],
    watch=[('name', 'name', 'orange'), ('score', 'score', 'cyan'), ('k', lambda S: S.get('self.k'), 'blue'), ('r', 'r', 'green')],
    skip=['self.name = name', 'self.score = score', 'self.top_heap = []', 'self.rest_heap = []', 'self.k = 1', 'return False', 'return True', 'if self.score < other.score', 'if self.score > other.score'],
    captions={
        'if len(self.top_heap) < self.k': lambda S, B, r_: (
            f'`top` 里只有 {len(S["self.top_heap"])} 个 < k = {S["self.k"]}：还没装满，`{S.name}` 直接进 top' if len(S['self.top_heap']) < S['self.k']
            else f'`top` 已装满 {S["self.k"]} 个：要拿 `{S.name}` 和 top 堆顶（第 k 好）比一比'),
        'if score > self.top_heap[0].score': lambda S, B, r_: (
            f'`{S.name}` 比 top 堆顶 `{S["self.top_heap"][0].name}` ==更好==：它该进 top，堆顶被挤出去' if r_ is None and (S.score > S['self.top_heap'][0].score or (S.score == S['self.top_heap'][0].score and S.name < S['self.top_heap'][0].name))
            else f'`{S.name}` 不比 top 堆顶 `{S["self.top_heap"][0].name}` 好：直接放进 rest'),
        'heapq.heappush(self.top_heap, Top(name, score))': '新景点先进 top 堆',
        'min_top = heapq.heappop(self.top_heap)': '弹出 top 里最差的（堆顶）：它不再属于最好的 k 个',
        'name, score = min_top.name, min_top.score': '把被挤出的 `{name}` 当作要放进 rest 的景点',
        'heapq.heappush(self.rest_heap, Rest(name, score))': '`{name}` 放进 rest 堆',
        'res = heapq.heappop(self.top_heap)': '弹出 top 堆顶：它就是这一次要查的第 `{self.k}` 好',
        'heapq.heappush(self.top_heap, res)': '看过 `{res.name}` 后放回去，top 堆不变',
        'self.k += 1': '下一次查第 `{self.k}` 好，所以 `k` 加 1',
        'if self.rest_heap': lambda S, B, r_: ('rest 不空：它的最好的一个要补进 top，让 top 重新有 k 个' if S['self.rest_heap'] else 'rest 是空的，无需补'),
        'max_rest = heapq.heappop(self.rest_heap)': '弹出 rest 堆顶 = 剩下里最好的 `{max_rest.name}`',
        'heapq.heappush(self.top_heap, Top(max_rest.name, max_rest.score))': '补进 top：top 又有 {len(self.top_heap)} 个 = 新的 k',
        'return res.name': '返回 ==`{ret}`==',
    },
    cards=dict(
        one_liner='k 每次加 1：top 堆放最好的 k 个，其余放 rest 堆',
        complexity='`add` / `get` 都是 `O(log n)`；空间 `O(n)`',
        problem=['`add(name, score)` 加景点：分高者好，同分字典序小者好',
                 '`get()`：第 k 次调用返回当前第 k 好的景点',
                 '示例：`bradford 2`、`branford 3`，`get` → `branford`'],
        quote='这里k是从1开始逐1递增的，因此带来了操作的空间。……维护大小为k的小根堆top，其中储存了当前数组中最大的k个值，那么这个堆的堆顶就是当前所有值中第k大的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`top` 小根堆装最好的 k 个：堆顶就是第 k 好，查询直接看它',
              '`rest` 大根堆装其余：堆顶是剩下里最好的，k 变大时补给 top',
              '字符串不能取相反数：所以给 Top、Rest 各重载 `__lt__` 来定顺序'],
        summary=['`add` / `get` 都是几次堆操作，`O(log n)`；空间 `O(n)`',
                 '易错：同分时字典序小的更好，Top 与 Rest 的 `__lt__` 方向正好相反',
                 '易错：`get` 先弹出再压回，别忘了把 `k` 加 1 并从 rest 补一个',
                 '对比灵神：灵神用一个有序列表按下标取；yiduobo 用对顶堆，不需要平衡树',
                 '原文是 Python 2 写法，但这份代码在 Python 3 里可直接运行，无需修改'],
    ),
)
