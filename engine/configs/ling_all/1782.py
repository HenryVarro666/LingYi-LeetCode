CONFIG = dict(
    num=1782, title='统计点对的数目', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='度数计数 + 贡献法 + 后缀和',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·图论算法', '难度分 2457'],
    code='''
class Solution:
    def countPairs(self, n: int, edges: List[List[int]], queries: List[int]) -> List[int]:
        deg = [0] * (n + 1)
        cnt_e = dict()  # 比 Counter 快一点
        for x, y in edges:
            if x > y: x, y = y, x
            deg[x] += 1
            deg[y] += 1
            cnt_e[(x, y)] = cnt_e.get((x, y), 0) + 1
        cnt_deg = Counter(deg[1:])

        # 2)
        cnts = [0] * (max(deg) * 2 + 2)
        for deg1, c1 in cnt_deg.items():
            for deg2, c2 in cnt_deg.items():
                if deg1 < deg2:
                    cnts[deg1 + deg2] += c1 * c2
                elif deg1 == deg2:
                    cnts[deg1 + deg2] += c1 * (c1 - 1) // 2

        # 3)
        for (x, y), c in cnt_e.items():
            s = deg[x] + deg[y]
            cnts[s] -= 1
            cnts[s - c] += 1

        # 4) 计算 cnts 的后缀和
        for i in range(len(cnts) - 1, 0, -1):
            cnts[i - 1] += cnts[i]

        for i, q in enumerate(queries):
            queries[i] = cnts[min(q + 1, len(cnts) - 1)]
        return queries
''',
    call='Solution().countPairs(4, [[1,2],[2,4],[1,3],[2,3],[2,1]], [2, 3])',
    expect=[6, 5],
    skip=['if x > y', 'deg[y] += 1', 'for deg2, c2', 'elif deg1 == deg2', 'for i in range(len(cnts)', 'for x, y in edges', 'cnt_e[(x, y)]', 'for (x, y), c', 'cnts[s] -= 1', 'for i, q in enumerate', 'for deg1, c1'],
    max_steps=90,
    views=[
        dict(type='array', var='deg', h=160, label='deg[i]：与点 i 相连的边数（下标 0 不用）',
             color=lambda S, i, v: 'yellow' if 'x' in S and '_line' in S and S['_line'] in (6, 7, 8) and i in (S['x'], S['y']) else None),
        dict(type='map', var='cnt_e', h=120, fmt=lambda k, v: f'{k[0]}-{k[1]}  出现 {v} 次'),
        dict(type='map', var='cnt_deg', h=110, fmt=lambda k, v: f'度数 {k} 的点有 {v} 个'),
        dict(type='array', var='cnts', h=190, label='cnts[i]：cnt 恰好等于 i 的点对数（最后变成后缀和）',
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='queries', h=140, label='queries（答案直接写回）'),
    ],
    watch=[('deg1', 'deg1', 'blue'), ('deg2', 'deg2', 'pink'), ('c1', 'c1', 'blue'), ('c2', 'c2', 'pink'), ('s', 's', 'yellow'), ('q', 'q', 'green')],
    captions={
        'deg = [0]': '`deg[i]` 是与点 `i` 相连的边数；节点从 1 开始，所以长 `n + 1`',
        'cnt_e = dict': '`cnt_e` 记每条边出现几次：`1-2` 和 `2-1` 算同一条，所以先把小号放前面',
        'deg[x] += 1': '边 `{x}-{y}` 两端的度数各加一：`deg[{x}] = {deg[x]}`，`deg[{y}] = {deg[y] + 1}`；这条边累计出现 `{cnt_e.get((x, y), 0) + 1}` 次',
        'cnt_deg = Counter': '只关心度数的取值：==度数之和是 `2m`，所以不同的度数至多 `O(根号 m)` 种==，可以两两暴力枚举',
        'cnts = [0]': '`cnts[i]` = `cnt` 恰为 `i` 的点对数；最大和是 `2 * max(deg)`，再多留 1 格防越界。下面二重循环枚举度数 `deg1`、`deg2`（各有 `c1`、`c2` 个点）',
        'if deg1 < deg2': lambda S, B, r: (f'`{S.deg1} < {S.deg2}`：一个取 `{S.deg1}`、一个取 `{S.deg2}`，乘法原理 `{S.c1} × {S.c2}` 对' if S.deg1 < S.deg2
                                           else f'`{S.deg1} = {S.deg2}`：同度数的点两两配对，要用组合数' if S.deg1 == S.deg2
                                           else f'`{S.deg1} > {S.deg2}`：和 `({S.deg2}, {S.deg1})` 重复，规定 `deg1 <= deg2`，不算'),
        'cnts[deg1 + deg2] += c1 * c2': '`cnts[{deg1 + deg2}] += {c1} × {c2}` → {cnts[deg1 + deg2]}',
        'c1 * (c1 - 1)': '`cnts[{deg1 + deg2}] += C({c1}, 2)` → {cnts[deg1 + deg2]}',
        's = deg': '修正重复统计：点对 `({x}, {y})` 被当成 `cnt = deg[{x}] + deg[{y}] = {s}`，但它们之间的 `{c}` 条边算了两遍：真实 `cnt = {s} - {c} = {s - c}`',
        'cnts[s] -= 1': '把 `cnts[{s}]` 里的这一对拿掉 → {cnts[s]}',
        'cnts[s - c] += 1': '从 `cnts[{s}]` 拿掉这一对，放到正确的位置 `cnts[{s - c}]` → {cnts[s - c]}',
        'for i in range(len(cnts)': '从后往前累加：`cnts[i]` 变成「`cnt >= i` 的点对数」',
        'cnts[i - 1] += cnts[i]': '`cnts[{i - 1}] += cnts[{i}]` → {cnts[i - 1]}',
        'queries[i] = cnts': '询问 `q = {q}`：严格大于 `q` 等价于 `>= q + 1` → `cnts[min({q} + 1, {len(cnts) - 1})] = {queries[i]}`，写回 `queries[{i}]`',
        'return queries': '返回 `{queries}`',
    },
    cards=dict(
        one_liner='度数只有 O(根号 m) 种：按度数分组两两枚举，再修正重边',
        complexity='时间 `O(n + m + q)`，空间 `O(n + m)`',
        problem=['无向图（可能有重边），点对 `(a, b)` 的 `cnt` = 与 `a` 或 `b` 相连的边数',
                 '对每个 `queries[j]`，求 `cnt > queries[j]` 的点对数（`a < b`）',
                 '示例：`n=4, edges=[[1,2],[2,4],[1,3],[2,3],[2,1]], queries=[2,3]` → `[6,5]`'],
        quote='deg 的元素和等于 2m。想一想，如果你有 2m 个相同的积木，你最多能搭多少个高度不同的积木塔？ ……deg 中至多有 O(√m) 个不同的数字！这样就可以直接暴力枚举了。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`cnt(x,y) = deg[x] + deg[y] - (x-y 的边数)`，先不管重边，数「度数之和恰好为 i」的方案',
              '按度数分组：同度数的点个数相乘，不同度数至多 `O(根号 m)` 种，二重循环也只是 `O(m)`',
              '重边修正：对每条边，把 `cnts[s]` 减一、`cnts[s - c]` 加一，最后做后缀和回答询问'],
        summary=['复杂度 `O(n + m + q)`，比方法一每个询问双指针 `O(q(n+m))` 更快',
                 '方法一：排序 `deg` 后相向双指针数点对，再逐条边修正重复统计',
                 '易错：`deg1 == deg2` 要用 `c1 * (c1 - 1) // 2`；`cnts` 末尾多留一格',
                 '直接把 `queries` 当答案数组用，省空间；节点编号从 1 开始'],
    ),
)
