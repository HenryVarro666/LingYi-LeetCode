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

_VAL = {}   # 自底向上返回的乘积（只对 target 路径上的节点有意义）
_acc = 1
for _u in reversed(_AP):
    if _u != _TARGET:
        _acc *= _NC[_u]
    _VAL[_u] = _acc


def _lines():
    src = CONFIG['code'].strip('\n').split('\n')
    return {k: next(i + 1 for i, s in enumerate(src) if k in s) for k in ('for y in g[x]', 'if y != fa', 'if x == target')}


def _state(S):
    i = S['_inner']
    cur = i.get('x') if 'fa' in i else None
    st = {u: {} for u in _INFO.order}
    st[_TARGET]['mark'] = 'pink'
    if cur is None:
        if 'prod' in i and i['prod']:         # 回到最外层：全部回溯完毕
            for u in _AP:
                st[u].update(fill='green', badge=f'返回 {_VAL[u]}', bcolor='green')
        return st
    L = _lines()
    k = 0
    if 'y' in i and i['y'] in _KIDS.get(cur, []):
        k = _KIDS[cur].index(i['y']) + (0 if S['_line'] in (L['for y in g[x]'], L['if y != fa']) else 1)
    p, done = _INFO.phase(cur, k)
    found = bool(i.get('prod')) or (cur == _TARGET and S['_line'] == L['if x == target'])
    for u in _INFO.order:
        d = st[u]
        if found and u in _AP and _INFO.depth[u] >= _INFO.depth[cur]:
            d.update(fill='green', badge=f'返回 {_VAL[u]}', bcolor='green')
            if u in p:
                d.update(outline='yellow', edge='yellow')
        elif u in p:
            d.update(outline='yellow', edge='yellow', badge=f'left_t={_T - _INFO.depth[u]}', bcolor='yellow')
            if u == cur:
                d['ptr'] = 'x'
        elif u in done:
            d.update(fill='red', badge='返回 0', bcolor='red')
    return st


def _info(S):
    i = S['_inner']
    if 'x' not in i or 'fa' not in i:
        return '粉点 = target；绿 = 找到 target 的路径，红 = 这棵子树里没有 target'
    x = i['x']
    c = len(_KIDS.get(x, []))
    if c == 0:
        return f'节点 `{x}` 没有儿子（`len(g[{x}]) = 1`，只有虚拟父亲或父节点）'
    return f'节点 `{x}` 有 `{c}` 个儿子 → 跳到每个儿子的概率都是 `1/{c}`；乘上儿子个数 `{c}` 就是在乘分母'


def _cap_zero(S, B, ret):
    if ret is None:
        return f'`left_t = {S.left_t}` > 0：时间没用完，青蛙还能继续跳'
    return f'`left_t = 0`：t 秒用完了，青蛙必须恰好在 target → 节点 `{S.x}` {"就是" if ret else "不是"} target，返回 `{ret}`'


def _cap_tar(S, B, ret):
    if ret is None:
        return f'节点 `{S.x}` 不是 target → 继续往儿子里找'
    if ret:
        return f'到达 target `{S.x}`，还剩 `left_t = {S.left_t}` 秒：它是==叶子==（`len(g[x]) == 1`），青蛙停在原地 → 返回 `True`'
    return f'到达 target `{S.x}`，但还剩 `left_t = {S.left_t}` 秒且它有儿子：青蛙会==跳走== → 概率 0，返回 `False`'


def _cap_prod(S, B, ret):
    if ret:
        return (f'儿子 `{B.y}` 里找到了 target，返回 `{B.prod}`；乘上 `{B.x}` 的儿子数 `{len(B.g[B.x]) - 1}` → =={ret}==，'
                f'==直接返回，不再看别的儿子==')
    return f'儿子 `{B.y}` 的子树里没有 target（返回 `0`）→ 继续看下一个儿子'


def _cap_fa(S, B, ret):
    if S.y == S.fa:
        return f'`y = {S.y}` 是父节点 `{S.fa}` → ==不能跳回去=='
    return f'`y = {S.y}` 是 `{S.x}` 的儿子 → 去那里找 target'


