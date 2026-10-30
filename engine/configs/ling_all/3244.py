def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    qs = S['queries']
    n = S['n']
    fa = S.get('fa')
    k = len(S['ans']) if 'ans' in S else 0
    cur = (S['l'], S['r']) if 'l' in S and 'ans' in S and k < len(qs) else None
    cv.text((x0 + 18, y0 + 4), '城市（蓝 = 仍要走的边，灰 = 已合并，弧线 = 新增道路）', 22, T['muted'], bold=True)
    sx = x0 + 60
    step = (x1 - x0 - 120) / (n - 1)
    yb = y0 + (y1 - y0) * 0.5
    pos = [sx + i * step for i in range(n)]
    for i in range(n - 1):
        merged = fa is not None and i < len(fa) and fa[i] != i
        cv.arrow((pos[i] + 22, yb), (pos[i + 1] - 22, yb), T['dim'] if merged else T['blue'], 4 if not merged else 2, 12)
    for a, (u, v) in enumerate(qs):
        if a < k or (cur and (u, v) == cur):
            col = T['yellow'] if cur and (u, v) == cur and a == k else T['green']
            cv.arc_arrow((pos[u], yb - 24), (pos[v], yb - 24), (v - u) * step * 0.2, col, 4 if col == T['yellow'] else 3, 13)
    for i in range(n):
        cv.rect((pos[i] - 22, yb - 22, pos[i] + 22, yb + 22), fill=T['panel2'], outline=T['border'], r=22)
        cv.text((pos[i], yb), i, 26, T['text'], anchor='mm', bold=True, mono=True)
    if 'cnt' in S:
        cv.text((x0 + 18, y1 - 78), f"从 0 到 {n - 1} 还要走的边数 cnt = {S['cnt']}（= 并查集连通块数）", 26, T['text'], bold=True)
    if cur:
        cv.text((x0 + 18, y1 - 40), f"当前新增 {cur[0]} → {cur[1]}：把边 {cur[0]} … {cur[1] - 2} 合并到边 {cur[1] - 1}", 24, T['yellow'], bold=True)


CONFIG = dict(
    num=3244, title='新增道路查询后的最短距离 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='区间并查集 · 合并边',
    tags=['灵神题单', '常用数据结构', '难度分 2270'],
    code='''
class Solution:
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        fa = list(range(n - 1))

        # 非递归并查集
        def find(x: int) -> int:
            rt = x
            while fa[rt] != rt:
                rt = fa[rt]
            while fa[x] != rt:
                fa[x], x = rt, fa[x]
            return rt

        ans = []
        cnt = n - 1  # 并查集连通块个数
        for l, r in queries:
            fr = find(r - 1)
            i = find(l)
            while i < r - 1:
                cnt -= 1
                fa[i] = fr
                i = find(i + 1)
            ans.append(cnt)
        return ans
''',
    call='Solution().shortestDistanceAfterQueries(7, [[2,5],[3,5],[0,5]])',
    expect=[4, 4, 2],
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='fa', pointers={'i': 'blue', 'fr': 'pink'}, label='fa：节点 i 表示边 i→i+1', h=170,
             color=lambda S, i, v: 'pink' if i == S.get('fr') else None,
             dim=lambda S, i, v: v != i),
        dict(type='array', var='ans', label='ans', h=120, color=lambda S, i, v: 'green'),
    ],
    skip=['rt = x', 'ans = []', 'while fa[rt]', 'rt = fa[rt]', 'while fa[x]', 'fa[x], x = rt'],
    watch=['l', 'r', 'fr', 'i', ('cnt', 'cnt', 'green')],
    captions={
        'fa = list': '并查集的节点 `i` 代表==边== `i→i+1`，共 `n-1` 条边；起初每条边自成一块',
        'cnt = n - 1': '`cnt` = 并查集连通块数 = 从 0 走到 n-1 要走的边数，起初 `n-1`',
        'for l, r in queries': '新增一条捷径 `l→r`；题目保证不交叉，遇到捷径就走',
        'fr = find(r - 1)': '捷径相当于把边 `l ... r-2` 并到边 `r-1` 上。先找 `r-1` 所在块的根 `fr`',
        'i = find(l)': '从边 `l` 所在块的根开始：`i` = ==第一个还没被合并的边==',
        'while i < r - 1': lambda S, B, r_: (f'`i = {S.i} < r-1 = {S.r - 1}`：这条边还在捷径范围内，要被并走' if S.i < S.r - 1
                                              else f'`i = {S.i} >= r-1 = {S.r - 1}`：范围内的边都已合并，结束'),
        'cnt -= 1': '合并掉一条边 → 少走一步：`cnt` 减 1',
        'fa[i] = fr': '把边 `i` 并入 `r-1` 所在块：`fa[i] = fr`',
        'i = find(i + 1)': '跳到下一个还没合并的边，已合并的靠并查集==一步跳过==，所以每条边只被合并一次',
        'ans.append(cnt)': '处理完这条捷径，最短路长度 = `cnt` = =={cnt}==',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='捷径不交叉，遇到就走：把被跨过的边合并，连通块数就是最短路',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`n` 个城市，初始 `i → i+1` 有单向道路',
                 '依次新增道路 `u→v`（不会交叉），每次求 `0` 到 `n-1` 的最短距离',
                 '示例：`n=5, queries=[[2,4],[0,2],[0,4]]` → `[3,2,1]`'],
        quote='由于题目保证添加的边（捷径）不会交叉，从贪心的角度看，遇到捷径就走捷径是最优的。把目光放在边上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['并查集节点 `i` = 边 `i→i+1`；连 `L→R` 就是把边 `L…R-2` 合并到边 `R-1`',
              '合并的同时维护连通块数 `cnt`，它就是答案',
              '每条边只会被合并一次，`find(i+1)` 会跳过已合并的边'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '易错：并查集大小 `n-1`（边数），合并范围是 `l … r-2` 并入 `r-1`',
                 '代码里的 `r - 1` 就是「最后一条被捷径覆盖的边」',
                 '题解另有「记录跳转位置 nxt」的写法，同样 `O(n+q)`，本视频演示区间并查集',
                 '视频中 find 内部的循环（路径压缩）折叠为一步「返回根」',
                 '本视频示例：`n=7`，`queries=[[2,5],[3,5],[0,5]]` → `[4,4,2]`'],
    ),
)
