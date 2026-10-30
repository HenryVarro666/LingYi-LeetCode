# 示例 2：n=5, edges=[[1,0],[1,2],[1,3],[3,4]], good=[0,1,0,1,1]
N_ = 5
GOOD_ = [0, 1, 0, 1, 1]
POS_ = {0: (0.5, 0.10), 1: (0.5, 0.36), 2: (0.28, 0.64), 3: (0.72, 0.64), 4: (0.72, 0.90)}
EDGE_ = [(0, 1), (1, 2), (1, 3), (3, 4)]
REC = {'sub': set(), 'ans': set()}


def rec(kind, add=True, reset=False):
    def f(S, B, ret):
        if reset:
            REC['sub'].clear(); REC['ans'].clear()
        x = S['_inner'].get('x')
        y = S['_inner'].get('y')
        if kind == 'sub':
            REC['sub'].add(x)
        elif kind == 'ans0':
            REC['ans'].add(0)
        elif kind == 'ansy':
            REC['ans'].add(y)
        return CAPS[kind](S, B, ret) if kind in CAPS else None
    return f


CAPS = {}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 120, y1 - y0 - 110
    P = {k: (x0 + 60 + v[0] * W, y0 + 55 + v[1] * H) for k, v in POS_.items()}
    inn = S.get('_inner', {})
    cx, cy = inn.get('x'), inn.get('y')
    cv.text((x0 + 18, y0 + 4), '树（绿 = 好点 +1，红 = 坏点 −1；黄框 = 当前 x，粉框 = 儿子 y）', 22, T['muted'], bold=True)
    for a, b in EDGE_:
        hot = (cx, cy) in ((a, b), (b, a))
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    sub, ans = S.get('sub_score'), S.get('ans')
    for k, (px, py) in P.items():
        cv.rect((px - 26, py - 26, px + 26, py + 26), fill=T['green'] if GOOD_[k] else T['red'], r=26)
        if k == cx:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['yellow'], width=5, r=34)
        if k == cy:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['pink'], width=5, r=34)
        cv.text((px, py), k, 30, T['bg'], anchor='mm', bold=True)
        lines = []
        if sub is not None and sub[k] != 0:
            lines.append(('sub=%d' % sub[k], T['cyan']))
        if ans is not None and ans[k] != 0:
            lines.append(('ans=%d' % ans[k], T['orange']))
        side = -1 if k in (2,) else 1
        for i, (s, c) in enumerate(lines):
            cv.text((px + 42, py - 14 + i * 28) if k != 2 else (px - 42, py - 14 + i * 28), s, 24, c,
                    anchor='lm' if k != 2 else 'rm', bold=True, mono=True)


def cap_dfs_enter(S, B, ret):
    x = S['_inner']['x']
    return f'节点 `{x}` 是{"好" if GOOD_[x] else "坏"}点：先记自己：`sub_score[{x}]` = =={S.sub_score[x]}==（这一块一定包含 `{x}`）'


