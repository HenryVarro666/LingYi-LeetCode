ST = [1, 2, 3, 4, 6]
EN = [3, 5, 10, 6, 9]
PR = [20, 20, 100, 70, 60]
ACTIVE = (5, 6, 8)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    jobs = S.get('jobs')
    if not jobs:
        jobs = [(e, s, p) for s, e, p in zip(ST, EN, PR)]
        title = '工作（未排序）'
    else:
        title = 'jobs：按结束时间排序（黄 = 第 i 个，绿 = 前 j 个，都不和它重叠）'
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    lo, hi = 0, max(e for e, _, _ in jobs)
    L, R = x0 + 90, x1 - 50
    X = lambda v: L + (v - lo) / (hi - lo) * (R - L)
    live = S.get('_line') in ACTIVE and 'i' in S and not (S.get('_line') == 5 and B.get('i') == S.get('i'))
    i = S.get('i') if live else None
    j = S.get('j') if live and S.get('_line') != 5 else None
    rowh = min(52, (y1 - y0 - 100) / len(jobs))
    y = y0 + 48
    for k, (e, s, p) in enumerate(jobs):
        c = (110, 120, 132)
        if i is not None and k == i:
            c = T['yellow']
        elif j is not None and k < j:
            c = T['green']
        elif i is not None and k > i:
            c = (60, 66, 76)
        cv.text((x0 + 24, y + rowh / 2), f'#{k}', 20, T['dim'], anchor='lm', mono=True)
        cv.rect((X(s), y + 6, X(e), y + rowh - 6), fill=c, r=8)
        cv.text(((X(s) + X(e)) / 2, y + rowh / 2), f'{p}', 22, T['bg'], anchor='mm', bold=True)
        cv.text((X(s) - 6, y + rowh / 2), str(s), 18, T['muted'], anchor='rm')
        cv.text((X(e) + 6, y + rowh / 2), str(e), 18, T['muted'], anchor='lm')
        y += rowh
    if i is not None:
        st = jobs[i][1]
        cv.dashed((X(st), y0 + 44), (X(st), y + 4), T['yellow'], 2)
    for v in range(lo, hi + 1):
        cv.text((X(v), y1 - 24), str(v), 16, T['dim'], anchor='mt')


def _text(S, B):
    line = S.get('_line')
    if 'f' not in S:
        return '按结束时间排序后，`f[i]` = ==前 i 个==工作的最大报酬'
    if line == 8:
        i, j, p, f = S['i'], S['j'], S['p'], S['f']
        return f"`f[{i + 1}] = max(f[{i}], f[{j}] + {p}) = max({f[i]}, {f[j] + p})` = =={f[i + 1]}=="
    return '`f[i]`：前 i 个工作的最大报酬，`f[0] = 0`'


def _fcol(S, k, v):
    if S.get('_line') != 8:
        return None
    i, j = S['i'], S['j']
    if k == i + 1:
        return 'yellow'
    if k == i:
        return 'blue'
    if k == j:
        return 'green'
    return None


def _max(S, B, ret):
    i, j, p, f = S.i, S.j, S.p, S.f
    no, yes = f[i], f[j] + p
    if yes > no:
        return f'选第 {i} 个：`f[{j}] + {p} = {yes}` > 不选 `f[{i}] = {no}` → `f[{i + 1}] = {yes}`'
    return f'不选第 {i} 个：`f[{i}] = {no}` ≥ 选 `f[{j}] + {p} = {yes}` → `f[{i + 1}] = {no}`'


CONFIG = dict(
    num=1235, title='规划兼职工作', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='按结束时间排序 · 选或不选 DP + 二分',
    tags=['labuladong', '灵神题单·动态规划', '难度分 2023'],
    code='''
class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))  # 按照结束时间排序
        f = [0] * (len(jobs) + 1)
        for i, (_, st, p) in enumerate(jobs):
            j = bisect_left(jobs, (st + 1,), hi=i)  # hi=i 表示二分上界为 i（默认为 n）
            # 状态转移中，为什么是 j 不是 j+1：上面算的是 > st，-1 后得到 <= st，但由于还要 +1，抵消了
            f[i + 1] = max(f[i], f[j] + p)
        return f[-1]
''',
    call=f'Solution().jobScheduling({ST}, {EN}, {PR})',
    expect=150,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=_text, size=24, h=56),
        dict(type='array', var='f', label='f（黄 = f[i+1]，蓝 = 不选 f[i]，绿 = 选 f[j]）', h=190, cell=80, color=_fcol),
    ],
    watch=[('i', 'i', 'yellow'), ('st', 'st'), ('p', 'p'), ('j', 'j', 'green')],
    captions={
        'jobs = sorted(': '按结束时间排序：`jobs` 里每项是 `(end, start, profit)`',
        'f = [0] * (len': '`f[0] = 0`：前 0 个工作报酬为 0；下标整体 +1 避免 `f[-1]`',
        'for i, (_, st, p)': lambda S, B, r: (f'第 `{S.i}` 个工作：`[{S.st}, {S.jobs[S.i][0]}]`，报酬 `{S.p}`'
                                               if B.get('i') != S.get('i') else '所有工作处理完'),
        'j = bisect_left': '二分找结束时间 `> {st}` 的第一个位置 `j = {j}` → 前 ==j 个==工作都在 `{st}` 或之前结束（不重叠）',
        'f[i + 1] = max': _max,
        'return f[-1]': '前 n 个工作的最大报酬 `f[{len(jobs)}]` = =={ret}==',
    },
    cards=dict(
        one_liner='按结束时间排序，第 i 个工作选或不选',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 份兼职：`[startTime[i], endTime[i]]`，报酬 `profit[i]`',
                 '时间重叠的工作不能同时做（在 X 结束可以立刻做 X 开始的）；求最大报酬',
                 f'示例 / 本视频：`startTime = {ST}`，`endTime = {EN}`，`profit = {PR}` → `150`'],
        quote='不选第 i 个工作，那么最大报酬等于前 i−1 个工作的最大报酬；选第 i 个工作，设 j 是最大的满足 ==endTime[j] ≤ startTime[i]== 的 j，那么最大报酬等于前 j 个工作的最大报酬加上 profit[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按结束时间排序后，前 j 个工作都==不会与第 i 个重叠==',
              '`f[i+1] = max(f[i], f[j+1] + profit[i])`，`f[0] = 0`',
              '结束时间有序 → `j` 用二分：查 `≥ st + 1` 等价于查 `> st`'],
        summary=['时间 `O(n log n)`：排序 + n 次二分',
                 '为什么是 `f[j]`：二分得到的是 `> st`，`−1` 得 `≤ st`，再 `+1` 抵消',
                 '`hi=i`：只在前 i 个里找；`(st + 1,)` 这个元组比任何 `(st, …)` 都大',
                 '同类题：1751. 最多可以参加的会议数目 II、2008. 出租车的最大盈利'],
    ),
)
