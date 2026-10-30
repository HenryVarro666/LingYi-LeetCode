EDGES = [[0, 1, 2], [1, 2, 5], [3, 4, 3], [2, 3, 7], [4, 5, 4]]
COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange', 'red']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _color(S, i, v):
    fa = S.get('fa')
    if fa is None:
        return None
    r = _root(fa, i)
    return COLS[r % len(COLS)] if any(_root(fa, j) == r and j != i for j in range(len(fa))) else None


def _info(S):
    fa = S.get('fa')
    if fa is None:
        return '倒推：先按 `time` 从大到小排序，再一条条把边加回图里'
    roots = sorted({_root(fa, i) for i in range(len(fa))})
    groups = ' '.join('{' + ','.join(str(i) for i in range(len(fa)) if _root(fa, i) == r) + '}' for r in roots)
    return f'`parts = {S["parts"]}`，`k = {S["k"]}`：{groups}'


def _edge(S):
    es = S.get('edges')
    if es is None:
        return ''
    t = S.get('t')
    if t is None or 'x' not in S:
        return '边（x, y, time）：' + '  '.join(f'({a},{b},{c})' for a, b, c in es)
    return '边（降序）：' + '  '.join(f'=={a},{b},{c}==' if (a, b, c) == (S['x'], S['y'], t) else f'({a},{b},{c})' for a, b, c in es)


CONFIG = dict(
    num=3608, title='包含 K 个连通分量需要的最小时间', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='离线倒推 + 并查集',
    tags=['七、并查集', '难度分 1893'],
    code='''
class Solution(object):
    def minTime(self, n, edges, k):
        
        if not edges:
            return 0

        edges.sort(key=lambda d:d[2], reverse=True)
        fa = [x for x in range(n)]
        parts = n

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y, t in edges:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                parts -= 1
                if parts < k:
                    return t
                fa[fa_x] = fa_y
        
        return 0
''',
    call=f'Solution().minTime(6, {EDGES}, 3)',
    expect=3,
    views=[
        dict(type='text', fn=_edge, size=24, h=60),
        dict(type='array', var='fa', label='fa（同色 = 同一个连通块）', color=_color, h=200,
             pointers={'fa_x': 'blue', 'fa_y': 'pink'}),
        dict(type='text', fn=_info, size=26, h=70),
    ],
    watch=[('parts', 'parts', 'green'), ('k', 'k', 'orange'), ('t', 't', 'yellow')],
    skip=['fa = [x for', 'parts = n'],
    captions={
        'if not edges': '先处理特例：没有边就直接返回 0；本例有 5 条边，继续',
        'edges.sort': '按 `time` ==从大到小==排序：删除顺序倒过来，就是加边顺序',
        'for x, y, t in edges': '取下一条边 `({x}, {y})`，时间 `t = {t}`',
        'fa_x = find': '找 `{x}` 的祖先 `fa_x`（带路径压缩）',
        'fa_y = find': '找 `{y}` 的祖先 `fa_y`',
        'if fa_x != fa_y': lambda S, B, r: (f'祖先 `{S.fa_x}` ≠ `{S.fa_y}`：两端点原来不连通 → 这条边会==合并==两块' if S.fa_x != S.fa_y
                                             else f'祖先都是 `{S.fa_x}`：早已连通，这条边不改变块数'),
        'parts -= 1': '合并了两块，`parts` 减一 → =={parts}==',
        'if parts < k': lambda S, B, r: (f'`parts = {S.parts} < k = {S.k}`：块数不够了 → ==这条边不能留==' if S.parts < S.k
                                          else f'`parts = {S.parts} ≥ k = {S.k}`：块数还够，继续加边'),
        'return t': '加上这条边就少于 `k` 块，所以必须删掉 `time <= {t}` 的边 → 答案 =={t}==',
        'fa[fa_x] = fa_y': '把 `{fa_x}` 的祖先改成 `{fa_y}`：两块并成一块',
        'return 0': '所有边加完块数仍 `>= k`：不用删边，答案 0',
        'fa[x] = find': '路径压缩：`fa[{x}]` 直接指向祖先',
    },
    cards=dict(
        one_liner='拆连通块很麻烦，倒推成加边就是并查集',
        complexity='时间 `O(m log m + m α(n))`，空间 `O(n)`',
        problem=['`n` 个点的无向图，边 `[u, v, time]` 在 `time` 时刻被移除',
                 '求最小 `t`，移除所有 `time <= t` 的边后至少有 `k` 个连通分量',
                 '本视频：`n=6`，5 条边，`k=3` → `3`'],
        quote='拆分连通分量是比较麻烦的，所以对于这类问题，如果可以离线处理，那么就可以离线倒推。',
        quote_src='—— yiduobo 题解原文',
        idea=['先假设所有点孤立，把删边顺序反过来：按 `time` 从大到小逐条==加边==',
              '用并查集维护连通性，`parts` 记录当前连通块数',
              '加到某条边使 `parts < k`，这条边的 `time` 就是答案；全加完还够就是 `0`'],
        summary=['时间 `O(m log m)`，空间 `O(n)`',
                 '只有 `fa_x != fa_y` 才合并并让 `parts` 减一，判断 `parts < k` 也在这里面',
                 '没有边时直接返回 `0`；全部加完仍 `>= k` 也返回 `0`',
                 '原文 Python 2 风格，在 Python 3 下无需改动',
                 '对比灵神：灵神把并查集封装成类；yiduobo 用嵌套 `find` 函数手写'],
    ),
)
