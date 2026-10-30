def _comp(S):
    v = S.get('vis')
    return None if v is None else v


CONFIG = dict(
    num=1722, title='执行交换操作后的最小汉明距离', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='建图 DFS · 连通块内抵消',
    tags=['贪心与思维', '难度分 1892'],
    code='''
class Solution:
    def minimumHammingDistance(self, source: List[int], target: List[int], allowedSwaps: List[List[int]]) -> int:
        n = len(source)
        g = [[] for _ in range(n)]
        for i, j in allowedSwaps:
            g[i].append(j)  # 建图
            g[j].append(i)

        def dfs(x: int) -> None:
            vis[x] = True  # 避免重复访问
            # 抵消相同的元素，最终剩下 source 和 target 各自多出来的元素（对称差）
            diff[source[x]] += 1
            diff[target[x]] -= 1
            for y in g[x]:
                if not vis[y]:
                    dfs(y)

        vis = [False] * n
        ans = 0
        for x in range(n):
            if not vis[x]:
                diff = defaultdict(int)
                dfs(x)
                ans += sum(map(abs, diff.values()))
        return ans // 2  # 有 ans // 2 对多出来的元素
''',
    call='Solution().minimumHammingDistance([1,2,3,4,5], [3,1,1,5,5], [[0,1],[1,2],[3,4]])',
    expect=2,
    views=[
        dict(type='array', var='source', label='source（黄 = 正在 dfs 的下标，绿 = 已归入某个连通块）', h=140,
             pointers={'x': 'yellow'},
             color=lambda S, i, v: 'green' if S.get('vis') and S['vis'][i] else None),
        dict(type='array', var='target', label='target', h=110,
             color=lambda S, i, v: 'green' if S.get('vis') and S['vis'][i] else None),
        dict(type='map', var='diff', label='diff：值 → source 多出的个数（负数 = target 多出）', h=90,
             fmt=lambda k, v: f'{k}: {v:+d}'),
        dict(type='text', fn=lambda S: ('连通边：' + '　'.join(f'{i}—{j}' for i, j in S['allowedSwaps'])) if 'allowedSwaps' in S else '', size=24, h=50),
        dict(type='calls', h=130),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'n = len(source)': '`n = {n}`：下标 0 ~ n−1 是图中的点',
        'g = [[]': '`g[i]` 存和下标 `i` 能交换的下标（邻接表）',
        'g[i].append(j)': '`allowedSwaps` 里的 `[{i}, {j}]` 就是一条无向边：先加 `{i} → {j}`',
        'g[j].append(i)': '再加反向 `{j} → {i}`，连通块里的下标可以随意交换',
        'vis[x] = True': '访问下标 `{x}`，标记已访问，避免重复',
        'diff[source[x]] += 1': '`source[{x}] = {source[x]}`：这个连通块里 source 多出一个 `{source[x]}` → `diff = {dict(diff)}`',
        'diff[target[x]] -= 1': '`target[{x}] = {target[x]}`：和 target 的同值抵消 → `diff = {dict(diff)}`。剩下的正负数就是对不上的元素',
        'for y in g[x]': '依次看邻居（看完了就回到上一层）',
        'if not vis[y]': lambda S, B, r: (f'邻居 {S.y} 没访问 → 属于同一个连通块，继续 dfs' if not S.vis[S.y] else f'邻居 {S.y} 已访问，跳过'),
        'dfs(y)': '递归进入邻居 `{y}`',
        'vis = [False]': '`vis` 记录每个下标是否访问过',
        'ans = 0': '`ans` 累计各连通块「多出来的元素个数」',
        'for x in range(n)': lambda S, B, r: (f'枚举下标 `{S.x}`' if B.get('x') != S.x else '所有下标都枚举完了'),
        'if not vis[x]': lambda S, B, r: (f'下标 {S.x} 没访问过 → 一个新的连通块，从它开始 dfs' if not S.vis[S.x] else f'下标 {S.x} 已经在之前的连通块里，跳过'),
        'diff = defaultdict': '为这个连通块准备空的 `diff`',
        'dfs(x)': '从 `{x}` 出发 dfs，把整个连通块的元素都计入 `diff`',
        'ans += sum': '这个连通块：`diff = {dict(diff)}`，所有 |值| 之和 = `{sum(map(abs, diff.values()))}`（source 多出的 + target 多出的）→ `ans = {ans}`',
        'return ans // 2': 'source 多出的和 target 多出的一一配对，每对贡献 1 个汉明距离：`{ans} // 2 = {ret}`',
    },
    cards=dict(
        one_liner='连通块内元素可任意排列，只看「多出来」的元素',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`allowedSwaps[i] = [a, b]` 表示可以任意次交换 `source` 的这两个下标',
                 '汉明距离 = 对应位置不同的个数，求交换后 `source` 与 `target` 的最小汉明距离',
                 '本视频：`[1,2,3,4,5]`、`[3,1,1,5,5]`，边 `[0,1],[1,2],[3,4]` → `2`'],
        quote='G 的同一个连通块中的节点（下标）可以随意交换。……source 多了一个 1 和一个 3，target 多了一个 2 和一个 4，每对多出来的元素，无法匹配，会贡献 1 个汉明距离。',
        quote_src='—— 灵茶山艾府题解',
        idea=['allowedSwaps 当作边建图，连通块内下标可以任意重排',
              '块内 `source` 的值 +1，`target` 的值 −1：相同的值抵消，剩下的就是对不上的',
              '`sum(abs)` 同时数了 source 和 target 两边的多余元素，所以最后 `// 2`'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错：每个连通块要新建一个 `diff`，不能跨块累计',
                 '易错：`diff` 里正负两边都要算，答案是 `ans // 2`，不是 `ans`',
                 '相似题：1202 交换字符串中的元素（同样是连通块内任意排列）'],
    ),
)
