N0 = 5
EDGES0 = [[0, 1], [1, 2], [2, 3], [3, 4]]
LABEL0 = 'abcba'
POS = [(0.1, 0.5), (0.3, 0.5), (0.5, 0.5), (0.7, 0.5), (0.9, 0.5)]
DFS_LINES = range(20, 32)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '图（字母 = label；蓝 = 左端 x，粉 = 右端 y，绿 = 已访问集合）', 22, T['muted'], bold=True)
    line = S.get('_line', 0)
    in_dfs = line in DFS_LINES and 'vis' in S
    x, y = S.get('x'), S.get('y')
    vis = S.get('vis', 0) if in_dfs else 0
    v, w = (S.get('v'), S.get('w')) if line in range(23, 31) else (None, None)
    w_, h_ = x1 - x0, y1 - y0
    pts = [(x0 + px * w_, y0 + h_ * 0.5) for px, _ in POS]
    for a, b in EDGES0:
        cv.line([pts[a], pts[b]], T['border'], 4)
    for i, (px, py) in enumerate(pts):
        fill = T['panel2']
        if x is not None and (in_dfs or line >= 34):
            if i == x:
                fill = T['blue']
            elif i == y and in_dfs:
                fill = T['pink']
            elif vis >> i & 1:
                fill = T['green']
        if in_dfs and i in (v, w) and line >= 26 and fill == T['panel2']:
            fill = T['yellow']
        elif in_dfs and vis >> i & 1 and fill == T['panel2']:
            fill = T['green']
        r = 40
        cv.rect((px - r, py - r, px + r, py + r), fill=fill, r=r, outline=T['border'])
        cv.text((px, py - 4), LABEL0[i], 36, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py + r + 14), f'节点 {i}', 18, T['dim'], anchor='mt')
    if in_dfs and x is not None and y is not None:
        cv.text((x0 + 18, y1 - 40), f'左端 x = {x}（{LABEL0[x]}），右端 y = {y}（{LABEL0[y]}），已访问 {[i for i in range(N0) if vis >> i & 1]}', 24, T['text'], bold=True)


def _formula(S):
    line = S.get('_line', 0)
    if line >= 33 and S.get('ans') is not None:
        return f'`ans = {S["ans"]}`，理论最大值 `theoretical_max = {S.get("theoretical_max")}`（等于它就能提前返回）'
    if line in DFS_LINES and 'res' in S:
        return f'`dfs(x={S["x"]}, y={S["y"]})` 目前最多还能向两侧扩展 `res = {S["res"]}` 个节点（不算 x、y）'
    return '中心扩展：左右端点同时向外走一步，==两端字母必须相同=='


def _cap_if(S, B, ret):
    v, w = S.v, S.w
    if S.vis >> w & 1:
        return f'右边的邻居 `w = {w}` 已访问过，跳过'
    if v == w:
        return f'`v = w = {v}`：左右会走到同一个节点，不行（每个点最多访问一次）'
    if S.label[w] != S.label[v]:
        return f'`label[{v}] = {S.label[v]}` ≠ `label[{w}] = {S.label[w]}` → 两端字母不同，不是回文，不能扩展'
    return f'`label[{v}] = label[{w}] = {S.label[v]}` ==相同== → 回文可以向两侧各长一格'


