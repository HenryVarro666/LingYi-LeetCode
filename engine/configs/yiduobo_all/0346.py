CONFIG = dict(
    num=346, title='数据流中的移动平均值', difficulty='Easy', category='设计',
    author='yiduobo', technique='定长队列 + 维护总和',
    tags=['队列'],
    code='''
import queue

class MovingAverage(object):

    def __init__(self, size):
        self.q = queue.Queue(size)
        self.s = 0

    def next(self, val):
        if self.q.full():
            self.s -= self.q.get()
        self.q.put(val)
        self.s += val
        
        return self.s * 1.0 / self.q.qsize()
''',
    setup='''
import queue as _qm
_Orig = _qm.Queue
class _Snap:
    def __init__(self, items, size):
        self.queue = deque(items)
        self.maxsize = size
    def qsize(self):
        return len(self.queue)
    def full(self):
        return len(self.queue) >= self.maxsize
class _Q(_Orig):
    def __deepcopy__(self, memo):
        return _Snap(list(self.queue), self.maxsize)
_qm.Queue = _Q
''',
    call='''m = MovingAverage(3)
res = []
res.append(round(m.next(1), 2))
res.append(round(m.next(10), 2))
res.append(round(m.next(3), 2))
res.append(round(m.next(5), 2))
res''',
    expect=[1.0, 5.5, 4.67, 6.0],
    views=[
        dict(type='text', fn=lambda S: (f"窗口 `{list(S['self.q'].queue)}`　总和 `{S['self.s']}`　个数 `{S['self.q'].qsize()}`" if 'self.q' in S else '还没创建'), size=30, h=60),
        dict(type='queue', var='self.q.queue', label='队列 q（队首 → 队尾，容量 size = 3）', fmt=lambda x: str(x), h=200),
    ],
    watch=['val', ('s', 'self.s', 'green'), ('队列长度', 'len(self.q.queue)', 'blue')],
    captions={
        'self.q = queue.Queue': '建一个容量为 `size` 的队列，只存最近 `size` 个数',
        'self.s = 0': '`s` 记录队列里所有数的和，这样算平均值不用重新求和',
        'if self.q.full()': lambda S, B, r: (f'队列已满（{S["self.q"].qsize()} 个）→ 最老的数要先离开' if S['self.q'].full() else f'队列还没满（{S["self.q"].qsize()} 个）→ 直接加入'),
        'self.s -= self.q.get()': '弹出队首（最老的数），同时从总和里减掉：`s` = {self.s}',
        'self.q.put(val)': '新来的 `{val}` 加到队尾',
        'self.s += val': '新数也加进总和：`s` = =={self.s}==',
        'return self.s': '平均值 = `{self.s} / {self.q.qsize()}` = =={round(ret, 2)}==',
    },
    cards=dict(
        one_liner='用容量为 k 的队列装窗口，再记一个总和 s',
        complexity='每次 `next` 时间 `O(1)`，空间 `O(size)`',
        problem=['`MovingAverage(size)`：数据流里最近 `size` 个整数的平均值',
                 '`next(val)` 加入新数，返回当前滑动窗口平均值',
                 '本视频：`size=3`，依次输入 `1, 10, 3, 5`'],
        quote='使用一个容量为k的队列维护这个数据流，同时使用一个变量s记录当前队列中数值的总和。',
        quote_src='—— yiduobo 题解原文',
        idea=['队列满了先弹队首，同时 `s` 减掉它，窗口始终只有最近 k 个',
              '新数入队、`s` 加上它，平均值 = `s / 队列元素数`',
              '前几次队列没满，除数就是已经收到的个数'],
        summary=['时间 `O(1)`：不用每次重新求和，靠 `s` 增量维护',
                 '先弹旧数再加新数；顺序反了会在满队列上阻塞',
                 '乘 `1.0` 保证是小数除法',
                 '原文为 Python 2 写法，`import Queue` / `Queue.Queue` 已改为 `import queue` / `queue.Queue`；setup 里只加了让动画能拷贝队列状态的小补丁，算法不变'],
    ),
)
