def _layout(g, n):
    """简单树布局：叶子按 dfs 序等距排开，父节点在子节点中间；返回 {i: (列坐标, 深度)}"""
    pos, cnt = {}, [0]

    def go(x, d):
        ch = g[x]
        if not ch:
            pos[x] = (cnt[0], d)
            cnt[0] += 1
        else:
            for y in ch:
                go(y, d + 1)
            pos[x] = ((pos[ch[0]][0] + pos[ch[-1]][0]) / 2, d)
    go(0, 0)
    return pos, cnt[0]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g, vals, n = S.get('g'), S.get('vals'), S.get('n')
    cv.text((x0 + 18, y0 + 4), '树（黄 = 正在 dfs；青色 k = 挂在该节点的询问）', 22, T['muted'], bold=True)
    if g is None or vals is None:
        return
    pos, w = _layout(g, n)
    dmax = max(d for _, d in pos.values())
    gx = (x1 - x0 - 120) / max(1, w - 1) if w > 1 else 0
    gy = min(110, (y1 - y0 - 160) / max(1, dmax))
    P = {i: (x0 + 60 + c * gx, y0 + 100 + d * gy) for i, (c, d) in pos.items()}
    for i in range(n):
        for y in g[i]:
            cv.line([P[i], P[y]], T['border'], 3)
    cur = S.get('x')
    qs = S.get('qs')
    for i in range(n):
        X, Y = P[i]
        hot = (i == cur)
        cv.rect((X - 28, Y - 24, X + 28, Y + 24), fill=T['yellow'] if hot else T['panel2'], outline=T['border'], r=24)
        cv.text((X, Y), i, 28, T['bg'] if hot else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 30), f'v={vals[i]}', 18, T['muted'], anchor='mt', mono=True)
        if qs and qs[i]:
            cv.text((X + 32, Y - 30), ','.join(f'k={k}' for k, _ in qs[i]), 18, T['cyan'], anchor='lm', bold=True)


