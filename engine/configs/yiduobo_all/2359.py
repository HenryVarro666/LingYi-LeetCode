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
    def closestMeetingNode(self, edges, node1, node2):

        dis1 = {node1: 0}
        used = set([-1, node1])
        now = node1
        step = 0
        while edges[now] not in used:
            now = edges[now]
            step += 1
            dis1[now] = step
            used.add(now)
        
        dis2 = {node2: 0}
        used = set([-1, node2])
        now = node2
        step = 0
        while edges[now] not in used:
            now = edges[now]
            step += 1
            dis2[now] = step
            used.add(now)
        
        res = -1
        min_dis = None
        for node in dis1:
            if node in dis2:
                d = max(dis1[node], dis2[node])
                if min_dis is None or min_dis > d:
                    min_dis = d
                    res = node
        
        return res
'''
LN = _mk(CODE)
EDGE_LIST = [1, 2, 3, 1, 3]
NM = [str(i) for i in range(5)]
POS = {'0': (0, .5), '1': (.33, .5), '2': (.66, .02), '3': (.66, .98), '4': (1, .98)}
EDGES = [(NM[i], NM[e]) for i, e in enumerate(EDGE_LIST)]


def _draw(cv, S, B, box, T):
    d1, d2 = S.get('dis1', {}), S.get('dis2', {})
    st, sub = {}, {}
    line = S.get('_line', 0)
    for i in range(5):
        a, b = i in d1, i in d2
        if a and b:
            st[NM[i]] = 'purple'
        elif a:
            st[NM[i]] = 'blue'
        elif b:
            st[NM[i]] = 'pink'
        if a or b:
            sub[NM[i]] = f"{d1.get(i, '-')}/{d2.get(i, '-')}"
    if 'node' in S and LN('for node in dis1') <= line < LN('return res'):
        st[NM[S['node']]] = 'yellow'
    elif 'now' in S and line < LN('res = -1'):
        st[NM[S['now']]] = 'yellow'
    if S.get('res', -1) >= 0:
        st[NM[S['res']]] = 'green'
    _gdraw(cv, box, T, POS, EDGES, st, sub, None, '蓝 node1 走过 · 粉 node2 走过 · 紫 都走过 · 下方 = dis1/dis2 · 绿 当前最优', R=34)


def _walk(S, B, r):
    e = S.edges[S.now]
    if e == -1:
        return f'下一步 `edges[{S.now}] = -1`：无路可走 → 停下'
    if e in S.used:
        return f'下一步 `edges[{S.now}] = {e}` 已经走过：成环了 → 停下'
    return f'下一步 `edges[{S.now}] = {e}` 没走过 → 继续往下走'


CONFIG = dict(
    num=2359, title='找到离给定两个节点最近的节点', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='两次沿出边走 · 哈希表记步数',
    tags=['难度分 1715'],
    code=CODE,
    call='Solution().closestMeetingNode([1,2,3,1,3], 0, 4)',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='map', var='dis1', label='dis1（node1 走到各点的步数）', h=120),
        dict(type='map', var='dis2', label='dis2（node2 走到各点的步数）', h=120),
    ],
    watch=[('now', 'now', 'yellow'), ('step', 'step', 'cyan'), ('res', 'res', 'green'), ('min_dis', 'min_dis', 'orange')],
    skip=['for node in dis1', 'now = node1', 'now = node2', 'step = 0'],
    max_steps=85,
    captions={
        'dis1 = {node1': '`dis1[点]` = 从 `node1` 走到这个点的步数，起点步数为 0',
        'dis2 = {node2': '`dis2[点]` = 从 `node2` 走到这个点的步数，起点步数为 0',
        'used = set': lambda S, B, r: ('`used` 记走过的点；先放进 `-1`，这样「无路可走」和「走回头」用同一个判断' if 'dis2' not in S
                                       else '清空 `used`，从 `node2` 重新走一遍'),
        'while edges[now] not in used': _walk,
        'now = edges[now]': '沿出边走到 `{now}`',
        'step += 1': '`step = {step}`',
        'dis1[now] = step': '`dis1[{now}] = {step}`：从 node1 走到 {now} 要 {step} 步',
        'dis2[now] = step': '`dis2[{now}] = {step}`：从 node2 走到 {now} 要 {step} 步',
        'used.add(now)': '`{now}` 记入 `used`，不会再走第二遍',
        'res = -1': '`res = -1`：还没找到都能到的点',
        'min_dis = None': '`min_dis` 记当前最小的「较大距离」，None 表示还没有',
        'if node in dis2': lambda S, B, r: (f'点 `{S.node}`：node2 也能走到 → 是候选' if S.node in S.dis2
                                            else f'点 `{S.node}`：node2 走不到 → 不是候选'),
        'd = max': '两人到 `{node}` 的距离 `{dis1[node]}`、`{dis2[node]}`，较大值 `d = {d}`',
        'if min_dis is None': lambda S, B, r: ('第一个候选，直接采用' if B.min_dis is None
                                               else (f'`min_dis = {S.min_dis}` > `d = {S.d}`：更近 → 更新' if S.min_dis > S.d
                                                     else f'`min_dis = {S.min_dis}` ≤ `d = {S.d}`：不更近（相等也不换，保留编号小的）')),
        'min_dis = d': '`min_dis = {min_dis}`',
        'res = node': '`res = {res}`：目前最好的会合点',
        'return res': '最近的会合点 =={ret}==',
    },
    cards=dict(
        one_liner='各走一遍记步数，再找两边都到过、较大值最小的点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每个节点至多一条出边，`edges[i]=-1` 表示没有出边，图里可能有环',
                 '求 `node1`、`node2` 都能到的点，使两边距离的较大值最小；并列取编号小的',
                 '示例：`edges=[1,2,3,1,3]`，`node1=0`，`node2=4` → `1`（含环 1→2→3→1）'],
        quote='由于每个节点只有一条出边，那么可以先从node1出发一直往下走，直到无法继续往下走，或者走回原来走到过的节点为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['出边唯一：从 `node1` 一路走下去，每个点最多访问一次，记下步数 `dis1`',
              '清空 `used`，同样从 `node2` 走一遍得到 `dis2`',
              '遍历 `dis1` 的点，在 `dis2` 里也有的就是候选，取 `max` 最小者'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`used` 初始放入 `-1`：`edges[now] == -1` 时一并停下',
                 '遍历 `dis1` 用严格 `>` 比较，距离相同保留先遇到的点；本例结果是编号 1',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神方法二让两人同时走、踩到脚印即停；yiduobo 分两次走完再枚举'],
    ),
)
