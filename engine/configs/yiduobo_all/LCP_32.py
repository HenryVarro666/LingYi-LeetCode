TASKS = [[5, 6, 2], [1, 7, 6], [2, 4, 1]]
LO, HI = 0, 8
NEED = {(a, b): p for a, b, p in TASKS}


def _cur(S):
    if 'x' not in S or 'tasks' not in S:
        return None
    for k, t in enumerate(S['tasks']):
        if t[0] == S['x'] and t[1] == S['y']:
            return k
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴：黄 = 当前任务区间，绿 = open_list 里已开机的时间段', 22, T['muted'], bold=True)
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
        y = top + j * rowh
        col = T['yellow'] if j == k else ((96, 110, 130) if (k is not None and j < k) else (70, 78, 90))
        cv.rect((X(a) + 4, y, X(b) + unit - 4, y + 24), fill=col, r=12)
        cv.text((X(a) - 2, y + 12), f'[{a},{b}] 需{NEED.get((a, b), t[2])}', 17, T['muted'], anchor='rm', mono=True)
    y = top + len(tasks) * rowh + 26
    cv.text((L - 20, y + 26), 'open_list', 22, T['green'], anchor='rm', bold=True, mono=True)
    for l, r in S.get('open_list', []):
        cv.rect((X(l) + 4, y, X(r) + unit - 4, y + 52), fill=T['green'], r=10, alpha=200)
        cv.text(((X(l) + X(r) + unit) / 2, y + 26), f'[{l},{r}]', 24, T['bg'], anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num='LCP 32', title='批量处理任务', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='按终点排序 + 开机段列表 + 前缀和二分',
    tags=['灵神题单·贪心与思维', '贪心算法'],
    code='''
class Solution(object):
    def processTasks(self, tasks):

        tasks.sort(key=lambda d:d[1])
        open_list = []
        s = []
        for x, y, p in tasks:
            if open_list and x <= open_list[-1][1]:
                l = 0
                r = len(open_list) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if open_list[mid][1] >= x:
                        r = mid
                    else:
                        l = mid + 1
                
                #二分找到[x, y]包含的开机时间，并计算还需要的开机时间p
                p -= s[-1] - s[l]
                if x <= open_list[l][0]:
                    p -= open_list[l][1] - open_list[l][0] + 1
                else:
                    p-= open_list[l][1] - x + 1
                
            if p > 0:
                #需要新增的开机时间区间为[y - p + 1, y]，如果出现了重合，那么就将其弹出并更新s和p
                while open_list and open_list[-1][1] >= y - p + 1:
                    s.pop()
                    p += open_list[-1][1] - open_list[-1][0] + 1
                    open_list.pop()                    
                #将新的开机区间加入到open_list并更新s
                open_list.append([y - p + 1, y])
                if not s:
                    s.append(p)
                else:
                    s.append(s[-1] + p)

        return s[-1]
''',
    call=f'Solution().processTasks({TASKS})',
    expect=6,
    views=[
        dict(type='array', var='s', label='s：open_list 各段时长的前缀和', h=190, cell=100),
        dict(type='custom', draw=_draw, h=400),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'cyan'), ('p', 'p', 'orange'), ('开机总时长', 's[-1] if s else 0', 'green')],
    captions={
        'tasks.sort': '==按终点从小到大排序==：把靠前区间的后半段开机，更可能惠及后面的区间',
        'open_list = []': '`open_list` 记录已经开机的时间段，从左到右单调递增',
        's = []': '`s` 是 `open_list` 各段时长的前缀和，用来 `O(1)` 求一片段的总时长',
        'for x, y, p': lambda S, B, ret: ('所有任务都处理完了' if B.get('x') == S.x and B.get('y') == S.y and 'x' in B else f'处理任务 `[{S.x}, {S.y}]`，需要开机 `{S.p}`'),
        9: '二分的范围：`l = 0`',
        10: '`r = {r}`（最后一段），在 `open_list` 里找第一段右端 `>= x` 的',
        'if open_list and x <= open_list[-1][1]': lambda S, B, ret: (
            f'`x = {S.x} <= {S.open_list[-1][1]}`（最后一段的右端）：[x, y] 里已有一部分机器开着' if S.open_list and S.x <= S.open_list[-1][1]
            else '`open_list` 为空或都在 x 左边：没有已开机时间可蹭'),
        'mid = (l + r) >> 1': '二分：找 `open_list` 中右端 `>= x` 的第一段（`l = {l}`，`r = {r}`，`mid = {mid}`）',
        'if open_list[mid][1] >= x': lambda S, B, ret: (f'`{S.open_list[S.mid][1]} >= x = {S.x}` → 答案在 mid 或左边，`r = mid`' if S.open_list[S.mid][1] >= S.x
                                                       else f'`{S.open_list[S.mid][1]} < x = {S.x}` → 这段在 x 左边，`l = mid + 1`'),
        'r = mid': '`r = {r}`',
        'l = mid + 1': '`l = {l}`',
        'p -= s[-1] - s[l]': '第 `{l}` 段右边的整段都在 [x, y] 内：减去前缀和之差 → `p = {p}`',
        'if x <= open_list[l][0]': lambda S, B, ret: (f'`x = {S.x} <= {S.open_list[S.l][0]}`：第 {S.l} 段整段在区间内' if S.x <= S.open_list[S.l][0]
                                                      else f'`x = {S.x} > {S.open_list[S.l][0]}`：第 {S.l} 段只有 `[x, {S.open_list[S.l][1]}]` 在区间内'),
        'p -= open_list[l][1] - open_list[l][0] + 1': '整段减去：`p = {p}`',
        'p-= open_list[l][1] - x + 1': '只减 `x` 到段尾这一截：`p = {p}`',
        'if p > 0': lambda S, B, ret: (f'`p = {S.p} > 0`：还要新开 {S.p} 个时间点，从区间末尾往前安排' if S.p > 0
                                       else f'`p = {S.p} <= 0`：已有开机时间已经够了'),
        'while open_list and open_list[-1][1] >= y - p + 1': lambda S, B, ret: (
            f'新增区间应是 `[{S.y - S.p + 1}, {S.y}]`，和最后一段 `{S.open_list[-1]}` 重叠 → ==先删掉旧段，把时长并回 p=='
            if S.open_list and S.open_list[-1][1] >= S.y - S.p + 1 else '新增区间和 `open_list` 不再重叠，不用合并'),
        's.pop()': '前缀和 `s` 同步弹出一项',
        'p += open_list[-1][1]': '旧段的时长加回 `p` → ==p = {p}==',
        'open_list.pop()': '删掉旧段，`open_list` 剩 {len(open_list)} 段',
        'open_list.append': '新开机段 `[{y - p + 1}, {y}]` 加入 `open_list`',
        'if not s': lambda S, B, ret: ('`s` 为空：前缀和就是 p' if not S.s else '`s` 不空：在上一项基础上累加'),
        's.append(p)': '`s = {s}`',
        's.append(s[-1] + p)': '`s = {s}`',
        'return s[-1]': '`s[-1]` 就是所有开机段的总时长：=={ret}==',
    },
    cards=dict(
        one_liner='按终点排序，缺的开机时间安排在区间末尾',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['任务 `[start, end, period]`：在闭区间内需要开机 `period` 个时间点（可不连续）',
                 '开机时可同时处理任意多个任务，求最少开机时长',
                 '本视频：`[[5,6,2],[1,7,6],[2,4,1]]` → `6`'],
        quote='选择对区间的终点排序是比较自然的想法，因为排序之后，如果尽量将靠前区间的后半部分时间开机的话，就更有可能惠及到后续的区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['终点排序后，对每个区间先算==已有的开机时间==，不够再从区间末尾往前补',
              '新开机段总是更靠右，`open_list` 单调递增 → 可以对起点二分，前缀和 `s` 求时长',
              '补的新段若和旧段重叠：先把旧段==删掉并把时长并回 p==，再一次性安排',
              '每段只进出一次，整体均摊 `O(1)`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '二分找的是第一个右端 `>= x` 的段，它可能只有一部分在区间内，要单独算',
                 '合并重叠段时，`s` 和 `open_list` 要同步弹出，并把时长加回 `p`',
                 '最后答案是 `s[-1]`（总时长），不要忘了任务都要处理完',
                 '对比灵神：灵神把栈项做成 `(l, r, 前缀和)` 一个元组；yiduobo 拆成 `open_list` 和 `s` 两个数组'],
    ),
)
