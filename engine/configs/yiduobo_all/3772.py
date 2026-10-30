# 示例 2：n=5, edges=[[1,0],[1,2],[1,3],[3,4]], good=[0,1,0,1,1]
GOOD_ = [0, 1, 0, 1, 1]
POS_ = {0: (0.5, 0.10), 1: (0.5, 0.36), 2: (0.28, 0.64), 3: (0.72, 0.64), 4: (0.72, 0.90)}
EDGE_ = [(0, 1), (1, 2), (1, 3), (3, 4)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 120, y1 - y0 - 110
    P = {k: (x0 + 60 + v[0] * W, y0 + 55 + v[1] * H) for k, v in POS_.items()}
    inn = S.get('_inner', {})
    cx, cy = inn.get('now'), inn.get('child')
    cv.text((x0 + 18, y0 + 4), '树（绿 = 好点，红 = 坏点；黄框 = now，粉框 = child）', 22, T['muted'], bold=True)
    for a, b in EDGE_:
        hot = (cx, cy) in ((a, b), (b, a))
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    f, res = S.get('f'), S.get('res')
    for k, (px, py) in P.items():
        cv.rect((px - 26, py - 26, px + 26, py + 26), fill=T['green'] if GOOD_[k] else T['red'], r=26)
        if k == cx:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['yellow'], width=5, r=34)
        if k == cy:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['pink'], width=5, r=34)
        cv.text((px, py), k, 30, T['bg'], anchor='mm', bold=True)
        lines = []
        if f is not None and f[k] != 0:
            lines.append(('f=%d' % f[k], T['cyan']))
        if res is not None and res[k] != 0:
            lines.append(('res=%d' % res[k], T['orange']))
        for i, (s, c) in enumerate(lines):
            left = k == 2
            cv.text((px - 42 if left else px + 42, py - 14 + i * 28), s, 24, c, anchor='rm' if left else 'lm', bold=True, mono=True)


def cap_f_add(S, B, ret):
    now, c = S['_inner']['now'], S['_inner']['child']
    v = S.f[c]
    why = f'`f[{c}]={v}` > 0 → ==累加==，选上这棵子树' if v > 0 else f'`f[{c}]={v}` ≤ 0 → ==不选==（`max(0, ·)` 取 0）'
    return f'{why}：`f[{now}]` {B.f[now]} → =={S.f[now]}=='


def cap_init(S, B, ret):
    now = S['_inner']['now']
    return f'节点 `{now}` 是{"好" if GOOD_[now] else "坏"}点，先给 `f[{now}]` 记自己的 =={S.f[now]}=='


def cap_pa(S, B, ret):
    now = S['_inner']['now']
    return f'`pa = res[{now}] − f[{now}] = {S.res[now]} − {S.f[now]}` = =={S.pa}==：{now} 的子树之外、经过父亲能凑出的分数'


def cap_other(S, B, ret):
    now, c = S['_inner']['now'], S['_inner']['child']
    return (f'`other = f[{now}] − max(0, f[{c}])` = {S.f[now]} − {max(0, S.f[c])} = =={S.other}==：'
            f'以 {now} 为根、==去掉 {c} 子树==后的得分')


def cap_res(S, B, ret):
    now, c = S['_inner']['now'], S['_inner']['child']
    return (f'`res[{c}] = f[{c}] + max(0, pa + other)` = {S.f[c]} + max(0, {S.pa} + {S.other}) = =={S.res[c]}==')


CONFIG = dict(
    num=3772, title='树中子图的最大得分', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='换根 DP · 向下 + pa 传递',
    tags=['灵神题单', '动态规划', '难度分 2235'],
    code='''
class Solution(object):
    def maxSubgraphScore(self, n, edges, good):
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        f = [0] * n
        def dfs(now, fa, f):
            if good[now]:
                f[now] = 1
            else:
                f[now] = -1
            
            for child in g[now]:
                if child == fa:
                    continue
                f[now] += max(0, dfs(child, now, f))
            
            return f[now]
        
        dfs(0, -1, f)

        res = [0] * n
        res[0] = f[0]

        def calc(now, fa, res):
            pa = res[now] - f[now]
            for child in g[now]:
                if child == fa:
                    continue
                
                other = f[now] - max(0, f[child])
                res[child] = f[child] + max(0, pa + other)
                calc(child, now, res)

        calc(0, -1, res)

        return res
''',
    call='Solution().maxSubgraphScore(5, [[1,0],[1,2],[1,3],[3,4]], [0,1,0,1,1])',
    expect=[2, 3, 2, 3, 3],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='calls', h=160, hide=('f', 'res')),
    ],
    watch=['now', 'child', 'pa', 'other'],
    skip=['g = [[]', 'g[now]', 'g[x].append', 'g[y].append', 'for x, y in edges', 'continue', 'f = [0] * n', 'if child == fa'],
    captions={
        'f[now] = 1': cap_init,
        'f[now] = -1': cap_init,
        'f[now] += max': lambda S, B, r: f'先递归算出孩子 `{S["_inner"]["child"]}` 的 `f`；返回值 > 0 才累加到 `f[{S["_inner"]["now"]}]`，否则整棵子树放弃',
        'dfs(0, -1, f)': '先以 0 为根向下递归，算出每个 `f[x]`：以 x 为根的子树里、包含 x 的最大得分',
        'res[0] = f[0]': '根 0 的子树就是整棵树，所以 `res[0] = f[0]` = =={f[0]}==',
        'pa = res[now]': cap_pa,
        'other = f[now]': cap_other,
        'res[child] = f[child]': cap_res,
        'calc(0, -1, res)': '再从 0 向下走一遍：用父亲的答案推出每个孩子的答案',
        'return f[now]': lambda S, B, r: (f'`f[{S["_inner"]["now"]}]` = =={S.f[S["_inner"]["now"]]}==，返回给父亲：' + ('大于 0 → ==父亲会把它累加进去==' if S.f[S['_inner']['now']] > 0 else '不大于 0 → ==父亲会放弃整棵子树==')),
    },
    cards=dict(
        one_liner='答案 = 子树得分 f + 子树之外的得分 pa',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，好点 +1、坏点 −1，连通子图得分 = 好点数 − 坏点数',
                 '对每个节点，求包含它的连通子图的最大得分',
                 '示例：`good=[0,1,0,1,1]` → `[2,3,2,3,3]`'],
        quote='对于这类问题，一种常见的处理方法是换根dp。不妨设0号节点为整棵树的根节点。',
        quote_src='—— yiduobo 题解',
        idea=['`f[x]`：x 为根的子树里、包含 x 的最大得分；`f[y] > 0` 才加给父亲',
              '非根节点 y 的答案拆两块：自己的 `f[y]` + 父亲那一侧 `pa[y]`',
              '父亲那一侧 = `f[x] − max(0, f[y])`（去掉 y）再加上 x 以上的 `pa`，为负则舍去'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`f` 是子树得分，`res = pa + f` 才是最终答案，`pa = res[now] − f[now]`',
                 '去掉孩子时减的是 `max(0, f[child])`，因为当初只加了正的部分',
                 '`pa + other` 为负就整块舍弃，所以外面包 `max(0, ·)`'],
    ),
)
