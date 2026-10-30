PARENT = [-1, 0, 0, 1, 1]
NUMS = [1, 2, 3, 4, 5]
K = 3


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(PARENT)
    kids = [[] for _ in range(n)]
    for i in range(1, n):
        kids[PARENT[i]].append(i)
    depth = [0] * n
    for i in range(1, n):
        depth[i] = depth[PARENT[i]] + 1
    pos, cnt = {}, [0]

    def lay(u):
        if not kids[u]:
            pos[u] = cnt[0]
            cnt[0] += 1
        else:
            for c in kids[u]:
                lay(c)
            pos[u] = sum(pos[c] for c in kids[u]) / len(kids[u])
    lay(0)
    leaves = cnt[0]
    md = max(depth)
    W = (x1 - x0 - 80) / max(leaves, 1)
    H = (y1 - y0 - 160) / max(md, 1)
    H = min(H, 100)
    cur = S.get('_inner', {}).get('x') if S.get('_inner') else S.get('x')
    ch = S.get('_inner', {}).get('y') if S.get('_inner') else S.get('y')
    cv.text((x0 + 18, y0 + 4), '树（括号里是 nums；蓝 = 正在算的 x，粉 = 刚返回的儿子 y）', 22, T['muted'], bold=True)
    P = {u: (x0 + 40 + W * (pos[u] + 0.5), y0 + 80 + H * depth[u]) for u in range(n)}
    for u in range(1, n):
        cv.line([P[PARENT[u]], P[u]], T['border'], 3)
    for u in range(n):
        px, py = P[u]
        fill = T['blue'] if u == cur else T['pink'] if u == ch else T['panel2']
        cv.rect((px - 34, py - 26, px + 34, py + 26), fill=fill, r=26, outline=T['border'])
        cv.text((px, py - 4), u, 26, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py + 38), f'({NUMS[u]})', 18, T['muted'], anchor='mm', mono=True)


def _merge0(S, B, ret):
    return f'开始算「不选 x={S.x}」：儿子 y={S.y} 选或不选都行，权重 `fy0[i]+fy1[i]`，与 `f0 = {S.f0}` 做模 {S.k} 卷积'


def _merge1(S, B, ret):
    return (f'「不选 x」算完：`nf0 = {S.nf0}`。再算「选 x={S.x}」：儿子 `y={S.y}` ==不能选==，只能用 `fy0 = {S.fy0}`')


def _merge2(S, B, ret):
    return (f'「选 x」算完：`fy0 = {S.fy0}` 与 `f1 = {B.f1}` 卷积 → `nf1 = {S.nf1}`；'
            f'`f0, f1` 换成合并儿子 `{S.y}` 之后的结果')


