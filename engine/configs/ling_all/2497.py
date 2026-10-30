VALS = [1, 2, 3, 4, 10, -10, -20]
EDGES = [[0, 1], [1, 2], [1, 3], [3, 4], [3, 5], [3, 6]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    vals = S['vals']
    g = S.get('g')
    k = S['k']
    cv.text((x0 + 18, y0 + 4), '每个节点 = 一个中心；g[i] = 它「值为正」的邻居值', 22, T['muted'], bold=True)
    done = 'g' in S and S['_line'] >= 7
    y = y0 + 50
    rowh = min(62, (y1 - y - 10) / len(vals))
    for i, v in enumerate(vals):
        cv.text((x0 + 24, y + rowh / 2), f'节点 {i}', 24, T['muted'], anchor='lm')
        cv.rect((x0 + 130, y + 6, x0 + 200, y + rowh - 6), fill=T['blue'], r=8)
        cv.text((x0 + 165, y + rowh / 2), v, 26, T['bg'], anchor='mm', bold=True)
        if g is not None:
            a = sorted(g[i], reverse=True)
            cv.text((x0 + 220, y + rowh / 2), '邻居', 20, T['dim'], anchor='lm')
            for j, w in enumerate(a):
                chosen = done and j < k
                X = x0 + 280 + j * 64
                cv.rect((X, y + 8, X + 56, y + rowh - 8), fill=T['green'] if chosen else T['border'], r=8)
                cv.text((X + 28, y + rowh / 2), w, 24, T['bg'] if chosen else T['text'], anchor='mm', bold=True)
            if done:
                tot = v + sum(a[:k])
                cv.text((x1 - 24, y + rowh / 2), f'星和 {tot}', 24, T['yellow'], anchor='rm', bold=True)
        y += rowh


def _star(S):
    return [(v + sum(nlargest(S.k, a)), i) for i, (v, a) in enumerate(zip(S.vals, S.g))]


CONFIG = dict(
    num=2497, title='图中最大星和', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='建图 + 枚举中心 + 取最大的 k 个正邻居',
    tags=[],
    code='''
class Solution:
    def maxStarSum(self, vals: List[int], edges: List[List[int]], k: int) -> int:
        g = [[] for _ in vals]
        for x, y in edges:
            if vals[y] > 0: g[x].append(vals[y])
            if vals[x] > 0: g[y].append(vals[x])
        return max(v + sum(nlargest(k, a)) for v, a in zip(vals, g))
''',
    call=f'Solution().maxStarSum({VALS}, {EDGES}, 2)',
    expect=16,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('k', 'k', 'orange')],
    captions={
        'g = [[] for _ in vals]': '`g[i]` 存节点 `i` 的所有==值为正==的邻居的值（负数邻居只会拉低星和，不选）',
        'for x, y in edges': lambda S, B, ret: (f'处理边 `({S.x}, {S.y})`' if (B.get('x'), B.get('y')) != (S.x, S.y) else '所有边都处理完了，g 建好'),
        'if vals[y] > 0': lambda S, B, ret: (f'`vals[{S.y}] = {S.vals[S.y]}` > 0 → 对 `{S.x}` 有用，放进 `g[{S.x}]`'
                                             if S.vals[S.y] > 0 else f'`vals[{S.y}] = {S.vals[S.y]}` ≤ 0 → 不会让 `{S.x}` 的星和变大，跳过'),
        'if vals[x] > 0': lambda S, B, ret: (f'`vals[{S.x}] = {S.vals[S.x]}` > 0 → 对 `{S.y}` 有用，放进 `g[{S.y}]`'
                                             if S.vals[S.x] > 0 else f'`vals[{S.x}] = {S.vals[S.x]}` ≤ 0 → 不会让 `{S.y}` 的星和变大，跳过'),
        'return max': lambda S, B, ret: (
            '枚举中心，星和 = 中心值 + 最大的 k 个正邻居：' + '，'.join(f'{i}号={t}' for t, i in _star(S))
            + f'。最大的是 =={max(t for t, i in _star(S))}=='),
    },
    max_steps=40,
    cards=dict(
        one_liner='枚举中心，邻居只取值最大的 k 个正数',
        complexity='时间 `O(n + m log n)`，空间 `O(n + m)`',
        problem=['无向图，节点有值；==星图==是一个中心加至多 `k` 个邻居（边都过中心）',
                 '星和 = 星图所有节点值之和，求至多 `k` 条边的最大星和',
                 '示例：`vals=[1,2,3,4,10,-10,-20]`，`k=2` → 中心 3 加邻居 1、4 → `16`'],
        quote='建图，枚举中心节点，选择至多 k 个最大的值为正数的邻居。',
        quote_src='—— 灵茶山艾府题解',
        idea=['建图时就只记录值为正的邻居：负数和 0 不会让星和变大',
              '中心必选；邻居从大到小挑，最多 `k` 个：`nlargest(k, a)`',
              '对每个节点算 `v + sum(nlargest(k, a))`，取最大'],
        summary=['时间 `O(n + m log n)`；用快速选择可降到 `O(n + m)`',
                 '易错：中心本身的值可能为负，但必须算上（不能不选中心）',
                 '`k = 0` 或没有正邻居时，`nlargest` 给出空列表，`sum` 为 0',
                 '建图时==只存正的邻居值==，比存全部再过滤更省空间'],
    ),
)
