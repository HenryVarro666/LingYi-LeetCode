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

_EMPS = [(1, 5, [2, 3]), (2, 3, [4, 5]), (3, 3, []), (4, 1, []), (5, 2, [])]
_IMP = {i: m for i, m, s in _EMPS}
_KIDS = {i: list(s) for i, m, s in _EMPS}
_PAR = {1: None}
for _i, _s in _KIDS.items():
    for _c in _s:
        _PAR[_c] = _i
_INFO = TreeInfo(_KIDS, _PAR, 1)

_SETUP = '''
class Employee(object):
    def __init__(self, id, importance, subordinates):
        self.id = id
        self.importance = importance
        self.subordinates = subordinates

emps = [%s]
''' % ', '.join(f'Employee({i}, {m}, {s})' for i, m, s in _EMPS)

_RES_LINE = 15
_WHILE_LINE = 12   # while l < r 所在行（代码第 12 行）


def _state(S):
    st = {u: dict(badge=f'重要度 {_IMP[u]}', bcolor='dim') for u in _INFO.order}
    if 'q' not in S or 'l' not in S:
        return st
    q = [e.id for e in S['q']]
    l = S['l']
    now = S['_inner'].get('now')
    cur = now.id if (now is not None and S['_line'] != _WHILE_LINE) else None
    for k, u in enumerate(q):
        if k < l and u != cur:
            st[u] = dict(fill='green', badge=f'已加 {_IMP[u]}', bcolor='green')
        elif u == cur:
            st[u] = dict(outline='yellow', badge=f'重要度 {_IMP[u]}', bcolor='yellow', ptr='now')
        else:
            st[u] = dict(outline='blue', badge=f'重要度 {_IMP[u]}', bcolor='blue')
    return st


def _info(S):
    if 'q' not in S or 'l' not in S:
        return '蓝框 = 在队列里等着，黄 = 正在处理，绿 = 重要度已加进 `res`'
    n = S['l'] - (1 if S['_line'] == _RES_LINE - 1 else 0)
    done = [S['q'][k].importance for k in range(max(0, min(n, len(S['q']))))]
    parts = ' + '.join(str(x) for x in done) if done else '0'
    return f"已处理的重要度：`{parts}`，`res = {S.get('res', 0)}`"


CONFIG = dict(
    num=690, title='员工的重要性', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='字典 + BFS 队列累加',
    tags=['灵神题单', '链表树与回溯'],
    setup=_SETUP,
    code='''
class Solution(object):
    def getImportance(self, employees, id):

        emp_dict = {}
        for emp in employees:
            emp_dict[emp.id] = emp

        l = 0
        r = 1
        res = 0
        q = [emp_dict[id]]
        while l < r:
            now = q[l]
            l += 1
            res += now.importance
            for sub in now.subordinates:
                q.append(emp_dict[sub])
                r += 1
        
        return res
''',
    call='Solution().getImportance(emps, 1)',
    expect=14,
    views=[
        dict(type='custom', draw=make_draw(_INFO, _state, '员工树（BFS：队列 q[l:r] 是等待处理的员工）', None), h=330),
        dict(type='queue', var='q', label='q（队列，下标 l 之前的已处理）', fmt=lambda e: f'员工{e.id}', h=110),
        dict(type='text', fn=_info, size=24, h=50),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('now', lambda S: S['_inner']['now'].id if 'now' in S['_inner'] else None, 'yellow'), ('res', 'res', 'green')],
    skip=['emp_dict[emp.id] = emp'],
    captions={
        'emp_dict = {}': '先建字典：==员工 id → 员工对象==，下属只给了 id，要靠它找人',
        'for emp in employees': lambda S, B, r: (f'员工 `{S.emp.id}` 放进字典' if 'emp' not in B or S.emp.id != B['emp'].id else '字典建好了'),
        'l = 0': '`l`、`r` 是队列的头尾下标：`q[l:r]` 是待处理的员工',
        'r = 1': '队列里先有 1 个员工（起点）',
        'res = 0': '`res` 累加重要度',
        'q = [emp_dict': '把起点员工 `{id}` 放进队列：从他开始向下 BFS',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：队列里还有人 → 继续' if S.l < S.r
                                          else f'`l = {S.l} = r = {S.r}`：队列空了，所有下属都处理过了 → 结束'),
        'now = q[l]': '取队头：员工 `{now.id}`（重要度 `{now.importance}`，下属 `{now.subordinates}`）',
        'l += 1': '队头出队：`l = {l}`',
        'res += now.importance': '`res = {B.res} + {now.importance} = ` =={res}==',
        'for sub in now.subordinates': lambda S, B, r: (f'下属 `{S.sub}` 要入队' if S['_inner'].get('sub') != B['_inner'].get('sub')
                                                        else f'`{S.now.id}` 的下属都入队了'),
        'q.append': '员工 `{sub}` 入队，等着被处理',
        'r += 1': '队尾后移：`r = {r}`',
        'return res': '队列处理完，总重要度 `res = ` =={res}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='员工是树上的节点：从起点向下 BFS，把重要度全加起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每个员工有 `id`、`importance` 和直系下属 `subordinates`（下属的 id 列表）',
                 '给定员工 `id`，返回他和==所有下属（含间接）==的重要度之和',
                 '本视频：5 个员工，`id = 1` → `14`'],
        quote='题目保证每个员工最多有一个上级，可能有多个下级，那么如果将员工视为节点，那么这就是由多棵树组成的森林。题目要求的员工的重要性，就是森林中某棵子树的节点元素之和。',
        quote_src='—— yiduobo 题解',
        idea=['员工构成「森林」，要求的就是 `id` 所在那棵==子树的节点值之和==',
              '先用字典把 id 变成员工对象；然后用列表当队列做 BFS，`l` 是队头、`r` 是队尾',
              '每取出一个员工就把他的重要度加进 `res`，再把他的下属全部入队'],
        result='运行结束，返回 `14`：`5 + 3 + 3 + 1 + 2`',
        summary=['时间 `O(n)`，空间 `O(n)`；BFS 和 DFS 都可以，这里用列表模拟队列',
                 '易错：`subordinates` 里是 ==id==，要经过字典换成员工对象',
                 '队列用下标 `l` 当队头、不真正删除元素，所以 `q` 会保留全部访问过的员工',
                 '对比灵神：灵神用递归（自底向上返回总和），yiduobo 用队列迭代累加',
                 '原文开头的 `Employee` 类定义（题目已给）是文档字符串，已删去，类定义放在 setup 里'],
    ),
)
