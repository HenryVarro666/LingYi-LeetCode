def _vals(S):
    i, j = S['i'], S['j']
    stay = S['f'][i + 1][j] + S['stayScore'][i][j]
    trav = [(fd + ts, d) for d, (fd, ts) in enumerate(zip(S['f'][i + 1], S['travelScore'][j]))]
    return stay, max(trav)


def _txt(S):
    if 'i' not in S or 'j' not in S or S.get('_line') != 6:
        return '`f[i][j]`：第 `i` 天到最后一天，从城市 `j` 出发能拿到的最多点数'
    i, j = S['i'], S['j']
    stay, (tv, d) = _vals(S)
    return (f'留在 `{j}`：`f[{i + 1}][{j}] + stay[{i}][{j}]` = {S["f"][i + 1][j]} + {S["stayScore"][i][j]} = {stay}　'
            f'去 `{d}`：`f[{i + 1}][{d}] + travel[{j}][{d}]` = {tv}')


def _color(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') != 6:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if r == i + 1:
        return 'blue' if c == j else 'cyan'
    return None


CONFIG = dict(
    num=3332, title='旅客可以得到的最多点数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='多维 DP（记忆化搜索 1:1 翻译成递推）',
    tags=['灵神题单·动态规划', '难度分 1828'],
    code='''
class Solution:
    def maxScore(self, n: int, k: int, stayScore: List[List[int]], travelScore: List[List[int]]) -> int:
        f = [[0] * n for _ in range(k + 1)]
        for i in range(k - 1, -1, -1):
            for j, ss in enumerate(stayScore[i]):
                f[i][j] = max(f[i + 1][j] + ss,
                              max(fd + ts for fd, ts in zip(f[i + 1], travelScore[j])))
        return max(f[0])
''',
    call='Solution().maxScore(3, 2, [[3, 4, 2], [2, 1, 2]], [[0, 2, 1], [2, 0, 4], [3, 2, 0]])',
    expect=8,
    skip=['for j, ss in enumerate', 'max(fd + ts for'],
    views=[
        dict(type='text', fn=_txt, size=22, h=90),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算；蓝 = 留在原地的来源，青 = 其余城市的来源）', h=310, cell=84,
             rows=lambda S: [f'第{k}天' if k < S['k'] else '结束' for k in range(S['k'] + 1)], cols=lambda S: [f'城市{c}' for c in range(S['n'])],
             color=_color),
        dict(type='table', var='travelScore', label='travelScore[j][d]：从 j 去 d 的点数', h=230, cell=64,
             rows=lambda S: [f'从{c}' for c in range(S['n'])], cols=lambda S: [f'去{c}' for c in range(S['n'])],
             color=lambda S, r, c, v: 'yellow' if r == S.get('j') and S.get('_line') == 6 else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ss', 'ss', 'yellow')],
    captions={
        'f = [[0] * n': '`f[i][j]` 对应 `dfs(i, j)`：第 `i` 天到第 `k-1` 天，从城市 `j` 出发的最多点数；`f[k][j] = 0`，旅程已经结束',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：算第 `{S.i}` 天要用第 `{S.i + 1}` 天的结果 → ==i 倒序==枚举' if S.get('i') != B.get('i') else '所有天都算完了'),
        'f[i][j] = max': lambda S, B, r: (lambda v: (f'城市 `{S.j}`：留在原地得 `{v[0]}`；去别的城市最好是去 `{v[1][1]}`，得 `{v[1][0]}`'
                                                     if S.f[S.i][S.j] == B.f[S.i][S.j] else
                                                     f'两者取大：`max({v[0]}, {v[1][0]})` → `f[{S.i}][{S.j}]` = =={S.f[S.i][S.j]}=='))(_vals(S)),
        'return max(f[0])': '起点城市可以任选：取 `f[0]` 的最大值 = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j]：第 i 天在城市 j，留下或去任意城市，取最大',
        complexity='时间 `O(kn^2)`，空间 `O(kn)`',
        problem=['`n` 座城市两两直达，旅客旅游==恰好 k 天==，起点任选',
                 '每天二选一：留在原地得 `stayScore[i][j]`，或去 `d` 得 `travelScore[j][d]`',
                 '示例：`n=3, k=2` → `8`'],
        quote='定义状态为 dfs(i,j)，表示第 i 天到第 k-1 天，从城市 j 开始旅游，可以获得的最多点数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['留在 `j`：`dfs(i+1, j) + stayScore[i][j]`；去 `d`：`dfs(i+1, d) + travelScore[j][d]`，取最大',
              '边界 `dfs(k, j) = 0`；答案是 `max(dfs(0, j))`（起点任选）',
              '记忆化搜索 1:1 翻译成递推：`i` 从大到小，`f[k][j] = 0`'],
        summary=['时间 `O(kn^2)`：状态 `O(kn)` × 转移 `O(n)`；空间 `O(kn)`',
                 '`travelScore[j][j] = 0`，所以“去自己”不会比“留下”更优，不必排除 `d = j`',
                 '灵神还给了记忆化搜索写法（`@cache`），这里演示 1:1 翻译后的递推',
                 '易错：`f` 要开 `k + 1` 行，且递推时 `i` 倒序'],
    ),
)
