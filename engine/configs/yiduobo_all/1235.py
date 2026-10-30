ST = [1, 2, 3, 3]
EN = [3, 4, 5, 6]
PR = [50, 10, 40, 70]
SORTED = sorted(zip(ST, EN, PR), key=lambda d: d[1])
LOOP = 6
BS = range(10, 20)


def _cur(S):
    if 's' not in S or 'e' not in S:
        return None
    t = (S['s'], S['e'], S['p'])
    return SORTED.index(t) if t in SORTED else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'info：按结束时间排序（黄 = 当前工作）', 24, T['muted'], bold=True)
    hi = max(EN)
    L, R = x0 + 90, x1 - 50
    X = lambda v: L + v / hi * (R - L)
    cur = _cur(S)
    if S.get('_line') == LOOP and B.get('s') == S.get('s') and B.get('e') == S.get('e'):
        cur = None
    rowh = min(50, (y1 - y0 - 90) / len(SORTED))
    y = y0 + 44
    for k, (s, e, p) in enumerate(SORTED):
        c = T['yellow'] if k == cur else ((110, 120, 132) if cur is None or k < cur else (60, 66, 76))
        cv.text((x0 + 24, y + rowh / 2), f'#{k}', 20, T['dim'], anchor='lm', mono=True)
        cv.rect((X(s), y + 6, X(e), y + rowh - 6), fill=c, r=8)
        cv.text(((X(s) + X(e)) / 2, y + rowh / 2), f'{p}', 22, T['bg'], anchor='mm', bold=True)
        cv.text((X(s) - 6, y + rowh / 2), str(s), 18, T['muted'], anchor='rm')
        cv.text((X(e) + 6, y + rowh / 2), str(e), 18, T['muted'], anchor='lm')
        y += rowh
    for v in range(0, hi + 1):
        cv.text((X(v), y1 - 24), str(v), 16, T['dim'], anchor='mt')


def _p(name):
    return lambda S: S.get(name) if S.get('_line') in BS else None


PL, PR_, PM = _p('l'), _p('r'), _p('mid')


def _text(S):
    if 'f' not in S:
        return '`f`：只保留==可能成为答案==的（结束时间, 收益），两者都单调递增'
    if S.get('_line') in BS and 'l' in S:
        return f"二分：在 `f[{S['l']}..{S['r']}]` 中找结束时间 `≤ {S['s']}` 的==最大== j"
    return '`f[j] = [结束时间, 收益]`：结束越晚收益越高，否则没必要保留'


def _cap_if(S, B, ret):
    s, last = S.s, S.f[-1][0]
    if s >= last:
        return f'`s = {s} ≥ {last}`（f 中最晚结束时间）：接在所有方案之后，==收益直接累加=='
    return f'`s = {s} < {last}`：和最后的方案冲突 → 二分找 `结束时间 ≤ {s}` 的最大 j'


def _cap_mid(S, B, ret):
    m = S.mid
    if S.f[m][0] <= S.s:
        return f'`f[{m}][0] = {S.f[m][0]} ≤ {S.s}`：mid 可行，答案在 mid 或右边 → `l = mid`'
    return f'`f[{m}][0] = {S.f[m][0]} > {S.s}`：mid 太晚 → `r = mid − 1`'


def _cap_gain(S, B, ret):
    r, p = S.r, S.p
    v, last = S.f[r][1] + p, S.f[-1][1]
    if v > last:
        return f'`f[{r}][1] + {p} = {v} > {last}`：比当前最好还高 → 值得保留'
    return f'`f[{r}][1] + {p} = {v} ≤ {last}`：结束更晚收益却不更高 → ==没有保留的必要=='


