POS = {3: (0.06, 0.50), 1: (0.40, 0.10), 2: (0.40, 0.90), 0: (0.74, 0.50)}


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
    W, H, R = (x1 - x0) * 0.5, (y1 - y0) - 70, 28

    def P(u):
        fx, fy = POS[u]
        return x0 + 70 + fx * W, y0 + 34 + fy * H

    done = set(q[:max(0, l - 1)])  # 早于 now 出队的点
    for u, vs in g.items():
        for v in vs:
            (ax, ay), (bx, by) = P(u), P(v)
            dx, dy = bx - ax, by - ay
            L = max(1.0, (dx * dx + dy * dy) ** 0.5)
            ux, uy = dx / L, dy / L
            hot = (u, v) == (now, nxt)
            c = T['yellow'] if hot else (T['dim'] if u in done else T['muted'])
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)), c, 5 if hot else 3, 14)
    for u in g:
        X, Y = P(u)
        if u in q[:l]:
            f = T['green']
        elif u in q:
            f = T['blue']
        else:
            f = None
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=f or T['panel2'],
                     outline=T['text'] if u == now else T['border'], width=4 if u == now else 2)
        cv.text((X, Y), u, 28, T['bg'] if f else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + R + 6), f'入度 {ind[u]}', 19, T['yellow'] if u == nxt else T['muted'], anchor='mt', bold=u == nxt)
    lx = x0 + 70 + W + 100
    for k, (name, f) in enumerate([('入度 > 0，还不能入队', None), ('入度 0，在队列中', 'blue'), ('已出队', 'green')]):
        yy = y0 + 40 + k * 46
        cv.d.ellipse((lx, yy, lx + 26, yy + 26), fill=T[f] if f else T['panel2'], outline=T['border'])
        cv.text((lx + 38, yy + 13), name, 21, T['muted'], anchor='lm')
    cv.text((lx, y0 + 40 + 3 * 46 + 6), '箭头 u → v：表示 g[u] 里有 v', 19, T['dim'], anchor='la')


def _edge(S, B, ret):
    if 'now' in B and (B.pre_lesson, B.now) == (S.pre_lesson, S.now):
        return '建图完成'
    note = '（`pre_lesson` 取到的其实是要学的课 a，边方向与文字相反，不影响判环）' if 'now' not in B else ''
    return f'`[{S.pre_lesson}, {S.now}]`：建边 `{S.pre_lesson} → {S.now}`，`{S.now}` 的入度 +1' + note


_state = {'first': False}  # 刚出队一个点 → 下一次 for 一定是第一条出边


def _pop(S, B, ret):
    _state['first'] = True
    return f'`l` → {S.l}，`{S.now}` 出队'


def _next(S, B, ret):
    first, _state['first'] = _state['first'], False
    if not S.g[S.now]:
        return f'`{S.now}` 没有出边'
    if first or B.next_lesson != S.next_lesson:
        return f'沿着边 `{S.now} → {S.next_lesson}` 走'
    return f'`{S.now}` 的出边处理完了'


CONFIG = dict(
    num=207, title='课程表', difficulty='Medium', category='图论',
    author='yiduobo', technique='拓扑排序 · BFS（Kahn 算法）',
    code='''
class Solution(object):
    def canFinish(self, numCourses, prerequisites):
        g = {index : [] for index in range(numCourses)}
        ind = [0] * numCourses

        for pre_lesson, now in prerequisites:
            ind[now] += 1
            g[pre_lesson].append(now)

        q = [index for index, x in enumerate(ind) if x == 0]
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

        return r == numCourses
''',
    call='Solution().canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]])',
    expect=True,
    views=[
        dict(type='custom', draw=draw_graph, h=300),
        dict(type='array', var='ind', label='ind（入度）', cell=76,
             color=lambda S, i, v: 'yellow' if i == S.get('next_lesson') and 'l' in S else None),
        dict(type='array', var='q', label='q（BFS 队列 = 拓扑序；灰 = 已出队）', cell=76, min_slots=4,
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S['l']),
    ],
    watch=[('now', 'now'), ('next_lesson', 'next_lesson', 'yellow'), 'l', 'r'],
    captions={
        'ind = [0]': '`g` 是邻接表（每门课一个列表）；`ind` 记入度 = 有多少条边指向这门课',
        'for pre_lesson, now in prerequisites': _edge,
        'ind[now] += 1': '`ind[{now}]` = {ind[now]}',
        'g[pre_lesson].append(now)': '`g[{pre_lesson}]` 加入 `{now}`',
        'l = 0': '入度为 0 的点 `{q}`（没有边指向它）先入队；`l` 指向队头',
        'r = len(q)': '`r = {r}`：已入队的个数（队尾）',
        'while l < r': lambda S, B, ret: (f'`l < r`（`{B.l} < {B.r}`）→ 队列非空，继续 BFS' if B.l < B.r
                                          else f'`l == r == {B.r}`：队列空了，BFS 结束'),
        'now = q[l]': '取出队头 `now = {now}`：指向它的边都已删完',
        'l += 1': _pop,
        'for next_lesson in g[now]': _next,
        'ind[next_lesson] -= 1': '删掉这条边：`ind[{next_lesson}]` 减一 → {ind[next_lesson]}',
        'if ind[next_lesson] == 0': lambda S, B, ret: (f'`ind[{S.next_lesson}] == 0`：指向它的边都删完了 → ==入队=='
                                                      if S.ind[S.next_lesson] == 0
                                                      else f'`ind[{S.next_lesson}]` 还是 {S.ind[S.next_lesson]}，还不能入队'),
        'q.append(next_lesson)': '`{next_lesson}` 加入队尾',
        'r += 1': '`r` → {r}',
        'return r == numCourses': lambda S, B, ret: (f'`r == numCourses`（`{S.r} == {S.numCourses}`）→ ==所有点都进过队列==，返回 `{ret}`'
                                                     if ret else f'`r = {S.r} < {S.numCourses}`：有点永远入不了队（在环上）→ 返回 `False`'),
    },
    skip=['g = {index', 'q = [index'],
    max_steps=70,
    cards=dict(
        one_liner='入度为 0 的课先学，学完删边；能把所有课都 BFS 一遍就没有环',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`[a, b]` 表示学 `a` 之前必须先学 `b`，判断能否学完所有课程',
                 '等价于：课程依赖构成的有向图==有没有环==',
                 '本视频示例：4 门课，`[[1,0],[2,0],[3,1],[3,2]]` → ==True=='],
        quote='将所有入度为0，即不需要前置课程的点加入到队列中，开始进行bfs……若某个点的入度减到了0，说明这门课程的前置课程已经被遍历完，可以开始学习了。',
        quote_src='—— yiduobo 题解',
        idea=['图论中的==拓扑排序==：入度 = 有多少条边指向这个点',
              '每出队一个点，就把它的出边“删掉”（终点入度减一），减到 0 就入队',
              '若可以 BFS 完整个图（`r == numCourses`），就能学完；环上的点入度永远减不到 0'],
        summary=['时间 `O(n+m)`：每个点入队一次，每条边删一次',
                 '队列用列表 + `l`、`r` 两个下标实现，`r` 恰好就是入过队的点数',
                 '细节：代码里 `pre_lesson` 其实是 `a`，建的是 `a → b`，和文字描述的方向相反',
                 '方向反过来不影响判环：反图有环 ⇔ 原图有环',
                 '原文为 Python 2 风格，删去了 `"""type"""` 文档字符串'],
    ),
)
