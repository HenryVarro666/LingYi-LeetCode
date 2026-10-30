def _get(ss, t):
    """get(t) 的结果：时间 <= t 的最后一个位置的前缀和（只用来写字幕）"""
    best = 0
    for tm, pre in ss:
        if tm <= t:
            best = pre
    return best


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ss = S.get('self.s')
    if ss is None:
        return
    n = len(ss)
    slots = max(n, 3)
    line = S.get('_line', 0)
    in_get = 't' in S
    win = in_get and 'left' in S and 'right' in S
    cv.text((x0 + 18, y0 + 4), 's[i] = (时间, 前缀和)：第 i 次考试的时间，和前 i 次的分数和（s[0] 是哨兵）', 22, T['muted'], bold=True)
    cell = min(150, (x1 - x0 - 60) / slots)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * slots) / 2
    top, ch = y0 + 120, 136
    if in_get:
        t = S['t']
        cv.text((x0 + 22, y0 + 50), f'get(t = {t})：找最后一个时间 ≤ {t} 的位置，取它的前缀和', 26, T['cyan'], bold=True)
    if win:
        lo, hi = S['left'], S['right']
        if hi >= lo:
            cv.rect((sx + lo * cell - 4, top - 14, sx + (hi + 1) * cell + 4, top + ch + 14), fill=T['cyan'], alpha=34, r=12)
            cv.rect((sx + lo * cell - 4, top - 14, sx + (hi + 1) * cell + 4, top + ch + 14), outline=T['cyan'], width=3, r=12)
    for i, (tm, pre) in enumerate(ss):
        X = sx + i * cell
        fill = T['panel2']
        outline, w = T['border'], 1
        txt_c = T['text']
        if in_get and 'mid' in S and i == S['mid'] and line in (14, 15, 17):
            ok = tm <= S['t']
            outline, w = (T['green'] if ok else T['red']), 5
        elif in_get and 'mid' in S and i == S['mid'] and line == 13:
            outline, w = T['yellow'], 5
        if in_get and line == 19 and i == S.get('left'):
            fill, txt_c = T['green'], T['bg']
        cv.rect((X + 5, top, X + cell - 5, top + ch), fill=fill, r=10, outline=outline, width=w)
        cv.text((X + cell / 2, top + 36), tm, 38, txt_c if fill == T['panel2'] else T['bg'], anchor='mm', bold=True)
        cv.line([(X + 16, top + ch / 2), (X + cell - 16, top + ch / 2)], T['border'], 2)
        cv.text((X + cell / 2, top + ch - 36), pre, 38, T['yellow'] if fill == T['panel2'] else T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top + ch + 20), i, 18, T['dim'], anchor='mt', mono=True)
    cv.text((sx - 8, top + 36), '时间', 18, T['muted'], anchor='rm')
    cv.text((sx - 8, top + ch - 36), '前缀和', 18, T['yellow'], anchor='rm')
    if in_get:
        rows = {}
        for name, c in (('left', 'blue'), ('mid', 'orange'), ('right', 'pink')):
            if name in S and 0 <= S[name] < n and (name != 'mid' or line in (13, 14, 15, 16, 17)):
                rows.setdefault(S[name], []).append((name, T[c]))
        for idx, lst in rows.items():
            X = sx + idx * cell + cell / 2
            for k, (name, c) in enumerate(lst):
                cv.tri_up(X, top + ch + 54 + k * 28, 9, c)
                cv.text((X, top + ch + 62 + k * 28), name, 20, c, anchor='mt', bold=True)
        if win and S['right'] < S['left']:
            cv.text((x0 + 22, top + ch + 160), 'right < left：区间收缩完毕', 22, T['dim'])


def _top(S):
    if 't' in S:
        if 'left' in S and 'right' in S and S['left'] < len(S['self.s']):
            return (f'不变量：`s[left]` 的时间一定 ≤ `t`（现在 `s[{S["left"]}]` 是 `{S["self.s"][S["left"]][0]}`）；'
                    f'`right` 右边的时间都 > `t`')
        return f'`t = {S["t"]}`：`s` 里时间 ≤ `t` 的最后一项，就是要找的位置'
    if 'startTime' in S and 'endTime' in S:
        a, b = S['startTime'], S['endTime']
        return f'`totalScore({a}, {b})` = `get({b})` − `get({a} − 1)`：前缀和相减，==先二分，再相减=='
    if 'time' in S and 'score' in S:
        return f'新考试：时间 `{S["time"]}`，分数 `{S["score"]}`；新前缀和 = 上一个前缀和 + 分数'
    return '`s` 按时间顺序存 `(时间, 前缀和)`，查询 `get(t)` = 时间 ≤ `t` 的所有考试总分'


def _cmp(S, B, r):
    v, t, mid = S.s[S.mid][0], S.t, S.mid
    if v > t:
        return f'`s[{mid}]` 的时间 `{v}` ==大于== `t = {t}`：它太晚了，答案在它左边'
    return f'`s[{mid}]` 的时间 `{v}` ≤ `t = {t}`：它==可能就是答案==，也可能更靠右'


def _first(S):
    """第一次 totalScore 里的第一次 get（只在这里讲全套解释）"""
    return S.get('startTime') == 1 and S.get('t') == S.get('endTime')


