N = 5
PRE = [[1, 0], [2, 1], [2, 3], [4, 2]]
POS = {0: (0.0, 0.08), 1: (0.42, 0.08), 3: (0.0, 0.92), 2: (0.42, 0.92), 4: (0.84, 0.5)}


def draw_graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('g')
    if not g:
        return
    ind = S.get('ind') or [0] * len(g)
    q = S.get('q') or []
    l = S.get('l', 0)
    now = S.get('now')
    nxt = S.get('next_lesson')
    W, H, R = (x1 - x0) * 0.5, (y1 - y0) - 110, 28

    def P(u):
        fx, fy = POS[u]
        return x0 + 70 + fx * W, y0 + 52 + fy * H

    hot_edge = (now, nxt) if S['_line'] in (19, 20, 21, 22) else None
    if S['_line'] in (9, 10, 11):
        hot_edge = (S.get('pre_lesson'), S.get('lesson'))
    for u, vs in enumerate(g):
        for v in vs:
            (ax, ay), (bx, by) = P(u), P(v)
            dx, dy = bx - ax, by - ay
            Ln = max(1.0, (dx * dx + dy * dy) ** 0.5)
            ux, uy = dx / Ln, dy / Ln
            hot = (u, v) == hot_edge
            used = 'now' in S and u in q[:l] and not hot
            c = T['yellow'] if hot else (T['dim'] if used else T['muted'])
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)), c, 5 if hot else 3, 14)
    for u in range(len(g)):
        X, Y = P(u)
        if 'l' in S and u in q[:l]:
            f = T['green']
        elif 'l' in S and u in q:
            f = T['blue']
        else:
            f = None
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=f or T['panel2'],
                     outline=T['text'] if u == now else T['border'], width=4 if u == now else 2)
        cv.text((X, Y), u, 28, T['bg'] if f else T['text'], anchor='mm', bold=True)
        up = u in (0, 1)
        cv.text((X, Y - R - 4 if up else Y + R + 6), f'入度 {ind[u]}', 19, T['yellow'] if u == nxt and 'now' in S else T['muted'],
                anchor='mb' if up else 'mt')
    lx = x0 + 70 + W * 0.84 + 110
    for k, (name, f) in enumerate([('还有先修课没学', None), ('可以学了（在队列中）', 'blue'), ('已学（已出队）', 'green')]):
        yy = y0 + 30 + k * 44
        cv.d.ellipse((lx, yy, lx + 26, yy + 26), fill=T[f] if f else T['panel2'], outline=T['border'])
        cv.text((lx + 38, yy + 13), name, 20, T['muted'], anchor='lm')
    cv.text((lx, y0 + 30 + 3 * 44 + 6), '箭头 a → b：学完 a 才能学 b', 19, T['dim'], anchor='la')


_state = {'first': False}


def _pop(S, B, ret):
    _state['first'] = True
    return f'出队 `now = {S.now}`：它的先修课都学完了，==排进课程顺序=='


def _next(S, B, ret):
    first, _state['first'] = _state['first'], False
    if not S.g[S.now]:
        return f'没有以 `{S.now}` 为先修课的课'
    if first or B.next_lesson != S.next_lesson:
        return f'`{S.now}` 是 `{S.next_lesson}` 的先修课'
    return f'`{S.now}` 的后继课程处理完了'


def _edge(S, B, ret):
    if 'lesson' in B and (B.lesson, B.pre_lesson) == (S.lesson, S.pre_lesson):
        return '建图完成'
    return f'`[{S.lesson}, {S.pre_lesson}]`：学 `{S.lesson}` 之前要先学 `{S.pre_lesson}`'


