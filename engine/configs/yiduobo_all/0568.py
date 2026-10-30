NAMES = ['城0', '城1', '城2']


def _fl(S, r, c, v):
    if S.get('j') is None or S.get('k') is None:
        return None
    if (r, c) == (S['k'], S['j']):
        return 'yellow'
    return None


def _dy(S, r, c, v):
    if S.get('j') is None or S.get('i') is None:
        return None
    return 'yellow' if (r, c) == (S['j'], S['i']) else None


def _cap_if(S, B, ret):
    k, j, i = S.k, S.j, S.i
    ok1 = S.flights[k][j] == 1
    if not ok1:
        return f'`flights[{k}][{j}] = 0`：城 {k} 飞不到城 {j} → 跳过'
    if S.g[k] is None:
        return f'能飞，但 `g[{k}] = None`：上一周到不了城 {k} → 跳过'
    cand = S.g[k] + S.days[j][i]
    if S.f[j] is None:
        return f'城 {k} → 城 {j} 可行，`f[{j}]` 还是空 → 用 `{S.g[k]} + {S.days[j][i]} = {cand}` 填入'
    if S.f[j] < cand:
        return f'`f[{j}] = {S.f[j]} < {cand}`（`g[{k}] + days[{j}][{i}]`）→ 更优，更新'
    return f'`f[{j}] = {S.f[j]} ≥ {cand}`：已有的更好 → 不更新'


CONFIG = dict(
    num=568, title='最大休假天数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按周 DP · 滚动数组',
    tags=[],
    code='''
class Solution(object):
    def maxVacationDays(self, flights, days):

        n = len(flights)
        for index in range(n):
            flights[index][index] = 1
        
        f = [None] * n
        f[0] = 0

        for i in range(len(days[0])):
            g = f[:]
            f = [None] * n
            for j in range(n):
                for k in range(n):
                    if flights[k][j] == 1 and g[k] is not None and (f[j] is None or f[j] < g[k] + days[j][i]):
                        f[j] = g[k] + days[j][i]

        return max(f)
''',
    call='Solution().maxVacationDays([[0,1,1],[1,0,1],[1,1,0]], [[1,3,1],[6,0,3],[3,3,3]])',
    expect=12,
    views=[
        dict(type='table', var='flights', rows=NAMES, cols=NAMES, color=_fl, label='flights[k][j]：能否从城 k 飞到城 j（对角线已置 1 = 留在原地）', h=190),
        dict(type='table', var='days', rows=NAMES, cols=['周0', '周1', '周2'], color=_dy, label='days[j][i]：在城 j 度过第 i 周的休假天数', h=190),
        dict(type='array', var='g', pointers={'k': 'pink'}, label='g：上一周各城市最大休假（None=到不了）', h=170),
        dict(type='array', var='f', pointers={'j': 'blue'}, label='f：这一周各城市最大休假', h=170),
    ],
    watch=['i', ('j', 'j', 'blue'), ('k', 'k', 'pink')],
    captions={
        'n = len': '`n = {n}` 个城市',
        'flights[index][index] = 1': '把对角线置 1：==留在原地也当成一次「飞行」==，这样两种情况合并',
        8: '`f[j]`：到达城 `j` 的最大休假天数，`None` 表示到不了',
        'f[0] = 0': '第 0 周开始前在城 0（出发城），休假 0 天：`f = {f}`',
        'for i in': lambda S, B, r: (f'开始第 `{S.i}` 周' if S.i != B.get('i') else '所有周都排完了'),
        'g = f[:]': '把上一周的结果存入 `g`：`g = {g}`',
        13: '新的一周先全置空，重新从 `g` 转移',
        'for j': lambda S, B, r: (f'目标城市 `j = {S.j}`' if S.j != B.get('j') else '三个目标城市都算完，进入下一周'),
        'for k': lambda S, B, r: (f'枚举出发城市 `k = {S.k}`' if S.k != B.get('k') else f'`j = {S.j}` 的所有出发城市都看过了'),
        'if flights[k][j]': _cap_if,
        'f[j] = g[k]': '`f[{j}] = g[{k}] + days[{j}][{i}]` = `{g[k]} + {days[j][i]}` = =={f[j]}==',
        'return max': '最后一周结束，在哪个城市都行，取最大：`max({f})` = =={ret}==',
    },
    cards=dict(
        one_liner='f[j] 记「这一周待在城 j」的最大休假天数，从上一周能飞来的城市转移',
        complexity='时间 `O(n²·K)`，空间 `O(n)`（`n` 城市数，`K` 周数）',
        problem=['`n` 个城市，从城 0 出发，每周一可以飞往能直达的城市，或留在原地',
                 '`flights[k][j] = 1` 表示可从 k 飞到 j；`days[j][i]` 是在城 j 度过第 i 周的休假天数',
                 '共 `K` 周，求最多休假天数；本视频：3 城市 3 周'],
        quote='方便起见，在这里可以将flighs[i][i]也置为1，这样一来就可以将情况1也归入情况2了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：第 `i` 周在城 `j` 的最大休假天数',
              '留在原地、飞过来本质都是 `f[k] + days[j][i]`，只要 `flights[k][j] == 1`',
              '`None` 表示到不了，必须先判断 `g[k] is not None` 才能相加'],
        summary=['时间 `O(n²·K)`，空间 `O(n)`',
                 '易错点：起点只有城 0，其余城市初始为 `None` 而不是 0',
                 '`None` 与 `< ` 不能直接比较，所以先判 `f[j] is None`',
                 '会直接修改传入的 `flights`（对角线置 1）；原文无需 Python 3 改动'],
    ),
)
