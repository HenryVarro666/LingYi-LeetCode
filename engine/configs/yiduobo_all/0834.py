import math as _m


def _tgraph(cv, T, box, pos, edges, ncol, nsub, ecol, title, R=30, bottom=62, side=None):
    """通用树/图：pos 为 0..1 的相对坐标；nsub 返回 str 或 [str]（画在节点下方）"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 80, x1 - 80, y0 + 52 + R + (50 if 'a' in (side or {}).values() else 0), y1 - R - bottom
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v in edges:
        c, wd = ecol(u, v)
        cv.line([P[u], P[v]], c, wd)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is None:
            continue
        sd = (side or {}).get(u, 'b')
        for k, line in enumerate([s] if isinstance(s, str) else s):
            if sd == 'b':
                cv.text((px, py + R + 4 + k * 23), line, 20, T['yellow'], anchor='mt', bold=True, mono=True)
            elif sd == 'a':
                cv.text((px, py - R - 4 - (len(s) - 1 - k) * 23 if not isinstance(s, str) else py - R - 4), line, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            elif sd == 'r':
                cv.text((px + R + 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='lm', bold=True, mono=True)
            else:
                cv.text((px - R - 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='rm', bold=True, mono=True)
N = 6
EDGES = [(0, 1), (0, 2), (2, 3), (2, 4), (2, 5)]
SIDE = {0: 'a', 2: 'r'}
POS = {0: (0.5, 0.0), 1: (0.2, 0.45), 2: (0.7, 0.45), 3: (0.42, 1.0), 4: (0.7, 1.0), 5: (0.98, 1.0)}


def _phase(S):
    inn = S['_inner']
    if 'dis' in inn:
        return 'dfs'
    if 'order' in inn and 'now' in inn:
        return 'loop'
    return None


def _draw(cv, S, B, box, T):
    ph = _phase(S)
    inn = S['_inner']
    sons, res, used, fa = S.get('sons'), S.get('res'), S.get('used'), S.get('fa')
    now = inn.get('now') if ph else None
    nxt = inn.get('next') if ph == 'dfs' else None

    def ncol(u):
        if ph is None:
            return T['panel2']
        if u == now:
            return T['blue']
        if ph == 'dfs' and u == nxt and used[u]:
            return T['yellow']
        if ph == 'loop' and res[u] != 0:
            return T['green']
        if ph == 'dfs' and used[u]:
            return T['cyan']
        return T['panel2']

    def nsub(u):
        if sons is None:
            return None
        s = [f'p={sons[u]}']
        if res[u] != 0:
            s.append(f'res={res[u]}')
        return s

    def ecol(u, v):
        if ph == 'loop' and now is not None and now != 0 and {u, v} == {now, fa[now]}:
            return T['yellow'], 6
        if ph == 'dfs' and nxt is not None and used[nxt] and {u, v} == {now, nxt}:
            return T['yellow'], 6
        return T['border'], 3

    _tgraph(cv, T, box, POS, EDGES, ncol, nsub, ecol, side=SIDE,
            title='树（蓝 = now，黄 = 刚走到的孩子，青 = dfs 已访问，绿 = res 已确定）')


def _txt(S):
    ph = _phase(S)
    inn = S['_inner']
    sons, res = S.get('sons'), S.get('res')
    if ph == 'dfs':
        now = inn['now']
        return f"`p = sons[{now}] = {sons[now]}`：{now} 的子树里除自己外的点数"
    if ph == 'loop':
        now = inn['now']
        f = S['fa'][now]
        if res[now] != 0:
            return f"`res[{now}] = res[{f}] + {S['N']} − 2 − 2×{sons[now]} = {res[f]} + {S['N'] - 2 - 2 * sons[now]}` = =={res[now]}=="
        return f'按 dfs 序处理节点 `{now}`：父亲 `{f}` 的结果一定已算好'
    return '先 dfs 求 `res[0]` 和各子树大小 `sons`，再按 dfs 序传给孩子'


CONFIG = dict(
    num=834, title='树中距离之和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='dfs + 按 dfs 序递推',
    tags=['灵神题单·动态规划', '难度分 2197'],
    code='''
class Solution(object):
    def sumOfDistancesInTree(self, N, edges):

        tree = {x : set() for x in range(N)}
        for x, y in edges:
            tree[x].add(y)
            tree[y].add(x)
        used = [False] * N
        sons = [0] * N
        fa = [0] * N
        used[0] = True
        order = []
        res = [0] * N
        res[0] = self.dfs(0, 0, order, used, sons, fa, tree)
        for now in order:
            res[now] = res[fa[now]] + N - 2 - sons[now] * 2
        return res

    def dfs(self, now, dis, order, used, sons, fa, tree):
        tmp = 0
        for next in tree[now]:
            if not used[next]:
                used[next] = True
                order.append(next)
                fa[next] = now
                tmp += self.dfs(next, dis + 1, order, used, sons, fa, tree)
                sons[now] += sons[next] + 1
        
        return sons[now] + tmp
''',
    call='Solution().sumOfDistancesInTree(6, [[0,1],[0,2],[2,3],[2,4],[2,5]])',
    expect=[8, 12, 6, 10, 10, 10],
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='calls', h=170, hide=('order', 'used', 'sons', 'fa', 'tree')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('sons', 'sons', 'yellow'),
           ('order', 'order', 'cyan'), ('res', 'res', 'green')],
    skip=['tree[x].add(y)', 'tree[y].add(x)', 'for x, y in edges', 'for next in tree[now]', 'if not used[next]', 'used[next] = True', 'fa[next] = now'],
    max_steps=80,
    captions={
        'tree = {': '先建邻接表：`tree[x]` 是 x 的邻居集合',
        'used = [False]': '`used` 标记已访问的点，避免走回头路',
        'sons = [0]': '`sons[i]`：以 i 为根的子树里，除了 i 自己的点数',
        'fa = [0]': '`fa[i]` 记录 i 的父亲，第二步要用',
        'order = []': '`order` 记录 dfs 访问顺序：保证处理孩子时父亲已算好',
        'res = [0]': '`res[i]` 是节点 i 到所有点的距离之和',
        'res[0] = self.dfs': '第一步：以 0 为根 dfs，一路记下 `sons`、`fa` 和 dfs 序，返回 0 到所有点的距离和',
        'for now in order': lambda S, B, r: ('每个点都推完了 → 结束循环' if B.get('now') == S.get('now') and S.res[S.now] != 0
                                             else f'第二步：按 dfs 序处理 `{S.now}`（`res[0] = {S.res[0]}` 已经有了）'),
        'res[now] = res[fa[now]]': ('`res[{now}] = res[{fa[now]}] + {N} − 2 − 2×{sons[now]}`：子树里 `{sons[now] + 1}` 个点近 1，'
                                    '其余 `{N - sons[now] - 1}` 个点远 1 → =={res[now]}=='),
        'tmp = 0': lambda S, B, r: f"进入节点 `{S['_inner']['now']}`：`tmp` 用来累加孩子子树的距离和",
        'order.append': '`{next}` 是 `{now}` 没访问过的孩子：标记访问、记入 dfs 序 `order = {order}`',
        'tmp += self.dfs': '往下走到孩子 `{next}`（`{now}` 记为它的父亲），距离 `{dis + 1}`',
        'sons[now] += sons[next] + 1': '孩子 `{next}` 回来了：`tmp = {tmp}`；`{now}` 的子树多了它：`sons[{now}] = {sons[now]}`',
        'return sons[now] + tmp': ('`{now}` 到子树内所有点的距离和 = 孩子们的 `{tmp}` + 每个点多走一步 `sons = {sons[now]}` = =={ret}=='),
        'return res': '每个点的答案都算出来了：`{res}`',
    },
    cards=dict(
        one_liner='先 dfs 求根的答案，再按 dfs 序用父亲的结果推孩子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树有 `N` 个点，求每个点到其他所有点的距离之和',
                 '示例：`N=6, edges=[[0,1],[0,2],[2,3],[2,4],[2,5]]`',
                 '→ `[8,12,6,10,10,10]`'],
        quote='平方的做法是很容易想到的，枚举每个节点，将树的结构调整成以该节点为根的树，然后进行一趟dfs即可求出该节点到其他节点的距离之和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`disNow = dis0 + dis1 + ... + disK + pNow`：孩子的距离和，加上子树每个点多走的一步',
              '父子换根：f2 = f0 + N − 2 − 2×p2，子树里的 p2 个点变近，其余变远',
              '做法：一次 dfs 记下 dfs 序和 `sons`，再按序递推'],
        summary=['时间 `O(n)`，空间 `O(n)`；暴力枚举根是 `O(n^2)`',
                 '`sons[x]` 不含 x 自己，所以公式里是 `N - 2 - 2*sons[x]`',
                 '必须按 dfs 序处理：算 `res[now]` 时 `res[fa[now]]` 已经有值',
                 '对比灵神：他用 size（含自己）和递归 reroot；这里用 sons + dfs 序循环，等价且不再递归',
                 '原文本身可直接在 Python 3 运行，未改动'],
    ),
)
