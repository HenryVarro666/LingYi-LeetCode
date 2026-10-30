G = [[1, 7, 3], [9, 8, 2], [4, 5, 6]]
P1 = (7, 21)    # 左下三角（含主对角线）所在代码行
P2 = (24, 38)   # 右上三角


def _phase(S):
    ln = S.get('_line', 0)
    if P1[0] <= ln <= P1[1]:
        return 1
    if P2[0] <= ln <= P2[1]:
        return 2
    return 0


def _on(S, i, j):
    ph = _phase(S)
    if ph == 0 or 'row' not in S:
        return False
    return i - j == S['row'] if ph == 1 else i - j == S['row'] - (S['n'] - 1)


def _written(S, i):
    ph, ln, x = _phase(S), S.get('_line'), S.get('x')
    if not isinstance(x, int):
        return False
    if ph == 1 and ln in (18, 19, 20, 21):
        return i < x or (i == x and ln == 19)
    if ph == 2 and ln in (35, 36, 37, 38):
        return i > x or (i == x and ln == 36)
    return False


def _cell(S, i, j, v):
    if not _on(S, i, j):
        return None
    return 'green' if _written(S, i) else 'blue'


def _cur(S, k):
    ph, ln = _phase(S), S.get('_line')
    if ph == 0 or ln in (7, 16, 24, 33) or 'x' not in S or 'y' not in S:
        return None
    return (S['x'], S['y'])[k]


def _hint(S):
    ph, ln = _phase(S), S.get('_line')
    if ph == 0:
        return '先处理左下三角（含主对角线），再处理右上三角'
    r, n = S['row'], S['n']
    if ph == 1:
        s = f'左下三角：起点 `({r}, 0)` 向右下走到最后一行'
    else:
        s = f'右上三角：终点 `({r}, {n - 1})` 向左上走到第 0 行'
    if ln in (15, 32):
        return s + '；==从小到大排序=='
    if ln in (18, 19, 20, 21, 35, 36, 37, 38):
        return s + '；==pop 取最大的，按原路填回=='
    return s


CONFIG = dict(
    num=3446, title='按对角线进行矩阵排序', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='模拟 · 沿对角线收集、排序、倒序填回',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1373'],
    code='''
class Solution(object):
    def sortMatrix(self, grid):
        
        n = len(grid)

        for row in range(n):
            x = row
            y = 0
            nums = []
            while x < n:
                nums.append(grid[x][y])
                x += 1
                y += 1
            
            nums.sort()
            x = row
            y = 0
            while x < n:
                grid[x][y] = nums.pop()
                x += 1
                y += 1
        
        for row in range(n - 1):
            x = row
            y = n - 1
            nums = []
            while x >= 0:
                nums.append(grid[x][y])
                x -= 1
                y -= 1
            
            nums.sort()
            x = row
            y = n - 1
            while x >= 0:
                grid[x][y] = nums.pop()
                x -= 1
                y -= 1
        
        return grid
''',
    call=f'Solution().sortMatrix({G})',
    expect=[[8, 2, 3], [9, 6, 7], [4, 5, 1]],
    skip=[7, 8, 9, 10, 12, 13, 16, 17, 20, 21, 24, 25, 26, 27, 29, 30, 33, 34, 37, 38],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前对角线，绿 = 已填回；粉框 = 当前走到的格子）', cell=110, h=370,
             color=_cell, cursors=[(lambda S: _cur(S, 0), lambda S: _cur(S, 1), 'pink')]),
        dict(type='array', var='nums', label='nums（收集到的对角线；排序后从末尾 pop 填回）', cell=96, h=190),
        dict(type='text', fn=_hint, size=26, h=90),
    ],
    watch=[('row', 'row', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'cyan'), ('nums', 'nums', 'green')],
    captions={
        4: '`n = {n}`：方阵边长。对角线分两批处理',
        6: lambda S, B, r: ('左下三角的对角线都处理完了' if 'row' in B and S.row == B.row else
                            f'左下三角第 `{S.row}` 条对角线：起点 `({S.row}, 0)`，向右下走到最后一行；先把数收集进 `nums`'),
        11: '收集 `grid[{x}][{y}]` = {nums[-1]} → `nums = {nums}`；`x`、`y` 各加 1，往右下走一格',
        15: '走到 `x = {x}` 越过最后一行，收集完毕。`nums` 从小到大排序：`{nums}`，末尾最大；再回到起点 `({row}, 0)` 边走边 pop 填回',
        18: lambda S, B, r: (f'`x = {S.x} < n`：继续填回' if S.x < S.n else '这条对角线填完了'),
        19: '`nums.pop()` 取走最大的 {grid[x][y]} 填到 `grid[{x}][{y}]`；剩下 `nums = {nums}`',
        23: lambda S, B, r: ('右上三角的对角线也都处理完了' if 'x' in B and 'row' in B and S.row == B.row and S._line == 23 and B.row != 2 and S.row == S.n - 2
                             and B.get('_line') == 23 else
                             f'右上三角第 `{S.row}` 条对角线：终点 `({S.row}, {S.n - 1})`，往左上走到第 0 行；先收集进 `nums`'),
        28: '收集 `grid[{x}][{y}]` = {nums[-1]} → `nums = {nums}`；`x`、`y` 各减 1，往左上走一格',
        32: '走到 `x = {x}` 越过第 0 行，收集完毕。`nums` 从小到大排序：`{nums}`，末尾最大；再回到终点 `({row}, {n - 1})` 边走边 pop 填回',
        35: lambda S, B, r: (f'`x = {S.x} >= 0`：继续填回' if S.x >= 0 else '这条对角线填完了'),
        36: '`nums.pop()` 取最大的 {grid[x][y]} 填到 `grid[{x}][{y}]`（越往左上越小）；剩下 `nums = {nums}`',
        40: '两批对角线都排好了 → 返回 `grid`',
    },
    cards=dict(
        one_liner='沿对角线走一遍收集，排序后倒序（pop）原路填回',
        complexity='时间 `O(n² log n)`，空间 `O(n)`',
        problem=['`n × n` 方阵：左下三角（含主对角线）的每条对角线按==非递增==排序',
                 '右上三角的每条对角线按==非递减==排序，返回调整后的矩阵',
                 '示例：`[[1,7,3],[9,8,2],[4,5,6]]` → `[[8,2,3],[9,6,7],[4,5,1]]`'],
        quote='将nums从小到大排序后，按相同的走法将nums倒序填充回矩阵就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['左下三角：对角线起点都在第 0 列，第 `row` 条的起点是 `(row, 0)`，一直走到最后一行',
              '右上三角：对角线终点都在最后一列，第 `row` 条的终点是 `(row, n-1)`，往左上走到第 0 行',
              '收集 → `sort` → 沿着相同的路线 `pop`：每次取最大，所以从起点到终点逐渐变小'],
        summary=['时间 `O(n² log n)`，空间 `O(n)`',
                 '易错：右上三角是从==终点==往左上走，`pop` 的最大值先放在终点，所以沿对角线向右下看是非递减',
                 '易错：第二批 `for row in range(n - 1)`，不重复处理主对角线',
                 '原文是 Python 2 风格，但可直接在 Python 3 运行，代码未改',
                 '灵神用 `k = i − j + n` 一次枚举全部对角线并用 `min_j` 决定升降序；yiduobo 分两批处理'],
    ),
)