CONFIG = dict(
    num=3615, title='图中的最长回文路径', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='回文中心扩展 + 状压记忆化搜索',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2463'],
    code='''
# 手写 max 更快
max = lambda a, b: b if b > a else a

class Solution:
    def maxLen(self, n: int, edges: List[List[int]], label: str) -> int:
        # 计算理论最大值
        odd = sum(c % 2 for c in Counter(label).values()) 
        theoretical_max = n - max(odd - 1, 0)  # 奇数选一个放正中心，其余全弃

        if len(edges) == n * (n - 1) // 2:  # 完全图，可以达到理论最大值
            return theoretical_max

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        # 计算从 x 和 y 向两侧扩展，最多还能访问多少个节点（不算 x 和 y）
        @cache
        def dfs(x: int, y: int, vis: int) -> int:
            res = 0
            for v in g[x]:
                if vis >> v & 1:
                    continue
                for w in g[y]:
                    if vis >> w & 1 == 0 and v != w and label[w] == label[v]:
                        tv, tw = v, w  # 注意不能直接交换 v 和 w，否则下个循环的 v 就不是原来的 v 了
                        if tv > tw:  # 保证 tv < tw，减少状态个数和计算量
                            tv, tw = tw, tv
                        res = max(res, dfs(tv, tw, vis | 1 << v | 1 << w) + 2)
            return res

        ans = 0
        for x, to in enumerate(g):
            # 奇回文串，x 作为回文中心
            ans = max(ans, dfs(x, x, 1 << x) + 1)
            if ans == theoretical_max:
                return ans
            # 偶回文串，x 和 x 的邻居 y 作为回文中心
            for y in to:
                # 保证递归参数 x < y，减少状态个数和计算量
                if x < y and label[x] == label[y]:
                    ans = max(ans, dfs(x, y, 1 << x | 1 << y) + 2)
                    if ans == theoretical_max:
                        return ans
        return ans
''',
    call=f'Solution().maxLen({N0}, {EDGES0}, {LABEL0!r})',
    expect=5,
    skip=['g = [[] for', 'g[x].append', 'g[y].append', 'for x, y in edges', 'continue', 'if tv > tw', 'tv, tw = tw, tv', 'for y in to', 'for v in g[x]', 'for w in g[y]'],
    max_steps=60,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='custom', draw=_draw, h=250),
        dict(type='calls', h=300),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('v', 'v', 'yellow'), ('w', 'w', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'odd = sum': '`label` 里出现奇数次的字母有 `{odd}` 种',
        'theoretical_max = n - max': '理论最大值：奇数次的字母只能留 1 个放中心 → `n - max({odd}-1, 0) = {theoretical_max}`',
        'if len(edges) ==': '`len(edges) = {len(edges)}`，完全图要 `{n*(n-1)//2}` 条 → 不是完全图，要真的搜',
        'res = 0': '`dfs({x}, {y})`：左端 `{x}`、右端 `{y}`，还能扩展 0 个节点（先设 0）',
        'if vis >> v & 1:': lambda S, B, r: f'左边的邻居 `v = {S.v}`：' + ('已经访问过 → 跳过' if S.vis >> S.v & 1 else '没访问过，可以用'),
        'if vis >> w & 1 == 0 and': _cap_if,
        'tv, tw = v, w': '用临时变量 `tv, tw` 保证 `tv < tw`（`dfs(x,y)` 和 `dfs(y,x)` 等价，只算一次）',
        'res = max(res, dfs(': '`v = {v}`、`w = {w}` 都放进路径：递归 `dfs({tv}, {tw}, ..)` 算外面还能扩多少，返回值 +2（这两个点）再和 `res = {res}` 取大',
        'return res': '`dfs({x}, {y})` 最多还能扩展 =={ret}== 个节点，返回上一层',
        'ans = 0': '`ans` 记录目前找到的最长回文长度',
        'for x, to in enumerate(g)': '枚举回文中心 `x = {x}`',
        'ans = max(ans, dfs(x, x': '奇回文：`x = {x}` 当中心，调用 `dfs({x}, {x}, ..)` 算向两侧最多还能扩几个点，长度 = 返回值 + 1',
        'if ans == theoretical_max': lambda S, B, r: (f'更新后 `ans = {S.ans}`，等于理论最大值 `{S.theoretical_max}` → 不可能更长，==直接返回==' if S.ans == S.theoretical_max
                                                      else f'更新后 `ans = {S.ans}` ≠ 理论最大值 `{S.theoretical_max}`，继续枚举'),
        'if x < y and label[x] == label[y]': lambda S, B, r: (f'偶回文中心 `({S.x}, {S.y})`：相邻且字母相同' if S.x < S.y and S.label[S.x] == S.label[S.y]
                                                              else f'`({S.x}, {S.y})` 不满足 x<y 且字母相同，跳过'),
        'ans = max(ans, dfs(x, y': '偶回文：`({x}, {y})` 当中心，调用 `dfs({x}, {y}, ..)`，长度 = 返回值 + 2',
        'return ans': '最长回文路径长度 = =={ret}==',
    },
    cards=dict(
        one_liner='从回文中心向两边扩展，集合记已访问',
        complexity='时间 `O(n^4 · 2^n)`，空间 `O(n^2 · 2^n)`',
        problem=['无向图 `n` 个节点，每个节点一个字母；每个点最多走一次',
                 '求一条路径上的字母能拼成的==最长回文串==的长度',
                 '示例：`n=3, edges=[[0,1],[1,2]], label="aba"` → `3`；本视频用路径图 `"abcba"`'],
        quote='核心思路：枚举回文中心，从中心向左右两边扩展（中心扩展法）。……已经访问过的节点，其访问顺序是不重要的，我们只需要知道访问过哪些点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(x, y, S)`：左右端点 `x`、`y`，已访问集合 `S`，向两侧最多还能扩多少个点',
              '枚举 `x` 的邻居 `v`、`y` 的邻居 `w`：都没访问过、`v ≠ w`、字母相同才能扩 → `dfs(v, w, ..) + 2`',
              '入口：奇回文 `dfs(x,x,{x})+1`；偶回文 `dfs(x,y,{x,y})+2`。另有完全图特判和「达到理论最大值就返回」两个优化'],
        summary=['时间 `O(n^4 2^n)` = 状态 `O(n^2 2^n)` × 转移 `O(n^2)`',
                 '易错：不能直接交换 `v, w`（会影响后面的循环）；`v == w` 不能同时选',
                 '优化 `x ≤ y`：`dfs(x,y)` 与 `dfs(y,x)` 结果相同；完全图直接返回理论最大值',
                 '用的是 `@cache` 记忆化搜索，题解里没有递推写法'],
    ),
)
