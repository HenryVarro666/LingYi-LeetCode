import math as _m


def _gdraw(cv, box, T, pos, edges, state, sub=None, hot=None, title='', R=30, fs=26):
    """有向图：pos={名字:(fx,fy)}，edges=[(a,b)]，state={名字:颜色名或None}，sub={名字:下方小字}，hot=高亮边 (a,b)"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    half = {k: max(R, (cv.tlen(k, fs, bold=True) + 30) / 2) for k in pos}
    mx = max(half.values())
    w, h = x1 - x0 - 2 * mx - 40, y1 - y0 - 2 * R - 100
    P = {k: (x0 + 20 + mx + fx * w, y0 + 50 + R + fy * h) for k, (fx, fy) in pos.items()}

    def edge_pt(k, ux, uy, pad):
        a, b = half[k] + pad, R + pad
        t = 1 / _m.sqrt((ux / a) ** 2 + (uy / b) ** 2)
        return t

    for a, b in edges:
        if a not in P or b not in P:
            continue
        (ax, ay), (bx, by) = P[a], P[b]
        d = _m.hypot(bx - ax, by - ay) or 1
        ux, uy = (bx - ax) / d, (by - ay) / d
        ta, tb = edge_pt(a, ux, uy, 3), edge_pt(b, ux, uy, 6)
        on = hot is not None and (a, b) == tuple(hot)
        cv.arrow((ax + ux * ta, ay + uy * ta), (bx - ux * tb, by - uy * tb),
                 T['yellow'] if on else T['dim'], width=6 if on else 3, head=16 if on else 13)
    for k, (cx, cy) in P.items():
        c = state.get(k)
        fill = T[c] if c else T['panel2']
        cv.rect((cx - half[k], cy - R, cx + half[k], cy + R), fill=fill, outline=T['border'], width=3, r=R)
        cv.text((cx, cy), k, fs, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if sub and sub.get(k) not in (None, ''):
            cv.text((cx, cy + R + 6), sub[k], 22, T['muted'], anchor='mt', bold=True)


def _mk(CODE):
    lines = CODE.strip('\n').split('\n')
    return lambda s: next(i + 1 for i, l in enumerate(lines) if s in l)

CODE = '''
class Solution(object):
    def minimumTime(self, n, relations, time):

        ind = [0] * n
        g = {}
        for x, y in relations:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = set()
            g[x].add(y)
            ind[y] += 1
        
        f = {}
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
                f[index] = time[index]
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                if next not in f:
                    f[next] = f[now]
                else:
                    f[next] = max(f[next], f[now])

                ind[next] -= 1
                if ind[next] == 0:
                    f[next] += time[next]
                    q.append(next)
                    r += 1
        
        return max(f.values())
'''
LN = _mk(CODE)
POS = {'1': (0, 0), '2': (0, .5), '3': (0, 1), '4': (.5, 1), '5': (1, .5)}
TIME = [1, 2, 3, 4, 5]
EDGES = [(str(a), str(b)) for a, b in [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]]]


def _draw(cv, S, B, box, T):
    q, f, ind, l = S.get('q'), S.get('f'), S.get('ind'), S.get('l', 0)
    st, sub, hot = {}, {}, None
    for k in POS:
        sub[k] = f't={TIME[int(k) - 1]}'
    if q is not None and f is not None and ind is not None and l is not None and len(ind) == 5:
        line, now = S['_line'], S.get('now')
        cur = now if (now is not None and LN('now = q[l]') <= line <= LN('r += 1')) else None
        for i in range(5):
            k = str(i + 1)
            if i in q[:l]:
                st[k] = 'green'
            if i in q[l:]:
                st[k] = 'cyan'
            if i in f:
                sub[k] = f't={TIME[i]} f={f[i]}'
        if cur is not None:
            st[str(cur + 1)] = 'yellow'
            nx = S.get('next')
            if nx is not None and line >= LN('if next not in f'):
                hot = (str(cur + 1), str(nx + 1))
    _gdraw(cv, box, T, POS, EDGES, st, sub, hot, '节点 = 课号 · t = 耗时 · 青 待处理 · 黄 当前 now · 绿 已处理', R=32)


CONFIG = dict(
    num=2050, title='并行课程 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='拓扑排序 · 入度归零时定型',
    tags=['图论算法', '难度分 2084'],
    code=CODE,
    call='Solution().minimumTime(5, [[1,5],[2,5],[3,5],[3,4],[4,5]], [1,2,3,4,5])',
    expect=12,
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='array', var='q', label='q（拓扑队列，蓝箭头 = l 指向的 now）', pointers={'l': 'blue'}, h=170),
        dict(type='map', var='f', label='f（课号−1 → 完成时间）', h=120),
        dict(type='text', fn=lambda S: ('`ind` 还剩前置课数（课 1~5）：' + '  '.join(f'==课{i+1}:{v}==' if v == 0 else f'课{i+1}:{v}' for i, v in enumerate(S['ind']))) if 'ind' in S else '', h=60),
    ],
    max_steps=85,
    watch=[('now', 'now', 'yellow'), ('next', "next if isinstance(next, int) else '-'", 'pink'), ('l', 'l', 'blue'), ('r', 'r', 'cyan')],
    skip=['x -= 1', 'y -= 1', 'ind = [0] * n', 'g = {}'],
    captions={
        'if x not in g': lambda S, B, r: (f'课 `{S.x+1}` 还没有后继课集合：先建一个' if S.x not in S.g else f'课 `{S.x+1}` 已经有后继集合了，直接加边'),
        'g[x].add(y)': '建边 `{x+1} → {y+1}`：前置课指向后置课',
        'ind[y] += 1': '课 `{y+1}` 多一门前置课：`ind[{y}] = {ind[y]}`',
        'if ind[index] == 0': lambda S, B, r: (f'课 `{S.index+1}` 没有前置课 → 可以直接开学' if S.ind[S.index] == 0
                                               else f'课 `{S.index+1}` 还有 `{S.ind[S.index]}` 门前置课，先不入队'),
        'f[index] = time[index]': '没有前置课：完成时间就是自己的耗时 `f[{index}] = {f[index]}`',
        'l = 0': '`l`、`r` 框出这一批队列：`q[l:r]` 是还没处理的课',
        'while l < r': lambda S, B, rr: (f'队列还有 `{S.r - S.l}` 门课，继续' if S.l < S.r else '队列处理完了 → 结束'),
        'now = q[l]': '取出 `now = {now}`（课 {now+1}）：它的 `f[now]` 已是最终完成时间 `{f[now]}`',
        'l += 1': '`l` 右移，`now` 出队',
        'if next not in f': lambda S, B, r: (f'后继课 `{S.next+1}` 还没有 f → 直接继承 `f[{S.now}]`' if S.next not in B.f
                                             else f'后继课 `{S.next+1}` 已有 f = `{S.f[S.next]}`，要和 `f[{S.now}]` 比大小'),
        'f[next] = f[now]': '`f[{next}] = f[{now}] = {f[next]}`：下一门课至少要等 `now` 学完',
        'f[next] = max': '`f[{next}] = max({B.f[next]}, {f[now]}) = {f[next]}`：等最晚学完的那门前置课',
        'ind[next] -= 1': '`now` 的影响处理完了：`ind[{next}] = {ind[next]}`',
        'if ind[next] == 0': lambda S, B, r: (f'`ind[{S.next}] = 0`：前置课都考虑过了，`f[{S.next}]` 里是开学时间' if S.ind[S.next] == 0
                                              else f'`ind[{S.next}] = {S.ind[S.next]}`：还有前置课没完成，先等'),
        'f[next] += time[next]': '开学时间加上耗时：`f[{next}] = {B.f[next]} + {time[next]}` = =={f[next]}==',
        'q.append(next)': '课 `{next+1}` 入队，轮到它去更新后继',
        'r += 1': '`r` 右移，队尾多一个',
        'return max': '`f` 里最大的就是总时长：=={ret}==',
    },
    cards=dict(
        one_liner='f[now] 表示完成 now 的最早时间，拓扑序上不断刷新后继',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 门课，`relations` 给出「前置课 → 后置课」，可同时学任意多门',
                 '`time[i]` 是第 `i+1` 门课的月数，求学完全部课的最少月数',
                 '示例：`time=[1,2,3,4,5]`，5 条边 → `12`'],
        quote='对于每个next，首先使用f[next] = max(f[next], f[now])来更新f[next]，表示在开始学习next之前必须先等待now完成学习。',
        quote_src='—— yiduobo 题解原文',
        idea=['建图：前置课指向后置课，`ind` 统计前置课数量',
              '入度 0 的课 `f` 就是自己的耗时，先入队',
              '遍历 `now` 的后置课：`f[next]` 取最大，`ind` 减一；==减到 0 才加上 `time[next]`==，再入队'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '`f[next] += time[next]` 只在入度归零时做一次：此时 `f[next]` 是所有前置课完成时间的最大值',
                 '课号从 1 开始，建图时先 `x -= 1`、`y -= 1`',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神出队时才加 `time[x]`；yiduobo 在入队前就加好，出队即是最终值'],
    ),
)