CONFIG = dict(
    num=3590, title='第 K 小的路径异或和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='离线 DFS + 启发式合并',
    tags=['难度分 2646'],
    setup='''
class SortedSet(list):  # 演示用的最小实现，行为同 sortedcontainers.SortedSet（本题只用到 构造 / |= / len / 下标）
    def __init__(self, it=()):
        super().__init__(sorted(set(it)))

    def __ior__(self, other):
        for x in other:
            i = bisect.bisect_left(self, x)
            if i == len(self) or self[i] != x:
                self.insert(i, x)
        return self
''',
    code='''
class Solution:
    def kthSmallest(self, par: List[int], vals: List[int], queries: List[List[int]]) -> List[int]:
        n = len(par)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[par[i]].append(i)

        qs = [[] for _ in range(n)]
        for i, (x, k) in enumerate(queries):
            qs[x].append((k, i))

        ans = [-1] * len(queries)

        def dfs(x: int, xor: int) -> SortedSet:
            xor ^= vals[x]

            st = SortedSet([xor])
            for y in g[x]:
                set_y = dfs(y, xor)
                # 启发式合并：小集合并入大集合
                if len(set_y) > len(st):
                    st, set_y = set_y, st
                st |= set_y

            for k, qi in qs[x]:
                if k - 1 < len(st):
                    ans[qi] = st[k - 1]

            return st

        dfs(0, 0)
        return ans
''',
    call='Solution().kthSmallest([-1,0,0,1,1], [1,2,3,1,2], [[0,2],[1,3],[1,4]])',
    expect=[2, 3, -1],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='st', label='st：当前子树的有序集合（不同的路径异或和）', h=100, cell=70),
        dict(type='array', var='set_y', label='set_y：刚从儿子返回的集合', h=100, cell=70),
        dict(type='calls', label='dfs 调用栈', h=150),
    ],
    watch=['x', 'xor', 'k', ('ans', 'ans', 'green')],
    skip=[3, 4, 5, 6, 9, 10, 12, 8, 'n = len(par)'],
    max_steps=110,
    captions={
        'g = [[] for': '先建好「儿子列表」`g`，下面按父子关系 dfs',
        'qs = [[]': '==离线==：把询问按节点 `u` 分组，一边 dfs 一边回答，不必按输入顺序',
        'qs[x].append': '询问 `(k, 编号)` 挂到节点 `{x}` 上（树图里青色 `k=` 标出）',
        'ans = [-1]': '`ans` 先全填 -1：子树里不同异或和不够 `k` 个时就是 -1',
        'dfs(0, 0)': '从根 `0` 开始 dfs，`xor` 一路带着「根到当前节点的路径异或和」',
        'xor ^= vals[x]': '路径异或和 `s({x})` = 父节点的 `xor` ^ `vals[{x}]` = =={xor}==（==从 0 出发==，不是从询问的 u 出发）',
        'st = SortedSet([xor])': '节点 `{x}` 子树的有序集合先放自己的 `s = {xor}`',
        'for y in g[x]': lambda S, B, ret: ('枚举儿子 `y = {}`'.format(S.y) if 'y' in S and S.get('y') is not None and S.y in S.g[S.x] and S.get('_line') == 18 and B.get('y') != S.y else '儿子都处理完了'),
        'set_y = dfs(y, xor)': '递归处理儿子 `{y}`，拿回它子树的有序集合',
        'if len(set_y) > len(st)': '`set_y` 有 `{len(set_y)}` 个，`st` 有 `{len(st)}` 个 → {"set_y 更大，要交换" if len(set_y) > len(st) else "st 不小，直接把 set_y 并进来"}',
        'st, set_y = set_y, st': '==启发式合并==：交换，让 `st` 始终是大的那个，只搬小集合的元素',
        'st |= set_y': '把小集合 `set_y` 的元素逐个加进大集合：`st = {list(st)}`（每个元素最多被搬 `O(log n)` 次）',
        'for k, qi in qs[x]': lambda S, B, ret: ('子树 `{}` 的集合已完整 = `{}`，现在回答挂在它上面的询问'.format(S.x, list(S.st)) if S.get('qi') is not None and B.get('qi') != S.qi else '节点 `{}` 的询问回答完了'.format(S.x)),
        'if k - 1 < len(st)': '要第 `{k}` 小，集合有 `{len(st)}` 个：{"够，取下标 k-1" if k - 1 < len(st) else "不够 → 保持 -1"}',
        'ans[qi] = st[k - 1]': '第 `{k}` 小 = `st[{k - 1}]` = =={st[k - 1]}==，记入 `ans[{qi}]`',
        'return st': '返回 `{list(st)}`，让父节点去合并',
        'return ans': '全部回答完：`{ans}`',
    },
    cards=dict(
        one_liner='离线 dfs：子树集合从下往上合并，小的并进大的',
        complexity='时间 `O(n log²n + q log n)`，空间 `O(n + q)`',
        problem=['有根树（根 `0`），节点 `i` 有值 `vals[i]`；`s(x)` = 根到 `x` 路径上 `vals` 的异或',
                 '询问 `[u, k]`：`u` 的子树里，所有 `s(z)` 去重后的第 `k` 小；不够 `k` 个返回 -1',
                 '示例：`par=[-1,0,0,1,1]`，`vals=[1,2,3,1,2]`，询问 `[0,2] [1,3] [1,4]` → `[2,3,-1]`'],
        quote='离线，把询问按照 u 分组，这样我们可以一边 DFS 这棵树，一边回答询问。……启发式合并：每次把小的集合合并到大的集合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s(x)` 是从根 `0` 出发的路径异或和，dfs 时顺手带着 `xor` 往下传',
              '子树 `x` 的答案 = 自己的 `s` + 各儿子子树的集合（去重）→ 有序集合，第 `k` 小就是 `st[k-1]`',
              '启发式合并：小集合并入大集合，每个元素至多被搬 `O(log n)` 次，总共 `O(n log n)` 次插入'],
        summary=['时间 `O(n log²n + q log n)`，空间 `O(n + q)`',
                 '路径异或和一定从根 `0` 起算，而不是从询问的 `u` 起算',
                 '合并前先比大小、必要时交换；回答询问要在合并完所有儿子之后',
                 '题解另有两种写法：dfs 时间戳 + 莫队 + 树状数组 / 分块求第 k 小，见原题解',
                 '原文用 sortedcontainers.SortedSet，视频里用等价的小 SortedSet 代替'],
    ),
)
