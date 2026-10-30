def _in_total(S):
    return 'startTime' in S and 'endTime' in S


def _formula(S):
    if _in_total(S) and 'left' in S and 'right' in S:
        left, right, ps, ts = S['left'], S['right'], S['self.pre_sum'], S['self.times']
        if S.get('_line', 0) < 13:
            if right <= left:
                return f'区间 `[{S["startTime"]}, {S["endTime"]}]` 里没有考试：`left = right = {left}`'
            return f'区间 `[{S["startTime"]}, {S["endTime"]}]` 里的考试 = `times[{left}..{right - 1}]` = {ts[left:right]}'
        if right <= left:
            return f'没有考试：`pre_sum[{right}] − pre_sum[{left}]` = {ps[right]} − {ps[left]} = =={ps[right] - ps[left]}=='
        return (f'`times[{left}..{right - 1}]` = {ts[left:right]}　'
                f'`pre_sum[{right}] − pre_sum[{left}]` = {ps[right]} − {ps[left]} = =={ps[right] - ps[left]}==')
    if _in_total(S) and 'left' in S:
        return f'`left = {S["left"]}`：查询区间 `[{S["startTime"]}, {S["endTime"]}]` 的左端点在 `times` 里的位置'
    if _in_total(S):
        return f'查询时间区间 `[{S["startTime"]}, {S["endTime"]}]`（闭区间）：先用二分在 `times` 里找出落在区间内的考试'
    if 'time' in S and 'score' in S:
        return f'新考试：时间 `{S["time"]}`，分数 `{S["score"]}`'
    return '`times` 严格递增 → 可二分；`pre_sum` 是分数的前缀和 → 区间和 `O(1)`'


def _left_cap(S, B, r):
    return ('`bisect_left(times, {s})`：第一个 `≥ {s}` 的考试下标 = =={l}=='
            .format(s=S.startTime, l=S.left)
            + ('（没有这样的考试，停在末尾）' if S.left >= len(S['self.times']) else ''))


def _right_cap(S, B, r):
    return ('`bisect_right(times, {e})`：第一个 `> {e}` 的下标 = =={r}==；时间在范围内的考试就是下标 `[{l}, {r})`'
            .format(e=S.endTime, r=S.right, l=S.left))


def _ret_cap(S, B, r):
    ps = S['self.pre_sum']
    tail = '（区间里没有考试，`left == right`）' if S.left == S.right else ''
    return '`pre_sum[{}] − pre_sum[{}]` = {} − {} = =={}=={}'.format(S.right, S.left, ps[S.right], ps[S.left], r, tail)


CONFIG = dict(
    num=3709, title='设计考试分数记录器', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='有序时间数组二分 + 分数前缀和',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1648'],
    code='''
class ExamTracker:
    def __init__(self):
        self.times = []
        self.pre_sum = [0]  # 原理见题目 303. 区域和检索 - 数组不可变

    def record(self, time: int, score: int) -> None:
        self.times.append(time)
        self.pre_sum.append(self.pre_sum[-1] + score)

    def totalScore(self, startTime: int, endTime: int) -> int:
        left = bisect_left(self.times, startTime)
        right = bisect_right(self.times, endTime)
        return self.pre_sum[right] - self.pre_sum[left]
''',
    call='''t = ExamTracker()
out = []
t.record(1, 98)
out.append(t.totalScore(1, 1))
t.record(5, 99)
out.append(t.totalScore(1, 5))
out.append(t.totalScore(3, 4))
t.record(8, 60)
out.append(t.totalScore(2, 8))
out''',
    expect=[98, 197, 0, 159],
    views=[
        dict(type='array', var='self.times', label='times（考试时间，严格递增；青框 = 落在查询区间里的考试）', h=250, cell=92,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right - 1'), min_slots=4),
        dict(type='array', var='self.pre_sum', label='pre_sum（pre_sum[i] = 前 i 次考试的分数和）', h=250, cell=92,
             pointers={'left': 'blue', 'right': 'pink'}, min_slots=4,
             color=lambda S, i, v: 'green' if 'left' in S and 'right' in S and i in (S['left'], S['right']) and S.get('_line') == 13 else None),
        dict(type='text', fn=_formula, size=24, h=96),
        dict(type='calls', label='正在执行的方法', h=80),
    ],
    watch=[('startTime', 'startTime'), ('endTime', 'endTime'), ('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'self.times = []': '`times` 记录每次考试的时间：`time` 严格递增，所以它==天然有序==，可以二分',
        'self.pre_sum = [0]': '`pre_sum[i]` = 前 `i` 次考试的分数和；开头放个 `0`，区间和就是 `pre_sum[右] − pre_sum[左]`',
        'self.times.append(time)': '时间 `{time}` 追加到 `times` 末尾：新时间比旧的都大，数组仍然有序',
        'self.pre_sum.append': lambda S, B, r: '`pre_sum` 追加 `{} + {}` = =={}==：前 {} 次考试的分数和'.format(
            S['self.pre_sum'][-2], S.score, S['self.pre_sum'][-1], len(S['self.pre_sum']) - 1),
        'left = bisect_left': _left_cap,
        'right = bisect_right': _right_cap,
        'return self.pre_sum[right]': _ret_cap,
    },
    cards=dict(
        one_liner='时间严格递增 → 二分定位；分数前缀和 → 区间和 O(1)',
        complexity='`record` 均摊 `O(1)`，`totalScore` `O(log q)`，空间 `O(q)`',
        problem=['`record(time, score)`：记录一次考试；`time` 严格递增',
                 '`totalScore(startTime, endTime)`：时间在闭区间内的考试分数之和，没有就是 0',
                 '示例：`record(1,98)`、`record(5,99)`、`totalScore(1,5)` → `197`',
                 '本视频：再加一次 `record(8,60)`，`totalScore(2,8)` → `159`'],
        quote='time 参数是严格递增的，我们可以用一个 times 数组记录 time。这样 times 是严格递增数组，可以在上面二分查找。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`times` 有序 → 在上面二分，找出落在 `[startTime, endTime]` 里的考试下标范围',
              '`left`：第一个 `≥ startTime`；`right`：第一个 `> endTime`；考试 = 下标 `[left, right-1]`',
              '分数用前缀和 `pre_sum`：这些考试的总分 = `pre_sum[right] − pre_sum[left]`'],
        summary=['`record` 均摊 `O(1)`，`totalScore` `O(log q)`，`q` 是 `record` 次数',
                 '易错：`startTime` 用 `bisect_left`，`endTime` 用 `bisect_right`（右端点含）',
                 '`pre_sum` 开头的 `0` 不能少，否则 `left = 0` 时没法相减',
                 '区间里没有考试时 `left == right`，结果自然是 0'],
    ),
)
