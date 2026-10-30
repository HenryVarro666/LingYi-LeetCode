COINS = [0, 0, 0, 1, 1, 0, 0, 1]
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [5, 6], [5, 7]]
NN = len(COINS)
ADJ = [[] for _ in range(NN)]
for _x, _y in EDGES:
    ADJ[_x].append(_y)
    ADJ[_y].append(_x)
# 固定布局：以 0 为根按深度排列
DEPTH = {0: 0}
PAR = {0: -1}
_order = [0]
for _u in _order:
    for _v in ADJ[_u]:
        if _v not in DEPTH:
            DEPTH[_v] = DEPTH[_u] + 1
            PAR[_v] = _u
            _order.append(_v)
LEVELS = {}
for _u in _order:
    LEVELS.setdefault(DEPTH[_u], []).append(_u)
KIDS = {u: [v for v in ADJ[u] if PAR.get(v) == u] for u in range(NN)}
XS = {}
_slot = [0]


def _lay(u):
    if not KIDS[u]:
        XS[u] = _slot[0]
        _slot[0] += 1
    else:
        for v in KIDS[u]:
            _lay(v)
        XS[u] = (XS[KIDS[u][0]] + XS[KIDS[u][-1]]) / 2


_lay(0)
NSLOT = _slot[0]


def _pos(box, u):
    x0, y0, x1, y1 = box
    W = x1 - x0 - 100
    X = x0 + 50 + W * (XS[u] + 0.5) / NSLOT
    Y = y0 + 70 + DEPTH[u] * (y1 - y0 - 190) / max(1, max(LEVELS))
    return X, Y


