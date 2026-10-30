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
EDGES = [[0, 1, 2], [1, 2, 3], [1, 3, 5], [1, 4, 4], [2, 5, 6]]
NUMS = [2, 1, 2, 1, 3, 1]
PARENTS = [-1, 0, 1, 1, 1, 2]
WT = {2: 3, 1: 2, 3: 5, 4: 4, 5: 6}


def _path(x):
    p = []
    while x != -1:
        p.append(x)
        x = PARENTS[x]
    return p[::-1]


def _win(S):
    x = S['_inner'].get('now')
    if x is None:
        return None, [], set(), 0
    p = _path(x)
    st = S['_inner'].get('start', S['_inner'].get('pre_start', 0))
    return x, p, set(p[st:]), st


def _draw(cv, S, B, box, T):
    x, p, w, st = _win(S)
    gtree_draw(cv, box, T, PARENTS, lambda i: NUMS[i],
               lambda i: 'green' if i in w else ('orange' if i in p else None),
               lambda i: 'blue' if i == x else None, None,
               edge=lambda u: 'green' if (u in w and PARENTS[u] in w) else None, edge_label=lambda u: WT[u],
               title='树（圈内 = nums，边上 = 长度；绿 = 当前路径，橙 = 被挤出，蓝环 = now）')


def _fm(S):
    x, p, w, st = _win(S)
    if x is None:
        return f"最优 `res = {S.get('res')}`（长度, 节点数）"
    s = S['s']
    return f"终点 `{x}`，起点深度 `start = {st}`：长度 `s[-1] - s[{st}] = {s[-1]} - {s[st]} = {s[-1] - s[st]}`；`res = {S.get('res')}`"


CONFIG = dict(
    num=3425, title='最长特殊路径', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='树上 DP：最靠上的起点 + 前缀和',
    tags=['链表树与回溯', '难度分 2435'],
    code='''
class Solution(object):
    def longestSpecialPath(self, edges, nums):
        
        n = len(edges) + 1
        g = {x : {} for x in range(n)}

        for x, y, w in edges:
            g[x][y] = w
            g[y][x] = w

        last = {}
        for v in nums:
            last[v] = -1

        def dfs(now, fa, pre_start, last, s, level, res):
            start = max(last[nums[now]] + 1, pre_start)
            if start < level:
                length = s[-1] - s[start]
                cnt = level - start + 1
                if res[0] < length or (res[0] == length and res[1] > cnt):
                    res[0] = length
                    res[1] = cnt

            pre_last = last[nums[now]]
            last[nums[now]] = level
            for nxt in g[now]:
                if nxt == fa:
                    continue
                s.append(s[-1] + g[now][nxt])
                dfs(nxt, now, start, last, s, level + 1, res)
                s.pop()
            last[nums[now]] = pre_last

        res = [0, 1]
        dfs(0, -1, 0, last, [0], 0, res)
        return res
''',
    call='Solution().longestSpecialPath([[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], [2,1,2,1,3,1])',
    expect=[6, 2],
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', fn=_fm, size=24, h=55),
        dict(type='array', var='s', label='s（根到路径各节点的距离前缀和）', cell=60, h=125),
        dict(type='map', var='last', label='last（值 → 当前路径上最后出现的深度，−1 = 没出现）', h=120),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('start', lambda S: S['_inner'].get('start'), 'green'),
           ('level', lambda S: S['_inner'].get('level')), ('res', lambda S: S['_inner'].get('res'), 'yellow')],
    captions={
        'g = {x': '`g[x][y] = w`：用字典存邻居和边长',
        'last = {}': '`last[v]` = 值 `v` 在当前 dfs 路径上最后一次出现的==深度==，初始 `-1`',
        'start = max': '起点深度 `max(last[{nums[now]}] + 1, pre_start) = max({last[nums[now]] + 1}, {pre_start})` → 起点深度 `start` = =={start}==',
        'if start < level': '`start = {start}`，`level = {level}`：{"路径至少有 2 个节点，算一下长度" if start < level else "起点就是自己，路径只有一个节点（长度 0），不用更新"}',
        'length = s[-1]': '前缀和相减：`s[-1] - s[{start}] = {s[-1]} - {s[start]}` → 长度 =={length}==；节点数 = `level - start + 1`',
        'if res[0] < length': lambda S, B, r: (f"`length = {S.length}`，`cnt = {S.cnt}`，当前最优 `{S.res}`：" + ('长度更长，或一样长但节点更少 → ==更新==' if (S.res[0] < S.length or (S.res[0] == S.length and S.res[1] > S.cnt)) else '没有更好 → 不更新')),
        'last[nums[now]] = level': '先存 `pre_last = {pre_last}` 备份；值 `{nums[now]}` 在当前路径上最后出现在深度 `{level}`',
        'if nxt == fa': '孩子候选 `{nxt}`：{"是父节点，跳过" if nxt == fa else "往下走"}',
        's.append': '前缀和栈追加 `{s[-1]}`（加上边长 `{g[now][nxt]}`）',
        'dfs(nxt': '递归进入 `{nxt}`，把本节点的起点 `start = {start}` 当作 `pre_start` 传下去',
        'last[nums[now]] = pre_last': '离开 `{now}`：`s` 末尾弹出，`last[{nums[now]}]` 还原为 `{pre_last}` → ==回溯==',
        'res = [0, 1]': '答案初值 `[0, 1]`：任何单个节点都是长度 0、1 个节点的特殊路径',
        'dfs(0, -1': '从根节点 `0` 出发，前缀和 `s = [0]`',
        'return res': '返回 `{ret}`：最长 `{ret[0]}`，最少 `{ret[1]}` 个节点',
    },
    skip=['for nxt in g[now]', 'pre_last =', 'cnt = level', 'res[0] = length', 'for x, y, w in edges', 'g[x][y] = w', 'g[y][x] = w', 'for v in nums', 'last[v] = -1', 'n = len(edges)',
          'continue', 'res[1] = cnt', 's.pop()'],
    max_steps=100,
    cards=dict(
        one_liner='dp：以每个点为终点，起点取「最靠上」，用前缀和求长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，根 `0`，边有长度，节点有值',
                 '特殊路径：自上而下、经过节点值互不相同',
                 '求最长长度，及最长时的最少节点数',
                 '示例：`[6, 2]`'],
        quote='对于某个节点p，以p为终点的最长的特殊路径，就必然是以p为终点的所有特殊路径中起点最靠上的那一条。',
        quote_src='—— yiduobo 题解',
        idea=['`start[p] = max(start[fa], last[nums[p]] + 1)`，两个限制取靠下的那个',
              '`start` 和 `last` 都用==深度==表示，正好当前缀和数组 `s` 的下标',
              '`last` 是哈希表，进入节点时改、离开时还原（回溯）'],
        result='返回 `[6, 2]`',
        summary=['时间 `O(n)`，空间 `O(n)`（递归 + 前缀和）',
                 '易错：`last` 初始 `-1`；必须回溯；`start == level` 时路径长度 0，答案初值 `[0,1]` 已覆盖',
                 '对比灵神：他把 `last_depth` 存成「深度 +1」，用元组 `max` 同时比较长度与节点数',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
