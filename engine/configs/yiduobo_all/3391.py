def _layers(S):
    mat = S.get('self.matrix')
    if mat is None:
        return '（尚未创建）'
    parts = []
    for x, layer in enumerate(mat):
        cells = [f'({y},{z})' for y, row in enumerate(layer) for z, v in enumerate(row) if v == 1]
        parts.append(f'matrix[{x}] 有 {len(cells)} 个 1：' + (' '.join(cells) if cells else '无'))
    return '　｜　'.join(parts)


def _hp(t):
    return f'({t[0]},{t[1]})'


CONFIG = dict(
    num=3391, title='设计一个高效的层跟踪三维二进制矩阵', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='计数数组 + 堆 · 懒删除',
    tags=[],
    code='''
class Matrix3D(object):

    def __init__(self, n):
        self.matrix = [[[0] * n for _ in range(n)] for _ in range(n)]
        self.cnt = [0] * n
        self.heap = []
        for x in range(n):
            heapq.heappush(self.heap, (0, -x))

    def setCell(self, x, y, z):
        if self.matrix[x][y][z] == 1:
            return

        self.matrix[x][y][z] = 1
        self.cnt[x] += 1
        heapq.heappush(self.heap, (-self.cnt[x], -x))

    def unsetCell(self, x, y, z):
        if self.matrix[x][y][z] == 0:
            return

        self.matrix[x][y][z] = 0
        self.cnt[x] -= 1
        heapq.heappush(self.heap, (-self.cnt[x], -x))

    def largestMatrix(self):
        while self.cnt[-self.heap[0][1]] != -self.heap[0][0]:
            heapq.heappop(self.heap)
        return -self.heap[0][1]
''',
    call='''m = Matrix3D(3)
r = []
m.setCell(0, 0, 0)
m.setCell(1, 1, 0)
m.setCell(1, 0, 1)
m.setCell(1, 0, 1)
r.append(m.largestMatrix())
m.unsetCell(1, 0, 1)
r.append(m.largestMatrix())
m.setCell(2, 0, 0)
m.setCell(2, 1, 1)
r.append(m.largestMatrix())
r''',
    expect=[1, 1, 2],
    views=[
        dict(type='text', fn=_layers, size=22, h=70),
        dict(type='array', var='self.cnt', label='cnt[x]：每一层 1 的个数', pointers={'x': 'blue'}, h=170),
        dict(type='heap', var='self.heap', label='heap (−cnt, −x)', fmt=_hp, top_color='green', h=170),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('z', 'z', 'cyan'),
           ('堆顶(−cnt,−x)', lambda S: S['self.heap'][0] if S.get('self.heap') else None, 'green')],
    skip=['self.matrix = [[[0]', 'self.heap = []'],
    captions={
        'self.cnt = [0] * n': '`cnt[x]` 记录第 x 层现有多少个 1，初始全为 0',
        'for x in range': '依次把每一层放进堆',
        'heapq.heappush(self.heap, (0, -x))': '放入 `(0, {-x})`：取 `-x`，次数相同时 x 大的才在堆顶',
        'if self.matrix[x][y][z] == 1': lambda S, B, r: (f'`matrix[{S.x}][{S.y}][{S.z}]` 已经是 1 → 什么都不用做' if S['self.matrix'][S.x][S.y][S.z] == 1
                                                         else f'`matrix[{S.x}][{S.y}][{S.z}]` 是 0 → 需要置 1'),
        'if self.matrix[x][y][z] == 0': lambda S, B, r: (f'`matrix[{S.x}][{S.y}][{S.z}]` 已经是 0 → 什么都不用做' if S['self.matrix'][S.x][S.y][S.z] == 0
                                                         else f'`matrix[{S.x}][{S.y}][{S.z}]` 是 1 → 需要置 0'),
        12: '无事发生，直接返回',
        20: '无事发生，直接返回',
        'self.matrix[x][y][z] = 1': '置 1：`matrix[{x}][{y}][{z}] = 1`',
        'self.matrix[x][y][z] = 0': '置 0：`matrix[{x}][{y}][{z}] = 0`',
        'self.cnt[x] += 1': '第 {x} 层多了一个 1：`cnt[{x}]` = =={self.cnt[x]}==',
        'self.cnt[x] -= 1': '第 {x} 层少了一个 1：`cnt[{x}]` = =={self.cnt[x]}==',
        'heapq.heappush(self.heap, (-self.cnt[x], -x))': '压入新的 `({-self.cnt[x]}, {-x})`；这一层旧的记录不去找，留着以后再清',
        'while self.cnt[-self.heap[0][1]] != -self.heap[0][0]': lambda S, B, r: (
            f'堆顶记录第 {-S["self.heap"][0][1]} 层有 {-S["self.heap"][0][0]} 个 1，而 `cnt` 里实际是 {S["self.cnt"][-S["self.heap"][0][1]]} → ==不相等，是过期记录=='
            if S['self.cnt'][-S['self.heap'][0][1]] != -S['self.heap'][0][0]
            else f'堆顶记录第 {-S["self.heap"][0][1]} 层有 {-S["self.heap"][0][0]} 个 1，和 `cnt` 一致 → ==有效，停止清理=='),
        'heapq.heappop(self.heap)': '懒删除：把过期的堆顶弹掉',
        'return -self.heap[0][1]': '最多 1 的层（并列取最大 x）= =={ret}==',
    },
    cards=dict(
        one_liner='操作直接改数组，查询靠堆：过期记录等到了堆顶再删',
        complexity='`setCell` / `unsetCell` `O(log n)`，空间 `O(n³)`',
        problem=['`Matrix3D(n)`：`n×n×n` 的 0/1 矩阵，初始全 0',
                 '`setCell` / `unsetCell` 把某格置 1 / 置 0',
                 '`largestMatrix()`：返回 1 最多的 `matrix[x]` 的 x，并列取最大的 x'],
        quote='python原生的堆不支持删除指定元素的操作，于是在这里采用懒删除的方法比较方便。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 100`，三维数组直接模拟；`cnt[x]` 记每层 1 的个数',
              '堆里存 `(-cnt[x], -x)`：堆顶就是 1 最多、并列时 x 最大的层',
              '每次 `cnt` 变化就压入新记录；查询时堆顶和 `cnt` 对不上就弹掉'],
        summary=['`setCell` / `unsetCell` / `largestMatrix` 均摊 `O(log n)`，空间 `O(n³)`',
                 '易错：取 `-x` 才能让并列时 x 更大的排在小根堆顶',
                 '易错：已经是目标值时必须直接 `return`，否则 `cnt` 会重复计数',
                 '旧记录不会立刻删，只在堆顶不一致时才弹出',
                 '原文有 `import heapq`，引擎已预先注入，这里省略'],
    ),
)
