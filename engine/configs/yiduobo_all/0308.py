def _cur(S, name):
    return S.get(name) if isinstance(S.get(name), int) else None


CONFIG = dict(
    num=308, title='二维区域和检索 - 可变', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维树状数组', tags=['常用数据结构'],
    code='''
class NumMatrix(object):

    def add(self, x, y, v):
        tmp = y
        while x <= self.m:
            y = tmp
            while y <= self.n:
                self.f[x][y] += v
                y += y & -y

            x += x & -x

    def __init__(self, matrix):
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.f = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        self.matrix = [[0] * self.n for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                self.add(i + 1, j + 1, matrix[i][j])
                self.matrix[i][j] = matrix[i][j]

    def update(self, row, col, val):
        delta = val - self.matrix[row][col]
        self.matrix[row][col] = val
        self.add(row + 1, col + 1, delta)

    def get(self, x, y):
        res = 0
        tmp = y
        while x > 0:
            y = tmp
            while y > 0:
                res += self.f[x][y]
                y -= y & -y
            
            x -= x & -x

        return res

    def sumRegion(self, row1, col1, row2, col2):
        return self.get(row2 + 1, col2 + 1) - self.get(row2 + 1, col1) - self.get(row1, col2 + 1) + self.get(row1, col1)
''',
    call='''obj = NumMatrix([[3, 0], [5, 6]])
out = [obj.sumRegion(0, 1, 1, 1)]
obj.update(0, 1, 2)
out.append(obj.sumRegion(0, 1, 1, 1))
out''',
    expect=[6, 8],
    views=[
        dict(type='table', var='self.matrix', label='matrix（原始值，下标从 0）', h=190, cell=80,
             cursors=[('row', 'col', 'yellow', '改')]),
        dict(type='table', var='self.f', label='二维树状数组 f（下标从 1，第 0 行列不用）；黄 = 正在读写的格子', h=260, cell=80,
             cursors=[('x', 'y', 'yellow', '(x,y)')]),
        dict(type='text', h=70, size=28, fn=lambda S: (
            f"区域和 = get({S['row2']+1},{S['col2']+1}) − get({S['row2']+1},{S['col1']}) − get({S['row1']},{S['col2']+1}) + get({S['row1']},{S['col1']})"
            if 'row2' in S and 'col1' in S else '')),
    ],
    watch=['x', 'y', 'res', ('out', 'out', 'green')],
    skip=['while y <= self.n', 'while x <= self.m', 'y = tmp', 'while x > 0', 'while y > 0', 'tmp = y', 'self.m = len', 'self.n = len', 'self.f = [[0]', 'self.matrix = [[0]', 'self.matrix[i][j] = matrix[i][j]', 'for i in range(self.m)', 'for j in range(self.n)'],
    max_steps=110,
    captions={
        'self.f[x][y] += v': '`f[{x}][{y}]` 加上 `{v}` → {self.f[x][y]}：这一格管着一块矩形',
        'y += y & -y': '列方向 `y += lowbit(y)`：跳到管着它的下一格 → `{y}`',
        'x += x & -x': '行方向 `x += lowbit(x)`：往上一层 → `{x}`',
        'y = tmp': '内层从原来的列 `{tmp}` 重新开始跳',
        'while x <= self.m': '行 `x = {x}`，是否还在表内（`<= m = {self.m}`）：{"是" if x <= self.m else "否，更新完毕"}',
        'while y <= self.n': '列 `y = {y}`，是否还在表内（`<= n = {self.n}`）：{"是" if y <= self.n else "否，这一行更新完毕"}',
        'self.add(i + 1, j + 1': '把 `matrix[{i}][{j}] = {matrix[i][j]}` 以 1 起始的下标加入树状数组',
        'delta = val': '改动量 `delta = {val} - 旧值 = {delta}`，树状数组只需加差值',
        'self.matrix[row][col] = val': '先记下新值，下次再改时才能算对差',
        'self.add(row + 1, col + 1, delta)': '把差值 `{delta}` 加到所有管着 `({row+1},{col+1})` 的格子',
        'res += self.f[x][y]': '累加 `f[{x}][{y}]` → `res` = {res}',
        'y -= y & -y': '列方向 `y -= lowbit(y)`：去掉最低位 → `{y}`',
        'x -= x & -x': '行方向 `x -= lowbit(x)`：去掉最低位 → `{x}`',
        'return res': '这个前缀和 =={res}==（f 里按 lowbit 拆出来的几段相加）',
        'return self.get(row2 + 1': '容斥：大块 − 上边 − 左边 + 重叠的左上角，共调用四次 `get`',
        'while y > 0': '列 `y = {y}`，还有没加的段吗：{"有" if y > 0 else "没有了"}',
        'while x > 0': '行 `x = {x}`，还有没加的段吗：{"有" if x > 0 else "没有了"}',
    },
    cards=dict(
        one_liner='二维前缀和 + 二维树状数组：行列各按 lowbit 跳',
        complexity='单次更新/查询 `O(log m · log n)`，空间 `O(mn)`',
        problem=['设计 `NumMatrix`：`update(row, col, val)` 改一个格子，`sumRegion(r1, c1, r2, c2)` 求子矩形和',
                 '本视频：`[[3,0],[5,6]]`，查 `(0,1)-(1,1)` 得 `6`，把 `(0,1)` 改成 `2` 再查得 `8`'],
        quote='与一维树状数组的思路类似，在这里也是将区间和转全为前缀和来进行处理，即左上角为(row1, col1)，右下角为(row2, col2)的二维区间可以认为是右下角为(row2, col2)、(row2，col1 - 1)、(row1 - 1，col2)、(row1 - 1，col1 - 1)，左上角都是(1, 1)的前缀区间通过加减得到',
        quote_src='—— yiduobo 题解原文',
        idea=['区间和 = 四个以 (1,1) 为左上角的前缀和做容斥',
              '前缀和用二维树状数组维护：两重循环，分别按 lowbit 迭代行、列',
              '更新只加「新值 − 旧值」，所以要另存一份 `matrix`'],
        summary=['时间 `O(log m · log n)` 每次操作；建树 `O(mn log m log n)`',
                 '树状数组下标从 1 开始，`sumRegion` 里的 `row2 + 1`、`col1`、`row1` 正是容斥的偏移',
                 '`add` 内层要用 `tmp` 记住起始列，每走一行都要从头跳',
                 '更新前必须先算 `delta`，再写 `self.matrix`'],
    ),
)