CONFIG = dict(
    num=1235, title='规划兼职工作', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按结束时间排序 · 单调序列 + 二分',
    tags=['labuladong', '灵神题单·动态规划', '难度分 2023'],
    code='''
class Solution(object):
    def jobScheduling(self, startTime, endTime, profit):

        info = sorted(zip(startTime, endTime, profit), key=lambda d:d[1])
        f = [[0, 0]]
        for s, e, p in info:
            if s >= f[-1][0]:
                f.append([e, f[-1][1] + p])
            else:
                l = 0
                r = len(f) - 1
                while l < r:
                    mid = (l + r + 1) >> 1
                    if f[mid][0] <= s:
                        l = mid
                    else:
                        r = mid - 1

                if f[r][1] + p > f[-1][1]:
                    f.append([e, f[r][1] + p])

        return f[-1][1]
''',
    call=f'Solution().jobScheduling({ST}, {EN}, {PR})',
    expect=120,
    skip=['l = 0', 'r = len(f) - 1'],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=_text, size=24, h=56),
        dict(type='array', var=lambda S: [x[0] for x in S['f']], label='f[j][0]：结束时间', h=235, cell=90, min_slots=4,
             pointers={PL: 'blue', PR_: 'pink', PM: 'yellow'}, pointer_labels={PL: 'l', PR_: 'r', PM: 'mid'}),
        dict(type='array', var=lambda S: [x[1] for x in S['f']], label='f[j][1]：收益', h=120, cell=90, min_slots=4, index=False),
    ],
    watch=[('s', 's', 'yellow'), ('e', 'e'), ('p', 'p'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid')],
    captions={
        'info = sorted(': '按==结束时间==从小到大排序：希望工作尽快完结，同时收入最高',
        'f = [[0, 0]]': '`f` 存单调序列 `[结束时间, 收益]`，初始 `[0, 0]`',
        'for s, e, p in info': lambda S, B, r: (f'工作 `[{S.s}, {S.e}]`，报酬 `{S.p}`'
                                                if (B.get('s'), B.get('e')) != (S.s, S.e) else '所有工作处理完'),
        'if s >= f[-1][0]': _cap_if,
        "f.append([e, f[-1][1] + p])": '`f` 末尾加入 `[{e}, {f[-1][1]}]`：结束时间 `{e}` 必然大于 f 中所有时间',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，继续二分' if S.l < S.r else f'`l = r = {S.r}`：找到 j'),
        'mid = (l + r + 1) >> 1': '`mid = ({l} + {r} + 1) >> 1 = {mid}`（向上取整，避免 `l = mid` 死循环）',
        'if f[mid][0] <= s': _cap_mid,
        15: '`l` → {l}',
        'r = mid - 1': '`r` → {r}',
        'if f[r][1] + p > f[-1][1]': _cap_gain,
        "f.append([e, f[r][1] + p])": '`f` 末尾加入 `[{e}, {f[-1][1]}]`：接在 `f[{r}]` 之后做这份工作',
        'return f[-1][1]': '单调序列最后一项收益最高：=={ret}==',
    },
    cards=dict(
        one_liner='按结束时间排序，只保留「结束更晚、收益更高」的单调序列',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 份兼职：`[startTime[i], endTime[i]]`，报酬 `profit[i]`',
                 '时间重叠的工作不能同时做（在 X 结束可以立刻做 X 开始的）；求最大报酬',
                 f'示例 / 本视频：`startTime = {ST}`，`endTime = {EN}`，`profit = {PR}` → `120`'],
        quote='若存在某个f[i][p] <= f[i][q]，同时有p >= q，那么这里的f[i][p]就==没有存在的必要==的。因此我们在执行过程中不需要所有的时间点，而只需要保留可能成为答案的那些时间点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：前 i 件工作、最后完结时刻为 j 的最大收益',
              '结束更晚、收益却不更高的状态可以扔掉 → `f` 关于时间==单调递增==',
              '当前工作：二分找结束时间 `≤ start` 的最大 j，收益更高才追加到末尾'],
        summary=['时间 `O(n log n)`：排序 + 每份工作一次二分',
                 '二分找「最后一个 ≤ s」：`mid` 要向上取整 `(l + r + 1) >> 1`',
                 '易错：追加前要判断 `f[r][1] + p > f[-1][1]`，否则单调性被破坏',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神用 `f[i]` 表示前 i 个工作 + `bisect_left`，选或不选'],
    ),
)
