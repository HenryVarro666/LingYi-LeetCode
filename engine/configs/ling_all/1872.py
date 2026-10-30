A = [5, 9, 1, -4, -5, -4, -2]


def _formula(S):
    if 'i' not in S:
        if 'f' in S:
            return f'起点：只剩最后一步，一次全拿走 `f = dfs(n-1) = S[n-1] = {S["f"]}`'
        return '`f` = 当前先手能拿到的最大分差；`s` = 前缀和 `S[i]`'
    i, s, f = S['i'], S['s'], S['f']
    return f'`max(f, s − f)` = `max({f}, {s} − {f})` = `max({f}, {s - f})`'


def _color(S, k, v):
    if 'i' not in S:
        return None
    if k <= S['i']:
        return 'blue'
    return None


CONFIG = dict(
    num=1872, title='石子游戏 VIII', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='博弈 DP · 前缀和 + 空间优化',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2440'],
    code='''
class Solution:
    def stoneGameVIII(self, stones: List[int]) -> int:
        f = s = sum(stones)
        for i in range(len(stones) - 2, 0, -1):
            s -= stones[i + 1]
            f = max(f, s - f)  # 改成 if 判断更快，见写法二
        return f
''',
    call=f'Solution().stoneGameVIII({A!r})',
    expect=8,
    views=[
        dict(type='text', fn=_formula, size=26, h=70),
        dict(type='array', var='stones', label='stones（蓝 = 前缀 [0, i]：被拿走后合成的新石子，值 s）', h=300, cell=90,
             pointers={'i': 'blue'}, color=_color,
             dim=lambda S, k, v: 'i' in S and k > S['i']),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'cyan'), ('f', 'f', 'green')],
    captions={
        'f = s = sum': '总和 `{s}`。先手一次拿光所有石子，分差就是 `f = dfs(n-1) = S[n-1] = {f}`',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：先手这轮要拿到下标 `i` 为止（至少拿 2 个，所以 `i ≥ 1`）' if S.get('i') != B.get('i') else '`i` 走到 1，所有状态都算完了'),
        's -= stones': '`s` 减去 `stones[{i+1}] = {stones[i+1]}`，变成前缀和 `S[{i}] = {s}`',
        'f = max': '`f` 是 `dfs(i+1)`：不拿到 `i` 就留给 `i+1`，值 `{B.f}`；拿到 `i` 得 `s - f` = `{s} − {B.f}` = {s - B.f}。取大 → `f = {f}`',
        'return f': '答案 `dfs(1)` = =={ret}==',
    },
    cards=dict(
        one_liner='先手得分 = 前缀和 − 后手的最优，每步只在“拿到 i”和“留给 i+1”里选',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每回合拿走最左边至少 2 个石子，得分加上它们的和，再放回一个值为这个和的新石子',
                 '只剩一个石子时结束；Alice 想最大化分差，Bob 想最小化',
                 '示例：`[-1,2,-3,4,-5]` → `5`；本视频：`[5,9,1,-4,-5,-4,-2]` → `8`'],
        quote='dfs(i) = max(S_i - dfs(i+1), dfs(i+1))。递归入口：dfs(1)。注意不能是 dfs(0)，请仔细看 dfs 的定义，这会产生负数下标。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新石子的值恰好是前缀和 `S_j`，所以每次拿的得分就是 `S_j`',
              '“拿到 `j`” 的转移是后缀最大值，把 `j=i` 提出来，剩下的恰好是 `dfs(i+1)`',
              '于是 `dfs(i)` 只依赖 `dfs(i+1)`：一个变量 `f` 就够了'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '起点是 `dfs(n-1) = S[n-1]`，不能当成 `dfs(n) = 0`：总和为负时会算错',
                 '循环到 `i = 1` 为止，答案是 `dfs(1)`，不是 `dfs(0)`',
                 '灵神还给了：记忆化搜索、`f` 数组递推、写法二（用 `if` 代替 `max`，更快）'],
    ),
)
