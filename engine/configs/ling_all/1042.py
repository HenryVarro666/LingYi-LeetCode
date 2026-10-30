FLOWER = ['blue', 'pink', 'green', 'orange']


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    n = S['n']
    color = S.get('color')
    g = S.get('g')
    i = S.get('i')
    cur = (i + 1) if i is not None and color is not None else None
    nbrs = set()
    if cur is not None and g is not None:
        nbrs = {j + 1 for j in g[i]}
    cv.text((x0 + 18, y0 + 4), '花园（黄框 = 当前要种花的，粉框 = 它的邻居；灰 = 还没种）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 14
    R = min((x1 - x0) / 2 - 90, (y1 - y0) / 2 - 62)
    pos = {}
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        pos[k + 1] = (cx + R * math.cos(a), cy + R * math.sin(a))
    for a, b in S['paths']:
        hot = cur is not None and ((a == cur and b in nbrs) or (b == cur and a in nbrs))
        cv.line([pos[a], pos[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    for v in range(1, n + 1):
        X, Y = pos[v]
        c = color[v - 1] if color is not None else 0
        fill = T[FLOWER[c - 1]] if 1 <= c <= 4 else T['panel2']
        if v == cur:
            cv.rect((X - 38, Y - 38, X + 38, Y + 38), outline=T['yellow'], width=5, r=38)
        elif v in nbrs:
            cv.rect((X - 36, Y - 36, X + 36, Y + 36), outline=T['pink'], width=4, r=36)
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=fill, outline=T['border'], width=2, r=30)
        cv.text((X, Y), v, 30, T['bg'] if 1 <= c <= 4 else T['muted'], anchor='mm', bold=True)
    for k in range(4):
        X, Y = x1 - 150, y0 + 40 + k * 34
        cv.rect((X, Y, X + 24, Y + 24), fill=T[FLOWER[k]], r=6)
        cv.text((X + 34, Y + 12), f'花 {k + 1}', 22, T['text'], anchor='lm')


def _mask_txt(S):
    if 'mask' not in S:
        return ''
    m = S['mask']
    if m < 0:
        return f"取反后，`mask` 最低位的 1 在 ==第 {(m & -m).bit_length() - 1} 位== → 就是能种的花"
    used = [k for k in range(1, 5) if (m >> k) & 1]
    return f"`mask = {m:05b}`（低位在右）：邻居已用的花 = =={used if used else '无'}=="


def _cap_j(S, B, ret):
    if getattr(B, 'j', None) == S.j and S.j == S.g[S.i][-1] and S.mask != 1 or (S.mask == 1 and getattr(B, 'j', None) == S.j == S.g[S.i][-1] and len(S.g[S.i]) > 1):
        return '邻居都看完了，`mask` 里是邻居用过的花'
    return f'看邻居 `j = {S.j}`（花园 {S.j + 1}），它的花是 `color[{S.j}] = {S.color[S.j]}`'


def _cap_color(S, B, ret):
    i = S.i
    return f'`mask` 取反后最低的 1 在第 =={S.color[i]}== 位 → 花园 {i + 1} 种花 {S.color[i]}，和所有邻居都不同'


CONFIG = dict(
    num=1042, title='不邻接植花', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='度数至多 3 · 位运算选色',
    tags=['灵神题单', '难度分 1712'],
    code='''
class Solution:
    def gardenNoAdj(self, n: int, paths: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for u, v in paths:
            g[u - 1].append(v - 1)
            g[v - 1].append(u - 1)  # 建图

        color = [0] * n
        for i, nodes in enumerate(g):
            mask = 1  # 由于颜色是 1~4，把 0 加入 mask 保证下面不会算出 0
            for j in g[i]:
                mask |= 1 << color[j]
            mask = ~mask
            # Python 没有统计尾零的库函数，可以枚举，或者求 lowbit 的二进制长度减一
            color[i] = (mask & -mask).bit_length() - 1
        return color
''',
    call='Solution().gardenNoAdj(5, [[1,2],[2,3],[3,1],[3,4],[4,5]])',
    expect=[1, 2, 3, 1, 2],
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='array', var='color', pointers={'i': 'yellow'}, label='color（0 = 还没种）', h=190,
             color=lambda S, i, v: (FLOWER[v - 1] if 1 <= v <= 4 else None)),
        dict(type='text', fn=_mask_txt, h=70),
    ],
    watch=[('i', 'i', 'yellow'), ('mask', "mask", 'cyan'), ('j', 'j', 'pink')],
    captions={
        'g = [[]': '`g[x]` 存花园 x 的邻居（编号减 1，从 0 开始）',
        'g[v - 1].append': '双向路径：`{u}` 和 `{v}` 互为邻居，`g[{u-1}]` 加入 {v-1}，`g[{v-1}]` 加入 {u-1}',
        'color = [0] * n': '`color[i]` = 第 i 个花园的花；==0 表示还没种==',
        'for i, nodes in enumerate(g)': lambda S, B, r: ('所有花园都种好了，循环结束' if getattr(B, 'i', None) == S.i and S.color[S.i] else f'轮到花园 `{S.i + 1}`：邻居有 `{len(S.nodes)}` 个（题目保证 ≤ 3），4 种花一定够用'),
        'mask = 1': '`mask` 记录邻居已用的花，先放进 0，保证后面不会选出 0 号',
        'for j in g[i]': _cap_j,
        'XXX': '看邻居 `j = {j}`（花园 {j+1}），它的花是 `color[{j}] = {color[j]}`',
        'mask |= 1 << color[j]': '把邻居的花 `{color[j]}` 标进 `mask`：`mask = {mask:b}`',
        'mask = ~mask': '取反：==原来是 0（没人用）的位变成 1== → 最低的 1 就是可种的花',
        'color[i] =': _cap_color,
        'return color': '度数 ≤ 3 ⇒ 邻居最多占 3 种花，总有一种剩下 → 一遍扫描就够，答案 `{ret}`',
    },
    skip=['for u, v in paths', 'g[u - 1].append'],
    max_steps=110,
    cards=dict(
        one_liner='度数至多 3，4 种花总剩一种：挑个和邻居都不同的就行',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 个花园，`paths` 是双向路径，每个花园至多 3 条路',
                 '每个花园种 1~4 号花之一，==相连的花园花不能相同==，返回任一方案',
                 '示例：`n=3, paths=[[1,2],[2,3],[3,1]]` → `[1,2,3]`'],
        quote='问题相当于用 4 种颜色给图中的每个节点染色，要求相邻节点颜色不同。而「所有花园最多有 3 条路径可以进入或离开」，这相当于图中每个点的度数至多为 3，那么只要选一个和邻居不同的颜色即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['这是图染色：度数 ≤ 3，邻居最多挡住 3 种颜色，第 4 种永远能用',
              '所以不用回溯，按编号顺序给每个点挑一个邻居没用过的颜色',
              '位运算：用 `mask` 的第 k 位表示颜色 k 被用；取反后求最低位的 1 即可'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`（`m = len(paths)`）',
                 '易错：花园编号从 1 开始，建图时要 `-1`；颜色 1~4，所以 `mask` 初值 1 把 0 号占掉',
                 '没种花的邻居 `color = 0`，对应第 0 位，已被占住，不会误判',
                 '另一种写法：用集合 `set(range(1,5)) - {color[j] for j in nodes}`，`pop()` 取一个，思路相同',
                 '同类：图的 k 色贪心染色（度数 ≤ k-1）'],
    ),
)