CONFIG = dict(
    num=210, title='课程表 II', difficulty='Medium', category='图论',
    author='yiduobo', technique='拓扑排序 · BFS 队列即课程顺序',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def findOrder(self, numCourses, prerequisites):

        if numCourses == 0:
            return 0

        g = [[] for _ in range(numCourses)]
        ind = [0] * numCourses
        for lesson, pre_lesson in prerequisites:
            g[pre_lesson].append(lesson)
            ind[lesson] += 1

        q = [index for index in range(numCourses) if ind[index] == 0]
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next_lesson in g[now]:
                ind[next_lesson] -= 1
                if ind[next_lesson] == 0:
                    q.append(next_lesson)
                    r += 1

        if len(q) == numCourses:
            return q
        else:
            return []
''',
    call=f'Solution().findOrder({N}, {PRE})',
    expect=[0, 3, 1, 2, 4],
    skip=['if numCourses == 0', 'l += 1', 'r += 1'],
    views=[
        dict(type='custom', draw=draw_graph, h=300),
        dict(type='array', var='ind', label='ind（入度 = 还剩几门先修课没学）', cell=76,
             color=lambda S, i, v: 'yellow' if i == S.get('next_lesson') and 'now' in S else None),
        dict(type='array', var='q', label='q（BFS 队列 = 一种可行的课程顺序；灰 = 已出队）', cell=76, min_slots=5,
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S['l']),
    ],
    watch=[('now', 'now'), ('next_lesson', 'next_lesson', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'g = [[] for': '`g[a]`：以 `a` 为先修课的课程列表',
        'ind = [0]': '`ind[b]`：课程 `b` 的入度（先修课数量）',
        'for lesson, pre_lesson in': _edge,
        'g[pre_lesson].append(lesson)': '建边 `{pre_lesson} → {lesson}`',
        'ind[lesson] += 1': '`{lesson}` 多一门先修课：`ind[{lesson}]` = {ind[lesson]}',
        'q = [index for': '入度为 0 的课 `{q}` 没有先修课，==可以直接学==，先入队',
        'l = 0': '`l` 指向队首（下一门要学的课）',
        'r = len(q)': '`r = {r}`：队尾（已入队的课程数）',
        'while l < r': lambda S, B, ret: (f'`l = {B.l} < r = {B.r}`：还有能学的课' if B.l < B.r
                                          else f'`l = r = {B.r}`：没有能学的课了，拓扑排序结束'),
        'now = q[l]': _pop,
        'for next_lesson in g[now]': _next,
        'ind[next_lesson] -= 1': '学完 `{now}`，`{next_lesson}` 少一门先修课：`ind[{next_lesson}]` = {ind[next_lesson]}',
        'if ind[next_lesson] == 0': lambda S, B, ret: (f'`ind[{S.next_lesson}] = 0`：先修课全学完 → ==入队==' if S.ind[S.next_lesson] == 0
                                                       else f'`ind[{S.next_lesson}] = {S.ind[S.next_lesson]}`：还有先修课没学，暂不入队'),
        'q.append(next_lesson)': '`{next_lesson}` 入队，排在课程顺序的末尾',
        'if len(q) == numCourses': lambda S, B, ret: (f'`len(q) = {len(S.q)} == {S.numCourses}`：所有课都排进去了，没有环' if len(S.q) == S.numCourses
                                                      else f'`len(q) = {len(S.q)} < {S.numCourses}`：有环，有课永远学不了'),
        'return q': '==BFS 的队列就是一种可行的课程顺序==：返回 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='做一次 BFS 拓扑排序，队列本身就是课程顺序',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['共 `numCourses` 门课，`[a, b]` 表示学 `a` 之前必须先学 `b`',
                 '返回一种==能学完所有课==的顺序；不可能学完则返回空数组',
                 '示例：`4, [[1,0],[2,0],[3,1],[3,2]]` → `[0,1,2,3]` 或 `[0,2,1,3]`',
                 '本视频：`5, [[1,0],[2,1],[2,3],[4,2]]` → `[0,3,1,2,4]`'],
        quote='虽然是升级版，但是也只是要输出具体的课程顺序，实际上在使用bfs实现拓扑排序的过程中，==bfs的队列就是一种可行的课程顺序==。于是执行一次拓扑排序，输出bfs的队列即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['207 题的升级版：建图 + 统计入度，入度为 0 的课先入队',
              '出队一门课 = 学完它，后继课程入度减一，减到 0 就入队',
              '入队顺序满足先修关系 → 直接返回队列 `q`'],
        result='课程顺序 `[0,3,1,2,4]` ✓（每门课都排在它的先修课之后）',
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '`len(q) < numCourses` 说明有环：环上的课入度永远减不到 0',
                 '用 `l`、`r` 两个下标把数组当队列，出队的元素还留着，正好当答案',
                 '原文为 Python 2 风格，只删去了文档字符串；`numCourses == 0` 时返回 `0` 是原文写法（题目保证 ≥ 1，不会触发）'],
    ),
)
