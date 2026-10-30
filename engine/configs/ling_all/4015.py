# ---------- 一般树自绘（custom 视图）：按孩子列表布局，状态由当前步变量推出 ----------
def _tree_pos(CH, root, box, top=46, bottom=34):
    x0, y0, x1, y1 = box
    depth, pos, cnt = {}, {}, [0]

    def go(u, d):
        depth[u] = d
        ks = CH.get(u, [])
        if not ks:
            pos[u] = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            pos[u] = sum(pos[k] for k in ks) / len(ks)
    go(root, 0)
    nl, md = max(1, cnt[0]), max(depth.values()) + 1
    sp = min(110, (x1 - x0 - 60) / nl)
    dy = min(100, (y1 - y0 - top - bottom) / max(1, md))
    rad = max(16, min(26, sp * 0.36, dy * 0.3))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * (nl - 1)) / 2
    return {u: (sx + pos[u] * sp, y0 + top + depth[u] * dy + rad) for u in depth}, rad


def _gtree(cv, T, box, CH, root, cur, hl=(), done=(), badge=None, sub=None, title=None, anc=()):
    P, rad = _tree_pos(CH, root, box)
    if title:
        cv.text((box[0] + 18, box[1] + 4), title, 22, T['muted'], bold=True)
    for u, ks in CH.items():
        for k in ks:
            on = k in anc or k == cur
            cv.line([P[u], P[k]], T['yellow'] if on and u in anc or (on and u == cur) else T['border'], 5 if on else 3)
    for u, (X, Y) in P.items():
        fill, outl, w, tc = T['panel2'], T['border'], 2, T['text']
        if u in done:
            fill, tc = T['green'], T['bg']
        if u in hl:
            fill, tc = T['cyan'], T['bg']
        if u in anc:
            outl, w = T['yellow'], 4
        if u == cur:
            outl, w = T['blue'], 5
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outl, width=w)
        cv.text((X, Y), u, int(rad * 0.95), tc, anchor='mm', bold=True)
        if sub and u in sub:
            cv.text((X + rad + 6, Y - 4), sub[u], 20, T['yellow'], anchor='lm', bold=True, mono=True)
        if badge and u in badge:
            s = badge[u]
            bw = cv.tlen(s, 19, bold=True) + 14
            cv.rect((X - bw / 2, Y + rad + 4, X + bw / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
            cv.text((X, Y + rad + 16), s, 19, T['green'], anchor='mm', bold=True)


def _anc(PAR, u):
    out = []
    while u is not None and PAR.get(u) is not None:
        u = PAR[u]
        out.append(u)
    return out


def _preorder(CH, root):
    out = []

    def go(u):
        out.append(u)
        for k in CH[u]:
            go(k)
    go(root)
    return out


def _subtree(CH, u):
    out = [u]
    for k in CH[u]:
        out += _subtree(CH, k)
    return out

PARENT = [-1, 0, 0, 0, 2, 2]
NUMS = [5, 2, 3, 1, 4, 6]
N = len(PARENT)
CH = {i: [] for i in range(N)}
for _i in range(1, N):
    CH[PARENT[_i]].append(_i)
PAR = {i: (PARENT[i] if i else None) for i in range(N)}


def _draw(cv, S, B, box, T):
    inner = S.get('_inner', {})
    x = inner.get('x')
    depth = S.get('depth')
    badge = {}
    if depth is not None:
        badge = {u: f'd={depth[u]}' for u in range(N) if u == 0 or depth[u] > 0}
    if 'h' in S:
        badge = {u: f"{S['nums'][u]}×{S['h'] - depth[u]}" for u in range(N)}
    anc = set(_anc(PAR, x)) if x is not None else set()
    _gtree(cv, T, box, CH, 0, x, badge=badge, sub={u: f'v={NUMS[u]}' for u in range(N)}, anc=anc,
           title='树（旁边 v = nums[i]；绿框先是深度 d，最后变成 权重 = nums × (h − d)）')


CODE = '''
class Solution:
    def weightedSum(self, parent: list[int], nums: list[int]) -> int:
        n = len(parent)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parent[i]].append(i)

        depth = [0] * n
        def dfs(x: int) -> None:
            for y in g[x]:
                depth[y] = depth[x] + 1
                dfs(y)
        dfs(0)

        h = max(depth) + 1
        return sum(x * (h - d) for x, d in zip(nums, depth))
'''


def _g(S, k):
    return S['_inner'].get(k)


CONFIG = dict(
    num=4015, title='树的加权和', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='一次 DFS 记深度 + 公式求和',
    tags=['链表树与回溯', '难度分 1534'],
    code=CODE,
    call='Solution().weightedSum([-1,0,0,0,2,2], [5,2,3,1,4,6])',
    expect=37,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='depth', label='depth[i]（本代码里根的深度记为 0）', cell=70, h=120),
        dict(type='calls', h=190),
    ],
    watch=[('x', lambda S: _g(S, 'x'), 'blue'), ('y', lambda S: _g(S, 'y'), 'pink'), ('h', 'h', 'yellow')],
    captions={
        'n = len(parent)': '`parent[i]` 是 `i` 的父节点，一共 `n = {n}` 个节点',
        'g[parent[i]].append(i)': '`{i}` 的父亲是 `{parent[i]}` → 挂到 `g[{parent[i]}]`：`g[{parent[i]}] = {g[parent[i]]}`',
        'depth = [0] * n': '`depth[i]` 记录节点 `i` 的深度，根节点 `0` 先记为 `0`',
        'for y in g[x]': lambda S, B, r: (f"枚举 `{_g(S, 'x')}` 的孩子 `{_g(S, 'y')}`" if _g(S, 'y') != B['_inner'].get('y') or B['_inner'].get('x') != _g(S, 'x') else f"`{_g(S, 'x')}` 的孩子都处理完了，返回上一层"),
        'depth[y] = depth[x] + 1': lambda S, B, r: f"孩子比父亲深一层：`depth[{_g(S, 'y')}] = depth[{_g(S, 'x')}] + 1 = {S['depth'][_g(S, 'y')]}`",
        'dfs(y)': lambda S, B, r: f"带着刚算好的深度，进入孩子 `{B['_inner'].get('y')}`",
        'h = max(depth) + 1': '`depth` 里根是 0，所以树高 ==h = max(depth) + 1 = {h}==（题目的深度从 1 开始）',
        'return sum(': '题目的 `h - d + 1`（`d` 从 1 数）就是这里的 `h - depth`：逐个相乘再求和 = =={ret}==',
    },
    skip=['dfs(0)', 'for i in range(1, n)'],
    max_steps=80,
    cards=dict(
        one_liner='先把深度存进数组，权重 = `nums × (h − d)`，再扫一遍求和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`parent` 描述以 `0` 为根的树，`nums[i]` 是节点 `i` 的值',
                 '深度为 `d` 的节点权重是 `nums[i] * (h - d + 1)`，`h` 是树高，根深度为 1',
                 '求所有节点权重之和',
                 '示例：`parent = [-1,0,0,0,2,2]`，`nums = [5,2,3,1,4,6]` → `37`'],
        quote='在第一次 DFS 中，可以顺带求出每个节点的深度，保存到数组 depth 中。这样第二次 DFS 可以用简单的循环代替。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['先建 `g`：每个节点的孩子列表',
              '一次自顶向下 DFS：孩子深度 = 父亲深度 + 1，顺便存进 `depth`',
              '树高 `h = max(depth) + 1`，再用 `zip(nums, depth)` 一行求和'],
        result='`h = 3`，权重和 `15 + 4 + 6 + 2 + 4 + 6 = 37`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：代码里根的深度是 `0`，题目是 `1`，所以 `h = max(depth) + 1`，权重 `h - d` 正好对上 `h - d + 1`',
                 '写法一：先 DFS 求高度 `h`，再自顶向下递归把权重 `h` 每层减一',
                 '链状树深度为 `n`，递归会很深，Python 里要注意递归上限'],
    ),
)
