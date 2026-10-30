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

_EDGES = [[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]]
_APPLE = [False, False, True, False, True, True, False]
_KIDS, _PAR = build_kids(_EDGES, 0, sort=True)
_INFO = TreeInfo(_KIDS, _PAR, 0)


def _val(u):
    c = sum(_val(v) for v in _KIDS.get(u, []))
    return c + 2 if (c > 0 or _APPLE[u]) else 0


def _state(S):
    cur = S['_inner'].get('now')
    p, _ = _INFO.phase(cur)
    done = {u for u in _INFO.order if S['used'][u] and u not in p} if 'used' in S else set()
    if cur is None and S.get('res') is not None:
        done, p = set(_INFO.order), set()
    st = {}
    for u in _INFO.order:
        d = {}
        if _APPLE[u]:
            d['mark'] = 'red'
        if u in p:
            d['outline'] = 'yellow'
            d['edge'] = 'yellow'
            if u == cur:
                d['ptr'] = 'now'
        elif u in done:
            v = _val(u)
            d['badge'] = f'返回 {v}'
            d['bcolor'] = 'green' if v else 'dim'
            if v:
                d['fill'] = 'green'
        st[u] = d
    return st


def _cap_if(S, B, ret):
    now, cost = S.now, S.cost
    if cost > 0:
        return f'孩子们的 `cost = {cost}` > 0 → 子树里有苹果，==必须走到 {now}=='
    if S.hasApple[now]:
        return f'节点 `{now}` 自己有苹果 → 必须走过来'
    return f'`cost = 0` 且节点 `{now}` 没有苹果 → ==不用来==这一趟'


def _info(S):
    i = S['_inner']
    if 'now' not in i:
        return '红点 = 有苹果；每走进一个必要的节点要 ==往返 2 点代价=='
    return f"节点 `{i['now']}`：孩子们的代价之和 `cost = {i.get('cost', 0)}`，自己{'有' if _APPLE[i['now']] else '没有'}苹果"


CONFIG = dict(
    num=1443, title='收集树上所有苹果的最少时间', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS · 子树有苹果才走一个来回',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def minTime(self, n, edges, hasApple):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        used = [False] * n
        res = max(self.dfs(0, g, hasApple, used) - 2, 0)
        return res
        

    def dfs(self, now, g, hasApple, used):
        used[now] = True
        cost = 0
        for next in g.get(now, set()):
            if not used[next]:
                cost += self.dfs(next, g, hasApple, used)

        if cost > 0 or hasApple[now]:
            return cost + 2
        else:
            return 0
''',
    call='Solution().minTime(7, [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], [False,False,True,False,True,True,False])',
    expect=8,
    views=[
        dict(type='custom', draw=make_draw(_INFO, _state, '无向树（黄 = 递归路径，绿 = 已返回且要走）', '红点 = 有苹果'), h=330),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='calls', h=210, hide=('g', 'hasApple', 'used')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('cost', lambda S: S['_inner'].get('cost'), 'yellow'),
           ('used', 'used', 'dim')],
    skip=['g[x].add(y)', 'g[y].add(x)', 'g[x] = set()', 'g[y] = set()', 'if x not in g', 'if y not in g'],
    captions={
        'g = {}': '先把边表建成邻接表 `g`（每个节点一个集合）',
        'for x, y in edges': '边 `({x}, {y})` 是无向的：两个方向都要记进邻接表',
        'used = [False]': '`used` 防止从孩子又走回父亲',
        'res = max(': '从根 `0` 开始 dfs；根不用「回来」，所以最后要 ==减 2==，`max(…, 0)` 兜住没有苹果的情况',
        'used[now] = True': '走进节点 `{now}`，标记已访问',
        'cost = 0': '`cost` 累计 `{now}` 的所有孩子子树要花的代价',
        'for next in g.get': lambda S, B, r: (f'`{S.now}` 的邻居都看完了 → 孩子们的代价加完，`cost = {S.cost}`' if S['_inner'].get('next') == B['_inner'].get('next')
                                      else f'遍历 `{S.now}` 的邻居，下一个是 `{S.next}`'),
        'if not used[next]': lambda S, B, r: (f'`{S.next}` 没访问过 → 是孩子，递归进去' if not S.used[S.next]
                                              else f'`{S.next}` 已访问过 → 是父亲，跳过'),
        'cost += self.dfs': '进入孩子 `{next}`：先算它的子树要花多少，==回来再累加==到 `cost`',
        'if cost > 0 or hasApple': _cap_if,
        'return cost + 2': '节点 `{now}`：`cost + 2 = {cost} + 2 =` =={ret}==：==一来一去==，往返各 1 点',
        'return 0': '`{now}` 的子树里没有苹果 → 返回 `0`，==这个节点不用走进来==',
        'return res': '`dfs(0)` 把根的「往返 2」也算上了，减掉就是答案：`res` 就是 =={res}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='子树里有苹果才走进去，进去就是一个来回：2 点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树有 `n` 个节点，根是 `0`，每条边走一次花 1 秒；`hasApple[i]` 表示节点 `i` 有没有苹果',
                 '从根出发，收集所有苹果后==回到根==，最少花多少秒',
                 '本视频：`n = 7`，苹果在 `2、4、5` → `8`'],
        quote='对于树中的一个节点而言，只有当这个节点上有苹果，或者其子树中有苹果时才有必要走到这个节点上。如果有必要走到这个节点，那么需要一来一去两点代价。',
        quote_src='—— yiduobo 题解',
        idea=['dfs 返回「走进 now 子树并回到 now 的父亲」的代价',
              '先把孩子们的代价加成 `cost`；`cost > 0` 或自己有苹果就要走进来，返回 `cost + 2`',
              '否则返回 `0`；根没有父亲、不用「回来」，最后要减 `2`'],
        result='运行结束，返回 `8`：走过的边是 `0-1, 1-4, 1-5, 0-2`，各走两遍',
        summary=['时间 `O(n)`，空间 `O(n)`（邻接表 + 递归栈）',
                 '易错：根节点不需要往返，最后==减 2==；只有一个节点（或没有苹果）时用 `max(…, 0)` 兜底为 0',
                 '`used` 数组用来避免走回父亲；无向树没有环，所以不需要回溯清除',
                 '原文已是 Python 3 可运行的写法，代码未做改动'],
    ),
)
