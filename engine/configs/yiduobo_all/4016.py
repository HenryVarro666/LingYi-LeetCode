MAT = [[1, 1, 0], [1, 1, 1]]


def _info(S):
    if 'top' in S and S.get('_line', 0) >= 33 and S.get('v') is not None and 'bottom' in S:
        return f"到边长 `{S['v']}` 为止最靠边的位置：上 `{S['top']}`、下 `{S['bottom']}`、左 `{S['left']}`、右 `{S['right']}`"
    return ''


def _cell(S, i, j, v):
    if 'f' not in S:
        return None
    if i == S.get('i') and j == S.get('j'):
        return 'blue'
    return None


CONFIG = dict(
    num=4016, title='两个不重叠子正方形的最大面积', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='每种边长只记最上/下/左/右的正方形',
    tags=['灵神题单·单调栈', '灵神题单·动态规划', '难度分 1959'],
    code='''
class Solution(object):
    def maxArea(self, mat):
        
        m = len(mat)
        n = len(mat[0])

        ma = min(m, n)
        g = [[None] * 4 for _ in range(ma + 1)]

        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1:
                    if i == 0 or j == 0:
                        f[i][j] = 1
                    else:
                        f[i][j] = min(f[i - 1][j - 1], f[i][j - 1], f[i - 1][j]) + 1

                    v = f[i][j]
                    top, bottom, left, right = g[v]
                    if top is None or top > i:
                        top = i
                    if bottom is None or bottom < i:
                        bottom = i
                    if left is None or left > j:
                        left = j
                    if right is None or right < j:
                        right = j
                    g[v] = [top, bottom, left, right]
    
        top, bottom, left, right = None, None, None, None
        for v in range(ma, 0, -1):
            if g[v][0] is None:
                continue
            if top is None or top > g[v][0]:
                top = g[v][0]
            if bottom is None or bottom < g[v][1]:
                bottom = g[v][1]
            if left is None or left > g[v][2]:
                left = g[v][2]
            if right is None or right < g[v][3]:
                right = g[v][3]
            
            if top + v <= bottom or left + v <= right:
                return v * v
        
        return 0
''',
    call=f'Solution().maxArea({MAT})',
    expect=1,
    skip=['m = len', 'n = len', 'for i in range(m)', 'for j in range(n)', 'ma = min', 'if i == 0 or j == 0',
          'if top is None or top > i', 'if bottom is None or bottom < i', 'if left is None or left > j',
          'if right is None or right < j', 'top = i', 'bottom = i', 'left = j', 'right = j',
          'top, bottom, left, right = g[v]',
          'if top is None or top > g[v][0]', 'if bottom is None or bottom < g[v][1]',
          'if left is None or left > g[v][2]', 'if right is None or right < g[v][3]',
          'top = g[v][0]', 'bottom = g[v][1]', 'left = g[v][2]', 'right = g[v][3]',
          'top, bottom, left, right = None'],
    views=[
        dict(type='grid', var='mat', h=170, cell=64, label='mat（蓝 = 当前格）', cursors=[('i', 'j', 'blue', '')]),
        dict(type='grid', var='f', h=170, cell=64, label='f[i][j]：以 (i,j) 为右下角的最大全 1 正方形边长', cursors=[('i', 'j', 'yellow', '')]),
        dict(type='table', var='g', h=200, cell=70, label='g[v] = [最上行, 最下行, 最左列, 最右列]（边长 v 的右下角范围）',
             rows=lambda S: [f'v={k}' for k in range(len(S['g']))], cols=['上', '下', '左', '右']),
        dict(type='text', fn=_info, size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('v', 'v', 'yellow')],
    captions={
        'g = [[None]': '`g[v]` 记录边长为 `v` 的正方形，==右下角==出现过的最上、最下、最左、最右位置',
        'f = [[0] * n': '`f[i][j]`：以 `(i,j)` 为右下角的最大全 1 正方形边长',
        'if mat[i][j] == 1': '`mat[{i}][{j}] = {mat[i][j]}`',
        'f[i][j] = 1': '第一行/第一列：只能是边长 1',
        'f[i][j] = min': '`f[{i}][{j}] = min(左上, 左, 上) + 1` = =={f[i][j]}==：三个方向都撑得住才能扩大',
        'v = f[i][j]': '`(i,j)` 同时也是边长 `1..{f[i][j]}` 的右下角；只用最大边长 `v = {v}` 更新 `g[v]`，小的以后倒序合并',
        'g[v] = [': '更新 `g[{v}]` = =={g[v]}==（上 {g[v][0]}，下 {g[v][1]}，左 {g[v][2]}，右 {g[v][3]}）',
        'for v in range(ma, 0, -1)': '倒序枚举边长 `v = {v}`：先把更大边长的范围并进来，因为大的一定包含小的',
        'if g[v][0] is None': lambda S, B, r: (f'边长 `{S.v}` 没有出现过 → 跳过' if S.g[S.v][0] is None else f'边长 `{S.v}` 出现过，合并 `g[{S.v}]` 到 上/下/左/右'),
        'continue': '边长 `{v}` 的正方形不存在，换更小的',
        'if top + v <= bottom': lambda S, B, r: (
            f"合并后 上 `{S.top}`、下 `{S.bottom}`、左 `{S.left}`、右 `{S.right}`：`{S.top} + {S.v} <= {S.bottom}` → ==上下分得开== 成立" if S.top + S.v <= S.bottom else
            f"左 `{S.left}`、右 `{S.right}`：`{S.left} + {S.v} <= {S.right}` → ==左右分得开== 成立" if S.left + S.v <= S.right else
            f"`{S.top}+{S.v} <= {S.bottom}` 和 `{S.left}+{S.v} <= {S.right}` 都不成立 → 最上最下（最左最右）的两个边长 {S.v} 正方形会重叠，换更小的边长"),
        'return v * v': '找到：边长 `{v}` 的两个正方形不重叠 → 面积 =={ret}==',
        'return 0': '一个合法的都没有，返回 0',
    },
    cards=dict(
        one_liner='有解就必有分割线：最靠一边的两个正方形一定可行',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m×n` 的 0/1 矩阵，选两个==边长相同、不共享格子==的全 1 正方形',
                 '求能得到的最大单个正方形面积，选不出则返回 `0`',
                 '本视频：`[[1,1,0],[1,1,1]]` → `1`'],
        quote='若存在边长为k的正方形子矩阵对，那么至少在水平或者竖直方向上存在一条分割线，使得这两个正方形子矩阵分别处于这条分割线的两侧。',
        quote_src='—— yiduobo 题解原文',
        idea=['有分割线 → 最靠这一侧最外的两个边长 `k` 的正方形也在线两侧，也合法',
              '所以每种边长只需记最上、最下、最左、最右的右下角（`g[v]`），用 `f[i][j]` 的 DP 填',
              '从大到小枚举边长，累积合并 `g`；上下或左右分得开，当前 `v²` 就是答案'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '`f[i][j]` 只更新最大边长 `g[f[i][j]]`，较小边长靠“倒序合并”补上',
                 '判断 `top + v <= bottom`：两个右下角相距至少 `v` 才不重叠',
                 '原文本身已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神枚举分割线 + 前后缀最大正方形；这里每种边长只看最边缘的两个'],
    ),
)
