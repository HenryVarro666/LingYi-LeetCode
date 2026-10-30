GRID = [[4, 3, 8, 4, 1], [9, 5, 1, 9, 5], [2, 7, 6, 5, 7], [3, 5, 1, 2, 6]]


def _win(S):
    """(top, left) of the 3x3 window being examined, else None"""
    if 'i' in S and 'j' in S and 'ans' in S:
        return S['i'], S['j']
    return None


def _color(S, a, b, v):
    w = _win(S)
    if w is None:
        return None
    i, j = w
    if i <= a < i + 3 and j <= b < j + 3:
        if (a, b) == (i + 1, j + 1):
            return 'yellow'
        if 'r' in S and 'c' in S and (a, b) == (i + S['r'], j + S['c']):
            return 'orange'
        return 'blue'
    return None


def _cur(S):
    w = _win(S)
    return (w[0] + 1, w[1] + 1) if w else None


def _mask(S):
    if 'mask' not in S or 'r_sum' not in S:
        return ''
    m = S['mask']
    have = ''.join(str(k) for k in range(1, 10) if m >> k & 1) or '（空）'
    return f"已出现的数字：`{have}`　　`r_sum = {S['r_sum']}`　`c_sum = {S['c_sum']}`"


CONFIG = dict(
    num=840, title='矩阵中的幻方', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='枚举 + 中心必为 5 + 位掩码',
    code='''
class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0

        for i in range(m - 2):
            for j in range(n - 2):
                if grid[i + 1][j + 1] != 5:
                    continue

                mask = 0
                r_sum = [0] * 3
                c_sum = [0] * 3
                for r in range(3):
                    for c in range(3):
                        x = grid[i + r][j + c]
                        mask |= 1 << x
                        r_sum[r] += x
                        c_sum[c] += x

                if mask == 1022 and r_sum[0] == r_sum[1] == c_sum[0] == c_sum[1] == 15:
                    ans += 1

        return ans
''',
    call=f'Solution().numMagicSquaresInside({GRID})',
    expect=1,
    skip=['r_sum[r] += x', 'c_sum[c] += x', 'for c in range(3)', 'x = grid[i + r][j + c]'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝框 = 当前 3×3 子矩阵，黄 = 正中心，橙 = 正在统计的格子）', cell=100, h=380,
             color=_color, cursors=[(lambda S: (_cur(S) or (-1, -1))[0], lambda S: (_cur(S) or (-1, -1))[1], 'yellow')]),
        dict(type='text', fn=_mask, size=24, h=60),
    ],
    watch=['i', 'j', ('mask', 'bin(mask)', 'cyan'), ('r_sum', 'r_sum', 'blue'), ('c_sum', 'c_sum', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'm, n = len': '`m = {m}`，`n = {n}`：只需枚举 3×3 子矩阵的左上角 `(i, j)`',
        'ans = 0': '`ans` 统计幻方个数',
        'for i in range': lambda S, B, r: ('所有窗口都看完了' if B.get('i') == S.i else f'左上角行 `i = {S.i}`（最多到 `m - 3`）'),
        'for j in range': lambda S, B, r: ('这一行的窗口都看完了' if B.get('j') == S.j and B.get('i') == S.i else f'左上角 `({S.i}, {S.j})`：看以 `({S.i + 1}, {S.j + 1})` 为正中心的 3×3'),
        'if grid[i + 1][j + 1] != 5': lambda S, B, r: (f'正中心 `{S.grid[S.i + 1][S.j + 1]}` ≠ 5 → ==不可能是幻方==，跳过' if S.grid[S.i + 1][S.j + 1] != 5
                                                      else '正中心 `5`，==有可能是幻方==，继续检查（幻方正中心一定是 5）'),
        'continue': '中心不是 5，直接看下一个窗口',
        'mask = 0': '`mask` 的第 `x` 位表示数字 `x` 出现过',
        'r_sum = [0]': '`r_sum` 记每行之和',
        'c_sum = [0]': '`c_sum` 记每列之和',
        'for r in range': lambda S, B, r: ('3 行都统计完了' if B.get('r') == S.r and 'mask' in B and B.get('i') == S.i and B.get('j') == S.j else f'统计第 `{S.r}` 行'),
        'mask |= 1 << x': '数字 `{x}` 出现：`mask |= 1 << {x}` → `mask = {mask}`',
        'if mask == 1022': lambda S, B, r: (f'`mask = {S.mask}`' + (' == 1022：==恰好包含 1~9==' if S.mask == 1022 else f' ≠ 1022：数字不是 1~9 各一个')
                                           + f'；`r_sum = {S.r_sum}`，`c_sum = {S.c_sum}`'
                                           + ('，前两行前两列都是 15 → ==是幻方==' if S.mask == 1022 and S.r_sum[0] == S.r_sum[1] == S.c_sum[0] == S.c_sum[1] == 15 else ' → 不是幻方')),
        'ans += 1': '又找到一个幻方：`ans = {ans}`',
        'return ans': '共 `{ret}` 个幻方',
    },
    cards=dict(
        one_liner='幻方正中心必为 5；再用位掩码查 1~9，只验前两行前两列',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`3×3` 幻方：填入 `1~9` 各一次，每行、每列、两条对角线之和都相等',
                 '数一数 `grid` 里有多少个 `3×3` 子矩阵是幻方',
                 '示例：`[[4,3,8,4],[9,5,1,9],[2,7,6,2]]` → `1`；本视频用 4×5 的例子，答案同为 `1`'],
        quote='3×3 的幻方必须包含 1 到 9 所有数字，这意味着幻方元素和为 45。由于每行的和都要相等，所以每行的和为 15。',
        quote_src='—— 灵茶山艾府题解',
        idea=['过正中心的 4 条线之和为 `15×4 = 60`，中心被多算 3 次：`45 + 3x = 60`，所以 ==中心一定是 5==',
              '包含 1~9 且前两行之和为 15，第三行自动是 15；列同理',
              '再加上中心为 5，可证明两条对角线也自动是 15 → 不必单独验证'],
        summary=['时间 `O(mn)`，空间 `O(1)`：窗口固定 3×3',
                 '`mask == 1022` 即 `2^10 - 2`，表示恰好含 1~9 各一次',
                 '易错：`grid` 里的数最大到 15，不能只看和是否为 15，要查是否是 1~9 的排列',
                 '只验前两行前两列，靠“中心为 5 + 1~9 排列”推出其余'],
    ),
)
