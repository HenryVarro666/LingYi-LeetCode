from math import gcd


def _layout(g, n):
    """以 0 为根的树：返回 (children, depth, x 坐标(叶子序号))"""
    ch = {i: [] for i in range(n)}
    depth = {0: 0}
    st = [(0, -1)]
    order = []
    while st:
        x, fa = st.pop()
        order.append(x)
        for y in g[x]:
            if y != fa:
                ch[x].append(y)
                depth[y] = depth[x] + 1
                st.append((y, x))
    xs, cnt = {}, [0]

    def go(x):
        if not ch[x]:
            xs[x] = cnt[0]
            cnt[0] += 1
        else:
            for y in ch[x]:
                go(y)
            xs[x] = (xs[ch[x][0]] + xs[ch[x][-1]]) / 2
    go(0)
    return ch, depth, xs, max(cnt[0], 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g, nums = S['g'], S['nums']
    n = len(nums)
    ch, depth, xs, w = _layout(g, n)
    cv.text((x0 + 18, y0 + 4), '树（圈内 = 节点值；黄 = 栈上祖先，蓝 = 当前节点 x，绿 = 答案节点）', 22, T['muted'], bold=True)
    vd = S['val_depth_id']
    anc = {p[1] for p in vd if p[1] >= 0}
    cur = S.get('x') if '_inner' in S and 'x' in S['_inner'] else None
    ans_node = None
    if cur is not None and S['_line'] >= 21:
        a = S['ans'][cur]
        ans_node = a if a >= 0 else None
    sp = min(150, (x1 - x0 - 120) / w)
    sx = x0 + 60 + ((x1 - x0 - 120) - sp * (w - 1)) / 2
    md = max(depth.values())
    rad = 28
    top = y0 + 88
    dy = min(110, (y1 - y0 - 88 - rad - 24) / max(md, 1))
    pos = {i: (sx + xs[i] * sp, top + depth[i] * dy) for i in range(n)}
    for p in range(n):
        for c in ch[p]:
            cv.line([pos[p], pos[c]], T['border'], 3)
    for i in range(n):
        X, Y = pos[i]
        fill = T['panel2']
        if i in anc:
            fill = T['yellow']
        if i == ans_node:
            fill = T['green']
        if i == cur:
            fill = T['blue']
        cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=fill, r=rad, outline=T['border'])
        cv.text((X, Y), nums[i], 30, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((X + rad + 4, Y - rad - 2), f'#{i}', 20, T['dim'], anchor='lb', mono=True)


def _vd(S):
    vd = S.get('val_depth_id')
    if vd is None:
        return ''
    items = [f'值 {j} → ==(深度 {p[0]}，节点 {p[1]})==' for j, p in enumerate(vd) if p != (-1, -1)]
    return '`val_depth_id` 非空项：' + ('　'.join(items) if items else '无（没有祖先）')


CONFIG = dict(
    num=1766, title='互质树', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自顶向下 DFS + 按节点值记录最近祖先 + 恢复现场',
    tags=['灵神题单', '难度分 2232'],
    code='''
# 预处理：coprime[i] 保存 [1, MX) 中与 i 互质的所有元素
MX = 51
coprime = [[j for j in range(1, MX) if gcd(i, j) == 1]
           for i in range(MX)]

class Solution:
    def getCoprimes(self, nums: List[int], edges: List[List[int]]) -> List[int]:
        n = len(nums)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        ans = [0] * n
        val_depth_id = [(-1, -1)] * MX  # 包含深度和节点编号
        def dfs(x: int, fa: int, depth: int) -> None:
            val = nums[x]  # x 的节点值
            # 计算与 val 互质的祖先节点值中，节点深度最大的节点编号
            ans[x] = max(val_depth_id[j] for j in coprime[val])[1]
            tmp = val_depth_id[val]  # 用于恢复现场
            val_depth_id[val] = (depth, x)  # 保存 val 对应的节点深度和节点编号
            for y in g[x]:
                if y != fa:
                    dfs(y, x, depth + 1)
            val_depth_id[val] = tmp  # 恢复现场
        dfs(0, -1, 0)
        return ans
''',
    setup='from math import gcd',
    call='Solution().getCoprimes([2, 3, 3, 2], [[0, 1], [1, 2], [1, 3]])',
    expect=[-1, 0, 0, 1],
    skip=['MX = 51', 'coprime = ', 'for j in range(1, MX)', 'for _ in range(n)', 'g[x].append', 'g[y].append', 'for x, y in edges'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_vd, size=26, h=80),
        dict(type='array', var='ans', label='ans（-1 = 没有互质祖先）', cell=60, h=120),
        dict(type='calls', h=130),
    ],
    watch=['x', 'fa', 'depth', 'val', 'tmp'],
    captions={
        'n = len': '`n = {n}` 个节点',
        'g = [[]': '`g` 是邻接表，建好无向图',
        'ans = [0]': '`ans[x]` 存节点 x 最近的互质祖先编号',
        'val_depth_id = [': '`val_depth_id[v]`：值为 `v` 的 ==最近祖先== 的（深度，节点编号）。初始都是 `(-1, -1)`',
        'val = nums[x]': '进入节点 `{x}`，它的值 `val = {val}`',
        'ans[x] = max': lambda S, B, r: (f'只看 [1,50] 中与 {S.val} 互质的 {sum(gcd(S.val, j) == 1 for j in range(1, 51))} 个值，取祖先里 ==深度最大== 的 → '
                                       f'`ans[{S.x}] = {S.ans[S.x]}`'
                                       + ('（没有互质祖先）' if S.ans[S.x] == -1 else '')),
        'tmp = val_depth_id[val]': '先把值 `{val}` 原来记的祖先 `{tmp}` 存起来，待会要恢复',
        'val_depth_id[val] = (depth, x)': '节点 `{x}` 成为值 `{val}` 的最近祖先：记 `({depth}, {x})`，子孙都会看到它',
        'if y != fa': lambda S, B, r: (f'`y = {S.y}` 是父节点 `fa`，不能走回头路' if S.y == S.fa else f'`y = {S.y}` 是孩子 → 递归，深度 +1'),
        'dfs(y, x, depth + 1)': '进入孩子 `{y}`',
        'val_depth_id[val] = tmp': '==恢复现场==：离开节点 `{x}`，值 `{val}` 的记录还原成 `{tmp}`。否则兄弟节点会把 `{x}` 当祖先',
        'dfs(0, -1, 0)': '从根 0 出发，深度 0，没有父节点（-1）',
        'return ans': '每个节点的最近互质祖先都求出了：`{ans}`',
    },
    cards=dict(
        one_liner='值只有 50 种：每种值只记最深的祖先，再枚举互质的值取最深',
        complexity='时间 `O(nU)`，空间 `O(n + U)`，`U = 50`',
        problem=['树根为 0，每个节点有值 `nums[i]`（≤ 50）',
                 '对每个节点，求最近的、与它值 ==互质== 的祖先编号，没有则 -1',
                 '示例：`nums=[2,3,3,2]`，边 `0-1, 1-2, 1-3` → `[-1,0,0,1]`'],
        quote='对于节点值相同的祖先，只需枚举深度最大的。因此，对于节点 x，我们至多枚举它的 50 个祖先。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力枚举祖先，链状树会到 `O(n^2)`',
              '值 ≤ 50：用 `val_depth_id[v]` 记录值 `v` 的最近祖先（深度、编号）',
              '预处理 `coprime[v]`：[1,50] 中与 `v` 互质的数；取这些值里最深的祖先',
              'DFS 进入节点时覆盖记录，离开时 ==恢复现场==（回溯）'],
        summary=['时间 `O(nU)`，空间 `O(n + U)`；预处理不计',
                 '`max` 比较元组：先比深度，深度大的就是最近祖先',
                 '恢复现场必不可少：否则兄弟子树会读到别的分支的节点',
                 '实际 n 可达 1e5，递归深度大，提交时需注意栈深（演示树很小）'],
    ),
)
