def _rows(S):
    return [list(r) for r in S['a']] + [list(S['t'])]


def _color(S, i, j, v):
    a, t = S['a'], S['t']
    if i == len(a):
        return 'purple'
    if 'p' in S and S['p'] is a[i]:
        ok = all(a[i][k] <= t[k] for k in range(3))
        return ('green' if v == t[j] else 'blue') if ok else 'red'
    return None


CONFIG = dict(
    num=1899, title='合并若干三元组以形成目标三元组', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='筛掉超标三元组，看三个位置是否都能命中（Go 原文转写）',
    tags=['灵神题单', '贪心算法', '难度分 1636'],
    code='''
class Solution:
    def mergeTriplets(self, a: List[List[int]], t: List[int]) -> bool:
        found = [False] * 3
        for p in a:
            if p[0] <= t[0] and p[1] <= t[1] and p[2] <= t[2]:
                found[0] = found[0] or p[0] == t[0]
                found[1] = found[1] or p[1] == t[1]
                found[2] = found[2] or p[2] == t[2]
        return found[0] and found[1] and found[2]
''',
    call='Solution().mergeTriplets([[2,5,3],[1,8,4],[1,7,5]], [2,7,5])',
    expect=True,
    views=[
        dict(type='grid', var=_rows, label='a（红 = 超标不可用，绿 = 命中目标，紫 = 目标 t）', color=_color, rows=lambda S: [f'a[{i}]' for i in range(len(S['a']))] + ['t'], cols=['0', '1', '2'], h=330),
        dict(type='array', var='found', label='found（三个位置是否已命中）', color=lambda S, i, v: 'green' if v else None, h=170),
    ],
    watch=['found'],
    captions={
        'found = [False]': '`found[k]` 记录：目标的第 k 个数是否已经被某个可用三元组命中',
        'for p in a': '看下一个三元组 `p = {p}`',
        'if p[0] <= t[0]': lambda S, B, ret: (f'`p = {S.p}` 与目标 `{S.t}` 逐位比：' + ('三位都 `<=` → ==可用==，不会把任何位置抬过目标' if all(S.p[k] <= S.t[k] for k in range(3)) else '有一位超过目标 → ==不能用==，一用就再也降不回来')),
        'found[0] =': '第 0 位：`p[0] == t[0]` 吗？`found[0]` = {found[0]}',
        'found[1] =': '第 1 位：`p[1] == t[1]` 吗？`found[1]` = {found[1]}',
        'found[2] =': '第 2 位：`p[2] == t[2]` 吗？`found[2]` = {found[2]}',
        'return found[0]': '三个位置是否都命中：`{found}` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='先扔掉超标的三元组，剩下的看能否各位凑齐',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['三元组可以逐位取 `max` 合并，问能否得到目标三元组 `target`',
                 '示例：`[[2,5,3],[1,8,4],[1,7,5]]`，目标 `[2,7,5]` → `true`'],
        quote='若 (a_i,b_i,c_i) 各部分均不超过 (x,y,z)，则可以执行更新操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`max` 合并只会变大，所以任何一位超过目标的三元组都不能用',
              '剩下的三元组每位都不超过目标，合并后也不会超',
              '只要三个位置各有一个三元组恰好等于目标，合并出来就是目标'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错：必须先判断「三位都不超」再记录命中，否则会被超标三元组误导',
                 '三个位置可以由不同的三元组命中'],
    ),
)
