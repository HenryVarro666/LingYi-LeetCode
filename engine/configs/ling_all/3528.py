# ---- 一般树绘制（custom 视图）：按边集合和根节点分层布局
def gtree(edges, root):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    kids, depth = {}, {root: 0}

    def go(v, fa):
        kids[v] = []
        for w in adj.get(v, []):
            if w != fa:
                depth[w] = depth[v] + 1
                kids[v].append(w)
                go(w, v)
    go(root, None)
    xs, cnt = {}, [0]

    def lay(v):
        if not kids[v]:
            xs[v] = cnt[0]
            cnt[0] += 1
        else:
            for w in kids[v]:
                lay(w)
            xs[v] = (xs[kids[v][0]] + xs[kids[v][-1]]) / 2
    lay(root)
    return kids, depth, xs, cnt[0]


def make_tree_draw(edges, root, state_fn, title, elabel=None, arrows=False):
    kids, depth, xs, nleaf = gtree(edges, root)
    maxd = max(depth.values())

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        sp = min(120, (x1 - x0 - 60) / max(1, nleaf))
        dy = min(120, (y1 - y0 - 90) / max(1, maxd + 0.6))
        rad = max(16, min(28, sp * 0.36, dy * 0.26))
        sx = x0 + 30 + ((x1 - x0 - 60) - sp * nleaf) / 2
        pos = {v: (sx + sp * (xs[v] + 0.5), y0 + 70 + depth[v] * dy) for v in kids}
        for v in kids:
            for w in kids[v]:
                (ax, ay), (bx, by) = pos[v], pos[w]
                if arrows:
                    cv.arrow((ax, ay + rad), (bx, by - rad), T['border'], 3, 10)
                else:
                    cv.line([(ax, ay + rad), (bx, by - rad)], T['border'], 3)
                if elabel and (v, w) in elabel:
                    mx, my = ax + (bx - ax) * 0.4, ay + (by - ay) * 0.4
                    s = str(elabel[(v, w)])
                    cv.text((mx - 8, my), s, 20, T['orange'], anchor='rm', bold=True)
        for v in kids:
            X, Y = pos[v]
            st = state_fn(S, v) or {}
            fill = T[st['fill']] if st.get('fill') else T['panel2']
            cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=T['border'], width=2, r=rad)
            if st.get('ring'):
                cv.rect((X - rad - 5, Y - rad - 5, X + rad + 5, Y + rad + 5), outline=T[st['ring']], width=5, r=rad + 5)
            cv.text((X, Y), st.get('text', v), 24, T['bg'] if st.get('fill') else T['text'], anchor='mm', bold=True)
            if st.get('sub') is not None:
                cv.text((X + rad + 8, Y), st['sub'], 21, T[st.get('subc', 'green')], anchor='lm', bold=True)
            if st.get('tag'):
                cv.text((X - rad - 8, Y - rad), st['tag'], 20, T[st.get('tagc', 'pink')], anchor='rb', bold=True)
    return draw
# ---- end helper

CONV = [[0,1,2],[0,2,3],[1,3,4],[1,4,5],[2,5,2],[4,6,3],[5,7,4]]
EDGES = [(x, y) for x, y, w in CONV]
WT = {(x, y): w for x, y, w in CONV}


def _st(S, v):
    ans = S.get('ans')
    inn = S.get('_inner', {})
    cur = inn.get('x') if 'mul' in inn else None
    done = ans is not None and ans[v] != 0
    return dict(fill='green' if done else None, ring='yellow' if cur == v else None,
                sub=f'{ans[v]}' if done else None, subc='green')


CONFIG = dict(
    num=3528, title='单位转换 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='建树 + 自顶向下 DFS 传乘积',
    tags=['链表树与回溯', '难度分 1580'],
    code='''
class Solution:
    def baseUnitConversions(self, conversions: List[List[int]]) -> List[int]:
        MOD = 1_000_000_007
        n = len(conversions) + 1
        g = [[] for _ in range(n)]
        for x, y, weight in conversions:
            g[x].append((y, weight))

        ans = [0] * n
        def dfs(x: int, mul: int) -> None:
            ans[x] = mul
            for y, weight in g[x]:
                dfs(y, mul * weight % MOD)
        dfs(0, 1)
        return ans
''',
    call='Solution().baseUnitConversions(CONV)',
    setup='CONV = [[0,1,2],[0,2,3],[1,3,4],[1,4,5],[2,5,2],[4,6,3],[5,7,4]]',
    expect=[1, 2, 3, 8, 10, 6, 30, 24],
    views=[
        dict(type='custom', draw=make_tree_draw(EDGES, 0, _st, '单位树（橙色数字 = 边权，绿 = 已算出 ans，节点右侧数字 = ans，黄环 = 当前 dfs 的节点）', WT, arrows=True), h=370),
        dict(type='array', var='ans', label='ans[i] = 一个 0 号单位等于多少个 i 号单位',
             color=lambda S, i, v: 'green' if v != 0 else None, h=150),
        dict(type='calls', h=190),
    ],
    watch=[('x', lambda S: S['_inner'].get('x') if 'mul' in S['_inner'] else None, 'blue'), ('mul', lambda S: S['_inner'].get('mul'), 'orange')],
    captions={
        'g[x].append': '建树：有向边 `{x} → {y}`，边权 `{weight}`（只存「源 → 目标」）',
        'ans = [0] * n': '`ans` 先全填 0，每个节点恰好会被 dfs 到一次',
        'ans[x] = mul': '到达 `{x}`：从 0 一路乘过来的边权之积就是 `{mul}`，==写入 ans[{x}]==',
        'dfs(y, mul': '走向儿子 `{y}`：`mul * weight % MOD` = `{B.mul} * {weight}` = =={B.mul * weight % MOD}==，作为新的 `mul` 传下去',
        'dfs(0, 1)': '从 0 号单位出发，`mul = 1`（1 个 0 等于 1 个 0）',
        'return ans': '每个节点都已写入，返回 `{ans}`',
    },
    cards=dict(
        one_liner='n 个点 n-1 条边且 0 能到达所有点 → 这是棵树，DFS 往下传乘积',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有 `n` 种单位，`conversions[i] = [源, 目标, 倍数]`：1 个源单位 = 倍数 个目标单位',
                 '求 1 个 0 号单位等于多少个 `i` 号单位，结果对 `10^9+7` 取模',
                 '示例：`[[0,1,2],[1,2,3]]` → `[1,2,6]`'],
        quote='这意味着输入的是 n 个点和 n-1 条边的连通图，说明输入的是一棵树。建树。然后从 0 开始 DFS 这棵树，同时把从 0 到 i 的边权乘起来，即为 ans[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['==看出是树==：保证 0 到任何点的路径唯一 → 连通且 n-1 条边',
              '递归时额外传参数 `mul`：根到当前点的边权之积',
              '每走一条边就乘一次 `weight` 并取模，到点 `x` 时 `ans[x] = mul`'],
        summary=['时间 `O(n)`：每个节点恰好访问一次；空间 `O(n)`',
                 '易错：乘法后要立刻 `% MOD`，否则乘积会爆炸',
                 '只建单向边 `x → y` 即可，不会走回头路，所以不需要 `fa` 参数',
                 '同类：一般树题单「自顶向下 DFS」'],
    ),
)
