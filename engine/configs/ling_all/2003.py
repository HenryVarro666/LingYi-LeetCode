# ---- 通用的一般树画法：按 parents 数组布局，节点带颜色/外圈/下标注
def _gt_layout(parents):
    n = len(parents)
    ch = [[] for _ in range(n)]
    for i in range(1, n):
        ch[parents[i]].append(i)
    depth, xs, cnt = [0] * n, [0.0] * n, [0]

    def go(u, d):
        depth[u] = d
        if not ch[u]:
            xs[u] = cnt[0]
            cnt[0] += 1
        else:
            for v in ch[u]:
                go(v, d + 1)
            xs[u] = (xs[ch[u][0]] + xs[ch[u][-1]]) / 2
    go(0, 0)
    return ch, depth, xs, max(cnt[0], 1), max(depth) + 1


def gtree_draw(cv, box, T, parents, label, fill=None, ring=None, under=None, edge=None, edge_label=None, title=''):
    x0, y0, x1, y1 = box
    n = len(parents)
    ch, depth, xs, nleaf, nd = _gt_layout(parents)
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    sp = min(130, (x1 - x0 - 80) / max(1, nleaf))
    dy = min(120, (y1 - y0 - 125) / max(1, nd - 1))
    rad = max(18, min(30, sp * 0.36, dy * 0.3))
    sx = x0 + (x1 - x0 - sp * (nleaf - 1)) / 2
    P = {u: (sx + xs[u] * sp, y0 + 80 + depth[u] * dy) for u in range(n)}
    for u in range(1, n):
        a, b = P[parents[u]], P[u]
        ec = edge(u) if edge else None
        cv.line([a, b], T[ec] if ec else T['border'], 6 if ec else 3)
        if edge_label:
            s = edge_label(u)
            if s is not None:
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                w = cv.tlen(str(s), 18, bold=True) + 10
                cv.rect((mx - w / 2, my - 12, mx + w / 2, my + 12), fill=T['bg'], r=6)
                cv.text((mx, my), str(s), 18, T['muted'], anchor='mm', bold=True)
    for u in range(n):
        X, Y = P[u]
        f = fill(u) if fill else None
        rc = ring(u) if ring else None
        if rc:
            cv.rect((X - rad - 6, Y - rad - 6, X + rad + 6, Y + rad + 6), outline=T[rc], width=5, r=rad + 6)
        cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=T[f] if f else T['panel2'], outline=T['border'], r=rad)
        cv.text((X, Y), str(label(u)), 26, T['bg'] if f else T['text'], anchor='mm', bold=True)
        cv.text((X + rad + 6, Y - rad * 0.4), f'#{u}', 15, T['dim'], anchor='lm', mono=True)
        if under:
            s = under(u)
            if s:
                cv.text((X, Y + rad + 8), s, 19, T['green'], anchor='mt', bold=True)
    return P
PARENTS = [-1, 0, 1, 0, 3, 3]
NUMS = [5, 4, 6, 2, 1, 3]


def _draw(cv, S, B, box, T):
    n = len(PARENTS)
    vis = S.get('vis') or [False] * (n + 2)
    ans = S.get('ans') or [1] * n
    node, x = S.get('node'), S['_inner'].get('x')
    node = node if isinstance(node, int) and node >= 0 else None

    def fill(i):
        return 'green' if vis[min(NUMS[i], n + 1)] else None

    def ring(i):
        if i == x:
            return 'pink'
        if i == node:
            return 'blue'
        return None
    gtree_draw(cv, box, T, PARENTS, lambda i: NUMS[i], fill, ring,
               lambda i: f'ans {ans[i]}' if ans[i] != 1 else None,
               title='家族树（圈内 = 基因值，绿 = 已标记，蓝环 = node，粉环 = 正在遍历的 x）')


def _g(S):
    return S['nums'][S['node']] if S.get('node', -1) >= 0 else None


