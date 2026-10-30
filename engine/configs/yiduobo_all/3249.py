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

_state = _make_state('now', lambda i: i.get('tot') if 'tot' in i else None, lambda i: 'dfs' in i and 'now' not in i)


def _info(S):
    i = S['_inner']
    if 'now' not in i or 'fa' not in i:
        return '绿 = 好节点（孩子子树节点数都相同），红 = 不是好节点'
    return f"节点 `{i['now']}`：`target = {i.get('target')}`（第一个孩子的节点数），`tot = {i.get('tot', '?')}`，`same = {i.get('same', '?')}`"


def _cap_if(S, B, ret):
    if S.target is None:
        return f'`target` 还是 None：`{S.nxt}` 是第一个孩子，节点数 `{S.cnt}` 作为基准'
    if S.target != S.cnt:
        return f'`target = {S.target}` ≠ `cnt = {S.cnt}` → 孩子子树的节点数不同，==now 不是好节点=='
    return f'`target = {S.target}` = `cnt = {S.cnt}` → 目前孩子子树大小都相同'


CONFIG = dict(
    num=3249, title='统计好节点的数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 同时算子树节点数 · 全局计数',
    tags=['灵神题单', '链表树与回溯', '难度分 1566'],
    code='''
class Solution(object):
    def countGoodNodes(self, edges):

        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        global res
        res = 0

        def dfs(now, fa):
            target = None
            same = True
            tot = 0

            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                cnt = dfs(nxt, now)
                if target is None:
                    target = cnt
                elif target != cnt:
                    same = False
                tot += cnt
            
            if same:
                global res
                res += 1
            
            return tot + 1
        
        dfs(0, -1)
        return res
''',
    call='Solution().countGoodNodes([[0,1],[0,2],[1,3],[1,4],[4,5]])',
    expect=4,
    views=[
        dict(type='custom', draw=make_draw(_INFO, _state, '树（黄 = 递归路径，数字 = 子树节点数）', None), h=330),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('target', lambda S: S['_inner'].get('target'), 'cyan'),
           ('same', lambda S: S['_inner'].get('same'), 'pink'), ('tot', lambda S: S['_inner'].get('tot'), 'yellow')],
    skip=['g[x].append(y)', 'g[y].append(x)', 'global res', 'n = len(edges)', 'continue', 'if nxt == fa', 'target = None', 'same = True'],
    captions={
        'g = [[]': '`g[x]` 存节点 `x` 的所有邻居，无向边要==双向==记录',
        'for x, y in edges': lambda S, B, r: (f'边 `({S.x}, {S.y})`：两个端点互相加入邻接表' if S.x != B.get('x') or S.y != B.get('y')
                                              else '所有边处理完，树建好了'),
        'res = 0': '`res` 是全局变量，记录好节点的个数',
        'tot = 0': '节点 `{now}`：`target` 记第一个孩子的子树节点数，`same` 先假设为 True，`tot` 累加孩子子树的节点数',
        'for nxt in g[now]': lambda S, B, r: (f'`{S.now}` 的邻居都看完了 → 孩子子树共 `tot = {S.tot}` 个节点' if S['_inner'].get('nxt') == B['_inner'].get('nxt')
                                              else f'看邻居 `nxt = {S.nxt}`'
                                              + ('：是父亲，跳过' if S.nxt == S.fa else '：是孩子')),
        'cnt = dfs(nxt, now)': '递归求孩子 `{nxt}` 的子树节点数（同时它自己是否好节点也在里面判断）',
        'if target is None': lambda S, B, r: ('`target` 还是 None → 这是第一个孩子，节点数 `{}` 作为基准'.format(S.cnt) if S.target is None
                                              else f'`target = {S.target}` 已有基准，去和 `cnt = {S.cnt}` 比'),
        'target = cnt': '`target = {target}`：之后的孩子子树都要和它一样',
        'elif target != cnt': lambda S, B, r: (f'`target = {S.target}` ≠ `cnt = {S.cnt}` → ==不一样==' if S.target != S.cnt
                                               else f'`target = {S.target}` = `cnt = {S.cnt}` → 还一样'),
        'same = False': '`same = False`：节点 `{now}` 不是好节点（但其他孩子仍要继续递归、累加）',
        'tot += cnt': '`tot = {B.tot} + {cnt} = {tot}`',
        'if same': lambda S, B, r: (f'`same = True`：节点 `{S.now}` 的孩子子树节点数都一样（叶子也算）→ ==好节点==' if S.same
                                    else f'`same = False`：节点 `{S.now}` 的孩子子树大小不同 → 不是好节点'),
        'res += 1': '好节点 +1：全局计数 `res` 加一',
        'return tot + 1': '返回 `tot + 1 = {tot} + 1 =` =={ret}==：以 `{now}` 为根的子树节点数',
        'dfs(0, -1)': '从根 `0` 出发，`fa = -1` 表示没有父亲',
        'return res': '好节点共 =={ret}== 个',
    },
    max_steps=120,
    cards=dict(
        one_liner='一边递归求子树节点数，一边比较孩子们的节点数是否相同',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树有 `n` 个节点，根是 `0`',
                 '若某节点的==所有孩子子树的节点数都相同==，它就是好节点',
                 '本视频：`edges = [[0,1],[0,2],[1,3],[1,4],[4,5]]` → `4`'],
        quote='对于当前求解的节点now，先递归求解其所有的孩子节点是否为好节点，在这个过程可以同步计算以每个孩子节点为根节点的子树中有多少个节点。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(now, fa)` 返回以 `now` 为根的子树节点数 `tot + 1`',
              '第一个孩子的节点数记成 `target`，之后每个孩子都和它比，不同就 `same = False`',
              '`same` 仍为 True 就是好节点，用全局变量 `res` 计数'],
        result='运行结束，返回 `4`：好节点是 `2、3、4、5`，节点 `0`、`1` 不是',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：邻居里有父亲 `fa`，要跳过；发现不同大小后也要继续递归并累加 `tot`',
                 '`target` 用 `None` 表示「还没有基准」；叶子没有孩子，`same` 保持 True',
                 '对比灵神：灵神用 `nonlocal` 修改答案，yiduobo 用 `global res`，思路一致',
                 '原文已是 Python 3 可运行的写法，代码未做改动'],
    ),
)
