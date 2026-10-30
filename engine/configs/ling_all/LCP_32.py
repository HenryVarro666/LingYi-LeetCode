TASKS = [[1, 3, 2], [2, 5, 3], [5, 6, 2]]
LO, HI = 0, 7


def _cur(S):
    if 'start' not in S or 'tasks' not in S:
        return None
    for k, t in enumerate(S['tasks']):
        if t[0] == S['start'] and t[1] == S['end']:
            return k
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴：黄 = 当前任务区间，绿 = 栈里已开机的时间段', 22, T['muted'], bold=True)
    L, R = x0 + 130, x1 - 50
    unit = (R - L) / (HI - LO + 1)

    def X(v):
        return L + (v - LO) * unit
    top, axis = y0 + 56, y1 - 50
    for v in range(LO, HI + 1):
        cv.line([(X(v) + unit / 2, top), (X(v) + unit / 2, axis)], (36, 42, 52), 1)
        cv.text((X(v) + unit / 2, axis + 8), v, 22, T['dim'], anchor='mt', mono=True)
    tasks = S.get('tasks') or TASKS
    k = _cur(S)
    rowh = 38
    for j, t in enumerate(tasks):
        a, b = t[0], t[1]
        need = TASKS_NEED.get((a, b), t[2])
        y = top + j * rowh
        col = T['yellow'] if j == k else ((96, 110, 130) if (k is not None and j < k) else (70, 78, 90))
        cv.rect((X(a) + 4, y, X(b) + unit - 4, y + 24), fill=col, r=12)
        cv.text((X(a) - 2, y + 12), f'[{a},{b}] 需{need}', 17, T['muted'], anchor='rm', mono=True)
    y = top + len(tasks) * rowh + 26
    cv.text((L - 20, y + 26), 'st', 24, T['green'], anchor='rm', bold=True, mono=True)
    for (l, r, s) in S.get('st', []):
        if r < 0:
            continue
        cv.rect((X(l) + 4, y, X(r) + unit - 4, y + 52), fill=T['green'], r=10, alpha=200)
        cv.text(((X(l) + X(r) + unit) / 2, y + 26), f'[{l},{r}]', 24, T['bg'], anchor='mm', bold=True, mono=True)


TASKS_NEED = {(a, b): d for a, b, d in TASKS}


CONFIG = dict(
    num='LCP 32', title='批量处理任务', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='右端点排序 + 栈合并后缀 + 二分',
    tags=['灵神题单·贪心与思维', '贪心算法'],
    code='''
class Solution:
    def processTasks(self, tasks: List[List[int]]) -> int:
        tasks.sort(key=lambda t: t[1])
        st = [(-2, -2, 0)]  # 闭区间左右端点，栈底到栈顶的区间长度的和
        for start, end, d in tasks:
            _, r, s = st[bisect_left(st, (start,)) - 1]
            d -= st[-1][2] - s  # 去掉运行中的时间点
            if start <= r:  # start 在区间 st[i] 内
                d -= r - start + 1  # 去掉运行中的时间点
            if d <= 0: continue
            while end - st[-1][1] <= d:  # 剩余的 d 填充区间后缀
                l, r, _ = st.pop()
                d += r - l + 1  # 合并区间
            st.append((end - d + 1, end, st[-1][2] + d))
        return st[-1][2]
''',
    call=f'Solution().processTasks({TASKS})',
    expect=4,
    views=[
        dict(type='stack', var='st', label='st：(左端点, 右端点, 前缀长度和)', h=150, fmt=lambda x: str(x)),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'cyan'), ('d', 'd', 'orange'), ('开机时长', 'st[-1][2]', 'green')],
    captions={
        'tasks.sort': '==按右端点从小到大排序==：右边的任务要么和它不相交，要么只盖住它的==后缀==',
        'st = [': '栈里放已开机的闭区间，每项带「到此为止一共开了多久」；`(-2,-2,0)` 是哨兵',
        'for start, end, d': '取任务 `[{start}, {end}]`，需要开机 `{d}` 个时间点',
        '_, r, s =': '二分栈：定位 `start` 所在（或左边最近）的区间，`r = {r}`，`s = {s}`（它之前累计的时长）',
        'd -= st[-1][2] - s': '前缀和相减：栈里整段落在区间内的已开机 `{st[-1][2] - s}` 个点，任务还差 ==d = {d}==',
        'd -= r - start + 1': '`start` 落在栈中区间内：再减去 `[{start}, {r}]` 这 `{r - start + 1}` 个点 → `d = {d}`',
        'if start <= r': lambda S, B, ret: (f'`start = {S.start} <= r = {S.r}`：start 落在已开机区间里，里面的点也算' if S.start <= S.r
                                            else f'`start = {S.start} > r = {S.r}`：已开机区间都在 start 左边，不用再减'),
        'if d <= 0': lambda S, B, ret: (f'`d = {S.d} <= 0`：已开机的时间够了，`continue`' if S.d <= 0
                                        else f'`d = {S.d} > 0`：还差 {S.d} 个点，要在区间后缀补开机'),
        'while end - st[-1][1] <= d': lambda S, B, ret: (
            f'`end - st[-1][1] = {S.end - S.st[-1][1]} <= d = {S.d}`：补的后缀会和栈顶区间连成一片 → ==合并=='
            if S.end - S.st[-1][1] <= S.d else f'`end - st[-1][1] = {S.end - S.st[-1][1]} > d = {S.d}`：补的后缀和栈顶接不上 → 不用合并'),
        'l, r, _ = st.pop()': '弹出栈顶 `[{l}, {r}]`',
        'd += r - l + 1': '它的 `{r - l + 1}` 个点并入新区间 → ==d = {d}==',
        'st.append': '把 `[{end - d + 1}, {end}]` 开机，累计 `{st[-1][2]}` 个时间点',
        'return st[-1][2]': '栈顶的前缀和就是电脑最少开机时长：=={ret}==',
    },
    cards=dict(
        one_liner='右端点排序，缺的开机时间补在区间后缀，栈合并',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['任务 `[start, end, period]`：在闭区间内需要 `period` 个时间点（可不连续）',
                 '电脑开机时可同时处理任意多个任务，求最少开机时长',
                 '本视频（示例 1）：`[[1,3,2],[2,5,3],[5,6,2]]` → `4`'],
        quote='对于 tasks[i] 来说，它右侧的任务要么和它没有交集，要么包含它的区间后缀。……尽量把新增的时间点安排在区间 [start,end] 的后缀上，这样下一个区间就能统计到更多已有的时间点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按右端点排序，补的点放在区间==最右侧==，后面的任务更容易蹭到',
              '暴力用数组 `run` 标记开机点，数一数再补；时间点太多会超时',
              '补点总是从右往左，所以连成的区间可以放进==栈==，存前缀长度和',
              '在栈里二分 `start`，前缀和相减就能 `O(log n)` 数出区间内已开机时长'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '提示 3 的暴力写法 `O(nU)`，`U` 可达 10^9，会超时/超内存，视频演示的是栈优化版',
                 '先排序再贪心：补点只能补在区间后缀，不能补在前面',
                 '`start` 所在区间那一部分单独算：`r - start + 1`，别重复数',
                 '同类题：2589 完成所有任务的最少时间；757 是 `period = 2` 的特例'],
    ),
)
