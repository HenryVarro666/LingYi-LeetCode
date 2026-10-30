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

_EDGES = [[1, 2], [1, 3], [1, 7], [2, 4], [2, 6], [3, 5]]
_T, _TARGET = 3, 5
_KIDS, _PAR = build_kids(_EDGES, 1)
_INFO = TreeInfo(_KIDS, _PAR, 1)
_AP = _INFO.path(_TARGET)                      # 根到 target 的路径
_NC = {u: len(_KIDS.get(u, [])) for u in _INFO.order}   # 儿子个数
_DEN = {1: 1}                                   # 到达该节点的概率的分母
for _u in _INFO.order:
    for _v in _KIDS.get(_u, []):
        _DEN[_v] = _DEN[_u] * _NC[_u]

def _state(S):
    st = {u: {} for u in _INFO.order}
    st[_TARGET]['mark'] = 'pink'
    if 'used' not in S or 'q' not in S:
        return st
    used = {u for u in S['used'] if u in _DEN}
    front = set()
    if 'l' in S and 'r' in S and S['_inner'].get('now') is not None:
        front = {S['_inner']['now']}
    for u in used:
        st[u].update(fill='blue', badge=f'1/{_DEN[u]}', bcolor='blue')
    for u in front:
        st[u].update(outline='yellow', edge='yellow', ptr='now')
    return st


def _info(S):
    i = S['_inner']
    if 'step' not in S:
        return '蓝 = 已经到达过（下方是到达它的概率），粉点 = target'
    return f"第 `step = {S['step']}` 秒（共 `t = {S['t']}` 秒）：本轮从 `q[{S['l']}:{S['r']}]` 往外跳一步"


def _cap_hit(S, B, ret):
    if ret is None:
        if S.next != S.target:
            return f'`next = {S.next}` 不是 target `{S.target}` → 继续'
        return f'`next == target`：第 `step = {S.step}` 秒就到达 target 了'
    if S.step == S.t:
        return f'`step = {S.step} = t`：恰好第 t 秒到达 target → 答案 `1.0 / {B.h[B.next]}` = =={ret}=='
    return (f'`step = {S.step} < t = {S.t}`，但 target 没有孩子（`len(g[next]) == 1`）→ 青蛙停在原地，'
            f'答案 `1.0 / {B.h[B.next]}` = =={ret}==')


