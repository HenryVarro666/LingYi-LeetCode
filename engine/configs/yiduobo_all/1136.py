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
    def minimumSemesters(self, n, relations):

        ind = [0] * n
        g = {}

        for x, y in relations:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = set()
            
            g[x].add(y)
            ind[y] += 1
        
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
        
        head, tail = 0, len(q)
        res = 0
        while head < tail:
            res += 1
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
            
            head, tail = tail, len(q)
        
        if len(q) == n:
            return res
        
        return -1
'''
LN = _mk(CODE)
POS = {'1': (0, .5), '2': (.3, 0), '3': (.3, 1), '4': (.65, .5), '5': (1, .5)}
EDGES = [(str(a), str(b)) for a, b in [[1, 2], [1, 3], [2, 4], [3, 4], [4, 5]]]


def _draw(cv, S, B, box, T):
    q, ind, head, tail = S.get('q'), S.get('ind'), S.get('head'), S.get('tail')
    st, sub, hot = {}, {}, None
    if ind is not None and len(ind) == 5:
        for i in range(5):
            sub[str(i + 1)] = f'入度 {ind[i]}'
    if q is not None and head is not None and tail is not None and ind is not None and len(ind) == 5:
        line, now = S['_line'], S.get('now')
        for i in range(5):
            k = str(i + 1)
            if i in q[:head]:
                st[k] = 'green'
            elif i in q[head:tail]:
                st[k] = 'yellow'
            elif i in q[tail:]:
                st[k] = 'cyan'
        if now is not None and LN('for now in') < line < LN('head, tail = tail'):
            st[str(now + 1)] = 'orange'
            nx = S.get('next')
            if nx is not None and line >= LN('ind[next] -= 1') and nx in (S.get('g') or {}).get(now, ()):
                hot = (str(now + 1), str(nx + 1))
    _gdraw(cv, box, T, POS, EDGES, st, sub, hot, '节点 = 课号 · 黄 本学期 · 橙 正在处理 · 青 下学期 · 绿 已学完', R=32)


CONFIG = dict(
    num=1136, title='并行课程', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='拓扑排序 · 分层 BFS 数轮次',
    tags=[],
    code=CODE,
    call='Solution().minimumSemesters(5, [[1,2],[1,3],[2,4],[3,4],[4,5]])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var='q', label='q（黄框 = 本学期要学的 q[head:tail]）', window=('head', 'tail - 1'), h=170),
        dict(type='text', fn=lambda S: ('`ind` = 还没学完的前置课数：' + '  '.join(f'课{i+1}:{v}' for i, v in enumerate(S['ind']))) if 'ind' in S else '', h=60),
    ],
    watch=[('res', 'res', 'green'), ('head', 'head', 'blue'), ('tail', 'tail', 'cyan')],
    skip=['for now in', 'for next in', 'x -= 1', 'y -= 1', 'ind = [0] * n', 'g = {}'],
    max_steps=90,
    captions={
        'if x not in g': lambda S, B, r: (f'课 `{S.x+1}` 还没有后置课集合：先建一个' if S.x not in S.g else f'课 `{S.x+1}` 已有后置课集合，直接加边'),
        'g[x].add(y)': '建边 `{x+1} → {y+1}`：先修课指向后修课',
        'ind[y] += 1': '课 `{y+1}` 多一门前置课：`ind[{y}] = {ind[y]}`',
        'if ind[index] == 0': lambda S, B, r: (f'课 `{S.index+1}` 没有前置课 → 第一学期就能上' if S.ind[S.index] == 0
                                               else f'课 `{S.index+1}` 有 `{S.ind[S.index]}` 门前置课，先不入队'),
        'q.append(index)': '课 `{index+1}` 入度为 0：入队，作为第一批',
        'head, tail = 0, len(q)': '`q[head:tail]` 就是「这一轮」要处理的课：`{q[head:tail]}`',
        'res = 0': '`res` 记学期数：一轮 = 一学期',
        'while head < tail': lambda S, B, r: (f'这一批有 `{S.tail - S.head}` 门课，开始新一轮' if S.head < S.tail else '没有新课可上了 → 结束循环'),
        'res += 1': '新的一学期：`res = {res}`，本学期上 `q[{head}:{tail}]` = `{q[head:tail]}`',
        'ind[next] -= 1': '课 {now+1} 上完 → 它的后置课 {next+1} 少一门前置课：`ind[{next}] = {ind[next]}`',
        'if ind[next] == 0': lambda S, B, r: (f'`ind[{S.next}] = 0`：前置课全上完 → 下学期可上，入队' if S.ind[S.next] == 0
                                              else f'`ind[{S.next}] = {S.ind[S.next]}`：还有前置课没上完，先等'),
        'q.append(next)': '课 `{next+1}` 入队，排在下一批',
        'head, tail = tail': '一批处理完：新的一批是 `q[{head}:{tail}]` = `{q[head:tail]}`',
        'if len(q) == n': lambda S, B, r: (f'`len(q) = {len(S.q)}` 等于 `n = {S.n}`：所有课都入过队 → 无环' if len(S.q) == S.n
                                           else f'`len(q) = {len(S.q)}` < `n`：有课永远入不了队 → 有环'),
        'return res': '一共 `{res}` 轮 = 最少 =={res}== 个学期',
    },
    cards=dict(
        one_liner='拓扑排序一层一层剥，剥了几层就是几个学期',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 门课，`relations[i]=[a,b]` 表示课 `a` 是课 `b` 的先修课',
                 '每学期可以上任意多门「前置课都已学完」的课，求最少学期数',
                 '有环学不完则返回 `-1`。示例：5 门课 → `4`'],
        quote='若某一课程的入度被减到0时，说明该课程的所有前置课程已经学习完毕，那么就可以将该课程加入到拓扑排序的队列中。',
        quote_src='—— yiduobo 题解原文',
        idea=['建图并统计入度，入度为 0 的课先入队（第一学期）',
              '`q[head:tail]` 圈出一层：这一层的课同一学期上，`res += 1`',
              '上完就给后置课入度减 1，减到 0 的进入下一层；队列长度不等于 `n` 说明有环'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '一层一层处理（`head`、`tail` 圈出一批），所以轮次 = 学期数',
                 '`len(q) == n` 才无环；否则返回 `-1`',
                 '课号从 1 开始，建图先 `x -= 1`、`y -= 1`',
                 '原文已是 Python 3 可运行写法，代码未改动；本视频用无环示例；有环时 `len(q) == n` 不成立，返回 `-1`'],
    ),
)
