def _tf(b):
    return 'T' if b else 'F'


def _cap_cell(S, B, ret):
    i, j, x, f = S.i, S.j, S.x, S.f
    pre = f'新的一行：考虑 `nums[{i}] = {x}`。' if j == 0 else ''
    if j < x:
        return pre + f'`j = {j} < {x}`：放不下，==只能不选== → 抄上一格 `f[{i}][{j}]` = {_tf(f[i][j])}'
    return (pre + f'选 `{x}`（还差 {j - x}）：`f[{i}][{j - x}]` = {_tf(f[i][j - x])}；不选：`f[{i}][{j}]` = {_tf(f[i][j])}'
            f' → `f[{i + 1}][{j}]` = =={_tf(f[i + 1][j])}==')


def _col(S, r, c, v):
    if 'j' in S and 'x' in S:
        i, j, x = S['i'], S['j'], S['x']
        if r == i + 1 and c == j:
            return 'yellow'
        if r == i and c == j:
            return 'blue'
        if r == i and j >= x and c == j - x:
            return 'purple'
    return 'green' if v else None


def _text(S):
    if 'j' not in S or 'x' not in S:
        return '`f[i+1][j]`：前 `i+1` 个数（`nums[0..i]`）能否选出和==恰好==为 `j`'
    i, j, x, f = S['i'], S['j'], S['x'], S['f']
    if j < x:
        return f'`f[{i + 1}][{j}]` = `f[{i}][{j}]` = {_tf(f[i][j])}（`j < x`，只能不选）'
    return f'`f[{i + 1}][{j}]` = 选 `f[{i}][{j - x}]`={_tf(f[i][j - x])} 或 不选 `f[{i}][{j}]`={_tf(f[i][j])} → =={_tf(f[i + 1][j])}=='


CONFIG = dict(
    num=416, title='分割等和子集', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='0-1 背包（二维递推）',
    code='''
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        s = sum(nums)
        if s % 2:
            return False
        s //= 2  # 注意这里把 s 减半了

        n = len(nums)
        f = [[False] * (s + 1) for _ in range(n + 1)]
        f[0][0] = True
        for i, x in enumerate(nums):
            for j in range(s + 1):
                f[i + 1][j] = j >= x and f[i][j - x] or f[i][j]
        return f[n][s]
''',
    call='Solution().canPartition([1, 2, 3, 4])',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='grid', var='f', label='f（第 i+1 行 = 加入 nums[i]，列 = 目标和 j；黄 = 当前，蓝 = 不选，紫 = 选）',
             rows=lambda S: ['—'] + [f'+{x}' for x in S['nums']], cols=lambda S: list(range(S['s'] + 1)),
             cell=86, h=540, color=_col),
    ],
    watch=[('i', 'i', 'yellow'), ('x', 'x', 'yellow'), ('j', 'j', 'yellow'), ('s', 's', 'green')],
    skip=['f = [[False]', 'for i, x in enumerate', 'for j in range'],
    captions={
        's = sum': '元素和 `s = {s}`',
        'if s % 2': lambda S, B, ret: (f'`s = {S.s}` 是奇数 → 不可能平分' if S.s % 2 else
                                       f'`s = {S.s}` 是偶数 → 每个子集的和都得是 `{S.s // 2}`'),
        's //= 2': '问题变成：能否选出一些数，和==恰好等于== `s = {s}`？→ 0-1 背包',
        'f[0][0] = True': '`f` 共 `n+1 = {n + 1}` 行、`s+1 = {s + 1}` 列；==最上边插入一排==表示边界：`f[0][0] = True`（一个不选，和为 0）',
        'f[i + 1][j] = ': _cap_cell,
        'return f[n][s]': '答案在右下角：`f[{n}][{s}]` = =={ret}==，比如选 `1 + 4 = 5`',
    },
    cards=dict(
        one_liner='能否选出和恰好为 s/2 的子集：恰好装满型 0-1 背包',
        complexity='时间 `O(n·s)`，空间 `O(n·s)`（`s` 为元素和的一半）',
        problem=['只含正整数的非空数组 `nums`，能否分成==元素和相等==的两个子集？',
                 '示例：`[1,5,11,5]` → `true`（`[1,5,5]` 和 `[11]`）',
                 '演示：`[1,2,3,4]` → `true`（`[1,4]` 和 `[2,3]`）'],
        before=[dict(heading='一、分析', lines=[
            '设元素和为 `s`，两个子集的和都得是 `s/2` → `s` ==必须是偶数==',
            '问题变成：能否选出一个子序列，元素和==恰好等于== `s/2`？',
            '这就是「恰好装满」型 ==0-1 背包==',
        ])],
        quote='定义 dfs(i,j) 表示能否从 nums[0] 到 nums[i] 中选出一个和恰好等于 j 的子序列。考虑 nums[i] ==选或不选==……这两个只要有一个成立，dfs(i,j) 就是 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选（前提 `j ≥ nums[i]`）→ `dfs(i-1, j-nums[i])`；不选 → `dfs(i-1, j)`',
              '递推时==在 f 最上边插入一排==当边界：`f[i+1][j]` 对应 `dfs(i, j)`',
              '`f[0][0] = True` 翻译自 `dfs(-1, 0)`，答案 `f[n][s/2]`'],
        after=[dict(heading='更省空间 / 更快的写法', lines=[
            '`f[i+1]` 只用到 `f[i]` → 一维数组，==j 要倒序枚举==，否则同一个数会被选两次',
            'j 从 `min(前缀和, s/2)` 开始倒序；`f[s]` 一旦为真就提前返回',
            'bitset：`f |= f << x`，把一整行压成一个二进制数',
        ])],
        summary=['时间 `O(n·s)`，`s ≤ 100 × 200 / 2 = 10⁴`',
                 '易错：先判 `s` 奇偶，`s //= 2` 之后再开数组',
                 '易错：`f` 有 `n+1` 行，`nums[i]` 对应第 `i+1` 行，nums 的下标不用偏移',
                 '`j >= x and ...` 写在前面：防止 `j - x` 变成负下标（Python 不会报错！）'],
    ),
)
