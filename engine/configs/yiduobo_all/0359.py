CALLS = [(1, 'foo'), (2, 'bar'), (3, 'foo'), (8, 'bar'), (10, 'foo'), (11, 'foo')]


def _q(S):
    if 'self.q' not in S:
        return None
    return [f'{t}:{m}' for t, m in S['self.q']]


CONFIG = dict(
    num=359, title='日志速率限制器', difficulty='Easy', category='设计',
    author='yiduobo', technique='队列 + 集合（滑动 10 秒窗口）',
    code='''
class Logger(object):

    def __init__(self):
        self.head = self.tail = 0
        self.q = []
        self.used = set()

    def shouldPrintMessage(self, timestamp, message):
        while self.head < self.tail and timestamp - self.q[self.head][0] >= 10:
            self.used.remove(self.q[self.head][1])
            self.head += 1

        if message in self.used:
            return False

        self.used.add(message)
        self.q.append([timestamp, message])
        self.tail += 1
        return True
''',
    call='''lg = Logger()
calls = [(1, 'foo'), (2, 'bar'), (3, 'foo'), (8, 'bar'), (10, 'foo'), (11, 'foo')]
[lg.shouldPrintMessage(t, m) for t, m in calls]''',
    expect=[True, True, False, False, False, True],
    views=[
        dict(type='array', var=_q, label='q（时间戳:日志；暗 = 已过期出队，蓝箭头 = 队首 head）', cell=110, h=250,
             pointers={'self.head': 'blue'}, dim=lambda S, i, v: i < S.get('self.head', 0)),
        dict(type='set', var='self.used', label='used（当前 10 秒内出现过的日志）', fmt=lambda x: f"'{x}'", h=130),
        dict(type='text', size=28, h=100,
             fn=lambda S: (f"当前请求：`timestamp = {S['timestamp']}`，`message = '{S['message']}'`；早于 =={S['timestamp'] - 9}== 的算过期" if 'timestamp' in S else '')),
    ],
    watch=[('timestamp', 'timestamp', 'blue'), ('message', 'message', 'cyan'), ('head', 'self.head', 'pink'), ('tail', 'self.tail', 'orange')],
    skip=['self.head = self.tail = 0', 'self.used = set()'],
    captions={
        'self.q = []': '`q` 按时间顺序存 `[时间戳, 日志]`：队首最旧，队尾最新',
        'while self.head < self.tail': lambda S, B, r: ('队首 `{}` 已存在 `{}` 秒 ≥ 10 → ==过期==，弹出'.format(S['self.q'][S['self.head']], S.timestamp - S['self.q'][S['self.head']][0])
                                                        if S['self.head'] < S['self.tail'] and S.timestamp - S['self.q'][S['self.head']][0] >= 10
                                                        else ('队列空了，没有可弹的' if S['self.head'] >= S['self.tail'] else '队首 `{}` 还没过期（{} 秒 < 10）→ 后面的更新，也都没过期'.format(S['self.q'][S['self.head']], S.timestamp - S['self.q'][S['self.head']][0]))),
        'self.used.remove': '过期日志 `{self.q[self.head][1]!r}` 同步从 `used` 删除',
        'self.head += 1': '队首后移：`head` → {self.head}（出队）',
        'if message in self.used': lambda S, B, r: ('`{!r}` 还在 `used` 里 → 10 秒内打印过'.format(S.message) if S.message in S['self.used'] else '`{!r}` 不在 `used` 里 → 可以打印'.format(S.message)),
        'return False': '10 秒内重复 → 返回 `False`（不记录）',
        'self.used.add(message)': '记下 `{message!r}`',
        'self.q.append': '`[{timestamp}, {message!r}]` 入队尾',
        'self.tail += 1': '`tail` → {self.tail}',
        'return True': '允许打印 → 返回 `True`',
    },
    cards=dict(
        one_liner='用队列按时间排日志，过期的先弹出，再靠集合判重',
        complexity='每次调用均摊 `O(1)`，空间 `O(10 秒内的日志数)`',
        problem=['设计 `Logger`：`shouldPrintMessage(timestamp, message)` 判断这条日志能否打印',
                 '同一条日志在 ==10 秒内==只打印一次，时间戳单调不减',
                 '示例：`(1,foo)(2,bar)(3,foo)(8,bar)(10,foo)(11,foo)`',
                 '→ `T T F F F T`'],
        quote='使用队列记录日志以及其对应的时间戳。当一条新的日志到达时，先通过当前日志的时间戳减去10，将队列中过期的日志和时间戳弹出。',
        quote_src='—— yiduobo 题解原文',
        idea=['新请求到来：先把队首过期（相差 ≥ 10）的日志出队',
              '同时从集合 `used` 删掉它们，集合只含队列里的日志',
              '剩下的日志都在 10 秒内：命中集合就拒绝，否则入队并放行'],
        summary=['均摊 `O(1)`：每条日志最多入队、出队一次',
                 '易错：出队时要同步维护 `used`，否则会永远拒绝',
                 '过期条件是 `timestamp - 旧时间戳 >= 10`：差正好 10 秒就算过期（示例中 `(10,foo)` 差 9 被拒，`(11,foo)` 差 10 通过）',
                 '与第 346 题（数据流移动平均）同样是队列处理数据流'],
    ),
)
