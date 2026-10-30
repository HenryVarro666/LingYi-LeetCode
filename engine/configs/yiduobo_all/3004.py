def _layout_tree(n, edges, root=0):
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)
    pos, nxt = {}, [0]

    def go(x, fa, d):
        ch = [y for y in g[x] if y != fa]
        if not ch:
            pos[x] = (nxt[0], d)
            nxt[0] += 1
        else:
            for y in ch:
                go(y, x, d + 1)
            pos[x] = (sum(pos[y][0] for y in ch) / len(ch), d)
    go(root, -1, 0)
    return pos, nxt[0], max(d for _, d in pos.values()) + 1


def _draw_tree(cv, box, T, n, edges, fill, sub, ring=None, title='', subcolor='muted', inner=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    pos, w, h = _layout_tree(n, edges)
    sp = min(170, (x1 - x0 - 60) / max(1, w))
    R = max(18, min(28, sp * 0.36))
    dy = min(120, (y1 - y0 - 70 - 2 * R - 40) / max(1, h - 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * w) / 2 + sp / 2
    P = {k: (sx + a * sp, y0 + 60 + R + d * dy) for k, (a, d) in pos.items()}
    for a, b in edges:
        (ax, ay), (bx, by) = P[a], P[b]
        if pos[a][1] > pos[b][1]:
            (ax, ay), (bx, by) = (bx, by), (ax, ay)
        cv.line([(ax, ay), (bx, by)], T['dim'], 3)
    for k, (cx, cy) in P.items():
        c = fill.get(k)
        cv.rect((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'], outline=T['yellow'] if k == ring else T['border'],
                width=5 if k == ring else 3, r=R)
        cv.text((cx, cy), k, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        s = sub.get(k)
        if s not in (None, ''):
            tw = cv.tlen(s, 21, bold=True) + 10
            cv.rect((cx - tw / 2, cy + R + 4, cx + tw / 2, cy + R + 32), fill=T['panel'], r=6)
            cv.text((cx, cy + R + 8), s, 21, T[subcolor], anchor='mt', bold=True)


SNAP = {}
DONE = {}


def trk(fn=None, rec=None, reset=False):
    """caption wrapper: remember which nodes have returned (node -> returned value), keyed by this step's innermost-locals object"""
    def cap(S, B, ret):
        if reset:
            DONE.clear()
        if rec is not None:
            kv = rec(S, B, ret)
            if kv is not None:
                DONE[kv[0]] = kv[1]
        SNAP[id(S['_inner'])] = dict(DONE)
        return fn(S, B, ret) if callable(fn) else None
    return cap


def _done(S):
    return SNAP.get(id(S['_inner']), {})


def fill_caps(code, caps):
    """give every other statement line a tracking (default-text) caption"""
    out = dict(caps)
    for l in code.strip('\n').split('\n'):
        s = l.strip()
        if not s or s.startswith(('def ', 'class ', '#')) or any(k in l for k in out):
            continue
        out[s] = trk()
    return out
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]]
COLORS = [1, 1, 1, 1, 2, 1, 1]
PAL = {1: 'blue', 2: 'orange', 3: 'green'}


def _res(S):
    d = _done(S)
    return max([0] + list(d.values()))


def _draw(cv, S, B, box, T):
    colors = S.get('colors')
    if colors is None:
        return
    done, cur = _done(S), S['_inner'].get('now')
    fill = {i: PAL.get(c, 'purple') for i, c in enumerate(colors)}
    sub = {i: f'颜色 {c}' + (f' → {done[i]}' if i in done else '') for i, c in enumerate(colors)}
    if cur is not None and cur not in done:
        sub[cur] += f'  cnt={S["_inner"].get("cnt")}'
    _draw_tree(cv, box, T, len(colors), EDGES, fill, sub, ring=cur,
               title='树（填充色 = 节点颜色；下方：颜色 → dfs 返回值，-1 表示不是同色子树）')


def _info(S):
    if 'colors' not in S:
        return ''
    return f'全局 `res`（最大同色子树大小）= =={_res(S)}=='


CODE = '''
class Solution(object):
    def maximumSubtreeSize(self, edges, colors):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        

        def dfs(now, fa):
            cnt = 1

            for son in g.get(now, set()):
                if son != fa:
                    son_cnt = dfs(son, now)
                    if colors[son] == colors[now]:
                        if son_cnt == -1:
                            cnt = -1
                        elif cnt != -1:
                            cnt += son_cnt
                    else:
                        cnt = -1
            
            
            global res
            res = max(res, cnt)

            return cnt
        

        global res
        res = 0
        dfs(0, -1)
        return res
'''


def _cap_cnt(S, B, r):
    p = S['_inner']
    if S.colors[S.son] != S.colors[S.now]:
        return f'孩子 `{S.son}` 颜色 {S.colors[S.son]} ≠ 本节点颜色 {S.colors[S.now]} → 本节点不是同色子树：`cnt = -1`'
    return f'孩子那棵不是同色子树（返回 `-1`）→ 本节点也不是：`cnt = -1`'


CAPS = {
    'g = {}': trk(lambda S, B, r: '`g`：邻接表，每个点对应一个邻居集合（按 `edges` 建好，下面几行省略）', reset=True),
    'res = 0': trk(lambda S, B, r: '`res`：全局的最大同色子树节点数'),
    'dfs(0, -1)': trk(lambda S, B, r: '从根 `0` 向下递归'),
    'cnt = 1': trk(lambda S, B, r: f'进入节点 `{S.now}`（颜色 {S.colors[S.now]}）：先把自己当成一棵同色子树，`cnt = 1`'),
    'for son in g.get': trk(lambda S, B, r: (f'下一个邻居 `{S.son}`' + ('，是父节点 → 跳过' if S.son == S.fa else '，是孩子 → 递归')
                                              if S['_inner'].get('son') != B['_inner'].get('son') else
                                              f'`{S.now}` 的孩子都处理完了，`cnt = {S.cnt}`')),
    'son_cnt = dfs': trk(lambda S, B, r: f'递归孩子 `{B.son}`：返回它子树的大小，==-1 表示它那棵不是同色子树=='),
    'if colors[son] == colors[now]': trk(lambda S, B, r: f'孩子 `{S.son}` 颜色 {S.colors[S.son]}，本节点颜色 {S.colors[S.now]} → ' +
                                         ('同色，再看孩子那棵是不是同色子树' if S.colors[S.son] == S.colors[S.now] else '==颜色不同，本节点不可能是同色子树==')),
    'if son_cnt == -1': trk(lambda S, B, r: f'`son_cnt = {S.son_cnt}` ' + ('== -1：孩子那棵不是同色子树' if S.son_cnt == -1 else '≠ -1：孩子那棵是同色子树')),
    'cnt = -1': trk(_cap_cnt),
    'elif cnt != -1': trk(lambda S, B, r: f'`cnt = {S.cnt}` ' + ('≠ -1：本节点目前仍是同色子树 → 可以并入孩子' if S.cnt != -1 else '== -1：本节点已经不行了，不再累加')),
    'cnt += son_cnt': trk(lambda S, B, r: f'同色且孩子也是同色子树 → 节点数累加：`cnt = {B.cnt} + {S.son_cnt} = {S.cnt}`'),
    'res = max(res, cnt)': trk(lambda S, B, r: f'`res = max(res, {S.cnt})` → =={_res(S)}==（`-1` 不会更新 `res`）', rec=lambda S, B, r: (S.now, S.cnt)),
    'return cnt': trk(lambda S, B, r: f'节点 `{S.now}` 返回 `{r}`：' + ('它是一棵同色子树，大小 ' + str(r) if r != -1 else '不是同色子树，告诉父节点')),
    'return res': trk(lambda S, B, r: f'最大的同色子树有 `{r}` 个节点'),
}
CONFIG = dict(
    num=3004, title='相同颜色的最大子树', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='自底向上 DFS · -1 表示不同色', tags=['灵神题单·链表树与回溯'],
    code=CODE,
    call=f'Solution().maximumSubtreeSize({EDGES}, {COLORS})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=390),
        dict(type='text', fn=_info, h=50),
        dict(type='calls', h=150),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('cnt', lambda S: S['_inner'].get('cnt')), ('res', lambda S: _res(S) if 'colors' in S else None, 'green')],
    captions=fill_caps(CODE, CAPS),
    skip=['for x, y in edges', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()', 'g[x].add', 'g[y].add', 'if son != fa'],
    max_steps=120,
    cards=dict(
        one_liner='孩子同色且自己也是同色子树，才把节点数累加上来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，根为 `0`，`colors[i]` 是节点 `i` 的颜色',
                 '子树里所有节点颜色都相同，就叫 ==同色子树==；求最大同色子树的节点数',
                 '本视频：`colors=[1,1,1,1,2,1,1]`，树 `0-1, 0-2, 1-3, 1-4, 2-5, 2-6` → `3`'],
        quote='以now为根节点的子树而言，其为同色子树的条件为：1、now为叶子节点 2、now不是叶子节点，且now的所有子节点的颜色与now相同，同时以now的所有子节点为根节点的子树，也是同色子树',
        quote_src='—— yiduobo 题解原文',
        idea=['递归返回子树大小；==返回 -1 表示这棵不是同色子树==',
              '遍历孩子：颜色不同，或孩子返回 `-1`，当前就置 `cnt = -1`',
              '否则把孩子的节点数累加到 `cnt`；每个节点都用 `cnt` 更新全局 `res`'],
        result='节点 1 因为孩子 4 颜色不同返回 -1，根被拖累；节点 2 的子树 3 个节点同色，答案 3',
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '易错：一旦 `cnt = -1` 就不能再累加（`elif cnt != -1`），否则会把 `-1` 加回去',
                 '`res` 是全局变量，函数里要先声明 `global res`；`-1` 不会改变 `res`',
                 '原文是 Python 2 风格，但在 Python 3 下可直接运行，代码没有修改'],
    ),
)
