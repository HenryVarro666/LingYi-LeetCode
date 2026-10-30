# ---- 一般树绘制：从边表静态布局，状态（路径/已返回）由当前节点推出
def build_kids(edges, root, sort=False):
    adj = {}
    for x, y in edges:
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)
    kids, par, st = {}, {root: None}, [root]
    while st:
        u = st.pop()
        ks = sorted(adj.get(u, [])) if sort else list(adj.get(u, []))
        kids[u] = [v for v in ks if v != par[u]]
        for v in kids[u]:
            par[v] = u
            st.append(v)
    return kids, par


class TreeInfo:
    def __init__(self, kids, par, root):
        self.kids, self.par, self.root = kids, par, root
        self.order, self.depth = [], {root: 0}

        def pre(u):
            self.order.append(u)
            for v in kids.get(u, []):
                self.depth[v] = self.depth[u] + 1
                pre(v)
        pre(root)
        self.idx = {u: i for i, u in enumerate(self.order)}
        self.xs, cnt = {}, [0]

        def lay(u):
            ks = kids.get(u, [])
            if not ks:
                self.xs[u] = cnt[0]
                cnt[0] += 1
            else:
                for v in ks:
                    lay(v)
                self.xs[u] = (self.xs[ks[0]] + self.xs[ks[-1]]) / 2
        lay(root)
        self.nleaf = cnt[0]
        self.maxd = max(self.depth.values()) + 1

    def path(self, u):
        out = []
        while u is not None:
            out.append(u)
            u = self.par[u]
        return out[::-1]

    def sub(self, u):
        out = [u]
        for v in self.kids.get(u, []):
            out += self.sub(v)
        return out

    def phase(self, cur, k=0):
        """cur 是当前递归所在节点，k 是 cur 已经处理完的孩子个数。返回 (路径上的节点集合, 已返回的节点集合)"""
        if cur is None or cur not in self.idx:
            return set(), set()
        path = self.path(cur)
        done = set()
        for a, b in zip(path, path[1:] + [None]):
            ks = self.kids.get(a, [])
            n = k if b is None else ks.index(b)
            for v in ks[:n]:
                done.update(self.sub(v))
        return set(path), done


def make_draw(info, state, title, legend=None):
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        sp = min(120, (x1 - x0 - 80) / max(1, info.nleaf))
        dy = min(110, (y1 - y0 - 110) / max(1, info.maxd))
        rad = max(18, min(30, sp * 0.4, dy * 0.3))
        sx = x0 + 40 + ((x1 - x0 - 80) - sp * info.nleaf) / 2 + sp / 2
        P = {u: (sx + info.xs[u] * sp, y0 + 70 + info.depth[u] * dy + rad) for u in info.order}
        st = state(S)
        for u in info.order:
            for v in info.kids.get(u, []):
                on = st.get(v, {}).get('edge')
                cv.line([P[u], P[v]], T[on] if on else T['border'], 5 if on else 3)
        for u in info.order:
            X, Y = P[u]
            d = st.get(u, {})
            fill = T[d['fill']] if d.get('fill') else T['panel2']
            out = T[d['outline']] if d.get('outline') else T['border']
            cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=out, width=5 if d.get('outline') else 2)
            cv.text((X, Y), u, int(rad * 0.95), T['bg'] if d.get('fill') else T['text'], anchor='mm', bold=True)
            if d.get('mark'):
                cv.d.ellipse((X + rad * 0.55, Y - rad * 1.25, X + rad * 1.35, Y - rad * 0.45), fill=T[d['mark']])
            if d.get('badge') is not None:
                s = str(d['badge'])
                bc = T[d.get('bcolor', 'green')]
                w = cv.tlen(s, 20, bold=True) + 16
                cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=bc, width=2, r=8)
                cv.text((X, Y + rad + 18), s, 20, bc, anchor='mm', bold=True)
            if d.get('ptr'):
                cv.text((X - rad - 8, Y), d['ptr'], 20, T['blue'], anchor='rm', bold=True)
        if legend:
            cv.text((x1 - 18, y0 + 4), legend, 19, T['dim'], anchor='ra')
    return draw

_EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [4, 5]]
_KIDS, _PAR = build_kids(_EDGES, 0)
_INFO = TreeInfo(_KIDS, _PAR, 0)
_SIZE = {u: len(_INFO.sub(u)) for u in _INFO.order}


def _good(u):
    return len({_SIZE[v] for v in _KIDS.get(u, [])}) <= 1


def _make_state(cur_key, acc_key, fin_cond):
    """cur_key: 当前节点变量；acc_key: 已处理完的儿子子树大小之和（ling: size-1，yiduobo: tot）"""
    def _state(S):
        i = S['_inner']
        st = {}
        if fin_cond(i):
            for u in _INFO.order:
                st[u] = dict(fill='green' if _good(u) else 'red', badge=f'size {_SIZE[u]}', bcolor='green' if _good(u) else 'red')
            return st
        cur = i.get(cur_key) if 'fa' in i or 'now' in i else None
        k = 0
        if cur is not None and acc_key(i) is not None:
            acc, kids = acc_key(i), _KIDS.get(cur, [])
            while k < len(kids) and acc > 0:
                acc -= _SIZE[kids[k]]
                k += 1
        p, done = _INFO.phase(cur, k)
        for u in _INFO.order:
            d = {}
            if u in p:
                d.update(outline='yellow', edge='yellow')
                if u == cur:
                    d['ptr'] = cur_key
            elif u in done:
                g = _good(u)
                d.update(fill='green' if g else 'red', badge=f'size {_SIZE[u]}', bcolor='green' if g else 'red')
            st[u] = d
        return st
    return _state

_state = _make_state('x', lambda i: (i['size'] - 1) if 'size' in i else None, lambda i: 'dfs' in i and 'fa' not in i)


def _info(S):
    i = S['_inner']
    if 'x' not in i or 'fa' not in i:
        return '绿 = 好节点（儿子子树大小都相同），红 = 不是好节点'
    kids = _KIDS.get(i['x'], [])
    return f"节点 `{i['x']}` 有 {len(kids)} 个儿子；已累计 `size = {i.get('size', '?')}`，基准 `sz0 = {i.get('sz0', '?')}`"


def _cap_cmp(S, B, ret):
    if S.sz != S.sz0:
        return f'`sz = {S.sz}` ≠ `sz0 = {S.sz0}` → 儿子子树大小不一样，==不是好节点=='
    return f'`sz = {S.sz}` = `sz0 = {S.sz0}` → 目前大小还都一样'


def _cap_ans(S, B, ret):
    if S.ok:
        return f'`ok = True`：节点 `{S.x}` 的儿子子树大小都一样（叶子也算）→ ==好节点==，`ans = {S.ans}`'
    return f'`ok = False`：节点 `{S.x}` 的儿子子树大小不全相同 → 不是好节点，`ans` 不变 = {S.ans}'


