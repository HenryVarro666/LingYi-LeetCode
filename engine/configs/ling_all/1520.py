def _lr(S):
    """当前关注的区间 [l, r]（l 为 inf 时没有）"""
    l, r = S.get('l'), S.get('r')
    if l is None or r is None or l == float('inf') or l > r:
        return None
    return int(l), int(r)


def _s_color(S, i, v):
    lr = _lr(S)
    if lr and lr[0] <= i <= lr[1]:
        return 'yellow'
    return None


def _top(S):
    lr = _lr(S)
    line = S.get('_line')
    if 'pre_r' in S:
        return f"选区间：`pre_r = {S['pre_r']}`，已选 `{S.get('ans', [])}`"
    if 'vis' in S and 'intervals' in S:
        return f"以字母 `{S['i']}` 为起点做 DFS，合并出的区间 `[{lr[0]}, {lr[1]}]`" if lr else f"以字母 `{S['i']}` 为起点做 DFS"
    if 'i' in S and 'l' in S and 'g' in S:
        if line == 17 and 'j' in S:
            return f"字母 `{S['i']}` 的区间 `[{S['l']}, {S['r']}]` 里有没有字母 `{S['j']}`？有就连边 `{S['i']}→{S['j']}`"
        return f"字母 `{S['i']}` 的最左、最右位置 `[{S['l']}, {S['r']}]`：区间里出现的别的字母都要连边"

    return '先记录位置，再建「包含」关系的有向图'