def _ret_get(S, B, r):
    base = '`s[{}]` 时间 `{}` 是最后一个 ≤ `{}` 的 → `get({})` = =={}=='.format(S.left, S['self.s'][S.left][0], S.t, S.t, r)
    if 'startTime' in S and S.t == S.startTime - 1:
        hi, lo = _get(S['self.s'], S.endTime), r
        return base + '；`totalScore` = {} − {} = =={}=='.format(hi, lo, hi - lo) + ('（区间里没有考试）' if hi == lo else '')
    return base


CONFIG = dict(
    num=3709, title='设计考试分数记录器', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='(时间, 前缀和) 数组 · 手写二分求前缀和之差',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1648'],
    code='''
class ExamTracker(object):

    def __init__(self):
        self.s = [(0, 0)]

    def record(self, time, score):
        self.s.append((time, self.s[-1][1] + score))

    def get(self, t):
        left = 0
        right = len(self.s) - 1
        while left < right:
            mid = (left + right + 1) // 2
            if self.s[mid][0] > t:
                right = mid - 1
            else:
                left = mid

        return self.s[left][1]

    def totalScore(self, startTime, endTime):

        return self.get(endTime) - self.get(startTime - 1)

''',
    call='''t = ExamTracker()
out = []
t.record(1, 98)
t.record(5, 99)
out.append(t.totalScore(1, 5))
out.append(t.totalScore(3, 4))
out''',
    expect=[197, 0],
    views=[
        dict(type='custom', draw=_draw, h=410),
        dict(type='text', fn=lambda S: _top(S), size=24, h=96),
        dict(type='calls', label='正在执行的方法', h=140),
    ],
    watch=[('left', 'left', 'blue'), ('mid', 'mid', 'orange'), ('right', 'right', 'pink'), ('t', 't', 'cyan')],
    skip=['while left < right'],
    captions={
        'self.s = [(0, 0)]': '`s[i] = (时间, 前缀和)`：先放哨兵 `(0, 0)`，时间 0 之前前缀和为 0',
        'self.s.append': lambda S, B, r: '追加 `({}, {} + {})` = `({}, {})`：前缀和 = 上一项 + 本次分数'.format(
            S.time, S['self.s'][-2][1], S.score, S['self.s'][-1][0], S['self.s'][-1][1]),
        'left = 0': lambda S, B, r: ('`get({})`：在时间递增的 `s` 上二分，找==最后一个时间 ≤ {}==的位置'.format(S.t, S.t) if _first(S)
                                     else '`get({})`：同样二分，找最后一个时间 ≤ {} 的位置'.format(S.t, S.t)),
        'right = len(self.s) - 1': lambda S, B, r: ('二分范围 `[left, right] = [0, {}]`；哨兵时间 0 ≤ 任何 `t`，答案一定存在'.format(S.right) if _first(S)
                                                    else '二分范围 `[0, {}]`'.format(S.right)),
        'mid = (left + right + 1) // 2': lambda S, B, r: (
            '`mid = ({} + {} + 1) // 2` = =={}==：==向上取整==，否则 `left = mid` 会死循环'.format(S.left, S.right, S.mid)
            if (_first(S) and S.left == 0 and S.right == len(S['self.s']) - 1) else
            '`mid = ({} + {} + 1) // 2` = =={}=='.format(S.left, S.right, S.mid)),
        'if self.s[mid][0] > t': _cmp,
        'right = mid - 1': '`mid` 太晚，连同右边一起丢掉：`right` = =={right}==',
        'left = mid': '`mid` 不晚于 `t`，保留它（可能就是答案）：`left` = =={left}==',
        'return self.s[left][1]': _ret_get,
        'return self.get(endTime)': lambda S, B, r: '`totalScore({a}, {b})` = `get({b}) − get({a} − 1)`：各二分一次，再相减'.format(a=S.startTime, b=S.endTime),
    },
    cards=dict(
        one_liner='把区间和变成两个前缀和相减：先二分找位置，再相减',
        complexity='`record` `O(1)`，`totalScore` `O(log q)`，空间 `O(q)`',
        problem=['`record(time, score)`：记录一次考试；`time` 严格递增',
                 '`totalScore(startTime, endTime)`：时间在闭区间内的考试分数之和，没有就是 0',
                 '示例：`record(1,98)`、`record(5,99)`、`totalScore(1,5)` → `197`',
                 '再查 `totalScore(3,4)`：时间 3~4 没有考试 → `0`'],
        quote='由于本题是在线的，因此需要先对查询的起始和终止时间在record记录的时间序列中二分，得到区间的起点和终点，然后再使用前缀和之差计算对应的区间和。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目实际是==区间和==问题：转成前缀和，`区间和 = get(end) − get(start − 1)`',
              '`s[i] = (时间, 前缀和)`，开头放哨兵 `(0, 0)`',
              '`get(t)`：在 `s` 上二分，找最后一个时间 `≤ t` 的位置，返回它的前缀和'],
        summary=['`record` `O(1)`，`totalScore` `O(log q)`（两次二分）',
                 '易错：`mid` 要向上取整（`+1`），否则 `left = mid` 会死循环',
                 '`startTime − 1` 才能包含 `startTime` 当天的考试；哨兵保证 `get(0)` 不越界',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神用 `times` 和 `pre_sum` 两个数组 + `bisect`，yiduobo 手写二分'],
    ),
)
