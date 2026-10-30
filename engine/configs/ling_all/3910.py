import math


def _b(x, n):
    return format(x, f'0{n}b')[::-1]   # 低位在左：第 i 位 = 节点 i


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums, edges = S['nums'], S['edges']
    n = len(nums)
    sub, vis, q = S.get('sub'), S.get('vis'), S.get('q', 0)
    live = sub is not None and S.get('_line', 0) >= 23   # vis = u ^ sub 之后才画访问状态
    show_sub = sub is not None and S.get('_line', 0) >= 14
    bit = lambda m, i: m is not None and (m >> i & 1)
    cv.text((x0 + 18, y0 + 4), '图（蓝框 = 在当前子集 sub 中，黄 = 在队列 q 中，绿 = 已访问）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 10
    R = min(x1 - x0, y1 - y0) * 0.30
    pos = [(cx + R * math.cos(2 * math.pi * i / n - math.pi / 2), cy + R * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
    for a, b in edges:
        both = show_sub and bit(sub, a) and bit(sub, b)
        cv.line([pos[a], pos[b]], T['text'] if both else T['dim'], 5 if both else 3)
    r = 38
    for i, (px, py) in enumerate(pos):
        ins = show_sub and bit(sub, i)
        inq = live and ins and bit(q, i)
        seen = live and ins and bit(vis, i)
        fill = T['yellow'] if inq else T['green'] if seen else T['panel2']
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=fill, outline=T['blue'] if ins else T['border'], width=7 if ins else 2)
        light = fill != T['panel2']
        cv.text((px, py), nums[i], 36, T['bg'] if light else (T['text'] if ins or not show_sub else T['muted']), anchor='mm', bold=True)
        cv.text((px, py + r + 24), f'节点 {i}', 20, T['muted'], anchor='mm')


def _txt(S):
    if 'sub' not in S or 'u' not in S:
        return '集合用二进制表示：第 i 位 = 1 表示节点 i 在集合里（低位在左）'
    n = len(S['nums'])
    s = f"`sub = {_b(S['sub'], n)}`"
    if S.get('_line', 0) >= 23 and 'vis' in S:
        s += f"　`vis = {_b(S['vis'], n)}`　`q = {_b(S['q'], n)}`"
    return s


CONFIG = dict(
    num=3910, title='统计节点和为偶数的连通子图', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='枚举子集 + 位运算 BFS 判连通',
    tags=['灵神题单·链表树与回溯', '难度分 1859'],
    code='''
class Solution:
    def evenSumSubgraphs(self, nums: list[int], edges: list[list[int]]) -> int:
        n = len(nums)
        g = [0] * n
        for x, y in edges:
            g[x] |= 1 << y
            g[y] |= 1 << x

        ones = 0
        for i, x in enumerate(nums):
            ones |= x << i

        # 枚举节点集合 U = {0,1,2,...,n-1} 的非空子集 sub
        u = (1 << n) - 1
        ans = 0
        for sub in range(1, u + 1):
            # 计算子图的点权和
            s = (sub & ones).bit_count()
            if s % 2:
                continue

            # 判断子图是否连通
            vis = u ^ sub  # 技巧：把不在子图中的节点都标记为已访问
            q = sub & -sub  # 随便选一个在子图中的节点，开始 BFS
            vis |= q
            while q > 0:
                x = q & -q  # 出队
                q ^= x
                to = g[x.bit_length() - 1] & ~vis  # 访问 x 的（尚未访问过的）邻居
                q |= to  # x 的邻居入队
                vis |= to
            if vis == u:  # 所有节点都已访问，子图是连通的
                ans += 1

        return ans
''',
    call='Solution().evenSumSubgraphs([1, 0, 1], [[0, 1], [1, 2]])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='g', label='g（每个节点的邻居集合，十进制位掩码）', h=170, cell=90),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=['sub', 's', ('vis', 'vis', 'green'), ('q', 'q', 'yellow'), ('ans', 'ans', 'green')],
    skip=['g[x] |= 1 << y', 'g[y] |= 1 << x', 'ones |= x << i', 'for x, y in edges', 'for i, x in enumerate', 'continue'],
    max_steps=110,
    captions={
        'g = [0] * n': '`g[i]` 用二进制数保存节点 i 的所有邻居',
        'ones = 0': '`ones` 把 `nums` 压成二进制：第 i 位 = 节点 i 的值',
        'u = (1 << n) - 1': '全集 `u = {u}`（{n} 个 1），子集 `sub` 从 1 枚举到 `u`；`g = {g}`，`ones = {ones}`',
        'for sub in range': lambda S, B, r: (f"枚举非空子集 `sub = {S.sub}`" if S.sub != B.get('sub') else "所有非空子集都枚举完了"),
        's = (sub & ones)': '`sub & ones` 取出子集里值为 1 的节点，个数 `s = {s}`（点权和）',
        'if s % 2': lambda S, B, r: (f"点权和 `{S.s}` 是奇数 → 不合格，跳过" if S.s % 2 else f"点权和 `{S.s}` 是偶数 → 继续判断连通"),
        'vis = u ^ sub': '把不在子集里的节点都标成已访问：`vis = {vis}`，这样 BFS 不会走出去',
        'q = sub & -sub': '`sub & -sub` 取 lowbit，随便选一个子集内的节点当起点：`q = {q}`',
        'vis |= q': '起点标记已访问：`vis = {vis}`',
        'while q > 0': lambda S, B, r: (f"`q = {S.q}` 非空，队列里还有节点" if S.q > 0 else "`q = 0`，队列空了，BFS 结束"),
        'x = q & -q': '队列里取最低位的节点出队：`x = {x}`（节点 {x.bit_length() - 1}）',
        'q ^= x': '把 `x` 从 `q` 里去掉：`q = {q}`',
        'to = g[': '节点 {x.bit_length() - 1} 的邻居里尚未访问的：`to = {to}`',
        'q |= to': '新邻居入队：`q = {q}`',
        'vis |= to': '新邻居标记已访问：`vis = {vis}`',
        'if vis == u': lambda S, B, r: (f"`vis = {S.vis}` 等于 `u = {S.u}`：全访问了 → ==子图连通=="
                                        if S.vis == S.u else f"`vis = {S.vis}` ≠ `u = {S.u}`：有子集内的点够不着 → ==不连通=="),
        'ans += 1': '点权和为偶数且连通，`ans` → {ans}',
        'return ans': '一共 `{ans}` 个满足条件的子集',
    },
    cards=dict(
        one_liner='枚举所有子集，偶数和用位运算算，连通用位运算 BFS 判',
        complexity='时间 `O(m + n·2^n)`，空间 `O(n)`',
        problem=['无向图 `n` 个节点，节点值是 0 或 1',
                 '数一数有多少个节点子集：诱导子图==连通==，且节点值之和是==偶数==',
                 '示例：`nums=[1,0,1]`，`edges=[[0,1],[1,2]]` → `2`（`{1}` 和 `{0,1,2}`）'],
        quote='把 DFS 换成 BFS，用一个二进制数 q 代替队列，表示在队列中的节点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 13`，`2^n - 1` 个非空子集直接枚举',
              '点权和：`(sub & ones).bit_count()`，奇数直接跳过',
              '连通：技巧 `vis = u ^ sub`，把子集外的点预先标成已访问',
              'BFS 结束后 `vis == u`，说明子集里的点都走到了'],
        summary=['时间 `O(m + n·2^n)`，空间 `O(n)`',
                 '`vis = u ^ sub` 是关键技巧：子集外的点当作已访问，BFS 不会越界',
                 '`x.bit_length() - 1` 把 lowbit 转回节点编号',
                 '优化前版本：`nums` 异或和 + 递归 DFS，每次 `O(n+m)`；本版用位运算 BFS 更快',
                 '这不是严格的 BFS，只是遍历图的一种方法'],
    ),
)