def _tree(cv, S, B, box, T, state, title, extra=None):
    """state(u) -> (kind, label)；kind: normal/gone/leaf1/leaf2"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    P = {u: _pos(box, u) for u in range(NN)}
    st = {u: state(S, u) for u in range(NN)}
    for a, b in EDGES:
        gone = st[a][0] in ('gone', 'leaf1', 'leaf2') or st[b][0] in ('gone', 'leaf1', 'leaf2')
        col = T['dim'] if gone else T['muted']
        hot = extra(S, a, b) if extra else False
        cv.line([P[a], P[b]], T['red'] if hot else col, 6 if hot else 3)
    for u in range(NN):
        X, Y = P[u]
        kind, lab = st[u]
        fill = {'normal': T['panel2'], 'gone': (50, 54, 62), 'leaf1': T['orange'], 'leaf2': T['pink']}[kind]
        cv.rect((X - 34, Y - 34, X + 34, Y + 34), fill=fill, outline=T['yellow'] if COINS[u] else T['border'],
                width=6 if COINS[u] else 2, r=34)
        cv.text((X, Y - 2), u, 30, T['bg'] if kind in ('leaf1', 'leaf2') else (T['dim'] if kind == 'gone' else T['text']), anchor='mm', bold=True, mono=True)
        if lab != '':
            cv.text((X, Y + 52), lab, 22, T['cyan'], anchor='mm', bold=True, mono=True)
    cv.text((x0 + 18, y1 - 30), '黄框 = 有金币　橙 = 被删的叶子　粉 = 再删一层　暗 = 已拓扑删除', 20, T['muted'])
CODE = '''
class Solution(object):
    def collectTheCoins(self, coins, edges):

        n = len(coins)
        g = [[] for _ in range(n)]
        d = [0] * n
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
            d[x] += 1
            d[y] += 1
        
        q = []
        vis = set()
        for index in range(n):
            if d[index] == 1 and coins[index] == 0:
                q.append(index)
                vis.add(index)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                d[nxt] -= 1
                if d[nxt] == 1 and coins[nxt] == 0:
                    q.append(nxt)
                    vis.add(nxt)
                    tail += 1
        
        q = []
        f = [0] * n
        for index in range(n):
            if d[index] == 1 and coins[index] == 1:
                q.append(index)
                f[index] = 0
                vis.add(index)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                d[nxt] -= 1
                if d[nxt] == 1 and nxt not in vis:
                    f[nxt] = f[now] + 1
                    q.append(nxt)
                    tail += 1
                    vis.add(nxt)
        
        res = 0
        for x, y in edges:
            if f[x] >= 2 and f[y] >= 2:
                res += 2
        
        return res
'''
_lines = CODE.strip('\n').split('\n')
_LF = [i + 1 for i, s in enumerate(_lines) if 'f = [0] * n' in s][0]
_LR = [i + 1 for i, s in enumerate(_lines) if 'res = 0' in s][0]


def _removed1():
    deg = [len(a) for a in ADJ]
    q = [i for i in range(NN) if deg[i] == 1 and COINS[i] == 0]
    out = list(q)
    h = 0
    while h < len(q):
        u = q[h]
        h += 1
        for y in ADJ[u]:
            deg[y] -= 1
            if deg[y] == 1 and COINS[y] == 0:
                q.append(y)
                out.append(y)
    return out


R1 = _removed1()


def _state(S, u):
    if 'vis' not in S or 'd' not in S:
        return ('normal', '')
    ln = S.get('_line', 0)
    lab = S['f'][u] if (ln > _LF and 'f' in S) else ''
    if u in S['vis'] and u in R1:
        return ('gone', lab)
    if u in S['vis']:
        return ('leaf1' if COINS[u] and S['f'][u] == 0 and len(ADJ[u]) == 1 else 'leaf2', lab)
    return ('normal', lab)


def _hot(S, a, b):
    if 'f' not in S or S.get('_line', 0) < _LR:
        return False
    return S['f'][a] >= 2 and S['f'][b] >= 2


def _draw(cv, S, B, box, T):
    _tree(cv, S, B, box, T, _state, '树（下方青色 = f[i]：向外分叉里最远金币的距离）', _hot)


def _info(S):
    if 'vis' not in S:
        return ''
    t = f"已标记不用访问的点 `vis` = =={sorted(S['vis'])}=="
    if 'res' in S:
        t += f"　　必走边累计 `res` = =={S['res']}=="
    return t
CONFIG = dict(
    num=2603, title='收集树中金币', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='两轮拓扑 + 按边判断必走',
    tags=['图论算法', '链表树与回溯', '难度分 2712'],
    code=CODE,
    call=f'Solution().collectTheCoins({COINS}, {EDGES})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='d', label='d[i]（当前度数）', h=130,
             color=lambda S, i, v: 'orange' if 'vis' in S and i in S['vis'] else None),
        dict(type='text', fn=_info, size=24, h=60),
    ],
    watch=['now', 'nxt', ('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('res', 'res', 'green')],
    captions={
        'd = [0] * n': '先建图，并统计每个点的度数 `d`（度为 1 = 叶子）',
        'if d[index] == 1 and coins[index] == 0': lambda S, B, r: f'节点 `{S.index}`：度 {S.d[S.index]}、金币 {S.coins[S.index]}' + ('，==没金币的叶子==，收进队列并标记' if S.d[S.index] == 1 and S.coins[S.index] == 0 else '，不是'),
        'if d[nxt] == 1 and coins[nxt] == 0': lambda S, B, r: f'叶子 `{S.now}` 被删，邻居 `{S.nxt}`：度 {S.d[S.nxt]}、金币 {S.coins[S.nxt]}' + ('：又成了没金币的叶子，继续剪' if S.d[S.nxt] == 1 and S.coins[S.nxt] == 0 else '：停下，不继续剪'),
        'f = [0] * n': '`f[i]`：从 `i` 向外的分叉里，==最远金币离 i 多远==',
        'if d[index] == 1 and coins[index] == 1': lambda S, B, r: f'节点 `{S.index}`：度 {S.d[S.index]}、金币 {S.coins[S.index]}' + ('：==金币叶子==，`f = 0`，作为第二轮拓扑的起点' if S.d[S.index] == 1 and S.coins[S.index] == 1 else '：不是金币叶子'),
        'f[nxt] = f[now] + 1': '删掉 `{now}` 后 `{nxt}` 成了新叶子：外面最远金币又远一步 → `f[{nxt}] = {f[nxt]}`',
        'if f[x] >= 2 and f[y] >= 2': lambda S, B, r: f'边 `{S.x}-{S.y}`：两侧 f = `{S.f[S.x]}`、`{S.f[S.y]}`' + ('，==都 ≥ 2==：两边的金币都够不着对方 → 必走，来回 +2' if S.f[S.x] >= 2 and S.f[S.y] >= 2 else '，有一侧 < 2：另一侧收得到，不用走'),
        'res += 2': '这条边要来回走：`res = {res}`',
        'return res': '答案 `{res}`',
    },
    skip=['n = len', 'g = [[]', 'for x, y in edges', 'g[x].append', 'g[y].append', 'd[x] += 1', 'd[y] += 1', 'd[nxt] -= 1', 'if d[nxt] == 1 and nxt not in vis', 'q = []', 'vis = set()', 'for index in range',
          'q.append', 'vis.add', 'head, tail', 'while head < tail', 'now = q[head]', 'head += 1', 'for nxt in g[now]', 'tail += 1',
          'f[index] = 0', 'res = 0'],
    max_steps=90,
    cards=dict(
        one_liner='先剪无金币的枝，再算每点外侧金币多远，两侧都够远的边必走',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无根树，`coins[i]` 为 1 表示节点 `i` 有金币',
                 '任选起点，可收集距离 ==2 以内== 的金币或走到相邻点，最后回到起点',
                 '求最少经过的边数',
                 '示例：`coins=[0,0,0,1,1,0,0,1]` → `2`'],
        quote='若x这一侧存在一个距离x大于等于2的金币节点，同时y这一侧也存在一个距离y大于等于2的金币节点，那么x到y这条边就是必须要经过的。',
        quote_src='—— yiduobo 题解原文',
        idea=['从边出发：去掉某条边，树分成两半',
              '两半里的金币离这条边端点都 ≥ 2，谁也收不到对方 → 这条边必走',
              '某侧最远金币 < 2，说明是小分支，对面就能收走 → 不用走',
              '第一轮剪无金币叶子，第二轮从金币叶子起算 `f`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`f` 是「向外分叉最远金币距离」，被第一轮剪掉的点 `f` 保持 0',
                 '每条必走的边答案 +2（来回各一次）',
                 '对比灵神：灵神直接剪两层叶子数剩余边，yiduobo 逐条边判断',
                 '原文已是 Python 3 可运行，代码未改动'],
    ),
)