CONFIG = dict(
    num=2003, title='每棵子树内缺失的最小基因值', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='从基因值 1 出发往上走 · mex',
    tags=['链表树与回溯', '难度分 2415'],
    code='''
class Solution:
    def smallestMissingValueSubtree(self, parents: List[int], nums: List[int]) -> List[int]:
        n = len(parents)
        ans = [1] * n
        if 1 not in nums:  # 不存在基因值为 1 的节点
            return ans

        # 建树
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parents[i]].append(i)

        vis = [False] * (n + 2)
        mex = 2  # 缺失的最小基因值
        pre = -1
        node = nums.index(1)  # 出发点
        while node >= 0:
            vis[min(nums[node], n + 1)] = True  # 标记基因值
            nodes = [son for son in g[node] if son != pre]
            while nodes:
                x = nodes.pop()
                vis[min(nums[x], n + 1)] = True  # 标记基因值
                nodes.extend(g[x])  # 保存接下来需要遍历的点
            while vis[mex]:  # node 子树包含这个基因值
                mex += 1
            ans[node] = mex  # 缺失的最小基因值
            pre = node  # 下一轮循环不会遍历 pre 子树
            node = parents[node]  # 往上走
        return ans
''',
    call='Solution().smallestMissingValueSubtree([-1,0,1,0,3,3], [5,4,6,2,1,3])',
    expect=[7, 1, 1, 4, 2, 1],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='list(map(int, vis))', label='vis[基因值]（1 = 子树里出现过）', pointers={'mex': 'pink'}, cell=64, h=150),
        dict(type='array', var='nodes', label='nodes（待遍历的节点栈）', cell=64, h=110),
        dict(type='array', var='ans', label='ans', cell=64, h=120),
    ],
    watch=[('node', 'node', 'blue'), ('pre', 'pre'), ('mex', 'mex', 'pink'), ('x', lambda S: S['_inner'].get('x'))],
    captions={
        'if 1 not in nums': '基因值 `1` 在树里吗？{"在" if 1 in nums else "不在"} → ' + '{"继续" if 1 in nums else "所有子树都缺 1，直接返回全 1"}',
        'ans = [1] * n': '先假设每棵子树都缺 `1`：只有包含基因值 `1` 的子树答案才会变大',
        'g[parents[i]].append': '`{i}` 是 `{parents[i]}` 的儿子：建好「父 → 儿子」的邻接表',
        'vis = [False]': '`vis[v]` 记录基因值 `v` 是否出现；答案最大 `n+1`，所以开 `n+2` 格就够了',
        'mex = 2': '`mex` 从 `2` 开始：因为一定会访问到基因值 `1` 的节点，`1` 肯定在里面',
        'node = nums.index': '出发点 = 基因值 `1` 的节点 `{node}`：==只有它的祖先链上的子树才包含 1==，其余答案都是 `1`',
        'vis[min(nums[node]': '`node = {node}`：基因值 `{nums[node]}` 标记进 `vis`',
        'nodes = [son': '`node` 的儿子里除掉 `pre = {pre}`（它的子树上一轮已经遍历过）→ 待访问 `{nodes}`',
        'x = nodes.pop()': '取出节点 `{x}` 来访问',
        'vis[min(nums[x]': '节点 `{x}` 的基因值 `{nums[x]}` 标记进 `vis`',
        'nodes.extend': '把 `{x}` 的儿子 `{g[x]}` 也放进待访问栈 → `{nodes}`',
        'while nodes': lambda S, B, r: ('栈里还有节点，继续遍历这棵子树' if S.nodes else '子树遍历完毕：当前 `node` 子树的基因值都标好了'),
        'while vis[mex]': '`vis[{mex}]` 是 {vis[mex]} → ' + '{"这个基因值子树里有，mex 往后找" if vis[mex] else "子树里没有 mex → 它就是缺失的最小基因值"}',
        'mex += 1': '`mex` 不重置！上面的子树是下面的超集，答案只增不减 → `mex = {mex}`',
        'ans[node] =': '`ans[{node}] = {mex}`：以 `{node}` 为根的子树缺失的最小基因值',
        'pre = node': '记下 `pre = {node}`，往上走后不再重复遍历它的子树',
        'node = parents': '往上走一步：`node` 从 `{B.node}` 变成父节点 `{node}`' + '{"（到根之上，结束）" if node < 0 else ""}',
        'return ans': '其余节点的子树不含基因值 1，答案本来就是 `1` → 返回 `{ret}`',
    },
    skip=['for i in range(1, n)', 'pre = -1', 'g[parents[i]].append'],
    max_steps=90,
    cards=dict(
        one_liner='基因值 1 只有一个：只有它的祖先链上的答案不是 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['家族树，`parents[i]` 是 `i` 的父亲；`nums[i]` 是各不相同的基因值',
                 '求每棵子树里缺失的最小正整数基因值',
                 '示例：`parents=[-1,0,1,0,3,3]`，`nums=[5,4,6,2,1,3]`',
                 '输出 `[7,1,1,4,2,1]`'],
        quote='下面节点的基因值集合，一定是上面节点的基因值集合的子集。所以上面节点的 ans 值一定大于等于下面节点的 ans 值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['基因值互不相同 → `1` 只出现一次，不含 `1` 的子树答案都是 `1`',
              '从 `1` 所在节点一路往上走，子树越来越大，==每个节点只遍历一次==',
              '`mex` 不用重置，接着上一次往后找，总共最多加 `n` 次'],
        result='返回 `[7,1,1,4,2,1]`：只有 `4 → 3 → 0` 这条链上的答案不是 1',
        summary=['时间 `O(n)`：每个节点只访问一次，`mex` 总共只增不减',
                 '易错：别忘了 `1` 不在 `nums` 里时直接全返回 `1`',
                 '大于 `n+1` 的基因值用 `min(..., n+1)` 压进长 `n+2` 的数组',
                 '写法一用 DFS + 哈希表，写法二用手动栈；本视频演示最后的「栈 + 数组」写法'],
    ),
)
