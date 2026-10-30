G = [[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]]


def _color(S, i, j, v):
    if 'right' not in S:
        return 'green' if v else None
    if v:
        return 'green'
    inside = S['left'] <= j <= S['right'] and S['top'] <= i <= S['bottom']
    return 'purple' if inside else None


def _txt(S):
    if 'right' not in S:
        return ''
    if S['left'] > S['right']:
        return '边界还是初值（left 在最右、right 在最左），还没遇到 1'
    return f"矩形：行 `{S['top']}~{S['bottom']}`，列 `{S['left']}~{S['right']}`，面积 `{(S['bottom'] - S['top'] + 1) * (S['right'] - S['left'] + 1)}`"


CONFIG = dict(
    num=3195, title='包含所有 1 的最小矩形面积 I', difficulty='Medium', category='网格图',
    author='yiduobo', technique='扫描求 1 的外边界',
    tags=[],
    code='''
class Solution(object):
    def minimumArea(self, grid):

        m = len(grid)
        n = len(grid[0])

        left, right = n - 1, 0
        top, bottom = m - 1, 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    top = min(top, i)
                    bottom = max(bottom, i)
                    left = min(left, j)
                    right = max(right, j)

        return (bottom - top + 1) * (right - left + 1)
''',
    call='Solution().minimumArea([[0,0,1,0],[1,0,0,0],[0,0,0,1]])',
    expect=12,
    views=[
        dict(type='grid', var='grid', h=380, cursors=[('i', 'j', 'yellow', '(i,j)')], color=_color),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('top', 'top', 'cyan'), ('bottom', 'bottom', 'orange')],
    captions={
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列',
        'left, right = n - 1': '`left` 先放在最右 `{left}`，`right` 先放在最左 `0`：之后只会 left 变小、right 变大',
        'top, bottom = m - 1': '`top` 先放在最下 `{top}`，`bottom` 先放在最上 `0`',
        'if grid[i][j] == 1': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 1`：是 1，它不能在矩形外面 → 更新四条边' if S.grid[S.i][S.j] == 1
                                               else f'`grid[{S.i}][{S.j}] = 0`：不影响矩形'),
        'top = min': '`top` = min({B.top}, {i}) = =={top}==',
        'bottom = max': '`bottom` = max({B.bottom}, {i}) = =={bottom}==',
        'left = min': '`left` = min({B.left}, {j}) = =={left}==',
        'right = max': '`right` = max({B.right}, {j}) = =={right}==',
        'return': '外边界已定：高 `{bottom - top + 1}` × 宽 `{right - left + 1}` = =={ret}==',
    },
    cards=dict(
        one_liner='顶着最外侧的 1 画框，里面的 1 自然全被盖住',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['给定二进制矩阵 `grid`，用边水平/竖直的矩形盖住所有 `1`',
                 '求这种矩形的最小面积',
                 '本视频：`[[0,0,1,0],[1,0,0,0],[0,0,0,1]]` → `12`'],
        quote='只要矩形能覆盖住最外侧的1，那么就必然可以覆盖住内部的1。',
        quote_src='—— yiduobo 题解原文',
        idea=['列上至少要盖住 `left ~ right`，行上至少要盖住 `top ~ bottom`',
              '所有 1 都落在这个范围内，所以刚好盖住就是最优',
              '用 `min`/`max` 扫一遍网格求这四个值'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '初值：`left`/`top` 取最大下标，`right`/`bottom` 取 0，保证第一个 1 就能覆盖它们',
                 '最后宽高各 `+1`，是格子数不是距离',
                 '对比灵神：灵神用 `inf` 做初值并省去 bottom 的 max；yiduobo 四个值都用 min/max'],
    ),
)
