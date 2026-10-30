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
class Solution:
    def collectTheCoins(self, coins: List[int], edges: List[List[int]]) -> int:
        n = len(coins)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建图
        deg = list(map(len, g))  # 每个节点的度数（邻居个数）

        left_edges = n - 1  # 剩余边数
        # 拓扑排序，去掉没有金币的子树
        q = []
        for i, (d, c) in enumerate(zip(deg, coins)):
            if d == 1 and c == 0:  # 没有金币的叶子
                q.append(i)
        while q:
            left_edges -= 1  # 删除节点到其父节点的边
            for y in g[q.pop()]:
                deg[y] -= 1
                if deg[y] == 1 and coins[y] == 0:  # 没有金币的叶子
                    q.append(y)

        # 再次拓扑排序
        for i, (d, c) in enumerate(zip(deg, coins)):
            if d == 1 and c:  # 有金币的叶子（判断 c 是避免把没有金币的叶子也算进来）
                q.append(i)
        left_edges -= len(q)  # 删除所有叶子（到其父节点的边）
        for x in q:  # 遍历所有叶子
            for y in g[x]:
                deg[y] -= 1
                if deg[y] == 1:  # y 现在是叶子了
                    left_edges -= 1  # 删除 y（到其父节点的边）
        return max(left_edges * 2, 0)
'''
_lines = CODE.strip('\n').split('\n')
_L2 = [i + 1 for i, s in enumerate(_lines) if 'enumerate(zip' in s][1]


def _removed1():
    deg = [len(a) for a in ADJ]
    q = [i for i in range(NN) if deg[i] == 1 and COINS[i] == 0]
    out = []
    while q:
        u = q.pop()
        out.append(u)
        for y in ADJ[u]:
            deg[y] -= 1
            if deg[y] == 1 and COINS[y] == 0:
                q.append(y)
    return out


R1 = _removed1()


def _state(S, u):
    if 'left_edges' not in S or 'deg' not in S:
        return ('normal', '')
    lab = S['deg'][u]
    if S.get('_line', 0) < _L2:
        k = NN - 1 - S['left_edges']
        return ('gone', lab) if u in R1[:k] else ('normal', lab)
    if u in R1:
        return ('gone', lab)
    if u in S['q']:
        return ('leaf1', lab)
    if S['deg'][u] <= 1 and S.get('_line', 0) > _L2 + 4:
        return ('leaf2', lab)
    return ('normal', lab)


def _draw(cv, S, B, box, T):
    _tree(cv, S, B, box, T, _state, '树（数字 = 节点，下方青色 = 当前度数 deg）')


def _info(S):
    if 'left_edges' not in S:
        return ''
    t = f"剩余边数 `left_edges` = =={S['left_edges']}=="
    if S.get('_line', 0) >= 33:
        t += f"　　答案 `max(left_edges*2, 0)` = =={max(S['left_edges'] * 2, 0)}=="
    return t
CONFIG = dict(
    num=2603, title='收集树中金币', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='拓扑排序剪枝 · 剩余边数 ×2',
    tags=['图论算法', '链表树与回溯', '难度分 2712'],
    code=CODE,
    call=f'Solution().collectTheCoins({COINS}, {EDGES})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='deg', label='deg[i]（度数）', h=130,
             color=lambda S, i, v: 'orange' if 'q' in S and i in S['q'] else None),
        dict(type='text', fn=_info, size=26, h=60),
    ],
    watch=['x', 'y', ('left_edges', 'left_edges', 'green'), ('q', 'q', 'cyan')],
    captions={
        'g[y].append(x)': '建图：`{x}` 和 `{y}` 互为邻居',
        'deg = list': '`deg[i]` = 节点 `i` 的邻居个数，度为 1 就是叶子',
        'left_edges = n - 1': '一开始树有 `n-1 = {left_edges}` 条边',
        14: lambda S, B, r: f'节点 `{S.i}`：度 {S.d}，金币 {S.c}' + ('，==无金币的叶子==，去了也没用' if S.d == 1 and S.c == 0 else '，不是无金币叶子'),
        15: '放进队列，等会儿把它剪掉',
        17: '删掉一个无金币的叶子，等于==删掉它到父节点的那条边==：`left_edges = {left_edges}`',
        19: '邻居 `{y}` 少了一个邻居：度数 → `{deg[y]}`',
        20: lambda S, B, r: (f'`{S.y}` 度为 {S.deg[S.y]}、金币 {S.coins[S.y]}' + ('：又变成无金币叶子 → 入队，继续剪' if S.deg[S.y] == 1 and S.coins[S.y] == 0 else '：不满足，停')),
        25: lambda S, B, r: (f'节点 `{S.i}`：度 {S.d}、金币 {S.c}' + ('：==有金币的叶子==，距离 2 内的金币在祖父处就能收，也要剪' if S.d == 1 and S.c else '：不是有金币的叶子')),
        26: '有金币的叶子入队：这是要剪的第一层',
        27: '第一层：删掉所有有金币的叶子（各一条边）：`left_edges -= {len(q)}` → `{left_edges}`',
        30: '叶子 `{x}` 被删，邻居 `{y}` 度数 → `{deg[y]}`',
        31: lambda S, B, r: f'`{S.y}` 度数 → `{S.deg[S.y]}`' + ('：它现在成了叶子，要剪第二层' if S.deg[S.y] == 1 else '：还有别的分支，不剪'),
        32: '第二层：`{y}` 也被剪，删它到父节点的边：`left_edges = {left_edges}`',
        'return max': '剩下的边每条==走去再走回==，共 `{left_edges}` × 2 = `{left_edges*2}`；和 0 取最大，防止剩 -1',
    },
    skip=['n = len', 'g = [[]', 'for x, y in edges', 'g[x].append', 'q = []', 'for y in g[q.pop()]', 'for y in g[x]', 'for x in q', 'while q',
          'for i, (d, c) in enumerate(zip(deg, coins)):'],
    max_steps=90,
    cards=dict(
        one_liner='剪掉无金币的叶子，再剪两层叶子，剩下的每条边走两遍',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无根树，`coins[i]` 为 1 表示节点 `i` 有金币',
                 '任选起点，可收集距离 ==2 以内== 的金币或走到相邻点，最后回到起点',
                 '求最少经过的边数',
                 '示例：`coins=[0,0,0,1,1,0,0,1]` → `2`'],
        quote='由于题目要求最后回到出发点，无论从哪个点出发，每条边都必须走两次。这是因为把出发点作为树根，递归遍历这棵树，那么往下「递」是一次，往上「归」又是一次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['无金币的叶子不用去：拓扑排序一层层剪掉',
              '距离 2 内都能收：金币叶子不必走到，到它的祖父就行 → 再剪两层叶子',
              '剩下的点必须走到，每条边来回各一次，答案 `= 剩余边数 × 2`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：删点等于删它到父节点的边，计数用 `left_edges`',
                 '易错：全部被删时剩两点会重复扣一条边得 -1，要 `max(..., 0)`',
                 '拓扑排序不要求严格顺序，用栈代替队列也行',
                 '对比：yiduobo 用「每个点向外最远金币距离」判断边是否必走'],
    ),
)
