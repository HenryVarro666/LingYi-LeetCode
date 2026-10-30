CONFIG = dict(
    num=2077, title='殊途同归', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='按度数分类 · 数三角形',
    tags=['灵神题单·图论算法'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def numberOfPaths(self, n, corridors):

        linked = {}
        for x, y in corridors:
            if x not in linked:
                linked[x] = set()
            if y not in linked:
                linked[y] = set()
            linked[x].add(y)
            linked[y].add(x)
        
        m = len(corridors)
        threshold = int(sqrt(2 * m))
        triangle_set = set()

        over_set = set()

        for i in linked:
            if len(linked[i]) < threshold:
                for j in linked[i]:
                    for k in linked[i]:
                        if j == k or k not in linked[j]:
                            continue
                        triangle_set.add(tuple(sorted([i, j, k])))
            else:
                over_set.add(i)
        
        for i in over_set:
            for j in over_set:
                if i == j or j not in linked[i]:
                    continue
                for k in over_set:
                    if i == k or j == k or k not in linked[i] or k not in linked[j]:
                        continue
                    triangle_set.add(tuple(sorted([i, j, k])))
        
        return len(triangle_set)
''',
    call='Solution().numberOfPaths(5, [[1,2],[1,3],[2,3],[2,4],[3,4],[4,5]])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"`threshold = {S['threshold']}`：度数 `< {S['threshold']}` 的点 → 枚举邻居对；其余点 → 放进 `over_set` 暴力三重枚举" if 'threshold' in S else '`linked`：每个房间的相邻房间集合')),
        dict(type='map', var='linked', fmt=lambda k, v: f'{k}: {sorted(v)}', h=300, label='linked（邻接表）'),
        dict(type='set', var='over_set', label='over_set（度数 >= 阈值）', h=110),
        dict(type='set', var='triangle_set', label='triangle_set（已找到的三角形）', h=170),
    ],
    skip=['for x, y in corridors', 'for i in over_set', 'over_set.add(i)', 'if x not in linked', 'if y not in linked', '= set()', 'continue', 'linked[x].add(y)', 'for j in linked[i]', 'for k in linked[i]', 'for j in over_set', 'for k in over_set', 'over_set = set()', 'triangle_set = set()'],
    watch=['i', 'j', 'k', ('threshold', 'threshold', 'cyan')],
    captions={
        'linked[x].add(y)': '房间 `{x}` 的邻居里加入 `{y}`',
        'linked[y].add(x)': '无向边：房间 `{y}` 的邻居里加入 `{x}`，`linked = {linked}`',
        'threshold = int': '`m = {m}` 条边，阈值 `int(sqrt(2m)) = {threshold}`：度数和 = 2m，度数 >= 阈值的点至多 `sqrt(2m)` 个',
        'if len(linked[i]) < threshold': '房间 `{i}` 的度数是 `{len(linked[i])}`，阈值 `{threshold}` → {"度数小：枚举它的邻居对 (j, k)" if len(linked[i]) < threshold else "度数大：放进 over_set，稍后暴力枚举"}',
        'over_set.add(i)': '`{i}` 度数大，放进 `over_set = {over_set}`',
        'for j in linked[i]': '枚举 `{i}` 的邻居 `j = {j}`',
        'for k in linked[i]': '再枚举 `{i}` 的另一个邻居 `k = {k}`',
        'if j == k or k not in linked[j]': lambda S, B, r: (f'`j = {S.j}`、`k = {S.k}`：' + ('同一个点，跳过' if S.j == S.k else (f'`{S.k}` 在 `{S.j}` 的邻居里 → `i,j,k` 两两相连，是三角形' if S.k in S.linked[S.j] else f'`{S.j}` 和 `{S.k}` 不相邻 → 不成三角形'))),
        'triangle_set.add': '排序后 `{tuple(sorted([i, j, k]))}` 加入集合：==排序去重==，同一个三角形不会被数多次，现有 {len(triangle_set)} 个',
        'for i in over_set': '第二阶段：只在 `over_set` 里暴力枚举三个点，`i = {i}`',
        'for j in over_set': '`j = {j}`',
        'if i == j or j not in linked[i]': '`i = {i}`、`j = {j}`：{"同一点或不相邻，跳过" if (i == j or j not in linked[i]) else "相邻，继续找第三个点"}',
        'for k in over_set': '`k = {k}`',
        'if i == k or j == k or': '`({i},{j},{k})`：{"有重复点或有一对不相邻 → 跳过" if (i == k or j == k or k not in linked[i] or k not in linked[j]) else "三点两两相邻 → 三角形"}',
        'return len(triangle_set)': '三角形共 `{len(triangle_set)}` 个，就是答案 =={len(triangle_set)}==',
    },
    cards=dict(
        one_liner='度数小的点枚举邻居对，度数大的点数量少、直接暴力',
        complexity='时间 `O(M * sqrt(M))`，空间 `O(M)`',
        problem=['n 个房间，`corridors[i] = [a, b]` 表示 a、b 之间有一条走廊',
                 '一个「混乱度为 3」的环：三个房间两两相连，求这样的环（三角形）的个数',
                 '本视频：n = 5，6 条走廊 → `2`'],
        quote='按照每个节点的度与sqrt(2M)的大小将节点分为两类，对于度较小的这类节点可以枚举其相邻节点求解，因为度较小所以保证了枚举的复杂度。',
        quote_src='—— yiduobo 题解原文',
        idea=['总度数是 `2M`，所以度数 `>= sqrt(2M)` 的点最多 `sqrt(2M)` 个',
              '小度点：枚举两个邻居 `j, k`，看它们是否相连，总共约 `M*sqrt(M)` 次',
              '大度点：点数少，三重循环 `sqrt(M)^3` 也是 `M*sqrt(M)`',
              '三角形用排序后的元组放进集合，自动去重'],
        summary=['时间 `O(M * sqrt(M))`，空间 `O(M)`',
                 '三角形用 `tuple(sorted(...))` 去重，否则同一个环会被数多次',
                 '这是 LCP 16 找三角形部分的弱化版',
                 '原文已是 Python 3 可运行写法，只在 setup 补了 `from math import sqrt`'],
    ),
)
