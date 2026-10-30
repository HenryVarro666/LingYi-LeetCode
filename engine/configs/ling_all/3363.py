FR = [[1, 2, 3, 4], [5, 6, 8, 7], [9, 10, 11, 12], [13, 14, 15, 16]]


def _fcell(S, i, j, v):
    if 'i' not in S or 'j' not in S or S.get('_line') not in (9,):
        return None
    ci, cj = S['i'], S['j']
    if (i, j) == (ci, cj):
        return 'yellow'
    if i == ci - 1 and cj - 1 <= j <= cj + 1:
        return 'blue'
    return None


def _gcell(S, i, j, v):
    if i == j:
        return 'green'
    if 'i' in S and 'j' in S and (i, j) == (S['i'], S['j']):
        return 'yellow'
    return None


CONFIG = dict(
    num=3363, title='最多可收集的水果数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='主对角线 + 两次网格 DP（转置复用）',
    tags=['灵神题单', '网格图 DP', '难度分 2200'],
    code='''
class Solution:
    def maxCollectedFruits(self, fruits: List[List[int]]) -> int:
        def dp(fruits: List[List[int]]) -> int:
            n = len(fruits)
            f = [[0] * (n + 1) for _ in range(n - 1)]
            f[0][n - 1] = fruits[0][-1]
            for i in range(1, n - 1):
                for j in range(max(n - 1 - i, i + 1), n):
                    f[i][j] = max(f[i - 1][j - 1], f[i - 1][j], f[i - 1][j + 1]) + fruits[i][j]
            return f[-1][n - 1]

        ans = sum(row[i] for i, row in enumerate(fruits))
        return ans + dp(fruits) + dp(list(zip(*fruits)))
''',
    call=f'Solution().maxCollectedFruits({FR})',
    expect=100,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=lambda S: (f"`f[{S['i']}][{S['j']}] = max(f[{S['i']-1}][{S['j']-1}], f[{S['i']-1}][{S['j']}], f[{S['i']-1}][{S['j']+1}]) + fruits[{S['i']}][{S['j']}]` = =={S['f'][S['i']][S['j']]}==" if S.get('_line') == 9 and 'j' in S and 'i' in S else '绿 = 主对角线（小朋友 1 独占）；其余两位各做一次 `dp`'), size=24, h=60),
        dict(type='grid', var='fruits', label='fruits（绿 = 主对角线；dp 里黄 = 当前格）', cell=90, h=330, color=_gcell),
        dict(type='table', var=lambda S: S['f'] if 'f' in S else None, label='f[i][j]：从 (0,n-1) 走到 (i,j) 的最多水果（不过主对角线）', cell=80, h=250, color=_fcell),
    ],
    watch=[('n', 'n'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'f = [[0]': '`f[i][j]`：小朋友 2 倒着走，==从右上角 (0,n-1) 到 (i,j)== 的最大水果数；多一列放右边界外的 0',
        'f[0][n - 1] = fruits[0][-1]': '起点 `(0,{n-1})`：`f[0][{n-1}] = {fruits[0][-1]}`',
        'for i in range': lambda S, B, r: (f'第 `{S.i}` 行的 `f` 都算完了，循环结束' if S.f[S.i][S.n - 1] else f'`i = {S.i}`：算第 `{S.i}` 行，要用到已算好的第 `{S.i - 1}` 行'),
        'f[i][j] = max': '上一行三个来源取最大，加上本格 `{fruits[i][j]}`：`f[{i}][{j}]` = =={f[i][j]}==',
        'return f[-1][n - 1]': '终点是 `(n-2, n-1)`，右下角由三人共享，不在 `f` 里：`{ret}`',
        'ans = sum': '小朋友 1 只有一条路：==主对角线==，`ans = {ans}`',
        'return ans + dp': lambda S, B, r: (f'主对角线 `{S.ans}` + 小朋友 2 + 小朋友 3（矩阵按对角线翻转后复用 `dp`）= =={r}==' if r is not None else '先算小朋友 2 的 `dp(fruits)`，再把矩阵转置算小朋友 3'),
    },
    cards=dict(
        one_liner='左上小朋友只能走主对角线，另两位各做一次网格 DP',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`n × n` 的房间，三个小朋友分别从 `(0,0)`、`(0,n-1)`、`(n-1,0)` 出发',
                 '各走 `n-1` 步到右下角，重复房间只能收一次',
                 '示例：`[[1,2,3,4],[5,6,8,7],[9,10,11,12],[13,14,15,16]]` → `100`'],
        quote='由于从左上角出发的小朋友只能移动 n-1 次，所以他的走法有且仅有一种：主对角线。……对于从左下角出发的小朋友，我们可以把矩阵按照主对角线翻转，就可以复用同一套代码逻辑了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['小朋友 1：恰好 `n-1` 步，只能沿主对角线',
              '小朋友 2、3 不能越过对角线（否则回不到右下角），所以和 1 不会抢同一格',
              '小朋友 3 把矩阵转置，就和小朋友 2 一模一样，复用 `dp`'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`；滚动数组可到 `O(n)`，原地改 `fruits` 可到 `O(1)`',
                 '`j` 的下界 `max(n-1-i, i+1)`：不能越过两条边界线',
                 '终点 `(n-1,n-1)` 在主对角线上，已被小朋友 1 收走，所以 `dp` 只走到 `(n-2,n-1)`',
                 '灵神还给了记忆化搜索写法（`@cache` + 出界返回 `-inf`），本视频演示 1:1 翻译后的递推'],
    ),
)
