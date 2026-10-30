NUMS = [1, 5, 233, 7]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line') not in (9,):
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) == (i + 1, j) or (r, c) == (i, j - 1):
        return 'blue'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line') not in (9,):
        return '`f[i][j]` = 剩下 `nums[i..j]` 时，==先手得分 − 后手得分==的最大值'
    n = S['nums']
    return (f'`max({n[i]} − f[{i+1}][{j}], {n[j]} − f[{i}][{j-1}])` = '
            f'`max({n[i]} − {S["f"][i+1][j]}, {n[j]} − {S["f"][i][j-1]})`')


CONFIG = dict(
    num=486, title='预测赢家', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='博弈 DP · 得分之差（记忆化 1:1 翻译成递推）',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution:
    def predictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        f = [[0] * n for _ in range(n)]

        for i in range(n - 1, -1, -1):
            f[i][i] = nums[i]
            for j in range(i + 1, n):
                f[i][j] = max(nums[i] - f[i + 1][j], nums[j] - f[i][j - 1])

        return f[0][-1] >= 0
''',
    call=f'Solution().predictTheWinner({NUMS!r})',
    expect=True,
    skip=['for j in range'],
    views=[
        dict(type='array', var='nums', label='nums', h=210, cell=90, pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 它依赖的两格）', h=340, cell=80,
             rows=lambda S: [f'{k}' for k in range(len(NUMS))], cols=lambda S: [f'{k}' for k in range(len(NUMS))],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i][j]', 'f[i][j]', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'f = [[0] * n': '`f[i][j]` = 先手得分减后手得分的最大值；`i > j` 为空，值 0',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：要先有 `f[i+1][·]` → ==i 从大到小==枚举' if S.get('i') != B.get('i')
                                           else '所有区间都算完了'),
        'f[i][i] = nums[i]': '`f[{i}][{i}] = nums[{i}] = {nums[i]}`：只剩一个数，先手全拿，后手 0 分',
        'f[i][j] = max(': '拿左 `{nums[i]} − f[{i+1}][{j}]`，拿右 `{nums[j]} − f[{i}][{j-1}]`：对手在子区间的优势要减掉 → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[0][-1]': '`f[0][{n-1}] = {f[0][-1]}`：玩家 1 得分差 `>= 0`（平局也算赢）→ =={ret}==',
    },
    cards=dict(
        one_liner='只盯得分之差：每人都最大化「自己 − 对手」',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['玩家 1、2 轮流从数组==任意一端==取一个数，玩家 1 先手，各自加分',
                 '玩家 1 得分 `>=` 玩家 2（平局也算赢）就返回 `true`',
                 '示例：`[1,5,2]` → `false`；本视频：`[1,5,233,7]` → `true`'],
        quote='这意味着，我们只需关注得分之差 A−B 的值，而不是 A 和 B 具体是多少。维护一个值，比维护两个值更容易。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j)`：剩下 `nums[i..j]`，先手得分减后手得分的最大值',
              '先手取 `nums[i]` 后，对手成了先手：`nums[i] − dfs(i+1,j)`；取右端同理',
              '去掉递归的「递」，1:1 翻译成递推；`i` 倒序、`j` 正序'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`；一维数组可优化到 `O(n)`',
                 '易错：转移是 ==减==子问题（对手的优势），不是加',
                 '答案是 `f[0][n-1] >= 0`，平局先手也赢',
                 '题解还给了记忆化搜索（`@cache` 的 `dfs`）和一维空间优化写法',
                 '另外：`n` 为偶数时先手必胜（877 石子游戏），可直接返回 `true`'],
    ),
)