CONFIG = dict(
    num=3939, title='统计有根树中不相邻子集的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='树形 DP · 树上背包（模 k 卷积）',
    tags=['灵神题单', '动态规划', '难度分 2354'],
    code='''
class Solution:
    def countValidSubsets(self, parent: list[int], nums: list[int], k: int) -> int:
        MOD = 1_000_000_007
        n = len(parent)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parent[i]].append(i)

        def dfs(x: int) -> tuple[list[int], list[int]]:
            f0 = [0] * k  # f0[i] 表示不选 x 时，子树 x 的子集点权和模 k 为 i 的方案数
            f1 = [0] * k  # f1[i] 表示选 x 时，子树 x 的子集点权和模 k 为 i 的方案数
            f0[0] = 1
            f1[nums[x] % k] = 1

            for y in g[x]:
                fy0, fy1 = dfs(y)

                # 不选 x，那么 y 可选可不选
                nf0 = [0] * k
                for i in range(k):  # 枚举从子树 y 中选出的点权和模 k 为 i
                    v = fy0[i] + fy1[i]
                    if v == 0:  # 优化
                        continue
                    for j, w in enumerate(f0):  # 枚举从之前的子树中选出的点权和模 k 为 j
                        s = (i + j) % k
                        nf0[s] = (nf0[s] + v * w) % MOD

                # 选 x，那么 y 不能选
                nf1 = [0] * k
                for i, v in enumerate(fy0):  # 枚举从子树 y 中选出的点权和模 k 为 i
                    if v == 0:  # 优化
                        continue
                    for j, w in enumerate(f1):  # 枚举从 x 以及之前的子树中选出的点权和模 k 为 j
                        s = (i + j) % k
                        nf1[s] = (nf1[s] + v * w) % MOD

                f0, f1 = nf0, nf1

            return f0, f1

        f0, f1 = dfs(0)
        # 恰好被 k 整除即模 k 为 0，注意减去空集的方案数 1
        return (f0[0] + f1[0] - 1) % MOD
''',
    call=f'Solution().countValidSubsets({PARENT!r}, {NUMS!r}, {K})',
    expect=4,
    skip=['for i in range(k)', 'v = fy0[i] + fy1[i]', 'if v == 0', 'continue', 'for j, w in enumerate', 's = (i + j) % k',
          'nf0[s] =', 'nf1[s] =', 'for i, v in enumerate(fy0)', 'g = [[]', 'for i in range(1, n)', 'g[parent[i]]', 'n = len(parent)'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='f0', label='f0[i]：不选 x，子树和模 k = i 的方案数', h=120, cell=64),
        dict(type='array', var='f1', label='f1[i]：选 x，子树和模 k = i 的方案数', h=120, cell=64),
        dict(type='calls', h=120),
    ],
    watch=['x', 'y', 'fy0', 'fy1', 'nf0', 'nf1'],
    captions={
        10: '`f0`：==不选== x 时，子树和模 `k={k}` 为 i 的方案数',
        11: '`f1`：==选== x 时，子树和模 `k` 为 i 的方案数',
        'f0[0] = 1': '不选 x 且还没选儿子：空集，和为 0 → `f0[0] = 1`',
        'f1[nums[x] % k] = 1': '只选 x 自己：和模 k = `nums[{x}] % {k} = {nums[x] % k}` → `f1[{nums[x] % k}] = 1`',
        'fy0, fy1 = dfs(y)': '先递归算儿子 `y = {y}`，拿到它的 `fy0` 和 `fy1`',
        'nf0 = [0] * k': _merge0,
        'nf1 = [0] * k': _merge1,
        'f0, f1 = nf0, nf1': _merge2,
        'return f0, f1': '`dfs({x})` 返回：`f0 = {f0}`，`f1 = {f1}`',
        'f0, f1 = dfs(0)': '根的结果：`f0 = {f0}`，`f1 = {f1}`',
        'return (f0[0]': '和模 k 为 0：`f0[0] + f1[0] - 1` = `{f0[0]} + {f1[0]} - 1` = ==`{ret}`==（减 1 是去掉空集）',
    },
    cards=dict(
        one_liner='打家劫舍 III + 模 k 背包：选/不选 x 各存一个长度 k 的数组',
        complexity='时间 `O(nk^2)`，空间 `O(nk)`',
        problem=['有根树，每个点有权值，选一个==非空==子集', '子集里没有父子相邻，且权值和能被 `k` 整除',
                 '求方案数，对 `10^9+7` 取模。视频用 `parent=[-1,0,0,1,1], nums=[1,2,3,4,5], k=3`'],
        quote='考虑到 k 比较小，我们可以在 337 题的基础上，定义：dfs(x)_0[i] 表示不选节点 x 时，子树 x 的子集点权和模 k 为 i 的方案数；dfs(x)_1[i] 表示选节点 x 时……',
        quote_src='—— 灵茶山艾府题解',
        idea=['选 x 则儿子不能选，只能用 `fy0`；不选 x 则儿子可选可不选，用 `fy0 + fy1`',
              '合并一个儿子 = 模 k 的卷积：枚举儿子的和 `i` 与之前的和 `j`，落到 `(i+j)%k`，用乘法原理',
              '初始：`f0[0]=1`，`f1[nums[x]%k]=1`；答案 `f0[0]+f1[0]-1`'],
        summary=['时间 `O(nk^2)`：每条边做一次 `O(k^2)` 合并；空间 `O(nk)`',
                 '易错：最后要减去空集（`f0[0]` 里包含空集）',
                 '`nf1` 只能用 `fy0`，别把 `fy1` 也加进去',
                 '视频里为了省步数跳过了两层内部循环的逐行高亮，只展示每次合并的结果；灵神另给了字典版写法'],
    ),
)
