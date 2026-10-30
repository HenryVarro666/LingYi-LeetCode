def _dp(S):
    a = S.get('a')
    if not a or not isinstance(a, list):
        return None
    m, n = len(a), len(a[0])
    f = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if a[i][j] != '.':
                continue
            if i == 0 and j == 0:
                f[i][j] = 1
            else:
                f[i][j] = (f[i - 1][j] if i else 0) + (f[i][j - 1] if j else 0)
    return f


def _gc(S, i, j, v):
    return 'green' if v == '.' else None


def _txt(S):
    f = _dp(S)
    if f is None:
        return '构造 `m × n` 网格，使左上到右下恰好 `k` 条路径'
    return f"当前网格的路径数（右下角）= =={f[-1][-1]}==，目标 k = {S['k']}"


CONFIG = dict(
    num=3988, title='创建一个恰好有 K 条路径的网格图 I', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='构造 k×2 的空区域',
    tags=['灵神题单', '难度分 2055'],
    code='''
class Solution:
    def createGrid(self, m: int, n: int, k: int) -> list[str]:
        # 特判
        if k == 4 and m == 3 and n == 3:
            return ["..#", "...", "#.."]

        if m == 1 or n == 1:
            # 一行或一列，只能有一种方案
            if k > 1:
                return []
            return ['.' * n] * m

        # 至少要有 k 行或 k 列（特殊情况上面已判断）
        if m < k and n < k:
            return []

        # 初始全为 '#'（第一列全为 '.'）
        a = [['.'] + ['#'] * (n - 1) for _ in range(m)]
        a[-1] = '.' * n  # 最后一行全为 '.'
        if n >= k:  # 至少有 k 列
            # 倒数第二行开头 k 个 '.'
            for j in range(1, k):
                a[-2][j] = '.'
        else:  # 至少有 k 行
            # 第二列末尾 k 个 '.'
            for i in range(m - k, m - 1):
                a[i][1] = '.'
        return [''.join(row) for row in a]
''',
    call='Solution().createGrid(3, 4, 3)',
    expect=['.###', '...#', '....'],
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='grid', var='a', label='a（绿 = 空格 . ，灰 = 障碍 #）', cell=96, h=300, color=_gc,
             cursors=[('None', 'j', 'yellow')]),
        dict(type='table', var=_dp, label='每格的路径数（只走 . ，向右 / 向下）', cell=96, h=300),
    ],
    watch=['m', 'n', 'k'],
    captions={
        'if k == 4 and m == 3 and n == 3': '特判：`3×3` 且 `k = 4` 无法用通用构造，单独给一个解。这里 `k = {k}`，不触发',
        'if m == 1 or n == 1': '一行或一列只有一条路，`m = {m}, n = {n}` 都 ≥ 2 → 不是这种情况',
        'if m < k and n < k': '通用构造要有 ==至少 `k` 行或 `k` 列==；`m = {m}`、`n = {n}` 至少一个 ≥ `{k}` → 有解',
        "a = [['.']": '先全填 `#`，只留第一列为 `.`：每一行起点都能下来',
        "a[-1] = ": '最后一行全 `.`：路径最终都沿它走到右下角',
        'if n >= k': '`n = {n} ≥ k = {k}`：列数够，在倒数第二行开头 `k` 格打通',
        'for j in range(1, k)': '倒数第二行从第 1 列到第 `k-1` 列变成 `.`，凑出 `k×2` 的空区域',
        "a[-2][j] = '.'": '`a[-2][{j}]` 改成 `.`：右下 `2×k` 区域里，路径数 1、2、…、`k` 逐列递增',
        'else:': '列数不够就转置：在第二列末尾 `k` 行打通',
        "return [''.join": '每行拼成字符串返回；右下角路径数恰好 =={k}==',
    },
    cards=dict(
        one_liner='挖出一个 `k × 2` 的空区域，路径数恰好是 `k`',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
        problem=['给三个整数 `m`、`n`、`k`，构造 `m×n` 网格，只含 `.`（空）和 `#`（障碍）',
                 '只能向右、向下走，从 `(0,0)` 到 `(m-1,n-1)` 恰好 `k` 条路径',
                 '返回任意一个；不存在返回空数组。`k ≤ 4`',
                 '示例：`m=3, n=4, k=3` → `[".###","...#","...."]`'],
        quote='构造一个 k×2 或 2×k 的全为 . 的区域，这个区域从左上角移动到右下角，恰好有 k 条路径。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`2×k` 的全空区域，从左上走到右下恰好 `k` 条：在第一行走到第 `i` 列再下去',
              '其余格子全是障碍，路径只能走出这块区域和最后一行',
              '`3×3, k=4` 是唯一例外，特判；行列都 `< k` 无解'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：一行或一列只有一条路，`k > 1` 要返回空',
                 '`3×3, k=4` 必须特判，通用构造做不到',
                 '灵神还给了「倍增器」构造：`2×2` 空块串联，每块路径数 ×2，可处理大 `k`',
                 '同类题：贪心题单「构造题」'],
    ),
)
