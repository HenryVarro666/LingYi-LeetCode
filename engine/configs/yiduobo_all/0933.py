TMAX = 6500


def _timeline(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '时间轴（青色带 = 窗口 [t − 3000, t]，绿点 = 窗口内的请求）', 24, T['muted'], bold=True)
    q = S.get('self.q')
    if q is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    ax0, ax1 = x0 + 50, x1 - 50
    Y = y0 + 120

    def X(v):
        return ax0 + (ax1 - ax0) * v / TMAX

    cv.line([(ax0, Y), (ax1, Y)], T['border'], 3)
    for v in range(0, TMAX + 1, 1000):
        cv.line([(X(v), Y - 6), (X(v), Y + 6)], T['border'], 2)
        cv.text((X(v), Y + 12), v, 17, T['dim'], anchor='mt', mono=True)
    t = S.get('t')
    if t is not None:
        a = max(0, t - 3000)
        cv.rect((X(a), Y - 34, X(t), Y + 2), fill=T['cyan'], alpha=55, r=6)
        cv.rect((X(a), Y - 34, X(t), Y + 2), outline=T['cyan'], width=2, r=6)
        cv.text((X(a), Y - 40), f't−3000={t - 3000}', 18, T['cyan'], anchor='mb', bold=True)
        cv.text((X(t), Y - 40), f't={t}', 18, T['cyan'], anchor='lb' if t < TMAX * 0.8 else 'rb', bold=True)
    l = S.get('self.l', 0)
    for i, v in enumerate(q):
        inside = i >= l
        c = T['green'] if inside else T['dim']
        cv.rect((X(v) - 8, Y - 24, X(v) + 8, Y - 8), fill=c, r=8)
        row = i % 2
        cv.text((X(v), Y + 40 + row * 22), v, 18, T['text'] if inside else T['dim'], anchor='mt', bold=inside)


def _while(S, B, ret):
    q, l, t = B['self.q'], B['self.l'], B.t
    if l < len(q) and q[l] < t - 3000:
        return f'`q[l] = {q[l]} < t − 3000 = {t - 3000}`：距今超过 3000ms → ==移出窗口=='
    if l < len(q) and q[l] == t - 3000:
        return f'`q[l] = {q[l]}` 恰好等于 `t − 3000`：==边界也在窗口内==，左边界停下'
    if l < len(q):
        return f'`q[l] = {q[l]} ≥ t − 3000 = {t - 3000}`：还在 3000ms 以内，左边界停下'
    return '`l` 已经到末尾，停止'


CONFIG = dict(
    num=933, title='最近的请求次数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='数组 + 滑动窗口左边界',
    tags=['labuladong', '灵神核心路线'],
    code='''
class RecentCounter(object):

    def __init__(self):
        self.q = []
        self.l = 0

    def ping(self, t):
        self.q.append(t)
        while self.l < len(self.q) and self.q[self.l] < t - 3000:
            self.l += 1

        return len(self.q) - self.l
''',
    call='''c = RecentCounter()
[c.ping(1), c.ping(100), c.ping(3001), c.ping(3002), c.ping(6002)]''',
    expect=[1, 2, 3, 3, 2],
    views=[
        dict(type='custom', draw=_timeline, h=230),
        dict(type='array', var='self.q', label='q（所有请求；框 = 窗口 [l, 末尾]）', cell=84, h=210,
             pointers={'self.l': 'pink'}, pointer_labels={'self.l': 'l'},
             window=('self.l', 'len(self.q) - 1'),
             dim=lambda S, i, v: i < S.get('self.l', 0)),
        dict(type='text', fn=lambda S: (f'`ping({S["t"]})` 要数时间在 `[{S["t"] - 3000}, {S["t"]}]` 内的请求'
                                        if 't' in S else '`q` 只追加不删除，用 `l` 标记窗口左边界'), size=27, h=60),
    ],
    watch=[('t', 't', 'cyan'), ('l', 'self.l', 'pink'), ('len(q)', 'len(self.q)'),
           ('窗口大小', 'len(self.q) - self.l', 'green')],
    captions={
        'self.q = []': '`q` 按时间顺序存下所有请求',
        'self.l = 0': '`l` 是窗口左边界（下标）；右边界永远是最新的请求',
        'self.q.append(t)': '`ping({t})`：新请求加入末尾，成为窗口右边界',
        'while self.l <': _while,
        'self.l += 1': '左边界右移：`l` → `{self.l}`',
        'return len(self.q)': '窗口大小 `{len(self.q)} − {self.l}` = =={ret}== 个请求',
    },
    cards=dict(
        one_liner='请求按时间递增到来：右边界是当前请求，左边界只往右移',
        complexity='均摊每次 `ping` 为 `O(1)`，空间 `O(n)`',
        problem=['`RecentCounter()`：初始没有请求',
                 '`ping(t)`：在时刻 `t`（毫秒）新增一个请求，返回 `[t − 3000, t]` 内的请求数',
                 '保证每次 `t` 都==严格大于==上一次',
                 '示例：`ping(1), ping(100), ping(3001), ping(3002)` → `1, 2, 3, 3`'],
        quote='每新来一个时间节点，则通过==移动窗口左边界==将窗口内距离当前时间点超过3000ms的节点移出窗口，然后当前窗口的大小即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['请求按时间排好 → 用数组存下所有时间点',
              '窗口右边界 = 当前时间点，左边界 `l` 根据 3000ms 更新',
              '答案就是窗口大小 `len(q) − l`'],
        summary=['`l` 只增不减，所有 `ping` 总共移动 `O(n)` 次 → 均摊 `O(1)`',
                 '边界：`t − 3000` 这一刻的请求==要算上==，所以条件是 `<` 而不是 `<=`',
                 '这里 `q` 只追加不删除；也可以用 `deque` 的 `popleft` 真正删掉旧请求',
                 '原文代码可直接在 Python 3 运行，未做修改'],
    ),
)
