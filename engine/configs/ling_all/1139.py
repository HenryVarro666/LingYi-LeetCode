GRID = [[1, 1, 1, 0], [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1]]
_CODE = '''
class Solution:
    def largest1BorderedSquare(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        rs = [list(accumulate(row, initial=0)) for row in grid]  # 每行的前缀和
        cs = [list(accumulate(col, initial=0)) for col in zip(*grid)]  # 每列的前缀和
        for d in range(min(m, n), 0, -1):  # 从大到小枚举正方形边长 d
            for i in range(m - d + 1):
                for j in range(n - d + 1):  # 枚举正方形左上角坐标 (i,j)
                    # 上 左 下 右 四条边 1 的个数均为 d
                    if rs[i][j + d] - rs[i][j] == d and \\
                       cs[j][i + d] - cs[j][i] == d and \\
                       rs[i + d - 1][j + d] - rs[i + d - 1][j] == d and \\
                       cs[j + d - 1][i + d] - cs[j + d - 1][i] == d:
                        return d * d
        return 0
'''
_L = _CODE.strip('\n').splitlines()
L_J = next(k for k, s in enumerate(_L, 1) if 'for j in' in s)
L_RET = next(k for k, s in enumerate(_L, 1) if 'return d * d' in s)


def _sq(S):
    if 'i' not in S or 'j' not in S or 'd' not in S or not (L_J <= S['_line'] <= L_RET):
        return None
    return S['i'], S['j'], S['d']


def _color(S, i, j, v):
    q = _sq(S)
    if not q:
        return None
    a, b, d = q
    if a <= i < a + d and b <= j < b + d and (i in (a, a + d - 1) or j in (b, b + d - 1)):
        if S['_line'] == L_RET:
            return 'green'
        return 'pink' if v == 0 else 'blue'
    return None


def _cnt(S):
    i, j, d = S['i'], S['j'], S['d']
    rs, cs = S['rs'], S['cs']
    return (rs[i][j + d] - rs[i][j], cs[j][i + d] - cs[j][i],
            rs[i + d - 1][j + d] - rs[i + d - 1][j], cs[j + d - 1][i + d] - cs[j + d - 1][i])


def _chk(S, B, r):
    up, lf, dn, rt = _cnt(S)
    d = S.d
    t = f'`({S.i},{S.j})` 边长 `{d}`：上 `{up}`、左 `{lf}`、下 `{dn}`、右 `{rt}`'
    if up == lf == dn == rt == d:
        return t + '，四条边的 1 都是 `d` 个 → ==边框全是 1=='
    bad = [n for n, v in zip('上左下右', (up, lf, dn, rt)) if v != d]
    return t + f'，{"、".join(bad)}边不足 `{d}` 个，有 0 → 这个位置不行'


def _fn(S, B):
    q = _sq(S)
    if not q or S['_line'] == L_RET:
        return ''
    i, j, d = q
    rs, cs = S['rs'], S['cs']
    up = rs[i][j + d] - rs[i][j]
    lf = cs[j][i + d] - cs[j][i]
    dn = rs[i + d - 1][j + d] - rs[i + d - 1][j]
    rt = cs[j + d - 1][i + d] - cs[j + d - 1][i]
    return f'边长 `d={d}`，左上角 `({i},{j})`：上 `{up}`　左 `{lf}`　下 `{dn}`　右 `{rt}`　（都要等于 =={d}==）'


CONFIG = dict(
    num=1139, title='最大的以 1 为边界的正方形', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='行列前缀和 · 边长从大到小枚举',
    tags=[],
    code=_CODE,
    call=f'Solution().largest1BorderedSquare({GRID})',
    expect=4,
    skip=[7, 8, 11, 12, 13],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 正在检查的正方形的边框，粉 = 边上有 0，绿 = 找到）', cell=88, h=380,
             color=_color, cursors=[('i', 'j', 'yellow', '左上角')] if False else []),
        dict(type='text', fn=_fn, size=28, h=80),
        dict(type='table', var='rs', label='rs（每行的前缀和，首位补 0）', cell=56, h=190),
    ],
    watch=['m', 'n', ('d', 'd', 'blue'), ('i', 'i', 'pink'), ('j', 'j', 'pink')],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'rs = [': '`rs[i][k]` = 第 `i` 行前 `k` 个数的和：一段横线上有几个 1，两项相减就知道',
        'cs = [': '`cs[j][k]` = 第 `j` 列前 `k` 个数的和：一段竖线上有几个 1 同理。`rs = {rs}`',
        'for d in range': lambda S, B, r: ('==从大到小==枚举边长，先试最大的 `d = %d`：第一个合法的就是最大的，直接返回' % S.d if 'i' not in B
                                         else f'边长 `{B.d}` 没有合法的正方形 → 缩小到 `d = {S.d}` 再试'),
        'if rs[i][j + d]': _chk,
        'return d * d': '边长 `{d}` 的正方形边框全是 1 → 面积 `{d} × {d}` = =={ret}==',
        'return 0': '所有边长都试过了，没有 → `0`',
    },
    cards=dict(
        one_liner='行列各做一遍前缀和，四条边各 O(1) 查，边长从大到小试',
        complexity='时间 `O(mn·min(m,n))`，空间 `O(mn)`',
        problem=['`0/1` 网格，找==边框全是 1== 的最大正方形，返回它的面积（元素个数）',
                 '正方形里面可以是 0，只看四条边',
                 '示例：`[[1,1,1],[1,0,1],[1,1,1]]` → `9`',
                 '本视频：4×4 的网格（最大的只有边长 2）→ `4`'],
        quote='对于数组 nums，定义它的前缀和 s[0]=0，s[i+1] = sum(nums[0..i])……通过前缀和，我们可以把==子数组的元素和转换成两个前缀和的差==。',
        quote_src='—— 灵茶山艾府题解（前置知识：前缀和）',
        idea=['每行、每列各算一遍前缀和：任意一段横线/竖线上 1 的个数 = 两个前缀和之差',
              '枚举边长 `d` 和左上角 `(i,j)`，上、左、下、右四条边的 1 都等于 `d` 才合法',
              '边长从大到小枚举：==第一个合法的就是最大的==，立刻返回 `d*d`'],
        summary=['时间 `O(mn·min(m,n))`：边长 × 左上角位置，每次检查 `O(1)`',
                 '易错：`accumulate(..., initial=0)` 让前缀和多一位，所以用 `rs[i][j+d] - rs[i][j]`，下标不要少加 `d`',
                 '易错：下边是第 `i+d-1` 行，右边是第 `j+d-1` 列，不是 `i+d`、`j+d`',
                 '`zip(*grid)` 把列转成行，这样列前缀和和行前缀和写法一致'],
    ),
)