CONFIG = dict(
    num=1520, title='最多的不重叠子字符串', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='有向图 DFS 求区间 + 不相交区间贪心',
    tags=['灵神题单·贪心与思维', '贪心算法', '难度分 2363'],
    code='''
class Solution:
    def maxNumOfSubstrings(self, s: str) -> List[str]:
        # 记录每种字母的出现位置
        pos = defaultdict(list)
        for i, b in enumerate(s):
            pos[b].append(i)

        # 构建有向图
        g = defaultdict(list)
        for i, p in pos.items():
            l, r = p[0], p[-1]
            for j, q in pos.items():
                if j == i:
                    continue
                k = bisect_left(q, l)
                # [l, r] 包含第 j 个小写字母
                if k < len(q) and q[k] <= r:
                    g[i].append(j)

        # 遍历有向图
        def dfs(x: str) -> None:
            nonlocal l, r
            vis.add(x)
            p = pos[x]
            l = min(l, p[0])  # 合并区间
            r = max(r, p[-1])
            for y in g[x]:
                if y not in vis:
                    dfs(y)

        intervals = []
        for i, p in pos.items():
            # 如果要包含第 i 个小写字母，最终得到的区间是什么？
            vis = set()
            l, r = inf, 0
            dfs(i)
            intervals.append((l, r))

        # 435. 无重叠区间
        # 直接计算所选子串
        ans = []
        intervals.sort(key=lambda x: x[1])
        pre_r = -1
        for l, r in intervals:
            if l > pre_r:
                ans.append(s[l: r + 1])
                pre_r = r
        return ans
''',
    call='Solution().maxNumOfSubstrings("abbac")',
    expect=['bb', 'c'],
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='string', var='s', label='s（黄 = 当前区间 [l, r]）', cell=84, h=130, color=_s_color),
        dict(type='map', var='pos', label='pos：每个字母出现的位置', h=110, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var='g', label='g：有向图（i → 区间里出现的字母 j）', h=110, fmt=lambda k, v: f'{k} → {v}'),
        dict(type='array', var='intervals', label='intervals：每个字母对应的最终区间', h=170, cell=110, index=False),
        dict(type='calls', h=100),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('l', 'l', 'orange'), ('r', 'r', 'pink'), ('pre_r', 'pre_r', 'purple'), ('ans', 'ans', 'green')],
    skip=['for i, b in enumerate', 'pos[b].append(i)', 'continue', 'for j, q in pos.items()', 'if j == i', 'k = bisect_left', 'p = pos[x]'],
    max_steps=80,
    captions={
        'pos = defaultdict': '遍历 s，记下每个字母出现的所有下标（列表天然有序，方便二分）',
        'g = defaultdict': '建图：若字母 i 的区间 `[最左, 最右]` 里含字母 j，连==有向边 i → j==（选 i 就必须选 j）',
        'l, r = p[0], p[-1]': '字母 `{i}` 的最左、最右位置：`[l, r] = [{l}, {r}]`',
        'if j == i': lambda S, B, ret: ('同一个字母，跳过' if S.j == S.i else f'`j = {S.j}` 是另一个字母，检查它是否在 `[{S.l}, {S.r}]` 内'),
        'k = bisect_left': '二分：字母 `{j}` 的位置 `{q}` 中第一个 `>= l = {l}` 的下标 `k = {k}`',
        'if k < len(q)': lambda S, B, ret: (f'字母 `{S.j}` 的位置 `{S.q}` 里，二分得第一个 `>= {S.l}` 的是 `q[{S.k}] = {S.q[S.k]}`，`<= r = {S.r}` → 区间里有 `{S.j}`，==连边 {S.i}→{S.j}==' if S.k < len(S.q) and S.q[S.k] <= S.r
                                            else f'字母 `{S.j}` 在 `[{S.l}, {S.r}]` 里一个都没有 → 不连边（有向边：选 {S.i} 才必须选 {S.j}，反之不一定）'),
        'g[i].append(j)': '`g[{i}] = {g[i]}`',
        'intervals = []': '接下来：对每个字母 i，==从 i 出发 DFS==，所有能走到的字母区间取并集',
        'vis = set()': '换一个起点，重新记录访问过的字母',
        'l, r = inf, 0': '合并区间的初值：`l = inf`，`r = 0`',
        'dfs(i)': '从字母 `{i}` 出发 DFS',
        'vis.add(x)': '访问字母 `{x}`',
        'l = min(l, p[0])': '合并区间左端：`l = min({B.l}, {p[0]}) = {l}`',
        'r = max(r, p[-1])': '合并区间右端：`r = max({B.r}, {p[-1]}) = {r}`',
        'for y in g[x]': lambda S, B, ret: (f'字母 `{S.x}` 没有出边，这条路走完' if not S.g[S.x] else f'`{S.x}` 的出边都走完了，DFS 返回' if S.get('y') is not None and B.get('y') == S.y else f'沿边走：字母 `{S.x}` 的出边 `{S.g[S.x]}`'),
        'if y not in vis': lambda S, B, ret: (f'`{S.y}` 没访问过 → 递归' if S.y not in S.vis else f'`{S.y}` 已访问过 → 跳过'),
        'intervals.append': '字母 `{i}` 对应的最终区间 `({l}, {r})`，至多 26 个',
        'ans = []': '问题变成 435：最多选多少个互不重叠的区间。直接记下所选子串',
        'intervals.sort': '==按右端点排序==，右端点小的先选，给后面留更多空间',
        'pre_r = -1': '`pre_r` 是上一个已选区间的右端点',
        'for l, r in intervals': lambda S, B, ret: ('区间都看完了' if (B.get('l'), B.get('r')) == (S.l, S.r) and 'pre_r' in B and B.pre_r >= 0 else f'看区间 `[{S.l}, {S.r}]`'),
        'if l > pre_r': lambda S, B, ret: (f'`l = {S.l} > pre_r = {S.pre_r}` → 和已选区间不重叠，选它' if S.l > S.pre_r
                                           else f'`l = {S.l} <= pre_r = {S.pre_r}` → 和已选区间重叠，跳过'),
        'ans.append': '选中子串 `"{ans[-1]}"`',
        'pre_r = r': '`pre_r = {pre_r}`',
        'return ans': '所有选中的子串：=={ret}==',
    },
    cards=dict(
        one_liner='每个字母扩成最小合法区间，再做不相交区间贪心',
        complexity='时间 `O(n + |Σ|^2 log n)`，空间 `O(n + |Σ|^2)`',
        problem=['在小写字母串 `s` 中选最多的==互不重叠==子串；子串含某字母，就必须含 `s` 里该字母的全部',
                 '数量相同时选总长度最短的',
                 '本视频：`"abbac"` → `["bb", "c"]`（题目示例 `"abbaccd"` 同理）'],
        quote='如果子串包含字母 a，那么最左边的 a 和最右边的 a 一定要在子串中。……为了方便分析，把上述问题用有向图建模：如果区间 A 包含字母 b，那么连一条从 a 到 b 的有向边。',
        quote_src='—— 灵茶山艾府题解',
        idea=['含 `a` 就要含 `a` 的最左和最右；区间里又出现 `b`，就也要含 `b` 的全部 → ==a → b 的有向边==',
              '从字母 `i` DFS，所有能到的字母的区间并集，就是包含 `i` 的最小子串',
              '至多 26 个区间，问题变成 435：选最多互不重叠区间，按右端点排序贪心'],
        summary=['时间 `O(n + |Σ|^2 log n)`，空间 `O(n + |Σ|^2)`',
                 '边是==有向==的：`s = "aba"`，选 a 必须含 b，选 b 却不必含 a',
                 '按右端点排序、右端点小的先选，所以同数量时总长度最短',
                 '同样的做法可用于 3458（选 k 个特殊子串），只需多去掉整个 s 的区间'],
    ),
)
