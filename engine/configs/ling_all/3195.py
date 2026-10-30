G = [[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]]


def _color(S, i, j, v):
    if 'right' not in S or 'top' not in S or S['top'] == float('inf') or S['left'] == float('inf'):
        return 'green' if v else None
    inside = S['left'] <= j <= S['right'] and S['top'] <= i <= S['bottom']
    if v:
        return 'green'
    return 'purple' if inside else None


def _txt(S):
    if 'right' not in S:
        return ''
    if S['left'] == float('inf'):
        return '还没遇到 1，边界未定'
    return f"边界：行 `{S['top']}~{S['bottom']}`，列 `{S['left']}~{S['right']}`，面积 `{(S['right'] - S['left'] + 1) * (S['bottom'] - S['top'] + 1)}`"


CONFIG = dict(
    num=3195, title='包含所有 1 的最小矩形面积 I', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='维护 1 的上下左右边界',
    tags=[],
    code='''
class Solution:
    def minimumArea(self, grid: List[List[int]]) -> int:
        left = top = inf
        right = bottom = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x:
                    left = min(left, j)
                    right = max(right, j)
                    top = min(top, i)
                    bottom = i
        return (right - left + 1) * (bottom - top + 1)
''',
    call='Solution().minimumArea([[0,0,1,0],[1,0,0,0],[0,0,0,1]])',
    expect=12,
    views=[
        dict(type='grid', var='grid', h=380, cursors=[('i', 'j', 'yellow', '(i,j)')], color=_color),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('top', 'top', 'cyan'), ('bottom', 'bottom', 'orange')],
    captions={
        'left = top = inf': '`left`、`top` 取最小，所以先设为无穷大',
        'right = bottom = 0': '`right`、`bottom` 取最大，先设为 0',
        'if x': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 1`：遇到 1，用它的行列更新四条边' if S.x else f'`grid[{S.i}][{S.j}] = 0`：不是 1，跳过'),
        'left = min': '最左的 1 的列：`left` = min({B.left}, {j}) = =={left}==',
        'right = max': '最右的 1 的列：`right` = max({B.right}, {j}) = =={right}==',
        'top = min': '最上的 1 的行：`top` = min({B.top}, {i}) = =={top}==',
        'bottom = i': '按行从上往下扫，当前行 `{i}` 一定是目前最靠下的 → `bottom` = =={bottom}==',
        'return': '矩形宽 `{right} - {left} + 1 = {right - left + 1}`，高 `{bottom} - {top} + 1 = {bottom - top + 1}`，面积 =={ret}==',
    },
    cards=dict(
        one_liner='矩形只要框住最外面的四个 1：上下左右各取极值',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['二维 0/1 数组，求边平行于坐标轴、包含所有 `1` 的最小矩形面积',
                 '示例：`[[0,1,0],[1,0,1]]` → `6`',
                 '本视频：`3×4` 网格 → `12`'],
        quote='找到最左最右的 1 的列号，分别记作 left、right；找到最上最下的 1 的行号，分别记作 top、bottom。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历全部格子，遇到 `1` 就更新四个边界',
              '面积至少是 `(right-left+1) * (bottom-top+1)`，且正好取得到',
              '行是从上往下扫的，所以 `bottom = i` 不必取 max'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '`left`、`top` 初值要是无穷大，`right`、`bottom` 初值 0 即可',
                 '题目保证至少有一个 1，所以不会返回无穷大相关的值',
                 '宽、高都要 `+1`：只有一个 1 时面积为 1'],
    ),
)
