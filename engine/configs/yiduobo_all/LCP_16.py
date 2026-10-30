_EDGES = [(0, 1), (1, 2), (0, 2), (1, 3), (2, 3)]
_POS = {0: (0.12, 0.5), 1: (0.45, 0.12), 2: (0.45, 0.88), 3: (0.78, 0.5)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '游乐园图（圆圈里 = 编号，旁边 = 点权）', 24, T['muted'], bold=True)
    val = [3, 1, 4, 2]
    W, H = x1 - x0 - 200, y1 - y0 - 100
    P = {k: (x0 + 100 + W * a, y0 + 70 + H * b) for k, (a, b) in _POS.items()}
    tri = None
    if S['_line'] >= 85 and all(z in S for z in 'ijk'):
        tri = (S['i'], S['j'], S['k'])
    cur = set(tri) if tri else set()
    for a, b in _EDGES:
        on = a in cur and b in cur
        cv.line([P[a], P[b]], T['blue'] if on else T['border'], 6 if on else 3)
    for k, (x, y) in P.items():
        col = T['blue'] if k in cur else T['dim']
        cv.rect((x - 28, y - 28, x + 28, y + 28), fill=col, r=28)
        cv.text((x, y), k, 28, T['bg'], anchor='mm', bold=True)
        cv.text((x + 36, y - 30), f'w={val[k]}', 22, T['yellow'], anchor='lm', bold=True)
    if tri:
        v = sum(val[t] for t in tri)
        cv.text((x0 + 18, y1 - 6), f'当前三角形 {tuple(sorted(tri))}：点权和 = {v}', 24, T['text'], anchor='lb', bold=True)


