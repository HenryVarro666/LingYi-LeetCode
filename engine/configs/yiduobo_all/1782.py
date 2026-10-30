def _gtxt(S):
    if 'q' not in S or 'l' not in S or 'r' not in S or 'd' not in S:
        return ''
    l, r, d, q = S['l'], S['r'], S['d'], S['q']
    if l >= r:
        return f"`l >= r`：指针相遇，这个询问的双指针扫描结束，`res[-1] = {S['res'][-1]}`"
    return f"`d[l] + d[r] = {d[l]} + {d[r]} = {d[l] + d[r]}`，query = {q}；`l` 向右、`r` 向左，数「和 <= query」的不合法点对"


CONFIG = dict(
    num=1782, title='统计点对的数目', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='总点对数减去不合法 + 差分数组去重',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·图论算法', '难度分 2457'],
    code='''
class Solution(object):
    def countPairs(self, n, edges, queries):

        g = {}
        d = [0] * n
        for x, y in edges:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[x].get(y, 0) + 1
            g[y][x] = g[y].get(x, 0) + 1
            d[x] += 1
            d[y] += 1
        
        m = len(edges)
        delta = [0] * (m + 1)
        for x in g:
            for y in g[x]:
                if x < y:
                    delta[d[x] + d[y] - g[x][y]] -= 1
                    if d[x] + d[y] <= m:
                        delta[d[x] + d[y]] += 1
        
        f = [delta[0]]
        for index in range(1, m + 1):
            f.append(f[-1] + delta[index])

        d = sorted(d)
        res = []
        for q in queries:
            res.append(n * (n - 1) // 2 + f[q])
            l = 0
            r = n - 1
            while l < r:
                if d[l] + d[r] <= q:
                    res[-1] -= r - l
                    l += 1
                else:
                    r -= 1
        
        return res
''',
    call='Solution().countPairs(4, [[1,2],[2,4],[1,3],[2,3],[2,1]], [2, 3])',
    expect=[6, 5],
    skip=['x -= 1', 'y -= 1', 'if x not in g', 'if y not in g', 'g[x] = {}', 'g[y] = {}', 'g[y][x]', 'd[y] += 1',
          'for y in g[x]', 'if x < y', 'for x in g', 'if d[x] + d[y] <= m', 'while l < r', 'l = 0', 'r = n - 1', 'for index in range', 'for x, y in edges'],
    max_steps=90,
    views=[
        dict(type='map', var='g', h=170, fmt=lambda k, v: f'点 {k} 的邻居(重数)：{dict(sorted(v.items()))}'),
        dict(type='array', var='d', h=150, label='d[i]：与点 i 相连的边数（排序前下标 = 点号 - 1；排序后为升序；蓝 = l，粉 = r）',
             color=lambda S, i, v: ('blue' if i == S['l'] else 'pink' if i == S['r'] else None) if 'l' in S and 'r' in S and S.get('_line', 0) >= 33 else None),
        dict(type='array', var='delta', h=150, label='delta：差分数组（对 query 区间加减）'),
        dict(type='array', var='f', h=150, label='f[q]：去重后要修正的数量（delta 前缀和）'),
        dict(type='text', fn=_gtxt),
    ],
    watch=[('m', 'm', 'cyan'), ('q', 'q', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'g = {}': '`g[x][y]` 记 x、y 之间的边数（重边也算）',
        'd = [0]': '`d[x]` 是与 x 相连的边数',
        'g[x][y] = g[x].get': '边 `{x}-{y}`（点号已减 1）：`g[{x}][{y}] = {g[x][y]}`，`g[{y}][{x}]` 同步 +1',
        'd[x] += 1': '两端度数各加一：`d[{x}] = {d[x]}`，`d[{y}] = {d[y] + 1}`',
        'm = len': '`m` 是边数，差分数组长 `m + 1`：`d[x] + d[y]` 不会超过 `m`',
        'delta = [0]': '`delta` 记录：每对相连的 `(x, y)`（只在 `x < y` 时处理，每对一次；终点超过 `m` 就不用加回），query 落在哪个区间时要把答案减一',
        'delta[d[x] + d[y] - g[x][y]] -= 1': '`d[{x}] + d[{y}] = {d[x] + d[y]}`，重边 `{g[x][y]}` 条：query 在 `[{d[x] + d[y] - g[x][y]}, {d[x] + d[y] - 1}]` 时这一对其实不合法 → 区间起点处减一',
        'delta[d[x] + d[y]] += 1': '区间终点后一位 `{d[x] + d[y]}`（没超过 `m = {m}`）处加回来：`delta[{d[x] + d[y]}] += 1`',
        'f = [delta[0]]': '对 `delta` 求前缀和得到 `f`：`f[q]` = query 为 q 时要修正（减掉）的点对数（是个负数）',
        'f.append': '`f[{index}] = f[{index - 1}] + delta[{index}] = {f[-1]}`',
        'd = sorted': '度数排序，为了双指针',
        'res = []': ' 存每个 query 的答案',
        'for q in queries': '处理 query = {q}',
        'res.append': '先不管不合法的，假设所有点对：`n(n-1)/2 = {n * (n - 1) // 2}`，加上去重修正 `f[{q}] = {f[q]}` → `{res[-1]}`；再用双指针 `l = 0, r = n - 1` 减掉不合法的',
        'l = 0': '`l` 从最小度数开始',
        'r = n - 1': '`r` 从最大度数开始',
        'if d[l] + d[r] <= q': lambda S, B, ret: (
            f'`d[l] + d[r] = {S.d[S.l]} + {S.d[S.r]} = {S.d[S.l] + S.d[S.r]} <= {S.q}`：`l` 和 `l+1..r` 任何一个配都不合法' if S.d[S.l] + S.d[S.r] <= S.q
            else f'`d[l] + d[r] = {S.d[S.l]} + {S.d[S.r]} = {S.d[S.l] + S.d[S.r]} > {S.q}`：`r` 太大不会不合法，`r` 往左找'),
        'res[-1] -= r - l': '有 `(l, l+1) … (l, r)` 共 `r - l = {r - l}` 对不合法 → 从答案里去掉，`res[-1]` = {res[-1]}',
        'l += 1': '`d[l]` 变大 → 对应的 `r` 只会更小：`l` → {l}',
        'r -= 1': '`r` 左移到 {r}',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先数所有点对，减去 d[x]+d[y]<=q 的，再用差分数组修正重边',
        complexity='时间 `O(n log n + q(n + m))`，空间 `O(n + m)`',
        problem=['无向图（可能有重边），点对 `(a, b)` 的 `cnt` = 与 `a` 或 `b` 相连的边数',
                 '对每个 `queries[j]`，求 `cnt > queries[j]` 的点对数（`a < b`）',
                 '示例：`n=4, edges=[[1,2],[2,4],[1,3],[2,3],[2,1]], queries=[2,3]` → `[6,5]`'],
        quote='与x或y相连的边数就是d[x] + d[y] - g[x][y]……这里减去g[x][y]的原因是这部分边在计算d[x]和d[y]时都被计算了，也就是多计算了一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['先抛开去重：总共 `n(n-1)/2` 对，减去 `d[x]+d[y] <= q` 的，用排序后的双指针 `O(n)` 数出来',
              '`l` 右移时 `d[l]` 变大，配得上的 `r` 只会变小，所以 `r` 只左移',
              '去重：有边的一对，在 `q` 属于 `[d[x]+d[y]-g, d[x]+d[y]-1]` 时要少算一对，用差分数组 + 前缀和 `f[q]`'],
        summary=['时间 `O(n log n + q(n+m))`，空间 `O(n + m)`',
                 '原文为 Python 2 写法，`n * (n - 1) /2` 的整数除法已改为 `//`',
                 '易错：`delta` 区间终点 `d[x]+d[y]` 可能超过 `m`，要判断越界再加',
                 '对比灵神方法二：灵神按度数计数，不同度数只有 `O(根号 m)` 种；yiduobo 用总数减不合法'],
    ),
)
