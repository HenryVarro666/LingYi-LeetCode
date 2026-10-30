CONFIG = dict(
    num=3643, title='垂直翻转子矩阵', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='top / bottom 相向交换行',
    tags=['难度分 1235'],
    code='''
class Solution(object):
    def reverseSubmatrix(self, grid, x, y, k):
        
        top = x
        bottom = x + k - 1
        while top < bottom:
            for index in range(y, y + k):
                grid[top][index], grid[bottom][index] = grid[bottom][index], grid[top][index]
            top += 1
            bottom -= 1
        
        return grid
''',
    call='Solution().reverseSubmatrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 1, 0, 3)',
    expect=[[1, 2, 3, 4], [13, 14, 15, 8], [9, 10, 11, 12], [5, 6, 7, 16]],
    views=[
        dict(type='grid', var='grid', label='grid（绿框 = 子矩阵，蓝 = top 行，粉 = bottom 行）', cell=90, h=460,
             color=lambda S, i, j, v: ('blue' if i == S.get('top') else 'pink' if i == S.get('bottom') else 'green')
             if S['x'] <= i < S['x'] + S['k'] and S['y'] <= j < S['y'] + S['k'] and S.get('top') is not None
             and S['top'] < S['bottom'] + 1 and i in (S['top'], S['bottom']) else
             ('green' if S['x'] <= i < S['x'] + S['k'] and S['y'] <= j < S['y'] + S['k'] else None),
             cursors=[('top', 'index if "index" in _inner else None', 'yellow', '')]),
    ],
    watch=[('top', 'top', 'blue'), ('bottom', 'bottom', 'pink'), ('index', 'index', 'yellow')],
    captions={
        'top = x': '子矩阵最上面一行是 `x = {x}`：`top = {top}`',
        'bottom = x + k - 1': '最下面一行是 `x + k - 1`：`bottom = {bottom}`',
        'while top < bottom': lambda S, B, r: (f'`top = {S.top} < bottom = {S.bottom}` → 两行不同，要交换' if S.top < S.bottom
                                              else f'`top = {S.top} >= bottom = {S.bottom}` → 上下相遇，翻转完成'),
        'for index in range': '处理第 `{index}` 列（只换 `y` 到 `y+k-1` 这一段）',
        'grid[top][index]': '交换 `grid[{top}][{index}]` 与 `grid[{bottom}][{index}]`',
        'top += 1': '`top` 向下移动 → {top}',
        'bottom -= 1': '`bottom` 向上移动 → {bottom}',
        'return grid': '返回翻转后的 `grid`',
    },
    cards=dict(
        one_liner='上下两行指针向中间靠拢，只交换子矩阵那一段',
        complexity='时间 `O(k²)`，空间 `O(1)`',
        problem=['`(x, y)` 是正方形子矩阵左上角，`k` 是边长',
                 '把子矩阵的行顺序上下翻转，其余不动',
                 '示例：`x=1, y=0, k=3` 翻转第 1~3 行的前 3 列'],
        quote='子矩阵的左上角为(x, y)，那么矩阵最上面的行是x，最下面的行则为x + k - 1，于是可以设置两个变量top和bottom，从上下两侧向中靠拢。',
        quote_src='—— yiduobo 题解原文',
        idea=['`top = x`，`bottom = x + k - 1`',
              '若 `top < bottom`，交换两行中 `y` 到 `y+k-1` 的元素',
              '`top` 下移、`bottom` 上移，直到相遇'],
        summary=['时间 `O(k²)`，空间 `O(1)`',
                 '易错：列范围是 `[y, y+k)`，不是整行',
                 '易错：`top >= bottom` 就停，中间那一行不用动',
                 '原文就是 Python 3 可运行的写法，未做修改'],
    ),
)
