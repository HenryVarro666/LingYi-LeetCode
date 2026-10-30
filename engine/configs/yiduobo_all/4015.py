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
LV = {0: 1}
for _i in range(1, N):
    LV[_i] = LV[PARENT[_i]] + 1


def _draw(cv, S, B, box, T):
    q = S.get('q') or []
    head, tail = S.get('head', 0), S.get('tail', 0)
    cur = S.get('x') if 'x' in S and S.get('_line', 0) and head < tail else None
    layer = set(q[head:tail]) if 'head' in S and 'd' in S and S['d'] > 0 else set()
    badge = {u: f'层 {LV[u]}' for u in q}
    _gtree(cv, T, box, CH, 0, cur, hl=layer - {cur}, badge=badge, sub={u: f'v={NUMS[u]}' for u in range(N)},
           title='树（旁边 v = nums[i]；青色 = 当前这一层，绿框 = 层号 = 深度 d）')


def _form(S):
    if 's' not in S:
        return '目标：`Σ nums[u]·(h − d[u] + 1)` 拆开 = `(h+1)·Σ nums − Σ nums[u]·d[u]`'
    return f"`s = Σ nums[u]·d[u]` = =={S['s']}==，当前层 `d = {S['d']}`；最后 `(d+1)·sum(nums) − s`"


CODE = '''
class Solution(object):
    def weightedSum(self, parent, nums):
        
        n = len(parent)
        g = [[] for _ in range(n)]
        for x, p in enumerate(parent[1:], 1):
            g[p].append(x)
        
        s = 0
        d = 0
        q = [0]
        head, tail = 0, 1
        while head < tail:
            d += 1
            for x in q[head : tail]:
                s += nums[x] * d
                for y in g[x]:
                    q.append(y)
            
            head, tail = tail, len(q)
        
        return (d + 1) * sum(nums) - s
'''

CONFIG = dict(
    num=4015, title='树的加权和', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='公式变形 + BFS 按层累加深度',
    tags=['链表树与回溯', '难度分 1534'],
    code=CODE,
    call='Solution().weightedSum([-1,0,0,0,2,2], [5,2,3,1,4,6])',
    expect=37,
    views=[
        dict(type='text', fn=_form, size=24, h=70),
        dict(type='custom', draw=_draw, h=280),
        dict(type='array', var='q', label='队列 q（head..tail = 当前这一层）', cell=64, h=140,
             pointers={'head': 'blue', 'tail': 'pink'}),
    ],
    watch=[('d', 'd', 'yellow'), ('x', 'x', 'blue'), ('s', 's', 'green'), ('head', 'head', 'cyan'), ('tail', 'tail', 'pink')],
    captions={
        'n = len(parent)': '`n = {n}`，先根据 `parent` 建树',
        'g[p].append(x)': '`{x}` 的父亲是 `{p}` → `g[{p}] = {g[p]}`',
        's = 0': '`s` 累加每个节点的 `nums[x] * d`，也就是公式里被减掉的那一半',
        'd = 0': '`d` 是当前层的深度，进入每层前先 `+1`，根是第 1 层',
        'q = [0]': '队列从根节点 `0` 开始',
        'head, tail = 0, 1': '`q[head:tail]` 是当前层：此时只有根',
        'while head < tail': lambda S, B, r: ('当前层还有节点 → 继续按层处理' if S['head'] < S['tail'] else '队列空了：所有层都处理完，此时 `d` 就是树高 `h`'),
        'd += 1': '进入新的一层：`d = {d}`，这一层的节点深度都是 `{d}`',
        'for x in q[head : tail]': lambda S, B, r: (f"处理当前层的节点 `{S['x']}`（深度 `{S['d']}`）" if S['x'] != B.get('x') else '这一层的节点都处理完了'),
        's += nums[x] * d': '`s += nums[{x}] * d = {nums[x]} × {d}` → ==s = {s}==',
        'q.append(y)': '孩子 `{y}` 排进队尾，它属于下一层',
        'head, tail = tail, len(q)': '这一层处理完：新的一层是 `q[{head}:{tail}]` = `{q[head:tail]}`',
        'return': '`h = d = {d}`，`(h+1) × sum(nums) − s` = `{d + 1} × {sum(nums)} − {s}` = =={ret}==',
    },
    skip=['for x, p in enumerate'],
    max_steps=80,
    cards=dict(
        one_liner='先拆公式：`(h+1)·Σnums − Σ nums·d`，BFS 按层数深度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`parent` 描述以 `0` 为根的树，`nums[i]` 是节点 `i` 的值',
                 '深度为 `d` 的节点权重是 `nums[i] * (h - d + 1)`，`h` 是树高，根深度为 1',
                 '求所有节点权重之和',
                 '示例：`parent = [-1,0,0,0,2,2]`，`nums = [5,2,3,1,4,6]` → `37`'],
        quote='将h + 1和d分离，……前半部分就是nums之和乘以h + 1，而后半部分则是每个节点的节点值乘以其对应的深度，此时就可以先通过parent建树，然后从根节点向下一次bfs计算出这个加和。',
        quote_src='—— yiduobo 题解原文',
        idea=['把权重拆成两部分：`nums[u]·(h+1)` 减去 `nums[u]·d[u]`',
              '第一部分是 `(h+1) × sum(nums)`；第二部分要每个点的深度',
              '用 BFS：同一轮的节点深度相同，`d` 每轮加一，最后循环结束时的 `d` 正好是树高 `h`'],
        result='BFS 结束 `d = 3`，`s = 47` → `4 × 21 − 47 = 37`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`h` 不用单独求：BFS 的轮数就是树高',
                 '易错：`d` 在每轮开头先加一，根是第 1 层，和题目的深度定义一致',
                 '对比灵神：灵神 DFS 存 `depth` 再 `h - d` 求和；yiduobo 先代数变形，BFS 里只累加 `nums×d`',
                 '原文已是 Python 3 可运行的写法，未改动'],
    ),
)
