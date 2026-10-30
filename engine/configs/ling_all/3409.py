def _color(S, i, j, v):
    x, d = S.get('x'), S.get('d') if 'd' in S else S.get('j')
    jj = S.get('j')
    if x is None or jj is None or 'fx' not in S:
        return None
    r = i  # row = value
    if r == x and j == jj:
        return 'yellow'
    if j == jj and (r == x - jj or r == x + jj):
        return 'blue'
    return None


def _txt(S):
    if 'fx' not in S or 'j' not in S:
        return '`f[x][j]` = 以 x 结尾、最后两数之差 ==至少== 为 j 的最长子序列长度'
    x, j = S['x'], S['j']
    mx = len(S['f']) - 1
    cand = [v for v in (x - j, x + j) if 0 <= v <= mx]
    show = ' 或 '.join(f'`{v}`' for v in sorted(set(cand))) or '无（越界）'
    return f"`x = {x}`，`j = {j}`：倒数第二个数可以是 {show}（蓝格），取 `f[·][{j}] + 1` 最大，当前 `fx` = =={S['fx']}=="



CONFIG = dict(
    num=3409, title='最长相邻绝对差递减子序列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='f[x][j] 后缀最大值 · 值作为下标',
    tags=['灵神题单', '难度分 2500'],
    code='''
class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        mx = max(nums)
        max_d = mx - min(nums)
        f = [[0] * (max_d + 1) for _ in range(mx + 1)]
        for x in nums:
            fx = 1
            for j in range(max_d, -1, -1):
                if x - j >= 0:
                    fx = max(fx, f[x - j][j] + 1)
                if x + j <= mx:
                    fx = max(fx, f[x + j][j] + 1)
                f[x][j] = fx
        return max(map(max, f))
''',
    call='Solution().longestSubsequence([3,1,2,1])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=90),
        dict(type='table', var='f', label='f[x][j]：行 = 末尾值 x，列 = 最后两数之差至少为 j',
             rows=lambda S: [f'x={r}' for r in range(len(S['f']))],
             cols=lambda S: [f'j={c}' for c in range(len(S['f'][0]))],
             color=_color, h=380, cell=96),
        dict(type='text', h=100, size=26, fn=_txt),
    ],
    skip=['for j in range', 'if x - j', 'if x + j'],
    watch=[('x', 'x', 'pink'), ('j', 'j', 'blue'), ('fx', 'fx', 'green')],
    captions={
        'mx = max': '值域只有 `0..{mx}`，直接用「值」当下标，不再需要 `last` 数组',
        'max_d =': '差值最大为 `max_d = {max_d}`，`j` 只需枚举 `0..{max_d}`',
        'f = [[0]': '`f[x][j]` 表：行是末尾值，列是「最后两数之差至少为 j」',
        'fx = 1': '`x = {x}` 先单独成一个子序列：`fx = 1`',
        'for j in range': '`j` 倒序枚举：`f[x][j]` 要从 `f[x][j+1]`（差更大）转移，`fx` 就是在带着它',
        'if x - j >= 0': lambda S, B, r: f'倒数第二个数可以是 `x − j = {S.x - S.j}`：{"在范围内" if S.x - S.j >= 0 else "越界，不考虑"}',
        'fx = max(fx, f[x - j]': '接在 `{x-j}` 结尾（差 >= {j}）的子序列后：`fx = max({B.fx}, f[{x-j}][{j}] + 1)` = =={fx}==',
        'if x + j <= mx': lambda S, B, r: f'倒数第二个数也可以是 `x + j = {S.x + S.j}`：{"在范围内" if S.x + S.j <= S.mx else "越界，不考虑"}',
        'fx = max(fx, f[x + j]': '接在 `{x+j}` 结尾（差 >= {j}）的子序列后：`fx = max({B.fx}, f[{x+j}][{j}] + 1)` = =={fx}==',
        'f[x][j] = fx': '记下 `f[{x}][{j}] = {fx}`；`fx` 继续带到更小的 `j`（后缀最大值）',
        'return': '整张表的最大值就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='f[x][j] 记「最后一差至少为 j」，倒序枚举 j，后缀最大值自然带下来',
        complexity='时间 `O(nD)`，空间 `O(D^2)`，`D = max - min`',
        problem=['求 `nums` 的最长子序列，使相邻元素 ==绝对差非递增==',
                 '示例：`[6,5,3,4,2,1]` → `4`（6,4,2,1，差 2,2,1）',
                 '本视频：`[3,1,2,1]` → `4`（3,1,2,1，差 2,1,1）'],
        quote='定义 f[x][j] 表示以元素 x 结尾的、最后两个数之差至少为 j 的子序列的最长长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['倒数第二个数是 `x-j` 或 `x+j`，要求再前一差 `>= j`，用「至少 j」就不必枚举',
              '`j` 倒序，`fx` 一路带着 `f[x][j+1]`，相当于 `f[x][j] = max(f[x][j+1], …)`',
              '用「值」当下标代替 `last[]`：同值后出现的子序列只会更长'],
        summary=['时间 `O(nD)`，空间 `O(D^2)`',
                 '易错：`j = 0` 时 `x-j` 与 `x+j` 是同一格，所以用变量 `fx` 避免 `+1` 重复累加',
                 '`j` 必须倒序，否则拿不到「差更大」的转移',
                 '题解还给了优化前的写法（用 `last[x]` 记下标），这里演示优化后的写法'],
    ),
)
