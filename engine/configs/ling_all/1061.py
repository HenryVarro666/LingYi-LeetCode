def _root(fa, c):
    while fa[c] != c:
        c = fa[c]
    return c


def _groups(S):
    fa = S.get('fa')
    if not fa:
        return ''
    g = {}
    for c in sorted(fa):
        g.setdefault(_root(fa, c), []).append(c)
    parts = [f"[{r}: {''.join(m)}]" for r, m in sorted(g.items()) if len(m) > 1]
    return '合并出的小组（代表元：成员）  ' + ('　'.join(parts) if parts else '（暂时都是单独一个字母）')


def _links(S):
    fa = S.get('fa')
    if not fa:
        return ''
    ch = [f'{c}→{fa[c]}' for c in sorted(fa) if fa[c] != c]
    return '`fa` 中不指向自己的：' + ('　'.join(ch) if ch else '（无）')


CONFIG = dict(
    num=1061, title='按字典序排列最小的等效字符串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='并查集 · 小的当代表元',
    tags=[],
    setup='from string import ascii_lowercase',
    code='''
class Solution:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        fa = {c: c for c in ascii_lowercase}

        def find(x: str) -> str:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        def merge(x: str, y: str) -> None:
            small, big = sorted((find(x), find(y)))
            fa[big] = small  # 把大的代表元指向小的代表元

        for x, y in zip(s1, s2):
            merge(x, y)

        return ''.join(find(c) for c in baseStr)
''',
    call='Solution().smallestEquivalentString("abc", "cde", "eed")',
    expect='aab',
    views=[
        dict(type='string', var='s1', label='s1（上）与 s2（下）：同一列的两个字母等价', h=110),
        dict(type='string', var='s2', label='', h=90),
        dict(type='text', fn=_groups, size=24, h=60),
        dict(type='text', fn=_links, size=24, h=60),
        dict(type='calls', h=130),
    ],
    watch=[('small', lambda S: S['_inner'].get('small'), 'green'), ('big', lambda S: S['_inner'].get('big'), 'orange')],
    captions={
        'fa = {c: c': '26 个字母各自是一个集合：`fa[c] = c`，自己就是自己的代表元',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}` 不是自己 → 还没到代表元，继续往上找' if S.fa[S.x] != S.x else f'`{S.x}` 就是代表元，直接返回'),
        'fa[x] = find': '找到根后==路径压缩==：沿途的点直接指向代表元，下次 `find` 更快',
        'return fa[x]': '`find({x})` 返回代表元 `{ret}`',
        'small, big = sorted': '`x` 的代表元和 `y` 的代表元排序：`small = {small}`，`big = {big}`',
        'fa[big] = small': '把大的代表元指向小的：`fa[{big}] = {small}`，==代表元永远是组内最小字母==（若本来同组则不变）',
        'for x, y in zip': lambda S, B, r: (f'取一对等价字母 `{S.x} == {S.y}`' if B.get('x') != S.x else '所有等价对都合并完了'),
        'merge(x, y)': '合并 `{x}` 和 `{y}` 所在的组',
        'return \'\'.join': '每个字母换成自己所在组的代表元（= 组内最小字母）：对 `baseStr` 逐个 `find`',
    },
    cards=dict(
        one_liner='字母连边成图，合并时让小的当代表元',
        complexity='时间 `O(n + m)`，空间 `O(|Σ|)`，|Σ| = 26',
        problem=['`s1[i]` 与 `s2[i]` 是等价字符，等价关系满足自反、对称、传递',
                 '把 `baseStr` 的每个字母换成等价字母，使字典序最小',
                 '本视频：`s1 = "abc"`，`s2 = "cde"`，`baseStr = "eed"` → `"aab"`'],
        quote='在 s1[i] 和 s2[i] 之间连边，可以得到一个有 26 个节点的图。……用并查集实现更简单：只需在合并的时候，把大的代表元指向小的代表元。',
        quote_src='—— 灵茶山艾府题解',
        idea=['等价字母 = 连通块；`c` 要变成它所在连通块的最小字母',
              '用并查集，规定代表元就是块内最小字母：合并时 `fa[大] = 小`',
              '最后对 `baseStr` 每个字母 `find` 一下，就是答案'],
        summary=['时间 `O(n + m)`：字母只有 26 种，并查集操作视为 `O(1)`',
                 '关键：`sorted((find(x), find(y)))` 拿到两个代表元，大的指向小的',
                 '也可以建图后 DFS 求每个连通块的最小字母，并查集写起来更短',
                 '示例：分成 `{a,c,e}` 和 `{b,d}` 两组，`eed` → `aab`'],
    ),
)
