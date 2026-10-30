MAT = [[0, 0, 0],
       [0, 1, 0],
       [0, 0, 0]]

SETUP = '''
import bisect


class SortedList:
    """sortedcontainers.SortedList 的最小替代：只实现 add / discard / bisect_right / 下标访问"""

    def __init__(self):
        self.a = []

    def add(self, x):
        bisect.insort(self.a, x)

    def discard(self, x):
        k = bisect.bisect_left(self.a, x)
        if k < len(self.a) and self.a[k] == x:
            self.a.pop(k)

    def bisect_right(self, x):
        return bisect.bisect_right(self.a, x)

    def __getitem__(self, k):
        return self.a[k]

    def __iter__(self):
        return iter(self.a)

    def __len__(self):
        return len(self.a)

    def __repr__(self):
        return f'SortedList({self.a})'
'''


def _sl(S):
    sl = S.get('sl')
    return list(sl) if sl is not None and S.get('_line', 0) >= 38 else None


def _ring(S):
    a = S.get('ans')
    if S.get('_line') != 63 or not a or not a[0]:
        return set()
    sz, r, c = a[0], -a[1], -a[2]
    return {(x, y) for x in range(r, r + sz) for y in range(c, c + sz) if x in (r, r + sz - 1) or y in (c, c + sz - 1)}


def _color(S, i, j, v):
    ln = S.get('_line', 0)
    if ln == 63:
        return 'green' if (i, j) in _ring(S) else None
    k = S.get('k')
    if k is None or ln < 38:
        return None
    sl = S.get('sl')
    if sl is not None and i + j == k and i in list(sl):
        return 'green'
    if i + j == k:
        return 'blue'
    return None


def _txt1(S):
    ln = S.get('_line', 0)
    if not (38 <= ln < 63) or 'j' not in S or 'i' not in S or S['i'] + S['j'] != S['k']:
        return ''
    i, j = S['i'], S['j']
    return (f"`({i},{j})`：向左 `{j - S['left1'][i][j]}` 个 0，向下 `{S['down1'][i][j] - i}` 个 0，"
            f"向右 `{S['right1'][i][j] - j}` 个 0，向上 `{i - S['up1'][i][j]}` 个 0")


def _txt3(S):
    ln = S.get('_line', 0)
    if 'k' not in S or ln < 38 or ln == 63:
        return ''
    tr = {x: v for x, v in enumerate(S.get('to_remove', [])) if v}
    return f"反对角线 `i + j = {S['k']}`　到期表 `to_remove` = {tr if tr else '空'}　（第 x 行到期：把它的右上角从 sl 删掉）"


def _cap_add(S, B, r):
    i, j = S.i, S.j
    sz = min(j - S.left1[i][j], S.down1[i][j] - i)
    return (f"`({i},{j})` 是黑色，当==右上角==：`{i}` 加入 `sl` → {list(S.sl)}。向左 `{j - S.left1[i][j]}`、向下 `{S.down1[i][j] - i}` 个 0，"
            f"`sz = {sz}`：服务左下角在 `[{i}, {i + sz - 1}]` 行的正方形，第 `{i + sz - 1}` 行到期")


def _cap_i2(S, B, r):
    i, j = S.i, S.j
    sz = min(S.right1[i][j] - j, i - S.up1[i][j])
    return (f"`({i},{j})` 当==左下角==：向右 `{S.right1[i][j] - j}` 个 0，向上 `{i - S.up1[i][j]}` 个 0 → 边长至多 `{sz}`；"
            f"在 `sl` 里找大于 `{i - sz}` 的最小横坐标 → `i2 = {S.i2}`")


def _cap_ans(S, B, r):
    i2 = S.i2
    return (f"边长 `{S.i} - {i2} + 1 = {S.i - i2 + 1}`，`ans = max(..)` → `{S.ans}`")


def _cap_if(S, B, r):
    i, j = S.i, S.j
    if S.matrix[i][j] == 0:
        return f"`matrix[{i}][{j}] = 0`：黑色，可当右上角，也可当左下角"
    return f"`matrix[{i}][{j}] = 1`：白色，什么都不做"


def _cap_disc(S, B, r):
    return f"第 `{S.i}` 行：横坐标 `{S.i2}` 的右上角服务到期 → 从 `sl` 删掉 → {list(S.sl)}"


