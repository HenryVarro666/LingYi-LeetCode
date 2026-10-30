import math as _math


def _gdraw(cv, T, box, title, pos, edges, color_of, sub_of=None, ecolor_of=None, R=26):
    """有向图：pos = [(fx, fy)]（0~1 的相对位置），edges = [(a, b)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 100, y1 - y0 - 110
    P = [(x0 + 50 + fx * Wd, y0 + 60 + fy * Hd) for fx, fy in pos]
    es = set(edges)
    for a, b in edges:
        ec = (ecolor_of(a, b) if ecolor_of else None) or 'dim'
        col = T[ec] if isinstance(ec, str) else ec
        (xa, ya), (xb, yb) = P[a], P[b]
        if a == b:
            cv.arc_arrow((xa - 12, ya - R + 2), (xa + 12, ya - R + 2), 46, col, 3, 11)
            continue
        dx, dy = xb - xa, yb - ya
        L = _math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        off = 9 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        cv.arrow((xa + ux * (R + 3) + nx, ya + uy * (R + 3) + ny), (xb - ux * (R + 6) + nx, yb - uy * (R + 6) + ny), col, 3, 12)
    for i, (x, y) in enumerate(P):
        c = color_of(i)
        fill = T[c] if isinstance(c, str) else (c or T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
        cv.text((x, y), i, 26, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        if sub_of:
            s = sub_of(i)
            if s:
                cv.text((x, y + R + 6), s, 19, T['text'], anchor='mt', mono=True)
    return P


REC = [1, 2, 0, 0, 3]
K = 4
_N = len(REC)
POS = [(0.62, 0.8), (0.88, 0.8), (0.75, 0.15), (0.34, 0.8), (0.06, 0.8)]


def _ring_of(S):
    return set(v for c in S.get('circle_list', []) for v in c)


def _col(S, i):
    if 'circle_list' not in S:
        return None
    ring = _ring_of(S)
    if 'prefix_s' in S and 'now' in S:
        if i == S['now']:
            return 'pink'
    elif 'q' in S and S['q']:
        if i == S['q'][-1]:
            return 'pink'
        if i in S['q']:
            return 'yellow'
    if i in ring:
        return 'cyan'
    if i in S.get('g', {}):
        return 'orange'
    return None


def _draw(cv, S, B, box, T):
    r = S['receiver']
    _gdraw(cv, T, box, 'i → receiver[i]（青 = 环，橙 = 树枝，粉 = 当前点，黄 = 走过的路径）', POS,
           [(i, r[i]) for i in range(_N)], lambda i: _col(S, i))


def _ring_txt(S):
    if 'circle_list' not in S or not S['circle_list']:
        return '还没找到环'
    return '环 `circle_list` = ' + str(S['circle_list']) + '    环前缀和 `s_circle` = ' + str(S['s_circle'])


def _cap_walk(S, B, ret):
    last = S.q[-1]
    if last in S.g:
        return f'走到 `{last}`：它已经挂在构造好的树里 → 当前路径就是那棵树的一枝，直接==拼上去=='
    if last in S.vis:
        return f'走到 `{last}`：本次路径里出现过 → ==这两次出现之间就是一个环=='
    return f'走到 `{last}`：没见过 → 继续沿 receiver 往前走'


def _cap_dfs_t(S, B, ret):
    return f'`t = k + 1 = {S.t}`：起点本身也算一个接触的人，要数 {S.t} 个人的编号和'


def _cap_tree(S, B, ret):
    return f'这是树枝上的点：`prefix_s` 记录从树根（入环点）走到 `{S.now}` 的编号累加'


def _cap_len(S, B, ret):
    if len(B.prefix_s) == 0:
        return f'`prefix_s` 为空 → `{S.now}` 本身是环上的入环点，树里没有要累加的部分，只把自己放进 `prefix_s`'
    return f'`prefix_s` 不空 → `{S.now}` 在树枝上：累计和 = `{S.prefix_s[-1]} + {S.now}` = {S.prefix_s[-1] + S.now}，追加进 `prefix_s`'


def _cap_tless(S, B, ret):
    if B.t < len(S.prefix_s):
        return f'`t = {B.t}` < `len(prefix_s) = {len(S.prefix_s)}`：k 步走不到环，只在树枝上走 → 用前缀和相减'
    return f'`t = {B.t}` ≥ `len(prefix_s) = {len(S.prefix_s)}`：能走进环 → 先把树枝这一段全走完'


CONFIG = dict(
    num=2836, title='在传球游戏中最大化函数值', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='内向基环树 · 树 + 环 前缀和',
    tags=['灵神题单·图论算法', '灵神题单·链表树与回溯', '难度分 2769'],
    code='''
class Solution(object):
    def getMaxFunctionValue(self, receiver, k):

        circle_list = []
        s_circle = []
        g = {}

        for index in range(len(receiver)):
            if index not in g:
                q = [index]
                vis = set()
                while q[-1] not in g and q[-1] not in vis:
                    vis.add(q[-1])
                    q.append(receiver[q[-1]])
                
                if q[-1] not in g:
                    p = len(q) - 2
                    while q[p] != q[-1]:
                        p -= 1
                    
                    circle_list.append([])
                    for v in q[p : len(q) - 1]:
                        circle_list[-1].append(v)
                        g[v] = set()

                    s_circle.append([0])
                    for j in range(len(circle_list[-1])):
                        s_circle[-1].append(s_circle[-1][-1] + circle_list[-1][j])
                    for j in range(len(circle_list[-1])):
                        s_circle[-1].append(s_circle[-1][-1] + circle_list[-1][j])
                
                else:
                    p = len(q) - 1

                p -= 1
                while p >= 0:
                    g[q[p]] = set()
                    g[q[p + 1]].add(q[p])
                    p -= 1

        global res
        res = 0
        def dfs(now, prefix_s):
            t = k + 1
            v = 0
            if len(prefix_s) == 0:
                prefix_s.append(now)
            else:
                prefix_s.append(prefix_s[-1] + now)
                if t < len(prefix_s):
                    v = prefix_s[-1] - prefix_s[-t - 1]
                    t = 0
                else:
                    v = prefix_s[-1] - prefix_s[0]
                    t -= len(prefix_s) - 1
            
            rnd = t // len(circle_list[circle_id])
            t %= len(circle_list[circle_id])
            v += rnd * s_circle[circle_id][len(circle_list[circle_id])]
            v += s_circle[circle_id][circle_index + t] - s_circle[circle_id][circle_index]
        
            global res
            res = max(res, v)
            
            for child in g[now]:
                dfs(child, prefix_s)
            
            prefix_s.pop()

        for circle_id in range(len(circle_list)):
            for circle_index in range(len(circle_list[circle_id])):
                dfs(circle_list[circle_id][circle_index], [])

        return res
''',
    call=f'Solution().getMaxFunctionValue({REC}, {K})',
    expect=10,
    views=[
        dict(type='custom', draw=_draw, h=230),
        dict(type='text', fn=_ring_txt, h=70),
        dict(type='array', var=lambda S: (S['q'] if 'prefix_s' not in S else []), h=100, label='q（本次走过的路径）'),
        dict(type='array', var='prefix_s', h=130, label='prefix_s（树根到当前点的编号累计和）'),
    ],
    watch=[('t', 't', 'blue'), ('v', 'v', 'yellow')],
    skip=['circle_list = []', 's_circle = []', 'g = {}', 'vis.add', 'q.append(receiver', 'p -= 1', 'circle_list[-1].append', 'g[v] = set()',
          's_circle[-1].append', 'res = 0',
          'for v in q[p', 'for j in range(len(circle_list[-1])):', 'while q[p] != q[-1]', 'vis = set()', 'while p >= 0:',
          'for index in range', 'if index not in g', 'for circle_id', 'for circle_index', 'v = 0', 't %= len', 'else:', 'for child in g[now]', 'prefix_s.append(now)', 'prefix_s.append(prefix_s[-1] + now)', 'p = len(q)', 'p = len(q) - 2'],
    max_steps=56,
    captions={
        'q = [index]': '`{index}` 还没挂进任何树 → 从它出发一路沿 `receiver` 走，路径记在 `q`',
        'while q[-1] not in g': _cap_walk,
        'if q[-1] not in g': lambda S, B, r: ('路径末尾不在 `g`：它是本次路径里的重复点 → 末尾到上一次出现之间是新环' if S.q[-1] not in S.g
                                              else '路径末尾已在 `g` 里 → 这条路径只是挂在旧树上的一枝'),
        
        'circle_list.append([])': '倒着找到 `{q[-1]}` 上次出现的位置，`q[p:-1]` = {q[p:-1]} 就是一个环；每个点在 `g` 里建一个空的“儿子集合”',
        's_circle.append([0])': '给环做==复制两遍的前缀和==：环上走一圈以上也能用区间和 `s[b] - s[a]` 取',
        'g[q[p]] = set()': '路径上其余的点是树枝：`g[{q[p]}]` 建空集合',
        'g[q[p + 1]].add(q[p])': '树枝点 `{q[p]}` 挂到它的下一个点 `{q[p + 1]}` 的儿子里 → 树根在环上',
        'dfs(circle_list[circle_id][circle_index], [])': '从环上的点 `{circle_list[circle_id][circle_index]}` 向外 dfs 整棵树，树里每个点都是一个起点',
        't = k + 1': _cap_dfs_t,
        'if len(prefix_s) == 0': _cap_len,
        'if t < len(prefix_s)': _cap_tless,
        'v = prefix_s[-1] - prefix_s[-t - 1]': 'k 步不出树：`v = {prefix_s[-1]} - {prefix_s[-t - 1]}` = =={v}==（区间和 = 前缀和相减）',
        'v = prefix_s[-1] - prefix_s[0]': '树枝全走完：`v = {prefix_s[-1]} - {prefix_s[0]}` = =={v}==，走了 `{len(prefix_s) - 1}` 步',
        't -= len(prefix_s) - 1': '树里用掉 `{len(prefix_s) - 1}` 步，==还剩 `t = {t}` 个点==在环上走',
        'rnd = t': '环长 `{len(circle_list[circle_id])}`：剩下的 `t` 个点可以绕 `{rnd}` 整圈，再多走 `{t % len(circle_list[circle_id])}` 个',
        't %= len': '整圈绕完，余下 `t = {t}` 个点',
        'v += rnd *': '整圈贡献：`{rnd} × {s_circle[circle_id][len(circle_list[circle_id])]}`（环的编号和），`v` = {v}',
        'v += s_circle[circle_id][circle_index + t]': '余下部分在环上是一段区间和（环复制了两遍，所以不用取模）：`v` = =={v}==',
        'res = max(res, v)': '起点 `{now}` 的函数值 `v = {v}`：和全局最大值 `res` 比大小，留下较大的',
        'dfs(child, prefix_s)': '`{B.now}` 的儿子 `{child}` 也是起点：递归过去，沿用同一个 `prefix_s`',
        'prefix_s.pop()': '`{now}` 这棵子树处理完 → 回溯，弹出它的累计和',
        'return res': '全局最大值 `res` = =={ret}==',
    },
    cards=dict(
        one_liner='先造出“树 + 环”，再对每个点分三段算：树里走 + 绕整圈 + 环上余下',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`receiver[i]` 是 `i` 传球给的人，从 `x` 出发传 `k` 次',
                 '`f(x)` = `x` + 之后每个接球人的编号之和，求最大值（`k` 可达 10^10）',
                 '本视频：`receiver = [1,2,0,0,3]`，`k = 4` → `10`'],
        quote='传球路径在经过若干步之后一定会进入到某个环路中……每次传球都可以认为是先从起点在树中对应的节点开始向树根行走，走到树根后就意味着来到了环上，接下来可能要在这个环上走上几圈，最后再从这个入环点开始走完剩下的步数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把图拆成“环 + 挂在环上的树”：每个点走一遍，撞到旧点就拼树，撞到自己就成环',
              '每个起点分三段：==树里向根走==（前缀和相减）、==环上绕整圈==（圈数 × 环和）、==环上余下的几步==',
              '环的前缀和把数组复制两遍，区间和不用处理回绕'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`t = k + 1`：起点自己也要算进去，易错点',
                 '树枝上的 `dfs` 要共享 `prefix_s` 并在返回前 `pop`，否则路径会乱',
                 '原文为 Python 2 写法，`rnd = t / len(...)` 是整数除法，已改为 `//`',
                 '对比灵神：灵神用倍增 `O(n log k)`，yiduobo 的树 + 环做法是 `O(n)`'],
    ),
)
