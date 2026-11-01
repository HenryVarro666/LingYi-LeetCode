PARENTS = [-1, 2, 0, 2, 0]
NN = len(PARENTS)
CH = {v: [] for v in range(NN)}
for _w in range(1, NN):
    CH[PARENTS[_w]].append(_w)
PRE = []


def _pre(v):
    PRE.append(v)
    for c in CH[v]:
        _pre(c)


_pre(0)
SZ, SC = {}, {}


def _sz(v):
    s = sc = 1
    for c in CH[v]:
        t = _sz(c)
        s += t
        sc *= t
    SZ[v] = s
    SC[v] = sc * (NN - s if v > 0 else 1)
    return s


_sz(0)
DEPTH = {0: 0}
for _v in PRE[1:]:
    DEPTH[_v] = DEPTH[PARENTS[_v]] + 1
XP = {}
_leaf = [0]


def _xp(v):
    if not CH[v]:
        XP[v] = _leaf[0]
        _leaf[0] += 1
    else:
        for c in CH[v]:
            _xp(c)
        XP[v] = (XP[CH[v][0]] + XP[CH[v][-1]]) / 2


_xp(0)


def _sub(x):
    out = {x}
    for c in CH[x]:
        out |= _sub(c)
    return out


def _state(S, B):
    inner = S['_inner']
    v = inner.get('now')
    line = S.get('_line', 0)
    if v is None:
        return None, set(), set(), False
    anc = set()
    x = v
    while x > 0:
        x = PARENTS[x]
        anc.add(x)
    fin = {x for x in range(NN) if PRE.index(x) < PRE.index(v) and x not in anc}
    kids = CH[v]
    w = inner.get('child')
    if line >= 29:
        part = kids
    elif w is not None and line == 24 and ((B.get('_inner') or {}).get('child') == w):
        part = kids
    elif w is not None and line in (26, 27):
        part = kids[:kids.index(w) + 1]
    elif w is not None and line in (24, 25):
        part = kids[:kids.index(w)]
    else:
        part = []
    for c in part:
        fin |= _sub(c)
    return v, anc, fin, line >= 32


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    v, anc, fin, scored = _state(S, B)
    cv.text((x0 + 18, y0 + 4), '橙 = 当前，蓝 = 祖先，绿 = 已返回（附 score）', 22, T['muted'], bold=True)
    nl = max(XP.values()) + 1
    md = max(DEPTH.values()) + 1
    W = x1 - x0 - 80
    sp = min(150, W / nl)
    dy = min(120, (y1 - y0 - 110) / md)
    rad = 26
    sx = x0 + 40 + (W - sp * nl) / 2 + sp / 2
    pos = {k: (sx + XP[k] * sp, y0 + 70 + DEPTH[k] * dy + rad) for k in range(NN)}
    for k in range(1, NN):
        cv.line([pos[PARENTS[k]], pos[k]], T['border'], 3)
    for k in range(NN):
        X, Y = pos[k]
        if k == v:
            fill, ol = T['orange'], T['yellow']
        elif k in fin:
            fill, ol = T['green'], T['border']
        elif k in anc:
            fill, ol = T['blue'], T['border']
        else:
            fill, ol = T['panel2'], T['border']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=ol, width=3)
        cv.text((X, Y), k, 26, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        if k in fin or (k == v and scored):
            cv.text((X, Y + rad + 8), f'score {SC[k]}', 20, T['green'], anchor='mt', bold=True)


def _cap_loop(S, B, ret):
    i = S['_inner']
    now, c = i['now'], i.get('child')
    if (B.get('_inner') or {}).get('child') == c and c is not None:
        return f'`{now}` 的孩子都处理完了 → 循环结束，下面看有没有「剩下那块」'
    return f'取 `{now}` 的下一个孩子 `child = {c}`，先递归算它的子树大小'


def _cap_cnt(S, B, ret):
    i = S['_inner']
    return (f'孩子 `{i["child"]}` 的子树有 `child_cnt = {i["child_cnt"]}` 个点：'
            f'`cnt` 累加成 `{i["cnt"]}`')


def _cap_mul(S, B, ret):
    i = S['_inner']
    return f'去掉 `{i["now"]}` 后这棵孩子子树是独立一块：`score *= {i["child_cnt"]}` → `{i["score"]}`'


def _cap_n(S, B, ret):
    i = S['_inner']
    return (f'`n != cnt`（{S.n} != {i["cnt"]}）→ ==不是根==，还剩 `n - cnt = {S.n - i["cnt"]}` 个点成一块，'
            f'`score` → =={i["score"]}==')


def _cap_gt(S, B, ret):
    sc = S['_inner']['score']
    mx = S.get('self.max_score')
    return (f'`score = {sc}` 比最高分 `{mx}` 大 → 创下新纪录' if sc > mx
            else f'`score = {sc}` 没超过最高分 `{mx}` → 不是新纪录')


CONFIG = dict(
    num=2049, title='统计最高分的节点数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='一趟 DFS · 子树大小与剩余部分',
    tags=['灵神题单·链表树与回溯', '难度分 1912'],
    code='''
class Solution(object):
    def countHighestScoreNodes(self, parents):
        n = len(parents)
        self.max_score = 0
        self.res = 0

        childs = {}
        for index in range(1, n):
            fa = parents[index]
            if fa not in childs:
                childs[fa] = set()
            childs[fa].add(index)

        self.dfs(0, childs, n)
        return self.res

    def dfs(self, now, childs, n):
        if now not in childs:
            cnt = 1
            score = n - 1
        else:
            cnt = 1
            score = 1
            for child in childs[now]:
                child_cnt = self.dfs(child, childs, n)
                cnt += child_cnt
                score *= child_cnt
        
            if n != cnt:
                score *= (n - cnt)
        
        if score > self.max_score:
            self.res = 1
            self.max_score = score
        elif score == self.max_score:
            self.res += 1

        return cnt
''',
    call='Solution().countHighestScoreNodes([-1, 2, 0, 2, 0])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=170, hide=('childs',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('cnt', lambda S: S['_inner'].get('cnt')),
           ('score', lambda S: S['_inner'].get('score'), 'yellow'), ('max_score', 'self.max_score', 'orange'), ('res', 'self.res', 'green')],
    skip=['n = len', 'self.max_score = 0', 'self.res = 0', 'childs = {}', 'for index in range', 'fa = parents', 'if fa not in', 'childs[fa] = set()', 'cnt += child_cnt', 'self.dfs(0, childs, n)', 'cnt = 1', 'score = 1', 'self.max_score = score'],
    captions={
        'childs[fa].add': '建孩子表：`{index}` 的父亲是 `{fa}` → `childs = {childs}`',
        'if now not in childs': lambda S, B, ret: (f'`{B.now}` 不在 `childs` 里 → ==叶子==，没有孩子' if B.now not in B.childs else f'`{B.now}` 有孩子 → 先递归算它们的子树大小'),
        20: '叶子：删掉它后，其余 `n - 1 = {score}` 个点连成一块 → `score = {score}`',
        24: _cap_loop,
        'child_cnt = self.dfs': '递归求孩子 `{child}` 的子树大小 `child_cnt`',
        'score *= child_cnt': _cap_mul,
        'if n != cnt': lambda S, B, ret: (f'`n != cnt`（{S.n} != {S["_inner"]["cnt"]}）' + ('→ 不是根，要补「剩下那块」' if S.n != S['_inner']['cnt'] else '→ 相等，说明这就是根，没有剩下那块')),
        'score *= (n - cnt)': _cap_n,
        'if score > self.max_score': _cap_gt,
        'self.res = 1': lambda S, B, ret: f'刷新最高分为 `{S["_inner"]["score"]}`，`res` 重置为 `1`',
        'elif score == self.max_score': lambda S, B, ret: ('`score` 等于最高分 → 并列，`res` 加 1' if S['_inner']['score'] == S.get('self.max_score') else '`score` 小于最高分 → 什么也不做'),
        'self.res += 1': lambda S, B, ret: f'并列最高：`res` → {S.get("self.res")}',
        'return cnt': '返回子树大小 `{ret}` 给父节点去乘',
    },
    cards=dict(
        one_liner='删一个点，剩下三块：左子树、右子树、其余部分',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['根为 `0` 的二叉树，`parents[i]` 是 `i` 的父节点',
                 '删去一个节点后，==分数 = 剩下各非空子树大小之积==',
                 '返回最高分节点的个数。示例 `[-1,2,0,2,0]` → `3`'],
        quote='去除其他任意节点都会有上面提到的剩余的其他节点构成的子树。',
        quote_src='—— yiduobo 题解',
        idea=['对每个点，剩下的最多是左子树、右子树，以及「其余节点」这三块',
              '总节点数 `n` 已知，子树大小 `cnt` 自底向上算，其余部分就是 `n - cnt`',
              '叶子特殊：没有孩子，`score = n - 1`；根没有「其余部分」，用 `n != cnt` 判断'],
        result='运行结束，返回 `3`：节点 1、3、4 并列最高分 4',
        summary=['时间 `O(n)`：每个节点处理一次；空间 `O(n)`（`childs` 和递归栈）',
                 '易错：根的 `cnt == n`，不能再乘 `n - cnt = 0`，所以要 `if n != cnt`',
                 '易错：叶子的分数是 `n - 1`，不是 1',
                 '对照灵神：他把叶子并进统一循环，用 `v > 0` 判断根；这里把叶子单独拿出来写'],
    ),
)