CONFIG = dict(
    num=1377, title='T 秒后青蛙的位置', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 自底向上 · 只乘分母',
    tags=['灵神题单', '链表树与回溯', '难度分 1824'],
    code='''
class Solution:
    def frogPosition(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        g = [[] for _ in range(n + 1)]
        g[1] = [0]  # 减少额外判断的小技巧
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建树

        def dfs(x: int, fa: int, left_t: int) -> int:
            # t 秒后必须在 target（恰好到达，或者 target 是叶子停在原地）
            if left_t == 0: return x == target
            if x == target: return len(g[x]) == 1
            for y in g[x]:  # 遍历 x 的儿子 y
                if y != fa:  # y 不能是父节点
                    prod = dfs(y, x, left_t - 1)  # 寻找 target
                    if prod: return prod * (len(g[x]) - 1)  # 乘上儿子个数，并直接返回
            return 0  # 未找到 target

        prod = dfs(1, 0, t)
        return 1 / prod if prod else 0
''',
    call='Solution().frogPosition(7, [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], 3, 5)',
    expect=1 / 3,
    views=[
        dict(type='custom', draw=make_draw(_INFO, _state, '树（黄 = 递归路径，绿 = 找到，红 = 没有 target）', '粉点 = target'), h=340),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='calls', h=200),
    ],
    watch=[('x', lambda S: S['_inner'].get('x') if 'fa' in S['_inner'] else None, 'blue'),
           ('left_t', lambda S: S['_inner'].get('left_t'), 'yellow'),
           ('prod', lambda S: S['_inner'].get('prod'), 'pink')],
    skip=['g[x].append(y)', 'g[y].append(x)', 'for y in g[x]', 'n + 1)]'],
    captions={
        'g[1] = [0]': '给节点 `1` 加一个虚拟邻居 `0`：这样==每个节点的儿子数都是 `len(g[x]) - 1`==，根也一样，还不用特判 `n = 1`',
        'for x, y in edges': lambda S, B, r: (f'边 `({S.x}, {S.y})`：无向边，两个端点互相加入邻接表' if S.x != B.get('x') or S.y != B.get('y')
                                              else '建树完成：`g[x]` 里除了父节点，剩下的都是儿子'),
        'if left_t == 0': _cap_zero,
        'if x == target': _cap_tar,
        'if y != fa': _cap_fa,
        'prod = dfs(y, x': '跳到儿子 `{y}`，剩余时间 `left_t - 1 = {B.left_t - 1}`',
        'if prod: return': _cap_prod,
        'return 0': '`{x}` 的所有儿子里都没有 target → 返回 `0`',
        'prod = dfs(1, 0, t)': '从根 `1` 出发，剩余 `t = {t}` 秒；`fa = 0` 是虚拟父亲',
        'return 1 / prod': lambda S, B, r: (f'`prod = {S.prod}` 是路径上==分母的乘积==，概率是倒数 `1 / {S.prod}` = =={r}==' if S.prod
                                            else '`prod = 0`：到不了 target → 概率 `0`'),
    },
    max_steps=70,
    cards=dict(
        one_liner='青蛙一路往下，每步概率是 1/儿子数：只把分母乘起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树 `n` 个顶点，青蛙从顶点 `1` 出发，每秒等概率跳到一个==未访问==的相邻顶点',
                 '没有可跳的顶点时，青蛙留在原地',
                 '求 `t` 秒后青蛙在 `target` 的概率',
                 '本视频：`n = 7, t = 3, target = 5` → `1/3`'],
        quote='既然答案是由若干分子为 1 的分数相乘得到，那么干脆只把分母相乘，最后再计算一下倒数，就可以避免因浮点乘法导致的精度丢失了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['青蛙只能一路向下：跳进不含 `target` 的子树就回不来了',
              '`dfs(x, fa, left_t)` 找 `target`：恰好第 `t` 秒到，或提前到且 `target` 是叶子（留在原地）',
              '自底向上：找到后在「归」的过程中乘上每层的儿子数；没找到返回 `0`',
              '最后 `1 / prod`：只在找到之后才做乘法，没有盲目计算'],
        result='运行结束，返回 `1/3`：路径 `1 → 3 → 5`，只有第一步有 3 个儿子可选',
        summary=['时间 `O(n)`，空间 `O(n)`；乘积用整数存，最后取倒数，避免浮点误差',
                 '节点 `1` 加虚拟邻居 `0`，==儿子数统一为 `len(g[x]) - 1`==，也不用特判 `n = 1`',
                 '易错：到达 `target` 时若还有剩余时间，必须 `target` 是叶子才算（否则青蛙已跳走）',
                 '另一种写法是自顶向下：边「递」边乘儿子数，找到再记 `ans = 1 / prod`；会在不含 `target` 的子树里白乘',
                 '乘积最大约 `3^33`，超出 32 位整数；Python 没有溢出问题，其他语言要用 64 位'],
    ),
)
