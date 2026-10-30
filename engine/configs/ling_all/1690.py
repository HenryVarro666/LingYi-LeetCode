ST = [5, 3, 1, 4, 2]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line') != 8:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i + 1, j), (i, j - 1)):
        return 'blue'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line') != 8:
        return '`f[i][j]` = 剩下 `stones[i..j]` 时，==先手得分 − 后手得分==的最大值'
    s, f = S['s'], S['f']
    a, b = s[j + 1] - s[i + 1], s[j] - s[i]
    return f'`max({a} − {f[i+1][j]}, {b} − {f[i][j-1]})` = =={f[i][j]}==　（拿左得 {a}，拿右得 {b}）'


CONFIG = dict(
    num=1690, title='石子游戏 VII', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='区间 DP · 先后手得分差 + 前缀和',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 1951'],
    code='''
class Solution:
    def stoneGameVII(self, stones: List[int]) -> int:
        n = len(stones)
        s = list(accumulate(stones, initial=0))
        f = [[0] * n for _ in range(n)]
        for i in range(n - 2, -1, -1):
            for j in range(i + 1, n):
                f[i][j] = max(s[j + 1] - s[i + 1] - f[i + 1][j], s[j] - s[i] - f[i][j - 1])
        return f[0][-1]
''',
    call=f'Solution().stoneGameVII({ST!r})',
    expect=6,
    skip=['for j in range'],
    views=[
        dict(type='array', var='stones', label='stones', h=210, cell=84, pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 它依赖的两格）', h=330, cell=76,
             rows=lambda S: list(range(len(ST))), cols=lambda S: list(range(len(ST))), color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s', 's', 'cyan'), ('f[i][j]', 'f[i][j]', 'green')],
    captions={
        'n = len': '`n = {n}`',
        's = list': '前缀和 `s`：区间和 `stones[a..b] = s[b+1] − s[a]`，一眼就能求出每次的得分',
        'f = [[0]': '`f[i][j]` 对应 `dfs(i, j)`；`f[i][i] = 0`：只剩一颗，移除后没分',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：要先有 `f[i+1][·]` → ==i 从大到小==枚举' if S.get('i') != B.get('i')
                                           else '所有区间都算完了'),
        'f[i][j] = max(': '拿左得 `s[{j+1}]−s[{i+1}]` = {s[j+1]-s[i+1]}，拿右得 `s[{j}]−s[{i}]` = {s[j]-s[i]}；各自减去对手在剩余区间的优势 → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[0][-1]': '整排石子的先后手得分差 `f[0][{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='每回合得分 = 剩余石子之和；每人都最大化「己 − 敌」',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['石子排成一排，Alice 先手，每回合移除最左或最右的一颗',
                 '得分 = 移除后==剩余石子的和==；Alice 想最大化分差，Bob 想最小化',
                 '示例：`[5,3,1,4,2]` → `6`'],
        quote='每个玩家都需要最大化自己的得分减去对手的得分。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j)`：剩 `stones[i..j]`，先手得分减后手得分的最大值',
              '移除左端得 `s[j+1]−s[i+1]`，然后角色互换：减去 `dfs(i+1,j)`',
              '记忆化搜索 1:1 翻译成递推：`i` 倒序、`j` 正序'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`；一维数组可优化到 `O(n)`',
                 '易错：循环 `i` 从 `n-2` 开始，`f[i][i] = 0` 已由初始化给出',
                 '得分是==移除后剩余==的和，所以拿左端用 `s[j+1]−s[i+1]`',
                 '题解还有会超时的纯递归、`@cache` 记忆化和一维优化写法',
                 '同类：486 预测赢家、877 石子游戏'],
    ),
)
