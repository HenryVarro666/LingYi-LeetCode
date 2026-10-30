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

_EMPS = [(1, 5, [2, 3, 4]), (2, 3, [5, 6]), (3, 2, []), (4, 4, [7]), (5, 1, []), (6, 2, []), (7, 3, [8]), (8, -2, [])]
_IMP = {i: m for i, m, s in _EMPS}
_KIDS = {i: list(s) for i, m, s in _EMPS}
_PAR = {1: None}
for _i, _s in _KIDS.items():
    for _c in _s:
        _PAR[_c] = _i
_INFO = TreeInfo(_KIDS, _PAR, 1)


def _tot(u):
    return _IMP[u] + sum(_tot(v) for v in _KIDS[u])


_SETUP = '''
class Employee:
    def __init__(self, id, importance, subordinates):
        self.id = id
        self.importance = importance
        self.subordinates = subordinates

emps = [%s]
''' % ', '.join(f'Employee({i}, {m}, {s})' for i, m, s in _EMPS)


def _state(S):
    i = S['_inner']
    cur = i.get('id') if 'self' not in i else None
    p, done = _INFO.phase(cur)
    st = {}
    for u in _INFO.order:
        d = dict(badge=f'重要度 {_IMP[u]}', bcolor='dim')
        if u in p:
            d.update(outline='yellow', edge='yellow', bcolor='yellow')
            if u == cur:
                d['ptr'] = 'id'
        elif u in done:
            d.update(fill='green', badge=f'总和 {_tot(u)}', bcolor='green')
        st[u] = d
    return st


def _info(S):
    i = S['_inner']
    if 'self' in i or 'e' not in i:
        return '每个节点下方：灰 = 自己的重要度，绿 = 整棵子树的总和（已返回）'
    e = i['e']
    return f"员工 `{e.id}`：重要度 `{e.importance}`，直系下属 `{e.subordinates}`"


def _cap_entry(S, B, ret):
    e = S.e
    u = e.id
    par = _PAR[u]
    extra = ''
    if par is not None:
        ks = _KIDS[par]
        k = ks.index(u)
        if k > 0:
            extra = f'（上一个下属 `{ks[k - 1]}` 已返回总和 `{_tot(ks[k - 1])}`）'
    tail = '没有下属' if not e.subordinates else f'下属 `{e.subordinates}`'
    return f'`dfs({u})`：从哈希表取出员工 `{u}`，重要度 `{e.importance}`，{tail}{extra}'


def _cap_ret(S, B, ret):
    e = B.e
    if ret is not None:
        return f'员工 `{e.id}` 没有下属，`sum` 是空的 → 返回自己的重要度 =={ret}=='
    return (f'`{e.importance}` + `sum(dfs(sub) …)`：==递归==算每个下属 `{e.subordinates}` 的总重要度，先去 `dfs({e.subordinates[0]})`')


CONFIG = dict(
    num=690, title='员工的重要性', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='哈希表 + 自底向上 DFS',
    tags=['灵神题单', '链表树与回溯'],
    setup=_SETUP,
    code='''
class Solution:
    def getImportance(self, employees: List['Employee'], id: int) -> int:
        employees = {e.id: e for e in employees}
        def dfs(id: int) -> int:
            e = employees[id]
            return e.importance + sum(dfs(sub) for sub in e.subordinates)
        return dfs(id)
''',
    call='Solution().getImportance(emps, 1)',
    expect=18,
    views=[
        dict(type='custom', draw=make_draw(_INFO, _state, '员工树（黄 = 递归路径，绿 = 已返回）', None), h=420),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='calls', h=200),
    ],
    watch=[('id', lambda S: S['_inner'].get('id'), 'blue'), ('importance', lambda S: S['_inner']['e'].importance if 'e' in S['_inner'] else None, 'yellow')],
    captions={
        'employees = {': '建哈希表：==id → 员工对象==，这样给一个 id 就能一步找到员工和他的下属',
        'e = employees[id]': _cap_entry,
        'return e.importance': _cap_ret,
        'return dfs(id)': '从员工 `{id}` 开始 DFS（题目保证员工构成树，不用 vis 判重）',
    },
    max_steps=60,
    cards=dict(
        one_liner='员工的总重要度 = 自己 + 所有下属的总重要度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每个员工有 `id`、`importance`（重要度）和直系下属 `subordinates`',
                 '给定一个员工 `id`，返回他和==所有下属（含间接下属）==的重要度总和',
                 '示例：`[[1,5,[2,3]],[2,3,[]],[3,3,[]]]`，`id = 1` → `11`',
                 '本视频：8 个员工，`id = 1` → `18`'],
        quote='首先，创建一个哈希表，把第 i 个员工的 ID 映射到 employees[i] 对象上。然后从 id 开始 DFS（题目保证员工组成了树形结构）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['哈希表 `{e.id: e}`：下属只给了 id，靠它==按 id 找到员工对象==',
              '`dfs(id)` 返回以该员工为根的子树重要度之和',
              '自己的 `importance` 加上每个下属 `dfs(sub)` 的返回值；没有下属时 `sum` 为空，即只有自己'],
        result='运行结束，返回 `18`：`5+3+2+4+1+2+3−2`，重要度可以是负数',
        summary=['时间 `O(n)`：每个员工至多访问一次；空间 `O(n)`：哈希表 + 递归栈',
                 '易错：下属列表里是 ==id 不是下标==，不能直接 `employees[sub]`，必须先建哈希表',
                 '重要度可能为负（如 `-3`），所以不能用「有下属才累加」之类的剪枝',
                 '`sum(dfs(sub) for sub in e.subordinates)` 是生成器写法，没有下属时和为 `0`',
                 '同类题：一般树的自底向上 DFS（如 3249. 统计好节点的数目）'],
    ),
)
