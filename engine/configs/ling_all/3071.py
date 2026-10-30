def _inY(i, j, n):
    m = n // 2
    return (i < m and (j == i or j == n - 1 - i)) or (i >= m and j == m)


CONFIG = dict(
    num=3071, title='在矩阵上写出字母 Y 所需的最少操作次数', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='分别统计 Y 内外的值 + 枚举两种颜色', tags=[],
    code='''
class Solution:
    def minimumOperationsToWriteY(self, grid: List[List[int]]) -> int:
        cnt1 = [0] * 3
        cnt2 = [0] * 3
        n = len(grid)
        m = n // 2

        for i, row in enumerate(grid[:m]):
            cnt1[row[i]] += 1
            cnt1[row[-1 - i]] += 1
            for j, x in enumerate(row):
                if j != i and j != n - 1 - i:
                    cnt2[x] += 1
        for row in grid[m:]:
            cnt1[row[m]] += 1
            for j, x in enumerate(row):
                if j != m:
                    cnt2[x] += 1

        max_not_change = 0
        for i, c1 in enumerate(cnt1):
            for j, c2 in enumerate(cnt2):
                if i != j:
                    max_not_change = max(max_not_change, c1 + c2)
        return n * n - max_not_change
''',
    call='Solution().minimumOperationsToWriteY([[1,2,2],[1,1,0],[0,1,0]])',
    expect=3,
    views=[
        dict(type='grid', var='grid', h=330, cell=70, label='grid（蓝 = 属于 Y）',
             color=lambda S, i, j, v: 'blue' if _inY(i, j, len(S['grid'])) else None),
        dict(type='array', var='cnt1', h=150, label='cnt1：Y 内各值个数（下标 = 值）', cell=70,
             pointers={}),
        dict(type='array', var='cnt2', h=150, label='cnt2：Y 外各值个数', cell=70),
    ],
    watch=['n', 'm', 'i', 'j', 'x', ('max_not_change', 'max_not_change', 'green')],
    captions={
        'cnt1 = [0]': '`cnt1[v]`：Y 里值为 `v` 的格子数',
        'cnt2 = [0]': '`cnt2[v]`：Y 外值为 `v` 的格子数',
        'n = len': '`n = {n}`',
        'm = n // 2': '`m = {m}` 是中心所在行列：上半部分是第 `0 ~ m-1` 行，下半部分是第 `m ~ n-1` 行',
        'for i, row in enumerate(grid[:m])': '上半部分第 `{i}` 行：Y 的两条对角线在第 `{i}` 列和第 `{n-1-i}` 列',
        'cnt1[row[i]]': '左对角线格子 `({i}, {i})` 值为 `{row[i]}` → `cnt1[{row[i]}]` 加一',
        'cnt1[row[-1 - i]]': '右对角线格子 `({i}, {n-1-i})` 值为 `{row[-1-i]}` → `cnt1[{row[-1-i]}]` 加一',
        'for j, x in enumerate(row):': '逐格看这一行：`j = {j}`，`x = {x}`',
        'if j != i and j != n - 1 - i': '`j = {j}` 不是两条对角线所在列吗？{"==是，在 Y 外=="  if (j != i and j != n - 1 - i) else "否，已在 Y 里统计过"}',
        'if j != m': '`j = {j}` 不是中间竖线所在列吗？{"==是，在 Y 外==" if j != m else "否，这格在竖线上，已统计"}',
        'for row in grid[m:]': '下半部分（含中心行）：Y 只剩中间竖线 —— 第 `{m}` 列',
        'cnt1[row[m]]': '竖线格子值为 `{row[m]}` → `cnt1[{row[m]}]` 加一',
        'cnt2[x] += 1': '`x = {x}` 在 Y 外 → `cnt2[{x}]` 加一：`cnt2 = {cnt2}`',
        'max_not_change = 0': '接下来枚举：Y 改成 `i`、其余改成 `j`，==最多能保留多少格不变==',
        'for i, c1': '尝试把 Y 变成 `i = {i}`：Y 里已有 `c1 = {c1}` 个不用改',
        'for j, c2': '其余格子变成 `j = {j}`：Y 外已有 `c2 = {c2}` 个不用改',
        'if i != j': '`i = {i}`、`j = {j}`：{"==两种值不同，可行==" if i != j else "相同不满足“Y 内外不同”，跳过"}',
        'max_not_change = max': '保留的格子数 `c1 + c2 = {c1} + {c2} = {c1+c2}` → `max_not_change = {max_not_change}`',
        'return n * n': '总格子 `{n*n}` − 最多保留 `{max_not_change}` = ==`{ret}`== 次修改',
    },
    cards=dict(
        one_liner='最少修改 = 总格数 − 最多能保留不变的格数',
        complexity='时间 `O(n^2 + k^2)`，空间 `O(k)`，`k = 3`',
        problem=['`n x n` 矩阵（`n` 为奇数），值为 0/1/2；Y 由两条对角线和中间竖线组成',
                 '要求 Y 内值全相同、Y 外值全相同，且两者不同；每次操作改一格',
                 '示例：`[[1,2,2],[1,1,0],[0,1,0]]` → `3`'],
        quote='统计 Y 中的元素出现次数，记到一个长为 3 的数组 cnt1 中。统计不在 Y 中的元素出现次数，记到一个长为 3 的数组 cnt2 中。计算最多可以保留多少个元素不变。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cnt1`、`cnt2` 分别记录 Y 内、Y 外每种值的个数',
              '枚举 Y 变成 `i`、外面变成 `j`（`i != j`），保留数 = `cnt1[i] + cnt2[j]`',
              '答案 = `n * n` − 最大保留数'],
        summary=['时间 `O(n^2 + k^2)`，空间 `O(k)`',
                 '易错：中心格只算在 Y 里，别在 `cnt2` 里重复统计',
                 '易错：`i != j`，Y 内外的值必须不同',
                 '思考题：值域更大时，取 `cnt1`、`cnt2` 的最大值（冲突时用次大值）即可'],
    ),
)