CONFIG = dict(
    num=1377, title='T 秒后青蛙的位置', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS 逐秒扩展 · 记录到达概率的分母',
    tags=['灵神题单', '链表树与回溯', '难度分 1824'],
    code='''
class Solution(object):
    def frogPosition(self, n, edges, t, target):

        if n == 1:
            return 1.0

        g = {x : set() for x in range(1, n + 1)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        g[1].add(0)

        f = [0] * (n + 1)
        f[1] = 1.0
        q = [1]
        l = 0
        r = 1
        used = set([0, 1])
        step = 0
        while l < r:
            h = [0] * (n + 1)
            step += 1
            if step > t:
                break
            for now in q[l : r]:
                for next in g[now]:
                    if next not in used:
                        h[next] = f[now] * (len(g[now]) - 1)
                        q.append(next)
                        used.add(next)
                        if next == target:
                            if len(g[next]) == 1 or step == t:
                                return 1.0 / h[next]
                            else:
                                return 0.0

            l, r = r, len(q)
            f = h[:]
        
        return 0.0
''',
    call='Solution().frogPosition(7, [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], 3, 5)',
    expect=1 / 3,
    views=[
        dict(type='custom', draw=make_draw(_INFO, _state, '树（蓝 = 已到达，下方是到达概率，黄 = 正在往外跳）', '粉点 = target'), h=330),
        dict(type='queue', var='q', label='q（BFS 队列，q[l:r] 是本秒要往外跳的节点）', fmt=lambda x: str(x), h=110),
        dict(type='text', fn=_info, size=24, h=50),
    ],
    watch=[('step', 'step', 'blue'), ('l', 'l', 'cyan'), ('r', 'r', 'pink'), ('now', lambda S: S['_inner'].get('now'), 'yellow'),
           ('next', lambda S: S['_inner'].get('next'), 'green')],
    skip=['g[x].add(y)', 'g[y].add(x)', 'h = [0] * (n + 1)', 'f[1] = 1.0', 'f = h[:]', 'for now in q', 'used.add(next)', 'l = 0', 'r = 1', 'step = 0'],
    captions={
        'if n == 1': '只有一个节点：青蛙无处可去，永远在节点 `1` → 概率 `1.0`',
        'g = {x : set()': '建邻接表：每个节点一个集合',
        'for x, y in edges': lambda S, B, r: (f'边 `({S.x}, {S.y})`：两个端点互相加入' if S.x != B.get('x') or S.y != B.get('y')
                                              else '树建好了'),
        'g[1].add(0)': '给节点 `1` 加一个虚拟邻居 `0` 当父亲：这样==任何节点的孩子数都是 `len(g[x]) - 1`==',
        'f = [0]': '`f[i]`：到达节点 `i` 的概率的==分母==（起点 `f[1] = 1`）',
        'q = [1]': 'BFS 队列 `q`，从节点 `1` 开始：每一轮 = 青蛙跳 1 秒；`q[l:r]` 是本轮要往外跳的节点',
        'used = set': '`used` 记录已到达过的节点（`0` 是虚拟父亲，也算已用）；`step` 记录已经跳了几秒',
        'while l < r': lambda S, B, ret: (f'队列里还有节点（`l = {S.l} < r = {S.r}`）→ 开始新的一秒' if S.l < S.r
                                          else '队列空了，青蛙无处可去'),
        'step += 1': '第 `{step}` 秒开始',
        'if step > t': lambda S, B, ret: (f'`step = {S.step}` > `t = {S.t}`：t 秒用完了，target 还没碰到 → 答案 `0.0`' if S.step > S.t
                                          else f'`step = {S.step}` ≤ `t = {S.t}`：还可以继续跳'),
        'for next in g[now]': lambda S, B, r: (f'`{S.now}` 的邻居 `next = {S.next}`' if S['_inner'].get('next') != B['_inner'].get('next')
                                               else f'`{S.now}` 的邻居都看完了'),
        'if next not in used': lambda S, B, r: (f'`{S.next}` 没到达过 → 青蛙可以跳过去' if S.next not in S.used
                                                else f'`{S.next}` 已经用过（是父亲）→ 不能跳回去'),
        'h[next] = f[now]': '`h[{next}] = f[{now}] * (len(g[{now}]) - 1) =` =={int(h[next])}==：到达 `{next}` 的概率是 `1/{int(h[next])}`（先跳到 `{now}` 的某个孩子，每个孩子概率 `1/孩子数`）',
        'q.append(next)': '`{next}` 入队（同时记入 `used`），下一秒从它继续往外跳',
        'used.add(next)': '标记 `{next}` 已到达',
        'if next == target': _cap_hit,
        'if len(g[next]) == 1': lambda S, B, ret: (f'`len(g[{S.next}]) = {len(S.g[S.next])}`，`step = {S.step}`，`t = {S.t}`'
                                                    + ('：满足「叶子」或「恰好 t 秒」→ 概率就是 1/h' if (len(S.g[S.next]) == 1 or S.step == S.t)
                                                       else '：它有孩子，下一秒青蛙就会跳走 → 概率 0')),
        'return 1.0 / h[next]': '返回 `1.0 / {B.h[B.next]}` = =={ret}==：路径上各节点孩子数相乘的倒数',
        'return 0.0': '返回 `0.0`',
    },
    max_steps=80,
    cards=dict(
        one_liner='BFS 一秒一层：到达概率 = 路径上各节点孩子数乘积的倒数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树 `n` 个顶点，青蛙从顶点 `1` 出发，每秒等概率跳到一个==未访问==的相邻顶点',
                 '没有可跳的顶点时，青蛙留在原地',
                 '求 `t` 秒后青蛙在 `target` 的概率',
                 '本视频：`n = 7, t = 3, target = 5` → `1/3`'],
        quote='若第p轮就到达了target，且p < t，那么此时应该根据target是否有孩子节点来进行判断。若target没有孩子节点，那么青蛙会一直留在target，因此答案为f[target]。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]` 是首次到达 `i` 的概率：`f[i] = f[j] / k`（`j` 是父亲，有 `k` 个孩子）',
              '代码里存的是分母：`h[next] = f[now] * (孩子数)`，最后返回 `1.0 / h[next]`',
              'BFS 恰好执行 `t` 轮：`t` 轮后到达，或更早到达但 `target` 没有孩子，都是 `1/h`；否则 `0`'],
        result='运行结束，返回 `1/3`：第 2 秒到达叶子 `5`，剩下 1 秒原地不动',
        summary=['时间 `O(n)`，空间 `O(n)`；`h` 每轮新建，只保存当前这一轮到达的节点',
                 '节点 `1` 加虚拟邻居 `0`，孩子数统一为 `len(g[x]) - 1`',
                 '易错：提前到达 `target` 时，要看它有没有孩子；有孩子就会跳走，答案为 `0`',
                 '`step > t` 要先判断再扩展：t 秒用完还没到 `target`，答案为 `0.0`',
                 '原文已是 Python 3 可运行的写法，代码未做改动；思路讲的是概率 `f[i] = f[j]/k`，代码里存的是分母',
                 '对比灵神：灵神 DFS 一路向下，找到后乘分母；yiduobo 用 BFS 逐秒扩展'],
    ),
)