CONFIG = dict(
    num='LCP 16', title='游乐园的游览计划', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='度数分块找三角形 + 哈希分类讨论',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def maxWeight(self, edges, value):

        linked = {}
        for x, y in edges:
            if x not in linked:
                linked[x] = set()
            if y not in linked:
                linked[y] = set()
            linked[x].add(y)
            linked[y].add(x)
        
        n = len(linked)
        m = len(edges)
        #阈值划线
        threshold = int(sqrt(2 * m))
        triangle_set = set()

        over_set = set()
        #低度数的点构成的三角形
        for i in linked:
            if len(linked[i]) < threshold:
                for j in linked[i]:
                    for k in linked[i]:
                        if j == k or k not in linked[j]:
                            continue
                        triangle_set.add(tuple(sorted([i, j, k])))
            else:
                over_set.add(i)
        
        #高度数的点构成的三角形
        for i in over_set:
            for j in over_set:
                if i == j or j not in linked[i]:
                    continue
                for k in over_set:
                    if i == k or j == k or k not in linked[i] or k not in linked[j]:
                        continue
                    triangle_set.add(tuple(sorted([i, j, k])))
        
        def add(key, other, v, first, second, third):
            if key not in first:
                first[key] = [0, None]
            if key not in second:
                second[key] = [0, None]
            if key not in third:
                third[key] = [0, None]
            
            if v > first[key][0]:
                third[key] = second[key][:]
                second[key] = first[key][:]
                first[key][0] = v
                first[key][1] = other

            elif v > second[key][0]:
                third[key] = second[key][:]
                second[key][0] = v
                second[key][1] = other
            
            elif v > third[key][0]:
                third[key][0] = v
                third[key][1] = other

        def get(key, other, first, second, third):
            first_flag = second_flag = True
            for node in other:
                if node == first[key][1]:
                    first_flag = False
                if node == second[key][1]:
                    second_flag = False
                    third_flag = False

            if first_flag:
                return first[key]
            elif second_flag:
                return second[key]
            else:
                return third[key]

        first = {}
        second = {}
        third = {}
        max_node = {}
        res = 0
        for i, j, k in triangle_set:
            v = value[i] + value[j] + value[k]
            #情况1,
            res = max(res, v)

            #更新边为key的哈希表
            add((i, j), k, v, first, second, third)
            add((i, k), j, v, first, second, third)
            add((j, k), i, v, first, second, third)
            
            #更新点为key的哈希表
            if i not in max_node or max_node[i][0] < v:
                max_node[i] = [v, set([j, k])]
            if j not in max_node or max_node[j][0] < v:
                max_node[j] = [v, set([i, k])]
            if k not in max_node or max_node[k][0] < v:
                max_node[k] = [v, set([i, j])]

        for i, j, k in triangle_set:
            #情况2
            res = max(res, get((i, j), [k], first, second, third)[0] + value[k])
            res = max(res, get((i, k), [j], first, second, third)[0] + value[j])
            res = max(res, get((j, k), [i], first, second, third)[0] + value[i])

            #情况3-1
            if j not in max_node[i][1] and k not in max_node[i][1]:
                res = max(res, max_node[i][0] + value[j] + value[k])
            if i not in max_node[j][1] and k not in max_node[j][1]:
                res = max(res, max_node[j][0] + value[i] + value[k])
            if i not in max_node[k][1] and j not in max_node[k][1]:
                res = max(res, max_node[k][0] + value[i] + value[j])

            #情况3-2
            v1, other1 = get((i, j), [k], first, second, third)
            v2, other2 = get((i, k), [j, other1], first, second, third)
            res = max(res, v1 + v2 - value[i])
            v2, other2 = get((j, k), [i, other1], first, second, third)
            res = max(res, v1 + v2 - value[j])

            v1, other1 = get((i, k), [j], first, second, third)
            v2, other2 = get((i, j), [k, other1], first, second, third)
            res = max(res, v1 + v2 - value[i])
            v2, other2 = get((j, k), [i, other1], first, second, third)
            res = max(res, v1 + v2 - value[k])

            v1, other1 = get((j, k), [i], first, second, third)
            v2, other2 = get((i, j), [k, other1], first, second, third)
            res = max(res, v1 + v2 - value[j])
            v2, other2 = get((i, k), [j, other1], first, second, third)
            res = max(res, v1 + v2 - value[k])
        
        return res
''',
    call='Solution().maxWeight([[0,1],[1,2],[0,2],[1,3],[2,3]], [3,1,4,2])',
    expect=10,
    skip=[5, 6, 7, 8, 9, 10, 13, 17, 19, 23, 24, 25, 26, 28, 29, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80, 81, 82, 83, 98, 99, 100, 101, 118, 119, 121, 124, 125, 127, 130, 131, 133, 92, 93, 86, 126, 128, 132, 134, 112, 114, 122],
    max_steps=75,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='first', fmt=lambda k, v: f'边{k}: 最大={v[0]}（第三点 {v[1]}）', label='first：包含每条边的点权和最大的三角形', h=210, font=22),
        dict(type='map', var='max_node', fmt=lambda k, v: f'点{k}: {v[0]}（另两点 {sorted(v[1])}）', label='max_node：包含每个点的最大三角形', h=140, font=22),
    ],
    watch=['threshold', 'i', 'j', 'k', ('res', 'res', 'green')],
    captions={
        4: '`linked`：邻接表，记录每个游乐园连着哪些游乐园',
        11: '无向边：`{y}` 的邻居加入 `{x}`，现在 `linked[{y}] = {linked[y]}`',
        14: '`m = {m}` 条边（边数和点数同一量级）',
        16: '阈值 `int(sqrt(2m)) = {threshold}`：度数和是 `2m`，度数 `>= {threshold}` 的点至多 `sqrt(2m)` 个',
        21: '看点 `{i}`',
        22: lambda S, B, r: f'点 `{S.i}` 度数 `{len(S.linked[S.i])}`，阈值 `{S.threshold}` → ' + ('度数小：枚举它的邻居对 `(j, k)`，若 `j、k` 也相连就是三角形' if len(S.linked[S.i]) < S.threshold else '度数大：放进 `over_set`，稍后暴力枚举'),
        27: '`{i}` 的两个邻居 `{j}`、`{k}` 也相连 → 三角形 `{tuple(sorted([i, j, k]))}`，排序后放进集合去重：`{triangle_set}`',
        32: '度数大的点 `over_set = {over_set}`，点数太少（不足 3 个）→ 暴力三重枚举也没有新三角形',
        84: '`res` 记录答案；下面对每个三角形分情况讨论',
        85: lambda S, B, r: (f'取三角形 `({S.i}, {S.j}, {S.k})`' if not (B.get('i') == S.i and B.get('j') == S.j and B.get('k') == S.k) else '三角形都处理完了，第一遍结束'),
        86: '三角形点权和 `v = {v}`',
        88: '情况 1：两个三角形完全重叠，等价于选一个最大的三角形 → `res = {res}`',
        91: '更新 `first / second / third`（三条边各一次）：以边为 key，保存包含这条边的点权和最大的三个三角形（情况 2、3-2 要用）',
        92: '同样更新边 `({i},{k})`',
        93: '同样更新边 `({j},{k})`',
        96: '`max_node` 以点为 key，保存包含这个点的最大三角形（情况 3-1 要用）：点 `{i}`',
        97: '点 `{i}` 的最大三角形点权和 `{v}`，另两点 `{j}、{k}`',
        103: lambda S, B, r: (f'第二遍：对每个三角形，分情况讨论另一个三角形怎么选：`({S.i}, {S.j}, {S.k})`' if not (B.get('i') == S.i and B.get('j') == S.j and B.get('k') == S.k) else '所有三角形都枚举完'),
        105: '情况 2：两个三角形共用边 `({i},{j})`。取包含这条边、第三点不同的另一个最大三角形，再加 `value[{k}]`',
        106: '情况 2：共用边 `({i},{k})`，再加 `value[{j}]`',
        107: '情况 2：共用边 `({j},{k})`，再加 `value[{i}]`',
        110: '情况 2 做完，`res = {res}`。情况 3-1：只共用一个点（`{i}`、`{j}`、`{k}` 各试一次）：该点的最大三角形若不含另外两点，两个三角形就只重叠在这个点',
        111: '`max_node[{i}]` 的点权和加上 `value[{j}] + value[{k}]` → `res = {res}`',
        113: '`res` → {res}',
        115: '`res` → {res}',
        120: '情况 3-2：两个三角形各含一条边、共用一个点，共用点权只算一次：`{v1} + {v2} - value[{i}]` → `res = {res}`；共 6 种搭配，视频只演示前两种',
        122: '情况 3-2：共用点 `{j}`：`{v1} + {v2} - value[{j}]` → `res = {res}`',
        126: '情况 3-2：换一对边，共用点 `{i}`：`{v1} + {v2} - value[{i}]` → `res = {res}`',
        128: '情况 3-2：共用点 `{k}`：`{v1} + {v2} - value[{k}]` → `res = {res}`',
        132: '情况 3-2：共用点 `{j}`：`{v1} + {v2} - value[{j}]` → `res = {res}`',
        134: '情况 3-2：共用点 `{k}`：`{v1} + {v2} - value[{k}]` → `res = {res}`',
        136: '所有情况取最大 → ==答案 {res}==（两个三角形共用边 `(1,2)`，四个点全选）',
    },
    cards=dict(
        one_liner='先按度数分块高效找出所有三角形，再按重叠方式分情况取最大',
        complexity='时间 `O(M * sqrt(M))`，空间 `O(M)`',
        problem=['n 个游乐园，每个有点权 `value[i]`，`edges` 是双向道路',
                 '游览路线是由三个游乐园两两相连组成的环（==三角形==）',
                 '选两条路线（可以相同、可以有重叠），总价值 = ==去重后的点权和==，求最大值',
                 '本视频：4 个点，权重 `[3,1,4,2]`，5 条边 → `10`'],
        quote='不妨以sqrt(2M)为阈值划线，将度数小于阈值的节点归为一类，将度数大于等于阈值的节点归位另一类。',
        quote_src='—— yiduobo 题解原文',
        idea=['边数 `M` 与点数同量级：度数小的点枚举邻居对，度数大的点至多 `sqrt(2M)` 个，暴力三重循环',
              '情况 1：两个三角形完全重叠 → 取最大的一个',
              '情况 2：共用一条边 → 哈希表以边为 key，记最大的三个三角形，选第三点不同的',
              '情况 3：只共用一个点 → 3-1 点的最大三角形 + 另一个；3-2 用边哈希表的次大三角形，`v1 + v2 - 共用点`'],
        summary=['找三角形 `O(M * sqrt(M))`；三角形个数也是这个量级，可以逐个遍历',
                 '只共用一点时，最优解里必含该点最大三角形的另外两点（交换论证）',
                 '边表存==前三==大是为了避开两边第三点相同的情况',
                 '原文为 Python 2 风格，本题代码在 Python 3 可直接运行，只在 setup 补了 `from math import sqrt`',
                 '视频里的小例子省略了函数 `add / get` 的内部步骤（只演示调用）'],
    ),
)