CONFIG = dict(
    num='面试题 17.23', title='最大黑方阵', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举反对角线 · 有序集合维护右上角',
    tags=['灵神题单', '常用数据结构', '难度分 2800'],
    code='''
class Solution:
    def findSquare(self, matrix: List[List[int]]) -> List[int]:
        n = len(matrix)
        # 预处理每个格子左右上下最近的 1 的位置
        left1 = [[0] * n for _ in range(n)]
        right1 = [[0] * n for _ in range(n)]
        up1 = [[0] * n for _ in range(n)]
        down1 = [[0] * n for _ in range(n)]

        for i, row in enumerate(matrix):
            l = -1
            for j, x in enumerate(row):
                if x:
                    l = j
                left1[i][j] = l

            r = n
            for j in range(n - 1, -1, -1):
                if row[j]:
                    r = j
                right1[i][j] = r

        for j, col in enumerate(zip(*matrix)):
            u = -1
            for i, x in enumerate(col):
                if x:
                    u = i
                up1[i][j] = u

            d = n
            for i in range(n - 1, -1, -1):
                if col[i]:
                    d = i
                down1[i][j] = d

        ans = (0, 0, 0)  # (size, -r, -c)

        for k in range(n * 2 - 1):
            sl = SortedList()
            min_j = max(k - n + 1, 0)
            max_j = min(k, n - 1)
            to_remove = [[] for _ in range(n)]

            for j in range(max_j, min_j - 1, -1):
                i = k - j
                if matrix[i][j] == 0:
                    # (i,j) 作为正方形的右上角，可以服务于左下角横坐标在 [i,i+sz-1] 中的正方形
                    sl.add(i)
                    sz = min(j - left1[i][j], down1[i][j] - i)  # min(左,下)
                    to_remove[i + sz - 1].append(i)  # 在未来移除

                    # (i,j) 作为正方形的左下角
                    # 找 sl 中的大于 i-size 的最小横坐标 i2
                    sz = min(right1[i][j] - j, i - up1[i][j])  # min(右,上)
                    i2 = sl[sl.bisect_right(i - sz)]
                    # i-i2+1 就是 (i,j) 作为正方形左下角时，正方形的最大边长
                    ans = max(ans, (i - i2 + 1, -i2, -j))

                # 移除那些超过服务范围的右上角横坐标
                for i2 in to_remove[i]:
                    sl.discard(i2)

        return [-ans[1], -ans[2], ans[0]] if ans[0] else []
''',
    call=f'Solution().findSquare({MAT})',
    expect=[0, 0, 3],
    setup=SETUP,
    skip=[3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34,
          39, 40, 41, 42, 44, 45, 49, 50, 54, 60],
    max_steps=42,
    views=[
        dict(type='grid', var='matrix', label='matrix（0 = 黑；蓝 = 当前反对角线；绿 = sl 中的右上角；黄框 = 当前格子）', cell=96, h=330,
             color=_color, cursors=[(lambda S: S.get('i') if 38 <= S.get('_line', 0) < 63 else None, 'j', 'yellow')]),
        dict(type='text', fn=_txt1, size=22, h=40),
        dict(type='text', fn=_txt3, size=22, h=40),
        dict(type='array', var=_sl, label='sl：有序集合里的右上角横坐标', cell=80, h=150),
    ],
    watch=[('k', 'k', 'purple'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        36: '预处理：每格左右上下最近的 1 在哪，用来算连续 0 的长度。`ans` 记 `(边长, -r, -c)`，取 max 即边长最大、r c 最小',
        38: lambda S, B, r: (f'枚举第 `{S.k}` 条反对角线（`i + j = {S.k}`）：右上角都在同一条线上' if not ('k' in B and B.k == S.k) else '反对角线全部枚举完'),
        46: _cap_if,
        48: _cap_add,
        55: _cap_i2,
        57: _cap_ans,
        61: _cap_disc,
        63: lambda S, B, r: f'转成 `[r, c, size]` = `{r}`：绿色就是答案方阵',
    },
    cards=dict(
        one_liner='枚举左下角，右上角放进有序集合里查',
        complexity='时间 `O(n^2 log n)`，空间 `O(n^2)`',
        problem=['`n × n` 的方阵，`0` 是黑、`1` 是白，找四条边都是黑色的最大子方阵',
                 '返回 `[r, c, size]`：左上角行列和边长；多个答案取 `r` 最小，再取 `c` 最小',
                 '本视频：3×3 示例，外圈全黑、中间一个白 → `[0,0,3]`'],
        quote='考虑==左下角==在 (i,j) 的正方形，它的最大边长是多少？……这只看了正方形的下边和左边这两条边，我们还得确认上边和右边是否全为 0，这需要正方形右上角的信息。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左下角往右、往上的 0 取小，是边长上界；上边、右边还要靠==右上角==验证',
              '右上角都在同一条反对角线上 → 逐条反对角线遍历，下面的格子横坐标大，后访问',
              '有序集合里存“还在服务的右上角横坐标”，二分找大于 `i - sz` 的最小值 `i2`，边长就是 `i - i2 + 1`',
              '右上角服务到期（`i + sz - 1` 行）就删掉'],
        summary=['时间 `O(n^2 log n)`，空间 `O(n^2)`；这是进阶做法，可以解 `2000 × 2000`',
                 '`ans = (size, -r, -c)`：用元组 max 同时处理“边长最大、r 最小、c 最小”',
                 '易错：到期要在循环末尾删除，`to_remove` 下标是 `i + sz - 1`',
                 '原文用 `SortedList`，本视频在 `setup` 里写了最小替代，逻辑一致',
                 '相似题：CF628E Zbazi in Zeydabad'],
    ),
)
