def _cell(S, i, j, v):
    if 'res' in S and 'cols' in S and j == S['res'] and S['res'] < S['cols'] and v == 1:
        return 'green'
    return None


def _dim(S, i, j, v):
    return 'r' in S and i < S['r']


CONFIG = dict(
    num=1428, title='至少有一个1的最左端列', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='逐行二分最左的 1', tags=['灵神题单'],
    setup='''
class BinaryMatrix:
    def __init__(self, m):
        self.m = m
    def get(self, row, col):
        return self.m[row][col]
    def dimensions(self):
        return [len(self.m), len(self.m[0])]
''',
    code='''
class Solution(object):
    def leftMostColumnWithOne(self, binaryMatrix):

        rows, cols = binaryMatrix.dimensions()

        res = cols
        for r in range(rows):
            if binaryMatrix.get(r, res - 1) == 1:
                left = 0
                right = res - 1
                while left < right:
                    mid = (left + right) // 2
                    if binaryMatrix.get(r, mid) == 1:
                        right = mid
                    else:
                        left = mid + 1
                
                res = right
                if res == 0:
                    return 0
        
        if res == cols:
            return -1
        
        return res
''',
    call='Solution().leftMostColumnWithOne(BinaryMatrix([[0,0,0,1],[0,0,1,1],[0,1,1,1],[0,0,0,0]]))',
    expect=1,
    skip=['left = 0', 'right = res - 1'],
    views=[
        dict(type='text', fn=lambda S: (f"当前最左的 1 在第 `{S['res']}` 列（`res`）；第 `{S['r']}` 行只需在 `[{S['left']}, {S['right']}]` 里二分" if 'left' in S and 'r' in S and 'res' in S else (f"目前答案 `res = {S['res']}`（=列数表示还没找到）" if 'res' in S else ''))),
        dict(type='grid', var=lambda S: S['binaryMatrix'].m, label='binaryMatrix（绿 = 当前 res 列的 1）', color=_cell, dim=_dim, cell=110, h=420,
             cursors=[('r', 'mid', 'yellow', 'mid')],
             rows=lambda S: [f"行{i}" for i in range(len(S['binaryMatrix'].m))]),
    ],
    watch=['r', 'left', 'right', 'mid', ('res', 'res', 'green')],
    captions={
        'rows, cols =': '`rows = {rows}`，`cols = {cols}`（只能用 `get(r, c)` 看单元格）',
        'res = cols': '`res` 记录目前见到的最左 1 的列，先设成 `cols`（表示还没有）',
        'for r in range(rows)': '行与行互不相关，逐行处理：第 `{r}` 行',
        'if binaryMatrix.get(r, res - 1) == 1': lambda S, B, r: (f'`get({S.r}, {S.res - 1}) = 1`：这一行在 `res` 左边（含 res-1）有 1，值得二分' if S.binaryMatrix.get(S.r, S.res - 1) == 1 else f'`get({S.r}, {S.res - 1}) = 0`：这一行连 `res-1` 列都是 0，不可能更靠左 → ==整行跳过==，省掉二分'),
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：继续二分' if S.left < S.right else f'`left = right = {S.left}`：这一行最左的 1 就在这一列'),
        'mid = (left + right)': '`mid = {mid}`',
        'if binaryMatrix.get(r, mid) == 1': lambda S, B, r: (f'`get({S.r}, {S.mid}) = 1`：右边全是 1，最左的 1 在 `[left, mid]` → `right = mid`' if S.binaryMatrix.get(S.r, S.mid) == 1 else f'`get({S.r}, {S.mid}) = 0`：左边全是 0，最左的 1 在 `[mid+1, right]` → `left = mid + 1`'),
        'right = mid': '`right = mid = {right}`（mid 本身是 1，不能排除）',
        'left = mid + 1': '`left = mid + 1 = {left}`',
        'res = right': '这一行最左的 1 在第 `{right}` 列 → `res = {res}`（一定比之前更靠左）',
        'if res == 0': lambda S, B, r: ('已经在第 0 列，不可能更靠左 → 提前返回 0' if S.res == 0 else f'`res = {S.res} ≠ 0`：还可能有更靠左的，继续下一行'),
        'if res == cols': lambda S, B, r: ('`res` 仍等于 `cols`：没有任何一行有 1 → 返回 -1' if S.res == S.cols else f'`res = {S.res} < cols = {S.cols}`：找到了'),
        'return res': '最左的有 1 的列：`{res}`',
    },
    cards=dict(
        one_liner='逐行二分找最左的 1，只在比当前 res 更靠左时才二分',
        complexity='时间 `O(rows · log cols)`，空间 `O(1)`',
        problem=['二进制矩阵每行升序（0 在左、1 在右），只能 `get(r, c)` 取值、`dimensions()` 取尺寸',
                 '返回至少有一个 1 的最左边的列下标，没有则 `-1`',
                 '本视频：4×4 矩阵 → `1`'],
        quote='行与行之间并没有任何关联，因此在这里需要从上到下枚举每一行，然后找出当前行最左侧1所在的列，而其中最左侧的列即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['每行 0 在左、1 在右 → 最左的 1 可以二分',
              '`get(r, mid) == 1`：最左 1 在 `[left, mid]`，`right = mid`；否则 `left = mid + 1`',
              '用 `res` 记录已有答案，只有 `get(r, res-1) == 1` 才值得二分，否则整行跳过'],
        summary=['时间 `O(rows · log cols)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`mid = (left + right) / 2` 已改为 `//`；开头的类注释已删去，`BinaryMatrix` 在 setup 里模拟',
                 '`right = mid` 配 `left + right` 向下取整，不会死循环',
                 '`res == 0` 可提前返回；`res == cols` 说明全是 0，返回 -1'],
    ),
)
