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
    def largestPathValue(self, colors, edges):

        n = len(colors)
        ind = [0] * n
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            ind[y] += 1
        
        f = {index : {} for index in range(n)}
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
                f[index][colors[index]] = 1

        l = 0
        r = len(q)
        res = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                for color in f[now]:
                    cnt = f[now][color]
                    f[next][color] = max(f[next].get(color, 0), cnt)

                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
                    f[next][colors[next]] = f[next].get(colors[next], 0) + 1
                    res = max(res, max(f[next].values()))
        
        if len(q) != n:
            return -1
        
        return res
'''
LN = _mk(CODE)
COLORS = 'abaca'
NM = [f'{i}:{c}' for i, c in enumerate(COLORS)]
POS = {NM[0]: (0, .5), NM[1]: (.42, 0), NM[2]: (.42, 1), NM[3]: (.72, 1), NM[4]: (1, 1)}
EDGES = [(NM[a], NM[b]) for a, b in [[0, 1], [0, 2], [2, 3], [3, 4]]]


def _fs(d):
    return ' '.join(f'{k}{v}' for k, v in sorted(d.items()) if v)


def _draw(cv, S, B, box, T):
    q, f, l = S.get('q'), S.get('f'), S.get('l', 0)
    st, sub, hot = {}, {}, None
    if q is not None and f is not None and len(f) == 5:
        line, now = S['_line'], S.get('now')
        cur = now if (now is not None and LN('now = q[l]') <= line <= LN('res = max(res')) else None
        for i in range(5):
            if i in q[:l]:
                st[NM[i]] = 'green'
            if i in q[l:]:
                st[NM[i]] = 'cyan'
            sub[NM[i]] = _fs(f[i])
        if cur is not None:
            st[NM[cur]] = 'yellow'
            nx = S.get('next')
            if nx is not None and line >= LN('for color in') and nx in S['g'][cur]:
                hot = (NM[cur], NM[nx])
    _gdraw(cv, box, T, POS, EDGES, st, sub, hot, '节点 = 编号:颜色 · 下方 = f[node]（颜色+次数）· 青 在队列 · 黄 now · 绿 已处理', R=36)


def _fx(S):
    f, now = S.get('f'), S.get('now')
    if f is None or now is None or len(f) != 5 or S['_line'] < LN('now = q[l]'):
        return ''
    return f'`f[{now}]` = ' + (('{' + ', '.join(f"'{k}': {v}" for k, v in sorted(f[now].items())) + '}') if f[now] else '{}')


CONFIG = dict(
    num=1857, title='有向图中最大颜色值', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='拓扑排序 + 路径终点 DP',
    tags=['图论算法', '难度分 2313'],
    code=CODE,
    call="Solution().largestPathValue('abaca', [[0,1],[0,2],[2,3],[3,4]])",
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var='q', label='q（拓扑队列，箭头 = 队首 l）', pointers={'l': 'blue'}, h=170),
        dict(type='text', fn=_fx, h=60),
    ],
    watch=[('now', "now if isinstance(now, int) else '-'", 'yellow'), ('next', "next if isinstance(next, int) else '-'", 'pink'),
           ('l', 'l', 'blue'), ('res', 'res', 'green')],
    skip=['ind = [0] * n', 'n = len(colors)', 'for next in g[now]', 'for color in f[now]', 'cnt = f[now][color]'],
    max_steps=80,
    captions={
        'g = {index': '每个点一个后继集合 `g[node]`',
        'g[x].add(y)': '建边 `{x} → {y}`',
        'ind[y] += 1': '`{y}` 的入度加一：`ind[{y}] = {ind[y]}`',
        'f = {index': '`f[node][color]`：路径以 `node` 为终点时，`color` 最多出现几次',
        'if ind[index] == 0': lambda S, B, r: (f'点 `{S.index}` 入度为 0，没有前置节点 → 先入队' if S.ind[S.index] == 0
                                               else f'点 `{S.index}` 还有前置节点，先跳过'),
        'q.append(index)': '点 `{index}` 作为拓扑排序的起点入队',
        'f[index][colors[index]] = 1': '起点只有自己：`f[{index}][{colors[index]!r}] = 1`',
        'l = 0': '`q[l:r]` 是待处理的点，`l` 是队首',
        'res = 1': '`res` 先设为 1：单个点的路径颜色值至少是 1',
        'while l < r': lambda S, B, rr: (f'队列里还有 `{S.r - S.l}` 个点' if S.l < S.r else '队列空了，拓扑排序结束'),
        'now = q[l]': '取队首 `now = {now}`（颜色 `{colors[now]}`）：`f[{now}]` 已经定型',
        'l += 1': '`l` 右移，`now` 出队',
        'f[next][color] = max': '`now` 的颜色 `{color}` 有 `{cnt}` 个 → 更新后继 `{next}`：`f[{next}][{color!r}] = {f[next][color]}`',
        'ind[next] -= 1': '`now` 的影响传完：`ind[{next}] = {ind[next]}`',
        'if ind[next] == 0': lambda S, B, r: (f'`ind[{S.next}] = 0`：所有前置节点都传完了 → 可以入队' if S.ind[S.next] == 0
                                              else f'`ind[{S.next}] = {S.ind[S.next]}`：还有前置节点没传完，先不入队'),
        'q.append(next)': '点 `{next}` 入队',
        'r += 1': '`r` 右移：队尾多一个',
        'f[next][colors[next]]': '`f[next]` 定型了，这时才加上 `next` 自己的颜色 `{colors[next]}`：`f[{next}][{colors[next]!r}] = {f[next][colors[next]]}`',
        'res = max(res': '`res = max({B.res}, max(f[{next}].values()))` = =={res}==',
        'if len(q) != n': lambda S, B, r: (f'`len(q) = {len(S.q)}` < `n`：有点没入过队 → 有环' if len(S.q) != S.n
                                           else f'`len(q) = {len(S.q)}` = `n`：所有点都入过队 → 无环'),
        'return res': '最大颜色值 =={res}==',
    },
    cards=dict(
        one_liner='f[node][color]：以 node 为终点的路径里 color 最多几个',
        complexity='时间 `O((n+m)·26)`，空间 `O(n·26)`',
        problem=['有向图，每个点有一种颜色，路径的颜色值 = 路径上出现最多的颜色的点数',
                 '求所有路径的最大颜色值；图里有环则返回 `-1`',
                 '示例：`colors="abaca"`，边 `0→1,0→2,2→3,3→4` → `3`'],
        quote='因为在next进入队列之前，f[next]是不会对其他节点产生任何影响的，因此可以将这个本身颜色的加1放到next即将加入队列，也就是f[next]已经被f[now]更新定型的时刻再执行。',
        quote_src='—— yiduobo 题解原文',
        idea=['令 `f[node][color]` = 以 `node` 为终点时 `color` 最多的个数',
              '`f[node][color] = max(f[prev][color])`，`node` 自己的颜色再加 1',
              '按拓扑序更新：`now` 的每个颜色去刷新 `next`，==`next` 入度归零（定型）时才加上自己的颜色=='],
        summary=['时间 `O((n+m)·26)`，空间 `O(n·26)`',
                 '入度为 0 的点要手动把自己的颜色设成 1',
                 '`res` 在入队时更新；队列长度 `!= n` 说明有环，返回 `-1`',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神出队时才给 `f[x]` 加自己的颜色；yiduobo 在入队前加，两者等价'],
    ),
)