def cap_dfs_add(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    s = S.sub_score[y]
    why = f'子树 {y} 得分 `{s}` > 0 → ==选上==' if s > 0 else f'子树 {y} 得分 `{s}` ≤ 0 → ==不选==（加 0）'
    return f'{why}：`sub_score[{x}]` {B.sub_score[x]} → =={S.sub_score[x]}=='


def cap_f(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    return (f'从 `ans[{x}]={S.ans[x]}` 里去掉子树 {y} 的贡献 `max(sub_score[{y}],0)={max(S.sub_score[y],0)}`，'
            f'剩下的 F 换根后挂在 {y} 下面：`score_f` = =={S.score_f}==')


def cap_ans(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    return (f'`ans[{y}] = sub_score[{y}] + max(score_f, 0) = {S.sub_score[y]} + {max(S.score_f,0)}` = =={S.ans[y]}=='
            f'（F 为正才接上）')


CAPS.update(sub=cap_dfs_enter, ans0=lambda S, B, r: f'根 0 的子树就是整棵树，所以 `ans[0] = sub_score[0]` = =={S.ans[0]}==', ansy=cap_ans)

CONFIG = dict(
    num=3772, title='树中子图的最大得分', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='换根 DP',
    tags=['灵神题单', '动态规划', '难度分 2235'],
    code='''
# 手写 max 更快
max = lambda a, b: b if b > a else a

class Solution:
    def maxSubgraphScore(self, n: int, edges: List[List[int]], good: List[int]) -> List[int]:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        # sub_score[x] 表示（以 0 为根时）包含 x 的子树 x 的最大得分（注意是子树不是子图）
        sub_score = [0] * n
        # 计算 sub_score[x]
        def dfs(x: int, fa: int) -> None:
            sub_score[x] = 1 if good[x] else -1  # sub_score[x] 一定包含 x
            for y in g[x]:
                if y != fa:
                    dfs(y, x)
                    # 如果子树 y 的最大得分 > 0，选子树 y，否则不选
                    sub_score[x] += max(sub_score[y], 0)
        dfs(0, -1)

        ans = [0] * n
        ans[0] = sub_score[0]
        # 对于 x 的儿子 y，计算包含 y 的子图最大得分
        def reroot(x: int, fa: int) -> None:
            for y in g[x]:
                if y != fa:
                    # 从 ans[x] 中去掉子树 y。换根后，这部分内容变成 y 的一棵子树（记作 F）
                    score_f = ans[x] - max(sub_score[y], 0)
                    # 如果子树 F 的最大得分 > 0，选子树 F，否则不选
                    ans[y] = sub_score[y] + max(score_f, 0)
                    reroot(y, x)
        reroot(0, -1)
        return ans
''',
    call='Solution().maxSubgraphScore(5, [[1,0],[1,2],[1,3],[3,4]], [0,1,0,1,1])',
    expect=[2, 3, 2, 3, 3],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='calls', h=160),
    ],
    watch=['x', 'y', 'score_f'],
    skip=['g = [[]', 'g[x].append', 'g[y].append', 'for x, y in edges', 'max = lambda', 'if y != fa'],
    captions={
        'sub_score = [0] * n': '准备 `sub_score`：以 `0` 为根，记每棵==子树==（不含父亲）的最大得分',
        'sub_score[x] = 1 if': cap_dfs_enter,
        'sub_score[x] += max': cap_dfs_add,
        'dfs(0, -1)': '从根 0 出发做第一次 DFS，后序算出每棵子树的得分',
        'ans[0] = sub_score[0]': CAPS['ans0'],
        'reroot(0, -1)': '第二次 DFS：从根往下换根，`y` 是 `x` 的儿子，由 `ans[x]` 推出 `ans[y]`',
        'score_f = ans[x]': cap_f,
        'ans[y] = sub_score[y]': cap_ans,
    },
    cards=dict(
        one_liner='先算子树最优，再把「去掉儿子后的剩余部分」挂到儿子下面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，节点好（+1）或坏（−1），子图得分 = 好点数 − 坏点数',
                 '对每个节点 `i`，求包含 `i` 的连通子图的最大得分',
                 '示例：`good=[0,1,0,1,1]` → `[2,3,2,3,3]`'],
        quote='从 x 中去掉子树 y，剩余部分记作 F。换根后，F 变成挂在 y 下面的一棵子树。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一次 DFS：以 0 为根，`sub_score[x]` = 自己 + 所有 ==为正的== 儿子子树',
              '第二次 DFS：`ans[x]` 去掉 y 的贡献就是 F 的得分，F 为正才接到 y 下面',
              '转移：`ans[y] = sub_score[y] + max(ans[x] − max(sub_score[y],0), 0)`'],
        summary=['时间 `O(n)`，空间 `O(n)`（建图 + 递归栈）',
                 '易错：`sub_score` 是==子树==得分，不含父亲；`ans` 才是整棵树里的子图',
                 '去掉 y 的贡献时要减 `max(sub_score[y], 0)`，不是减 `sub_score[y]`',
                 '写法二：把 `sub_score`、`ans` 都直接记在 `good` 数组里，省掉两个数组',
                 '同类：换根 DP 模板，见 §12.4'],
    ),
)