CONFIG = dict(
    num=3249, title='统计好节点的数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 返回子树大小 · 自底向上',
    tags=['灵神题单', '链表树与回溯', '难度分 1566'],
    code='''
class Solution:
    def countGoodNodes(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        ans = 0
        def dfs(x: int, fa: int) -> int:
            size, sz0, ok = 1, 0, True
            for y in g[x]:
                if y == fa:
                    continue  # 不能递归到父节点
                sz = dfs(y, x)
                if sz0 == 0:
                    sz0 = sz  # 记录第一个儿子子树的大小
                elif sz != sz0:  # 存在大小不一样的儿子子树
                    ok = False  # 注意不能 break，其他子树 y 仍然要递归
                size += sz
            nonlocal ans
            ans += ok
            return size
        dfs(0, -1)
        return ans
''',
    call='Solution().countGoodNodes([[0,1],[0,2],[1,3],[1,4],[4,5]])',
    expect=4,
    views=[
        dict(type='custom', draw=make_draw(_INFO, _state, '树（黄 = 递归路径，数字 = 子树大小）', None), h=330),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('size', lambda S: S['_inner'].get('size'), 'yellow'),
           ('sz0', lambda S: S['_inner'].get('sz0'), 'cyan'), ('ok', lambda S: S['_inner'].get('ok'), 'pink'),
           ('ans', 'ans', 'green')],
    skip=['for y in g[x]', 'continue', 'g[x].append(y)', 'g[y].append(x)', 'nonlocal ans', 'n = len(edges)'],
    captions={
        'g = [[]': '`g[x]` 存节点 `x` 的所有邻居：边是无向的，建树时==两个方向都要加==',
        'for x, y in edges': lambda S, B, r: (f'边 `({S.x}, {S.y})`：`g[{S.x}]` 和 `g[{S.y}]` 互相加入' if S.x != B.get('x') or S.y != B.get('y')
                                              else '所有边处理完，树建好了'),
        'ans = 0': '`ans` 统计好节点个数（`dfs` 里用 `nonlocal` 修改）',
        'size, sz0, ok = 1': '节点 `{x}`：`size = 1`（自己），`sz0` 记第一个儿子的子树大小，`ok = True` 先假设是好节点',
        'if y == fa': lambda S, B, r: (f'邻居 `y = {S.y}` 是父节点 → ==不能递归回去==，跳过' if S.y == S.fa
                                       else f'邻居 `y = {S.y}` 不是父节点 `{S.fa}` → 是儿子'),
        'sz = dfs(y, x)': '递归求儿子 `{y}` 的子树大小（传入 `fa = {B.x}` 防止走回头）',
        'if sz0 == 0': lambda S, B, r: (f'`sz0 == 0`：`{S.y}` 是第一个儿子，子树大小 `{S.sz}` 当作基准' if S.sz0 == 0
                                        else f'`sz0 = {S.sz0}` 已有基准 → 去和 `sz = {S.sz}` 比'),
        'sz0 = sz': '`sz0 = {sz0}`：以后的儿子子树都要和它比',
        'elif sz != sz0': _cap_cmp,
        'ok = False': '`ok = False`；==不能 break==：后面的儿子仍要递归，否则 `size` 会算少',
        'size += sz': '`size = {B.size} + {sz} = {size}`：累加儿子子树的大小',
        'ans += ok': _cap_ans,
        'return size': '返回子树大小 =={ret}==：以 `{x}` 为根，交给父节点去比较',
        'dfs(0, -1)': '从根 `0` 开始 DFS，`fa = -1` 表示根没有父节点',
        'return ans': '好节点一共 `{ans}` 个',
    },
    max_steps=120,
    cards=dict(
        one_liner='DFS 返回子树大小，儿子子树大小全相同就是好节点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，`n` 个节点，根是 `0`',
                 '节点的==所有儿子的子树大小都相同==，它就是好节点（叶子也算）',
                 '本视频：`edges = [[0,1],[0,2],[1,3],[1,4],[4,5]]` → `4`'],
        quote='建树，然后从根节点 0 开始 DFS 这棵树。DFS 返回子树大小。对于节点 x，如果其是叶子节点，或者其所有儿子子树大小都一样，那么答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(x, fa)` 返回以 `x` 为根的子树大小：`1 + 所有儿子子树大小之和`',
              '遍历儿子时，用 `sz0` 记第一个儿子的大小，后面的和它比，不同就 `ok = False`',
              '叶子没有儿子，`ok` 保持 `True`，自然也是好节点'],
        result='运行结束，返回 `4`：好节点是 `2、3、4、5`，节点 `0`、`1` 不是',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：发现大小不同也==不能 break==，其他儿子仍要递归，否则 `size` 算少',
                 '无向树要传 `fa`，邻居里的父节点要跳过',
                 '`sz0 == 0` 当作「还没有基准」：子树大小至少为 1，所以不会混淆'],
    ),
)
