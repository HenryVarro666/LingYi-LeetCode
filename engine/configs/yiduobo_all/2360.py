import math


def _ln(code, sub):
    """1-based line number of the first code line containing sub (leading blank line stripped)"""
    for k, s in enumerate(code.strip('\n').split('\n')):
        if sub in s:
            return k + 1
    return -1


def _gdraw(cv, box, T, pos, E, node_fn, edge_fn, label_fn=None, title='', directed=True, R=30, base=0, node_w=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    w = x1 - x0 - 140
    h = y1 - y0 - 150
    P = [(x0 + 70 + fx * w, y0 + 60 + fy * h) for fx, fy in pos]
    es = set(E)
    for (a, b) in E:
        col, wd = edge_fn(a, b)
        (ax, ay), (bx, by) = P[a], P[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        off = 10 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        p0 = (ax + ux * R + nx, ay + uy * R + ny)
        p1 = (bx - ux * (R + 2) + nx, by - uy * (R + 2) + ny)
        if directed:
            cv.arrow(p0, p1, col, wd, head=16)
        else:
            cv.line([p0, p1], col, wd)
    for i, (x, y) in enumerate(P):
        fill, tc, ring = node_fn(i)
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, r=R, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((x, y), i + base, 26, tc, anchor='mm', bold=True)
        if label_fn:
            lab = label_fn(i)
            if lab:
                cv.text((x, y + R + 8), lab[0], 21, lab[1], anchor='mt', bold=True)


EDGES = [3, 3, 4, 2, 3, 6, 5, 8, -1]
POS = [(0.0, 0.1), (0.0, 0.85), (0.5, 0.1), (0.25, 0.48), (0.5, 0.85), (0.78, 0.1), (1.0, 0.1), (0.78, 0.85), (1.0, 0.85)]
CODE = '''
class Solution(object):
    def longestCycle(self, edges):

        n = len(edges)
        used = set()
        res = -1
        for index in range(n):
            if index not in used:
                now = index
                step = {}
                step[now] = 0
                while True:
                    next = edges[now]
                    if next == -1:
                        break

                    if next in step:
                        res = max(res, step[now] - step[next] + 1)
                        break
                    
                    if next in used:
                        break
                    
                    step[next] = step[now] + 1
                    now = next
                
                for num in step:
                    used.add(num)
        
        return res
'''
L_RES = _ln(CODE, 'res = max')


def _draw(cv, S, B, box, T):
    step = S.get('step') or {}
    used = S.get('used') or set()
    now = S.get('now')
    nxt = S.get('next')
    cyc = set()
    if S.get('_line') == L_RES and nxt in step:
        cyc = {k for k, v in step.items() if v >= step[nxt]}

    def node(i):
        if i in cyc:
            return T['green'], T['bg'], None
        ring = T['yellow'] if (now == i and S.get('_inner', {}).get('now') == i) else None
        if i in step:
            return T['blue'], T['bg'], ring
        if i in used:
            return (70, 76, 86), T['text'], ring
        return T['panel2'], T['muted'], ring

    def edge(a, b):
        if a in cyc and b in cyc:
            return T['green'], 5
        if a in step:
            return T['blue'], 4
        return T['dim'], 3

    def lab(i):
        if i in step:
            return (f'step={step[i]}', T['green'] if i in cyc else T['cyan'])
        return None
    E = [(i, e) for i, e in enumerate(EDGES) if e != -1]
    _gdraw(cv, box, T, POS, E, node, edge, lab, '黄圈 = now，蓝 = 本轮走过（step），灰 = 以前轮走过（used），绿 = 环')


CONFIG = dict(
    num=2360, title='图中的最长环', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='每轮单独记步数 + 全局 used',
    tags=['灵神题单·图论算法', '难度分 1897'],
    code=CODE,
    call=f'Solution().longestCycle({EDGES})',
    expect=3,
    skip=['n = len(edges)', 'step[now] = 0', 'while True', 'for num in step'],
    max_steps=90,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='edges', label='edges（-1 = 没有出边）', h=125, cell=66, pointers={'now': 'yellow'}),
        dict(type='map', var='step', label='step（本轮：点 → 第几步）', h=95, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='set', var='used', label='used（以前轮走过的点）', h=95),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'used = set()': '`used`：全局记录，以前轮次走过的点',
        'res = -1': '先假设没有环：`res = -1`',
        'for index in range': lambda S, B, r: ('所有起点都试过了' if S.index == B.get('index') and S.index == len(S.edges) - 1 and 'now' in S and S.index in S.used
                                              else f'枚举起点 `{S.index}`'),
        'if index not in used': lambda S, B, r: (f'起点 `{S.index}` 以前没走过 → 开一轮新的行走' if S.index not in S.used
                                                else f'起点 `{S.index}` 在 `used` 里：以前轮次走过它，环（若有）早已记录 → 跳过'),
        'now = index': '从 `{now}` 出发',
        'step = {}': '本轮另开一个记录 `step`，==不能用全局 used==：新环只能在本轮走过的点之间形成',
        'next = edges[now]': '下一个点 `next = {next}`',
        'if next == -1': lambda S, B, r: ('没有出边 → 走到死路，本轮结束' if S['next'] == -1 else '`next` 不是 -1，还能继续走'),
        'if next in step': lambda S, B, r: (f'`{S["next"]}` 在本轮 `step` 里 → 走回了本轮的点，==成环=='
                                            if S['next'] in S.step else f'`{S["next"]}` 本轮还没走过'),
        'res = max': '环长 = 步数差 + 1：`{step[now]} - {step[next]} + 1 = {step[now] - step[next] + 1}`，`res` → =={res}==',
        'if next in used': lambda S, B, r: (f'`{S["next"]}` 以前轮走过 → 它之后的路径已经走完，不会再回到本轮的点 → 不可能成环，结束本轮'
                                            if S['next'] in S.used else f'`{S["next"]}` 以前也没走过 → 继续往下走'),
        'step[next] = ': '记录 `{next}` 是本轮第 `{step[next]}` 步',
        'now = next': '走到 `{now}`',
        'used.add': '本轮走完，把走过的点并进全局 `used`：加入 `{num}`',
        'return res': '没有环时 `res` 仍是 -1；这里答案是 =={ret}==',
    },
    cards=dict(
        one_liner='每轮单独记步数：走回本轮的点，步数差 +1 就是环长',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有向图 `n` 个点，每个点==至多一条出边==，`edges[i]` 是 i 的终点，-1 表示没有',
                 '返回==最长的环==的长度，没有环返回 `-1`',
                 '示例：`[3,3,4,2,3]` → `3`。本视频的图多了两个连通块，答案同样是 3'],
        quote='新的环只可能是从本次行走路径上的某个节点出发，走回到本次行走路径上的某个节点',
        quote_src='—— yiduobo 题解原文',
        idea=['每个点只有一条出边：从每个点出发一直走，走到死路或走回走过的点',
              '本轮单独用 `step` 记步数；走回 `step` 里的点，==步数差 + 1== 就是环长',
              '一旦走到以前轮走过的点：后面的路径以前都走完了，本轮点不会在环上'],
        summary=['时间 `O(n)`：每个点只会被走一次，轮末合并进 `used`',
                 '环长是 `step[now] - step[next] + 1`，别漏了 +1',
                 '`step` 和 `used` 必须分开：混用就分不清“本轮”和“旧轮”',
                 '对比灵神：灵神用全局时间戳 `vis_time` 一个数组搞定，yiduobo 用本轮字典 + 全局集合'],
    ),
)
