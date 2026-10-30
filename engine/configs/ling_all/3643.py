CONFIG = dict(
    num=3643, title='垂直翻转子矩阵', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双指针 · 同 344 反转字符串',
    tags=['难度分 1235'],
    code='''
class Solution:
    def reverseSubmatrix(self, grid: List[List[int]], x: int, y: int, k: int) -> List[List[int]]:
        l, r = x, x + k - 1
        while l < r:
            for j in range(y, y + k):
                grid[l][j], grid[r][j] = grid[r][j], grid[l][j]
            l += 1
            r -= 1
        return grid
''',
    call='Solution().reverseSubmatrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 1, 0, 3)',
    expect=[[1, 2, 3, 4], [13, 14, 15, 8], [9, 10, 11, 12], [5, 6, 7, 16]],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 待翻转的子矩阵，蓝 = l 行，粉 = r 行）', cell=90, h=460,
             color=lambda S, i, j, v: (('blue' if i == S.get('l') else 'pink' if i == S.get('r') else 'green')
                                       if S['x'] <= i < S['x'] + S['k'] and S['y'] <= j < S['y'] + S['k'] else None),
             cursors=[('l', 'j if "j" in _inner else None', 'yellow', '')]),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('j', 'j', 'yellow')],
    captions={
        'l, r = x': '行号范围 `[{x}, {x}+{k}-1]`：`l = {l}`，`r = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}` → 这两行还没交换，继续' if S.l < S.r
                                       else f'`l = {S.l} >= r = {S.r}` → 双指针相遇，结束'),
        'for j in range': '换这两行的第 `{j}` 列（列范围 `[y, y+k-1]`）',
        'grid[l][j]': '交换 `grid[{l}][{j}]` 和 `grid[{r}][{j}]`',
        'l += 1': '`l` 下移 → {l}',
        'r -= 1': '`r` 上移 → {r}',
        'return grid': '返回翻转后的 `grid`',
    },
    cards=dict(
        one_liner='把「反转字符串」搬到行上：双指针交换整段列',
        complexity='时间 `O(k²)`，空间 `O(1)`',
        problem=['子矩阵左上角 `(x, y)`，边长 `k`，把它的行顺序上下翻转',
                 '示例：`x=1, y=0, k=3`',
                 '→ 第 1 行与第 3 行的前 3 列互换'],
        quote='类似 344. 反转字符串，用双指针实现：初始化 l=x，r=x+k-1。循环直到 l≥r。',
        quote_src='—— 灵茶山艾府题解',
        idea=['行号范围 `[x, x+k-1]`，列号范围 `[y, y+k-1]`',
              '`l`、`r` 从两端向中间，每次对每个 `j` 交换 `grid[l][j]` 与 `grid[r][j]`',
              '`l >= r` 时停止'],
        summary=['时间 `O(k²)`，空间 `O(1)`',
                 '易错：只交换列 `[y, y+k-1]`，不是整行',
                 '另一种写法：用切片整段交换 `grid[l][y:y+k], grid[r][y:y+k] = ...`'],
    ),
)
