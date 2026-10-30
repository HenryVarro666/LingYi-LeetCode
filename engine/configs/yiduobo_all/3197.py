G = [[1, 0, 1], [1, 1, 1]]
RET = 15


def _I(S):
    return S.get('_inner') or S


def _in_area(S):
    I = _I(S)
    return 'x1' in I and 'top' in I


def _gc(S, i, j, v):
    I = _I(S)
    if not _in_area(S):
        return None
    if I['top'] <= i <= I['bottom'] and I['left'] <= j <= I['right'] and S.get('_line') == RET:
        return 'yellow'
    if I['x1'] <= i <= I['x2'] and I['y1'] <= j <= I['y2']:
        return 'blue'
    return None


def _fml(S):
    I = _I(S)
    if _in_area(S):
        x1, y1, x2, y2 = I['x1'], I['y1'], I['x2'], I['y2']
        if S.get('_line') == RET:
            h, w = I['bottom'] - I['top'] + 1, I['right'] - I['left'] + 1
            return f'块 `({x1},{y1})~({x2},{y2})`：包住所有 1 的框 = `{h} × {w}` = =={max(1, h * w)}=='
        return f'块 `({x1},{y1})~({x2},{y2})`（蓝色）：找里面所有 1 的上下左右边界'
    if 'res' in S and 'i' in S or 'j' in S:
        return f'当前最小总面积 `res = {S["res"]}`'
    return '用 3 个矩形：先切一刀，再把其中一块切一刀，每块各自算最小外接矩形'


CONFIG = dict(
    num=3197, title='包含所有 1 的最小矩形面积 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举六种划分 + 逐块求外接矩形',
    tags=['动态规划', '常用数据结构', '难度分 2541'],
    code='''
class Solution(object):
    def minimumSum(self, grid):

        def minArea(x1, y1, x2, y2):
            top, bottom = x2, x1
            left, right = y2, y1
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    if grid[i][j] == 1:
                        top = min(top, i)
                        bottom = max(bottom, i)
                        left = min(left, j)
                        right = max(right, j)

            return max(1, (bottom - top + 1) * (right - left + 1))
        

        m = len(grid)
        n = len(grid[0])
        res = m * n

        for i in range(m - 1):
            for i2 in range(i + 1, m - 1):
                res = min(res, minArea(0, 0, i, n - 1) + minArea(i + 1, 0, i2, n - 1) + minArea(i2 + 1, 0, m - 1, n - 1))

            for j in range(n - 1):
                res = min(res, minArea(0, 0, i, n - 1) + minArea(i + 1, 0, m - 1, j) + minArea(i + 1, j + 1, m - 1, n - 1))
                res = min(res, minArea(i + 1, 0, m - 1, n - 1) + minArea(0, 0, i, j) + minArea(0, j + 1, i, n - 1))
        
        
        for j in range(n - 1):
            for j2 in range(j + 1, n - 1):
                res = min(res, minArea(0, 0, m - 1, j) + minArea(0, j + 1, m - 1, j2) + minArea(0, j2 + 1, m - 1, n - 1))
            
            for i in range(m - 1):
                res = min(res, minArea(0, 0, m - 1, j) + minArea(0, j + 1, i, n - 1) + minArea(i + 1, j + 1, m - 1, n - 1))
                res = min(res, minArea(0, j + 1, m - 1, n - 1) + minArea(0, 0, i, j) + minArea(i + 1, 0, m - 1, j))
        
        return res
''',
    call=f'Solution().minimumSum({G})',
    expect=5,
    skip=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 18, 19, 22, 23, 26, 31, 32, 35],
    views=[
        dict(type='text', fn=_fml, size=24, h=70),
        dict(type='grid', var='grid', label='grid（蓝 = 当前这一块，黄 = 块里所有 1 的外接矩形）', cell=96, h=330, color=_gc),
    ],
    watch=[('res', 'res', 'green')],
    captions={
        20: '`res` 初值取 `m × n`（整张网格都盖住一定够）',
        15: lambda S, B, r: f'块 `({S.x1},{S.y1})~({S.x2},{S.y2})`：外接矩形 `{S.bottom - S.top + 1} × {S.right - S.left + 1}` → 面积 =={max(1, (S.bottom - S.top + 1) * (S.right - S.left + 1))}==（没有 1 就按 1）',
        24: '划分 ①：横切两刀，上 / 中 / 下三条',
        27: '划分 ②：先横切，上面一整条；下面再竖切成左 / 右两块',
        28: '划分 ③：下面一整条；上面再竖切成左 / 右两块',
        33: '划分 ④：竖切两刀，左 / 中 / 右三条',
        36: '划分 ⑤：左边一整条；右边再横切成上 / 下两块',
        37: '划分 ⑥：右边一整条；左边再横切成上 / 下两块',
        39: '六种划分都试过了，最小总面积 = =={res}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='三块不重叠 = 切两刀，六种切法逐一试，每块取外接矩形',
        complexity='时间 `O((mn)^2)`，空间 `O(1)`',
        problem=['二进制网格里选 ==3 个互不重叠==的矩形，盖住所有 1，求面积和最小',
                 '示例：`[[1,0,1],[1,1,1]]` → `5`（2 + 2 + 1）'],
        quote='划分成三个部分可以认为是先在水平或者竖直方向上进行以此划分，然后对于划分出来的两个部分，再选取其中一个进行水平或者竖直方向上的划分。',
        quote_src='—— yiduobo 题解原文',
        idea=['先切一刀成两块，再切其中一块：全横、全竖各有一种重复，共 ==六种==',
              '每一块各派一个矩形，最小的就是块内所有 1 的外接矩形（3195 题）',
              '枚举切线位置，三块面积相加取最小'],
        summary=['时间 `O((mn)^2)`，本题 `m, n ≤ 30` 够用',
                 '易错：块里没有 1 时面积按 `max(1, …)` 算 1（矩形面积不能为 0）',
                 '易错：横切的切线 `i < m−1`、竖切 `j < n−1`，保证每块非空',
                 '对比灵神：灵神预处理四个角的 DP，把每块的外接矩形面积降到 `O(1)`'],
    ),
)
