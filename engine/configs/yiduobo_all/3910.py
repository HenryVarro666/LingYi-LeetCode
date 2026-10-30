import math


def _nodes(S):
    return set(S.get('nodes_set', ())) if 'nodes_set' in S else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums, edges = S['nums'], S['edges']
    n = len(nums)
    ns = _nodes(S)
    vis = set(S['vis']) if 'vis' in S and ns is not None else set()
    qset = set(S['q'][S['head']:S['tail']]) if 'q' in S and 'head' in S and 'tail' in S and ns is not None else set()
    cv.text((x0 + 18, y0 + 4), '图（蓝框 = 当前枚举的点集，黄 = 本层队列，绿 = 已入队过）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 10
    R = min(x1 - x0, y1 - y0) * 0.30
    pos = [(cx + R * math.cos(2 * math.pi * i / n - math.pi / 2), cy + R * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
    for a, b in edges:
        both = ns is not None and a in ns and b in ns
        cv.line([pos[a], pos[b]], T['text'] if both else T['dim'], 5 if both else 3)
    r = 38
    for i, (px, py) in enumerate(pos):
        ins = ns is not None and i in ns
        fill = T['yellow'] if ins and i in qset else T['green'] if ins and i in vis else T['panel2']
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=fill, outline=T['blue'] if ins else T['border'], width=7 if ins else 2)
        light = fill != T['panel2']
        cv.text((px, py), nums[i], 36, T['bg'] if light else (T['text'] if ins or ns is None else T['muted']), anchor='mm', bold=True)
        cv.text((px, py + r + 24), f'节点 {i}', 20, T['muted'], anchor='mm')


def _txt(S):
    if 'state' not in S:
        return '用整数 `state` 表示点集：第 i 位 = 1 表示节点 i 在集合里'
    n = len(S['nums'])
    s = f"`state = {format(S['state'], f'0{n}b')[::-1]}`（低位在左）"
    if 'nodes' in S:
        s += f" → 点集 `{S['nodes']}`"
    return s


CONFIG = dict(
    num=3910, title='统计节点和为偶数的连通子图', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='暴力枚举点集 + BFS 判连通',
    tags=['灵神题单·链表树与回溯', '难度分 1859'],
    code='''
class Solution(object):
    def evenSumSubgraphs(self, nums, edges):
        
        n = len(nums)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        res = 0
        for state in range(1, (1 << n)):
            nodes = []
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    nodes.append(index)
            
            nodes_set = set(nodes)
            q = [nodes[0]]
            vis = set([nodes[0]])
            head, tail = 0, 1
            s = 0
            while head < tail:
                for now in q[head : tail]:
                    s += nums[now]
                    for nxt in g[now]:
                        if nxt in nodes_set and nxt not in vis:
                            q.append(nxt)
                            vis.add(nxt)
                
                head, tail = tail, len(q)
            
            if len(q) == len(nodes) and s % 2 == 0:
                res += 1
        
        return res
''',
    call='Solution().evenSumSubgraphs([1, 0, 1], [[0, 1], [1, 2]])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='q', label='q（BFS 队列，按层处理 q[head:tail]）', h=170, cell=80),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=['state', 'nodes', ('s', 's', 'yellow'), 'head', 'tail', ('res', 'res', 'green')],
    skip=['g[x].append(y)', 'g[y].append(x)', 'for x, y in edges', 'for index in range(n)', 'nodes = []',
          'nodes.append(index)', 'for now in q[head : tail]', 'head, tail = 0, 1', 'while head < tail', 'vis.add(nxt)', 'vis = set', 's = 0', 'if state & (1 << index)', 'nodes_set = set(nodes)', 'for nxt in g[now]'],
    max_steps=110,
    captions={
        'g = [[]': '`g` 是邻接表，先建好图',
        'res = 0': '`res` 统计满足条件的点集个数',
        'for state in range': lambda S, B, r: (f"枚举点集 `state = {S.state}`，二进制 {format(S.state, '0%db' % len(S.nums))[::-1]}（低位在左）"
                                               if S.state != B.get('state') else "所有 `2^n - 1` 个非空点集都枚举完了"),
        'q = [nodes[0]]': '点集 `{nodes}`：任取一个点 `{nodes[0]}` 作为 BFS 起点放进队列，`vis` 记录入过队的点',
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一层：`head = {head}`，`tail = {tail}`',
        'while head < tail': lambda S, B, r: (f"`head = {S.head} < tail = {S.tail}`，这一层还有点要扩展"
                                              if S.head < S.tail else f"`head = {S.head} ≥ tail = {S.tail}`：没有新点入队，BFS 结束"),
        's += nums[now]': '取出这一层的点 `{now}`，累加它的值：`s += nums[{now}]` → `s = {s}`',
        'if nxt in nodes_set': lambda S, B, r: (
            f"邻居 `{S.nxt}` 在点集里且没访问过 → ==入队==" if (S.nxt in S.nodes_set and S.nxt not in S.vis)
            else (f"邻居 `{S.nxt}` 不在当前点集里 → 不能走" if S.nxt not in S.nodes_set else f"邻居 `{S.nxt}` 已经访问过")),
        'q.append(nxt)': '`{nxt}` 入队并记入 `vis`：`q = {q}`',
        'head, tail = tail': lambda S, B, r: (f'这一层处理完，下一层是 `q[{S.head}:{S.tail}]`' + ('，空了，BFS 结束' if S.head >= S.tail else '')),
        'if len(q) == len(nodes)': lambda S, B, r: (
            f"BFS 入队了 `{len(S.q)}` 个点，点集共 `{len(S.nodes)}` 个：{'==连通==' if len(S.q) == len(S.nodes) else '==不连通=='}；点权和 `s = {S.s}` 是{'偶' if S.s % 2 == 0 else '奇'}数"),
        'res += 1': '连通且点权和为偶数 → `res` = {res}',
        'return res': '一共 `{res}` 个满足条件的点集',
    },
    cards=dict(
        one_liner='n 只有 13，直接枚举所有点集，BFS 判连通',
        complexity='时间 `O(2^n · (n + m))`，空间 `O(n + m)`',
        problem=['无向图 `n` 个点，点值是 0 或 1，`n ≤ 13`',
                 '统计非空点集的个数：诱导子图==连通==，且点值之和为==偶数==',
                 '示例：`nums=[1,0,1]`，`edges=[[0,1],[1,2]]` → `2`'],
        quote='题目中n的规模较小，因此可以直接暴力枚举所有的点集，一共是2^n - 1种可能，这里减1是因为空集是不合法的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`state` 的每一位表示一个点是否在集合里，从 1 枚举到 `2^n - 1`',
              '从集合里任取一点 BFS，扩展时只走==同在集合内==的邻居',
              'BFS 入队的点数 == 集合大小 → 连通；同时累加点值判断奇偶'],
        summary=['时间 `O(2^n · (n + m))`，空间 `O(n + m)`',
                 '`nxt in nodes_set` 这个条件保证只在诱导子图里走',
                 '用 `len(q) == len(nodes)` 判连通；`s` 只累加到已入队的点，连通时就是全集的点权和',
                 '对比灵神：灵神把集合、队列、visited 都压成整数做位运算，这里用 `set` 和列表，更直观'],
    ),
)
