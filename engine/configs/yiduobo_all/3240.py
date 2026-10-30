G = [[1, 0, 0, 0, 1], [0, 1, 1, 1, 0], [1, 0, 0, 1, 0]]


def _cells(S):
    if 'm' not in S or 'n' not in S:
        return [], None
    m, n, L = S['m'], S['n'], S['_line']
    if 'i' in S and 'j' in S and L <= 21:
        i, j = S['i'], S['j']
        return [(i, j), (i, n - 1 - j), (m - 1 - i, j), (m - 1 - i, n - 1 - j)], 'blue'
    if 22 <= L <= 23:
        return [(m // 2, n // 2)], 'pink'
    if 'left' in S and 29 <= L <= 38:
        return [(m // 2, S['left']), (m // 2, S['right'])], 'orange'
    if 'top' in S and L >= 43:
        return [(S['top'], n // 2), (S['bottom'], n // 2)], 'orange'
    return [], None


def _gc(S, i, j, v):
    cells, c = _cells(S)
    return c if (i, j) in cells else None


def _txt(S):
    if 'm' not in S:
        return '行列都回文：四个镜像格必须相同；中心格、中心行/列另算'
    cells, c = _cells(S)
    vals = [S['grid'][i][j] for i, j in cells]
    if c == 'blue':
        return f"四个镜像格 `{vals}`：`one = {sum(vals)}`，全变 0 要 {sum(vals)} 次，全变 1 要 {4 - sum(vals)} 次"
    if c == 'pink':
        return f"正中央格 `{vals[0]}`：必须是 0"
    if c == 'orange':
        return f"中心{'行' if 'left' in S and S['_line'] < 43 else '列'}的一对 `{vals}`：{'相同' if vals[0] == vals[1] else '不同，必须翻一个'}"
    return f"`res = {S.get('res', 0)}`，`one = {S.get('one', '-')}`，`changed = {S.get('changed', '-')}`"


CONFIG = dict(
    num=3240, title='最少翻转次数使二进制矩阵回文 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='三类格子 · 用 changed 判断要不要额外 +2',
    tags=['灵神题单', '思维题', '难度分 2080'],
    code='''
class Solution(object):
    def minFlips(self, grid):

        m = len(grid)
        n = len(grid[0])

        res = 0
        for i in range(m // 2):
            for j in range(n // 2):
                one = 0
                if grid[i][j] == 1:
                    one += 1
                if grid[i][n - 1 - j] == 1:
                    one += 1
                if grid[m - 1 - i][j] == 1:
                    one += 1
                if grid[m - 1 - i][n - 1 - j] == 1:
                    one += 1
                
                res += min(one, 4 - one)
        
        if m % 2 == 1 and n % 2 == 1 and grid[m // 2][n // 2] == 1:
            res += 1
        
        changed = False
        one = 0
        if m % 2 == 1:
            x = m // 2
            left, right = 0, n - 1
            while left < right:
                if grid[x][left] != grid[x][right]:
                    changed = True
                    res += 1
                elif grid[x][left] == 1:
                    one += 2
                
                left += 1
                right -= 1
        
        if n % 2 == 1:
            y = n // 2
            top, bottom = 0, m - 1
            while top < bottom:
                if grid[top][y] != grid[bottom][y]:
                    changed = True
                    res += 1
                elif grid[top][y] == 1:
                    one += 2
                
                top += 1
                bottom -= 1
        
        if one % 4 == 2 and not changed:
            res += 2
        
        return res
''',
    call=f'Solution().minFlips({G})',
    expect=5,
    skip=['m = len', 'n = len', 'left += 1', 'right -= 1', 'top += 1', 'bottom -= 1',
          'one += 1', 'x = m // 2', 'y = n // 2'],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='grid', var='grid', label='grid（蓝 = 四个镜像格，粉 = 正中央，橙 = 中心行/列上的一对）', cell=110, color=_gc, h=420),
    ],
    watch=[('res', 'res', 'green'), ('one', 'one', 'blue'), ('changed', 'changed', 'pink')],
    captions={
        'res = 0': '`res` 累计翻转次数。先处理==不在中心行/中心列==的格子',
        'for i in range(m // 2)': '枚举左上部分的行 `i`（`0 .. m // 2 - 1`）',
        'for j in range(n // 2)': '枚举左上部分的列 `j`；它的三个镜像 `(i, n-1-j)`、`(m-1-i, j)`、`(m-1-i, n-1-j)` 必须相同',
        10: '数这四个镜像格里 1 的个数 `one`',
        26: '`one` 重新清零：从现在起只统计中心行/列上==对称的 1 的个数==',
        'if grid[i][j] == 1': '`grid[{i}][{j}] = {grid[i][j]}`：{"是 1，one 加 1" if grid[i][j] == 1 else "是 0"}',
        'if grid[i][n - 1 - j]': '`grid[{i}][{n - 1 - j}] = {grid[i][n - 1 - j]}`：{"是 1，one 加 1" if grid[i][n - 1 - j] == 1 else "是 0"}',
        'if grid[m - 1 - i][j]': '`grid[{m - 1 - i}][{j}] = {grid[m - 1 - i][j]}`：{"是 1，one 加 1" if grid[m - 1 - i][j] == 1 else "是 0"}',
        'if grid[m - 1 - i][n - 1 - j]': '`grid[{m - 1 - i}][{n - 1 - j}] = {grid[m - 1 - i][n - 1 - j]}`：{"是 1，one 加 1" if grid[m - 1 - i][n - 1 - j] == 1 else "是 0"}',
        'res += min(one, 4 - one)': '四格里有 `{one}` 个 1：全变 0 要 `one` 次，全变 1 要 `4 - one` 次，取小 → `res = {res}`',
        'if m % 2 == 1 and n % 2 == 1': lambda S, B, r: ('`m`、`n` 都是奇数且中心格 `grid[{0}][{1}]` 是 1：==中心必须变 0==，否则 1 的个数是奇数'.format(B.m // 2, B.n // 2) if (B.m % 2 == 1 and B.n % 2 == 1 and B.grid[B.m // 2][B.n // 2] == 1) else '中心格不用翻（不存在或本来就是 0）'),
        23: '中心格翻成 0：`res = {res}`',
        'changed = False': '`changed` 记录中心行/列上有没有「必须翻」的操作',
        'if m % 2 == 1:': '`m` 是奇数 → 有中心行，从两端往中间检查，是否回文',
        'left, right = 0, n - 1': '中心行 `x = {x}`，双指针 `left = 0`、`right = {right}`',
        'while left < right': '`left = {left}` < `right = {right}`？{"是，继续检查这一对" if B.left < B.right else "否，这一排检查完了"}',
        'if grid[x][left] != grid[x][right]': lambda S, B, r: (f'`grid[{B.x}][{B.left}] = {B.grid[B.x][B.left]}` 与 `grid[{B.x}][{B.right}] = {B.grid[B.x][B.right]}`：'
                                                              + ('==不同，必须翻一个==' if B.grid[B.x][B.left] != B.grid[B.x][B.right] else '相同')),
        'changed = True': '这里有一次必须的操作：`changed = True`（后面可以拿它凑 4 的倍数）',
        'elif grid[x][left] == 1': '这一对相同：是 1 吗？{"是，对称的 1 多 2 个" if B.grid[B.x][B.left] == 1 else "不是，没有 1"}',
        'one += 2': '`one = {one}`：中心行/列上原本对称的 1 的个数',
        'if n % 2 == 1:': '`n` 是奇数 → 有中心列，同样从两端往中间检查',
        'top, bottom = 0, m - 1': '中心列 `y = {y}`，双指针 `top = 0`、`bottom = {bottom}`',
        'while top < bottom': '`top = {top}` < `bottom = {bottom}`？{"是，继续检查这一对" if B.top < B.bottom else "否，这一列检查完了"}',
        'if grid[top][y] != grid[bottom][y]': lambda S, B, r: (f'`grid[{B.top}][{B.y}] = {B.grid[B.top][B.y]}` 与 `grid[{B.bottom}][{B.y}] = {B.grid[B.bottom][B.y]}`：'
                                                              + ('==不同，必须翻一个==' if B.grid[B.top][B.y] != B.grid[B.bottom][B.y] else '相同')),
        'elif grid[top][y] == 1': '这一对相同：是 1 吗？{"是，对称的 1 多 2 个" if B.grid[B.top][B.y] == 1 else "不是，没有 1"}',
        'if one % 4 == 2 and not changed': lambda S, B, r: (f'`one = {B.one}`，`one % 4 = {B.one % 4}`，`changed = {B.changed}`：'
                                                            + ('==one 不是 4 的倍数，且没有可以改目标的操作 → 额外 +2（把两个对称的 1 变 0）==' if (B.one % 4 == 2 and not B.changed)
                                                               else 'one 已是 4 的倍数，或有操作可以顺带调整 → 不用额外操作')),
        'res += 2': '额外加 2：`res = {res}`',
        'return res': '最少翻转次数 `{res}`',
    },
    cards=dict(
        one_liner='格子分三类：四格一组、正中心、中心行列；最后看 1 的个数要不要多花 2 步',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m × n` 的 0/1 矩阵，可翻转任意格子',
                 '要求所有行和列都回文，并且矩阵里 1 的数量是 4 的倍数，求最少翻转次数',
                 '本视频：3×5 矩阵 → `5`'],
        quote='如果中心行或者中心列上执行过至少一次操作，那么就可以将某一次操作的目标变为两个1，这样一来就可以使得1的数量是4的倍数，同时依然可以达到操作次数的下限。',
        quote_src='—— yiduobo 题解原文',
        idea=['不在中心行列的格子：四个一组，`one` 个 1 → `min(one, 4 - one)`，自带 4 的倍数',
              '中心格：只有 m、n 都是奇数才有，必须是 0',
              '中心行/列：对称的 1 数成 `one`；有过操作（`changed`）就能顺带调整，否则 `one % 4 == 2` 时额外 +2'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：中心格为 1 要翻成 0（只在 m、n 都是奇数时）',
                 '`one` 统计的是==对称的 1 的个数==，每对加 2；变量 `one` 在中心行列统计前被重新置 0',
                 '`changed` 只在中心行/列遇到不对称的一对时才为真',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行；对比灵神：灵神用 `diff` 和 `cnt1 % 4` 一次性算出额外代价'],
    ),
)
